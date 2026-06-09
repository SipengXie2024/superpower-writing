#!/usr/bin/env python3
"""Prose-output eval harness for superpower-writing skills.

Skills in this plugin are prompt context, not executable code, so there is no
function to unit-test. What is testable is whether an agent that loaded a skill
produced output with the right properties: it refuses to fabricate a DOI, it
marks an unconfirmed number [UNVERIFIED], it stops and asks for figure data
instead of synthesizing measurements. Each such property is a rubric item, and
each scenario is a realistic user request plus a rubric.

Two layers, deliberately separated:

  full skill eval is agent-run. An agent produces output for a scenario prompt,
  the reply is saved as candidates/<run>/<id>.{md,txt}, and run.py --grade
  scores it. This needs a live model.

  --check-fixtures is regression-testing for the harness logic itself. It runs
  every scenario against its committed good/bad fixtures and asserts the
  expected pass/fail, with no model call at all. tests/smoke.sh calls this.

Asymmetry to keep in mind: failing a required check proves wrongness; passing
proves only that the output did not trip a known wire. Green machine-checks are
"did not trip a known wire", not "certified correct"; the manual rubric items
exist for substance a regex cannot judge.

Stdlib only. No pip installs. JSON scenarios (tomllib is 3.11+ only, so JSON
keeps the harness version-safe across the Python versions a contributor may run).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent.parent
SCENARIO_DIR = HERE / "scenarios"
FIXTURE_DIR = HERE / "fixtures"
EXPECTED_FILE = FIXTURE_DIR / "expected.json"

AUTO_CHECKS = {
    "regex_any",      # PASS if at least one pattern matches
    "regex_all",      # PASS if every pattern matches
    "regex_none",     # PASS if no pattern matches (forbidden content absent)
    "word_count_max",  # PASS if word/char count of section-or-doc <= target
    "word_count_min",  # PASS if word/char count of section-or-doc >= target
}
MANUAL_CHECK = "manual"
ALL_CHECKS = AUTO_CHECKS | {MANUAL_CHECK}

SEVERITIES = {"critical", "high", "medium", "low"}

# Statuses a fixture is allowed to assert in fixtures/expected.json.
EXPECTED_STATUSES = {"pass", "needs-manual", "fail-required", "partial"}


# --------------------------------------------------------------------------- #
# Check primitives
# --------------------------------------------------------------------------- #
@dataclass
class CheckResult:
    item_id: str
    status: str            # "pass" | "fail" | "manual" | "error"
    weight: float
    required: bool
    detail: str = ""
    evidence: list[str] = field(default_factory=list)


def _slice_section(text: str, section: str | None) -> str:
    """Return the substring captured by ``section`` (a regex; group 1 if it has
    groups, else the whole match). Falls back to the full text when ``section``
    is empty or does not match, so a check is never silently skipped.
    """
    if not section:
        return text
    m = re.search(section, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if not m:
        return text
    return m.group(1) if m.groups() else m.group(0)


def _count_units(text: str, unit: str) -> int:
    if unit == "chars":
        return len(re.sub(r"\s+", "", text))
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text)
    return len(words)


def run_check(item: dict[str, Any], candidate: str) -> CheckResult:
    """Evaluate one rubric item against candidate output text."""
    item_id = str(item.get("id", "<unnamed>"))
    weight = float(item.get("weight", 1))
    required = bool(item.get("required", False))
    check = item.get("check", MANUAL_CHECK)

    def ok(detail: str = "", evidence: list[str] | None = None) -> CheckResult:
        return CheckResult(item_id, "pass", weight, required, detail, evidence or [])

    def bad(detail: str, evidence: list[str] | None = None) -> CheckResult:
        return CheckResult(item_id, "fail", weight, required, detail, evidence or [])

    if check == MANUAL_CHECK:
        return CheckResult(item_id, "manual", weight, required,
                           item.get("guidance", "Requires human/LLM judgement."))

    if check not in AUTO_CHECKS:
        return CheckResult(item_id, "error", weight, required,
                           f"Unknown check type: {check!r}")

    text = _slice_section(candidate, item.get("section"))

    try:
        if check in {"regex_any", "regex_all", "regex_none"}:
            patterns = item.get("patterns") or (
                [item["pattern"]] if "pattern" in item else [])
            if not patterns:
                return CheckResult(item_id, "error", weight, required,
                                   "No patterns given.")
            hits = [p for p in patterns
                    if re.search(p, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)]
            if check == "regex_any":
                return ok(f"matched {len(hits)}/{len(patterns)}", hits[:3]) if hits \
                    else bad("no required pattern matched", patterns[:3])
            if check == "regex_all":
                missing = [p for p in patterns if p not in hits]
                return ok("all patterns matched") if not missing \
                    else bad(f"missing {len(missing)} pattern(s)", missing[:3])
            # regex_none
            return bad("forbidden pattern present", hits[:3]) if hits \
                else ok("no forbidden pattern present")

        if check in {"word_count_max", "word_count_min"}:
            unit = item.get("unit", "words")
            n = _count_units(text, unit)
            target = float(item["target"])
            if check == "word_count_max":
                return ok(f"{n} {unit} <= {target:.0f}") if n <= target \
                    else bad(f"{n} {unit} > {target:.0f} limit")
            return ok(f"{n} {unit} >= {target:.0f}") if n >= target \
                else bad(f"{n} {unit} < {target:.0f} minimum")

    except KeyError as exc:
        return CheckResult(item_id, "error", weight, required, f"missing field {exc}")
    except re.error as exc:
        return CheckResult(item_id, "error", weight, required, f"bad regex: {exc}")

    return CheckResult(item_id, "error", weight, required, "unreachable")


# --------------------------------------------------------------------------- #
# Scenario loading + validation
# --------------------------------------------------------------------------- #
class ScenarioError(Exception):
    pass


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PLUGIN_ROOT))
    except ValueError:
        return str(path)


def load_scenarios() -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for path in sorted(SCENARIO_DIR.glob("*.json")):
        try:
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ScenarioError(f"{rel(path)}: invalid JSON: {exc}") from exc
        data["_path"] = path
        if data.get("id") != path.stem:
            raise ScenarioError(
                f"{rel(path)}: id {data.get('id')!r} must equal file stem "
                f"{path.stem!r}")
        scenarios.append(data)
    return scenarios


def _validate_regex(sid: str, rid: str, pattern: Any) -> list[str]:
    if not isinstance(pattern, str):
        return [f"{sid}/{rid}: pattern must be a string, got {type(pattern).__name__}"]
    try:
        re.compile(pattern)
    except re.error as exc:
        return [f"{sid}/{rid}: bad regex {pattern!r}: {exc}"]
    return []


def validate_scenario(s: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    sid = s.get("id", "<no-id>")
    for field_name in ("id", "skill", "title", "category", "severity", "prompt", "rubric"):
        if field_name not in s:
            problems.append(f"{sid}: missing required field '{field_name}'")
    if not isinstance(sid, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(sid)):
        problems.append(f"{sid}: id must be lowercase-kebab")
    if s.get("severity") not in SEVERITIES:
        problems.append(f"{sid}: severity must be one of {sorted(SEVERITIES)}")

    skill = s.get("skill")
    if isinstance(skill, str):
        if skill.startswith("/") or ".." in Path(skill).parts:
            problems.append(f"{sid}: skill path must be repo-relative without '..'")
        elif not (PLUGIN_ROOT / skill).exists():
            problems.append(f"{sid}: skill path '{skill}' does not exist")

    rubric = s.get("rubric")
    if not isinstance(rubric, list) or not rubric:
        problems.append(f"{sid}: rubric must be a non-empty array")
        return problems

    seen_ids: set[str] = set()
    has_required = False
    for item in rubric:
        if not isinstance(item, dict):
            problems.append(f"{sid}: each rubric item must be an object")
            continue
        rid = item.get("id", "<no-id>")
        if rid in seen_ids:
            problems.append(f"{sid}: duplicate rubric id '{rid}'")
        seen_ids.add(rid)
        check = item.get("check", MANUAL_CHECK)
        if check not in ALL_CHECKS:
            problems.append(f"{sid}/{rid}: unknown check '{check}'")
        if "description" not in item:
            problems.append(f"{sid}/{rid}: missing description")
        if item.get("required") is True:
            has_required = True
        if "required" in item and not isinstance(item["required"], bool):
            problems.append(f"{sid}/{rid}: required must be boolean")
        if "section" in item:
            problems += _validate_regex(sid, rid, item["section"])
        if check in {"regex_any", "regex_all", "regex_none"}:
            pats = item.get("patterns") or (
                [item["pattern"]] if "pattern" in item else [])
            if not pats:
                problems.append(f"{sid}/{rid}: {check} needs patterns")
            for p in pats:
                problems += _validate_regex(sid, rid, p)
        if check in {"word_count_max", "word_count_min"} and "target" not in item:
            problems.append(f"{sid}/{rid}: {check} needs a target")
        if check == MANUAL_CHECK and "guidance" not in item:
            problems.append(f"{sid}/{rid}: manual check should carry guidance")
    if not has_required:
        problems.append(
            f"{sid}: scenario has no required rubric item; a scenario with no "
            f"gating wire can never fail-required")
    return problems


# --------------------------------------------------------------------------- #
# Grading
# --------------------------------------------------------------------------- #
def grade_text(s: dict[str, Any], text: str) -> dict[str, Any]:
    """Score one candidate text against a scenario's rubric.

    Status precedence: a required failure wins (fail-required); else any open
    machine failure or error is partial; else any open manual item is
    needs-manual; else pass. A scenario carrying manual items can never reach
    plain ``pass`` from machine checks alone, which is the point.
    """
    items_out = []
    earned = possible = 0.0
    required_failed: list[str] = []
    manual_items: list[str] = []
    errored: list[str] = []
    for item in s["rubric"]:
        res = run_check(item, text)
        items_out.append({
            "id": res.item_id, "status": res.status, "weight": res.weight,
            "required": res.required, "detail": res.detail, "evidence": res.evidence,
        })
        if res.status in {"pass", "fail"}:
            possible += res.weight
            if res.status == "pass":
                earned += res.weight
            elif res.required:
                required_failed.append(res.item_id)
        elif res.status == "manual":
            manual_items.append(res.item_id)
        elif res.status == "error":
            errored.append(res.item_id)
    auto_score = (earned / possible) if possible else None
    if required_failed:
        status = "fail-required"
    elif errored:
        status = "error"
    elif auto_score is not None and auto_score < 1.0:
        status = "partial"
    elif manual_items:
        status = "needs-manual"
    else:
        status = "pass"
    return {
        "id": s["id"], "skill": s["skill"], "category": s.get("category"),
        "status": status, "auto_score": auto_score, "earned": earned,
        "possible": possible, "required_failed": required_failed,
        "manual_items": manual_items, "errored": errored, "items": items_out,
    }


def find_candidate(candidate_dir: Path, sid: str) -> Path | None:
    for ext in (".md", ".txt"):
        p = candidate_dir / f"{sid}{ext}"
        if p.exists():
            return p
    return None


def grade_candidate(s: dict[str, Any], candidate_dir: Path) -> dict[str, Any]:
    cand = find_candidate(candidate_dir, s["id"])
    if cand is None:
        return {"id": s["id"], "skill": s["skill"],
                "category": s.get("category"), "status": "no-candidate",
                "items": [], "auto_score": None}
    text = cand.read_text(encoding="utf-8", errors="replace")
    out = grade_text(s, text)
    out["candidate"] = rel(cand)
    return out


# --------------------------------------------------------------------------- #
# Fixture self-test
# --------------------------------------------------------------------------- #
def load_expected() -> dict[str, str]:
    if not EXPECTED_FILE.exists():
        raise ScenarioError(f"missing fixture manifest {rel(EXPECTED_FILE)}")
    with EXPECTED_FILE.open(encoding="utf-8") as fh:
        data = json.load(fh)
    for key, want in data.items():
        if want not in EXPECTED_STATUSES:
            raise ScenarioError(
                f"{rel(EXPECTED_FILE)}: key '{key}' expects unknown status "
                f"'{want}' (allowed: {sorted(EXPECTED_STATUSES)})")
    return data


def check_fixtures(scenarios: list[dict[str, Any]]) -> int:
    """Run every scenario against its good/bad fixtures and assert the expected
    status. Exit non-zero on any mismatch, missing fixture, or orphan. This is
    the harness's own regression test; no model call happens here.
    """
    expected = load_expected()
    by_id = {s["id"]: s for s in scenarios}
    failures: list[str] = []
    checked = 0

    # Every scenario must have a good and a bad fixture declared and on disk.
    for sid in by_id:
        for kind in ("good", "bad"):
            key = f"{sid}.{kind}"
            if key not in expected:
                failures.append(f"{key}: no expectation in {rel(EXPECTED_FILE)}")
                continue
            fixture = find_candidate(FIXTURE_DIR, key)
            if fixture is None:
                failures.append(
                    f"{key}: expected fixture file "
                    f"{rel(FIXTURE_DIR / (key + '.md'))} not found")
                continue
            text = fixture.read_text(encoding="utf-8", errors="replace")
            got = grade_text(by_id[sid], text)["status"]
            want = expected[key]
            checked += 1
            mark = "ok" if got == want else "MISMATCH"
            line = f"  [{mark}] {key}: expected {want}, got {got}"
            print(line)
            if got != want:
                failures.append(
                    f"{key}: expected {want}, got {got}")
            # A good fixture must never trip a required wire; a bad one must.
            if kind == "good" and got == "fail-required":
                failures.append(f"{key}: good fixture tripped a required check")
            if kind == "bad" and got != "fail-required" and want == "fail-required":
                failures.append(f"{key}: bad fixture did not trip a required check")

    # Orphan fixtures: an expected.json key or *.md/*.txt with no scenario.
    valid_keys = {f"{sid}.{k}" for sid in by_id for k in ("good", "bad")}
    for key in expected:
        if key not in valid_keys:
            failures.append(f"{key}: expectation has no matching scenario")
    for pat in ("*.md", "*.txt"):
        for path in FIXTURE_DIR.glob(pat):
            if path.stem not in valid_keys:
                failures.append(f"{rel(path)}: orphan fixture (no scenario.kind)")

    print()
    if failures:
        print(f"FAIL: {len(failures)} fixture mismatch(es):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"OK: {checked} fixtures matched expectations "
          f"across {len(by_id)} scenarios.")
    return 0


# --------------------------------------------------------------------------- #
# Reporting helpers
# --------------------------------------------------------------------------- #
def cmd_list(scenarios: list[dict[str, Any]]) -> int:
    for s in scenarios:
        n_req = sum(1 for i in s["rubric"] if i.get("required"))
        n_manual = sum(1 for i in s["rubric"]
                       if i.get("check", MANUAL_CHECK) == MANUAL_CHECK)
        print(f"{s['id']:<34} [{s.get('severity','?'):<8}] "
              f"{s.get('category','?'):<20} "
              f"{len(s['rubric'])} items "
              f"({n_req} required, {n_manual} manual) -> {s['skill']}")
    print(f"\n{len(scenarios)} scenarios.")
    return 0


def print_grade(g: dict[str, Any]) -> None:
    head = f"{g['id']:<34} {g['status']}"
    if g.get("auto_score") is not None:
        head += f"  (machine {g['earned']:.0f}/{g['possible']:.0f})"
    print(head)
    for item in g.get("items", []):
        flag = "R" if item["required"] else " "
        line = f"    [{flag}] {item['status']:<7} {item['id']}"
        if item.get("detail"):
            line += f" - {item['detail']}"
        print(line)
    if g.get("manual_items"):
        print(f"    manual items pending: {', '.join(g['manual_items'])}")


def cmd_grade(scenarios: list[dict[str, Any]], candidate_dir: Path) -> int:
    if not candidate_dir.is_dir():
        print(f"error: {candidate_dir} is not a directory", file=sys.stderr)
        return 2
    any_required_fail = False
    for s in scenarios:
        g = grade_candidate(s, candidate_dir)
        print_grade(g)
        if g["status"] == "fail-required":
            any_required_fail = True
    print()
    print("Reminder: failing a required check proves wrongness; passing proves "
          "only it did not trip a known wire.")
    return 1 if any_required_fail else 0


def cmd_lint(scenarios: list[dict[str, Any]]) -> int:
    problems: list[str] = []
    for s in scenarios:
        problems += validate_scenario(s)
    if problems:
        print(f"{len(problems)} scenario problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"OK: {len(scenarios)} scenarios valid.")
    return 0


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="superpower-writing prose-output eval harness")
    ap.add_argument("--list", action="store_true",
                    help="list scenarios and exit")
    ap.add_argument("--grade", metavar="DIR",
                    help="score candidate agent outputs in DIR (DIR/<id>.md)")
    ap.add_argument("--check-fixtures", action="store_true",
                    help="run every scenario against its fixtures and assert "
                         "expected pass/fail; non-zero exit on mismatch")
    args = ap.parse_args(argv)

    try:
        scenarios = load_scenarios()
    except ScenarioError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not scenarios:
        print(f"error: no scenarios found under {rel(SCENARIO_DIR)}",
              file=sys.stderr)
        return 2

    # Always lint first so a malformed scenario fails loudly before anything.
    lint_problems: list[str] = []
    for s in scenarios:
        lint_problems += validate_scenario(s)
    if lint_problems:
        print(f"{len(lint_problems)} scenario problem(s):", file=sys.stderr)
        for p in lint_problems:
            print(f"  - {p}", file=sys.stderr)
        return 2

    if args.check_fixtures:
        return check_fixtures(scenarios)
    if args.list:
        return cmd_list(scenarios)
    if args.grade:
        return cmd_grade(scenarios, Path(args.grade))
    # Default: lint report (already passed above).
    return cmd_lint(scenarios)


if __name__ == "__main__":
    raise SystemExit(main())
