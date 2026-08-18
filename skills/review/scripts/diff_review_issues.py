#!/usr/bin/env python3
"""Diff one provider's old and new issue bundles for a post-revision re-review.

Aligns issues by root_cause_key (falling back to title) and labels each prior
issue FULLY_ADDRESSED (gone), PARTIALLY_ADDRESSED (severity changed), or
NOT_ADDRESSED (same severity); issues only in the new bundle are NEW.

Run once per provider: Codex old vs Codex new, Hermes old vs Hermes new.
Never diff across providers; the two lanes stay independent.

Adapted from the paper-audit skill's diff_review_issues.py.

Usage:
    python3 diff_review_issues.py old-issues.json new-issues.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _by_key(issues: list[dict]) -> dict[str, dict]:
    return {str(i.get("root_cause_key") or i.get("title")): i for i in issues}


def diff_issues(previous: list[dict], current: list[dict]) -> dict:
    previous_by_key = _by_key(previous)
    current_by_key = _by_key(current)
    statuses: list[dict] = []

    for key, old_issue in previous_by_key.items():
        new_issue = current_by_key.get(key)
        if new_issue is None:
            status = "FULLY_ADDRESSED"
        elif old_issue.get("severity") == new_issue.get("severity"):
            status = "NOT_ADDRESSED"
        else:
            status = "PARTIALLY_ADDRESSED"
        statuses.append(
            {
                "root_cause_key": key,
                "title": old_issue.get("title"),
                "previous_severity": old_issue.get("severity"),
                "current_severity": new_issue.get("severity") if new_issue else None,
                "status": status,
            }
        )

    new_items = [i for key, i in current_by_key.items() if key not in previous_by_key]
    counts = {
        "FULLY_ADDRESSED": sum(1 for s in statuses if s["status"] == "FULLY_ADDRESSED"),
        "PARTIALLY_ADDRESSED": sum(1 for s in statuses if s["status"] == "PARTIALLY_ADDRESSED"),
        "NOT_ADDRESSED": sum(1 for s in statuses if s["status"] == "NOT_ADDRESSED"),
        "NEW": len(new_items),
    }
    return {"counts": counts, "statuses": statuses, "new_issues": new_items}


def _load(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON array")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("previous", help="Old issues JSON (one provider)")
    parser.add_argument("current", help="New issues JSON (same provider)")
    args = parser.parse_args()

    try:
        diff = diff_issues(_load(args.previous), _load(args.current))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 2
    print(json.dumps(diff, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
