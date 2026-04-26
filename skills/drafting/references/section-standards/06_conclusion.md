---
section: conclusion
stem: 06_conclusion
framework: RSF
---

# Conclusion — RSF Standard (CS)

The §Conclusion is the shortest load-bearing section of the paper. Its only job is to close cleanly: restate the contribution, name the headline result, gesture forward. It MUST follow the **RSF** three-part structure: Restate → Summary → Forward-look. Total length is 100–250 words; longer means the Conclusion is doing work that belongs in §Discussion.

**Slug convention.** Keep the manuscript filename as `NN_conclusion.md` regardless of the rendered section title ("§7 Conclusion" / "§7 Concluding Remarks" / "§7 Summary"). The orchestrator matches `conclusion.md` by slug.

**Merged form.** When the paper uses "§N Discussion and Conclusion" (common in NeurIPS / ICML / ICLR), append a 2–3 sentence Conclusion to the end of §Discussion, still following the RSF template, but drop the RSF `[F]` Forward-look element — it is redundant with §Discussion's ILFS `[F]` Future work. In that case, the merged-section Conclusion is effectively **RS only** (2 sentences: Restate, Summary).

**Optional section.** Short papers (4-page workshops, extended abstracts, some venue formats) sometimes omit §Conclusion entirely and let §Discussion's `[S]` Significance paragraph serve as the close. This is acceptable; only write `.writing/manuscript/NN_conclusion.tex` when the paper commits to a standalone §Conclusion section.

**Hard constraints:**

- **No new content.** The Conclusion MUST NOT introduce concepts, numbers, citations, or arguments not already in the paper. If a claim is important enough to state in §Conclusion, it is important enough to have appeared in §Results, §Discussion, or earlier.
- **No verbatim Abstract copy.** The Conclusion and the Abstract cover similar ground but serve different purposes; copying the Abstract text wholesale is lazy and reviewers notice. Paraphrase with a different sentence structure and emphasis.
- **Length ceiling: 250 words.** Conclusions exceeding this word count are almost always doing §Discussion's job. Trim.

## Framework

**RSF = Restate, Summary, Forward-look.** Three elements in strict order that cleanly close the paper:

1. **R — Restate contribution.** One sentence reminding the reader what the paper set out to do. This mirrors §Introduction M3 and the Abstract's M element, but paraphrased.
2. **S — Summary of headline result.** One sentence naming the principal empirical or theoretical finding. May reference a key number or qualitative characterization.
3. **F — Forward-look.** One sentence gesturing at what the work enables or where it leads. Higher-level than §Discussion's `[F]` Future work — not a follow-up project list but a horizon statement.

## Role of each element

| Element             | Purpose                                                     | Typical content                                                       |
|---------------------|-------------------------------------------------------------|-----------------------------------------------------------------------|
| **R — Restate**     | Re-anchor the reader on the paper's core contribution.      | One sentence. Paraphrase of §Abstract M / §Introduction M3.           |
| **S — Summary**     | Name the principal result in one line.                      | One sentence. Qualitative statement of the headline finding; may cite one top-line number but not a full table. |
| **F — Forward-look**| Close with a horizon statement.                             | One sentence. "This enables …" or "We envision …". Not a follow-up project list. |

Each element is typically one sentence. The whole section may fit in a single paragraph (three sentences) or three very short paragraphs. Both forms are acceptable; the tag requirement below determines how to structure.

## Outline bullet requirement

`.writing/outline.md` §Conclusion MUST contain **exactly 3 bullets**, one per element, in the strict order R → S → F. Each bullet MUST be prefixed with its element label:

```
## Conclusion

- [R] <one-sentence restatement of the contribution>
- [S] <one-sentence headline result>
- [F] <one-sentence forward-look>
```

Rules:

- Exactly 3 bullets. Not 2, not 4.
- Strict R → S → F order.
- If the paper uses merged "§Discussion and Conclusion" form, omit `[F]` and shrink to 2 bullets `[R]` + `[S]` (RS only). §Discussion's `[F]` Future work carries the forward-look.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_conclusion.md` using `conc-c1`, `conc-c2`, `conc-c3`. These claims typically reference §Results findings and §Introduction contribution statements — the EVIDENCE for `[R]` and `[S]` is usually of `type: citation` pointing at prior sections via claim cross-reference, or `type: analysis` for the key number in `[S]`.

## Draft requirement

The matching `.writing/manuscript/<NN>_conclusion.tex` is structured either as **three one-sentence paragraphs** (preferred) or **one three-sentence paragraph with three structural tags stacked**. Both forms satisfy the tag requirement; pick based on what reads better for the paper.

### Form 1: Three-paragraph Conclusion (preferred)

```latex
\section{Conclusion}
\label{sec:conclusion}

% conclusion: R
% claim: conc-c1
<one-sentence paragraph: restatement of the paper's contribution.>

% conclusion: S
% claim: conc-c2
<one-sentence paragraph: headline result, optionally with one top-line
number.>

% conclusion: F
% claim: conc-c3
<one-sentence paragraph: forward-looking statement about enabled work or
broader horizon.>
```

### Form 2: Single-paragraph Conclusion

```latex
\section{Conclusion}
\label{sec:conclusion}

% conclusion: R
% conclusion: S
% conclusion: F
% claim: conc-c1
<one paragraph containing three sentences: Restate. Summary. Forward-look.>
```

In Form 2, all three `% conclusion: X` tags are stacked above a single `% claim: id`. The PreToolUse hook will accept this --- one claim tag is sufficient for the paragraph, and the three structural tags document the internal sentence roles for self-review.

Rules:

- Put structural tags immediately above the claim tag (Form 1) or stacked above a single claim tag (Form 2).
- **Total length: 100–250 words.** A Conclusion under 100 words is usually under-developed; over 250 means Discussion material has leaked in. Target ~150 words.
- **No references to figures or tables.** Figures/tables belong in §Methods / §Results / §Discussion. If a number is critical enough to appear in Conclusion, name it inline without a figure reference.
- **No new citations** ideally; one citation is acceptable only if it anchors the forward-look to a named external program or standard (rare).

## Style rules

- **Tense:** mostly present tense. R: simple past for what the paper did ("We proposed X") or simple present for what X is ("X is a framework for…"). S: simple past for reported results ("X achieved 85% accuracy on ImageNet") or simple present for generalizable findings ("X matches baseline performance at lower computational cost"). F: simple present for horizon statements ("This opens…"); simple future only for the Future work direction ("Future extensions will enable…").
- **Voice:** active voice. First-person plural ("we proposed", "we envision") is standard.
- **Tone:** confident but bounded. The Conclusion is the paper's parting word — it may speak with quiet conviction about what was demonstrated. Avoid both under-selling ("this paper makes modest progress toward …") and over-selling ("this work revolutionizes …").
- **Paraphrase the Abstract.** Compare §Conclusion sentences against the Abstract's M and R paragraphs; reword to avoid verbatim overlap. Reviewers who read Abstract and Conclusion back-to-back notice copy-paste.
- **No hedging stack-ups.** "It could potentially be argued that our approach may sometimes…" is not a Conclusion sentence; it is noise. If a claim belongs in Conclusion, state it directly.
- **Forward-look specificity.** The `[F]` sentence should gesture at something concrete — an application, a new problem the work enables, a next-step research direction — not a generic "more research is needed" sign-off. Generic sign-offs are the Conclusion's most common failure mode.
- **No acknowledgments, data availability, or author contributions here.** Those belong in their own sections (often at the very end of the paper, outside the IMRAD block).

## Common failure modes

- **Conclusion exceeds 250 words.** The section has absorbed §Discussion content. Symptom: RSF structure is no longer visible; reader cannot tell what the top-line message is. Fix: trim to 3 sentences (or a 4-sentence paragraph). Move any expanded content back into §Discussion.
- **Verbatim Abstract copy.** The Conclusion paragraph is word-for-word the Abstract's M / R section. Symptom: reviewers notice instantly. Fix: paraphrase with different sentence structure and a slight shift in emphasis (Abstract emphasizes "what we measured"; Conclusion emphasizes "what it means going forward").
- **New content introduced.** Conclusion cites a paper not previously cited, or reports a number not in §Results. Symptom: reviewer flags inconsistency. Fix: promote new content to an earlier section, or delete from Conclusion.
- **Generic forward-look.** `[F]` sentence is "We hope this inspires future work" or "More research is needed". Symptom: reader closes the paper unsure what just ended. Fix: name something specific — an application domain, a follow-up question, a broader research program.
- **Missing `[F]` in standalone Conclusion.** The Conclusion ends after `[S]` with no closing gesture. Symptom: the paper trails off. Fix: add a one-sentence `[F]` unless the paper uses merged "§Discussion and Conclusion" form (in which case §Discussion `[F]` carries the forward-look and this file's `[F]` is intentionally dropped).
- **Overclaiming significance.** `[S]` or `[F]` makes claims beyond what §Results supports ("X is the definitive solution to …"). Symptom: reviewers flag as overclaim; fairness scores drop. Fix: bound claims by §Results; use "achieves", "matches", "reduces" — not "solves", "revolutionizes", "dominates".
- **Stacked hedges.** "This work may potentially enable some applications in future …". Symptom: the Conclusion reads as uncertain about its own contribution. Fix: pick one hedge verb and commit ("This enables X" / "This may enable X" — not both).

### Purpose and placement

The Conclusion provides a concise summary of key findings and their significance. It may be a separate section or the final paragraph of §Discussion; check venue requirements. At most 1--2 paragraphs. Do NOT introduce new information, new citations, or new arguments here --- if a claim is important enough to state in §Conclusion, it must have appeared earlier.

What NOT to introduce in §Conclusion:

- New citations not present in the body.
- New numbers not reported in §Results.
- New arguments or technical claims not made in §Methods or §Discussion.
- Acknowledgments, data-availability statements, or author contributions (those belong in their own sections).

Example:

> This work introduces Sparse-fold Attention, a memory-efficient inference mechanism for large language models. Sparse-fold reduces GPU memory consumption by 60% during inference while maintaining within-1% accuracy on standard benchmarks. These results suggest that structured sparsity is a viable path toward deploying transformer models on resource-constrained hardware, opening the door to efficient on-device inference.

Note how the example restates the contribution (R), names the headline result with a number (S), and closes with a forward-look that gestures at a concrete enabled application (F) --- without introducing anything not already established in the body.

### Conclusion vs. Abstract

The Conclusion and the Abstract cover overlapping ground but serve different readers. The Abstract is the recruiter: a reader scanning search results decides whether to read the paper based on the Abstract alone. The Conclusion is the closer: a reader who has finished the body wants a crisp summary to carry away. Write the Abstract to hook; write the Conclusion to consolidate. Never copy text between them --- paraphrase with different emphasis and structure.

### When to omit the Conclusion

Short workshop papers (4 pages), extended abstracts, and some venue formats (NeurIPS/ICML merged Discussion-and-Conclusion) may omit a standalone §Conclusion. In those cases, let §Discussion's `[S]` Significance paragraph serve as the closing statement. Do not force a standalone §Conclusion if the page budget makes it feel redundant.
