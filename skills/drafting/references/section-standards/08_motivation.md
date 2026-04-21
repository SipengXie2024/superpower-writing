---
section: motivation
stem: 08_motivation
framework: SFR
opt_in: true
---

# Motivation — SFR Standard (OPT-IN)

> **OPT-IN STANDARD.** Unlike Abstract / Introduction / Background / Related Work, which are universal across academic writing, a dedicated §Motivation section is a **subfield convention**, not a general "八股". Do NOT create a `.writing/manuscript/NN_motivation.tex` file unless the paper explicitly benefits from it. When unsure, omit §Motivation and let Introduction's CARS M2 carry the niche-establishment burden.

**When to opt in.** §Motivation earns its page count only when Introduction's M2 cannot fit the full problem case — typically because demonstrating baseline failure requires a concrete use case walkthrough, quantitative measurement, or an illustrative figure that would overflow Introduction. Venues and subfields where §Motivation is an expected convention:

- **Systems / OS / networking**: SOSP, OSDI, NSDI, ATC, EuroSys — motivating examples driven by real workloads or traces.
- **Architecture / hardware**: ISCA, MICRO, HPCA, ASPLOS — motivating examples driven by microbenchmark numbers on existing hardware.
- **Security**: USENIX Security, CCS, NDSS — motivating examples driven by attack scenarios or concrete vulnerabilities.
- **Database systems**: VLDB, SIGMOD (occasional) — motivating examples driven by query workload or data-scale pathologies.

**When to skip.** ML / NLP / CV / theoretical CS papers almost never use §Motivation — Introduction M2 suffices. Clinical, biology, and IMRAD-strict papers never use §Motivation. If your target venue is not in the opt-in list above and your advisor / co-authors have not asked for one, omit it.

**Stem is not fixed.** When opted in, §Motivation typically occupies the §2 slot (before §Background, which then shifts to §3). This file governs `.writing/manuscript/NN_motivation.tex` regardless of its numeric prefix; match resolves via slug-ending fallback.

**Interaction with Introduction and Background.** §Motivation overlaps topically with both. Compress Introduction's CARS M2 (`[N]` bullets) to one high-level gap sentence when §Motivation is present — the detailed problem statement now lives in §Motivation, not Introduction. Similarly, keep §Background's L element brief when §Motivation already demonstrated the failure; §Background's L can reference §Motivation's findings rather than re-proving them ("as shown in §Motivation, baseline X incurs O(n²) memory overhead...").

## Framework

**SFR = Scenario, Failure, Requirements.** Three paragraphs (plus an optional requirements list) that together build an irrefutable case for why the paper's contribution is needed. The skeleton answers three questions in sequence: *what concrete situation are we talking about → how do existing solutions fail in this situation → what properties must a correct solution have*.

The power of SFR comes from specificity. A §Motivation that succeeds shows the reader a precise scenario, measures the baseline's failure on that scenario with numbers, and abstracts the measurement into a short list of requirements. §Methods then reads as the inevitable answer to those requirements — the contribution is pre-justified by the time the reader gets there.

## Role of each element

| Element                       | Purpose                                                                                                            | Answers                                                           |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| **S — Scenario**              | Walk the reader through one concrete use case in enough detail that the numbers in F are legible.                 | *What situation are we actually talking about?*                   |
| **F — Failure (quantified)**  | Measure or demonstrate how existing solutions fail on the scenario. Numbers preferred over prose.                 | *What exactly breaks, and by how much?*                           |
| **R — Requirements**          | Abstract the observed failure into 3–5 concrete requirements a correct solution must satisfy.                     | *What does a winning solution need, stated independently of our proposal?* |

The R element is typically rendered as a bulleted list (like the contributions list in Introduction's CS/engineering variant), not a prose paragraph. This is conventional in systems/architecture venues and improves referability — §Methods can explicitly map each subsection back to a requirement number from R.

## Outline bullet requirement

`.writing/outline.md` §Motivation MUST contain **3–6 bullets total**, with at least one bullet per element, appearing in the strict order S → F → R. Each bullet MUST be prefixed with its element label in square brackets:

- `[S]` — Scenario
- `[F]` — Failure (quantified)
- `[R]` — Requirement (one bullet per requirement; typically 3–5 total)

```
## Motivation

- [S] <one-sentence description of the concrete use case>
- [F] <one-sentence summary of how baseline fails in that case, ideally with a headline number>
- [R] <requirement 1: one-sentence actionable property the solution must satisfy>
- [R] <requirement 2: ...>
- [R] <requirement 3: ...>
```

Rules:

- Exactly 1 `[S]` bullet (one scenario per Motivation; more than one fragments the narrative).
- 1–2 `[F]` bullets (a second F bullet is used when the failure has two distinct quantitative dimensions, e.g., latency AND memory).
- 2–5 `[R]` bullets, one per requirement. Fewer than 2 means the requirements are too vague; more than 5 means they are over-fragmented.
- Strict order S → F → R. Do not mix a second scenario in after F; if a second scenario is needed, the paper likely needs a different framing.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_motivation.md` using `mot-c1`, `mot-c2`, … The F bullets MUST carry citation or measurement evidence at claim time (numbers without sources are not evidence-ready).

## Draft requirement

The matching `.writing/manuscript/<NN>_motivation.tex` MUST be structured as **3 paragraphs plus an optional requirements list** matching the outline's element ordering. Each paragraph MUST be preceded by a LaTeX line comment marking its element, and §Motivation stem does not end in an unprotected slug, so every paragraph also needs a `% claim: id` (or `% draft-only`) tag:

```latex
\section{Motivation}
\label{sec:motivation}

% motivation: S
% claim: mot-c1
<paragraph 1: Scenario --- 3--6 sentences setting up one concrete use case.
May include a figure (\includegraphics) or pseudocode block (algorithm
environment).>

% motivation: F
% claim: mot-c2
<paragraph 2: Failure --- 3--6 sentences with at least one quantitative
measurement or comparison. Table (\begin{table}) or figure
(\begin{figure}) often replaces part of the prose.>

% motivation: R
% claim: mot-c3
The scenario above imposes the following requirements on any correct
solution:
\begin{itemize}
  \item \textbf{R1 --- <noun phrase>:} <one-sentence actionable requirement>.
  \item \textbf{R2 --- <noun phrase>:} <one-sentence actionable requirement>.
  \item \textbf{R3 --- <noun phrase>:} <one-sentence actionable requirement>.
\end{itemize}
```

Rules:

- Put `% motivation: X` on the line immediately above `% claim: id`. Both tags are required for each of S, F, R paragraphs.
- The **R element is typically a single paragraph containing an itemize list**, not multiple paragraphs. One `% motivation: R` / `% claim: mot-c3` pair covers the whole R list. If requirements are genuinely heterogeneous (some algorithmic, some deployment), a second `% motivation: R` paragraph is acceptable.
- **The R list MUST use the `R1 / R2 / R3` numbering**. §Methods and §Evaluation will reference requirements by number ("§4.2 satisfies R2 by..."); dropping the numbering breaks referability.
- **The F paragraph MUST be quantitative.** A Motivation whose F element has no numbers reads as hand-waving. Use a table, inline number, or figure — any of these works, but there must be something measurable.
- Length budget: ~400–900 words total. S ≈ 30–40%, F ≈ 30–40%, R ≈ 25–35%. If S expands beyond 400 words it has bloated into Background; move domain generalization out.
- Figures and tables: a figure illustrating the scenario (pseudocode, system diagram) or a table showing baseline failure numbers is strongly encouraged. Reviewers in systems / architecture venues actively expect one of these.

## Style rules

- **Tense:**
  - S: simple present for the scenario's structure ("Consider a microservice topology with 12 services..."); simple past for any empirical measurement that seeded the scenario ("We observed this pattern in 34 of 50 production traces we analyzed").
  - F: simple past for measured results ("The baseline required 4.7 GB of memory"); simple present for structural failures ("The baseline algorithm does not converge when n > 1024").
  - R: simple present, imperative-adjacent ("The solution must process requests in O(1) time per event").
- **Voice:** active voice throughout. First-person plural ("we observe", "we find") is conventional in systems / architecture.
- **Citations:** F MUST carry citations or measurement provenance. Prior benchmarks, baselines, or your own preliminary measurements are all acceptable; unsourced numbers are not. S and R typically carry few or no citations.
- **No forward references by section number.** Refer to the solution by content ("our approach addresses this by...") not by "§4".
- **Figures / tables:** exactly one is normal; two is the upper bound (one in S for the scenario, one in F for measurements). More than two fragments the narrative.

## Common failure modes

- **F without numbers.** Motivation ends with "baselines struggle with this case" and no measurement. Symptom: reviewer writes "the motivation lacks quantitative evidence." Fix: add at least one number — latency, memory, error rate, whatever is operative — even if a rough microbenchmark.
- **S is too abstract.** Scenario reads as "imagine a large-scale distributed system..." without any specific workload, tenant count, data rate, or topology. Symptom: F's numbers feel unmotivated because the reader cannot picture the situation. Fix: anchor S in a single named workload / trace / benchmark.
- **R is missing or aspirational.** Requirements like "The solution should be efficient" or "Easy to deploy" are not actionable. Symptom: §Methods cannot map its design back to R. Fix: rewrite R as falsifiable claims ("Memory footprint ≤ 128 MB per tenant", "Tail latency < 50 ms at p99").
- **Motivation duplicates Introduction.** Scenario and failure numbers already appeared in §1. Symptom: reviewer asks "why is this section not folded into Introduction?" Fix: either remove §Motivation or compress Introduction's M2 to one sentence referencing §Motivation.
- **More than one scenario.** Two or three scenarios listed in parallel, each with its own F. Symptom: narrative fragments, R becomes an intersection of competing requirements. Fix: pick the strongest scenario and demote the others to §Evaluation.
- **R count mismatch with §Methods.** R lists 4 requirements; §Methods only addresses 2. Symptom: reviewer flags "the proposed approach does not satisfy R3 and R4." Fix: audit every R bullet against the final §Methods — drop requirements the paper cannot defend, or add methods to address them.
