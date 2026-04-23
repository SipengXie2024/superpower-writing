---
section: abstract
stem: 00_abstract
framework: BPMRC
---

# Abstract — BPMRC Standard

The abstract MUST follow the **BPMRC** structure: Background → Problem → Method → Result → Conclusion. This is the structured-abstract skeleton adopted by JAMA, BMJ, NEJM, Lancet, and most IMRAD venues. Use it even for narrative (unstructured) abstracts — the labels disappear but the five elements remain, in this order.

## Framework

**BPMRC = Background, Problem, Method, Result, Conclusion.** The skeleton forces a reviewer to answer, in sequence: *why does this field matter → what is missing → what did you do → what did you find → so what?* Reviewers who cannot answer any one of those questions after reading the abstract will reject the paper at the triage desk, regardless of what the body delivers. Enforcing the skeleton at outline and draft time eliminates the single most common structural defect in submitted abstracts.

## Role of each element

| Element            | Sentences | Purpose                                                                                           |
|--------------------|-----------|---------------------------------------------------------------------------------------------------|
| **B — Background** | 1–2       | Establish context, topical importance, and current state of knowledge. Answers: *why does this field matter?* |
| **P — Problem**    | 1         | State the specific gap, unresolved question, or controversy this paper addresses. Answers: *what is missing?* |
| **M — Method**     | 1–2       | Design, population/dataset, intervention or analytical approach, primary outcome measure. Answers: *what did you do?* |
| **R — Result**     | 1–2       | Quantitative headline findings with effect sizes, confidence intervals, or p-values where applicable. Answers: *what did you find?* |
| **C — Conclusion** | 1         | Interpretation plus one-sentence implication or forward-look. Answers: *so what?*                 |

## Outline bullet requirement

`.writing/outline.md` §Abstract MUST contain **exactly 5 bullets**, in the order B → P → M → R → C. Each bullet MUST be prefixed with its element label in square brackets:

```
## Abstract

- [B] <one-sentence background claim>
- [P] <one-sentence problem statement>
- [M] <one-sentence method claim>
- [R] <one-sentence headline result>
- [C] <one-sentence conclusion / implication>
```

Outlining self-review (Step 7 of `superpower-writing:outlining`) MUST grep `^- \[B\]`, `^- \[P\]`, `^- \[M\]`, `^- \[R\]`, `^- \[C\]` against the Abstract block and fail if any label is missing, duplicated, or out of order. The earlier "3–7 bullets" heuristic from the generic outlining table does NOT apply to Abstract — BPMRC fixes the count at 5.

Each labeled bullet still seeds a claim stub in `.writing/claims/section_00_abstract.md` with `id`s `abs-b1`, `abs-p1`, `abs-m1`, `abs-r1`, `abs-c1` (or `abs-b1`..`abs-b2` if Background uses two sentences). The claim-first protocol still applies downstream; BPMRC only constrains structure.

## Draft requirement

`.writing/manuscript/00_abstract.tex` MUST be structured as **exactly 5 paragraphs**, one per BPMRC element, in order. Each paragraph MUST be preceded by a LaTeX line comment marking its role (`%` at column 0):

```latex
\begin{abstract}
% bpmrc: B
<paragraph 1: background --- 1--2 sentences>

% bpmrc: P
<paragraph 2: problem --- 1 sentence>

% bpmrc: M
<paragraph 3: method --- 1--2 sentences>

% bpmrc: R
<paragraph 4: result --- 1--2 sentences>

% bpmrc: C
<paragraph 5: conclusion --- 1 sentence>
\end{abstract}
```

**Hook interaction.** The stem `00_abstract` matches the `_abstract` slug in `UNPROTECTED_SLUGS` inside `hooks/enforce-claims.py`, so the PreToolUse hook does NOT require `% claim: id` tags here. But the `% bpmrc: X` tags ARE required. The `section-drafter` Step C self-review runs `grep -cE '^\s*% bpmrc: [BPMRC]' .writing/manuscript/00_abstract.tex` against the draft and fails the section if the count is not exactly 5 or if any of B/P/M/R/C is missing.

**Paragraph merging is forbidden.** A common anti-pattern is collapsing Background + Problem into one paragraph, or Method + Result into one. Do not do this. Each element owns its own paragraph even when its contribution is one sentence. Reviewers parse abstracts structurally; merged paragraphs force them to re-segment the text and increase triage-reject risk.

## Length budget

Target ~250 words total, or whatever the venue's abstract word limit dictates. If `.writing/metadata.yaml` has a `venue.abstract_word_limit` field, honor it over the 250-word default. Rough distribution:

| Element    | Share of word budget |
|------------|----------------------|
| Background | 15–20%               |
| Problem    | 10%                  |
| Method     | 25–30%               |
| Result     | 30–35%               |
| Conclusion | 10–15%               |

A well-balanced abstract gives Method and Result the most real estate; Background and Conclusion are cheap sentences that frame, not carry, the content.

## Style rules

- **Tense:** past tense for Method and Result ("We enrolled 1,247 patients"; "Accuracy increased by 12.3%"); present tense for Background and Conclusion ("T2D remains the leading cause of adult blindness"; "These findings suggest..."); present-perfect tense for Problem when framing an unresolved state ("No prior study has measured...").
- **Voice:** active voice wherever possible ("We measured X" over "X was measured"), matching upstream `scientific-writing` conventions.
- **No citations** in the abstract unless the venue explicitly allows them (rare — check venue instructions before including any).
- **No undefined abbreviations** on first occurrence. The abstract is standalone; readers cannot be expected to have read the glossary.
- **No figure/table/equation references** ("Figure 2 shows..." belongs in the body).
- **Declare study registration** (trial ID, PROSPERO ID, OSF preregistration ID) at the end of the Method paragraph if `metadata.yaml` `preregistration.registry` is non-null.
- **Three-layer numeric discipline (Abstract layer).** The Abstract is the headline layer. Report effect size as **percent change or relative ratio only**; do NOT carry absolute counts alongside percent changes (e.g., write "-41.5%", not "19,130 to 11,189 (-41.5%)"). Uncertainty (CI, p-value, SD) MAY accompany the headline percent if it fits in one clause; otherwise defer to §Results. The full absolute breakdown belongs in §Results. §Introduction is the direction-only layer (write "an order-of-magnitude reduction", not a specific percent). This three-layer split prevents reviewers from cross-checking three copies of the same number and finding drift between them.
- **Numbers MUST carry units, comparators, and uncertainty where one clause permits.** "Accuracy improved by 10" is not a verifiable result; "Accuracy improved by +10.3 pp (95% CI 8.1–12.5, p < 0.001)" is. Consistent with the three-layer rule above, prefer percent-change or relative-ratio forms in the abstract; push absolute baseline-to-new pairs down to §Results.

## Common failure modes

- **Missing problem statement.** Background flows directly into Method; reviewers flag "unclear motivation" or "the contribution is not justified". Fix: always write the P paragraph, even if it feels redundant with B.
- **Result buried in interpretation.** "We demonstrate that X is effective" is Conclusion phrasing, not Result phrasing. Results must be quantitative and descriptive; Conclusion is where you may interpret.
- **Conclusion overreaches.** Claiming implications that exceed what the Result supports (e.g., "This will transform clinical practice" when the study had N=30 in one center). Keep Conclusion bounded by the evidence in Result.
- **Numbers without units or CIs.** Triggers reviewer suspicion even when the paper's body has the full numbers. Carry the full quantitative claim into the abstract.
- **Method buried inside Background.** A sentence like "To address this, we conducted a randomized trial in 3,000 adults" belongs in M, not B. If Background ends with "we did X", split it.
- **Five elements smashed into one paragraph.** Produces an unstructured blob that defeats the whole skeleton. The `% bpmrc: X` tag enforcement exists to catch this.
