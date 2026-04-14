---
description: Verify scientific-agent-skills and (optionally) Zotero credentials are available.
---

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh` and, if `.writing/metadata.yaml` has `zotero.enabled: true`, also run `${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh`.

If any check fails, surface the install command or setup instructions emitted by the script and stop. If all pass, report "deps OK" and exit.
