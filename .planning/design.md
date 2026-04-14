# superpower-writing Design

**Status:** Draft v2 (post spec-interview, ready for writing-plans)
**Date:** 2026-04-14
**Author:** @SipengXie2024 (brainstormed with Claude)

## 1. Problem & Scope

Academic paper writing (IMRAD research articles) is a long-horizon, multi-phase task
with the same structural needs as a medium-sized software project: persistent state
across sessions, stage gates, claim/evidence traceability, review loops, and parallel
decomposition. `superpower-planning` already encodes this skeleton for code work.
`scientific-agent-skills` (k-dense-ai) provides rich **content** skills for the
academic domain — `scientific-writing`, `literature-review`, `peer-review`,
`citation-management`, `research-lookup`, `scientific-schematics`, etc. — but lacks
the process glue. **superpower-writing** fills the gap: it is an orchestration-only
plugin that mirrors the superpower-planning lifecycle, adapted to manuscripts.

**In scope (v1):** IMRAD research manuscripts.
**Out of scope:** reviews, grants, theses, venue-specific templating, figure
rendering, citation formatting — all delegated to scientific-agent-skills.

## 2. Dependency Model

superpower-writing depends on the **scientific-agent-skills** collection (K-Dense-AI).
Key correction from brainstorming: this is **not a Claude Code plugin** — it is an
[Agent Skills standard](https://agentskills.io/) distribution. Installed via
`npx skills add K-Dense-AI/scientific-agent-skills`, skills land as top-level
entries (e.g. `scientific-writing`, `literature-review`) with no plugin prefix. The
Skill tool invokes them directly by bare name.

**Hard-fail policy:** when required skills are missing, refuse to run and surface
the install command. No degraded mode — silent fallback risks producing
unverified manuscripts.

### Required upstream skills

`scientific-writing`, `literature-review`, `peer-review`, `citation-management`,
`research-lookup`, `scientific-schematics` (mandatory per scientific-writing SKILL.md
for graphical abstracts). Optional: `scientific-critical-thinking`,
`scientific-brainstorming`.

### Dual-layer dependency check

- **SessionStart hook** (`hooks/check-deps.sh`): probes Agent Skills install
  locations (`~/.claude/skills/<name>/SKILL.md` and platform-standard paths) for
  the required set. On miss, injects a system-reminder containing:
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  and (if missing) the `uv` installer snippet from upstream README.
- **main skill check**: the same script re-runs when a user invokes any writing
  skill directly, covering disabled-hook cases.
- On success, `.writing/findings.md` records `deps_verified_at: <ts>` to short-
  circuit re-checks inside the same session.

## 3. Directory Layout

```
superpower-writing/
  plugin.json
  hooks/
    check-deps.sh            # SessionStart
  scripts/
    init-writing-dir.sh      # bootstraps .writing/
    check-deps.sh            # same logic, invokable from main
  commands/
    outline.md               # /writing:outline
    draft.md                 # /writing:draft
    revise.md                # /writing:revise
    submit.md                # /writing:submit
    stash.md, archive.md
  skills/
    main/                    # router + dep check + stage routing
    outlining/               # brainstorm + outline(=spec) in one chain
    writing-plans/           # decompose sections/figures/tables into tasks
    drafting/                # serial (subagent + 2-stage review) OR parallel (team)
    claim-verification/      # claim-first drafting protocol + pre-submit verify
    revision/                # internal + journal review loops unified
    submission/              # freeze gate + archive
```

Seven skills total. Utility skills from superpower-planning (stashing,
git-worktrees, parallel-agents) collapse into main/drafting since they are lighter
lifts here.

## 4. `.writing/` Persistent State (disk RAM)

```
.writing/
  outline.md                 # IMRAD outline + per-section claim list; spec equivalent
  findings.md                # lit synthesis, user decisions, reviewer context, deps status
  progress.md                # Section/Figure status dashboard
  manuscript/
    00_abstract.md
    01_introduction.md
    02_methods.md
    03_results.md
    04_discussion.md
    05_conclusion.md
    06_references.md
  claims/
    section_<n>_claims.md    # claim -> required evidence -> verification status
  figures/                   # generated via scientific-schematics
  reviews/
    internal_<date>.md
    journal_<round>.md
  archive/                   # post-submission frozen copy
  stash/<paper-name>/        # multi-paper context switch
```

## 5. Skill Mapping (SP → SW)

| superpower-planning            | superpower-writing      | Key adaptation                                                                                          |
|--------------------------------|-------------------------|---------------------------------------------------------------------------------------------------------|
| brainstorming + spec-interview | outlining               | Output = `outline.md` (IMRAD headings + per-section claim list + data gaps)                             |
| writing-plans                  | writing-plans           | Task unit = section/figure/table; annotate dependencies (Methods blocks Results)                        |
| subagent/team/executing-plans  | drafting                | Two internal modes: serial (with 2-stage review) and parallel (per-section team)                        |
| tdd + verification             | claim-verification      | Claim-first stubs before prose; verifier checks citation resolution, number/table consistency, reporting-guideline checklist (CONSORT/STROBE/PRISMA), [NEEDS-EVIDENCE] zeroed |
| requesting/receiving-review + debugging | revision      | Unified collect -> classify (Major/Minor/OutOfScope) -> respond-per-item -> apply-diff; covers internal review and journal revision                                         |
| finishing-branch + archiving + releasing | submission   | Pre-submit freeze gate: all claims verified, references resolvable, graphical abstract present; then archive                                                                |
| stashing                       | (folded into main)      | `.writing/stash/<paper-name>/`                                                                           |
| git-worktrees                  | (folded into main)      | Useful for rebuttals isolated from main manuscript branch                                                |
| parallel-agents                | (folded into drafting)  | Not standalone                                                                                           |

## 6. Claim-First Writing Protocol (TDD analog — core novelty)

### 6.1 Claim file format

Outlining produces `claims/section_<NN>_<slug>.md` paired 1:1 with
`manuscript/<NN>_<slug>.md` (identical stem). Each claim is a YAML block:

```yaml
- id: meth-c1
  CLAIM: Cohort of 1,247 T2D patients from NHANES 2018-2023
  EVIDENCE:
    - type: dataset
      ref: NHANES-2018-2023
    - type: citation
      doi: 10.xxxx/...
  STATUS: stub | evidence_ready | verified
```

### 6.2 Paragraph binding

Each load-bearing paragraph in a manuscript file is prefixed with an HTML comment:

```markdown
<!-- claim: meth-c1 -->
We enrolled 1,247 patients with T2D from NHANES cycles 2018-2023...
```

Exploratory prose uses `<!-- draft-only -->` to opt out of enforcement. Any
`draft-only` marker still present at submission-gate time fails verification.

### 6.3 Hard enforcement via PreToolUse hook

`hooks/enforce-claims.sh` (PreToolUse, matchers: Edit/Write on `**/manuscript/**.md`)
parses the tool call's target file, loads the matching `claims/section_<NN>_*.md`,
and blocks the write if any paragraph in the new content references a claim whose
STATUS is not `evidence_ready` (or higher). Draft-only paragraphs are allowed
through. The hook rejects writes with an actionable message pointing to the
offending claim id.

### 6.4 Verification depth (submission gate)

claim-verification runs three checks:

1. **Claim completeness** — every `<!-- claim: X -->` has a matching STATUS=verified claim; every paragraph lacking a marker is either in an allow-listed section (e.g., Acknowledgments) or fails.
2. **Citation resolution** — for each `citation` EVIDENCE entry, invoke
   `citation-management` / `research-lookup`: DOI must resolve (HTTP 200 at doi.org), and the retrieved abstract must semantically support the claim (LLM pass). This is expensive; run once per submission round, cache results in `.writing/verify-cache.json`.
3. **Numeric/table consistency** — numbers in prose (`1,247`, `p=0.03`) must appear identically in at least one table or figure caption; checked by simple regex extraction plus manual overrides list for narrative figures.

Reporting-guideline checklist (CONSORT/STROBE/PRISMA, selected in
`metadata.yaml`) is a fourth pass delegated to upstream `peer-review` skill.

## 7. Stage Gates

```
(dep-check) -> outlining -> writing-plans -> drafting -> revision* -> submission
                                     ^                        |
                                     +--- loop on reviews ----+
```

Each gate writes a dashboard row to `.writing/progress.md`. Skipping a gate
requires explicit user override (e.g. `--skip-outline` on a 2-paragraph note).

## 8. Execution Strategies (drafting)

Borrow directly from SP:

- **serial / subagent-driven**: one subagent per section, two-stage review
  (spec-reviewer + quality-reviewer) inline. Best for short papers or when sections
  share heavy context.
- **parallel / team-driven**: Agent Team spawns N section drafters plus a dedicated
  reviewer. Best for long papers where sections are loosely coupled (e.g.
  Introduction and Methods can progress independently once outline is frozen).
- No `executing-plans` equivalent — separate-session execution adds little for prose.

## 9. Review Loop (revision)

Unified model covers both internal (co-author) and external (journal reviewer) input:

1. **Intake:** paste/upload review into `.writing/reviews/<id>.md`.
2. **Classify:** Major / Minor / OutOfScope / Factually-wrong — user confirms.
3. **Respond-per-item:** generate point-by-point response draft referencing
   manuscript line numbers and supporting evidence.
4. **Apply-diff:** revise manuscript files; update `progress.md` and
   `claims/` if claims are added/removed.
5. **Second verification pass** before closing the round.

## 10. Metadata & Scientific-Integrity State

`.writing/metadata.yaml` is the single source of truth for all reporting-
compliance state. Populated during outlining, verified at submission gate.

```yaml
authors:
  - name: Sipeng Xie
    affil: ...
    orcid: 0000-...
    coi: none
preregistration:
  registry: OSF           # or null, ClinicalTrials.gov, etc.
  url: osf.io/xxxxx
  deviations: []          # list of {date, description, rationale}
data_availability:
  statement: "Raw data at Zenodo DOI:..."
  access: open            # open | restricted | on-request | none
code_availability:
  url: github.com/.../analysis
  license: MIT
reporting_guideline: STROBE  # drives checklist choice in claim-verification
```

Submission gate refuses to proceed if any top-level key is missing or flagged
`TODO`. This is a **presence check**, not a correctness check — the user owns the
truthfulness of each field; superpower-writing owns the gate.

## 11. Known `[NEEDS-EVIDENCE]` (remaining)

- Whether the PreToolUse hook reliably intercepts Edit/Write across all Claude Code
  tool variants (Edit, Write, NotebookEdit, MultiEdit) — confirm in prototype.
- Whether claim-first drafting meaningfully slows composition vs quality gain —
  pilot on one short paper.
- Semantic-match strength of `research-lookup` for citation verification (false-
  positive/negative rates on a curated test set).
- Agent Skills install path on macOS vs Linux vs Windows-WSL — hook must probe all.

## 12. Explicitly YAGNI (v1)

- Re-implementing literature search, citation formatting, figure rendering, LaTeX
  compile — all upstream.
- Venue-specific templates — `venue-templates` skill exists upstream.
- Non-IMRAD formats (reviews, grants, theses) — defer to v2+.
- Auto-submission to journal portals — manual hand-off.
- Multi-author collaboration with `.writing/` in git — v1 is single-author.
- Zotero round-trip via `pyzotero` — v1 uses manual `.writing/refs.bib`; v2
  revisits pull vs push vs sync.

## 13. Decisions Log (from spec-interview, 2026-04-14)

| Question | Decision |
|----------|----------|
| Claim enforcement mechanism | Hard: PreToolUse hook blocks manuscript writes without evidence_ready claim |
| Cross-plugin fallback on missing upstream | Hard-fail with install command, no degraded mode |
| Claim↔manuscript mapping | Filename correspondence + `<!-- claim: id -->` tags + `<!-- draft-only -->` escape |
| Multi-author model | Single-author v1 |
| Scientific-integrity state | `.writing/metadata.yaml` (single file) |
| Citation verification depth | Strict: DOI resolve + abstract semantic match via research-lookup |
| Zotero integration | v2 only; v1 manual refs |
| Install command | `npx skills add K-Dense-AI/scientific-agent-skills` (verified in upstream README) |
