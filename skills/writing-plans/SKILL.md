---
name: writing-plans
description: Decomposes an approved outline into executable per-section/per-figure/per-table tasks with dependency graph. Output is .writing/plan.md. Use after outlining produces .writing/outline.md and before drafting begins.
---

# Writing Plans

## Overview

Convert an approved IMRAD outline into an executable task list for drafting. Input: `.writing/outline.md` (structure + key claims), `.writing/metadata.yaml` (reporting guideline + Zotero config), `.writing/claims/section_*.md` (stub claims per section). Output: `.writing/plan.md` — the single source of truth for drafting. The plan enumerates per-section prose tasks, per-figure generation tasks, per-table assembly tasks, an explicit dependency table, and a Parallelism Groups analysis that the drafting skill consumes when the user picks serial vs parallel mode.

**Announce at start:** "I'm using the writing-plans skill to decompose the outline into an executable plan."

**Save plan to:** `.writing/plan.md`

**Relation to the code-side `superpower-planning:writing-plans` skill:** identical philosophy (bite-sized tasks, file-path precision, explicit parallelism groups, self-review), adapted to manuscripts. Task unit is the section/figure/table, not the source file. The TDD analog is the claim-first protocol enforced by `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` during drafting — plan steps that write prose always pair with a claim-resolution step first.

## When to Use

- `outlining` skill has produced `.writing/outline.md` and stub `claims/section_*.md` files, and the user is ready to draft.
- User explicitly requests "make a writing plan", "decompose sections into tasks", "/writing:plan".
- At the start of a revision round when the review introduces new sections or substantially new claims — re-plan the impacted subset rather than re-planning the whole paper.

Do NOT invoke this skill before outlining completes. A missing or TODO-laden outline means the plan has nothing to bind to — abort and route back to `outlining`.

## Checklist

- [ ] Preconditions verified: `.writing/outline.md`, `.writing/metadata.yaml` (no TODO), `claims/section_*.md` all exist
- [ ] File structure locked: manuscript/ filenames enumerated with their stems matching claims/
- [ ] Per-section tasks written (draft + verify-claims + internal-review triplet per section)
- [ ] Per-figure tasks written (one per schematic; delegates to `scientific-schematics`)
- [ ] Per-table tasks written
- [ ] Dependency table written (Methods → Results; Intro ↔ Discussion loose coupling; Abstract last)
- [ ] Parallelism Groups analysis written
- [ ] Self-review run inline (spec coverage, placeholder scan, type consistency, evidence gaps)
- [ ] Hand-off to `drafting` skill via AskUserQuestion (serial vs parallel vs separate-session)

## Process

### Step 1: Verify preconditions

Stop and route back to the correct upstream skill if any precondition fails:

1. `.writing/outline.md` exists and is non-empty. If missing → route to `outlining`.
2. `.writing/metadata.yaml` has no `TODO` top-level keys (except multi-author v1 YAGNI list). If TODO present → instruct user to finish outlining/metadata pass first.
3. `.writing/claims/` contains one `section_<NN>_<slug>.md` per section listed in outline.md. If missing → route to `outlining`.
4. `.writing/manuscript/` subdir exists (created by `init-writing-dir.sh`).

### Step 2: File-structure pass

Before task decomposition, list the exact manuscript files the plan will write to. One file per IMRAD section, default layout:

```
.writing/manuscript/
  00_abstract.md
  01_introduction.md
  02_methods.md
  03_results.md
  04_discussion.md
  05_conclusion.md
  06_references.md
```

Optional sections (Supplementary, Acknowledgments, Data Availability Statement) appear only if the outline calls for them. Each `NN_slug.md` pairs 1:1 with `claims/section_NN_<slug>.md` — stems match exactly. File-structure pass output goes into the plan header so readers see the write set before tasks.

### Step 3: Write the plan document

Use this exact header template:

```markdown
# <Paper working title> — Writing Plan

> **For Claude:** Execute this plan via the drafting skill using the mode chosen in Execution Handoff (serial or parallel).
> Writing dir: .writing/

**Goal:** Draft a submission-ready IMRAD manuscript covering <one-sentence paper thesis from outline.md>.

**Architecture:** Section-per-file under `.writing/manuscript/`, claim-first drafting enforced by PreToolUse hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh`, figures delegated to `scientific-schematics`, citations resolved through the Zotero→network dual source of truth configured in `metadata.yaml`.

**Reporting guideline:** <CONSORT | STROBE | PRISMA | ARRIVE | none> (from metadata.yaml).

---

## File Write Set
<bulleted list of manuscript/*.md and figures/*.svg|png the plan produces>

---

## Tasks
<per-section / per-figure / per-table tasks — see templates below>

---

## Dependencies
<table>

---

## Parallelism Groups
<analysis>

---

## Self-Review
<inline checklist>

---

## Execution Handoff
<three options via AskUserQuestion>
```

### Step 4: Per-section task template (repeat for each IMRAD section)

Each section is a three-step triplet: draft, verify-claims, internal-review. Do NOT write prose in the plan itself — the plan enumerates tasks; drafting writes prose. Use this exact template per section:

````markdown
### Task M.1: Draft Methods

**Files:**
- Read: `.writing/outline.md` §Methods, `.writing/claims/section_02_methods.md`, `.writing/metadata.yaml`
- Write: `.writing/manuscript/02_methods.md`

**Preconditions:**
- Every claim in `claims/section_02_methods.md` is STATUS=evidence_ready (drafting flips stub → evidence_ready; PreToolUse hook blocks writes otherwise).

- [ ] **Step 1: Resolve evidence for each stub claim**

  For each claim in `claims/section_02_methods.md` with `STATUS: stub`:
  - For `type: citation` EVIDENCE → call `Skill(skill="citation-management")` then `Skill(skill="research-lookup")` (Zotero-first if `metadata.yaml zotero.enabled: true` — call `Skill(skill="pyzotero")` first).
  - For `type: dataset` → confirm the dataset identifier resolves (e.g., open the referenced URL/DOI).
  - For `type: figure` or `type: table` → confirm the artifact is scheduled in a figure/table task in this plan.
  - Flip STATUS to `evidence_ready` once every EVIDENCE entry is resolved.

- [ ] **Step 2: Draft prose via scientific-writing**

  Invoke `Skill(skill="scientific-writing")` with:
  - section: Methods
  - outline excerpt: <copy from outline.md>
  - claims: <load claims/section_02_methods.md>
  - metadata: `.writing/metadata.yaml`

  Each load-bearing paragraph MUST be prefixed with `<!-- claim: <id> -->` matching a claim id. Exploratory text uses `<!-- draft-only -->`. The PreToolUse hook will block the Write tool if a paragraph references a stub-status claim.

- [ ] **Step 3: Commit**

  ```bash
  cd <project root>
  git -c user.email=sipeng@local -c user.name=sipeng add .writing/manuscript/02_methods.md .writing/claims/section_02_methods.md
  git -c user.email=sipeng@local -c user.name=sipeng commit -m "draft: methods section"
  ```

### Task M.2: Verify Methods claims

**Files:**
- Read: `.writing/manuscript/02_methods.md`, `.writing/claims/section_02_methods.md`
- Write: `.writing/verify-report.md` (append section), update `STATUS` in claims file.

- [ ] **Step 1: Invoke `Skill(skill="claim-verification")` scoped to Methods**

  Run the four-pass verifier on Methods only (completeness, citation resolution dual source, numeric/table consistency, reporting-guideline subset). On all-pass, flip eligible claims `evidence_ready` → `verified`.

- [ ] **Step 2: Commit**

  ```bash
  git -c user.email=sipeng@local -c user.name=sipeng add .writing/claims/section_02_methods.md .writing/verify-report.md
  git -c user.email=sipeng@local -c user.name=sipeng commit -m "verify: methods claims"
  ```

### Task M.3: Internal review of Methods

**Files:**
- Read: `.writing/manuscript/02_methods.md`, `.writing/verify-report.md`
- Write: `.writing/reviews/internal_methods_<date>.md`

- [ ] **Step 1: Invoke `Skill(skill="peer-review")` as co-author reviewer**

  Prompt the skill to produce Major/Minor/OutOfScope comments against Methods prose. Store the output under `.writing/reviews/internal_methods_<ISO-date>.md`.

- [ ] **Step 2: If review raises Major issues, route to `revision` skill**

  `revision` handles intake → classify → respond-per-item → apply-diff → re-verify. This skill does NOT apply diffs itself.

- [ ] **Step 3: Commit review file**

  ```bash
  git -c user.email=sipeng@local -c user.name=sipeng add .writing/reviews/
  git -c user.email=sipeng@local -c user.name=sipeng commit -m "review: internal review of methods"
  ```
````

Repeat the triplet (draft / verify / review) for each section: Introduction (I), Methods (M), Results (R), Discussion (D), Conclusion (C), Abstract (A). Numbering scheme: `<letter>.1` draft, `<letter>.2` verify, `<letter>.3` review.

### Step 5: Figure tasks

For each figure listed in outline.md (plus the mandatory graphical abstract per upstream `scientific-writing`):

````markdown
### Task F<n>: Figure <n> — <short name>

**Files:**
- Read: `.writing/outline.md` §Figures, relevant `claims/*.md` entries of `type: figure`
- Write: `.writing/figures/fig<n>_<slug>.svg` (or `.png`) + `.writing/figures/fig<n>_<slug>_caption.md`

- [ ] **Step 1: Delegate generation to `Skill(skill="scientific-schematics")`**

  Provide: figure spec from outline, data reference from claims, required style (e.g., journal target format), and requested output format (SVG for schematics, PNG for data plots).

- [ ] **Step 2: Write caption to `fig<n>_<slug>_caption.md`**

  Caption is plain Markdown; it will be inlined into the relevant manuscript section via `![Fig n. ...](../figures/fig<n>_<slug>.svg)` when drafting runs.

- [ ] **Step 3: Update matching claims to reference the generated asset**

  For every claim with `type: figure` and `ref: fig<n>_<slug>`, confirm the artifact now exists on disk. This allows Pass 2d of claim-verification to succeed.

- [ ] **Step 4: Commit**

  ```bash
  git -c user.email=sipeng@local -c user.name=sipeng add .writing/figures/
  git -c user.email=sipeng@local -c user.name=sipeng commit -m "figure: fig<n> <slug>"
  ```
````

The graphical abstract is mandatory — always emit a Task F0 for it regardless of outline.

### Step 6: Table tasks

For each table listed in outline.md:

````markdown
### Task T<n>: Table <n> — <short name>

**Files:**
- Read: source data (dataset id or analysis script output referenced by outline.md)
- Write: Markdown table embedded in the owning section file (e.g., `.writing/manuscript/03_results.md`) or a standalone `.writing/tables/tab<n>_<slug>.md` included via transclusion.

- [ ] **Step 1: Build the table**

  Prefer embedding Markdown pipe tables directly in the owning section. Only break out to `tables/tab<n>_<slug>.md` when the table exceeds ~40 rows or is reused across sections.

- [ ] **Step 2: Ensure every numeric cell appears in a claim or a footnote**

  Numbers in tables are the ground-truth pool for Pass 3 of claim-verification. If a table cell introduces a new number not attested in a claim, either: (a) add a new claim stub to the matching `claims/section_*.md`, or (b) footnote the cell with its source.

- [ ] **Step 3: Commit**

  ```bash
  git -c user.email=sipeng@local -c user.name=sipeng add .writing/manuscript/ .writing/tables/ .writing/claims/
  git -c user.email=sipeng@local -c user.name=sipeng commit -m "table: tab<n> <slug>"
  ```
````

### Step 7: Dependency table

Write this table in the plan. It encodes which tasks block which, mirroring the IMRAD causal chain:

```markdown
## Dependencies

| Task | Blocks | Rationale |
|------|--------|-----------|
| M.1 Draft Methods | R.1 Draft Results | Results reference Methods procedures; Methods must exist first. |
| M.1 Draft Methods | F<n> Figures that depict methodology | Figure captions cite Methods paragraphs. |
| R.1 Draft Results | D.1 Draft Discussion | Discussion interprets Results. |
| F<n> (data figures) | R.1 Draft Results | Results inline data figures; figure assets must exist first. |
| F0 Graphical Abstract | A.1 Draft Abstract | Graphical abstract often informs abstract framing. |
| I.1 Draft Introduction | D.1 Draft Discussion | Discussion closes loops opened in Introduction (shadow dependency — not hard). |
| All section drafts | A.1 Draft Abstract | Abstract summarizes the whole paper; draft last. |
| All section verifies | submission | Submission gate refuses if any claim is not STATUS=verified. |
```

The `I.1 → D.1` edge is marked "shadow dependency" because Introduction and Discussion can be drafted concurrently in parallel mode — but the user should expect a pass-two edit of Introduction after Discussion lands, since Introduction sets up loops that Discussion closes.

### Step 8: Parallelism Groups

After the dependency table, write an explicit parallelism analysis. Drafting mode selection hinges on this.

```markdown
## Parallelism Groups

- **Group P0** (serial, blocks everything): precondition check + file-structure confirmation.
- **Group P1** (parallel, <k> tasks): M.1 Draft Methods, I.1 Draft Introduction, F0 Graphical Abstract, T<n> data-only tables (those not dependent on Results interpretation).
- **Group P2** (parallel, after P1): F<data-figures> Figures, R.1 Draft Results.
- **Group P3** (parallel, after P2): D.1 Draft Discussion, C.1 Draft Conclusion.
- **Group P4** (serial, after P3): A.1 Draft Abstract (summarizes everything).
- **Group P5** (parallel per section, after each draft): verify-claims tasks (M.2, R.2, D.2, …).
- **Group P6** (parallel per section, after verify): internal-review tasks (M.3, R.3, …).

**Parallelism score:** <N> of <Total> tasks run in parallel groups; max width <K> in Group P2.
```

**Tips for maximizing parallelism:**
- Introduction and Methods share no claim overlap → always parallel.
- Figures can run in parallel with Results *only* if the figures do not depend on yet-to-be-written Results interpretation; outline.md should have pre-computed whether each figure is data-driven (parallelizable) or interpretation-driven (serial after R.1).
- Verify-claims and internal-review are per-section independent.

### Step 9: Self-Review (inline)

Run these checks before calling the plan done. Fix issues inline, no re-review.

1. **Spec coverage:** Does every section listed in `.writing/outline.md` have a draft / verify / review triplet? Does every figure in the outline have a matching F<n> task? Does every table? Does the graphical abstract have a task? List gaps and fix.
2. **Placeholder scan:** No `TBD`, `TODO`, `add appropriate X`, `similar to task Y`, or `fill in details`. Every task names exact files it reads and writes.
3. **Type consistency:** The claim ids used in the prose-drafting steps must match the ids declared in `claims/section_*.md` files produced by outlining. Section numbering (`02_methods`) must match across the plan.
4. **Evidence gaps:** If `.writing/outline.md` carries `[NEEDS-EVIDENCE]` markers (e.g., a specific cohort size still to confirm), write an Evidence Gap Summary table: decision, evidence needed, timing, owning task.

If any check fails, fix inline. Do not emit a plan with known gaps.

### Step 10: Hand-off via AskUserQuestion

Present exactly three options for execution. Recommend based on parallelism score but never omit options.

- **Option 1: Serial / Subagent-Driven drafting** — one subagent per section, two-stage review (spec + quality) inline. Best for short papers (≤4 sections with prose) or when sections share heavy context. Invokes `Skill(skill="drafting")` with `mode: serial`.
- **Option 2: Parallel / Team-Driven drafting** — Agent Team spawns N section drafters plus a dedicated reviewer. Best when parallelism score is high and sections are loosely coupled. Invokes `Skill(skill="drafting")` with `mode: parallel`.
- **Option 3: Separate-session drafting** — open a new session in this working directory, invoke `Skill(skill="drafting")` there with `mode: session-handoff`. Best when the user wants manual per-section checkpoints.

**Recommendation logic:**
- Parallelism score ≥ 60% AND section count ≥ 5 → recommend Parallel.
- Section count ≤ 3 → recommend Serial.
- User explicitly wants checkpoints → recommend Separate-session.

After user choice, invoke `Skill(skill="drafting")` with the selected mode and the path to `.writing/plan.md`.

## Key Principles

### Task unit is the artifact, not the file

Code plans think in files. Writing plans think in sections/figures/tables — each is a research artifact with its own verification contract. A single section task still touches a single file, but the Why of the task is the artifact (this argument, this figure, this claim set), not the file path.

### Claim-first is the TDD analog — bake it in

Every draft task's Step 1 must be "resolve claim evidence" before Step 2 "write prose". The PreToolUse hook enforces this at the harness level, but a good plan preempts it by sequencing evidence resolution ahead of the Write tool call. A plan that lists Step 1 as "write Methods prose" will be blocked by the hook and the user will blame the plan, not their skipped evidence work.

### Dependencies encode causal order, not just file order

Methods blocks Results because the scientific argument requires it — not because they happen to share a claim file. The dependency table makes this explicit so the parallelism analysis downstream reflects real constraints, not accidental file ordering.

### Parallelism score is an honest number

Do not inflate parallelism by declaring tasks parallel that really share context. Introduction and Methods are genuinely parallel (disjoint claim sets, disjoint literature). Results and Discussion are NOT parallel — Discussion interprets Results. Be honest; downstream drafting mode selection depends on this being accurate.

### The plan does not write prose

This skill is a planner. It never invokes `scientific-writing` itself. Every prose-writing Step appears in a task that `drafting` will execute later. Keep the separation clean: plans are orchestration, drafting is production.

### Shadow dependencies (I ↔ D) are loose, not hard

Introduction and Discussion reference each other thematically — Intro opens loops, Discussion closes them. In serial mode, always draft I → M → R → D → A. In parallel mode, allow I and D to start concurrently but expect a pass-two Intro edit after Discussion lands. Plans in parallel mode must schedule this edit as an explicit R.4 / I.4 touch-up task.

### Separate `.planning/` from `.writing/`

This plan lives at `.writing/plan.md`, NOT `.planning/plan.md`. `.planning/` (if present) belongs to superpower-planning's code-side work. `.writing/` is the single persistent-state directory for this plugin. Keep them separated — a paper project may sit inside a code project and both must coexist.

### Hand-off is mandatory

Never finish the skill without presenting the three drafting modes via AskUserQuestion. The plan is useless until the user picks how to execute it — the choice drives which execution skill runs next.

## Remember

- Exact file paths always (`.writing/manuscript/02_methods.md`, not "the methods file").
- Every task includes its git commit command with `-c user.email=sipeng@local -c user.name=sipeng` — matches the plugin's committed-by convention.
- Bare skill names for upstream (`scientific-writing`, `scientific-schematics`, `peer-review`, `pyzotero`, `citation-management`, `research-lookup`) — never `plugin:` prefixed.
- Plan size budget: one file, one pass. If the plan exceeds ~800 lines, split into sub-plans by IMRAD phase (e.g., `plan-part-methods.md`, `plan-part-results.md`) and reference from a top-level index.
- `.writing/plan.md` is source of truth for drafting; status tracking lives in `.writing/progress.md`.
