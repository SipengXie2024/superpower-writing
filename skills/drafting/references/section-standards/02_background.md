---
section: background
stem: 02_background
framework: DNPL
---

# Background / Preliminaries — DNPL Standard

The §Background (sometimes titled §Preliminaries or §Technical Background) section prepares the reader for §Methods by establishing the technical vocabulary and baseline approach this paper will assume and then extend. It MUST follow the **DNPL** four-part structure: Domain recap → Notation/Definitions → Prior approach → Limitation of prior. This skeleton is the convention across CS, ML, systems, database, graphics, and theoretical-CS papers.

**Stem is not fixed.** This file governs any `.writing/manuscript/NN_background.tex` regardless of its numeric prefix: `02_background.tex` when Background is §2 directly after Introduction, or `03_background.tex` when a §Motivation section takes the §2 slot. Match resolves via slug-ending fallback (see `README.md`).

## Framework

**DNPL = Domain recap, Notation/definitions, Prior approach, Limitation of prior.** Four paragraphs that together walk the reader from "here is the problem space" to "here is precisely what fails about the current state of the art, which is what this paper will fix". The skeleton is pedagogical in intent: a reader who has just read the Introduction should be able to follow §Methods only after absorbing these four elements in this order.

Why this structure dominates: papers that skip D or N force the reader to flip back to Introduction or other papers to reconstruct notation; papers that skip P leave §Methods' contributions hanging in a vacuum; papers that skip L leave the reader confused about why a new method was needed at all. Every DNPL element answers a question the reader will otherwise carry into §Methods and resolve less charitably.

## Role of each element

| Element                          | Purpose                                                                                           | Answers                                                                      |
|----------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **D — Domain recap**             | Restate the problem domain in one paragraph, lifting at most one sentence from Introduction M1.   | *What problem space are we in, and what are its moving parts?*               |
| **N — Notation / Definitions**   | Introduce every symbol, variable, dataset name, and formal term that §Methods and §Results reuse. | *What language will the rest of the paper speak?*                            |
| **P — Prior approach / Baseline**| Describe the dominant existing approach(es) using the notation just defined. Include pseudocode or a compact equation set when relevant. | *What is the current state of the art, described in the same terms as our method?* |
| **L — Limitation of prior**      | Point out the specific, concrete defect in the prior approach(es) that motivates the next section. | *Why is the current state of the art insufficient?*                          |

An optional fifth element — a short **summary paragraph** reiterating L and bridging to §Methods — is permitted but not required. When included, tag it as `% background: L` (same label as Limitation) rather than introducing a new label.

## Outline bullet requirement

`.writing/outline.md` §Background MUST contain **4–6 bullets total**, with at least one bullet per element, appearing in the strict order D → N → P → L. Each bullet MUST be prefixed with its element label in square brackets:

- `[D]` — Domain recap
- `[N]` — Notation / Definitions
- `[P]` — Prior approach
- `[L]` — Limitation of prior

```
## Background

- [D] <one-sentence recap of the problem domain>
- [N] <notation / formalism the paper will reuse>
- [P] <dominant prior approach described in that notation>
- [L] <specific limitation of the prior approach>
```

Rules:

- All `[D]` bullets come before any `[N]`; all `[N]` before any `[P]`; all `[P]` before any `[L]`. No interleaving.
- Bullets can repeat within a label (e.g., two `[P]` bullets if the paper needs to introduce two baselines in parallel) as long as the D→N→P→L group ordering holds.
- Fewer than 4 total bullets almost always means D or N was skipped — reviewers will notice. More than 6 means Background has bloated into a literature review; consider moving material to §Related Work.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_background.md` using the existing `bg-c1`, `bg-c2`, … claim-ID convention from `outlining` Step 4. Background claims are typically citation-dense (D, P, L) and definition-dense (N); expect 3–5 citations in a 4-bullet Background.

## Draft requirement

The matching `.writing/manuscript/<NN>_background.tex` MUST be structured as **4–6 paragraphs** matching the outline's element ordering. Each paragraph MUST be preceded by a LaTeX line comment marking its element. §Background's stem does NOT end in an unprotected slug, so every paragraph also needs a `% claim: id` (or `% draft-only`) tag for the PreToolUse hook:

```latex
\section{Background}
\label{sec:background}

% background: D
% claim: bg-c1
<paragraph 1: Domain recap --- 2--4 sentences.>

% background: N
% claim: bg-c2
<paragraph 2: Notation / Definitions --- 3--6 sentences. Introduce every
symbol the rest of the paper will reuse. Example: Let $f_\theta : \mathcal{X}
\to \mathcal{Y}$ denote a parameterized classifier with parameters $\theta$.>

% background: P
% claim: bg-c3
<paragraph 3: Prior approach --- 4--8 sentences. May include a compact
equation set or a short pseudocode block via Algorithm environment. Example:
\begin{equation}
  \mathrm{Attn}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d}}\right) V
  \label{eq:attention}
\end{equation}>

% background: L
% claim: bg-c4
<paragraph 4: Limitation of prior --- 2--4 sentences, concrete and specific.>
```

Rules:

- Put `% background: X` on the line immediately above `% claim: id`. Both tags are required.
- Elements appear in order D → N → P → L. No interleaving; no out-of-order paragraphs.
- The **N paragraph is special**: it should include every symbol §Methods will reuse. Readers should never have to guess what a variable means when it reappears in §Methods or §Results.
- The **P paragraph** should describe prior approaches using the notation from N, not informally. If a reader finishes P and still cannot articulate what the baseline does in one sentence, P has failed.
- The **L paragraph must be concrete**, not aesthetic. "Prior approaches are not as scalable" is not a limitation; "Prior approaches require $O(n^2)$ memory, exceeding commodity GPU capacity for $n > 32k$" is. L is where §Methods' contribution earns its shape, so precision here pays off downstream.
- Length budget: ~500–1,200 words total. Notation-heavy papers (theoretical CS, cryptography) may push to 2,000 words; applied ML/systems papers typically stay under 1,000.
- Equations: inline via `$...$`, display via `\[ ... \]` or `\begin{equation} ... \end{equation}`. Label only equations referenced later (via `\label{eq:foo}` + `\eqref{eq:foo}`).

## Style rules

- **Tense:**
  - D: simple present ("Image classification models assign a label to an input image").
  - N: simple present for definitions ("Let $f_\theta$ denote a parameterized classifier").
  - P: simple present for how the baseline works ("Softmax attention computes..."); simple past for historical statements ("Vaswani et al. introduced multi-head attention").
  - L: simple present for structural limitations ("This approach scales quadratically in sequence length"); simple past for empirical limitations observed in prior work ("Prior benchmarks reported latencies above 200 ms").
- **Voice:** active voice; avoid "it is well known that…" and "it has been shown that…" — cite specifically or drop the claim.
- **Citations:** dense in D, P, L; usually sparse in N (notation is often conventional, not cited). Cite the canonical source for every baseline mentioned in P; cite the benchmark or measurement source for every limitation in L. Use `\cite{citekey}` (standard LaTeX); group multiple cites as `\cite{a,b,c}`.
- **No forward references by section number.** "As we will see in §4..." couples this section to section numbering that may shift. Refer by content ("our method addresses this by...") not by section number.
- **Notation hygiene:** every symbol introduced in N MUST be used somewhere in §Methods or §Results; conversely, every symbol §Methods uses MUST be defined in N. Dangling or unused notation is a reviewer magnet.

## Common failure modes

- **Domain dump.** Four paragraphs of §D (history of the field) and one rushed paragraph each for N, P, L. Symptom: reviewer asks "why is this section not in Related Work?" Fix: D is one paragraph; expand P and L.
- **Missing L.** Background ends at P, leaving §Methods with no bridge. Symptom: reviewer says "motivation for the method is unclear." Fix: always write at least one L paragraph; be specific about what fails.
- **Notation introduced mid-Method.** Symbols appear in §Methods that were never defined in N. Symptom: readers flip back and forth hunting for definitions. Fix: move every symbol to N, even at the cost of a longer N paragraph.
- **Baseline described informally.** P describes the prior approach in words but not using N's notation, forcing the reader to map English to formulas. Symptom: §Methods' comparison paragraphs read as hand-waving. Fix: rewrite P using equations and defined symbols from N.
- **Limitation not actionable.** L says "prior approaches have limitations" without specifying which. Symptom: reviewers fill in their own limitations and find the Method addresses the wrong one. Fix: make L quantitative or mechanism-specific — readers should be able to predict what §Methods will propose from reading L alone.
- **Background blurs into Related Work.** D + P grow into a full literature review, duplicating §Related Work. Symptom: two sections with the same content. Fix: keep Background narrow (just enough to support §Methods); push broader coverage to §Related Work.
