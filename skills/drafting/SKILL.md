---
name: drafting
description: Orchestrates prose drafting section-by-section, in serial (subagent + 2-stage review) or parallel (Agent Team) mode. Each section subagent must resolve claim EVIDENCE via research-lookup before writing prose (claim-first protocol; PreToolUse hook enforces this). Use after writing-plans produces .writing/plan.md.
---

# Drafting

Drive prose production for the LaTeX manuscript. For every section in `.writing/plan.md`, resolve evidence for every claim first, then write `% claim: id`-tagged paragraphs (LaTeX line comments) in `manuscript/*.tex`. This skill owns the writing-specific prompt template, the Zotero-aware evidence loop, and the graphical abstract dispatch; execution is handled by the local `superpower-writing:{subagent-driven, team-driven, executing-plans}` engines.

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
- [ ] Every load-bearing paragraph carries `% claim: id`; drafting notes use `% draft-only` (both are LaTeX line comments at column 0).
- [ ] If `.writing/glossary.md` exists: the first introduction of every glossary term is tagged `% define: <id>` in the section matching `defined_in`; subsequent uses in other sections that should be ordering-checked are tagged `% use: <id>`.
- [ ] PreToolUse hook did not block any write (visible as exit-2 JSON from `enforce-claims.sh` or `enforce-terms.sh`).
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

Every drafter subagent receives the same prompt body, customized with the section number, slug, the verbatim task text from `.writing/plan.md`, and — when a matching file exists — the section-specific writing standard. The template is the core contribution of this skill; copy it into the dispatch prompt exactly, including the claim-first warnings and the section-standard block (they are what makes the PreToolUse hook and the structural self-review survivable).

Read the full template at [`references/section-drafter-prompt.md`](references/section-drafter-prompt.md) and resolve its two placeholders before dispatch:

- `{INSERTED}` → verbatim task text from `.writing/plan.md §Task-{NN}`.
- `{SECTION_STANDARD}` → resolved via **two-level fallback (slug-ending match)** against [`references/section-standards/`](references/section-standards/):

  1. **Exact-stem match.** Try `section-standards/<NN>_<slug>.md`. Used when the paper's stem number matches a standards file's canonical slot (e.g., default-layout CS paper's `02_background` → `02_background.md`).
  2. **Slug-ending scan.** If (1) misses, scan `section-standards/` for any file whose name ends in `_<slug>.md`. Exactly one match → use it. Multiple matches → abort with configuration error. Examples: `03_background` (motivation opted in, background shifted) → `02_background.md`; `02_related_work` (early placement) → `07_related_work.md`; `02_motivation` (opt-in position) → `08_motivation.md`.
  3. **No match.** Substitute the single line:

     ```
     No section-specific standard applies; use general IMRAD conventions from scientific-writing.
     ```

  The canonical filenames in `section-standards/` are `00_abstract.md`, `01_introduction.md`, `02_background.md`, `03_methods.md`, `04_results.md`, `05_discussion.md`, `06_conclusion.md`, `07_related_work.md`, `08_motivation.md`. See [`references/section-standards/README.md`](references/section-standards/README.md) for the full contract.

The orchestrator (serial / parallel / session-handoff) layers its review gates on top of this body without modifying Steps A–C. Section standards are data injected into the prompt, not another gate in the pipeline — every engine resolves them the same way.

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

  One `scientific-schematics` invocation per figure. The prose paragraph that introduces the figure still needs a `% claim: id` tag pointing at whatever claim the figure supports (usually a mechanism or pipeline claim). The figure file itself goes to `.writing/figures/<slug>.pdf` (LaTeX prefers PDF/EPS vector formats) and is not subject to the PreToolUse hook (the matcher only covers `manuscript/*.tex`).

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

**Section standards refine, never contradict.** The files under `references/section-standards/` prescribe section-specific skeletons (BPMRC for abstracts, and whatever conventions get added for introductions, methods, etc.). They are loaded verbatim into the drafter prompt so every section that has a standard gets the same treatment. When a standard and the outline disagree, the drafter escalates rather than silently picking one — drift between outline and draft is a structural bug, not a judgment call. Adding a new standard is a `section-standards/<stem>.md` file plus, optionally, an outline-level reference in the outlining skill; no orchestrator change is needed.

**Zotero miss is not a failure.** A DOI absent from the user's Zotero library just means the user has not yet vetted it. Network fallback is normal and expected. The only failure mode is "no credible source anywhere", which must be escalated.

**Graphical abstract is a first-class task.** Upstream requires one. Do not skip it, and do not inline its generation into a prose section — route it through `scientific-schematics` as its own task.

**Progress dashboard is the handoff contract.** `claim-verification` and `revision` read `.writing/progress.md` to know what has been drafted, verified, or reviewed. A section is not "drafted" until its row is updated and committed.

**Do not fight the hook.** If `enforce-claims.sh` blocks a write, the hook is telling you the claim-first protocol was violated. Resolve the underlying cause (missing claim entry, stub STATUS, untagged paragraph). Never propose disabling the hook or bypassing it with a sneaky `MultiEdit`.

**Locked-term renames are not prose edits.** If the user or a sub-agent proposes renaming a term that is already locked in `.writing/progress.md` naming decisions, in `.writing/outline.md` bullet labels, or in prior drafted prose across multiple manuscript files, do NOT silently apply the edit. Delegate to `Skill(skill="superpower-writing:revision")` Step 2.5 (locked-term rename impact scan) even when no formal review round is in progress. The drafting skill handles prose within an agreed spec; renames cross the prose/spec boundary and need an audit of which files mention the old term and an explicit findings.md entry so the planning-file audit trail survives the rename. Applying a locked-term rename as if it were a single-file edit silently desynchronizes the manuscript from its naming history.

**Define terms before they flow across sections.** When `.writing/glossary.md` is present, the companion `enforce-terms.sh` hook blocks writes that use a term in a section before the section declared as its definition site. The fix is the same shape as the claim protocol: add or update the glossary entry, move the `% define: <id>` to the right section, or reorder sections so the term lands before its first use. `% use: <id>` is an **opt-in** annotation — you only tag the uses you want the hook to verify. An untagged occurrence of the term is not checked, so this remains a lightweight discipline rather than a universal requirement.

## Integration

- `superpower-writing:writing-plans` — produces `.writing/plan.md`; drafting reads it verbatim.
- `superpower-writing:claim-verification` — downstream; consumes `.writing/manuscript/*.tex` and confirms every claim tag.
- `superpower-writing:revision` — downstream; called when reviews come back.
- `superpower-writing:subagent-driven` / `team-driven` / `executing-plans` — the actual execution engines.
- Upstream `scientific-writing` — voice and structure rules.
- Upstream `scientific-schematics` — graphical abstract + schematics.
- Upstream `research-lookup`, `citation-management` — evidence resolution (network).
- Plugin-level `.mcp.json` `zotero` server — Zotero Web API tools. Search: `zotero_search_items` (DOI / title lookup), `zotero_semantic_search` (AI similarity search with paragraph-level matching over PDF fulltext). Read: `zotero_get_item_metadata` (markdown or BibTeX), `zotero_get_item_fulltext` (server-side PDF text — use sparingly, often 70K+ chars; prefer `zotero_semantic_search` to find relevant chunks first). Write: `zotero_add_by_doi` (auto-fetches metadata + open-access PDF). Collection nav: `zotero_get_collections`, `zotero_get_collection_items`.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` — PreToolUse enforcement of the claim-first protocol.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-terms.sh` — opt-in PreToolUse enforcement of term-definition-before-use ordering. Activates when `.writing/glossary.md` is present.
