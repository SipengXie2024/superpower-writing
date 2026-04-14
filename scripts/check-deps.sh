#!/usr/bin/env bash
# Detect whether scientific-agent-skills (K-Dense-AI, agentskills.io standard)
# is installed on this system. Required by every superpower-writing skill.

set -euo pipefail

REQUIRED=(
  scientific-writing
  literature-review
  peer-review
  citation-management
  research-lookup
  scientific-schematics
)

# Agent Skills standard installs to platform-specific locations. Probe the
# common ones. First match wins.
CANDIDATE_ROOTS=(
  "$HOME/.claude/skills"
  "$HOME/.claude/plugins/cache"
  "$HOME/.cursor/skills"
  "$HOME/.config/claude-code/skills"
  "$HOME/.codex/skills"
  "$HOME/Library/Application Support/Claude/skills"
  "/usr/local/share/claude/skills"
)

found_root=""
missing=()

for skill in "${REQUIRED[@]}"; do
  hit=""
  for root in "${CANDIDATE_ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    if find "$root" -maxdepth 5 -type f -path "*/$skill/SKILL.md" -print -quit 2>/dev/null | grep -q .; then
      hit="$root"
      [[ -z "$found_root" ]] && found_root="$root"
      break
    fi
  done
  [[ -z "$hit" ]] && missing+=("$skill")
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

echo "[superpower-writing] deps OK (found at: $found_root)"
exit 0
