#!/usr/bin/env bash
# End-to-end smoke test for superpower-writing scaffold (LaTeX).
# Exercises: dir init, dep check (permissive re: missing upstream), Zotero
# check, file-presence audit.

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT"
cd "$WORK"

pass() { echo "  PASS: $1"; }
fail() { echo "  FAIL: $1" >&2; exit 1; }

echo "== 1. init-writing-dir =="
bash "$PLUGIN_ROOT/scripts/init-writing-dir.sh"
[[ -f .writing/outline.md       ]] && pass "outline.md"         || fail "outline.md missing"
[[ -f .writing/metadata.yaml    ]] && pass "metadata.yaml"      || fail "metadata.yaml missing"
[[ -f .writing/progress.md      ]] && pass "progress.md"        || fail "progress.md missing"
[[ -f .writing/findings.md      ]] && pass "findings.md"        || fail "findings.md missing"
[[ -d .writing/manuscript       ]] && pass "manuscript/"        || fail "manuscript/ missing"
[[ -d .writing/claims           ]] && pass "claims/"            || fail "claims/ missing"
grep -q "zotero:" .writing/metadata.yaml && pass "metadata has zotero block" || fail "metadata missing zotero block"

echo "== 2. check-zotero.sh (no env) =="
(unset ZOTERO_API_KEY ZOTERO_LIBRARY_ID ZOTERO_LIBRARY_TYPE
 bash "$PLUGIN_ROOT/scripts/check-zotero.sh" &>/dev/null) \
  && fail "check-zotero should fail without creds" \
  || pass "check-zotero fails without creds as expected"

echo "== 4. plugin manifest sanity =="
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json'))" && pass "plugin.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/marketplace.json'))" && pass "marketplace.json valid"

echo "== 5. skill + command + agent presence =="
for name in outlining drafting claim-verification polish rebuttal idea literature citations scientific-visualization scientific-schematics domain-glossary wait-what; do
  [[ -f "$PLUGIN_ROOT/skills/$name/SKILL.md" ]] \
    && pass "skills/$name/SKILL.md" \
    || fail "missing skills/$name/SKILL.md"
done
for cmd in outline draft archive; do
  [[ -f "$PLUGIN_ROOT/commands/$cmd.md" ]] \
    && pass "commands/$cmd.md" \
    || fail "missing commands/$cmd.md"
done
for a in citation-auditor; do
  [[ -f "$PLUGIN_ROOT/agents/$a.md" ]] \
    && pass "agents/$a.md" \
    || fail "missing agents/$a.md"
done

python3 "$PLUGIN_ROOT/skills/scientific-schematics/scripts/imagegen.py" --help >/dev/null 2>&1 \
  && pass "scientific-schematics/scripts/imagegen.py --help" \
  || fail "scientific-schematics/scripts/imagegen.py missing or --help failed"

echo "== 5b. deletion audit =="
for gone in output-styles skills/submission skills/revision skills/peer-review skills/verification \
            skills/finishing-branch skills/lightweight-execute skills/subagent-driven \
            skills/team-driven commands/submit.md commands/revise.md agents/rebuttal-auditor.md \
            skills/collaborating-with-codex skills/collaborating-with-hermes \
            scripts/paired_consult.py scripts/consult_handoff.py \
            skills/_shared/core/dual-consult-protocol.md \
            skills/review; do
  [[ ! -e "$PLUGIN_ROOT/$gone" ]] \
    && pass "removed: $gone" \
    || fail "deleted component still present: $gone"
done

for file in \
  hooks/hooks.json \
  hooks/session-start.sh \
  LICENSE; do
  [[ -f "$PLUGIN_ROOT/$file" ]] && pass "$file" || fail "missing $file"
done

echo "== 6. section-standards presence =="
for std in 00_abstract 01_introduction 02_background 03_methods 04_results 05_discussion 06_conclusion 07_related_work 08_motivation; do
  [[ -f "$PLUGIN_ROOT/skills/drafting/references/section-standards/$std.md" ]] \
    && pass "section-standards/$std.md" \
    || fail "missing section-standards/$std.md"
done

echo "== eval case frontmatter parses as YAML =="
# An unquoted ": " inside a description turns the whole block into a nested
# mapping. The harness tolerates it, so nothing surfaced until a plain YAML
# reader hit two cases in one day, both written that morning.
python3 - "$PLUGIN_ROOT" <<'PY2'
import pathlib, re, sys, yaml
root = pathlib.Path(sys.argv[1]) / "evals"
n = 0
for case in sorted(p for p in root.iterdir() if p.is_dir() and p.name != "results"):
    # A case is either prompt.md + graders/*.md, or a single case.yaml carrying
    # the graders inline (needed when it wants a scaffold_script or add_dirs).
    if (case / "case.yaml").exists():
        try:
            cy = yaml.safe_load((case / "case.yaml").read_text(encoding="utf-8"))
        except Exception as e:
            sys.exit(f"  FAIL: evals/{case.name}/case.yaml is not valid YAML: {e}")
        if not (cy.get("execution") or {}).get("allowed_tools"):
            sys.exit(f"  FAIL: evals/{case.name}/case.yaml has no execution.allowed_tools")
        if not cy.get("graders"):
            sys.exit(f"  FAIL: evals/{case.name}/case.yaml has no graders")
        sc = (cy.get("context") or {}).get("scaffold_script")
        if sc and not (case / sc).exists():
            sys.exit(f"  FAIL: evals/{case.name}/case.yaml names scaffold_script {sc} which is missing")
        n += 1
        continue
    text = (case / "prompt.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"  FAIL: evals/{case.name}/prompt.md has no frontmatter")
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        sys.exit(f"  FAIL: evals/{case.name}/prompt.md frontmatter is not valid YAML: {e}")
    if not fm.get("allowed_tools"):
        sys.exit(f"  FAIL: evals/{case.name}/prompt.md has no allowed_tools")
    for g in sorted((case / "graders").glob("*.md")):
        gm = re.match(r"^---\n(.*?)\n---", g.read_text(encoding="utf-8"), re.S)
        if not gm:
            sys.exit(f"  FAIL: evals/{case.name}/graders/{g.name} has no frontmatter")
        try:
            yaml.safe_load(gm.group(1))
        except Exception as e:
            sys.exit(f"  FAIL: evals/{case.name}/graders/{g.name} frontmatter is not valid YAML: {e}")
    n += 1
print(f"  PASS: {n} eval cases, every prompt and grader frontmatter parses")
PY2

echo "== 7. skill linter (ratchet) =="
# lint_skills.py exits 0 when clean or every error is grandfathered in
# scripts/lint_skills_baseline.txt; exits 1 on a NEW violation. Run from the
# plugin root so it discovers skills/ and the baseline beside it.
(cd "$PLUGIN_ROOT" && python3 scripts/lint_skills.py) \
  && pass "lint_skills.py clean (no new violations)" \
  || fail "lint_skills.py reported NEW violation(s); run: python3 scripts/lint_skills.py"

echo "== 8. eval-harness fixture self-test =="
# run.py --check-fixtures lints every scenario then asserts each good/bad
# fixture grades to its expected status. No model call. Exits non-zero on any
# mismatch, missing fixture, or orphan.
(cd "$PLUGIN_ROOT" && python3 tests/eval-harness/run.py --check-fixtures) \
  && pass "eval-harness fixtures match expectations" \
  || fail "eval-harness --check-fixtures failed; run: python3 tests/eval-harness/run.py --check-fixtures"

echo ""
echo "ALL SMOKE TESTS PASSED"
