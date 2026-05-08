#!/usr/bin/env bash
# Initialize a .bid/ workspace for cn-bid-writing.

set -euo pipefail

TARGET="${1:-.bid}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
TEMPLATE_DIR="$PLUGIN_ROOT/templates"
DATE=$(date +%Y-%m-%d)

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET"/{chapters,prompts/sections,inputs,export,archive,stash}

PROJECT_ROOT="$(pwd)"
GITIGNORE="$PROJECT_ROOT/.gitignore"
add_ignore_line() {
  local line="$1"
  if [[ -f "$GITIGNORE" ]]; then
    if ! grep -qF "$line" "$GITIGNORE" 2>/dev/null; then
      echo "$line" >> "$GITIGNORE"
      echo "Added $line to .gitignore"
    fi
  elif [[ -d "$PROJECT_ROOT/.git" ]]; then
    printf '%s\n' "$line" > "$GITIGNORE"
    echo "Created .gitignore with $line"
  fi
}

add_ignore_line ".bid/export/*.docx"
add_ignore_line ".bid/export/*.tmp"

create_if_missing() {
  local src="$1" dst="$2"
  if [[ -f "$dst" ]]; then
    echo "$dst already exists, skipping"
  else
    sed "s|\[YYYY-MM-DD\]|$DATE|g; s|\[DATE\]|$DATE|g" "$src" > "$dst"
    echo "Created $dst"
  fi
}

create_if_missing "$TEMPLATE_DIR/metadata.yaml" "$TARGET/metadata.yaml"
create_if_missing "$TEMPLATE_DIR/outline.yaml" "$TARGET/outline.yaml"
create_if_missing "$TEMPLATE_DIR/outline.md" "$TARGET/outline.md"
create_if_missing "$TEMPLATE_DIR/progress.md" "$TARGET/progress.md"
create_if_missing "$TEMPLATE_DIR/findings.md" "$TARGET/findings.md"
create_if_missing "$TEMPLATE_DIR/prompts/global.md" "$TARGET/prompts/global.md"

[[ -f "$TARGET/inputs/README.md" ]] || cat > "$TARGET/inputs/README.md" <<'README'
# 外部输入材料

把招标文件、客户要求、技术材料、案例素材或用户自定义 prompt 放在这里，并在 outline.yaml 的 input_refs 或 prompt_refs 中引用。
README

cat <<EOF
Initialized $TARGET/
  files:   metadata.yaml  outline.yaml  outline.md  progress.md  findings.md
  subdirs: chapters/  prompts/sections/  inputs/  export/  archive/  stash/

Next step: edit $TARGET/outline.yaml or invoke the cn-bid-writing outlining workflow.
EOF
