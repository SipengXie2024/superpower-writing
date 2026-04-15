#!/usr/bin/env bash
# PreToolUse wrapper. Dispatches to the python implementation.
set -euo pipefail
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
exec python3 "$PLUGIN_ROOT/hooks/enforce-claims.py"
