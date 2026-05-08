---
description: Create or update the outline for a Chinese bid document.
argument-hint: "[bid topic or requirements]"
---

Invoke the `cn-bid-writing:outlining` skill. Topic or requirements: $ARGUMENTS.

The skill will initialize `.bid/` if needed, then update `.bid/outline.md` and `.bid/outline.yaml` with a multi-level section tree suitable for section-by-section drafting.
