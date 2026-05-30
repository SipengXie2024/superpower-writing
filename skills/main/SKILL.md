---
name: main
description: Router and dependency gate for superpower-writing. Loaded at session start. Verifies bundled domain skills are installed, routes between outlining/writing-plans/drafting/claim-verification based on stage in .writing/progress.md. Produces a detailed evidence-backed skeleton for human refinement. Use when the user starts an academic-writing task (paper, manuscript, IMRAD draft, skeleton).
---

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a writing skill applies to your task, you MUST invoke it. No exceptions, no rationalizations.

This plugin is self-contained. Domain content (writing principles, figures/tables, citation styles) lives in plugin-local reference files under `skills/drafting/references/`. Skills that were previously upstream (`research-lookup`, `citation-management`, `literature-review`, `scientific-schematics`, `scientific-visualization`) now ship as plugin-local skills invoked with the `superpower-writing:` prefix — e.g. `Skill(skill="superpower-writing:research-lookup")`.
</EXTREMELY-IMPORTANT>

## Announce on Entry

When this skill is first invoked in a session, say exactly:

> "I'm using the superpower-writing main skill to route this task."

Then perform the dep check and `.writing/` detection below before doing anything else.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you — follow it directly. Never use the Read tool on skill files.

**Upstream vs local naming:**

- Local (this plugin): `Skill(skill="superpower-writing:drafting")` — prefixed.
- Plugin-local domain skills: `Skill(skill="superpower-writing:research-lookup")`, `Skill(skill="superpower-writing:citation-management")`, etc. — prefixed with `superpower-writing:`. These ship with this plugin.
- Execution: large parallel drafting and cross-section review run as a Claude Code **dynamic workflow** (ask Claude to run a workflow — include "workflow" in the request — or turn on `/effort ultracode`). `Skill(skill="superpower-writing:executing-plans")` is the manual-batch fallback. Both ship with this plugin; no sibling-plugin dependency.

# Dependency Gate (HARD)

Before any routing, confirm dependencies. These are **hard gates, not advisory**.

## Step 1: Upstream Skills Check

Run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh
```

This probes the plugin's own `skills/` directory first (the bundled domain skills ship there), then legacy Agent Skills install locations for back-compat. Required: `literature-review`, `citation-management`, `research-lookup`, `scientific-schematics`, `scientific-visualization`, plus a PyYAML probe for the claim hook.

**On non-zero exit:** refuse all subsequent superpower-writing skill invocations and surface the script's output verbatim — it names the missing dependency and the fix. A missing bundled skill means the plugin install is incomplete (re-clone or reinstall the plugin); a missing `pyyaml` is fixed with:

```
pip install --user --upgrade pyyaml
```

Do not proceed to outlining / drafting / anything. Silent degradation produces unverified manuscripts.

## Step 2: Zotero Credentials Check (conditional)

If `.writing/metadata.yaml` exists and parses with `zotero.enabled: true`, **also** run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh
```

This verifies `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`, and `ZOTERO_LIBRARY_TYPE` are set (from `.env` or the launching shell), that the `zotero-mcp` binary is on PATH, and that the Zotero Web API responds. **Hard-fail on non-zero exit** — do not fall back to network-only silently. If the user wants to disable Zotero, have them set `zotero.enabled: false` in `.writing/metadata.yaml`.

If `metadata.yaml` is absent or `zotero.enabled` is unset/false, skip this step.

## Step 3: `.writing/` Detection

Check for `.writing/` in the project root.

- **Absent and task is writing-related** (paper, manuscript, IMRAD draft, outline, abstract, methods section, skeleton, etc.): run

  ```bash
  ${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh
  ```

  This creates `outline.md`, `findings.md`, `progress.md`, `metadata.yaml`, `main.tex`, `refs.bib`, and subdirs `manuscript/ claims/ figures/ reviews/ archive/`.

- **Present:** read `.writing/progress.md` and `.writing/findings.md` to recover context before routing. Run `git diff --stat` to see manuscript changes since the last session.

- **Absent and task is not writing-related:** do nothing; yield to other skills.

# Session Recovery

When `.writing/` already exists at session start:

1. Read `.writing/progress.md` — Section/Figure dashboard shows current stage per section and which claims are stub vs evidence_ready vs verified.
2. Read `.writing/findings.md` — lit synthesis, prior decisions, reviewer context.
3. Read `.writing/metadata.yaml` — authors, preregistration, data/code availability, reporting guideline, Zotero config.
4. `git diff --stat -- .writing/` to see what changed since last session.
5. **Foot-gun check:** run `find .writing/manuscript -maxdepth 1 -name '*.md' -type f` — any `.md` file under `manuscript/` is a drafting mistake (the hook only enforces `.tex`). Warn the user and suggest renaming to `.tex` before continuing; do NOT silently proceed, since unenforced drafts accumulate unresolved claims.
6. Update planning files with any newly recovered context, then route based on the stage below.

# Stage Gate Routing

The writing lifecycle (skeleton-first — the plugin produces a detailed, evidence-backed skeleton for the human author to refine, not a submission-ready paper):

```
(dep-check) -> outlining -> writing-plans -> drafting -> claim-verification
                                                              |
                                            (skeleton ready for human refinement)
```

Each stage writes a dashboard row to `.writing/progress.md`. Route by inspecting the dashboard:

| Current state in `.writing/progress.md` | Missing artifact | Next skill to invoke |
|------------------------------------------|------------------|----------------------|
| No dashboard yet, `outline.md` empty | outline + claims stubs | `superpower-writing:outlining` |
| Outline present, `metadata.yaml` still has TODOs | metadata completeness | `superpower-writing:outlining` (complete metadata before advancing) |
| Outline + metadata complete, no `plan.md` | per-section/figure plan | `superpower-writing:writing-plans` |
| `plan.md` present, `manuscript/*.tex` empty or partial | prose | `superpower-writing:drafting` |
| Draft complete, no `verify-report.md` or report has failures | evidence audit | `superpower-writing:claim-verification` |
| All sections drafted, claim-verification PASS, no unresolved `[NEEDS-EVIDENCE]` or `% draft-only` | skeleton ready | done — hand the evidence-backed skeleton to the human author for refinement |

Skipping a gate (e.g., jumping from outline directly to drafting without writing-plans) requires explicit user override, surfaced as a warning.

# Planning Approach Routing

When the user starts a non-trivial writing task (multi-section paper, multi-day project, significant structural decisions), do NOT auto-enter plan mode or auto-invoke brainstorming. Present the choice via `AskUserQuestion`:

**Option 1: Quick Plan (Plan Mode)** — Lightweight read-only exploration. Best for a medium-scope task with known IMRAD shape, quick alignment on scope before outlining.

**Option 2: Structured Brainstorming** — Full pipeline: `superpower-writing:brainstorming` (design doc) → `superpower-writing:spec-interview` (refinement) → `superpower-writing:outlining` (IMRAD structure + claims). Best for a new research manuscript, complex methods, multi-study papers, or when the narrative arc is still unclear.

**Option 3: Stash Current Work** — Pause an in-progress paper safely; move `.writing/` (except `archive/`) into `.writing/stash/<paper-name>/`. Best when switching to a different paper, awaiting co-author input, or waiting on external data.

**When to skip this choice:**
- Trivial edits (fix a typo, tweak one sentence) → just do it.
- User explicitly asks for one mode ("let's brainstorm", "/outline") → honor it.
- Already mid-brainstorm or mid-outline → continue the current flow.

**After Plan Mode completes:** If the approved plan reveals complex work (3+ sections, figures, multi-round lit review), suggest transitioning to `superpower-writing:writing-plans` for a formal decomposition plan. Plan-mode output feeds the plan — reference it, don't re-derive.

# Execution Routing

When the user says "execute the plan", "start drafting", "write the paper", "implement the sections", do NOT directly invoke a single execution skill. Instead:

1. If no plan exists at `.writing/plan.md`, invoke `superpower-writing:writing-plans` — it produces `.writing/plan.md` directly (no further delegation; the writing-domain skill now owns the planning mechanics).
2. If a plan exists, present the execution strategy via `AskUserQuestion`:

   - **Claude Code Dynamic Workflow** (recommended for multi-section papers) — ask Claude to run a workflow that executes `.writing/plan.md` (include the word "workflow" in the request so Claude writes one), or turn on `/effort ultracode`. The workflow drafts independent sections in parallel with the `superpower-writing:section-drafter` agent, then runs the two-stage review as a pipeline — `superpower-writing:spec-reviewer` for outline/claim alignment, then `superpower-writing:manuscript-reviewer` for writing quality. It reads `.writing/plan.md`, `.writing/outline.md`, and `.writing/findings.md`, and writes drafted prose, progress, and findings back into `.writing/`. The claim-first PreToolUse hook still fires on every section write.
   - **Manual Batch Session** → `superpower-writing:executing-plans`, for a separate or manual session that drafts plan batches and stops at checkpoints. Best when workflows are unavailable or the user wants explicit per-batch review.

3. Recommend based on paper shape: many loosely-coupled sections, heavy per-section lit search, or a long paper → Dynamic Workflow; the user wants manual checkpoints across days or workflow support is unavailable → Manual Batch Session.

Drafting mechanics (the per-section claim-first prompt, the Zotero-first evidence loop, the graphical-abstract dispatch) live in `superpower-writing:drafting`, which both paths invoke per section.

# Stash / Resume Routing

- **Stash current paper:** when the user says pause / set aside / switch papers / come back later → move everything except `.writing/archive/` into `.writing/stash/<paper-name>/`. Use `superpower-writing:stashing` for the mechanics; the `<paper-name>` label should match `metadata.yaml` `title` (slugified) or the user-provided name.

- **Resume a stashed paper:** when the user says resume / continue / pick up <paper>, move `.writing/stash/<paper-name>/*` back into `.writing/` (keeping any existing `archive/`). Run a **stale-findings check** before routing further: re-read `findings.md`, cross-check DOIs in claims against current Zotero/network state, flag any citations that have been retracted or updated since stash.

- **Multi-paper concurrency:** only one active paper at a time in `.writing/`. Other papers live under `.writing/stash/`.

# Skills Inventory

Skills in this plugin (all invoked as `superpower-writing:<name>`):

| Skill | Purpose |
|-------|---------|
| `superpower-writing:main` | This router. Loaded at session start. Dep gate + stage routing. |
| `superpower-writing:outlining` | Idea → IMRAD outline + per-section claim stubs + populated `metadata.yaml`. Combines design-exploration and spec-writing. |
| `superpower-writing:writing-plans` | Approved outline → executable per-section/per-figure/per-table task plan with dependency graph. Writes `.writing/plan.md`. |
| `superpower-writing:drafting` | Section-by-section prose writing via a dynamic workflow (parallel sections) or a manual batch session. Enforces claim-first protocol: each section subagent resolves EVIDENCE via `research-lookup` / `citation-management` **before** writing tagged prose. |
| `superpower-writing:claim-verification` | Evidence-reliability check. Walks every `% claim: id` LaTeX line comment, confirms `\cite{}` citekeys resolve against `.writing/refs.bib`, runs semantic match against abstracts to catch hallucinated or mismatched citations, optionally checks numeric/table consistency. Run on demand or when the skeleton is ready for the human author. |

Plugin-local domain skills (invoked with `superpower-writing:` prefix):

| Skill | Used by | Purpose |
|-------|---------|---------|
| `literature-review` | outlining, drafting, claim-verification | Structured lit synthesis. |
| `research-lookup` | drafting, claim-verification | Paper/abstract retrieval for evidence resolution. |
| `citation-management` | drafting, claim-verification | Citation formatting, DOI resolution, bibliography assembly. |
| `scientific-schematics` | drafting | Graphical abstracts and schematic figures (architecture / data-flow / pipeline diagrams). |
| `scientific-visualization` | drafting | Publication-ready data plots (CDFs, throughput curves, training curves, ablation bars, Pareto fronts) for IEEE / ACM / USENIX / NeurIPS / ICML / ICLR. CS-tailored. |
| `zotero-mcp` (MCP) | drafting, claim-verification, outlining | All Zotero calls when `zotero.enabled: true`. Registered in `.mcp.json`. Core tools: `zotero_search_items` (DOI / title / author lookup), `zotero_get_item_metadata` (markdown or BibTeX export), `zotero_get_item_fulltext` (server-side extracted PDF text, web-API mode supported), `zotero_semantic_search` (AI similarity search over the chunked library — paragraph-level matches when paper bodies are indexed), `zotero_advanced_search`, `zotero_get_collections` / `zotero_get_collection_items`, `zotero_add_by_doi` (auto-fetches metadata + open-access PDF). Scite citation intelligence via `scite_enrich_item` / `scite_enrich_search` / `scite_check_retractions`. |

# Claim-First Protocol

Every load-bearing paragraph in `.writing/manuscript/*.tex` must carry a LaTeX line-comment marker at column 0 (allowing leading whitespace):

- `% claim: <id>` — links to an entry in `.writing/claims/section_<NN>_<slug>.md` with fields `id`, `CLAIM`, `EVIDENCE`, `STATUS` ∈ {`stub`, `evidence_ready`, `verified`}.
- `% draft-only` — scratch prose that will be replaced before the next stage gate.

A **PreToolUse hook** (`${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh`) blocks any Edit / Write / MultiEdit / NotebookEdit targeting `**/manuscript/*.tex` when:

- a `% claim: id` tag references a claim with `STATUS: stub`, or
- the claim file is missing, or
- untagged load-bearing prose lands in a protected section.

The hook exempts any section stem whose slug is in `UNPROTECTED_SLUGS` (`abstract`, `references`, `acknowledgments`) from paragraph-tag enforcement. Slug match is by slug-ending: `00_abstract` matches `_abstract`; `09_references` matches `_references`; `10_acknowledgments` matches `_acknowledgments`. All other `manuscript/NN_*.tex` files require every load-bearing paragraph to carry `% claim: id` or `% draft-only`.

Markdown manuscript files (`.md` under `manuscript/`) are NOT intercepted — the plugin operates on LaTeX only. If a `.md` slips into `manuscript/`, it falls through unenforced; convert to `.tex` before claim-verification.

## Citation Placement Rule

The abstract is **citation-free**. `CITATION_FREE_SLUGS = {"abstract"}` in the hook — any stem ending in `_abstract` (e.g. `00_abstract.tex`) is blocked when the write contains any LaTeX citation command (`\cite`, `\citep`, `\citet`, `\nocite`, `\parencite`, `\textcite`, `\autocite`, `\footcite`, `\citeauthor`, `\citeyear`, `\citealt`, `\citealp`, or any `\*cite*` variant) or a `% claim: id` tag. The abstract is a self-contained summary of the paper's own findings; references belong in the body. Every body section (`01_introduction.tex`, `02_background.tex`, `03_methods.tex`, `04_results.tex`, `05_discussion.tex`, etc.) MUST back every load-bearing claim with a `\cite{citekey}` whose citekey resolves against `.writing/refs.bib`; missing citations surface as FAILs in `claim-verification` Pass 2.

Drafting and claim-verification skills must be aware of this hook and surface its block reason to the user. The fix is always: resolve EVIDENCE first (via `research-lookup` / `citation-management` / Zotero lookup), bump `STATUS` to `evidence_ready`, then write prose.

# User Instructions

Instructions say WHAT, not HOW. "Add a methods paragraph" or "tighten the abstract" doesn't mean skip workflows. Always:

1. Dep gate (check-deps + check-zotero when enabled).
2. `.writing/` recovery or init.
3. Stage-appropriate routing per the table above.
4. Plugin-local skills for domain content and orchestration.
5. Claim-first protocol enforced by the PreToolUse hook — don't try to bypass it.
