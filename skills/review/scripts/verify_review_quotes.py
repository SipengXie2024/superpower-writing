#!/usr/bin/env python3
"""Verify that every issue's quote exists verbatim in the manuscript source.

Reads one provider's issue bundle (a JSON array of issue objects, each with a
"quote" field), normalizes whitespace on both sides, and checks that each quote
occurs in at least one source file. LaTeX sources wrap lines freely, so exact
substring matching only works after collapsing all whitespace runs to single
spaces.

Run once per provider bundle; never merge bundles across providers.

Usage:
    python3 verify_review_quotes.py issues.json --source .writing/manuscript [--source main.tex] [--write-back]

Exit codes: 0 all quotes verified, 1 at least one unverified, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SOURCE_SUFFIXES = {".tex", ".bib", ".md", ".typ", ".txt"}


def normalize(text: str) -> str:
    return " ".join(text.split())


def collect_sources(paths: list[str]) -> dict[str, str]:
    """Map file path -> whitespace-normalized content for every source file."""
    sources: dict[str, str] = {}
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files = sorted(f for f in p.rglob("*") if f.suffix.lower() in SOURCE_SUFFIXES)
        elif p.is_file():
            files = [p]
        else:
            print(f"[ERROR] Source not found: {raw}", file=sys.stderr)
            raise SystemExit(2)
        for f in files:
            try:
                sources[str(f)] = normalize(f.read_text(encoding="utf-8", errors="replace"))
            except OSError as e:
                print(f"[WARN] Skipping unreadable {f}: {e}", file=sys.stderr)
    if not sources:
        print("[ERROR] No readable source files found", file=sys.stderr)
        raise SystemExit(2)
    return sources


def verify_issues(issues: list[dict], sources: dict[str, str]) -> list[dict]:
    updated: list[dict] = []
    for issue in issues:
        quote = normalize(str(issue.get("quote", "")))
        hit_file = None
        if quote:
            for path, text in sources.items():
                if quote in text:
                    hit_file = path
                    break
        patched = dict(issue)
        patched["quote_verified"] = hit_file is not None
        patched["quote_file"] = hit_file
        updated.append(patched)
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("issues_file", help="Path to one provider's issues JSON array")
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Manuscript file or directory (repeatable)",
    )
    parser.add_argument(
        "--write-back",
        action="store_true",
        help="Rewrite the issues file with quote_verified/quote_file annotations",
    )
    args = parser.parse_args()

    issues_path = Path(args.issues_file)
    try:
        issues = json.loads(issues_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ERROR] Cannot read issues file: {e}", file=sys.stderr)
        return 2
    if not isinstance(issues, list):
        print("[ERROR] Issues file must be a JSON array", file=sys.stderr)
        return 2

    sources = collect_sources(args.source)
    updated = verify_issues(issues, sources)

    if args.write_back:
        issues_path.write_text(
            json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    verified = sum(1 for i in updated if i["quote_verified"])
    for i in updated:
        if not i["quote_verified"]:
            label = i.get("id") or i.get("title") or "<untitled>"
            print(f"UNVERIFIED: {label}")
    print(f"Verified {verified}/{len(updated)} quotes")
    return 0 if verified == len(updated) else 1


if __name__ == "__main__":
    raise SystemExit(main())
