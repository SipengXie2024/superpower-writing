---
description: Draft one or all sections of the paper. Enforces claim-first protocol via PreToolUse hook.
argument-hint: "[section name or 'all']"
---

Invoke the `superpower-writing:drafting` skill. Section (if specified): $ARGUMENTS.

The skill orchestrates per-section LaTeX prose generation in serial or parallel mode. Each drafter subagent must resolve claim EVIDENCE (Zotero first when enabled, network fallback) to `STATUS: evidence_ready` before the PreToolUse hook at `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` permits writing to `.writing/manuscript/*.tex`.
