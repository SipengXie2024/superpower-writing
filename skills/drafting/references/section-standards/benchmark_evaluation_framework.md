---
section: evaluation_framework
stem: benchmark_evaluation_framework
framework: GSTM
---

# Evaluation Framework: Benchmark Variant (CS)

The §Evaluation Framework section defines what the benchmark measures and how. In a benchmark paper this section carries the contribution: the problem definition, the task scope, and the measurement taxonomy ARE the contribution, the way a method is the contribution in a technique paper. It MUST state design goals, fix the task scope, lay out a fine-grained taxonomy, and specify how each dimension is scored. It usually renders as "§2 Task and Design Goals" or "§2 Benchmark Overview", appearing before §Construction.

**Slug convention.** Keep the manuscript slug as `evaluation_framework` regardless of the rendered title. Author it as `.writing/manuscript/NN_evaluation_framework.tex` so the slug-ending match resolves here. See `benchmark_README.md` for the full benchmark-variant resolution table.

**Scope.** Benchmark and dataset papers for CS / ML / NLP / CV / systems / databases. Technique papers do not have this section; their problem statement is one element of §Methods (OFCA Formalization).

## The problem definition IS the contribution

State the evaluation dimension with the rigor a technique paper gives its method. A benchmark wins by defining a measurement that prior work could not make, then making it high-quality and reproducible. The gap statement, the design goals, and the taxonomy are not preamble to the data; they are the intellectual contribution the data serves. Treat a vague evaluation dimension as a missing contribution, not a stylistic weakness.

## Framework

**GSTM = Goals, Scope, Taxonomy, Measurement.** Four elements that answer, in order: what should a good benchmark for this dimension achieve, what does it cover and exclude, how is the capability decomposed, and how is each part scored.

1. **Goals (G).** Use the G1–G4 standard, plus custom goals as needed. G1 Coverage (the benchmark spans the breadth of the target capability). G2 Fine-grained diagnostics (it pinpoints where models fail, not just whether). G3 Scalability (construction is reproducible and extensible at low cost). G4 Quality (annotations are accurate and evaluation is reliable).
2. **Scope (S).** What the benchmark evaluates and, explicitly, what it does not, with a reason for each exclusion. Scope pre-empts the reviewer question "why didn't you include X?".
3. **Taxonomy (T).** The backbone of fine-grained evaluation, in one of three proven patterns: Capability × Difficulty matrix, Phenomenon type × Severity spectrum, or Multi-dimensional quality framework.
4. **Measurement (M).** How each sub-dimension is scored: the metric, the scoring method (exact match, model-as-judge, human rating), the range, and the automation level. When a model-as-judge is used, the framework states how the judge was validated against human ratings.

A framework that names goals but no taxonomy cannot support fine-grained findings. A taxonomy with no measurement spec cannot be applied. All four elements are required.

## Role of each element

| Element | Purpose | Typical content |
|---------|---------|-----------------|
| **G: Goals** | Declare what a good benchmark for this dimension must achieve. | G1 Coverage, G2 Diagnostics, G3 Scalability, G4 Quality, each with the strategy that meets it. |
| **S: Scope** | Fix the boundary; pre-empt "why not X?". | In-scope capabilities; out-of-scope capabilities each with a reason (different question, already covered, deferred). |
| **T: Taxonomy** | Decompose the capability for diagnosis. | One of: Capability × Difficulty; Phenomenon × Severity; Multi-dimensional quality. Dimensions, sub-dimensions, and the total evaluation-cell count. |
| **M: Measurement** | Specify how each dimension is scored. | Per-sub-dimension metric, scoring method, range, automation; model-as-judge validation when applicable. |
| *(Optional)* **Difficulty calibration** | State the expected top-model score on the hardest subset. | A sanity check that the hardest tier is hard enough to have headroom for future models. |

The optional difficulty-calibration note is recommended: a benchmark whose hardest subset is already near-saturated has a short useful life.

## Outline bullet requirement

`.writing/outline.md` §Evaluation Framework MUST contain **5–8 bullets total**, satisfying:

- **2–4 `[G]` Goal bullets**, at least covering coverage, diagnostics, and quality.
- **1 `[S]` Scope bullet** stating in-scope and out-of-scope with reasons.
- **1 `[T]` Taxonomy bullet** naming the pattern and the dimensions.
- **1–2 `[M]` Measurement bullets** specifying metrics and scoring per dimension.

Bullets MUST appear in the strict order G → S → T → M, each prefixed with its label:

```
## Evaluation Framework

- [G] G1 Coverage: span four ambiguity types across five severity levels via stratified sampling.
- [G] G2 Diagnostics: per-type, per-severity cells isolate where models fail.
- [G] G4 Quality: two-annotator labeling with kappa >= 0.75.
- [S] In scope: single-turn Text-to-SQL under ambiguity. Out of scope: multi-turn dialogue (different research question).
- [T] Taxonomy: Phenomenon x Severity; 4 ambiguity types x 5 severity levels = 20 evaluation cells.
- [M] Measurement: execution accuracy (exact match, auto) per cell; clarification-rate via model-as-judge, validated against 200 human labels.
```

Rules:

- All `[G]` before `[S]`, then `[T]`, then `[M]`. No interleaving.
- Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_evaluation_framework.md` using `eval-c1`, `eval-c2`, … The `[M]` model-as-judge-validation claim typically resolves to `type: analysis`; goal and scope bullets are usually design statements that bind to `type: analysis` or carry no external citation.
- Never fabricate cell counts, metric correlations, or validation sample sizes. Use placeholders and mark unresolved items `[NEEDS-EVIDENCE]`.

## Draft requirement

The matching `.writing/manuscript/<NN>_evaluation_framework.tex` is organized as subsections: design goals, task scope, taxonomy, measurement. The LaTeX-comment-tag rule applies at the paragraph level: at least one paragraph per element carries the matching `% eval: X` tag plus the required `% claim: id` tag (§Evaluation Framework stem does not end in an unprotected slug).

```latex
\section{Task and Design Goals}
\label{sec:eval}

% eval: G
% claim: eval-c1
We design the benchmark around four goals.
\begin{itemize}
  \item \textbf{G1 Coverage:} <strategy>.
  \item \textbf{G2 Fine-grained diagnostics:} <strategy>.
  \item \textbf{G3 Scalability:} <strategy>.
  \item \textbf{G4 Quality:} <strategy>.
\end{itemize}

\subsection{Task Scope}

% eval: S
% claim: eval-c2
<paragraph: what the benchmark evaluates; what it excludes and why.>

\subsection{Taxonomy}

% eval: T
% claim: eval-c3
<paragraph: the taxonomy pattern, dimensions, sub-dimensions, and total
evaluation-cell count. Reference Figure~\ref{fig:taxonomy} if the taxonomy
is shown as a matrix.>

\subsection{Evaluation Protocol}

% eval: M
% claim: eval-c4
<paragraph: per-sub-dimension metric, scoring method, range, automation.
If a model-as-judge is used, state how it was validated against human
ratings (correlation or agreement on a held-out set).>
```

Rules:

- Put `% eval: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- **Scope MUST state exclusions with reasons.** A scope paragraph that lists only in-scope capabilities fails self-review; the exclusions are what pre-empt reviewer pushback.
- **Taxonomy MUST give a concrete cell count.** "A fine-grained taxonomy" fails; "four types × five severity levels = 20 cells" passes. The cell count is what later lets §Findings report per-cell results.
- **Model-as-judge MUST report a validation number.** If scoring uses a model judge, the protocol states its correlation or agreement with human labels on a held-out set; an unvalidated model-judge is a reviewer red flag.
- **Length budget:** roughly 800–2,000 words. Shorter than §Construction; this section frames the contribution, §Construction delivers the data.

## Style rules

- **Tense:** present tense for the framework's stable design ("The taxonomy has four dimensions"; "Each cell is scored by execution accuracy"). Past tense only for the validation experiment ("We validated the judge against 200 human labels").
- **Voice:** active voice. First-person plural ("we evaluate", "we define") is standard.
- **Goal-to-strategy coupling.** Each design goal names the concrete strategy that meets it. A goal stated without a strategy ("we aim for high quality") is aspirational, not a design decision.
- **Taxonomy-to-gap coupling.** Explain why this taxonomy diagnoses the blind spot the §Introduction gap pointed at. A taxonomy disconnected from the gap reads as arbitrary.
- **Citations:** cite the prior benchmarks the scope positions against and any standard metric whose definition is borrowed. The benchmark's own definitions are this paper's contribution, not citations.
- **Never fabricate.** Do not invent cell counts, metric correlations, or human-validation sample sizes. Mark unresolved items `[NEEDS-EVIDENCE]`.

## Common failure modes

- **Vague evaluation dimension.** The section never states precisely what new thing is measured. Symptom: reviewer writes "the contribution is unclear; this looks like yet another dataset". Fix: state the evaluation dimension as the contribution, with the rigor a technique paper gives its method.
- **No out-of-scope statement.** Scope lists only what is included. Symptom: reviewer asks "why didn't you cover X?" repeatedly. Fix: list exclusions, each with a one-clause reason.
- **Single overall score, no taxonomy.** The benchmark reports one number per model with no fine-grained breakdown. Symptom: reviewer writes "this tells me models are bad but not where". Fix: add a taxonomy with dimensions and difficulty tiers; report per-cell results in §Findings.
- **Unvalidated model-as-judge.** Scoring uses a model judge with no check against human ratings. Symptom: reviewer writes "how do you know the judge is reliable?". Fix: report the judge's correlation or agreement with human labels on a held-out set.
- **Taxonomy unmoored from the gap.** The taxonomy's dimensions do not map to the evaluation blind spot the introduction raised. Symptom: reviewer cannot see why these dimensions. Fix: tie each dimension back to the gap; cut dimensions that diagnose nothing the gap named.
