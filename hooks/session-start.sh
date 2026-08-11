#!/usr/bin/env bash
# SessionStart hook for superpower-writing plugin
#
# Emits a reminder only when this is a writing project (.writing/ exists)
# that has no repo-root CONTEXT.md yet. Silent no-op everywhere else.

set -euo pipefail

if [ ! -d ".writing" ] || [ -f "CONTEXT.md" ]; then
    exit 0
fi

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<NO_PROJECT_GLOSSARY>\nThis writing project has no repo-root CONTEXT.md (project glossary / ubiquitous language) yet. Do NOT scaffold it empty. The moment idea, outlining, or design talk resolves the first domain term (the contribution name, the system name), create CONTEXT.md with that term (superpower-writing:domain-glossary) and tell the user the glossary has started.\n</NO_PROJECT_GLOSSARY>"
  }
}
EOF

exit 0
