---
description: Draft or continue one or more bid sections as Markdown.
argument-hint: "[section-id|all]"
---

Invoke the `cn-bid-writing:drafting` skill. Draft target: $ARGUMENTS.

The skill reads `.bid/outline.yaml`, `.bid/prompts/`, and `.bid/inputs/`, then writes or continues the mapped file under `.bid/chapters/`.
