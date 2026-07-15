---
name: drafting
description: Use when turning an approved outline and its claim stubs into LaTeX manuscript prose, writing each section's paragraphs under the claim-first discipline (resolve evidence, then write `% claim: id`-tagged prose). Reads the per-section writing standards, style cautions, and terminology ledger. Trigger after outlining, when `.writing/manuscript/*.tex` is empty or a section still needs prose; before claim-verification and polish. Also trigger on "draft the paper", "write the Methods section", "turn the outline into prose".
---

# Drafting

Turn claims into sentences. You draft each section yourself, in outline order, no mode selection, no parallel subagents, no review pipeline. The hard rule is **claim-first**: no prose may cite a claim whose `STATUS` is still `stub`. Resolve evidence, then write.

**Announce at start:** "I'm using the drafting skill to write manuscript prose."

## Preconditions

Draft only once outlining has produced:

- `.writing/outline.md` (approved) and `.writing/claims/section_*.md` (stub entries per section).
- `.writing/metadata.yaml` filled (note `writing_profile`, `zotero.enabled`, `zotero.auto_push_new_citations`).
- `.writing/manuscript/` exists (from `init-writing-dir.sh`).

Skip this skill to copy-edit existing prose (use `polish`) or to verify a finished draft (use `claim-verification`).

## The protocol

Read [`references/claim-first.md`](references/claim-first.md) and follow it for every section. It is the load-bearing doorway to the rest of the writing references, so read it before your first section. In short, per section:

1. **Resolve evidence first (Step A).** For each `STATUS: stub` claim, resolve its source Zotero-first, then via `superpower-writing:literature` / `superpower-writing:citations` as fallback. Advance to `evidence_ready`. No prose until every claim in the section is resolved.
2. **Write LaTeX prose (Step B).** Tag each load-bearing paragraph `% claim: id` (or `% draft-only`) at column 0. Never invent citekeys.
3. **Bookkeeping (Step C).** Quick self-read, update `.writing/progress.md`, commit. The exhaustive mechanical sweep is `claim-verification`'s job, not a gate to rebuild here.

## Writing standards (read as guidance, not gates)

- **Per-section shape.** For each section read the matching `references/section-standards/<slug>.md` (resolve by slug-ending). It describes paragraph shape, required structural tags, tense and length. Treat it as guidance that refines `references/writing-principles.md`; if it genuinely conflicts with the outline, surface the conflict rather than silently picking one.
- **Terminology ledger.** Before the first section, build the canonical-term table from [`../_shared/core/terminology-ledger.md`](../_shared/core/terminology-ledger.md): one name per thing across sections. Surface collisions and let the user pick; never coin a name to fill a gap.
- **Style cautions.** Read [`references/style-cautions.md`](references/style-cautions.md) before writing any section intro, overview paragraph, or thesis sentence, and clear its scans.
- **Systems papers.** When `metadata.yaml` has `writing_profile: systems`, read [`references/systems-evidence-contract.md`](references/systems-evidence-contract.md) for structured `analysis`/`artifact` evidence and the Results/Discussion boundary.

## Figures

Figures are their own tasks, not inlined into a prose section. Dispatch per type and `\input`/`\includegraphics` the result:

- Structural (architecture / flowchart / pipeline / timeline) → `superpower-writing:tikz-figures`.
- Data plots (bars / scaling / heatmap / cost curves) → `superpower-writing:scientific-visualization`.
- Pictorial concept art or a graphical abstract (systems papers usually omit it) → `superpower-writing:scientific-schematics`.

The prose paragraph that introduces a figure still carries a `% claim: id` tag for the claim it supports; figure files themselves carry no claim tags. See [`references/figures-and-tables.md`](references/figures-and-tables.md).

## After drafting

Hand the manuscript to `superpower-writing:claim-verification` (mechanical evidence + citation check), then `superpower-writing:polish` (prose quality).

## Key principles

**Claim-first, always.** Evidence before prose is the plugin's central discipline, not an optional gate. If drafting ever feels fast because you skipped evidence resolution, the gap resurfaces at claim-verification and you redo the work.

**You draft inline.** A strong model writes the sections directly. There is no orchestration to configure and no subagent to dispatch, the value here is the discipline and the standards, not a pipeline.

**Locked-term renames cross the prose/spec boundary.** If a rename touches a term already locked in `.writing/progress.md`, `outline.md`, or prior drafted prose, do not apply it as a single-file edit. Grep every `.writing/manuscript/*.tex`, `outline.md`, and `findings.md`, update them together, and record the rename in `findings.md` so the audit trail survives.

**Define terms before use.** When `.writing/glossary.md` is present, do not use a term before its declared definition section; fix by moving the `% define: <id>` or reordering sections.
