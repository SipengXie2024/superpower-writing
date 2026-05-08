#!/usr/bin/env bash
# Validate a .bid/ workspace for cn-bid-writing.

set -euo pipefail

TARGET="${1:-.bid}"

failures=0
fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}
pass() {
  echo "PASS: $1"
}

[[ -d "$TARGET" ]] || { echo "FAIL: $TARGET missing" >&2; exit 1; }
[[ -f "$TARGET/metadata.yaml" ]] && pass "metadata.yaml exists" || fail "metadata.yaml missing"
[[ -f "$TARGET/outline.yaml" ]] && pass "outline.yaml exists" || fail "outline.yaml missing"
[[ -d "$TARGET/chapters" ]] && pass "chapters exists" || fail "chapters directory missing"

if [[ -f "$TARGET/outline.yaml" ]]; then
  python3 - "$TARGET" <<'PY' || failures=$((failures + 1))
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML unavailable: {exc}", file=sys.stderr)
    sys.exit(1)

target = Path(sys.argv[1])
try:
    data = yaml.safe_load((target / "outline.yaml").read_text(encoding="utf-8")) or {}
except Exception as exc:
    print(f"FAIL: outline.yaml cannot be parsed: {exc}", file=sys.stderr)
    sys.exit(1)

sections = data.get("sections") or []
if not isinstance(sections, list):
    print("FAIL: outline.yaml sections must be a list", file=sys.stderr)
    sys.exit(1)
if not sections:
    print("FAIL: outline.yaml has no sections", file=sys.stderr)
    sys.exit(1)


def normalized(value):
    return re.sub(r"\s+", "", str(value or ""))


def has_nearby_caption(lines, index, pattern):
    start = max(0, index - 2)
    end = min(len(lines), index + 3)
    return any(re.search(pattern, lines[i]) for i in range(start, end) if i != index)


def looks_like_table_row(line):
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def validate_markdown_format(file_name, text):
    ok = True
    lines = text.splitlines()
    for index, line in enumerate(lines):
        for alt in re.findall(r"!\[([^\]]*)\]\([^)]*\)", line):
            if not alt.strip():
                print(f"FAIL: chapter {file_name} image missing alt text", file=sys.stderr)
                ok = False
            if not has_nearby_caption(lines, index, r"图\s*\d+"):
                print(f"FAIL: chapter {file_name} missing figure caption", file=sys.stderr)
                ok = False
    for index, line in enumerate(lines):
        if looks_like_table_row(line) and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}:?", lines[index + 1]):
            if not has_nearby_caption(lines, index, r"表\s*\d+"):
                print(f"FAIL: chapter {file_name} missing table caption", file=sys.stderr)
                ok = False
    return ok


parent_ids = {str(section.get("parent_id")).strip() for section in sections if section.get("parent_id") is not None}
leaf_count = 0
failed = False
for section in sections:
    sid = str(section.get("id") or "").strip()
    title = str(section.get("title") or "").strip()
    if not sid or not title:
        print(f"FAIL: section missing id/title: {section!r}", file=sys.stderr)
        failed = True
        continue
    if sid in parent_ids:
        print(f"PASS: parent section {sid} has children")
        continue
    leaf_count += 1
    file_name = str(section.get("file") or "").strip()
    if not file_name:
        print(f"FAIL: leaf section {sid} missing file", file=sys.stderr)
        failed = True
        continue

    for field in ("functional_indicators", "performance_indicators"):
        value = section.get(field)
        if value is None:
            print(f"FAIL: leaf section {sid} missing {field}", file=sys.stderr)
            failed = True
        elif not isinstance(value, list):
            print(f"FAIL: leaf section {sid} {field} must be a list", file=sys.stderr)
            failed = True

    format_requirements = section.get("format_requirements") or {}
    if format_requirements and not isinstance(format_requirements, dict):
        print(f"FAIL: leaf section {sid} format_requirements must be a mapping", file=sys.stderr)
        failed = True
        format_requirements = {}
    if format_requirements and not str(section.get("docx_template") or "").strip():
        print(f"FAIL: leaf section {sid} missing docx_template", file=sys.stderr)
        failed = True

    chapter = target / file_name
    if not chapter.exists():
        print(f"FAIL: missing chapter {file_name} for section {sid}", file=sys.stderr)
        failed = True
        continue
    text = chapter.read_text(encoding="utf-8")
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    body = re.sub(r"[#>*_`\-\s]", "", body)
    count = len(body)
    min_chars = int(section.get("min_chars") or 0)
    if count < min_chars:
        print(f"FAIL: chapter {file_name} below min_chars ({count} < {min_chars})", file=sys.stderr)
        failed = True
    else:
        print(f"PASS: chapter {file_name} chars {count} >= {min_chars}")

    normalized_text = normalized(text)
    for field in ("functional_indicators", "performance_indicators"):
        indicators = section.get(field)
        if isinstance(indicators, list):
            for item in indicators:
                if str(item or "").strip() and normalized(item) not in normalized_text:
                    print(f"FAIL: chapter {file_name} missing {field}: {item}", file=sys.stderr)
                    failed = True
    if format_requirements and not validate_markdown_format(file_name, text):
        failed = True

if leaf_count == 0:
    print("FAIL: outline.yaml has no leaf sections", file=sys.stderr)
    failed = True

sys.exit(1 if failed else 0)
PY
fi

if command -v pandoc >/dev/null 2>&1; then
  pass "pandoc available"
else
  echo "WARN: pandoc not found; docx export will only build combined markdown" >&2
fi

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi
