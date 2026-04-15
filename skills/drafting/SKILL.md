---
name: drafting
description: Orchestrates prose drafting section-by-section, in serial (subagent + 2-stage review) or parallel (Agent Team) mode. Each section subagent must resolve claim EVIDENCE via research-lookup before writing prose (claim-first protocol; PreToolUse hook enforces this). Use after writing-plans produces .writing/plan.md.
---

# Drafting

Drive prose production for the manuscript. For every section in `.writing/plan.md`, resolve evidence for every claim first, then write `<!-- claim: id -->`-tagged paragraphs. This skill owns the writing-specific prompt template, the Zotero-aware evidence loop, and the graphical abstract dispatch; execution is handled by the local `superpower-writing:{subagent-driven, team-driven, executing-plans}` engines.

**Announce at start:** "I'm using the drafting skill to produce manuscript prose."

## Overview

Drafting is the stage where claims become sentences. The hard rule is **claim-first**: no prose may cite a claim whose `STATUS` is still `stub`. Resolve evidence, then write.

> Claim-first protocol: see `superpower-writing:main` §Claim-First Protocol.

This skill only shapes the per-section prompt and the bookkeeping. The orchestration engine is one of three local `superpower-writing` skills, picked by mode:

- **serial** → `subagent-driven` (one implementer per section + spec review + quality review)
- **parallel** → `team-driven` (Agent Team with dedicated reviewer, multiple sections in flight)
- **session-handoff** → `executing-plans` (batch execution across sessions with human checkpoints)

All three already know how to read `.writing/plan.md` as their task source once the per-section template below is injected into their implementer prompts.

## When to Use

Invoke after `writing-plans` has produced `.writing/plan.md` with per-section draft tasks. Do NOT invoke before:

- `.writing/outline.md` exists and was approved.
- `.writing/claims/section_*.md` files exist (one per section) with at least stub entries.
- `.writing/metadata.yaml` is filled (non-YAGNI fields).
- `.writing/plan.md` lists the concrete section/figure/table tasks.

Skip this skill if the user only wants to revise existing prose (use `revision`) or verify an already-drafted manuscript (use `claim-verification`).

## Checklist

Before dispatching any section:

- [ ] `.writing/plan.md` exists and lists draft tasks.
- [ ] `.writing/claims/section_<NN>_<slug>.md` exists for every section listed.
- [ ] `.writing/metadata.yaml` has been read; note `zotero.enabled` and `zotero.auto_push_new_citations`.
- [ ] `.writing/manuscript/` directory exists (created by `init-writing-dir.sh`).
- [ ] Graphical-abstract slot is tracked in `.writing/progress.md` (required by upstream `scientific-writing`).

Per section, before marking complete:

- [ ] Every claim id referenced in the prose resolves to `STATUS ∈ {evidence_ready, verified}` in its claims file.
- [ ] Every load-bearing paragraph carries `<!-- claim: id -->`; drafting notes use `<!-- draft-only -->`.
- [ ] PreToolUse hook did not block any write (visible as exit-2 JSON from `enforce-claims.sh`).
- [ ] `.writing/progress.md` Task Dashboard row updated (Status, Claim Verification, Citation Check).

## Process

### 1. Mode selection

Use `AskUserQuestion` to let the user pick the execution strategy. Do NOT default silently.

```
Question: How should I draft this manuscript?
Header:   "Drafting mode"
Options:
  - Label:       "Serial (subagent-driven)"
    Description: "One implementer subagent per section, two-stage review after each. Best for short papers or when sections depend on each other."
  - Label:       "Parallel (team-driven)"
    Description: "Agent Team drafts independent sections in parallel with a dedicated reviewer. Best for long papers with independent sections."
  - Label:       "Session handoff (executing-plans)"
    Description: "Batch execution across sessions with human checkpoints between batches. Best when you want to review in chunks."
```

Recommend by heuristic:

- ≤ 3 draft sections OR sections with heavy narrative cross-refs (Intro ↔ Discussion) → serial.
- ≥ 4 independent sections (Methods + Results blocks) → parallel.
- User explicitly wants to checkpoint between batches, or session is long-running → session-handoff.

Then hand off:

- serial → `Skill(skill="superpower-writing:subagent-driven")` with implementer subagent type `superpower-writing:section-drafter`, spec-reviewer `superpower-writing:spec-reviewer`, and manuscript reviewer `superpower-writing:manuscript-reviewer` (writing-quality lens).
- parallel → `Skill(skill="superpower-writing:team-driven")` spawning one `superpower-writing:section-drafter` per independent section plus one shared `superpower-writing:manuscript-reviewer`. Keep `superpower-writing:spec-reviewer` for plan alignment.
- session-handoff → `Skill(skill="superpower-writing:executing-plans")` (same agent types, separate session).

The `section-drafter` agent file at `agents/section-drafter.md` already encodes the claim-first protocol and the Zotero-first evidence resolution flow; the per-section prompt (next section) layers the specific section details on top of that baseline. Inject `.writing/plan.md` task text verbatim.

### 2. Per-section subagent prompt template

Every drafter subagent receives the same prompt body, customized only with section number, slug, and the verbatim task text from `.writing/plan.md`. The template is the core contribution of this skill — copy it into the dispatch prompt exactly, including the claim-first warnings (they are what makes the PreToolUse hook survivable).

Read the full template at [`references/section-drafter-prompt.md`](references/section-drafter-prompt.md) and inject the verbatim task text where marked. The orchestrator (serial / parallel / session-handoff) layers its review gates on top of this body without modifying Steps A–C.

### 3. Graphical abstract and schematics

Upstream `scientific-writing` mandates at least one graphical abstract plus at least one schematic figure. Do not attempt to draw these with prose tools.

- For the graphical abstract:

  ```
  Skill(skill="scientific-schematics")
  Output: .writing/figures/graphical_abstract.png
  Caption: write into .writing/figures/graphical_abstract.md (caption only)
  ```

  Treat this as its own "section task" in the plan, not a sub-step of a prose section. Route it through whichever mode was chosen in step 1 — the `scientific-schematics` call is the implementer's responsibility, not this skill's.

- For additional schematics referenced in Methods or Results:

  One `scientific-schematics` invocation per figure. The prose paragraph that introduces the figure still needs a `<!-- claim: id -->` tag pointing at whatever claim the figure supports (usually a mechanism or pipeline claim). The figure file itself goes to `.writing/figures/<slug>.png` and is not subject to the PreToolUse hook (the matcher only covers `manuscript/*.md`).

### 4. Progress tracking after each section

After each section returns (drafted and committed), the orchestrator updates `.writing/progress.md` Task Dashboard. Expected columns:

| Section | Status | Claim Verification | Citation Check | Reviewer Cycle | Key Outcome |
|---------|--------|--------------------|----------------|----------------|-------------|
| 02_methods | drafted | 5/5 evidence_ready | pending | - | 1247-patient T2D cohort described |

Set:

- **Status**: `drafted` once prose is committed. `verified` is reserved for claim-verification.
- **Claim Verification**: ratio of `evidence_ready` or `verified` claims to total claims in that section's claims file. This is a lightweight count; the real check is the claim-verification skill.
- **Citation Check**: `pending` until `claim-verification` runs. This skill does not perform DOI resolution / semantic matching.
- **Reviewer Cycle**: filled by the underlying `subagent-driven` / `team-driven` / `executing-plans` engine.

If any claim remains `stub` (because of a `[NEEDS-EVIDENCE]` miss), set Status to `blocked: <count> unresolved` and surface to the user. Do NOT mark the section drafted while stubs remain in its prose.

### 5. Zotero integration

The Zotero-first / network-fallback / optional auto-push flow is fully specified in Step A of the section-drafter prompt. On runtime failures (rate limit, auth revoke mid-draft), treat the failing call as a Zotero miss, continue via `research-lookup` / `citation-management`, and log the failure to `.writing/findings.md` under "Issues" so the user can fix credentials between sections. `main` runs `${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh` at session start, so credentials are already verified by the time drafting begins.

## Key Principles

**Claim-first, always.** Evidence before prose is the central discipline of this plugin. The hook is the backstop, not the workflow — the workflow is Step A of the template. If drafting ever feels "fast" because a subagent skipped Step A, the hook will stop it and you will redo the work. Do it right the first time.

**Own the prompt; invoke execution by name.** This skill owns the per-section prompt template and the claim-first bookkeeping. Execution (parallelism, review gates, session management) is handled by the local `superpower-writing:{subagent-driven, team-driven, executing-plans}` engines, which this skill invokes by name.

**Zotero miss is not a failure.** A DOI absent from the user's Zotero library just means the user has not yet vetted it. Network fallback is normal and expected. The only failure mode is "no credible source anywhere", which must be escalated.

**Graphical abstract is a first-class task.** Upstream requires one. Do not skip it, and do not inline its generation into a prose section — route it through `scientific-schematics` as its own task.

**Progress dashboard is the handoff contract.** `claim-verification` and `revision` read `.writing/progress.md` to know what has been drafted, verified, or reviewed. A section is not "drafted" until its row is updated and committed.

**Do not fight the hook.** If `enforce-claims.sh` blocks a write, the hook is telling you the claim-first protocol was violated. Resolve the underlying cause (missing claim entry, stub STATUS, untagged paragraph). Never propose disabling the hook or bypassing it with a sneaky `MultiEdit`.

## Integration

- `superpower-writing:writing-plans` — produces `.writing/plan.md`; drafting reads it verbatim.
- `superpower-writing:claim-verification` — downstream; consumes `.writing/manuscript/*.md` and confirms every claim tag.
- `superpower-writing:revision` — downstream; called when reviews come back.
- `superpower-writing:subagent-driven` / `team-driven` / `executing-plans` — the actual execution engines.
- Upstream `scientific-writing` — voice and structure rules.
- Upstream `scientific-schematics` — graphical abstract + schematics.
- Upstream `research-lookup`, `citation-management`, `pyzotero` — evidence resolution.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` — PreToolUse enforcement of the claim-first protocol.
