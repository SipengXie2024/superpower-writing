---
section: construction
stem: benchmark_construction
framework: SSEQ-Split
---

# Construction Pipeline: Benchmark Variant (CS)

The §Construction Pipeline section is the technical core of a benchmark paper, equivalent to §Methods in a technique paper. It describes how the benchmark's data is built so that another team can reproduce it, scale it, and trust its quality. Reviewers scrutinize this section hardest; a vague pipeline is a top rejection reason for benchmark submissions. It MUST document a paradigm choice and every pipeline stage with explicit inputs, operations, outputs, and quality gates.

**Slug convention.** Keep the manuscript filename's slug as `construction` regardless of the rendered title. The paper may render it as "§3 Benchmark Construction", "§3 Data Construction", or "§3 Dataset Pipeline"; still author it as `.writing/manuscript/NN_construction.tex` so the slug-ending match resolves to this file. See `benchmark_README.md` for the full benchmark-variant resolution table.

**Scope.** Benchmark and dataset papers for CS / ML / NLP / CV / systems / databases. This is the heaviest chapter of such a paper. Technique papers use `03_methods.md` (OFCA) instead.

## Framework

**Five stages: Source selection, Seed generation, Enrichment, Quality control, Split.** Plus one upstream decision: the **construction paradigm**. The five stages answer, in order: where does raw material come from, how are initial samples produced, how are they annotated, how is quality enforced, and how is the data partitioned. The paradigm decides how stages 1 and 2 work.

Three proven construction paradigms (pick one or combine):

1. **Reverse Synthesis.** Fix the answer first, then generate a matching question. Define an enumerable answer space, generate matching conditions, wrap in natural language, validate uniqueness. Use when the answer space is enumerable (statistical tests, chart types, code patterns) and you need precise control over difficulty and category balance. Advantage: unambiguous ground truth by construction.
2. **Controlled Injection.** Start from clean seeds, then systematically inject the target phenomenon at calibrated severity levels, then validate naturalness. Use when studying one phenomenon (ambiguity, noise, bias, adversarial perturbation) across intensity gradients. Advantage: isolates the variable of interest and enables severity-stratified analysis.
3. **Adaptive Generation plus Expert Annotation.** Use models to generate candidate data, then apply multi-stage human annotation (screening, fine-grained scoring, cross-validation). Use when the task needs nuanced human judgment that cannot be automated. Advantage: combines model scalability with human-judgment quality.

A pipeline that documents stages without naming its paradigm leaves the reviewer guessing how ground truth was established. A paradigm without staged documentation leaves the data irreproducible.

## Role of each element

| Element | Purpose | Typical content |
|---------|---------|-----------------|
| **Paradigm** | Declare how samples and ground truth are produced. | One of Reverse Synthesis, Controlled Injection, Adaptive Generation; a one-paragraph rationale for the choice. |
| **Source selection** | Specify where raw material comes from and how it is cleaned. | Sources, licensing, filtering, dedup; coverage audit and license check as the quality gate. |
| **Seed generation** | Produce initial samples by the chosen paradigm. | Paradigm-specific method; format validation and uniqueness as the gate. |
| **Enrichment** | Add metadata, labels, taxonomy tags. | Annotation of category, difficulty, phenomenon type; taxonomy-coverage balance as the gate. |
| **Quality control** | Enforce explicit quality gates on every sample. | Inter-annotator agreement (Cohen's or Fleiss' kappa, ICC), expert spot-check, adversarial validation, automated sanity checks; an agreement threshold as the gate. |
| **Split** | Partition into train/dev/test without leakage. | Stratified split; distribution-balance check and contamination check as the gate. |
| **Statistical profile** | Summarize the constructed dataset. | Counts per split, distribution across taxonomy categories, difficulty histogram, scale comparison with prior benchmarks. |

Every benchmark documents all five stages. The statistical profile is non-optional: a benchmark paper without a dataset-statistics table reads as under-characterized.

## Outline bullet requirement

`.writing/outline.md` §Construction MUST contain **5–9 bullets total**, satisfying:

- **Exactly 1 `[PD]` Paradigm bullet** naming the construction paradigm and why it fits.
- **At least 1 bullet per stage**, labeled `[SS]` Source selection, `[SG]` Seed generation, `[EN]` Enrichment, `[QC]` Quality control, `[SP]` Split. Stages may be split across more than one bullet when a stage is complex.
- **1 `[ST]` Statistics bullet** describing the planned dataset-statistics table and figures.

Bullets MUST appear in the strict order PD → SS → SG → EN → QC → SP → ST, each prefixed with its label:

```
## Construction

- [PD] Paradigm: Controlled Injection; clean Text-to-SQL seeds, inject four ambiguity types at five severity levels.
- [SS] Sources: 2k clean (question, SQL) pairs from prior corpora; license-checked, deduped.
- [SG] Seed generation: select unambiguous seeds; one seed per (schema, query-shape) cell.
- [EN] Enrichment: annotate each injected sample with ambiguity type and severity level.
- [QC] Quality control: two annotators per sample; Cohen's kappa >= 0.75 threshold; expert spot-check of 10%.
- [SP] Split: stratified by ambiguity type and severity; time-gated to resist contamination.
- [ST] Statistics: counts per split, per-type and per-severity distribution, scale vs. three prior benchmarks.
```

Rules:

- All `[PD]` before any `[SS]`, then strict stage order, `[ST]` last. No interleaving.
- Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_construction.md` using `con-c1`, `con-c2`, … The `[QC]` and `[ST]` claims typically resolve to `type: analysis` (a computed statistic in this paper) or `type: table`; source bullets may carry `type: citation` for borrowed corpora and `type: dataset` for the constructed artifact.
- Never invent dataset sizes, agreement scores, or source counts at outlining time. Use placeholders (`N=[TODO]`) and mark unresolved provenance `[NEEDS-EVIDENCE]`.

## Draft requirement

The matching `.writing/manuscript/<NN>_construction.tex` is organized as subsections: the paradigm and one subsection per stage, ending with a statistics subsection. The LaTeX-comment-tag rule applies at the paragraph level: at least one paragraph per element carries the matching `% construction: X` tag plus the required `% claim: id` tag (§Construction stem does not end in an unprotected slug, so every load-bearing paragraph needs a claim tag or `% draft-only`).

```latex
\section{Benchmark Construction}
\label{sec:construction}

% construction: PD
% claim: con-c1
<paragraph: name the paradigm and justify it. Reference the pipeline figure.>

\begin{figure}[t]
  \centering
  % Figure 2: the pipeline, left-to-right, with per-stage data counts on arrows
  % and quality gates as distinct shapes. Show one concrete sample flowing through.
  \caption{Construction pipeline. Arrows annotate sample counts at each stage.}
  \label{fig:pipeline}
\end{figure}

\subsection{Source Selection}

% construction: SS
% claim: con-c2
<paragraph: sources, licensing, filtering, dedup. Cite borrowed corpora via
\cite{source-a,source-b}.>

\subsection{Seed Generation}

% construction: SG
% claim: con-c3
<paragraph: paradigm-specific generation; how ground truth is fixed.>

\subsection{Enrichment and Annotation}

% construction: EN
% claim: con-c4
<paragraph: metadata, taxonomy tags, difficulty labels.>

\subsection{Quality Control}

% construction: QC
% claim: con-c5
<paragraph: agreement metric with threshold, spot-check rate, sanity checks.>

\subsection{Splitting}

% construction: SP
% claim: con-c6
<paragraph: stratified split strategy and contamination mitigation.>

\subsection{Dataset Statistics}

% construction: ST
% claim: con-c7
<paragraph: Table~\ref{tab:stats} reference; counts, distributions, scale
comparison. Numbers must match the table exactly.>
```

Rules:

- Put `% construction: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- **The pipeline MUST be visualized.** Reference `Figure~\ref{fig:pipeline}` from the paradigm paragraph; the figure is a separate claim (`type: figure`). A construction section with no pipeline figure fails drafting self-review.
- **Every stage states input, operation, output, and quality gate.** A stage paragraph that omits its quality gate fails self-review; quality gates are what make the data trustworthy.
- **Quality control reports a concrete agreement number with a threshold.** Forms like "annotators agreed well" fail; "Cohen's kappa = 0.81 (threshold 0.75)" passes. Escape `%` as `\%` in LaTeX prose.
- **Dataset-statistics numbers in prose MUST match the statistics table** (Pass 3 of claim-verification checks this). The constructed dataset is a `type: dataset` EVIDENCE entry, not a citation.
- **Length budget:** roughly 1,500–3,500 words. This is the heaviest section; under-specifying it is the most common benchmark-paper rejection cause.

## Style rules

- **Tense:** past tense for the construction actions performed ("We sampled 2,000 seeds"; "Two annotators labeled each sample"). Present tense only for describing stable properties of the released dataset ("The benchmark contains 18,400 examples") and for referencing figures and tables ("Figure 2 shows the pipeline").
- **Voice:** active voice. First-person plural ("we construct", "we annotate") is standard.
- **Reproducibility discipline.** Each stage names who performs it (automated script, model, human annotator, domain expert), how long it takes, and what can go wrong. A pipeline a reader cannot re-run is not reproducible, which defeats the benchmark's purpose.
- **Citations:** cite borrowed source corpora and any prior pipeline whose method is reused. Do not cite the constructed dataset itself; it is this paper's artifact and is referenced as a `type: dataset` EVIDENCE entry.
- **Never fabricate provenance.** Do not invent source URLs, license identifiers, annotator counts, or agreement scores. Mark unresolved items `[NEEDS-EVIDENCE]` and let the user supply them. A benchmark paper rests on its construction integrity; a fabricated statistic here is the most damaging kind.
- **Contamination transparency.** State explicitly how the construction resists training-data contamination (time-gating, synthetic generation, novel sources, private evaluation scripts). Reviewers increasingly require this; omitting it invites a major-revision request.

## Common failure modes

- **Vague pipeline.** Stages described in one sentence each with no inputs, operations, or gates. Symptom: reviewer writes "the construction process is unclear; I cannot assess data quality". Fix: document every stage with explicit input, operation, output, and quality gate; add the pipeline figure with per-stage counts.
- **No quality gate.** The pipeline generates data but reports no inter-annotator agreement, spot-check, or sanity check. Symptom: reviewer writes "how do you know the labels are correct?". Fix: add at least three quality-control strategies; report a concrete agreement metric with its threshold.
- **Missing contamination mitigation.** No statement of how the benchmark resists data leakage into model training sets. Symptom: reviewer writes "the data may already be in training corpora". Fix: add a contamination subsection naming the mitigation (time-gating, synthetic sources, private scripts).
- **Unnamed paradigm.** The section lists steps without declaring whether ground truth comes from reverse synthesis, controlled injection, or adaptive generation. Symptom: reviewer cannot tell how ground truth was established. Fix: open with the paradigm and its rationale, then map the stages onto it.
- **Statistics divorced from the table.** Prose cites dataset sizes that do not match the statistics table. Symptom: claim-verification Pass 3 flags the mismatch; reviewers lose trust. Fix: make every prose number derive from the statistics table; update both in the same edit.
