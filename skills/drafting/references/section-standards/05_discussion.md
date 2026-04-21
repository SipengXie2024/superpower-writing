---
section: discussion
stem: 05_discussion
framework: ILFS
---

# Discussion — ILFS Standard (CS)

The §Discussion section is where §Results' numbers become arguments. Readers arrive with quantitative findings; Discussion tells them *what those findings mean, what they cannot claim, where the work goes next, and why any of it matters*. It MUST follow the **ILFS** four-part structure: Interpretation → Limitations → Future work → Significance/Implications. This is the most common "八股" across CS, ML, systems, and engineering venues.

**Slug convention.** Keep the manuscript filename as `NN_discussion.md` regardless of the rendered section title ("§6 Discussion" / "§6 Analysis and Discussion"). The orchestrator matches `discussion.md` by slug.

**Merged form.** Some CS venues (NeurIPS, ICML, ICLR, some short systems workshops) routinely merge §Discussion and §Conclusion into a single section titled "Discussion and Conclusion" or "Concluding Remarks". When the paper opts for the merged form, keep this file's structure for the Discussion half and append the three-sentence Conclusion (RSF pattern — see `conclusion.md`) at the end. In the merged case, the RSF `[F]` Forward-look is redundant with ILFS `[F]` Future work; drop one to avoid duplication (usually drop the Conclusion's forward-look and keep Discussion's `[F]` paragraph as the canonical future-work statement).

**Scope.** CS / ML / systems / DB / graphics. Clinical and biology papers follow different Discussion conventions (BARS, PRISMA-flavored discussion templates); those are handled upstream by `peer-review`, not by this file.

**Hard constraint: do not re-report §Results numbers.** A §Discussion paragraph that opens with "Our approach achieved 85.3% accuracy, a 3.2 pp improvement…" is duplicating §Results. Instead, reference the result abstractly ("The 3-point accuracy gain on ImageNet") and move directly into *why* it happened or *what it implies*. The single exception: the `[I]` Interpretation paragraph may restate a headline number *once* as the anchor for its causal explanation; everything else should reference numbers by description.

## Framework

**ILFS = Interpretation, Limitations, Future, Significance.** Four elements in a strict sequence that answer, in order: *why did the results come out as they did → what can we not claim from them → where does this work go next → why should the reader care*.

Why this structure dominates: papers that skip `[I]` leave reviewers to invent their own interpretations (often uncharitable ones). Papers that skip `[L]` trigger the single most common reviewer complaint in CS ("limitations not acknowledged"). Papers that skip `[F]` miss the opportunity to pre-empt "follow-up direction" critiques. Papers that skip `[S]` fail to earn their conclusion — the reader finishes unsure what the contribution unlocks. All four are load-bearing; none is optional.

## Role of each element

| Element                              | Purpose                                                                                         | Typical content                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **I — Interpretation**               | Explain *why* the results look the way they do. Mechanism, causation, alignment with prior work. | 1–3 paragraphs. Each grounded in a specific §Results finding. May compare to prior CS literature. |
| **L — Limitations**                  | State the boundaries of what this paper can claim. Threats to internal and external validity.   | 1–2 paragraphs. Specific, concrete limitations — not aesthetic hedging. Include scope boundaries, baselines not tested, settings not evaluated. |
| **F — Future work**                  | Propose concrete next directions the findings open up. Not wishlist; specific projects.         | 1–2 paragraphs OR a bulleted list of 2–4 items. Each item actionable enough to be a separate paper. |
| **S — Significance / Implications**  | Spell out what the paper changes for practitioners, researchers, or the broader field.          | 1–2 paragraphs. Answer "so what?" without re-reporting results. Theoretical / practical / empirical implications. |

The `[I]` element does the most narrative heavy-lifting. The other three are defensive (`[L]`), generative (`[F]`), and evaluative (`[S]`); they are shorter on average. A Discussion where `[L]` exceeds `[I]` suggests the paper is over-hedged.

## Outline bullet requirement

`.writing/outline.md` §Discussion MUST contain **4–8 bullets total**, with at least one bullet per element, appearing in the strict order I → L → F → S. Each bullet MUST be prefixed with its element label in square brackets:

- `[I]` — Interpretation
- `[L]` — Limitations
- `[F]` — Future work
- `[S]` — Significance / Implications

```
## Discussion

- [I] <why did RQ1's headline result appear as it did — causal / mechanistic explanation>
- [I] <why did RQ2's scaling curve appear as it did>
- [L] <specific threat to validity, e.g., dataset is English-only, no adversarial evaluation>
- [L] <scope limitation, e.g., only tested on hardware class X, not Y>
- [F] <concrete next direction 1>
- [F] <concrete next direction 2>
- [S] <practical implication for practitioners or system designers>
- [S] <theoretical implication for the research field>
```

Rules:

- All `[I]` bullets before any `[L]`; all `[L]` before any `[F]`; all `[F]` before any `[S]`. No interleaving.
- Typical distribution: 1–3 `[I]` + 1–2 `[L]` + 1–2 `[F]` + 1–2 `[S]`, totaling 4–8 bullets.
- Every `[I]` bullet SHOULD ground its explanation in a specific §Results finding (reference by RQ number: "RQ1's 3.2 pp improvement is explained by…").
- Every `[L]` bullet MUST be concrete, not aesthetic. "Our approach has limitations" is not a limitation; "Our evaluation uses only English-language benchmarks; cross-lingual performance is untested" is.
- Every `[F]` bullet MUST be actionable — specific enough that a reader could scope it as a follow-up paper. "Explore more efficient variants" is vague; "Replace the dense attention in §3.3 with a sparse variant at input lengths > 16k to test whether gains persist" is actionable.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_discussion.md` using `disc-c1`, `disc-c2`, …

## Draft requirement

The matching `.writing/manuscript/<NN>_discussion.tex` is organized as four subsections (or sometimes as four paragraphs with implicit headings). The LaTeX-comment-tag rule applies at the **paragraph** level: at least one paragraph per element type carries the matching `% discussion: X` tag, plus the required `% claim: id` tag:

```latex
\section{Discussion}
\label{sec:discussion}

\subsection{Interpretation}

% discussion: I
% claim: disc-c1
<paragraph: why RQ1 result appeared as it did --- causal / mechanistic
argument. Grounded in \S\ref{sec:results} finding. Compare to prior-work
expectations if relevant.>

% discussion: I
% claim: disc-c2
<paragraph: why RQ2's scaling behavior appeared as it did. Mechanism-oriented,
not number-oriented.>

\subsection{Limitations}

% discussion: L
% claim: disc-c3
<paragraph: specific threat to validity. Internal or external. Concrete scope
boundary with a named example.>

\subsection{Future Work}

% discussion: F
% claim: disc-c4
<paragraph OR \begin{itemize}...\end{itemize}: 2--4 actionable next
directions.>

\subsection{Implications}

% discussion: S
% claim: disc-c5
<paragraph: practical implication for practitioners / system designers /
researchers. Theoretical significance. ``So what?'' answer.>
```

Rules:

- Put `% discussion: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- **Subsection titles** can be freely renamed (`\subsection{Why X works}` / `\subsection{Threats to validity}` / `\subsection{Future directions}`). The `% discussion: X` tag tracks structure; subsection prose is editorial.
- **Section boundaries**: §Discussion does NOT re-cite baselines' numeric comparisons (those live in §Results) and does NOT introduce new experiments (those belong earlier or in revision). The only new material allowed in §Discussion is interpretation, limitation acknowledgment, and extrapolation.
- **Length budget:** ~800–2,000 words total. Short ML workshop papers may compress to ~400 words; long systems papers may push to ~3,000 words. Interpretation (`[I]`) should occupy 35–50% of the budget; Limitations 15–25%; Future work 10–20%; Implications 15–25%.
- **Figures and tables** are typically absent from §Discussion. An occasional qualitative example or schematic explaining a mechanism is acceptable. Quantitative tables belong in §Results.

## Style rules

- **Tense:**
  - I: simple present for mechanisms ("The attention pattern allows the model to …"); simple past for observed causes grounded in §Results ("The 3-point gain came from …").
  - L: simple present for current scope boundaries ("Our evaluation does not include …"); simple past for methodological choices ("We did not test cross-lingual transfer").
  - F: simple present imperative-adjacent for proposed directions ("A natural extension is …"); simple future for outlook ("Future work should investigate …").
  - S: simple present for implications ("These findings suggest that …"); simple present for significance claims ("This is the first result to …").
- **Voice:** active voice. First-person plural ("we attribute", "we interpret", "we conjecture") is standard when making arguments; avoid passive hedging ("it could be argued that…").
- **Hedging calibration.** CS Discussion sections tend to under-hedge on implications and over-hedge on limitations. Calibrate: use "suggest" / "indicate" / "we hypothesize" for interpretations that rely on mechanism; use "demonstrate" / "show" only for claims the §Results numbers directly establish. For limitations, use concrete scope statements rather than apologetic softeners ("Our evaluation does not cover X" rather than "Our evaluation might have some limitations potentially including X").
- **Prior-work comparison.** Discussion is the natural place to compare findings with prior CS literature ("Contrary to Smith et al.'s report of …, we find …"). Cite specifically; do not make sweeping claims about "the literature" without citations.
- **Limitation language.** Acceptable patterns: "Our evaluation is limited to …", "We did not test …", "Results may not generalize to …". Avoid empty hedges ("further research is needed", "more work is warranted").
- **Future-work actionability.** Each `[F]` bullet should name (a) what would be done, (b) why it is a natural extension of this paper, and (c) what success would look like. Vague "explore X" items signal the author has not actually thought about the follow-up.
- **No forward references by section number.** "As discussed in §7" becomes wrong after a renumber. Refer by content.
- **Citations:** moderate density. `[I]` is citation-bearing (mechanism arguments often cite prior work); `[L]` is sparse (limitations are usually this paper's scope, not another paper's claim); `[F]` may cite preliminary work in the proposed direction; `[S]` may cite downstream applications that the work enables. Use the same DOI format as the rest of the paper.
- **No new experiments.** A Discussion that reports a new number ("we additionally tested X and found …") is smuggling §Results material. Either promote the experiment to §Results or delete.

## Common failure modes

- **Re-reporting §Results.** `[I]` paragraphs lead with "Our approach achieved 85.3% accuracy…". Symptom: Discussion reads as a Results recap. Fix: reference findings abstractly ("the 3-point gain") and move into the causal argument immediately.
- **Missing `[L]`.** Discussion lists interpretations and implications but no limitations. Symptom: reviewer writes "limitations not adequately discussed" — this is the single most common reviewer complaint for CS papers. Fix: include at least one `[L]` paragraph with 2–3 specific, concrete limitations.
- **Aesthetic limitations.** `[L]` consists of meaningless hedges ("limitations exist", "more research is needed"). Symptom: reviewer writes "limitations are too vague". Fix: make each limitation concrete, scoped, and specific — name the untested setting, the missing baseline, the unevaluated metric.
- **Future work wishlist.** `[F]` lists 8 tangentially related follow-ups. Symptom: reader can tell the author has not prioritized. Fix: pick 2–4 follow-ups that are natural extensions of this paper's findings; each should be scoped enough to be a distinct project.
- **Unhinged significance claims.** `[S]` overreaches ("This work will revolutionize AI"). Symptom: reviewer flags as overclaim; fairness scores drop. Fix: calibrate against what §Results actually establishes. Significance claims bounded by evidence.
- **Interpretation disconnected from §Results.** `[I]` paragraphs explain a mechanism that does not obviously link to any specific §Results finding. Symptom: reviewer writes "the interpretation does not follow from the reported results". Fix: every `[I]` paragraph should reference a specific RQ or table/figure in §Results as the empirical anchor for its explanation.
- **New experiments smuggled in.** `[I]` includes numbers not in §Results. Symptom: reviewer flags the math, asks where it came from. Fix: move all numeric claims to §Results; §Discussion only interprets.
- **Future work contradicts Limitations.** `[F]` proposes doing something `[L]` said was out of scope. Symptom: structural incoherence. Fix: either move the item from `[F]` to §Results (if actually done) or from `[L]` to §Results caveats (if actually addressed).
- **Merged Discussion-Conclusion without RSF ending.** When the paper uses "Discussion and Conclusion", some authors stop after §Significance without an explicit Conclusion. Symptom: the paper ends abruptly. Fix: append a 2–3 sentence Conclusion (RSF pattern, see `conclusion.md`) as a closing paragraph; drop the RSF `[F]` if it duplicates ILFS `[F]`.
