---
name: drafting
description: Orchestrates prose drafting section-by-section via a Claude Code dynamic workflow (parallel sections + two-stage review) or a manual batch session. Each section drafter must resolve claim EVIDENCE via research-lookup before writing prose (claim-first protocol; PreToolUse hook enforces this). Use after writing-plans produces .writing/plan.md.
---

# Drafting

Drive prose production for the LaTeX manuscript. For every section in `.writing/plan.md`, resolve evidence for every claim first, then write `% claim: id`-tagged paragraphs (LaTeX line comments) in `manuscript/*.tex`. This skill owns the writing-specific prompt template, the Zotero-aware evidence loop, and the graphical abstract dispatch; orchestration is handled by a Claude Code dynamic workflow (parallel section drafting + a two-stage review pipeline) or, as a manual fallback, by `superpower-writing:executing-plans`.

**Announce at start:** "I'm using the drafting skill to produce manuscript prose."

## Overview

Drafting is the stage where claims become sentences. The hard rule is **claim-first**: no prose may cite a claim whose `STATUS` is still `stub`. Resolve evidence, then write.

> Claim-first protocol: see `superpower-writing:main` §Claim-First Protocol.

This skill only shapes the per-section prompt and the bookkeeping. Orchestration is picked by mode:

- **workflow** → a Claude Code dynamic workflow drafts independent sections in parallel with the `section-drafter` agent, then runs the two-stage review as a pipeline (`spec-reviewer` for outline/claim alignment, then `manuscript-reviewer` for writing quality). Default for multi-section papers.
- **manual-batch** → `executing-plans` (batch execution across a separate or manual session with checkpoints). Fallback when workflows are unavailable or the user wants explicit per-batch review.

Both read `.writing/plan.md` as the task source once the per-section template below is injected into the drafter prompt.

## When to Use

Invoke after `writing-plans` has produced `.writing/plan.md` with per-section draft tasks. Do NOT invoke before:

- `.writing/outline.md` exists and was approved.
- `.writing/claims/section_*.md` files exist (one per section) with at least stub entries.
- `.writing/metadata.yaml` is filled (non-YAGNI fields).
- `.writing/plan.md` lists the concrete section/figure/table tasks.

Skip this skill if the user only wants to copy-edit existing prose (use `polish` or `polish-by-diff`) or verify an already-drafted manuscript (use `claim-verification`).

## Checklist

Before dispatching any section:

- [ ] `.writing/plan.md` exists and lists draft tasks.
- [ ] `.writing/claims/section_<NN>_<slug>.md` exists for every section listed.
- [ ] `.writing/metadata.yaml` has been read; note `zotero.enabled` and `zotero.auto_push_new_citations`.
- [ ] `.writing/manuscript/` directory exists (created by `init-writing-dir.sh`).
- [ ] If the paper includes a graphical abstract (systems papers usually omit it), its slot is tracked in `.writing/progress.md`.

Per section, before marking complete:

- [ ] Every claim id referenced in the prose resolves to `STATUS ∈ {evidence_ready, verified}` in its claims file.
- [ ] Every load-bearing paragraph carries `% claim: id`; drafting notes use `% draft-only` (both are LaTeX line comments at column 0).
- [ ] If `.writing/glossary.md` exists: the first introduction of every glossary term is tagged `% define: <id>` in the section matching `defined_in`; subsequent uses in other sections that should be ordering-checked are tagged `% use: <id>`.
- [ ] PreToolUse hook did not block any write (visible as exit-2 JSON from `enforce-claims.sh` or `enforce-terms.sh`).
- [ ] `.writing/progress.md` Task Dashboard row updated (Status, Spec Review, Manuscript Review, Claim Verification).

## Process

### 1. Mode selection

Use `AskUserQuestion` to let the user pick the execution strategy. Do NOT default silently.

```
Question: How should I draft this manuscript?
Header:   "Drafting mode"
Options:
  - Label:       "Dynamic Workflow"
    Description: "A Claude Code workflow drafts independent sections in parallel, then runs spec + manuscript review as a pipeline. Best for multi-section papers."
  - Label:       "Manual Batch (executing-plans)"
    Description: "Batch execution across a separate or manual session with checkpoints. Best when workflows are unavailable or you want explicit per-batch review."
```

Recommend by heuristic:

- Multi-section paper, loosely-coupled sections, or heavy per-section lit search → Dynamic Workflow.
- User wants manual checkpoints across batches, or workflow support is unavailable → Manual Batch.

Then hand off:

- **Dynamic Workflow** → ask Claude to run a workflow (include the word "workflow" in the request) or turn on `/effort ultracode`. The workflow drafts each section with the `superpower-writing:section-drafter` agent (the per-section prompt below is its task body), then pipes each drafted section through `superpower-writing:spec-reviewer` (outline/claim alignment) and `superpower-writing:manuscript-reviewer` (writing quality). Independent sections run in parallel; the claim-first PreToolUse hook fires on every write. The two-stage review contract — gate order, 3-round cap, and the plan-alignment gate — is specified in `skills/planning-foundation/references/review-loop-protocol.md`.
- **Manual Batch** → `Skill(skill="superpower-writing:executing-plans")` in a separate or manual session, using the same `section-drafter` prompt body and the same two-stage review (`spec-reviewer` then `manuscript-reviewer`) at each batch checkpoint.

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
     No section-specific standard applies; use general IMRAD conventions from writing-principles.md.
     ```

  The canonical filenames in `section-standards/` are `00_abstract.md`, `01_introduction.md`, `02_background.md`, `03_methods.md`, `04_results.md`, `05_discussion.md`, `06_conclusion.md`, `07_related_work.md`, `08_motivation.md`. See [`references/section-standards/README.md`](references/section-standards/README.md) for the full contract.

Whichever execution path runs (dynamic workflow or manual batch), it layers its review gates on top of this body without modifying Steps A–C. Section standards are data injected into the prompt, not another gate in the pipeline — both paths resolve them the same way.

### 3. Graphical abstract and schematics

Systems papers usually carry at least one schematic figure (architecture / data-flow / pipeline). A graphical abstract is **optional** — include one only when the venue or author explicitly requests it; most CS/systems venues omit it. Do not attempt to draw either with prose tools.

- For the graphical abstract (when the paper includes one):

  ```
  Skill(skill="superpower-writing:scientific-schematics")
  Output: .writing/figures/graphical_abstract.png
  Caption: write into .writing/figures/graphical_abstract.md (caption only)
  ```

  Treat this as its own "section task" in the plan, not a sub-step of a prose section. Route it through whichever mode was chosen in step 1 — the `scientific-schematics` call is the implementer's responsibility, not this skill's.

- For additional schematics referenced in Methods or Results:

  One `scientific-schematics` invocation per figure. The prose paragraph that introduces the figure still needs a `% claim: id` tag pointing at whatever claim the figure supports (usually a mechanism or pipeline claim). The figure file itself goes to `.writing/figures/<slug>.pdf` (LaTeX prefers PDF/EPS vector formats) and is not subject to the PreToolUse hook (the matcher only covers `manuscript/*.tex`).

### 4. Progress tracking after each section

After each section returns (drafted and committed), the orchestrator updates `.writing/progress.md` Task Dashboard. Expected columns:

| Section / Figure | Status | Spec Review | Manuscript Review | Plan Align | Claim Verification | Key Outcome |
|------------------|--------|-------------|-------------------|------------|--------------------|-------------|
| 02_methods | drafted | PASS | PASS | PASS | 5/5 evidence_ready | 1247-patient T2D cohort described |

Set:

- **Status**: `drafted` once prose is committed. `verified` is reserved for claim-verification.
- **Spec Review / Manuscript Review / Plan Align**: filled by the two-stage review pipeline (and the plan-alignment gate) — the workflow runs it per section, the manual-batch path runs it at each checkpoint. See `skills/planning-foundation/references/review-loop-protocol.md`. Leave as `-` when no review gate applies.
- **Claim Verification**: ratio of `evidence_ready` or `verified` claims to total claims in that section's claims file. This is a lightweight count; the real check (DOI resolution / semantic matching) is the claim-verification skill.

If any claim remains `stub` (because of a `[NEEDS-EVIDENCE]` miss), set Status to `blocked: <count> unresolved` and surface to the user. Do NOT mark the section drafted while stubs remain in its prose.

### 5. Zotero integration

The Zotero-first / network-fallback / optional auto-push flow is fully specified in Step A of the section-drafter prompt. On runtime failures (rate limit, auth revoke mid-draft), treat the failing call as a Zotero miss, continue via `research-lookup` / `citation-management`, and log the failure to `.writing/findings.md` under "Issues" so the user can fix credentials between sections. `main` runs `${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh` at session start, so credentials are already verified by the time drafting begins.

## Key Principles

**Claim-first, always.** Evidence before prose is the central discipline of this plugin. The hook is the backstop, not the workflow — the workflow is Step A of the template. If drafting ever feels "fast" because a subagent skipped Step A, the hook will stop it and you will redo the work. Do it right the first time.

**Own the prompt; delegate orchestration.** This skill owns the per-section prompt template and the claim-first bookkeeping. Orchestration (parallelism, review gates, session management) is handled by a Claude Code dynamic workflow or, as a manual fallback, by `superpower-writing:executing-plans`.

**Section standards refine, never contradict.** The files under `references/section-standards/` prescribe section-specific skeletons (BPMRC for abstracts, and whatever conventions get added for introductions, methods, etc.). They are loaded verbatim into the drafter prompt so every section that has a standard gets the same treatment. When a standard and the outline disagree, the drafter escalates rather than silently picking one — drift between outline and draft is a structural bug, not a judgment call. Adding a new standard is a `section-standards/<stem>.md` file plus, optionally, an outline-level reference in the outlining skill; no orchestrator change is needed.

**Zotero miss is not a failure.** A DOI absent from the user's Zotero library just means the user has not yet vetted it. Network fallback is normal and expected. The only failure mode is "no credible source anywhere", which must be escalated.

**Figures are first-class tasks.** A graphical abstract is optional (systems papers usually omit it), but whenever the paper includes a graphical abstract or schematic, do not inline its generation into a prose section — route it through `superpower-writing:scientific-schematics` as its own task.

**Progress dashboard is the handoff contract.** `claim-verification` and the human author read `.writing/progress.md` to know what has been drafted, verified, or reviewed. A section is not "drafted" until its row is updated and committed.

**Do not fight the hook.** If `enforce-claims.sh` blocks a write, the hook is telling you the claim-first protocol was violated. Resolve the underlying cause (missing claim entry, stub STATUS, untagged paragraph). Never propose disabling the hook or bypassing it with a sneaky `MultiEdit`.

**Locked-term renames are not prose edits.** If the user or a sub-agent proposes renaming a term that is already locked in `.writing/progress.md` naming decisions, in `.writing/outline.md` bullet labels, or in prior drafted prose across multiple manuscript files, do NOT silently apply the edit. Treat it as a cross-file rename: grep every `.writing/manuscript/`, `.writing/outline.md`, and `.writing/findings.md` file for the old term, update them together in one pass, and record the rename in `.writing/findings.md` so the audit trail survives. The drafting skill handles prose within an agreed spec; renames cross the prose/spec boundary and need an audit of which files mention the old term and an explicit findings.md entry so the planning-file audit trail survives the rename. Applying a locked-term rename as if it were a single-file edit silently desynchronizes the manuscript from its naming history.

**Define terms before they flow across sections.** When `.writing/glossary.md` is present, the companion `enforce-terms.sh` hook blocks writes that use a term in a section before the section declared as its definition site. The fix is the same shape as the claim protocol: add or update the glossary entry, move the `% define: <id>` to the right section, or reorder sections so the term lands before its first use. `% use: <id>` is an **opt-in** annotation — you only tag the uses you want the hook to verify. An untagged occurrence of the term is not checked, so this remains a lightweight discipline rather than a universal requirement.

## Style cautions for section intros and argumentative prose

Seven patterns slip past outline compliance and prose-quality review because they look locally fluent but corrupt the paper's structure or invite reviewer attacks. The canonical rules, verbatim before/after example, and scanning checks live at [`references/style-cautions.md`](references/style-cautions.md); the drafter prompt template loads that file at write time, and both reviewer agents paraphrase it with added severity and flagging context — keep the three wordings in sync when any rule changes (see the reference's "Loaded by" block).

At a glance:

- **Overview paragraph discipline** — for opening paragraphs that preview their own subsections. No mechanism spoilers, no prominence labels on peer subsections (`central insight`, `extension`, etc.), sweep peer items on every fix.
- **Section responsibility discipline** — each IMRAD section has a narrow job; numbers must not drift across boundaries. Placement test: "could a third party independent of our system compute this from the raw data alone?" Yes → ground/workload; no → results.
- **No dataset pre-hedging in argumentative prose** — `on X dataset` or `in our workload` inside thesis sentences pre-narrows the claim. Allowed only where numbers are first reported and in the discussion's external-validity block.
- **Section intros foreground claims, not roadmaps** — replace `The remaining subsections discuss X, Y, Z` with a claim-first thesis; subsection pointers become parenthetical `\S\ref{...}`. Reference file has the verbatim before/after.
- **Forward-reference discipline in intros** — a section's intro must not use technical terms defined only later in the same section.
- **Results topic and closing sentences carry qualitative conclusions** — first sentence states the qualitative answer to the RQ, last sentence states the design or scientific implication, middle carries numbers and methodology. Reading first+last pairs end-to-end across the section should yield a defensible standalone narrative.
- **Multi-corpus results are parallel, not anchored** — list corpora as peers (`X% on A, Y% on B, ..., over n_A, n_B, ... respectively`); the connector `the same comparison reproduces this structure on the other corpora` is a retrofitting tell and should be replaced with a single parallel listing.

## Integration

- `superpower-writing:writing-plans` — produces `.writing/plan.md`; drafting reads it verbatim.
- `superpower-writing:claim-verification` — downstream; consumes `.writing/manuscript/*.tex` and confirms every claim tag.
- `superpower-writing:executing-plans` — manual-batch execution fallback; the primary path is a Claude Code dynamic workflow that drafts sections in parallel and reviews them in a pipeline.
- Plugin-local `writing-principles.md` — voice and structure rules.
- Plugin-local `superpower-writing:scientific-schematics` — graphical abstract + schematics.
- Plugin-local `superpower-writing:research-lookup`, `superpower-writing:citation-management` — evidence resolution (network).
- Plugin-level `.mcp.json` `zotero` server — Zotero Web API tools. Search: `zotero_search_items` (DOI / title lookup), `zotero_semantic_search` (AI similarity search with paragraph-level matching over PDF fulltext). Read: `zotero_get_item_metadata` (markdown or BibTeX), `zotero_get_item_fulltext` (server-side PDF text — use sparingly, often 70K+ chars; prefer `zotero_semantic_search` to find relevant chunks first). Write: `zotero_add_by_doi` (auto-fetches metadata + open-access PDF). Collection nav: `zotero_get_collections`, `zotero_get_collection_items`.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` — PreToolUse enforcement of the claim-first protocol.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-terms.sh` — opt-in PreToolUse enforcement of term-definition-before-use ordering. Activates when `.writing/glossary.md` is present.
