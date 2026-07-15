---
description: Draft one or all sections of the paper under the claim-first protocol.
argument-hint: "[section name or 'all']"
---

Invoke the `superpower-writing:drafting` skill. Section (if specified): $ARGUMENTS.

You draft each section yourself, inline and in outline order, with no parallel subagents. For each section, resolve every claim's EVIDENCE first (Zotero when enabled, network fallback via `literature` / `citations`) to `STATUS: evidence_ready`, then write LaTeX prose tagged with its claim ids to `.writing/manuscript/*.tex`. The evidence-before-prose rule is non-negotiable; see the skill's `references/claim-first.md`.
