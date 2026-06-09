---
section: findings
stem: benchmark_findings
framework: RSFF
---

# Empirical Findings: Benchmark Variant (CS)

The §Empirical Findings section reports what evaluating models on the benchmark reveals. Unlike a technique paper's §Results, its purpose is not to prove one method beats baselines. Its purpose is to reveal where and why model capability boundaries sit, and what that implies for future work. It MUST organize analysis around research questions and condense each major analysis into a bolded "Finding X:" sentence that reads like a lemma. The section often renders as "§5 Experiments" or "§5 Evaluation".

**Slug convention.** Keep the manuscript slug as `findings` regardless of the rendered title. Author it as `.writing/manuscript/NN_findings.tex` so the slug-ending match resolves here. See `benchmark_README.md` for the full benchmark-variant resolution table.

**Scope.** Benchmark and dataset papers for CS / ML / NLP / CV / systems / databases. Technique papers use `04_results.md` (RSRT); the structures overlap on RQs and Setup but diverge on the Finding-X convention and the capability-boundary purpose.

## Framework

**RSFF = Research questions, Setup, per-RQ Findings, Forward opportunities.** Four elements that answer, in order: what does the evaluation ask, how is it run, what does each analysis reveal as a bolded Finding, and what future work do the Findings open. The middle element is the benchmark paper's signature: every major analysis ends in a numbered, bolded Finding.

The benchmark variant differs from technique-paper §Results in two ways. First, the baselines are many models across architecture families and scales (typically 10–15), not a few competitors. Second, the unit of reporting is the Finding, a lemma-like sentence that states a capability boundary and points at future work, not a leaderboard delta.

## Role of each element

| Element | Purpose | Typical content |
|---------|---------|-----------------|
| **RQ: Research Questions** | Declare the 2–4 questions the evaluation answers. | Numbered list covering construction quality, capability boundaries, and the human-vs-model gap. |
| **S: Setup** | Specify the evaluated models and the protocol so results are reproducible. | 10–15 models across open/closed, scale, architecture, specialization; prompting strategies; metrics; repetitions; temperature; human baseline when available. |
| **F: per-RQ Findings** | One subsection per RQ; each major analysis ends in a bolded Finding. | The overall-performance table, category breakdown, difficulty gradient, error taxonomy; each analysis followed by a bolded "Finding X:" sentence. |
| **FO: Forward Opportunities** | Derive future-research directions from the Findings. | 3–5 directions, each traceable to a specific Finding. |

The overall-performance table is non-optional and is usually the largest table in the paper. The human baseline is strongly recommended when the task admits one.

## The "Finding X:" convention

This is the signature writing technique of a benchmark paper. After each major analysis, extract one bolded, numbered Finding that reads like a lemma. A Finding is a claim a future reader cites by number.

Each Finding MUST be:

- **Surprising or non-obvious.** "Bigger models are better" is not a Finding. "Models above 70B parameters gain on reasoning cells but not on retrieval cells" is.
- **Specific.** It names concrete models, categories, or conditions, not "models in general".
- **Actionable for future work.** It implies what future research should address. A Finding that closes inquiry rather than opening it is under-using the convention.
- **Supported by data.** It is backed by the analysis directly above it, with numbers.

Micro-structure for each Finding paragraph: a lead sentence stating the result in one line, then the evidence (specific numbers, models, conditions), then the scope and boundary conditions, then a forward pointer to what it implies. The forward pointer is what makes the Finding actionable.

## Outline bullet requirement

`.writing/outline.md` §Findings MUST contain **7–14 bullets total**, satisfying:

- **2–4 `[RQ]` Research Question bullets**, covering construction quality, capability boundaries, and the human-AI gap.
- **1–2 `[S]` Setup bullets** listing the model panel, prompting strategies, metrics, repetitions, and human baseline.
- **As many `[F]` Finding bullets as `[RQ]` bullets, in matching order.** Each `[F]` bullet states the bolded Finding the matching RQ produces, with a headline number.
- **1–2 `[FO]` Forward-opportunity bullets** deriving future directions from the Findings.

Bullets MUST appear in the strict order RQ → S → F → FO, each prefixed with its label:

```
## Findings

- [RQ] RQ1: Do current models handle the four ambiguity types, and where do they fail?
- [RQ] RQ2: Does model scale close the capability gap on ambiguous queries?
- [RQ] RQ3: How does the human baseline compare to the best model?
- [S] Models: 13 LLMs across open/closed, 7B-100B+, decoder-only and encoder-decoder; zero-shot and 3-shot; execution accuracy; 3 runs; temperature 0.
- [F] Finding 1: all 13 models score below 30% on severity-5 ambiguity, revealing a clarification blind spot.
- [F] Finding 2: scale improves type-A ambiguity monotonically but has no effect on type-D, suggesting different scaling properties.
- [F] Finding 3: humans reach 82% via clarification dialogue versus 41% for the best model, isolating interaction as the gap.
- [FO] Forward opportunity: clarification-dialogue training targeted at the severity-5 blind spot.
```

Rules:

- All `[RQ]` before any `[S]`, all `[S]` before any `[F]`, all `[F]` before any `[FO]`. No interleaving.
- **`[F]` bullet count MUST equal `[RQ]` bullet count** (each RQ yields exactly one headline Finding; supporting analyses can produce extra Findings inside the subsection at drafting time, but the outline tracks one per RQ).
- Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_findings.md` using `find-c1`, `find-c2`, … The `[F]` claims resolve to `type: analysis`, `type: table`, or `type: figure`; baseline numbers borrowed from prior papers go in `[S]` with `type: citation`.
- Each `[F]` bullet SHOULD carry a headline number at outline time. Never fabricate model scores; use placeholders (`N=[TODO]`) until the runs exist.

## Draft requirement

The matching `.writing/manuscript/<NN>_findings.tex` is organized as subsections: research questions, setup, one subsection per RQ, forward opportunities. The LaTeX-comment-tag rule applies at the paragraph level: at least one paragraph per element carries the matching `% findings: X` tag plus the required `% claim: id` tag.

```latex
\section{Experiments}
\label{sec:findings}

\subsection{Research Questions}

% findings: RQ
% claim: find-c1
We evaluate along three research questions:
\begin{itemize}
  \item \textbf{RQ1:} Do current models handle the four ambiguity types?
  \item \textbf{RQ2:} Does scale close the gap on ambiguous queries?
  \item \textbf{RQ3:} How does the human baseline compare?
\end{itemize}

\subsection{Setup}

% findings: S
% claim: find-c2
<paragraph: the model panel across axes, prompting strategies, metrics,
repetitions, temperature, human baseline. Cite model sources via \cite{...}.>

\subsection{RQ1 --- Per-type capability}

% findings: F
% claim: find-c3
<paragraph: the overall-performance table reference + per-type analysis.
NO interpretation beyond the Finding.>

\begin{table}[t]
  \centering
  \caption{Overall performance. Bold is best per column; underline is second.}
  \label{tab:overall}
  % Largest table in the paper: all models x all dimensions, grouped by
  % closed/open/specialized, with a human row when available.
\end{table}

\noindent\textbf{Finding 1.} <one-sentence lemma>. <evidence: numbers, models,
conditions>. <scope and boundary>. <forward pointer to future work>.

\subsection{RQ2 --- Scale effect}

% findings: F
% claim: find-c4
<paragraph: scale analysis + Figure~\ref{fig:scale} reference.>

\noindent\textbf{Finding 2.} <lemma + evidence + scope + forward pointer>.

\subsection{Forward Opportunities}

% findings: FO
% claim: find-c5
<paragraph: 3-5 future directions, each traceable to a Finding above.>
```

Rules:

- Put `% findings: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- **Every RQ subsection ends in at least one bolded Finding.** A subsection that reports numbers without extracting a Finding fails self-review; the Finding is the unit of contribution.
- **The overall-performance table is required and MUST be referenced** from the first `[F]` subsection. It is a separate claim (`type: table`). Bold the best per column; group models by category; include a human row when available.
- **Every headline number carries a comparator and, where applicable, uncertainty.** "Models do poorly" fails; "all 13 models score below 30\% on severity-5, versus 82\% for humans" passes. Report mean ± std for non-deterministic setups. Escape `%` as `\%`.
- **Findings state facts and a forward pointer, not mechanism.** The "why this happens" mechanism belongs in §Discussion; the Finding's forward pointer says what future work should address, which is a direction, not a causal explanation.
- **Length budget:** roughly 1,500–4,000 words, lean longer than a technique paper's §Results because the model panel is large and the analyses are multi-angle.

## Style rules

- **Tense:** past tense for reported measurements ("GPT-class models scored 41\%"). Present tense for table and figure references ("Table 2 reports per-cell accuracy") and stable setup properties ("The panel spans 13 models").
- **Voice:** active voice. First-person plural for the evaluation acts ("we evaluate", "we measured").
- **Number presentation.** Absolute numbers carry units; comparative numbers carry a baseline anchor; non-deterministic results carry mean ± std over the stated number of runs. Use 2–3 significant figures.
- **Baseline fairness.** Document equal optimization effort across models; under-tuning competitors ("baseline nerfing") is a reviewer red flag. Each model uses its best known configuration.
- **Citations:** cite model sources and any borrowed baseline number in §Setup. Do not cite this paper's own measured results.
- **Negative-result transparency.** Report cells where every model fails; those are often the most actionable Findings. Omitting them invites distrust during reproducibility checks.
- **Never fabricate scores.** Do not invent model accuracies, human-baseline numbers, or agreement statistics. Mark unresolved items `[NEEDS-EVIDENCE]` until the runs exist.

## Common failure modes

- **Leaderboard without Findings.** The section reports a big table and per-cell numbers but extracts no bolded Findings. Symptom: reviewer writes "what did we learn beyond a ranking?". Fix: after each analysis, extract a numbered, bolded Finding that states a capability boundary and points at future work.
- **Obvious Findings.** Findings restate "bigger models are better" or "the task is hard". Symptom: reviewer writes "the findings are not surprising". Fix: make each Finding specific and non-obvious, naming the cells or model families where behavior diverges.
- **Findings with no forward pointer.** Findings state a result but do not say what future work should address. Symptom: §Forward Opportunities feels disconnected. Fix: end each Finding with a one-clause implication; derive §Forward Opportunities directly from those clauses.
- **Too few models.** The panel has three or four models. Symptom: reviewer writes "the evaluation is too narrow to characterize the capability landscape". Fix: evaluate 10–15 models across open/closed, scale, architecture, and specialization axes.
- **No human baseline on a human-judgeable task.** The task admits a human upper bound but only model numbers are reported. Symptom: reviewer asks "how far are models from humans?". Fix: run a human baseline on a sample and report it as a row in the overall table.
- **Mechanism creep into Findings.** Finding paragraphs explain why a result happened ("because attention dilutes over long inputs"). Symptom: §Discussion becomes redundant. Fix: keep Findings factual with a forward pointer; move causal explanation to §Discussion.
