#!/usr/bin/env bash
# Initialize a .writing/ directory in the current project. Combines the
# writing-domain skeleton (manuscript/, claims/, figures/, reviews/, archive/
# plus metadata.yaml and outline.md) with upstream planning-foundation's
# idempotent re-run + .gitignore auto-registration behavior.
#
# Usage: ./init-writing-dir.sh [target-dir]
#   Default target: .writing in the current working directory.
#   Re-running is safe: missing files are created, existing files are preserved.

set -euo pipefail

TARGET="${1:-.writing}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
TEMPLATE_DIR="$PLUGIN_ROOT/templates"
DATE=$(date +%Y-%m-%d)

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  echo "Is CLAUDE_PLUGIN_ROOT set correctly?" >&2
  exit 1
fi

mkdir -p "$TARGET"/{manuscript,claims,figures,reviews,archive}

# .gitignore: add .writing/verify-cache.json and .writing/stash/ if not present.
# (Full .writing/ is NOT ignored — drafts live under version control.)
PROJECT_ROOT="$(pwd)"
GITIGNORE="${PROJECT_ROOT}/.gitignore"
add_ignore_line() {
  local line="$1"
  if [[ -f "$GITIGNORE" ]]; then
    if ! grep -qF "$line" "$GITIGNORE" 2>/dev/null; then
      echo "$line" >> "$GITIGNORE"
      echo "Added $line to .gitignore"
    fi
  elif [[ -d "${PROJECT_ROOT}/.git" ]]; then
    printf '%s\n' "$line" > "$GITIGNORE"
    echo "Created .gitignore with $line"
  fi
}
add_ignore_line ".writing/verify-cache.json"
add_ignore_line ".writing/stash/"

create_if_missing() {
  local src="$1" dst="$2"
  if [[ -f "$dst" ]]; then
    echo "$dst already exists, skipping"
  else
    sed "s|\[YYYY-MM-DD\]|$DATE|g; s|\[DATE\]|$DATE|g" "$src" > "$dst"
    echo "Created $dst"
  fi
}

create_if_missing "$TEMPLATE_DIR/progress.md"   "$TARGET/progress.md"
create_if_missing "$TEMPLATE_DIR/findings.md"   "$TARGET/findings.md"
create_if_missing "$TEMPLATE_DIR/metadata.yaml" "$TARGET/metadata.yaml"
[[ -f "$TARGET/outline.md" ]] || : > "$TARGET/outline.md"

cat <<EOF

Initialized $TARGET/
  files:   progress.md  findings.md  metadata.yaml  outline.md
  subdirs: manuscript/  claims/  figures/  reviews/  archive/

Next step: open \`$TARGET/outline.md\` and start outlining, or invoke the
\`superpower-writing:outlining\` skill.
EOF
