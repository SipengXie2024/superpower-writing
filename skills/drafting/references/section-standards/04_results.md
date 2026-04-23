---
section: results
stem: 04_results
framework: RSRT
---

# Results — RSRT Standard (CS)

The §Results section reports the empirical findings the paper's contribution produces. In CS it is variously titled §Evaluation, §Experiments, §Empirical Evaluation, or §Experimental Evaluation; the underlying "八股" is the same. It MUST follow the **RSRT** four-part structure: Research Questions → Setup → Per-RQ Results → Takeaways. This structure forces the paper to state *what it is measuring and why* before reporting numbers, which is the single most effective defense against reviewer complaints about cherry-picking or unclear evaluation scope.

**Slug convention.** Keep the manuscript filename as `NN_results.tex` regardless of the rendered section title. The orchestrator matches `results` by slug-ending; a paper rendered as "§5 Evaluation" still authors as `.writing/manuscript/04_results.tex` with `## Results` as the outline heading.

**Scope.** CS / ML / NLP / CV / systems / databases / graphics. Clinical and biology papers follow CONSORT / STROBE / PRISMA reporting conventions, not this file — those are handled by upstream `peer-review`.

**Discussion boundary.** §Results states facts; §Discussion interprets them. Do NOT write "this demonstrates that our approach is superior" in §Results — that belongs in §Discussion. §Results may use neutral comparative language ("X outperforms Y by 3.2 pp") but never causal or evaluative language ("X is better because…"). The only exception is the `[T]` Takeaways element, which allows a tight one-paragraph synthesis of headline findings without explanation.

## Framework

**RSRT = Research Questions, Setup, (per-RQ) Results, Takeaways.** Four elements in a strict sequence that answer, in order: *what are we trying to measure → how are we measuring it → what did we measure → what is the headline pattern*.

Why this structure dominates: papers that skip RQ force reviewers to reverse-engineer the evaluation scope from the results, often incorrectly; papers that skip S bury setup details in §Methods, forcing readers to flip back and forth; papers that skip T leave reviewers with twelve tables and no synthesis of what was learned. The four elements are sequenced and non-optional (with T being the only soft element — a dense results section with a clear table caption can sometimes omit T).

## Role of each element

| Element                          | Purpose                                                                                    | Typical content                                                                                        |
|----------------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **RQ — Research Questions**      | Declare the 3–5 specific questions the evaluation answers. Sets scope.                     | Numbered list: "RQ1: Does X outperform baselines on Y? RQ2: How does X scale with input size?"         |
| **S — Setup**                    | Specify the experimental apparatus so results are reproducible and comparable.             | Datasets, baselines, metrics, hardware, training regime, hyperparameter search protocol.               |
| **R — (per-RQ) Result**          | One subsection per RQ reporting findings with numbers, tables, and figures. NO interpretation. | Headline number with comparator and uncertainty; supporting figure or table; brief factual narration. |
| **T — Takeaways**                | One-paragraph synthesis of the headline findings across RQs.                               | "Across RQ1–RQ3, X achieves SOTA on Y while preserving linear scaling and requiring no architectural changes." |

The `[R]` element stands in 1-to-1 correspondence with `[RQ]`: every RQ deserves exactly one R result, and no R result may exist without a corresponding RQ. Papers that report measurements without a matching RQ are padding the evaluation.

## Outline bullet requirement

`.writing/outline.md` §Results MUST contain **7–15 bullets total**, satisfying these rules:

- **3–5 `[RQ]` bullets.** Fewer than 3 RQs means the evaluation is too narrow to defend a CS paper; more than 5 RQs means the questions are over-fragmented — merge.
- **1–3 `[S]` bullets.** Setup can be consolidated into one bullet ("[S] Datasets X, Y, Z; baselines A, B; metrics top-1 accuracy, FLOPs; hardware 8× A100") or split across dimensions (one bullet per dimension). Either works; 1 is common for short papers.
- **Exactly as many `[R]` bullets as `[RQ]` bullets, in matching order.** If the outline has `[RQ] RQ1`, `[RQ] RQ2`, `[RQ] RQ3`, then the `[R]` bullets must be in the same order: `[R] RQ1 result`, `[R] RQ2 result`, `[R] RQ3 result`.
- **0–2 `[T]` bullets.** Optional but recommended; 1 bullet suffices for most papers.

Each bullet MUST be prefixed with its element label in square brackets, and all bullets MUST appear in the strict order RQ → S → R → T:

```
## Results

- [RQ] RQ1: Does X outperform baselines on benchmark Y?
- [RQ] RQ2: How does X scale with input size?
- [RQ] RQ3: Which components of X contribute most to its performance?
- [S] Datasets: CIFAR-10, ImageNet; baselines: ViT-B, MAE; metrics: top-1 accuracy, FLOPs, latency; hardware: 8× A100 80GB.
- [R] RQ1 result: X improves top-1 accuracy from 82.1% to 85.3% (+3.2 pp; 95% CI [2.7, 3.7]) over ViT-B on ImageNet.
- [R] RQ2 result: X scales linearly up to 1M-token inputs, 4.1× lower latency than ViT-B at 512k tokens.
- [R] RQ3 result: Ablation reveals component C contributes 2.1 of the 3.2 pp improvement; components A and B contribute <0.6 pp each.
- [T] Across RQ1–RQ3, X achieves SOTA on ImageNet while preserving linear scaling; ablation confirms the novel C module is the primary source of gains.
```

Rules:

- All `[RQ]` bullets before any `[S]`; all `[S]` before any `[R]`; all `[R]` before any `[T]`. No interleaving.
- **`[R]` bullet count MUST equal `[RQ]` bullet count.** The outlining self-review in Step 7 enforces this.
- Each `[R]` bullet SHOULD already contain the headline number with comparator and (where available) uncertainty. Placeholder ranges (`N=[TODO]`) are acceptable at outlining time but every final bullet must carry a concrete number before drafting can begin.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_results.md` using `res-c1`, `res-c2`, … The `[R]` claims typically resolve to `type: analysis` (a computed statistic in this paper) or `type: figure` / `type: table`; not to `type: citation` (that would be prior work, not this paper's result).

## Draft requirement

The matching `.writing/manuscript/<NN>_results.tex` is typically organized as multiple subsections: §Research Questions, §Setup, §Per-RQ Results (usually one subsection per RQ), §Takeaways. The LaTeX-comment-tag rule applies at the **paragraph** level: at least one paragraph per element type carries the matching `% results: X` tag, plus the required `% claim: id` tag (§Results stem does not end in an unprotected slug).

```latex
\section{Results}
\label{sec:results}

\subsection{Research Questions}

% results: RQ
% claim: res-c1
We evaluate X along three research questions:
\begin{itemize}
  \item \textbf{RQ1:} Does X outperform baselines on benchmark Y?
  \item \textbf{RQ2:} How does X scale with input size?
  \item \textbf{RQ3:} Which components of X contribute most to performance?
\end{itemize}

\subsection{Experimental Setup}

% results: S
% claim: res-c2
<paragraph: datasets, preprocessing, splits. Cite benchmark sources via
\cite{cifar10,imagenet}.>

% results: S
% claim: res-c3
<paragraph: baselines, metrics, hardware, hyperparameter-search protocol.>

\subsection{RQ1 --- Comparison against baselines}

% results: R
% claim: res-c4
<paragraph: headline number + Table~\ref{tab:main} reference + brief factual
narration. NO interpretation.>

\begin{table}[t]
  \centering
  \caption{Main results on ImageNet.}
  \label{tab:main}
  \begin{tabular}{lrrr}
    \toprule
    Method  & Top-1 (\%) & FLOPs (G) & Latency (ms) \\
    \midrule
    ViT-B   & 82.1 & 17.6 & 14.3 \\
    X (ours)& \textbf{85.3} & 16.8 & 13.9 \\
    \bottomrule
  \end{tabular}
\end{table}

\subsection{RQ2 --- Scaling behavior}

% results: R
% claim: res-c5
<paragraph: scaling numbers + Figure~\ref{fig:scaling} reference.>

\subsection{RQ3 --- Ablation study}

% results: R
% claim: res-c6
<paragraph: ablation table + component contribution numbers.>

\subsection{Takeaways}

% results: T
% claim: res-c7
<paragraph: one-paragraph synthesis across RQs. No causal explanation ---
save that for \S\ref{sec:discussion}.>
```

Rules:

- Put `% results: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- **Every `[R]` subsection MUST anchor on a table or figure.** The `[R]` paragraph should explicitly reference `Table~\ref{tab:X}` or `Figure~\ref{fig:X}`; the table/figure itself is a separate claim (type: `figure` or `type: table`). Results paragraphs without a figure/table reference fail drafting self-review.
- **Every headline claim MUST carry a number with comparator.** Forms like "X outperforms baselines" fail; "X improves top-1 accuracy from 82.1\% to 85.3\% (+3.2 pp)" passes. Where applicable, include uncertainty (CI, standard deviation, p-value). Remember to escape `%` as `\%` in LaTeX prose.
- **Three-layer numeric discipline (Results layer).** §Results is the only layer that carries both absolute counts AND percent changes alongside each other (e.g., "19,130 to 11,189 units, a 41.5\% reduction"). §Abstract states percent only; §Introduction states direction only; §Results is the ground-truth breakdown. When the same effect is mentioned in all three places, the number shown in §Abstract and any direction claim in §Introduction MUST derive from the §Results breakdown --- if the breakdown changes after a revision, update §Abstract and §Introduction in the same commit to prevent drift.
- **Factual language only.** Use neutral comparative forms: "X outperforms Y by +3.2 pp" / "X reduces latency by 41\%" / "X scales linearly up to 1M tokens". Do NOT write "X demonstrates superiority" / "X is clearly better" --- those belong in §Discussion.
- **Subsection titles** can be freely renamed (`\subsection{Main Results}` / `\subsection{Benchmark Comparison}`). The `% results: X` tag tracks structure; subsection prose is editorial.
- **Length budget:** ~1,500–4,000 words total for most CS papers. ML benchmark papers lean longer (multiple benchmarks, multiple baselines, ablations); theoretical papers with mostly empirical sanity checks lean shorter. Short ML workshop papers may compress to ~800 words, but the RSRT elements all remain.
- **Figures and tables are load-bearing.** A CS §Results with fewer than 2 figures/tables is under-illustrated. Typical count: 1 main results table, 1–2 scaling or ablation figures, 0–1 qualitative example figure. Each table/figure MUST be referenced in an `[R]` paragraph.

## Style rules

- **Tense:**
  - RQ: simple present ("We evaluate X along three research questions…").
  - S: simple past for what was done ("We trained on CIFAR-10 for 100 epochs"); simple present for stable setup facts ("The model has 86M parameters").
  - R: simple past for measurements ("X achieved 85.3% accuracy"); simple present for reporting tables/figures ("Table 1 reports top-1 accuracy across five benchmarks"); simple past for observed patterns ("Latency scaled linearly up to 1M tokens").
  - T: simple present for headline findings ("X achieves SOTA on ImageNet").
- **Voice:** active voice. First-person plural ("we evaluate", "we measured") is standard.
- **Number presentation:**
  - Absolute numbers MUST carry units ("85.3%", "4.1× speedup", "1,247 MB memory", "0.82 F1").
  - Comparative numbers MUST carry a baseline anchor ("+3.2 pp over ViT-B", "4.1× lower than PyTorch baseline", "41% reduction from 2.4 s to 1.4 s").
  - Statistical results MUST carry uncertainty ("(95% CI [2.7, 3.7])", "(SD = 0.4)", "(p < 0.001)") when applicable to the subfield. ML papers vary on this — some always report CIs, some never; check venue norms.
  - Precision: 2–3 significant figures is standard for accuracy/latency/memory. Don't report "85.3247% accuracy" when the measurement uncertainty is ±0.1%.
- **Table conventions.** Main-result tables should: (a) highlight the best number per column in bold; (b) include the baseline(s) as explicit rows for direct comparison; (c) use consistent significant figures across cells; (d) caption the metric direction ("higher is better" / "lower is better") when non-obvious.
- **Figure conventions.** Error bars / CIs / standard deviations are required on empirical curves when reported as a claim. A performance curve without error bars invites reviewer suspicion.
- **Citations:** §Results is less citation-dense than §Background or §Related Work. Cite (a) benchmark / dataset sources in §Setup; (b) baseline sources in §Setup (when not already cited in §Related Work); (c) metric sources if the metric is non-standard. Do not cite results of THIS paper — those are self-references.
- **Claim-first integration.** Every `[R]` result has a corresponding claim with EVIDENCE of type `analysis`, `figure`, or `table`. Do not copy numbers from prior papers into `[R]` — those belong in `[S]` as baseline reference numbers, with `type: citation` EVIDENCE.

## Common failure modes

- **Results without RQs.** Section opens directly with "Table 1 shows…". Symptom: reviewer writes "the evaluation scope is unclear" or "why these specific experiments?". Fix: always write §5.1 Research Questions with 3–5 explicit RQs; the `[R]` subsections then answer them 1-to-1.
- **Interpretation creep.** `[R]` paragraphs include sentences like "This shows that our approach is fundamentally better because…". Symptom: §Discussion becomes redundant. Fix: scrub §Results for causal / evaluative language; move all "because" / "demonstrates" / "indicates" sentences to §Discussion.
- **Cherry-picking.** Only favorable metrics reported; unfavorable ones omitted. Symptom: reviewer asks "how does X perform on metric Z?" when metric Z is standard in the subfield. Fix: report all conventional metrics even when your approach doesn't win; discuss unfavorable outcomes in §Discussion §Limitations.
- **Missing error bars.** Performance curves or benchmark tables reported without uncertainty estimates. Symptom: reviewer writes "the reported differences may not be statistically significant". Fix: run seeds or bootstrap CIs for every headline number; at minimum include standard deviation over 3–5 runs.
- **Tables without baseline comparator.** Main-result table lists only this paper's numbers, forcing the reader to flip to cited papers for comparison. Symptom: reviewer writes "comparison to prior work unclear". Fix: include explicit baseline rows in every main-result table.
- **Setup buried in §Methods.** Evaluation hyperparameters and baseline configurations appear only in §Methods §Implementation, not in §Results §Setup. Symptom: reviewers hunt across sections to confirm fair comparison. Fix: duplicate essential setup facts (dataset names, baseline names, metrics) into §Results §Setup; cross-reference §Methods for training details.
- **No ablation for ML papers claiming novel components.** Paper introduces novel components A, B, C and reports only end-to-end performance. Symptom: reviewer writes "unclear which component contributes to gains". Fix: add an ablation RQ + result subsection; isolate each component's contribution.
- **Takeaway paragraph is interpretation, not synthesis.** `[T]` reads as "this proves our approach is superior…" rather than a factual summary. Symptom: §Discussion has nothing left to say. Fix: `[T]` restates the headline numbers across RQs in one paragraph; save the "why" for §Discussion.
- **Too many tables without text anchoring.** §Results has six tables and three figures but only four paragraphs of text. Symptom: reviewer cannot follow the evaluation narrative. Fix: every table/figure MUST be referenced by at least one paragraph; untethered tables go to appendix.
