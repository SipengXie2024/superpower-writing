#!/usr/bin/env bash
# SessionStart hook. Runs the shared dep-check script and emits a
# system-reminder summarizing status. Never blocks session start
# (exit 0 always); reminder is advisory.
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT="$("$PLUGIN_ROOT/scripts/check-deps.sh" 2>&1)" || true
STATUS=$?

if [[ $STATUS -ne 0 ]]; then
  BODY="superpower-writing dependency check FAILED.

$OUTPUT

Do not invoke any superpower-writing skill (main, outlining, writing-plans,
drafting, claim-verification, revision, submission) until the missing
dependencies are installed."
else
  BODY="superpower-writing deps OK. Bundled domain skills detected."
fi

cat <<EOF
<system-reminder>
$BODY
</system-reminder>
EOF
exit 0
