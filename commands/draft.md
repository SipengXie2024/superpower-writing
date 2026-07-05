---
description: Draft one or all sections of the paper under the claim-first protocol.
argument-hint: "[section name or 'all']"
---

Invoke the `superpower-writing:drafting` skill. Section (if specified): $ARGUMENTS.

The skill orchestrates per-section LaTeX prose generation via a Claude Code dynamic workflow (parallel sections) or a manual batch session. Each drafter subagent must resolve claim EVIDENCE (Zotero first when enabled, network fallback) to `STATUS: evidence_ready` before writing to `.writing/manuscript/*.tex` — a required drafting discipline.
