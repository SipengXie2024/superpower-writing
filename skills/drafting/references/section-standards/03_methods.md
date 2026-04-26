---
section: methods
stem: 03_methods
framework: OFCA
---

# Methods — OFCA Standard (CS)

The §Methods section is the paper's technical core. In CS papers it goes by many names depending on subfield — §Method (singular), §Approach, §Design, §Architecture, §Algorithm, §System, §Technique, or the author-preferred "§3 Our Approach" — but the underlying "八股" is the same. It MUST follow the **OFCA** four-part structure (plus an optional fifth element): Overview → Formalization → Core → Analysis, with optional Implementation details. Section subtitles in the final paper can be chosen freely; the structural skeleton is what matters.

**Slug convention.** Keep the manuscript filename as `NN_methods.tex` regardless of the rendered section title. The orchestrator matches `methods` by slug-ending. If your paper renders "§3 Design" in the final PDF, still author it as `.writing/manuscript/03_methods.tex` with `## Methods` as the outline heading — the rendered title can be changed at typeset time without touching the plugin's bookkeeping. This avoids maintaining parallel standards files for §Design / §Approach / §Algorithm synonyms.

**Scope.** This standard targets CS papers broadly: ML / NLP / CV / systems / databases / graphics / theoretical CS / applied CS. Clinical, biology, and IMRAD-strict medical papers should not use this file — their §Methods follows CONSORT / STROBE / PRISMA checklist conventions instead (handled upstream by `peer-review`).

## Framework

**OFCA = Overview, Formalization, Core, Analysis.** Four elements, sequenced, that together answer the four questions a reviewer asks of any CS §Methods:

1. *What does the whole system / algorithm look like at a glance?* → **Overview (O)** — high-level picture, often anchored by a pipeline/architecture figure.
2. *What precise problem are we solving, in formal terms?* → **Formalization (F)** — problem statement using notation from §Background.
3. *What is the technical contribution, described in enough detail for a competent reader to reimplement?* → **Core (C)** — algorithms, data structures, design rules, training objectives — the meat.
4. *Why should I trust the approach works?* → **Analysis (A)** — correctness argument, complexity bound, invariant, convergence claim, or theoretical guarantee.

The optional fifth element:

5. *What did we actually build, in engineering terms?* → **Implementation (I)** — deployment details that affect reproducibility (language, frameworks, hyperparameters, hardware). Common in systems / ML-applied papers; skipped in pure theory papers.

An OFCA Methods that fails any of O/F/C/A invites predictable reviewer complaints. O failure: "I got lost in the details before I understood the big picture." F failure: "The problem statement is vague; what exactly is the input and output?" C failure: "Implementation details are insufficient for reproduction." A failure: "No correctness / complexity argument given."

## Role of each element

| Element                       | Purpose                                                                                           | Typical content                                                                         |
|-------------------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| **O — Overview**              | Give the reader a one-screen picture of the whole approach before diving into details.           | 1 paragraph + 1 figure (pipeline diagram / architecture schematic). Narrative, no math. |
| **F — Formalization**         | State the problem precisely in the notation established in §Background.                          | Input type, output type, objective function, constraints, any assumptions.              |
| **C — Core**                  | Describe the main technical contribution(s) in reimplementable detail.                            | Algorithms (with pseudocode), data structures, training loss, design invariants, novel components. Typically spans 2–4 subsections.  |
| **A — Analysis**              | Justify why the approach is correct / efficient / sound.                                         | Correctness proof sketch, complexity bound (time / space / sample / communication), invariant argument, convergence claim. |
| *(Optional)* **I — Implementation** | Document engineering details needed for reproduction or to clarify non-obvious deployment choices. | Programming language, libraries, hyperparameter values, hardware specs, dataset preprocessing, training time.   |

Not every paper includes A (applied ML papers often defer analysis to §Experiments or a technical appendix) or I (theory papers omit entirely). F is occasionally folded into O when the problem statement is trivial (e.g., standard supervised classification). But O and C are never optional — a CS paper without either is not a technical paper.

## Outline bullet requirement

`.writing/outline.md` §Methods MUST contain **4–10 bullets total**, satisfying these rules:

- At least 1 `[O]` bullet (Overview) — always required.
- At least 1 `[F]` bullet (Formalization) — required unless §Background contains no formal notation; drop F only with deliberate justification.
- At least 2 `[C]` bullets (Core) — always required; one per major component / subsection of the core contribution.
- At least 1 `[A]` bullet (Analysis) — required unless the paper defers all analysis to §Experiments (acceptable only for purely empirical ML).
- 0–2 `[I]` bullets (Implementation) — optional; include when systems / applied paper needs engineering detail.

Each bullet MUST be prefixed with its element label in square brackets, and all bullets MUST appear in the strict order O → F → C → A → I:

```
## Methods

- [O] <one-sentence overview: what the approach does at 10,000 feet>
- [F] <problem statement in formal notation>
- [C] <core component 1: name + one-line description>
- [C] <core component 2: name + one-line description>
- [C] <core component 3: name + one-line description>
- [A] <one-sentence correctness or complexity claim>
- [I] <implementation highlight: framework / hyperparameters / hardware>
```

Rules:

- All `[O]` bullets before any `[F]`; all `[F]` before any `[C]`; all `[C]` before any `[A]`; all `[A]` before any `[I]`. No interleaving.
- Typical distribution is 1 `[O]` + 1 `[F]` + 2–4 `[C]` + 1 `[A]` + 0–2 `[I]`, totaling 5–9 bullets.
- Fewer than 4 total bullets means the Methods is under-specified — a CS paper with Methods listing only "[O] overview, [C] algorithm" leaves too much to the reader.
- More than 10 total bullets means the Methods has bloated or should be split across subsections / appendices — consolidate.

Each labeled bullet seeds a claim stub in `.writing/claims/section_<NN>_methods.md` using `meth-c1`, `meth-c2`, … (existing convention from `outlining` Step 4). Every `[C]` bullet and every `[A]` bullet is a hard technical claim — EVIDENCE typically resolves to a pseudocode block, equation, theorem, or reference implementation.

## Draft requirement

The matching `.writing/manuscript/<NN>_methods.tex` is typically organized as multiple subsections (\subsection{Overview}, \subsection{Formalization}, \subsection{Core Design}, etc.), each spanning one or more paragraphs. The LaTeX-comment-tag rule applies at the **paragraph** level, not the subsection level: at least one paragraph per element type carries the matching `% methods: X` tag, in addition to the `% claim: id` tag required by the PreToolUse hook (§Methods stem does not end in an unprotected slug).

```latex
\section{Methods}
\label{sec:methods}

\subsection{Overview}
\label{sec:methods:overview}

% methods: O
% claim: meth-c1
<paragraph: one-screen description of the approach. Refer to
Figure~\ref{fig:pipeline} (pipeline diagram).>

\subsection{Problem Formalization}

% methods: F
% claim: meth-c2
<paragraph: formal problem statement using notation from \S\ref{sec:background}.
Input / output types, objective, constraints.>

\subsection{Core Design}

% methods: C
% claim: meth-c3
<paragraph: core component 1. May include pseudocode (Algorithm~\ref{alg:main})
or key equations.>

\begin{algorithm}[t]
  \caption{Main procedure.}
  \label{alg:main}
  \begin{algorithmic}[1]
    \State $x \gets \mathrm{init}()$
    \For{$t = 1$ \textbf{to} $T$}
      \State $x \gets \mathrm{step}(x)$
    \EndFor
    \State \Return $x$
  \end{algorithmic}
\end{algorithm}

% methods: C
% claim: meth-c4
<paragraph: core component 2.>

% methods: C
% claim: meth-c5
<paragraph: core component 3.>

\subsection{Analysis}

% methods: A
% claim: meth-c6
<paragraph: correctness argument or complexity bound. May include a theorem
statement + proof sketch via \begin{theorem} + \begin{proof}.>

\subsection{Implementation}

% methods: I
% claim: meth-c7
<paragraph: hyperparameters, framework, hardware, non-obvious engineering
choices.>
```

Rules:

- Subsection titles (`\subsection{Overview}`) are editorial --- rename freely (`\subsection{System Architecture}` / `\subsection{Algorithm Design}` / `\subsection{Correctness}`). The `% methods: X` tag on paragraphs is what the structural self-review tracks, not the heading text.
- Put `% methods: X` on the line immediately above `% claim: id`. Both tags are required on every load-bearing paragraph.
- The **Overview paragraph SHOULD reference a figure** via `Figure~\ref{fig:pipeline}` (use `~` tie before \ref to prevent line breaks). This is a reviewer expectation for CS papers; Methods without an architecture figure reads as under-illustrated. Use `scientific-schematics` to draw it; `\includegraphics` the resulting PDF.
- **Pseudocode goes in `[C]` paragraphs** via the `algorithm` + `algorithmic` environments (algorithmicx package). Label with `\label{alg:<name>}` and reference as `Algorithm~\ref{alg:<name>}`.
- **Equations go in `[F]`, `[C]`, and `[A]` paragraphs** --- inline via `$...$`, display via `\[ ... \]` or `\begin{equation} ... \end{equation}`. Label only equations referenced later (`\label{eq:foo}` + `\eqref{eq:foo}`).
- **The Analysis paragraph's rigor scales with claim strength.** Empirical claims ("our approach is faster") need §Experiments, not §Methods §A. Theoretical claims ("runs in $O(n \log n)$ time", "converges to a local minimum") need a theorem statement and proof sketch in §Methods §A (use `\begin{theorem}` / `\begin{proof}`); the full proof may move to an appendix.
- **Length budget:** ~1,000–3,000 words total for most CS papers, scaling with subfield. Theory papers with dense proofs may push to 4,000+ words. Short ML workshop papers may compress to 600 words (1 O paragraph, 2 C paragraphs, skip F/A/I).

## Style rules

- **Tense:** past tense dominates for actions performed ("We measured", "We trained", "We implemented"). Use passive voice only when the actor is genuinely irrelevant ("The dataset was shuffled before each epoch" --- the reader does not care who shuffled it). Use present tense for established procedures or facts about tools ("PyTorch provides automatic differentiation").
- **Voice:** active voice; first-person plural ("we") is standard. Avoid "it is done by…" and "in order to…"; prefer "we do X by…" and "to…".
- **Pseudocode conventions.** Use a standard style (e.g., Cormen-style `while` / `for` / `return`, OR functional-style `let x = ... in ...`). Label every algorithm (`Algorithm 1`, `Algorithm 2`) and give it a descriptive caption. Every variable in pseudocode MUST be defined in §Background §N or §Methods §F — no introducing notation mid-algorithm.
- **Equation conventions.** Number any equation referenced later. Unnumbered display equations are reserved for derivations where only the final line is cited.
- **Figure conventions.** §Methods typically contains 1 pipeline figure (in §Overview) and occasionally 1–2 additional schematics for complex subcomponents. Avoid figure-dumping; each figure must be referenced in text.
- **Citations:** sparse compared to §Background and §Related Work. Cite only (a) foundational primitives the core uses (e.g., Transformer attention in an ML paper builds on Vaswani 2017); (b) prior algorithms the proof analysis compares against; (c) baselines explicitly extended or modified. If a citation belongs in §Background or §Related Work, move it there.
- **Reproducibility language.** When specifying hyperparameters or hardware in §I, be concrete and absolute: "batch size 256, AdamW with learning rate 3e-4, weight decay 0.01, 50 epochs on 8× A100 80GB" — not "standard hyperparameters" or "modern GPUs". Reviewers who want to reproduce need exact numbers.
- **First-use term discipline (carries in from §Introduction).** Any term emphasized with `\emph{...}` for the first time in §Methods must carry an operational gloss in the same sentence or the next. If the term is already defined formally in §Background §N or §Methods §F, a one-clause reminder ("\emph{dispatch mode} --- how each op selects a kernel") is still worth the extra line, since readers skim and a naked term without a local gloss forces a back-reference. Do NOT name a term and defer its definition to a later paragraph under the same section; keep gloss and name adjacent.
- **Subsection granularity.** Organize §Core into named subsections, one per major component. A monolithic §3.2 Core paragraph spanning 2,000 words forces readers to search for the component they care about. Typical pattern: one subsection per `[C]` outline bullet.
- **Complexity claims must be stated formally.** If §Analysis claims "runs in linear time", state it as a theorem or lemma with the input parameters, the computational model, and the bound. Prose-only complexity claims are unverifiable.
- **Dataset and benchmark descriptions must be self-contained.** Even when §Results §Setup repeats the details, §Methods should state the dataset name, size, and any preprocessing in the `[I]` Implementation element. This avoids forcing readers to cross-reference §Results to understand what the method was applied to.
- **Novelty boundary.** Each paragraph in §Core should make clear what is novel vs. what is adopted from prior work. If a paragraph describes a standard technique without marking it as such, a reviewer may assume the author is claiming it as novel. Use phrasing like "Following [cite], we adopt…" for non-novel components.

## Common failure modes

- **Missing overview.** Methods opens directly with Algorithm 1 or a formal definition. Symptom: reviewer writes "hard to follow the high-level approach". Fix: add a §3.1 Overview paragraph with a pipeline figure before any algorithm or equation.
- **Overview without a figure.** §3.1 is a prose-only paragraph describing the architecture. Symptom: reviewer writes "consider adding an overview figure". Fix: invoke `scientific-schematics` to produce a pipeline diagram and reference it in the overview paragraph.
- **Formalization left implicit.** Paper uses symbols that were not defined in §Background §N or §Methods §F. Symptom: readers flip back hunting for definitions. Fix: write §F explicitly, even when the problem seems standard; include input / output types, objective, and constraints.
- **Core without pseudocode.** §Core describes the algorithm in prose only. Symptom: reviewer writes "the algorithm is not precisely specified, reimplementation is ambiguous". Fix: add at least one pseudocode block (Algorithm 1) showing the main procedure.
- **Analysis deferred to appendix without a summary.** §A says "See Appendix B for the proof" with no in-paper claim. Symptom: reviewer without time to read the appendix cannot verify the headline complexity claim. Fix: state the theorem and a one-paragraph proof sketch in §A; the appendix carries the full proof.
- **Core buried inside Implementation.** The main technical novelty is mentioned only in §Implementation among hyperparameter tables. Symptom: reviewer missed the contribution. Fix: promote any core technical decision to §C and keep §I for pure engineering details.
- **Implementation-heavy, design-light.** §Methods is 80% hyperparameters and 20% design. Symptom: reviewer writes "insufficient technical contribution". Fix: expand §C with at least 2 paragraphs of design rationale per core component, keep §I concise.
- **Over-specification of standard components.** §Methods re-derives a standard technique (e.g., softmax attention) in full detail. Symptom: reviewer writes "§3.2 reviews standard material, consider compressing". Fix: cite the canonical reference in one sentence and focus §Methods on novel contributions.
- **Correctness claim without formal statement.** §A says "our approach is correct by construction" without a theorem or invariant. Symptom: reviewer writes "correctness argument is informal". Fix: state the invariant or lemma explicitly; even a short theorem with one-paragraph proof sketch is better than prose assurance.
- **Insufficient detail for replication.** Key steps are omitted or described at too high a level for a competent reader to reproduce. Symptom: reviewer writes "the method cannot be reproduced from the description alone". Fix: every algorithmic step should carry enough detail (parameter values, data structures, loop bounds) that a reader can implement it without guessing.
- **Methods appearing for the first time in Results.** A technique or measurement procedure is first mentioned in §Results rather than §Methods. Symptom: reviewer writes "this analysis was not described in the methods". Fix: all procedures belong in §Methods; §Results only reports outcomes.
- **Including results or interpretation in Methods.** §Methods contains performance numbers or comparative claims that belong in §Results or §Discussion. Symptom: reviewer writes "the methods section reads like a results section". Fix: keep §Methods procedural --- describe what was done, not what was found.
- **Missing statistical tests or evaluation protocol.** The paper reports outcomes without naming the statistical procedure, significance threshold, or evaluation protocol used. Symptom: reviewer writes "how were these numbers computed?". Fix: name every test, metric, and evaluation protocol; state the significance level and any multiple-comparison correction.
- **Datasets/Benchmarks/Workloads under-described.** The paper mentions a dataset or benchmark without stating its size, source, preprocessing, or train/test split. Symptom: reviewer writes "insufficient detail about the evaluation setup". Fix: for each dataset or workload, state its name, size, source citation, and any preprocessing or filtering applied.
- **Undefined abbreviations.** A technical abbreviation is used without being spelled out at first mention. Symptom: reader cannot parse the method. Fix: define every abbreviation at first use in §Methods, even if it was defined earlier in the paper (readers may jump directly to §Methods).
- **Hyperparameter choices unjustified.** Key hyperparameter values are stated without explanation ("batch size 128, learning rate 5e-4"). Symptom: reviewer writes "how were these values chosen?". Fix: briefly state the selection method (grid search, prior work default, sensitivity analysis) for every important hyperparameter.
- **Missing comparison to alternative designs.** §Core presents one design without discussing why alternatives were rejected. Symptom: reviewer asks "why not use approach X instead?". Fix: for each core design decision, include 1--2 sentences explaining why the chosen approach was preferred over the natural alternative.
- **Proof sketch too thin.** §Analysis states a theorem but the proof sketch is a single sentence ("by induction"). Symptom: reviewer writes "the proof sketch is too abbreviated to verify". Fix: provide at least one paragraph outlining the key steps; the full proof goes in the appendix.
- **Inconsistent notation with §Background.** §Methods uses a symbol defined differently in §Background N, or introduces a new symbol that collides with an existing one. Symptom: reader confusion on re-reading. Fix: audit all symbols in §Methods against §Background N before submission; resolve any collisions.
- **Pipeline figure missing data flow.** The overview figure shows boxes and arrows but does not label the data flowing between stages. Symptom: reviewer cannot trace the input-to-output path. Fix: label every arrow in the pipeline figure with the data type or tensor shape; the reader should be able to follow the transformation at each stage.
- **Reproducibility checklist gap.** The paper mentions "standard data augmentation" or "default settings" without specifying what those are. Symptom: reviewer writes "reproducibility is compromised by vague hyperparameter descriptions". Fix: enumerate every non-obvious setting explicitly; if a setting is "standard", cite the reference that defines the standard.
- **Missing ablation hooks.** §Core describes components that are not individually evaluated in §Results. Symptom: reviewer asks "does component A actually help?". Fix: for each major `[C]` component, ensure §Results includes a corresponding ablation RQ. If an ablation is infeasible, state why in §Discussion §Limitations.
