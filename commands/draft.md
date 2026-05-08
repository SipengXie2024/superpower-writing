---
description: Draft or continue one or more bid sections as Markdown.
argument-hint: "[section-id|all]"
---

Invoke the `cn-bid-writing:drafting` skill. Draft target: $ARGUMENTS.

The skill reads `.bid/outline.yaml`, `.bid/prompts/`, and `.bid/inputs/`, then drafts selected leaf sections in parallel with `bid-section-writer` agents. Each section must pass `bid-section-verifier` against the outline before `bid-section-polisher` performs humanization.
