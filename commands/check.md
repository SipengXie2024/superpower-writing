---
description: Check bid workspace structure, chapter mappings, and minimum character counts.
argument-hint: "[target dir, default .bid]"
---

Invoke the `cn-bid-writing:verification` skill. Target directory: $ARGUMENTS.

The skill runs `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh`, explains failures, and does not claim readiness until checks pass.
