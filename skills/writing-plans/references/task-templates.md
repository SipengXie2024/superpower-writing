# Task Templates

These are the exact per-section / per-figure / per-table task templates that `writing-plans/SKILL.md` Steps 5-7 reference. Copy them verbatim into `.writing/plan.md`, substituting the IMRAD section letter and numbering. Every draft task is a three-step triplet: draft, verify-claims, internal-review. Numbering scheme: `<letter>.1` draft, `<letter>.2` verify, `<letter>.3` review — letters are I (Introduction), M (Methods), R (Results), D (Discussion), C (Conclusion), A (Abstract).

Do NOT write prose in the plan itself — the plan enumerates tasks; drafting writes prose.

## Per-section template (repeat for each IMRAD section)

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
  git add .writing/manuscript/02_methods.md .writing/claims/section_02_methods.md
  git commit -m "draft: methods section"
  ```

### Task M.2: Verify Methods claims

**Files:**
- Read: `.writing/manuscript/02_methods.md`, `.writing/claims/section_02_methods.md`
- Write: `.writing/verify-report.md` (append section), update `STATUS` in claims file.

- [ ] **Step 1: Invoke `Skill(skill="claim-verification")` scoped to Methods**

  Run the four-pass verifier on Methods only (completeness, citation resolution dual source, numeric/table consistency, reporting-guideline subset). On all-pass, flip eligible claims `evidence_ready` → `verified`.

- [ ] **Step 2: Commit**

  ```bash
  git add .writing/claims/section_02_methods.md .writing/verify-report.md
  git commit -m "verify: methods claims"
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
  git add .writing/reviews/
  git commit -m "review: internal review of methods"
  ```

> **Note:** Log unexpected discoveries, technical decisions, and drafting insights to `.writing/findings.md` after each task.
````

## Per-figure template

For each figure listed in outline.md (plus the mandatory graphical abstract F0):

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
  git add .writing/figures/
  git commit -m "figure: fig<n> <slug>"
  ```
````

The graphical abstract is mandatory — always emit a Task F0 for it regardless of outline.

## Per-table template

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
  git add .writing/manuscript/ .writing/tables/ .writing/claims/
  git commit -m "table: tab<n> <slug>"
  ```
````
