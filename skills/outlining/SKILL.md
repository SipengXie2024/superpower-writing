---
name: outlining
description: Use when starting a new paper or when `.writing/outline.md` is missing or needs a major restructure. Converts a research idea into an IMRAD outline plus a per-section claim list, sharpened through an interleaved interview. Produces `.writing/outline.md` (structure + key claims), `.writing/claims/section_*.md` (claim stubs), and a filled `.writing/metadata.yaml`. No manuscript prose is written here, this is the spec phase before drafting.
---

# Outlining : IMRAD structure, claims, and the interview

This is the **spec phase**. Its output is the input to `drafting`. Nothing is written as manuscript prose here. Three deliverables:

1. `.writing/outline.md`, IMRAD structure with 3-7 key claims per section.
2. `.writing/claims/section_<NN>_<slug>.md`, one file per section, a YAML list of claim stubs prose will later bind to.
3. `.writing/metadata.yaml`, authors, availability, `writing_profile`, and reporting fields filled.

The outline is a claim spine, not a table of contents. Every bullet is an **assertion the paper will make** ("We show X"), not a topic ("Overview of methods"). The claim-first discipline only works if outlining produces real claims.

## Two load-bearing contracts

- **Filename stems.** Sections whose stem ends in `_abstract`, `_references`, or `_acknowledgments` are exempt from paragraph claim-tags. Every other section's `.tex` file must carry `% claim: id`-tagged prose. If you add a new exempt section, treat its slug like abstract/references. The contract covers `.tex` files, not `.md`.
- **Abstract is citation-free.** Any `_abstract` stem emits no `\cite`/`\citep`/`\citet`/`\nocite`/any `\*cite*` command and no `% claim:` tag, it summarizes the paper's own claims in prose. It still carries BPMRC structural tags. Do not create `claims/section_00_abstract.md`.

Optional term-definition-before-use: copy `templates/glossary.md` to `.writing/glossary.md` to activate `% define:`/`% use:` ordering checks; add a glossary entry when you add the term's claim stub.

## Process

### Step 1 : Capture the contribution

Lock down three things and write them to `.writing/findings.md`:

- **Core contribution** in one sentence. Everything downstream anchors to this.
- **Target venue or venue class**, which sets the reporting guideline and structural norms.
- **Unit of evidence** (dataset, trace, benchmark, proof), what counts as EVIDENCE later.

If the contribution is not yet decided, do not force a half-formed idea through IMRAD, that produces a fake outline masking missing thinking. Route to `superpower-writing:idea` first (it generates candidate directions, checks novelty against prior work, and evaluates the survivor against a top-venue bar, all advisory). The surviving direction becomes the contribution sentence. When the contribution is already decided (the common case), skip ahead.

### Step 2 : Ground in the literature

Before proposing claims, synthesize the landscape with `superpower-writing:literature`: what is known, contested, missing. Record each finding in `.writing/findings.md` under Research Findings (citation + one-sentence takeaway + which IMRAD section it informs). Two or three passes is normal; a single sweep usually misses a baseline or a competing result.

### Step 3 : Draft a rough IMRAD skeleton

Pick the paper type first: **technique** (new method, the default) or **benchmark/dataset** (the artifact is data + an evaluation protocol). They use different skeletons; do not mix them. Ask via `AskUserQuestion` when unclear.

Write the skeleton into `.writing/outline.md` with 3-7 claim bullets per section, using the section frameworks below as **readable guidance**, they encode real rhetorical structure, not a checklist to satisfy mechanically. For the full template and examples of any framework, read the matching file under `../drafting/references/section-standards/` (resolve by slug: `<NN>_<slug>.md`, else the single `*_<slug>.md`).

| Section | Framework | Bullets | Include by default? |
|---------|-----------|---------|---------------------|
| Abstract | BPMRC (Background/Problem/Method/Result/Conclusion) | 5, labeled `[B][P][M][R][C]` | Always |
| Introduction | CARS (Territory/Niche/Occupy) | 4-7, `[T][N][O]` in order | Always |
| Background | DNPL (Domain/Notation/Prior/Limitation) | 4-6, `[D][N][P][L]` | CS/ML/systems; skip for IMRAD-strict medical |
| Motivation | SFR (Scenario/Failure/Requirements) | 3-6, `[S][F][R]` | Opt-in (systems/architecture/hardware) |
| Related Work | Thematic groups | 2-4, `[G]`, each states theme + how we differ | CS/ML/systems |
| Methods | OFCA (Overview/Formalization/Core/Analysis, +Implementation) | 4-10, `[O][F][C][A][I]` in order | CS/ML/systems/theory |
| Results | RSRT (Research questions/Setup/Results/Takeaways) | 7-15, one `[R]` per `[RQ]` | CS/ML/systems |
| Discussion | ILFS (Interpretation/Limitations/Future/Significance) | 4-8, `[I][L][F][S]` in order | CS/ML/systems |
| Conclusion | RSF (Restate/Summary/Forward) | 3 (2 if merged with Discussion) | CS/ML/systems |

Adapt to venue variations: combined Results and Discussion (interleave `[R]`/`[I]`), conclusion folded into Discussion, ML-conference format (Related Work in appendix). Medical/biology venues use IMRAD-strict (skip Background/Motivation/Related Work; follow CONSORT/STROBE/PRISMA). For a benchmark paper, §Methods and §Results become evaluation-framework / construction / findings sections, read `../drafting/references/section-standards/benchmark_README.md` first.

### Step 4 : Interview to sharpen (interleaved loop)

The skeleton is cheap and reviewable; sharpen it before it fans out into dozens of claim files. Interview the user with `AskUserQuestion`, one or two questions per round, refine the skeleton in place after each answer, and loop until it converges. Probe these dimensions, self-resolve any the draft, findings, or literature already answer; spend questions only on what genuinely needs the user:

- **Contribution boundary.** Is every bullet in service of the one-sentence contribution? What is deliberately out of scope?
- **Claim → evidence.** For each key claim, what evidence backs it, a dataset, a run you have, a proof, a citation? Which claims have no data yet?
- **Venue framing.** What does this venue expect structurally, and how should the contribution be framed for its reviewers?
- **Novelty.** What is new relative to the closest prior work, stated concretely (not "we are the first")?
- **Reviewer attacks.** What are the three most likely reviewer objections, and does the outline pre-empt each?
- **Narrative spine.** Does every Introduction gap have a Discussion bullet answering it, and vice versa?

Record non-obvious answers (rejected framings, known weaknesses, missing data) to `.writing/findings.md`. Only once the skeleton holds up does it earn claim stubs.

### Step 5 : Materialize claim stubs

For every bullet, add a YAML entry to the matching `.writing/claims/section_<NN>_<slug>.md` (stem matches the manuscript file that will pair with it):

```yaml
- id: meth-c1
  CLAIM: 1,247 jobs from the Google cluster trace 2019
  EVIDENCE:
    - type: dataset
      ref: google-trace-2019
    - type: citation
      doi: 10.xxxx/...
  STATUS: stub
```

- **id**: short, section-prefixed, unique (`meth-c1`, `res-c2`). Prose binds via `% claim: meth-c1`.
- **CLAIM**: one sentence restating the bullet, no hedging, no citations in this line.
- **EVIDENCE**: what must be true to survive verification. `type` ∈ `citation` (needs `doi`/`arxiv`/`ref`), `dataset` (`ref`), `figure`/`table` (`id`), `analysis` (`description`; on systems papers use the structured source fields from `systems-evidence-contract.md`), `artifact` (first-party `ref` + `role`).
- **STATUS**: always `stub` here. Drafting advances it to `evidence_ready`; claim-verification to `verified`. Leave placeholders like `doi: 10.xxxx/...` when the source is unknown, but never invent DOIs.

Stubs are intentional: the claim-first discipline forbids prose against stubs, so claim files must mature before prose references them.

### Step 6 : Fill `metadata.yaml`

Replace every `TODO`/empty key with a real value: authors (name/affil/orcid/coi), preregistration, data/code availability, and `reporting_guideline` (CS/ML/systems papers normally `none`). Verification checks presence, not truthfulness, the user owns that; use `null` for fields that truly do not apply. Ask via `AskUserQuestion` for anything you cannot infer; never fabricate names, ORCIDs, grants, or URLs.

**`writing_profile` gate.** Set `writing_profile: systems` or `default`. Fill it from the user's explicit statement or a clear systems venue; when unsure, ask once, do not infer from `reporting_guideline: none` (ML and theory papers use `none` too) and do not scan the body to guess. For an older project missing the field, pause the first relevant flow, ask once, write it, then continue. Structured `analysis` evidence is required on all profiles; `writing_profile` only toggles the systems wording and figure references.

Optional Zotero seeding: when `metadata.yaml` has `zotero.enabled: true` and a `collection_key`, seed `citation` EVIDENCE from that collection via `zotero_get_collection_items` (record `source: zotero` + `zotero_item_key`). Skip silently when disabled. Never push new items during outlining, that is a drafting concern.

### Step 7 : Self-review (readable checklist, not a linter)

Before handing off, read the outline once and confirm:

- **Placeholders.** No stray `TODO`/`xxxx` beyond intentional evidence placeholders; unresolved items marked `[NEEDS-EVIDENCE]` with a one-line rationale in `findings.md`.
- **Scope.** Every claim serves the one-sentence contribution; tangential bullets move to future-work notes.
- **I↔D narrative.** Every Introduction gap has a Discussion answer, and every Discussion interpretation points back to a Results bullet.
- **Framework fit.** Each section roughly matches its framework's shape and order (e.g. Introduction runs Territory → Niche → Occupy; Results has one `[R]` per `[RQ]`). This is a judgment read, not a grep, fix obvious breaks, do not police label counts.
- **Challenge → module → contribution spine.** Each prior-work limitation maps to a challenge, each challenge to one Methods core module, each module to a contribution, each contribution to a section. A spine that does not close end to end reads as incoherent regardless of how strong any single piece is, reconcile before drafting.

### Step 8 : Handoff

Update `.writing/progress.md` (mark outlining complete with section and claim counts). Then hand off to `superpower-writing:drafting`, which resolves each claim's evidence and writes the LaTeX prose section by section.

## Key principles

**Claims, not topics.** A bullet must have a truth value and bind to evidence.

**The interview is the point.** A well-structured outline of the wrong paper is the expensive mistake. The interleaved interview exists to catch a wrong contribution, a missing baseline, or an unanswerable reviewer attack while the outline is still cheap to change.

**Metadata gate now, not later.** Unresolved authorship, availability, and `writing_profile` compound; resolving them while the paper's shape is malleable is cheap, at the submission deadline it is not.

**Don't fabricate.** No invented DOIs, ORCIDs, or grant numbers. When information is missing, ask or mark `[NEEDS-EVIDENCE]`, fabrication in outlining contaminates every downstream stage.
