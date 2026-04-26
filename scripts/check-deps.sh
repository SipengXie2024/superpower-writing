#!/usr/bin/env bash
# Detect whether scientific-agent-skills (K-Dense-AI, agentskills.io standard)
# is installed on this system. Required by every superpower-writing skill.

set -euo pipefail

REQUIRED=(
  literature-review
  peer-review
  citation-management
  research-lookup
  scientific-schematics
)

# Agent Skills standard installs to platform-specific locations. Probe the
# common ones, plus this plugin's own skills/ directory (preferred when present
# so the dep-check resolves against shipped copies before any external install).
# First match wins.
CANDIDATE_ROOTS=(
  "$(dirname "${BASH_SOURCE[0]}")/../skills"
  "$HOME/.claude/skills"
  "$HOME/.claude/plugins/cache"
  "$HOME/.cursor/skills"
  "$HOME/.config/claude-code/skills"
  "$HOME/.codex/skills"
  "$HOME/Library/Application Support/Claude/skills"
  "/usr/local/share/claude/skills"
)

found_root=""
missing=("${REQUIRED[@]}")

# One find per root (≤7 invocations total). For each root, collect the set of
# parent-directory names of any SKILL.md and intersect with REQUIRED. The first
# root whose set covers ALL required skills wins.
for root in "${CANDIDATE_ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  present="$(find "$root" -maxdepth 5 -type f -name SKILL.md 2>/dev/null \
              | awk -F/ '{print $(NF-1)}' | sort -u)"
  root_missing=()
  for skill in "${REQUIRED[@]}"; do
    grep -qx "$skill" <<<"$present" || root_missing+=("$skill")
  done
  if (( ${#root_missing[@]} == 0 )); then
    found_root="$root"
    missing=()
    break
  fi
  # Track the smallest-missing root so an eventual failure surfaces the best candidate.
  if (( ${#root_missing[@]} < ${#missing[@]} )); then
    missing=("${root_missing[@]}")
  fi
done

if (( ${#missing[@]} > 0 )); then
  cat >&2 <<EOF
[superpower-writing] Dependency check FAILED.

Missing upstream skills: ${missing[*]}

Install scientific-agent-skills (K-Dense-AI) via the agentskills.io standard:

    npx skills add K-Dense-AI/scientific-agent-skills

If 'uv' is not yet installed (required by upstream scientific skills for
Python dependencies):

    curl -LsSf https://astral.sh/uv/install.sh | sh

Roots searched:
EOF
  for root in "${CANDIDATE_ROOTS[@]}"; do echo "  $root" >&2; done
  exit 1
fi

# The PreToolUse hook (hooks/enforce-claims.py) requires PyYAML. Probe it so
# users find out at SessionStart rather than at first Edit.
if ! python3 -c "import yaml" 2>/dev/null; then
  cat >&2 <<EOF
[superpower-writing] Dependency check FAILED.

Upstream skills OK, but PyYAML is missing. The PreToolUse hook parses YAML
claim files and will block every manuscript write until you install it:

    pip install --user pyyaml
EOF
  exit 1
fi

echo "[superpower-writing] deps OK (skills at $found_root; PyYAML present)"
exit 0
