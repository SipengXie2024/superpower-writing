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

output_name=$(python3 - "$TARGET" <<'PY'
import sys
from pathlib import Path
try:
    import yaml
except Exception:
    print("bid-document.docx")
    sys.exit(0)
data = yaml.safe_load((Path(sys.argv[1]) / "metadata.yaml").read_text(encoding="utf-8")) or {}
print(((data.get("export") or {}).get("output_name")) or "bid-document.docx")
PY
)

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found; generated $COMBINED only" >&2
  exit 0
fi

args=("$COMBINED" "-o" "$OUT_DIR/$output_name")
reference_docx=$(python3 - "$TARGET" <<'PY'
import sys
from pathlib import Path
try:
    import yaml
except Exception:
    sys.exit(0)
data = yaml.safe_load((Path(sys.argv[1]) / "metadata.yaml").read_text(encoding="utf-8")) or {}
ref = ((data.get("export") or {}).get("reference_docx")) or ""
if ref:
    print(ref)
PY
)
if [[ -n "$reference_docx" ]]; then
  args+=("--reference-doc=$reference_docx")
fi

pandoc "${args[@]}"
echo "Generated $OUT_DIR/$output_name"
