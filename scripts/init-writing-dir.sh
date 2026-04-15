#!/usr/bin/env bash
# Initialize a .writing/ directory in the current project. Mirrors the
# .planning/ pattern used by superpower-planning.

set -euo pipefail

TARGET="${1:-.writing}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
TEMPLATE_DIR="$PLUGIN_ROOT/templates"

if [[ -d "$TARGET" ]]; then
  echo "$TARGET already exists; refusing to overwrite." >&2
  exit 1
fi

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  echo "Is CLAUDE_PLUGIN_ROOT set correctly?" >&2
  exit 1
fi

mkdir -p "$TARGET"/{manuscript,claims,figures,reviews,archive}

cp "$TEMPLATE_DIR/progress.md"  "$TARGET/progress.md"
cp "$TEMPLATE_DIR/findings.md"  "$TARGET/findings.md"
cp "$TEMPLATE_DIR/metadata.yaml" "$TARGET/metadata.yaml"
: > "$TARGET/outline.md"

cat <<EOF
Initialized $TARGET/
  files:   progress.md  findings.md  metadata.yaml  outline.md
  subdirs: manuscript/  claims/  figures/  reviews/  archive/

Next step: open \`$TARGET/outline.md\` and start outlining, or invoke the
\`superpower-writing:outlining\` skill.
EOF
