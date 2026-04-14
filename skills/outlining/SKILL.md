---
name: outlining
description: Converts a research idea into a complete IMRAD outline plus per-section claim list. Combines design-exploration and spec-writing into one chain. Output is .writing/outline.md (structure + key claims), populated claims/section_*.md files, and .writing/metadata.yaml filled. Use when starting a new paper or when outline is missing.
---

# Outlining — IMRAD Structure and Claim Stubs

This is the **spec phase** for a research paper. Output of outlining is the input to writing-plans and drafting. Nothing gets written as manuscript prose here. The deliverables are three files:

1. `.writing/outline.md` — IMRAD structure with 3-7 key claims per section.
2. `.writing/claims/section_<NN>_<slug>.md` — one file per manuscript section, each containing a YAML list of claim stubs that prose will later bind to.
3. `.writing/metadata.yaml` — author, preregistration, data/code availability, reporting-guideline fields filled out.

All three must be complete before handing off to `superpower-writing:writing-plans`. Incomplete metadata blocks the submission gate later — fix it now while context is fresh.

## When to Use

Trigger this skill when:

- User starts a new paper and `.writing/outline.md` is empty (or missing).
- User has a research idea but no IMRAD structure yet.
- Existing outline needs significant restructuring (major scope shift, co-author request to pivot framing).
- Any claim file under `.writing/claims/` is missing for a planned section.

Do NOT use this skill for:

- Copy-editing existing prose (use `revision`).
- Post-review restructuring after journal feedback (use `revision`).
- Filling in numeric details in an already-outlined paper (belongs to `drafting` with claim-first protocol).

## Checklist (each must pass before handoff)

- [ ] `.writing/` exists; if not, `main` skill must initialize it first.
- [ ] `.writing/metadata.yaml` has no top-level key still set to `TODO` (authors, preregistration, data_availability, code_availability, reporting_guideline).
- [ ] `.writing/outline.md` has IMRAD sections: Abstract, Introduction, Methods, Results, Discussion, Conclusion, with 3-7 bullets each.
- [ ] Every bullet has a matching claim stub in the right `claims/section_<NN>_<slug>.md` file, `STATUS: stub`, `EVIDENCE` populated with type/ref placeholders.
- [ ] Intro and Discussion are narrative-consistent: every Introduction gap/question has a Discussion bullet addressing it, and vice versa.
- [ ] Upstream `literature-review` has been invoked at least once; key references are recorded in `.writing/findings.md` under Research Findings.
- [ ] Scope check done: no bullet falls outside the paper's stated contribution.
- [ ] If `metadata.yaml` has `zotero.enabled: true` and a `collection_key` is set, EVIDENCE entries have been optionally seeded from that Zotero collection.

# Process

## Step 1: Capture the research idea

Before any IMRAD structure, lock down:

- The **core contribution** in one sentence. If the user can't state it, spend time here — everything downstream anchors to this.
- The **target venue or venue class** (e.g., clinical journal, systems conference, ML workshop). This picks the reporting guideline (CONSORT / STROBE / PRISMA / none) which goes into `metadata.yaml`.
- The **unit of evidence**: dataset, cohort, simulation, benchmark, proof — whichever is the study's primary thing. This determines what counts as EVIDENCE later.

Write these three into `.writing/findings.md` under the Requirements section.

If the idea is still exploratory, stop and route to `superpower-planning:brainstorming` first. Outlining assumes the contribution is already decided; brainstorming is where it gets decided. Don't force a half-formed idea through IMRAD — it produces a fake outline that masks missing thinking.

## Step 2: Iterative literature retrieval

Before proposing section-level claims, ground the paper in prior work. This is the only phase in the pipeline where broad literature reading happens; later phases only resolve specific cited items.

```
Skill(skill="literature-review")
```

Use it to synthesize the landscape around the core contribution: what is known, what is contested, what is missing. Follow up with targeted lookups:

```
Skill(skill="research-lookup")
```

For specific papers you or the user mention, for canonical datasets, or for recent preprints.

Record findings in `.writing/findings.md` under Research Findings. Each finding entry should include: citation (with DOI where possible), one-sentence takeaway, and which IMRAD section it will inform (Intro / Methods / Results / Discussion).

**Iterate:** after the first sweep, reflect on what gaps remain. Typical gaps:

- No methodological precedent for a key choice → look up the method's canonical source.
- Competing prior results → look up both and note the contested framing for Discussion.
- Missing baseline → look up standard benchmarks in the subfield.

Two or three retrieval passes is normal. A single sweep usually misses something.

## Step 3: Draft the IMRAD outline

Open `.writing/outline.md` (created by `init-writing-dir.sh`; initially empty). Write the IMRAD skeleton with 3-7 bullets per section. Each bullet is a **claim** — an assertion the paper will make, not a topic heading. "We show X" is a claim; "Overview of methods" is not.

Recommended bullet counts:

| Section | Bullets | Purpose |
|---------|---------|---------|
| Abstract | 3-5 | Background / question / method / result / implication — one sentence each. |
| Introduction | 4-7 | Gap, why it matters, prior work, remaining question, this paper's contribution, approach preview. |
| Methods | 3-6 | Population/dataset, intervention/procedure, measurement, analysis, ethics/preregistration. |
| Results | 3-7 | One bullet per headline finding. No interpretation. |
| Discussion | 4-6 | Interpretation, comparison to prior work, limitations, mechanism, implications. |
| Conclusion | 2-3 | One-sentence recap, one-sentence implication, one-sentence forward-look. |

Use short imperative claims. Numeric values that belong in prose (e.g., sample size) can be placeholders (`N=[TODO]`) at this stage — they become EVIDENCE entries once resolved.

## Step 4: Materialize claim stubs

For every bullet in the outline, create a YAML entry in the matching `.writing/claims/section_<NN>_<slug>.md` file. The filename stem must match the manuscript filename that will pair with it:

```
.writing/manuscript/02_methods.md
.writing/claims/section_02_methods.md
```

Claim YAML format (per design.md §6.1):

```yaml
- id: meth-c1
  CLAIM: Cohort of 1,247 T2D patients from NHANES 2018-2023
  EVIDENCE:
    - type: dataset
      ref: NHANES-2018-2023
    - type: citation
      doi: 10.xxxx/...
  STATUS: stub
```

Rules:

- **id** is short, section-prefixed, and unique within the paper (`meth-c1`, `intro-c3`, `res-c2`, `disc-c4`). Prose binding uses these ids via `<!-- claim: meth-c1 -->`.
- **CLAIM** is a single sentence restating the bullet from the outline — no hedging, no citations in this line.
- **EVIDENCE** lists what would have to be true for the claim to survive verification. Valid `type` values:
  - `citation` — a paper or preprint; must have a `doi` (or `arxiv`, `ref`) field.
  - `dataset` — a named dataset; `ref` required.
  - `figure` — a figure in this paper; `id` field pointing to its planned figure id.
  - `table` — a table in this paper; `id` field.
  - `analysis` — a computed statistic to be produced during drafting; `description` field.
- **STATUS** is always `stub` at outlining time. It advances to `evidence_ready` only after the drafting subagent resolves each EVIDENCE item (DOI resolves, dataset is accessible, figure is drawn), and to `verified` only after `claim-verification` passes.
- Leave placeholders like `doi: 10.xxxx/...` when the exact source is not yet known — drafting will resolve them. But don't invent DOIs.

> Claim-first protocol: see `superpower-writing:main` §Claim-First Protocol.

Outlining produces stubs on purpose: the hook blocks prose against stubs so claim files must mature before prose can reference them.

## Step 5: Optional Zotero seeding

Applicable only when `.writing/metadata.yaml` contains:

```yaml
zotero:
  enabled: true
  collection_key: "ABCD1234"
```

If both conditions hold, seed `EVIDENCE` `citation` entries from the pre-curated collection. The user has already vetted these references, so they are safe starting points.

```
Skill(skill="pyzotero")
```

Use it to list items in `collection_key`. For each item with a DOI and an abstract that plausibly supports a claim, add a pre-filled EVIDENCE entry with `source: zotero` and `zotero_item_key: <key>`:

```yaml
- id: intro-c2
  CLAIM: Prior work found effect X in population Y
  EVIDENCE:
    - type: citation
      doi: 10.1038/...
      source: zotero
      zotero_item_key: ABCD1234
  STATUS: stub
```

Skip this step silently when `zotero.enabled` is unset or false, or when `collection_key` is empty. Drafting will still query Zotero per-claim; outlining only seeds obvious matches to save work later.

Never push new items to Zotero during outlining — that's a drafting concern (see `drafting` SKILL.md).

## Step 6: Fill `metadata.yaml`

Open `.writing/metadata.yaml`. The template has every top-level key set to `TODO` or empty. Replace each with a real value:

```yaml
authors:
  - name: <user-provided>
    affil: <user-provided>
    orcid: <user-provided or null>
    coi: <declare: none | grant:... | equity:... | employment:...>
preregistration:
  registry: <OSF | ClinicalTrials.gov | null | ...>
  url: <url or null>
  deviations: []   # keep empty list; populated later if protocol deviates
data_availability:
  statement: <one-sentence statement>
  access: <open | restricted | on-request | none>
code_availability:
  url: <repo url or null>
  license: <SPDX id or null>
reporting_guideline: <CONSORT | STROBE | PRISMA | none>
```

**Presence check, not correctness check:** the submission gate only verifies these fields are set. The user owns truthfulness. If a field truly does not apply (e.g., no preregistration for a computational paper), use `null` — not `TODO`.

Ask the user for any field you cannot infer. Do not fabricate author names, ORCIDs, affiliations, grant numbers, or preregistration URLs. Use `AskUserQuestion` when information is missing.

`reporting_guideline` is load-bearing: it drives the upstream `peer-review` checklist at claim-verification time. Pick the right one now:

- Randomized trial → `CONSORT`
- Observational study → `STROBE`
- Systematic review / meta-analysis → `PRISMA`
- Computational / systems / ML method paper → `none` (or a venue-specific checklist if the user names one)

## Step 7: Self-review

Before handing off, spec-review the outline against three checks (mirrors `superpower-planning:writing-plans` self-review pattern):

1. **Placeholder scan** — grep outline.md and claims/*.md for `TODO`, `xxxx`, `[NEEDS-EVIDENCE]`. Any hit that is not an intentional evidence placeholder (e.g., `doi: 10.xxxx/...`) must be resolved or explicitly annotated with `[NEEDS-EVIDENCE]` plus rationale.

2. **I↔D narrative consistency** — every question/gap raised in Introduction has a matching answer/limitation/implication in Discussion. Every Discussion interpretation points back to a Results bullet that produced the finding being interpreted. Gaps here produce papers that feel hollow.

3. **Scope check** — each claim bullet is directly in service of the one-sentence core contribution from Step 1. Tangential bullets must be moved to future-work notes or removed. Scope creep at outlining time compounds into wasted drafting effort.

If any check fails, fix and re-run. Record any unresolvable items as `[NEEDS-EVIDENCE]` in `.writing/findings.md` under Decisions — they must be resolved before submission but are not a blocker for advancing to writing-plans.

## Step 8: Handoff

Update `.writing/progress.md` — mark the outlining row complete with a one-line summary of sections and claim counts (e.g., "6 sections / 27 claims; zotero-seeded 8").

Hand off:

```
Skill(skill="superpower-writing:writing-plans")
```

That skill decomposes the outline into executable per-section / per-figure / per-table tasks with a dependency graph, producing `.writing/plan.md`. Drafting comes after.

# Key Principles

**Claims, not topics.** An outline bullet must state an assertion. "Methods overview" is a heading, not a claim. "We enrolled 1,247 T2D patients from NHANES 2018-2023" is a claim — it has a truth value and binds to evidence. The claim-first protocol only works if outlining produces real claims.

**Stubs are intentional.** Every claim starts `STATUS: stub`. The PreToolUse hook blocks prose writes against stubs on purpose. That block is the feature, not a bug to work around. Drafting advances stubs to `evidence_ready` after resolving EVIDENCE — that is how the paper earns its prose.

**Metadata gate now, not later.** Filling `metadata.yaml` at outlining feels bureaucratic; skipping it feels fast. But unresolved `TODO`s compound: authors keep changing, reporting-guideline choices shape verification, data-availability statements affect what can be published. Resolving this while the paper's shape is still malleable is cheap; resolving it at submission gate under deadline pressure is expensive.

**Literature-review first, lookup-second.** `literature-review` synthesizes; `research-lookup` retrieves. Use synthesis to form the outline's narrative arc, then retrieval to ground individual claims. Reversing the order produces paper-shaped bibliographies instead of arguments.

**Zotero is opt-in and non-blocking.** Zotero seeding saves work when the user has a curated collection. It never gates outlining. When disabled or unavailable, outlining proceeds network-only; drafting can still push newly discovered citations later (if `auto_push_new_citations: true`).

**Don't fabricate.** No invented DOIs, fake ORCIDs, or guessed grant numbers. When information is missing, ask the user via `AskUserQuestion` or mark the item `[NEEDS-EVIDENCE]` with a one-line rationale. Fabrication in outlining contaminates every downstream stage.

**One-session scope.** Outlining is usually one session. If it stretches across sessions, the paper's scope is probably still unclear — loop back to brainstorming rather than forcing more outline passes.
