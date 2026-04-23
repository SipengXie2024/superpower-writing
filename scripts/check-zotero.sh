#!/usr/bin/env bash
# Verify Zotero Web API credentials and the zotero-mcp binary are
# available. Called by skills only when `.writing/metadata.yaml` has
# `zotero.enabled: true`.
#
# Never prints secret values. Exit 1 on missing/invalid config.

set -euo pipefail

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

errors=()

[[ -z "${ZOTERO_API_KEY:-}" ]]     && errors+=("ZOTERO_API_KEY is not set")
[[ -z "${ZOTERO_LIBRARY_ID:-}" ]]  && errors+=("ZOTERO_LIBRARY_ID is not set")

lib_type="${ZOTERO_LIBRARY_TYPE:-user}"
case "$lib_type" in
  user|group) ;;
  *) errors+=("ZOTERO_LIBRARY_TYPE must be 'user' or 'group' (got: $lib_type)") ;;
esac

if (( ${#errors[@]} > 0 )); then
  echo "[superpower-writing] Zotero credentials missing/invalid:" >&2
  for e in "${errors[@]}"; do echo "  - $e" >&2; done
  cat >&2 <<'EOF'

Setup:
  1. cp .env.example .env
  2. Fill ZOTERO_API_KEY, ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE (user|group)
     API key: https://www.zotero.org/settings/keys
  3. export them in the shell that launches Claude Code (or source .env there).

To disable Zotero integration entirely, set zotero.enabled: false in
.writing/metadata.yaml.
EOF
  exit 1
fi

# Verify the zotero-mcp binary is on PATH. Plugin-level .mcp.json invokes it
# by name, so if it's missing the MCP server will never start.
if ! command -v zotero-mcp >/dev/null 2>&1; then
  cat >&2 <<'EOF'
[superpower-writing] zotero-mcp binary not found on PATH.

Install it with one of:
    uv tool install zotero-mcp
    pipx install zotero-mcp
    pip install zotero-mcp

Requires Python 3.10+.
EOF
  exit 1
fi

# Probe the Web API. Key never appears in stdout/stderr.
http_code=$(curl -sS -o /dev/null -w '%{http_code}' \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/${lib_type}s/${ZOTERO_LIBRARY_ID}/items?limit=1" || echo "000")

case "$http_code" in
  200)
    echo "[superpower-writing] Zotero OK (${lib_type}s/${ZOTERO_LIBRARY_ID}; zotero-mcp: $(command -v zotero-mcp))"
    exit 0
    ;;
  403)
    echo "[superpower-writing] Zotero auth FAILED (HTTP 403). Check API key permissions at https://www.zotero.org/settings/keys" >&2
    exit 1
    ;;
  404)
    echo "[superpower-writing] Zotero library not found (HTTP 404). Check ZOTERO_LIBRARY_ID and ZOTERO_LIBRARY_TYPE." >&2
    exit 1
    ;;
  *)
    echo "[superpower-writing] Zotero probe failed (HTTP $http_code). Is the network available?" >&2
    exit 1
    ;;
esac
