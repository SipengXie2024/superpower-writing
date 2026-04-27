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

# ── Verify image-generator is built ─────────────────────────────────────
IMAGE_GEN_ROOT="$(dirname "${BASH_SOURCE[0]}")/../tools/image-generator"
IMAGE_GEN_CLI="$IMAGE_GEN_ROOT/dist/cli.js"

if [[ ! -f "$IMAGE_GEN_CLI" ]]; then
  cat >&2 <<EOF
[superpower-writing] Dependency check FAILED.

image-generator is not built. Run:

    cd tools/image-generator && npm install && npm run build

EOF
  exit 1
fi

# Check Node.js version (>= 20 required by image-generator)
if ! node -e "const v = process.versions.node.split('.').map(Number); process.exit(v[0] < 20 ? 1 : 0)" 2>/dev/null; then
  cat >&2 <<EOF
[superpower-writing] Dependency check FAILED.

image-generator requires Node.js >= 20. Found: $(node --version 2>/dev/null || echo 'not installed')

Install or update Node.js: https://nodejs.org/
EOF
  exit 1
fi

# Check Codex OAuth credentials (warning only — user may not need image generation)
TOKEN_FILE="$HOME/.config/superpower-writing/codex-tokens.json"
if [[ ! -f "$TOKEN_FILE" ]]; then
  cat >&2 <<EOF
[superpower-writing] Dependency check WARNING.

image-generator is not authenticated. Run once:

    node $IMAGE_GEN_CLI login

This opens a browser for OAuth (requires ChatGPT Plus/Pro account).
Diagram generation will not work until you log in.
EOF
fi

echo "[superpower-writing] deps OK (skills at $found_root; PyYAML present; image-gen built)"
exit 0
