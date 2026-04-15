#!/usr/bin/env bash
# Reset .writing/ to clean state while preserving archive/ and stash/
#
# Usage: writing-reset.sh [project-root]
#
# Removes: progress.md, findings.md, agents/
# Preserves: archive/, stash/
# Then runs init-writing-dir.sh to recreate canonical files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PROJECT_ROOT="${1:-.}"
PLANNING_DIR="${PROJECT_ROOT}/.writing"

if [ ! -d "$PLANNING_DIR" ]; then
    echo "[writing-reset] No .writing/ directory found. Nothing to reset."
    exit 0
fi

# Remove active planning files
rm -f "${PLANNING_DIR}/progress.md"
rm -f "${PLANNING_DIR}/findings.md"
rm -f "${PLANNING_DIR}/design.md"
rm -f "${PLANNING_DIR}/plan.md"

# Remove agents directory
if [ -d "${PLANNING_DIR}/agents" ]; then
    rm -rf "${PLANNING_DIR}/agents"
    echo "[writing-reset] Removed .writing/agents/"
fi

# Recreate canonical files from templates (init takes the .writing/ target dir)
"${SCRIPT_DIR}/init-writing-dir.sh" "$PLANNING_DIR"

echo "[writing-reset] .writing/ reset to clean state (archive/ and stash/ preserved)"
