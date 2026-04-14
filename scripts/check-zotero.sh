#!/usr/bin/env bash
# Verify Zotero API credentials are available. Called by skills that touch
# Zotero only when `.writing/metadata.yaml` has `zotero.enabled: true`.
#
# Never prints secret values. Exit 1 on missing/invalid config.

set -euo pipefail

# Load .env from current project root if present (without echoing).
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

errors=()

if [[ -z "${ZOTERO_API_KEY:-}" ]]; then
  errors+=("ZOTERO_API_KEY is not set")
fi

if [[ -z "${ZOTERO_USER_ID:-}" && -z "${ZOTERO_GROUP_ID:-}" ]]; then
  errors+=("neither ZOTERO_USER_ID nor ZOTERO_GROUP_ID is set (need one)")
fi

if (( ${#errors[@]} > 0 )); then
  cat >&2 <<EOF
[superpower-writing] Zotero credentials missing:
EOF
  for e in "${errors[@]}"; do echo "  - $e" >&2; done
  cat >&2 <<EOF

Setup:
  1. cp .env.example .env
  2. Fill in ZOTERO_API_KEY and ZOTERO_USER_ID (or ZOTERO_GROUP_ID).
     Key from: https://www.zotero.org/settings/keys
  3. Ensure .env is in .gitignore (default).

To disable Zotero integration entirely, set zotero.enabled: false in
.writing/metadata.yaml.
EOF
  exit 1
fi

# Sanity check by hitting a low-cost Zotero API endpoint. Don't print the response body.
target_id="${ZOTERO_GROUP_ID:-$ZOTERO_USER_ID}"
target_type="users"
[[ -n "${ZOTERO_GROUP_ID:-}" ]] && target_type="groups"

http_code=$(curl -sS -o /dev/null -w '%{http_code}' \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/${target_type}/${target_id}/items?limit=1" || echo "000")

case "$http_code" in
  200)
    echo "[superpower-writing] Zotero OK (${target_type}/${target_id})"
    exit 0
    ;;
  403)
    echo "[superpower-writing] Zotero auth FAILED (HTTP 403). Check API key permissions at https://www.zotero.org/settings/keys" >&2
    exit 1
    ;;
  404)
    echo "[superpower-writing] Zotero library not found (HTTP 404). Check ZOTERO_USER_ID / ZOTERO_GROUP_ID." >&2
    exit 1
    ;;
  *)
    echo "[superpower-writing] Zotero probe failed (HTTP $http_code). Is the network available?" >&2
    exit 1
    ;;
esac
