#!/usr/bin/env bash
# Detect whether scientific-agent-skills (K-Dense-AI, agentskills.io standard)
# is installed on this system. Required by every superpower-writing skill.

set -euo pipefail

REQUIRED=(
  literature-review
  citation-management
  research-lookup
  scientific-schematics
  scientific-visualization
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

Missing bundled domain skills: ${missing[*]}

These skills ship inside this plugin and are normally found under the
plugin's own skills/ directory. A missing skill means the plugin itself
is incomplete — re-clone or reinstall:

    git clone https://github.com/SipengXie2024/superpower-writing.git
    # then: claude plugin marketplace add /absolute/path/to/superpower-writing

(The earlier upstream dependency on K-Dense-AI/scientific-agent-skills
was dissolved in v0.7.0; legacy install roots are still probed for
back-compat but new installs should use the bundled copies.)

Roots searched:
EOF
  for root in "${CANDIDATE_ROOTS[@]}"; do echo "  $root" >&2; done
  exit 1
fi

# The PreToolUse hook (hooks/enforce-claims.py) requires PyYAML. Probe both
# import AND a real parse so a broken/partial install fails at SessionStart
# rather than at the first manuscript Edit.
if ! python3 -c "import yaml; yaml.safe_load('a: 1')" 2>/dev/null; then
  cat >&2 <<EOF
[superpower-writing] Dependency check FAILED.

Bundled skills OK, but PyYAML is missing or broken. The PreToolUse hook
parses YAML claim files and will block every manuscript write until it is
installed and parsing correctly:

    pip install --user --upgrade pyyaml
EOF
  exit 1
fi

# ── Figure-generation backend (Codex CLI) — warning only ────────────────
# scientific-schematics delegates diagram generation to Codex's native
# image_gen via the collaborating-with-codex bridge. The bridge needs the
# `codex` CLI on PATH; the rest of the writing lifecycle works without it.
if ! command -v codex >/dev/null 2>&1; then
  cat >&2 <<EOF
[superpower-writing] Dependency check WARNING.

The 'codex' CLI was not found on PATH. Figure generation
(superpower-writing:scientific-schematics) delegates to Codex's built-in
image_gen and will not work until Codex CLI is installed and authenticated.
Everything else in the plugin works without it.
EOF
fi

echo "[superpower-writing] deps OK (skills at $found_root; PyYAML present)"
exit 0
