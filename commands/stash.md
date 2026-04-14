---
description: Pause the current paper and stash its .writing/ state into .writing/stash/<name>/.
argument-hint: "[paper name slug]"
---

Move the current working state (everything under `.writing/` except `archive/` and `stash/` itself) into `.writing/stash/$ARGUMENTS/`, resetting the active workspace. Re-initialize an empty `.writing/` via `${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh` if the user wants to start a new paper.

Use `/writing:resume-stash` (future) or manually move files back to restore. For now, invoke `superpower-writing:main` and let its Stash/Resume routing handle the details.
