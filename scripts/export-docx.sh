#!/usr/bin/env bash
# Build combined markdown and, when pandoc is available, docx output.

set -euo pipefail

TARGET="${1:-.bid}"
OUT_DIR="$TARGET/export"
COMBINED="$OUT_DIR/combined.md"

mkdir -p "$OUT_DIR"

if [[ ! -f "$TARGET/outline.yaml" ]]; then
  echo "outline.yaml missing" >&2
  exit 1
fi

python3 - "$TARGET" "$COMBINED" <<'PY'
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:
    print(f"PyYAML unavailable: {exc}", file=sys.stderr)
    sys.exit(1)

target = Path(sys.argv[1])
combined = Path(sys.argv[2])
data = yaml.safe_load((target / "outline.yaml").read_text(encoding="utf-8")) or {}
sections = data.get("sections") or []
if not sections:
    print("outline.yaml has no sections", file=sys.stderr)
    sys.exit(1)

parent_ids = {str(section.get("parent_id")).strip() for section in sections if section.get("parent_id") is not None}
parts = []
for section in sections:
    sid = str(section.get("id") or "").strip()
    if sid in parent_ids:
        continue
    file_name = section.get("file")
    title = section.get("title")
    level = int(section.get("level") or 1)
    if not file_name or not title:
        print(f"leaf section missing file/title: {section!r}", file=sys.stderr)
        sys.exit(1)
    chapter = target / file_name
    if not chapter.exists():
        print(f"missing chapter {file_name}", file=sys.stderr)
        sys.exit(1)
    text = chapter.read_text(encoding="utf-8").strip()
    heading = "#" * max(1, min(level, 6))
    parts.append(f"{heading} {title}\n\n{text}\n")

if not parts:
    print("outline.yaml has no leaf sections", file=sys.stderr)
    sys.exit(1)

combined.write_text("\n\n".join(parts), encoding="utf-8")
print(f"Generated {combined}")
PY

export_info=$(python3 - "$TARGET" <<'PY'
import sys
from pathlib import Path
try:
    import yaml
except Exception:
    print("bid-document.docx")
    print("")
    sys.exit(0)

target = Path(sys.argv[1])
metadata = yaml.safe_load((target / "metadata.yaml").read_text(encoding="utf-8")) or {}
outline = yaml.safe_load((target / "outline.yaml").read_text(encoding="utf-8")) or {}
export = metadata.get("export") or {}
print(export.get("output_name") or "bid-document.docx")
sections = outline.get("sections") or []
parent_ids = {str(section.get("parent_id")).strip() for section in sections if section.get("parent_id") is not None}
templates = sorted({str(section.get("docx_template") or "").strip() for section in sections if str(section.get("id") or "").strip() not in parent_ids and str(section.get("docx_template") or "").strip()})
if len(templates) > 1:
    print(f"ERROR: multiple docx_template profiles in one export: {', '.join(templates)}", file=sys.stderr)
    sys.exit(2)
if templates:
    profile = templates[0]
    path = (export.get("docx_templates") or {}).get(profile)
    if not path:
        print(f"ERROR: docx_template profile not configured: {profile}", file=sys.stderr)
        sys.exit(2)
    ref = Path(path)
    if not ref.is_absolute():
        ref = target / ref
    print(str(ref))
else:
    print(export.get("reference_docx") or "")
PY
)
output_name=$(printf '%s\n' "$export_info" | sed -n '1p')
reference_docx=$(printf '%s\n' "$export_info" | sed -n '2p')

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found; generated $COMBINED only" >&2
  exit 0
fi

args=("$COMBINED" "-o" "$OUT_DIR/$output_name")
if [[ -n "$reference_docx" ]]; then
  args+=("--reference-doc=$reference_docx")
fi

pandoc "${args[@]}"
echo "Generated $OUT_DIR/$output_name"
