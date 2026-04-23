---
name: outlining
description: Converts a research idea into a complete IMRAD outline plus per-section claim list. Combines design-exploration and spec-writing into one chain. Output is .writing/outline.md (structure + key claims), populated claims/section_*.md files, and .writing/metadata.yaml filled. Use when starting a new paper or when outline is missing.
---

# Outlining — IMRAD Structure and Claim Stubs

This is the **spec phase** for a research paper. Output of outlining is the input to writing-plans and drafting. Nothing gets written as manuscript prose here. The deliverables are three files:

1. `.writing/outline.md` — IMRAD structure with 3-7 key claims per section.
2. `.writing/claims/section_<NN>_<slug>.md` — one file per manuscript section, each containing a YAML list of claim stubs that prose will later bind to.
3. `.writing/metadata.yaml` — author, preregistration, data/code availability, reporting-guideline fields filled out.

**Filename-stem contract (load-bearing).** The PreToolUse claim-first hook at `hooks/enforce-claims.py` matches slug-ending: any manuscript file whose stem ends in `_<slug>` for slug ∈ `UNPROTECTED_SLUGS` (`abstract`, `references`, `acknowledgments`) is exempt from claim-tag enforcement. Concretely `00_abstract.tex`, `09_references.tex`, and `10_acknowledgments.tex` all pass through without paragraph tags. Every other section filename MUST contain real prose tagged with `% claim: id` or the write is blocked. If you introduce a new unnumbered section (e.g. a data-availability block) whose content should be exempt, add its slug to `UNPROTECTED_SLUGS` in `hooks/enforce-claims.py`. The hook only intercepts `.tex` files; `.md` files under `manuscript/` pass through unenforced.

**Abstract is citation-free (load-bearing).** Any stem ending in `_abstract` additionally belongs to `CITATION_FREE_SLUGS` in the hook. Writes to such files that contain any LaTeX citation command (`\cite{}`, `\citep{}`, `\citet{}`, `\nocite{}`, `\parencite{}`, or any `\*cite*` variant) or a `% claim: id` tag are blocked. The abstract summarizes the paper's own claims in prose; it cites nothing. BPMRC structural tags (`% bpmrc: B`, `% bpmrc: P`, etc.) are still required — they are not citations. Do NOT create a `claims/section_00_abstract.md` file; drafting would try to bind abstract paragraphs to it and the hook would reject those writes.

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

If the idea is still exploratory, stop and route to `superpower-writing:brainstorming` first. Outlining assumes the contribution is already decided; brainstorming is where it gets decided. Don't force a half-formed idea through IMRAD — it produces a fake outline that masks missing thinking.

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

| Section | Bullets | Included by default? | Purpose |
|---------|---------|----------------------|---------|
| Abstract | **5 (BPMRC, fixed)** | Always | Background / Problem / Method / Result / Conclusion — one bullet each, labeled `[B] [P] [M] [R] [C]`. See section-standard below. |
| Introduction | **4–7 (CARS)** | Always | Territory / Niche / Occupy — at least one bullet per Move, labeled `[T] [N] [O]` in that strict order. |
| Background / Preliminaries | **4–6 (DNPL)** | CS / ML / systems / DB / graphics / theoretical-CS papers; omit for IMRAD-strict medical / biology papers | Domain / Notation / Prior / Limitation — at least one bullet per element, labeled `[D] [N] [P] [L]` in order. |
| Motivation | **3–6 (SFR)** | **OPT-IN** — only systems / architecture / hardware / some security venues that require a dedicated motivating example | Scenario / Failure / Requirements — labeled `[S] [F] [R]`. When included, compress Introduction's `[N]` to a single high-level gap bullet to avoid duplication. |
| Related Work | **2–4 (ThematicGroup)** | CS / ML / systems / engineering papers; optional for strict IMRAD. May sit at §2 (systems/security convention) or near the end before §Conclusion (ML convention) | One thematic group per bullet, labeled `[G]`. Each bullet MUST state both the theme and how this paper differs. |
| Methods (CS) | **4–10 (OFCA)** | CS / ML / systems / DB / graphics / theory papers | Overview / Formalization / Core / Analysis, optional Implementation — labeled `[O] [F] [C] [A] [I]`, strict O→F→C→A→I order. `[O]` and `[C]` required; `[F]` and `[A]` strongly recommended; `[I]` optional for systems/applied. |
| Methods (medical / biology) | 3–6 | IMRAD-strict clinical / biology papers | Population/dataset, intervention/procedure, measurement, analysis, ethics/preregistration. Follows CONSORT / STROBE / PRISMA when applicable. No section standard file yet. |
| Results (CS) | **7–15 (RSRT)** | CS / ML / systems / DB / graphics papers | Research Questions / Setup / Per-RQ Results / Takeaways — labeled `[RQ] [S] [R] [T]`, strict RQ→S→R→T order. `[RQ]` count MUST equal `[R]` count (1-to-1 correspondence). |
| Results (medical / biology) | 3–7 | IMRAD-strict clinical / biology papers | One bullet per headline finding. No interpretation. Follows CONSORT / STROBE / PRISMA when applicable. No section standard file yet. |
| Discussion (CS) | **4–8 (ILFS)** | CS / ML / systems / DB / graphics papers | Interpretation / Limitations / Future work / Significance — labeled `[I] [L] [F] [S]`, strict I→L→F→S order, each element at least 1 bullet. May merge with §Conclusion. |
| Discussion (medical / biology) | 4–6 | IMRAD-strict clinical / biology papers | Interpretation, comparison to prior work, limitations, mechanism, implications. No section standard file yet. |
| Conclusion (CS) | **3 exact (RSF)** | CS / ML / systems papers | Restate / Summary / Forward-look — labeled `[R] [S] [F]`, strict R→S→F. Exactly 3 bullets (2 when merged with §Discussion: RS only). Total ≤ 250 words. Optional section for short papers. |
| Conclusion (medical / biology) | 2–3 | IMRAD-strict clinical / biology papers | One-sentence recap, one-sentence implication, one-sentence forward-look. No section standard file yet. |

Use short imperative claims. Numeric values that belong in prose (e.g., sample size) can be placeholders (`N=[TODO]`) at this stage — they become EVIDENCE entries once resolved.

**Section inclusion guidance:**

- **IMRAD-strict venues** (NEJM / Lancet / JAMA / most biology): include only Abstract, Introduction, Methods, Results, Discussion, Conclusion. Skip Background, Motivation, Related Work — their content folds into Introduction and Discussion.
- **Default CS / ML / systems**: add Background and Related Work. Motivation remains opt-in — only include it if the paper genuinely needs a dedicated motivating-example section (see `08_motivation.md` for the trigger conditions).
- **Related Work placement:** decide §2 (early) vs. near-end based on the target venue's norm. The standards file applies identically regardless of position; only the manuscript stem number changes.

**Section-specific standards.** For every section listed above, check whether a matching file exists under `skills/drafting/references/section-standards/`. Resolution is by **two-level match (slug-ending)**: first try `<NN>_<slug>.md` for exact stem; if miss, scan `section-standards/` for any file ending in `_<slug>.md` and use the single match. Canonical filenames today: `00_abstract.md`, `01_introduction.md`, `02_background.md`, `03_methods.md`, `04_results.md`, `05_discussion.md`, `06_conclusion.md`, `07_related_work.md`, `08_motivation.md`. If one is found, it is binding — read it now and shape the bullets to satisfy its outline requirements before moving to Step 4. The standards files codify conventions drafting will also enforce, so an outline that disagrees with its standard guarantees rework at drafting time.

- `00_abstract.md` (canonical slot — §0/§1 fixed): requires the **5-bullet BPMRC structure** above. Prefix each Abstract bullet with `[B]`, `[P]`, `[M]`, `[R]`, or `[C]` in that order:

  ```
  ## Abstract

  - [B] <one-sentence background>
  - [P] <one-sentence problem / gap>
  - [M] <one-sentence method>
  - [R] <one-sentence headline result>
  - [C] <one-sentence conclusion / implication>
  ```

- `01_introduction.md` (canonical slot — §0/§1 fixed): requires the **CARS (Create A Research Space) 3-Move structure**. Write 4–7 bullets total, with at least one per Move, in the strict order M1 → M2 → M3. Prefix each Introduction bullet with `[T]` (Territory / M1), `[N]` (Niche / M2), or `[O]` (Occupy / M3):

  ```
  ## Introduction

  - [T] <centrality: why this topic matters>
  - [T] <prior work: state of the field>
  - [N] <gap / contradiction / open question>
  - [O] <this paper's purpose + approach>
  - [O] <principal contributions / key findings>
  ```

  All `[T]` bullets come before any `[N]`; all `[N]` come before any `[O]`. Typical distribution is 2–3 `[T]` + 1–2 `[N]` + 1–2 `[O]`. The CS/engineering contributions-list variant is a drafting-time choice (see `01_introduction.md` §Draft requirement) — at outline time, still write a single `[O]` bullet per principal contribution. **If the paper also includes §Motivation**, compress the `[N]` bullets to exactly 1 (a single high-level gap sentence).

- `02_background.md` (governs any `NN_background.tex` manuscript stem): requires the **DNPL 4-part structure**. Write 4–6 bullets total, with at least one per element, in the strict order Domain → Notation → Prior → Limitation. Labels: `[D] [N] [P] [L]`. Manuscript stem is typically `02_background` (no Motivation) or `03_background` (with Motivation).

  ```
  ## Background

  - [D] <domain recap: the problem space>
  - [N] <formal notation and definitions the rest of the paper will reuse>
  - [P] <dominant prior approach described in that notation>
  - [L] <concrete limitation of the prior approach>
  ```

- `08_motivation.md` (slug-only, **OPT-IN**; governs any `NN_motivation.tex` manuscript stem): requires the **SFR 3-part structure**. Write 3–6 bullets total: exactly 1 `[S]` Scenario bullet, 1–2 `[F]` Failure bullets (quantitative), and 2–5 `[R]` Requirement bullets (one per requirement). Only include §Motivation when the paper targets a venue that expects one (systems / architecture / hardware / some security); otherwise skip the section entirely. Manuscript stem is typically `02_motivation` when opted in.

  ```
  ## Motivation

  - [S] <one-sentence description of the concrete use case>
  - [F] <one-sentence summary of how baseline fails, with a headline number>
  - [R] <requirement 1: one-sentence actionable property>
  - [R] <requirement 2: ...>
  ```

- `07_related_work.md` (governs any `NN_related_work.tex` manuscript stem, whether §2 early-placement or near-end late-placement): requires the **Thematic-Group structure**. Write 2–4 bullets total, one per thematic group, labeled `[G]`. Each bullet MUST state both the theme's shared approach and how this paper differs (differentiator in the bullet text, not deferred to drafting).

  ```
  ## Related Work

  - [G] <theme 1: shared approach + how we differ>
  - [G] <theme 2: shared approach + how we differ>
  - [G] <theme 3: shared approach + how we differ>
  ```

- `03_methods.md` (governs any `NN_methods.tex` manuscript stem for CS / ML / systems / DB / graphics / theory papers): requires the **OFCA (+I) structure**. Write 4–10 bullets total: at least 1 `[O]` Overview and 2 `[C]` Core, with `[F]` Formalization and `[A]` Analysis strongly recommended; `[I]` Implementation is optional (0–2). Strict order O → F → C → A → I. Keep the manuscript filename as `<NN>_methods.tex` even if the paper renders the section as "§3 Design" / "§3 Approach" / "§3 Algorithm" — the slug is a plugin-internal convention, not a rendered heading.

  ```
  ## Methods

  - [O] <one-sentence overview of the approach>
  - [F] <formal problem statement>
  - [C] <core component 1: name + one-line description>
  - [C] <core component 2>
  - [C] <core component 3>
  - [A] <one-sentence correctness or complexity claim>
  - [I] <implementation highlight: framework / hyperparameters / hardware>
  ```

- `04_results.md` (governs any `NN_results.tex` manuscript stem for CS / ML / systems / DB / graphics papers): requires the **RSRT four-part structure**. Write 7–15 bullets total: 3–5 `[RQ]` Research Questions, 1–3 `[S]` Setup, exactly as many `[R]` Results as `[RQ]` (1-to-1 in order), 0–2 `[T]` Takeaways. Strict order RQ → S → R → T. Keep filename as `<NN>_results.tex` even when the paper renders as "§5 Evaluation" / "§5 Experiments".

  ```
  ## Results

  - [RQ] RQ1: <question 1>
  - [RQ] RQ2: <question 2>
  - [RQ] RQ3: <question 3>
  - [S] Datasets / baselines / metrics / hardware (1–3 bullets)
  - [R] RQ1 result: <headline number with comparator and uncertainty>
  - [R] RQ2 result: <...>
  - [R] RQ3 result: <...>
  - [T] <one-sentence synthesis across RQs>
  ```

- `05_discussion.md` (governs any `NN_discussion.tex` manuscript stem for CS papers): requires the **ILFS four-part structure**. Write 4–8 bullets total: at least 1 `[I]` Interpretation, 1 `[L]` Limitations, 1 `[F]` Future work, 1 `[S]` Significance. Strict order I → L → F → S. §Discussion and §Conclusion may be merged as "Discussion and Conclusion"; when merged, append the RSF Conclusion template to the end of Discussion and drop RSF `[F]` to avoid duplicating ILFS `[F]`.

  ```
  ## Discussion

  - [I] <why RQ1 result appeared as it did — mechanism or causation>
  - [I] <why RQ2 scaling behavior appeared as it did>
  - [L] <specific threat to validity or scope boundary>
  - [F] <concrete future-work direction>
  - [S] <practical or theoretical implication>
  ```

- `06_conclusion.md` (governs any `NN_conclusion.tex` manuscript stem for CS papers): requires the **RSF three-part structure**. Write **exactly 3 bullets** in the strict order R → S → F. Total section length ≤ 250 words. No new content, no verbatim Abstract copy. When §Conclusion is merged into §Discussion (common in NeurIPS / ICML), omit `[F]` and shrink to 2 bullets (RS only) — the forward-look lives in §Discussion's ILFS `[F]`.

  ```
  ## Conclusion

  - [R] <one-sentence restatement of the contribution>
  - [S] <one-sentence headline result>
  - [F] <one-sentence forward-look>
  ```

- All IMRAD sections now have matching standards files. If the paper introduces a non-IMRAD section (e.g., §Glossary, §Ethics Statement, §Reproducibility Checklist), no standards file applies — generic bullet count from the table above governs, and `{SECTION_STANDARD}` falls through to the "no standard applies" text.

## Step 4: Materialize claim stubs

For every bullet in the outline, create a YAML entry in the matching `.writing/claims/section_<NN>_<slug>.md` file. The filename stem must match the manuscript filename that will pair with it:

```
.writing/manuscript/03_methods.tex
.writing/claims/section_03_methods.md
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

- **id** is short, section-prefixed, and unique within the paper (`meth-c1`, `intro-c3`, `res-c2`, `disc-c4`). Prose binding uses these ids via `% claim: meth-c1` (LaTeX line comment at column 0).
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

Before handing off, spec-review the outline against four checks (mirrors `superpower-writing:writing-plans` self-review pattern):

1. **Placeholder scan** — grep outline.md and claims/*.md for `TODO`, `xxxx`, `[NEEDS-EVIDENCE]`. Any hit that is not an intentional evidence placeholder (e.g., `doi: 10.xxxx/...`) must be resolved or explicitly annotated with `[NEEDS-EVIDENCE]` plus rationale.

2. **I↔D narrative consistency** — every question/gap raised in Introduction has a matching answer/limitation/implication in Discussion. Every Discussion interpretation points back to a Results bullet that produced the finding being interpreted. Gaps here produce papers that feel hollow.

3. **Scope check** — each claim bullet is directly in service of the one-sentence core contribution from Step 1. Tangential bullets must be moved to future-work notes or removed. Scope creep at outlining time compounds into wasted drafting effort.

4. **Section-standard conformance** — for every section that has a matching file under `skills/drafting/references/section-standards/` (resolved via the two-level match rule: exact `<NN>_<slug>.md` first, slug-ending `*_<slug>.md` scan as fallback), verify the outline satisfies the "Outline bullet requirement" part of that standard. Concretely:

   - Abstract (`00_abstract.md`, BPMRC): grep the Abstract block and confirm exactly 5 bullets appear in the order `^- \[B\]`, `^- \[P\]`, `^- \[M\]`, `^- \[R\]`, `^- \[C\]`. Any missing, duplicate, or out-of-order label fails the check.
   - Introduction (`01_introduction.md`, CARS): grep the Introduction block and confirm (a) total bullet count is between 4 and 7 inclusive; (b) at least one `^- \[T\]`, one `^- \[N\]`, and one `^- \[O\]` line exists; (c) every `^- \[T\]` line appears before every `^- \[N\]`, and every `^- \[N\]` before every `^- \[O\]`. Any interleaving (e.g. `[T] ... [N] ... [T] ...`) fails the check. When §Motivation is present in the outline, additionally confirm §Introduction has exactly one `^- \[N\]` bullet (compressed form).
   - Background (`02_background.md`, DNPL): when the outline has a §Background block, grep it and confirm (a) total bullet count is between 4 and 6 inclusive; (b) at least one `^- \[D\]`, one `^- \[N\]`, one `^- \[P\]`, and one `^- \[L\]` line exists; (c) strict D → N → P → L group ordering (all D before any N, all N before any P, all P before any L). Any interleaving fails.
   - Motivation (`08_motivation.md`, SFR, opt-in): when the outline has a §Motivation block, grep it and confirm (a) exactly one `^- \[S\]` bullet; (b) between 1 and 2 `^- \[F\]` bullets; (c) between 2 and 5 `^- \[R\]` bullets; (d) strict S → F → R group ordering. If §Motivation is present, also verify Introduction's `^- \[N\]` count equals 1 (the compression rule above).
   - Related Work (`07_related_work.md`, ThematicGroup): when the outline has a §Related Work block, grep it and confirm (a) total bullet count is between 2 and 4 inclusive; (b) every bullet starts with `^- \[G\]`; (c) every `[G]` bullet text contains a differentiator clause — grep each bullet for `unlike`, `in contrast`, `whereas`, `differs`, or `orthogonal` (case-insensitive). Bullets that only name a theme without stating differentiation fail the check.
   - Methods (`03_methods.md`, OFCA, CS papers only): when the outline has a §Methods block and the paper is CS / ML / systems / theory (not IMRAD-strict medical), grep it and confirm (a) total bullet count is between 4 and 10 inclusive; (b) at least 1 `^- \[O\]` bullet and at least 2 `^- \[C\]` bullets exist; (c) strict O → F → C → A → I group ordering — all `[O]` before any `[F]`, all `[F]` before any `[C]`, all `[C]` before any `[A]`, all `[A]` before any `[I]`. Warn (do not fail) when `[F]` or `[A]` are missing: they are strongly recommended but skippable with deliberate justification; fail only when `[O]` or `[C]` is missing.
   - Results (`04_results.md`, RSRT, CS papers only): when the outline has a §Results block and the paper is CS / ML / systems (not IMRAD-strict medical), grep it and confirm (a) total bullet count is between 7 and 15 inclusive; (b) between 3 and 5 `^- \[RQ\]` bullets; (c) between 1 and 3 `^- \[S\]` bullets; (d) `^- \[R\]` bullet count EXACTLY equals `^- \[RQ\]` bullet count (1-to-1 correspondence); (e) strict RQ → S → R → T group ordering. `[T]` is optional (0–2). Additionally, warn if any `^- \[R\]` bullet text does not contain at least one digit — every `[R]` result SHOULD carry a headline number at outline time (placeholders like `N=[TODO]` count as a digit for this check).
   - Discussion (`05_discussion.md`, ILFS, CS papers only): when the outline has a §Discussion block and the paper is CS / ML / systems (not IMRAD-strict medical), grep it and confirm (a) total bullet count is between 4 and 8 inclusive; (b) at least one `^- \[I\]`, one `^- \[L\]`, one `^- \[F\]`, and one `^- \[S\]` line exists; (c) strict I → L → F → S group ordering — all `[I]` before any `[L]`, all `[L]` before any `[F]`, all `[F]` before any `[S]`. When §Conclusion is absent or merged into §Discussion, this rule still applies to the Discussion portion.
   - Conclusion (`06_conclusion.md`, RSF, CS papers only): when the outline has a §Conclusion block and the paper is CS / ML / systems, grep it and confirm (a) standalone form: exactly 3 bullets in the strict order `^- \[R\]`, `^- \[S\]`, `^- \[F\]` — no more, no fewer; OR (b) merged form (when §Discussion's label mentions "Discussion and Conclusion" or the outline heading is "## Discussion and Conclusion"): exactly 2 bullets in the order `^- \[R\]`, `^- \[S\]`, with `[F]` omitted because §Discussion's `[F]` carries the forward-look. Any other bullet count or ordering fails the check.
   - Additional sections: apply the same pattern — read the standards file's "Outline bullet requirement" section and verify its specific rule.

   If a check fails, fix the outline and re-run; do not advance to writing-plans with a structural mismatch. Sections without a matching standards file are exempt.

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
