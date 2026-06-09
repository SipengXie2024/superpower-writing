#!/usr/bin/env python3
"""Map adjudicator per-point rulings to one advisory verdict.

The adjudicator thread emits per-point rulings only. This script owns the
count -> verdict mapping so the thread that wrote the rulings can never grade
its own outcome. The mapping is a pure function of (ruling, severity) tuples:
a script with no taste can compute it, so it is a Type-A check.

Input: a memo JSON on stdin or at a path argument, shaped as:

    {"points": [
        {"id": "P1",
         "ruling": "answered_by_current_text" | "partially" | "unresolved",
         "severity": "critical" | "major" | "minor"},
        ...
    ]}

`severity` is only consulted for points that are `partially` or `unresolved`;
for `answered_by_current_text` it is ignored and may be omitted.

Output (stdout): a JSON object with the computed verdict, the recommended
3-way action, the reason code, and the tallied counts. Exit code 0 on a clean
compute, 2 on malformed input. The verdict is ADVISORY: the caller surfaces it
to the user and never auto-mutates .writing/ state on its basis.
"""

import json
import sys

RULINGS = {"answered_by_current_text", "partially", "unresolved"}
SEVERITIES = {"critical", "major", "minor"}

# 3-way action vocabulary ported from r5 nature-skills paper-review.md.
ACTION_PASS = "pass"
ACTION_REVISION = "needs revision"
ACTION_EXPERIMENT = "needs NEW experiment"


def _load(argv):
    if len(argv) > 1 and argv[1] not in ("-", ""):
        with open(argv[1], "r", encoding="utf-8") as fh:
            return json.load(fh)
    return json.load(sys.stdin)


def _validate(points):
    if not isinstance(points, list) or not (3 <= len(points) <= 7):
        raise ValueError(
            f"expected 3-7 atomic points, got {len(points) if isinstance(points, list) else type(points).__name__}"
        )
    for p in points:
        ruling = p.get("ruling")
        if ruling not in RULINGS:
            raise ValueError(f"point {p.get('id', '?')}: bad ruling {ruling!r}")
        if ruling != "answered_by_current_text":
            sev = p.get("severity")
            if sev not in SEVERITIES:
                raise ValueError(
                    f"point {p.get('id', '?')}: {ruling} needs severity in {sorted(SEVERITIES)}, got {sev!r}"
                )


def compute(points):
    """Return (verdict, reason_code, action) from the rulings.

    Verdict ladder, most severe first; the first matching row wins:
      FAIL  unresolved_critical                  >=1 unresolved at critical
      FAIL  unresolved_needs_experiment          >=1 unresolved at major that is
                                                  an empirical/evidence gap (caller
                                                  sets needs_experiment: true)
      WARN  unresolved_major_or_minor            >=1 unresolved at major/minor
      WARN  partial_critical_or_repeated_major   >=1 partially@critical OR
                                                  >=2 partially@major
      PASS  defense_survives_minor_partial_only  0 unresolved, all partials minor
      PASS  defense_survives                     0 unresolved, 0 partial
    """
    unresolved = [p for p in points if p["ruling"] == "unresolved"]
    partial = [p for p in points if p["ruling"] == "partially"]

    unresolved_crit = [p for p in unresolved if p["severity"] == "critical"]
    unresolved_major = [p for p in unresolved if p["severity"] == "major"]
    unresolved_minor = [p for p in unresolved if p["severity"] == "minor"]
    partial_crit = [p for p in partial if p["severity"] == "critical"]
    partial_major = [p for p in partial if p["severity"] == "major"]

    needs_experiment = any(
        p.get("needs_experiment") is True for p in unresolved
    )

    if unresolved_crit:
        return "FAIL", "unresolved_critical", ACTION_EXPERIMENT if any(
            p.get("needs_experiment") is True for p in unresolved_crit
        ) else ACTION_REVISION
    if needs_experiment:
        return "FAIL", "unresolved_needs_experiment", ACTION_EXPERIMENT
    if unresolved_major or unresolved_minor:
        return "WARN", "unresolved_major_or_minor", ACTION_REVISION
    if partial_crit or len(partial_major) >= 2:
        return "WARN", "partial_critical_or_repeated_major", ACTION_REVISION
    if partial:
        return "PASS", "defense_survives_minor_partial_only", ACTION_PASS
    return "PASS", "defense_survives", ACTION_PASS


def main(argv):
    try:
        memo = _load(argv)
        points = memo if isinstance(memo, list) else memo.get("points")
        _validate(points)
        verdict, reason, action = compute(points)
    except (ValueError, KeyError, AttributeError, json.JSONDecodeError) as exc:
        json.dump({"error": str(exc)}, sys.stdout)
        sys.stdout.write("\n")
        return 2

    counts = {
        "answered_by_current_text": sum(
            1 for p in points if p["ruling"] == "answered_by_current_text"
        ),
        "partially": sum(1 for p in points if p["ruling"] == "partially"),
        "unresolved": sum(1 for p in points if p["ruling"] == "unresolved"),
    }
    json.dump(
        {
            "verdict": verdict,
            "reason_code": reason,
            "recommended_action": action,
            "counts": counts,
            "total_points": len(points),
        },
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
