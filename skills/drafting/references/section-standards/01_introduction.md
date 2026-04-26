---
section: introduction
stem: 01_introduction
framework: CARS
---

# Introduction — CARS Standard

The introduction MUST follow John Swales' **CARS** (Create A Research Space) model — three Moves, in order, that together persuade the reader the paper deserves its page count. CARS has been the textbook default across STEM and social-science venues since 1990; use it even when the introduction reads narratively, because the underlying 3-Move skeleton is what reviewers track whether they realize it or not.

## Framework

**CARS = Create A Research Space.** Three Moves:

1. **M1 — Establishing a Territory.** Show the topic matters and has an active research community.
2. **M2 — Establishing a Niche.** Show an unresolved gap, contradiction, or unanswered question exists inside that territory.
3. **M3 — Occupying the Niche.** Announce how this paper fills the gap and preview its contribution.

An introduction that only has M1 reads like a textbook chapter. One that jumps from M1 to M3 without M2 leaves reviewers asking "why was this study needed?" The Moves are sequenced and non-optional; omitting any one is the single most common structural defect in first-author submissions.

## Role of each element

| Move                                    | Purpose                                                                             | Canonical sub-steps                                                                                                             |
|-----------------------------------------|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| **M1 — Establishing a Territory**       | Prove the topic is worth the reader's time and connect to the research community.   | S1a claiming centrality ("X is a widely studied…"); S1b topic generalization (current state / trends); S1c reviewing prior work |
| **M2 — Establishing a Niche**           | Carve out an unresolved question inside that territory the paper will address.      | S2a counter-claim (contradicting a prior result); S2b indicating a gap; S2c raising a question; S2d continuing a tradition      |
| **M3 — Occupying the Niche**            | Commit to a concrete contribution that fills the niche, preview outcome + structure.| S3a outlining purpose / research question; S3b announcing principal findings; S3c indicating paper structure (optional)         |

In practice, every introduction picks one or two sub-steps per Move — not all of them. What the skeleton enforces is the *Move* sequence (M1 → M2 → M3), not the sub-step list.

## Interaction with §Motivation (when opted in)

When the paper includes a dedicated §Motivation section (see `motivation.md` — typical in systems / architecture / hardware / security venues), Introduction's M2 must be **compressed** to avoid duplicating content that now lives in §Motivation:

- **Outline:** reduce `[N]` bullets to **exactly 1**, stating the gap at the highest level ("No prior system supports X at production scale"). The detailed problem scenario and quantitative failure belong in §Motivation, not here.
- **Draft:** the single `% cars: N` paragraph should be 2–4 sentences that flag the gap and defer to §Motivation ("We elaborate on this gap in §Motivation."). Do not pre-announce the motivating scenario's numbers or requirements in Introduction — §Motivation owns those.
- **M1 and M3 are unchanged** by the presence of §Motivation. Territory and contribution framing stay in Introduction regardless.

When §Motivation is not present (ML / theoretical / clinical / most CS papers), treat the normal CARS rules below as authoritative — M2 may have 1–2 bullets as usual.

## Outline bullet requirement

`.writing/outline.md` §Introduction MUST contain **4–7 bullets total**, with at least one bullet per Move, appearing in the order M1 → M2 → M3. Each bullet MUST be prefixed with its Move label in square brackets:

- `[T]` — a Move-1 (Territory) bullet
- `[N]` — a Move-2 (Niche) bullet
- `[O]` — a Move-3 (Occupy) bullet

```
## Introduction

- [T] <centrality: why this topic matters>
- [T] <prior work: state of the field, relevant foundational results>
- [N] <gap / contradiction / unanswered question>
- [O] <this paper's purpose + approach>
- [O] <this paper's principal contributions>
```

Rules:

- **At least 1 bullet per label**, in the strict order T → N → O (all T bullets before any N bullet; all N bullets before any O bullet).
- **Typical distribution** is 2–3 `[T]` + 1–2 `[N]` + 1–2 `[O]`. Fewer than 4 total bullets almost always means M1 or M3 was under-developed; more than 7 means the introduction has bled into literature review (move it to a dedicated §Related Work or tighten the bullets).
- **No sub-step labels in the outline.** Keep bullets at the Move level; the specific sub-step (centrality vs. prior-work vs. gap-indication) is a drafting-time decision.

Outlining self-review (Step 7 of `superpower-writing:outlining`) MUST grep the Introduction block and confirm: (a) `^- \[T\]` appears at least once before any `^- \[N\]` line; (b) `^- \[N\]` appears at least once before any `^- \[O\]` line; (c) at least one `^- \[O\]` line exists; (d) total bullet count is between 4 and 7 inclusive.

Each labeled bullet still seeds a claim stub in `.writing/claims/section_01_introduction.md` using the existing `intro-c1`, `intro-c2`, … convention from `outlining` Step 4 — CARS does not override claim-ID numbering.

## Draft requirement

`.writing/manuscript/01_introduction.tex` MUST be structured as **4–7 paragraphs** matching the outline's Move ordering. Each paragraph MUST be preceded by a LaTeX line comment marking its Move:

```latex
\section{Introduction}
\label{sec:introduction}

% cars: T
% claim: intro-c1
<paragraph 1: Territory --- centrality / topic generalization. Citations via
\cite{smith2019,chen2020}.>

% cars: T
% claim: intro-c2
<paragraph 2: Territory --- prior work review.>

% cars: N
% claim: intro-c3
<paragraph 3: Niche --- gap / unresolved question.>

% cars: O
% claim: intro-c4
<paragraph 4: Occupy --- purpose + approach.>

% cars: O
% claim: intro-c5
<paragraph 5: Occupy --- contributions / principal findings.>
```

Rules:

- Both tags coexist: `% cars: X` for structural self-review, `% claim: id` for the PreToolUse hook (Introduction stem does NOT end in an unprotected slug — every paragraph still needs a claim tag or `% draft-only`). Put `% cars: X` on the line immediately above `% claim: id`.
- Moves appear in order T → N → O. All T-tagged paragraphs come first, then all N-tagged, then all O-tagged. No interleaving.
- **T → N transition rule.** The first sentence of the first `N` paragraph MUST name, as concrete nouns, both T-side subjects whose mismatch the paragraph will pose as the gap. Do NOT open with a demonstrative anaphor ("This gap...", "This problem...", "This limitation...") --- readers scanning linearly have not yet identified which T-strand is meant, and scanning back costs them a mental re-parse of §1. Wrong: ``This gap has not been posed before.'' Right: ``The mismatch between <T1 concrete noun> and <T2 concrete noun> has not been posed as a <framing> problem before.'' Subsequent `N` paragraphs may use shorter anaphora once both T-sides have been named explicitly in the first `N` paragraph.
- Length budget: ~400–800 words total for most venues (M1 ≈ 30–40%, M2 ≈ 15–25%, M3 ≈ 35–45%). Venues with strict word limits (Nature, Science) may push toward 300 words and 3 paragraphs (still one per Move, M1 and M3 compressed). Venues with no limits (long-form CS / social science) may push toward 1,500 words and 7 paragraphs. Do not exceed 7 paragraphs — if more material is needed, it belongs in §Related Work.

### CS / engineering variant --- explicit contributions list

For CS, ML, systems, and engineering venues (typically indicated by `metadata.yaml` `reporting_guideline: none` combined with a venue such as an ACM/IEEE/ICML/NeurIPS conference), the final `% cars: O` paragraph MAY be replaced with --- or followed by --- an itemize list of contributions. The list form is customary in these venues and reviewers actively look for it.

```latex
% cars: O
% claim: intro-c5
Our contributions are as follows:
\begin{itemize}
  \item \textbf{<Contribution 1 noun phrase>:} <one-sentence description that
        stands up to the strongest reviewer>. (\S\ref{sec:foo})
  \item \textbf{<Contribution 2 noun phrase>:} <one-sentence description>.
        (\S\ref{sec:bar})
  \item \textbf{<Contribution 3 noun phrase>:} <one-sentence description>.
        (\S\ref{sec:baz})
\end{itemize}
```

Rules for the contributions list:

- **3–5 items.** Fewer than 3 looks like an under-scoped paper; more than 5 looks like over-claiming. If you genuinely have more, merge the weakest into a parent contribution.
- **Noun-phrase heading per bullet**, not a full sentence. "Novel caching policy" beats "We introduce a novel caching policy that…"
- **Each bullet carries forward to the paper's body.** The `\S\ref{...}` pointer is required --- if the contribution does not survive the rest of the paper, it does not belong in this list.
- **No distinct claim id per bullet required.** The whole list can sit under one claim id (e.g., `intro-c5`) because the real evidence for each contribution lives in its Results section. But the bullet-level factual statements still must be true --- do not pad the list with aspirational claims.

An optional trailing `% cars: O` paragraph may be added to describe paper organization ("Section~\ref{sec:related} reviews related work; Section~\ref{sec:methods} presents..."). This is stylistic and not required.

## Style rules

- **Tense:**
  - M1 centrality / generalization: present tense for established knowledge and general truths ("Transformer models dominate NLP benchmarks").
  - M1 prior work: simple past for specific prior studies and their findings ("Smith et al. measured…") or present perfect for cumulative findings ("Multiple studies have shown…").
  - M2 gap-indication: present perfect for unresolved state ("No prior work has addressed…"); simple present for contradictions ("These results conflict").
  - M3 purpose + findings: simple past for what was done in this study ("We conducted a cohort study of 1,247 patients"), simple present for generalizable claims ("The approach generalizes to any…").
- **Voice:** active voice wherever possible, matching the conventions in `writing-principles.md`. First-person plural ("we") is standard for empirical sciences; some humanities-adjacent venues prefer passive or impersonal.
- **Citations are expected** — unlike the abstract, the introduction is citation-dense, especially M1 and M2. Every factual claim about the field and every statement about prior work needs a citation. Use `\cite{citekey}` (standard LaTeX); group multiple cites in one site as `\cite{a,b,c}`.
- **No results numbers that do not appear in Results.** Reviewers check; pre-announcing a number that does not reappear in Results erodes trust.
- **Three-layer numeric discipline (Introduction layer).** §Introduction refers to results by direction, not magnitude --- "an order-of-magnitude reduction", "a substantial speed-up", "near-linear scaling", "eliminating the dominant bottleneck". Specific percents and absolute counts live in §Abstract (percent-only) and §Results (full breakdown); repeating them here triples the reviewer's consistency-check surface and multiplies the drift risk under revision.
- **First-use term discipline.** The first time the paper names a load-bearing technical term, introduce it with `\emph{term}` and, in the same sentence or the next, a one-clause operational gloss that tells the reader what the term means well enough to read the next paragraph. Do NOT name a term and defer its definition to a later section. Pattern: ``\emph{X} --- <one-line operational gloss>.'' The formal definition may still live in §Background §N or §Methods §F; the gloss pays down the cognitive debt until the reader gets there, so the rest of §Introduction reads without a forward-reference hole.
- **Figure / table references allowed**, but only to teasers that will reappear in the body. If you reference Figure 1 in the introduction, Figure 1 had better be the paper's conceptual / pipeline figure.
- **Paragraph transitions between Moves.** The T-to-N transition is the most important seam in the paper. The first sentence of the first `[N]` paragraph must name both the T-side subjects whose mismatch forms the gap. Do NOT open with a demonstrative anaphor ("This gap...") --- the reader has not yet identified which T-strand is meant.
- **Opening-hook discipline.** Do not start with a vacuous generality ("Since the dawn of computing...") or a textbook definition ("A database is a structured collection of data..."). Open with a specific, concrete claim that signals the paper's stakes.
- **Length discipline.** Target 400--800 words for most venues. Introductions over 1,000 words have usually leaked into literature-review territory; move that material to §Related Work.
- **Citation density.** M1 and M2 are citation-dense (every factual claim needs a reference); M3 is citation-sparse (your own contribution needs no citation). If M3 has more citations than M2, the contribution is under-developed relative to the literature review.
- **Contribution-count norm.** For CS/ML venues, 3--5 contributions is the sweet spot. Fewer than 3 suggests under-scoping; more than 5 suggests over-claiming or fragmentation. Merge weak contributions into stronger parent claims.

## Common failure modes

- **Missing M2 (no niche).** Introduction jumps from prior work straight to "In this paper we…". Reviewers flag "motivation unclear" or "contribution not positioned against prior work". Fix: always write at least one `[N]` paragraph, even if the gap feels obvious to you.
- **M1 as a literature dump.** Five paragraphs reviewing every tangentially related paper, with no narrative thread. M1 should be argumentative, not exhaustive. Move encyclopedic coverage to §Related Work. If `[T]` bullets exceed 3, tighten.
- **Gap-contribution mismatch.** M2 frames gap A ("no benchmark for real-time inference under 10 ms"); M3 announces contribution B ("we propose a new attention variant"). Readers walk away confused. Audit: does each M3 contribution answer exactly one M2 gap? If not, rewrite one of them.
- **Contributions list over-promises.** "A novel, state-of-the-art, theoretically-grounded framework that…" — strip the superlatives. Each bullet should survive the question "can I point to the exact subsection that proves this?"
- **Buried thesis.** The paper's central claim does not appear until paragraph 5. M3 should open with purpose ("This paper investigates…" or "We propose…"); do not make the reader hunt.
- **Related-work creep.** M1 + M2 grow to 60%+ of the introduction, squeezing M3 into one rushed paragraph. Rebalance — move related-work detail to §Related Work and use the freed space for M3.
- **Abstract echo in §Introduction first paragraph.** The first paragraph of §Introduction repeats Abstract-B's opening sentence structure and enumerates the same related systems with the same connectors. Symptom: a reader who has already read the abstract gets no new signal from the first 100 words of the body, and reviewers score the paper "context-light". Fix: assume the reader has already absorbed the abstract. §Introduction T1 starts one level deeper — technical stakes, mechanism detail, or methodology exposition — and treats the abstract's context as given, not restated. Opening the first T paragraph with a verbatim or near-verbatim copy of Abstract-B's first sentence is a hard fail; rewrite from a different angle (e.g., abstract frames "what", introduction frames "how" or "why-now").

### Key questions to answer

Every introduction must let the reader answer these six questions after a single read-through. If any answer is missing, the CARS skeleton is incomplete:

1. **What is the problem?** Name the concrete task or challenge in one sentence.
2. **Why does it matter?** State the practical or theoretical consequence of leaving the problem unsolved.
3. **What has been tried?** Summarize the dominant existing approach(es) and cite the canonical references.
4. **What is the gap?** Identify the specific limitation, contradiction, or open question that prior work leaves unaddressed.
5. **What do we contribute?** List the paper's contributions in a form the reader can verify against the body (preferably a numbered list for CS venues).
6. **How is this paper organized?** Briefly map the remaining sections so the reader can navigate.

Questions 1--3 map to M1 (Territory), question 4 maps to M2 (Niche), and questions 5--6 map to M3 (Occupy).
