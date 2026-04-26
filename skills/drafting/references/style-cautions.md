# Style cautions for section intros and argumentative prose

Five patterns slip past outline compliance and prose-quality review because they look locally fluent but corrupt the paper's structure or invite reviewer attacks. Teach every drafter these before prose is produced, and have every reviewer flag them before the draft ships. They are additive to the prose-style guidance in `section-standards/*.md`: section standards shape paragraph count and structural tags; these cautions shape argumentative structure and term ordering.

Loaded by:

- `skills/drafting/SKILL.md` §Style cautions for section intros and argumentative prose — one-line summary per rule.
- `skills/drafting/references/section-drafter-prompt.md` §Step B — the drafter subagent reads this file at write time.
- `agents/manuscript-reviewer.md` item 7 (Systems-paper argumentative structure) — canonical wording for flagged patterns.
- `agents/spec-reviewer.md` item 5 (Argumentative-structure compliance) — canonical wording for compliance-level flags.

## Overview paragraph discipline

Opening paragraphs that preview their own subsections must obey three rules.

1. **No mechanism spoilers.** If a subsection will formally introduce a concept, mechanism, or defined term, the overview must not name or describe that concept. Point to the subsection by the problem it tackles, not by the solution it will present. Reject phrasings like "introduces the X split" or "defines the Y mechanism" when X or Y is what the subsection itself opens with. Prefer "details how per-contract constants are handled across family members" over "introduces the invariant/variant split, SkelOT's central design insight."

2. **No prominence labels on peer subsections.** Strip both overselling labels ("central insight", "key contribution", "main result", "novel", "the core idea") and underselling labels ("extension", "auxiliary", "minor", "secondary", "not the main focus", "treated as an extension to the core mechanism") from descriptions of individual subsections. Describe every subsection by what it does, in parallel voice. Let ordering, subsection length, and content itself convey weight. Scope limitations that do belong in the paper go in the specific subsection, in a dedicated scope paragraph, or in limitations — never in the top-level overview, because at that position they read as the author handing reviewers a ready-made attack on the downgraded subsection.

3. **Sweep peer items on every fix.** When revising an overview, any fix on one item must propagate to all peer items in the same paragraph. If one subsection was overlabeled ("central insight"), re-inspect every peer for the mirror failure ("extension", "auxiliary"). If one spoiler was removed, scan the rest for other term leaks. A paragraph that calls one subsection "central insight" and another "extension to the core mechanism" has a consistency bug even if each label was written in a different revision pass.

## Lesson 1 — Section responsibility discipline

Each IMRAD section in a systems paper has a narrow job, and numbers must not drift across section boundaries.

- **Ground / Workload section** (typically §3): dataset-independent observations the paper's system is *designed to exploit*. No system-definition premises.
- **Design section** (§4): mechanism definition only. Forward-point to §evaluation for numeric validation. Do NOT dump empirical percentages or distributional facts that depend on the system's definitions.
- **Results section** (§7): empirical findings that *use* the system's mechanism to be measurable.
- **Discussion section**: validity caveats only. Does not restate numbers already reported.

Placement test: "could a third party independent of our system compute this from the raw data alone?" Yes → ground. No → results. A 99.37% statistic that depends on the system's definition of "variant" (cross-member immediate disagreement) is a §Results fact, not a §Ground / Workload fact, no matter how much it looks like a distributional property of the dataset.

## Lesson 2 — Do not pre-hedge scope in argumentative prose

Argumentative sentences must not annotate claims with the dataset name. Phrases like "on X dataset", "in our workload", "on Base mainnet" inside thesis sentences pre-narrow the claim and invite the "does this generalize?" reviewer attack.

Dataset naming is allowed at exactly two places:

1. The subsection where numbers are first reported ("observed across blocks X--Y of Base Mainnet").
2. The discussion section's external-validity block.

Elsewhere — intros, theses, claim sentences, contribution lists — prose is dataset-agnostic.

## Lesson 3 — Section intros foreground claims, not roadmaps

Section intros must not read as "The next subsections do X, Y, Z". That is reporting-style writing: it signals weak argumentation and wastes the intro's rhetorical real estate.

Instead:

- State the conditions / claims / thesis as intrinsically important ("For P to hold, three conditions must be satisfied: ...").
- Push subsection pointers into parenthetical `\S\ref{...}` at the end of the clause where each condition is stated, so they act as navigation hints rather than as the sentence's subject.
- Close with a one-sentence result preview ("All three hold on our workload") rather than "The remaining subsections discuss X, Y, Z in turn".

**Before:**

> The remaining subsections ask (i) how much the boundary reduces units (§3.2), (ii) whether reduction falls on costly bytecode (§3.3), (iii) whether the reuse is durable (§3.4).

**After:**

> For the boundary to be worthwhile, three conditions must hold. First, the boundary must collapse enough distinct bytecodes to be worth exploiting at scale (§3.2). Second, the reduction must fall on bytecodes costly enough to matter (§3.3). Third, the families must be durable templates, not one-off bursts (§3.4). All three hold on our workload.

## Lesson 4 — Forward-reference discipline in intros

A section's intro must not use technical terms that are only defined later in the same section. If §3.1 defines "skeleton", intros to §3 cannot say "skeleton-level reuse" or "skeleton-keyed". Use already-introduced upstream terms (e.g., "reuse boundary") until the definition subsection has been read.

Practical check: scan the intro for any word that appears `\emph{...}` or is first-defined later in the section. If found, replace with its upstream paraphrase or relocate the definition.

## How to apply at drafting time

Before writing any section intro, overview paragraph, thesis sentence, or contribution-list bullet, run the following scan against the intended prose:

1. **Overview scan** — is this paragraph previewing its own subsections? If yes, check every peer item for (a) mechanism spoilers, (b) prominence labels, (c) inconsistency with other peers. Fix all three classes before moving on.
2. **Placement scan (Lesson 1)** — for every percentage or distributional number in Design: can an independent third party compute it from raw data alone? If no, move to Results and replace with a `\S\ref{sec:results}` forward-pointer.
3. **Dataset pre-hedge scan (Lesson 2)** — grep the draft for the dataset name in thesis / contribution / intro positions. Strip unless the sentence is inside the numbers-first subsection or the external-validity block.
4. **Roadmap scan (Lesson 3)** — does any section intro read "The remaining subsections..." or "§X.Y discusses..."? Rewrite as a claim-first thesis with parenthetical `\S\ref{...}`.
5. **Forward-reference scan (Lesson 4)** — for each section's intro paragraph, list the emphasized terms (`\emph{...}`) and defined-later nouns. Replace each with an upstream paraphrase, or relocate the definition.

## How to apply at review time

The reviewer agents (`manuscript-reviewer.md` item 7; `spec-reviewer.md` item 5) carry the patterns and severities inline, since agent files are loaded whole as system prompts. Use this reference as the canonical source when updating reviewer wording so the two agents stay in sync.

## Imported Patterns (from scientific-writing dissolution)

Five patterns originally extracted from the scientific-writing skill's Common Writing Pitfalls, adapted for systems-paper context. These complement the five structural patterns above: the structural patterns govern where claims live and how intros are organized; these govern word- and sentence-level clarity.

### Jargon Overload

A draft accumulates domain-specific shorthand until a reader outside the immediate sub-area cannot follow the argument. Systems papers are particularly vulnerable because reviewers span compiler runtime, architecture, networking, and ML audiences -- a term obvious to one group is opaque to another.

**Why it hurts.** Jargon-dense prose excludes reviewers. A reader who stalls on an undefined acronym stops evaluating the argument and starts second-guessing the paper's clarity. This is a top-five rejection reason at systems venues, where program committees are deliberately cross-area.

**How to apply.** Define every non-standard abbreviation at first use. Treat "first use" per-section for the abstract and main text independently. If a term appears fewer than three times in the paper, write it out each time -- the abbreviation saves nothing. When a paragraph introduces more than two new abbreviations, split the paragraph or move definitions earlier. Standard abbreviations (CPU, GPU, RAM, API, OS, VM) need no definition; everything else does.

**BAD:**

> The BTB miss rate dominates the MMU path because CoW pages trigger NUMA-remote walks.

**GOOD:**

> The branch target buffer (BTB) miss rate dominates the memory management unit (MMU) path because copy-on-write (CoW) pages trigger non-uniform memory access (NUMA) remote walks.

### Nominalization

The draft replaces strong verbs with noun phrases -- "perform a comparison of" instead of "compare", "make a determination" instead of "determine", "provide a description of" instead of "describe". The sentence gains words, loses momentum, and pushes the main verb further from the subject.

**Why it hurts.** Nominalized constructions add syllables without adding information. In a systems paper where every word competes with equations, tables, and figures, wasted syllables are tax on the reader. They also obscure agency: "a comparison was performed" hides who compared what.

**How to apply.** After drafting a paragraph, scan for patterns like "make a N", "perform a N", "conduct a N", "provide a N", "carry out a N". Replace each with the corresponding verb. Apply the same scan to "the N of" constructions: "the optimization of" -> "optimizing", "the verification of" -> "verifying".

**BAD:**

> We performed a comparison of the two schedulers and made the determination that the work-stealing variant provides an improvement of 12% in tail latency.

**GOOD:**

> We compared the two schedulers and determined that the work-stealing variant improves tail latency by 12%.

### Hedging Calibration

The draft either over-hedges measured results ("appears to achieve up to a 12% improvement") or under-hedges generalizations drawn from a single workload ("this technique eliminates branch mispredictions"). Systems papers need calibrated hedging: measured numbers get minimal hedging, extrapolations get explicit hedging.

**Why it hurts.** Over-hedging a measured result signals that the author does not trust the measurement, inviting the reviewer to distrust it too. Under-hedging an unmeasured claim signals carelessness, inviting the reviewer to search for counter-examples. Both erode credibility.

**How to apply.** Apply a simple test to every claim sentence. If the sentence reports a directly measured number with a clear experimental setup, hedge minimally or not at all: "reduces latency by 12% (Table 2)". If the sentence generalizes beyond the experiment, hedge explicitly: "may generalize to other workloads" or "we expect this holds for". Never double-hedge ("could perhaps possibly") -- one hedge word per unsupported claim is sufficient.

**BAD:**

> Our approach appears to achieve a roughly 12% improvement in throughput (Figure 4), and we believe this eliminates the need for hardware transactional memory in all server workloads.

**GOOD:**

> Our approach improves throughput by 12% (Figure 4). Whether this improvement extends to workloads dominated by irregular memory access remains an open question.

### Abbreviation Discipline

The paper introduces an abbreviation at first use but then uses the expanded form anyway, or defines an abbreviation that appears only once or twice. Alternatively, the paper accumulates so many abbreviations that readers cannot track them without a glossary.

**Why it hurts.** An abbreviation used only once wastes the reader's attention on a definition they will never need again. An abbreviation used inconsistently (sometimes expanded, sometimes not) creates confusion about whether two different abbreviations refer to the same concept. More than about five non-standard abbreviations in a paper forces the reader to flip back and forth.

**How to apply.** After the final draft, generate a list of every abbreviation and count its occurrences. Remove any abbreviation used fewer than three times. If the paper retains more than five non-standard abbreviations, add a "Key abbreviations" table in an appendix or footnote. Check that each abbreviation is defined exactly once per section (abstract and main text count as separate sections). Never abbreviate in section titles or figure captions.

**BAD:**

> We implemented a just-in-time (JIT) compiler. The JIT compiles bytecode at runtime. We evaluated the JIT on three benchmarks.

(The abbreviation is fine here, but elsewhere in the same paper:)

> The JCC (JIT compilation cache) stores compiled code. The just-in-time compiler flushes the JCC on context switch.

(Inconsistent: "JIT" vs "just-in-time compiler" after definition; JCC defined but used only twice.)

**GOOD:**

> We implemented a just-in-time (JIT) compiler. The JIT compiles bytecode at runtime. We evaluated it on three benchmarks.

(JCC either written out as "compilation cache" each time, or given a stable abbreviation used consistently.)

### Common Pitfalls (composite)

Several sentence-level faults recur across systems papers: passive-voice overuse in methods and design sections, weak verb choice ("utilize" for "use", "leverage" for "apply"), vague modifiers ("very", "really", "quite", "significantly" without a p-value), redundant pairs ("each and every", "basic and fundamental", "null and void"), and narrative drift in methods sections where the prose wanders between what was done, why it was done, and what the result was.

**Why it hurts.** Passive voice in design sections hides the system's architecture behind actor-less sentences, making it unclear whether the system or the experimenter performs each action. Weak verbs inflate sentences without adding precision. Vague modifiers invite the reviewer to ask "how much?" and suspect the number is unflattering. Redundant pairs waste space. Narrative drift in methods forces the reader to re-read paragraphs to separate procedure from rationale.

**How to apply.** Run five micro-scans on the final draft. (1) Passive scan: flag every passive clause in design and methods. Rewrite half or more as active, keeping passive only when the receiver of the action is the topic sentence's subject. (2) Weak-verb scan: search for "utilize", "leverage", "facilitate", "implement" (when "build" or "write" works). Replace each with a concrete verb. (3) Modifier scan: delete "very", "really", "quite", "highly" unless followed by a measurable comparison. Replace "significantly" with a parenthesized p-value or remove it. (4) Redundancy scan: delete one element of each redundant pair. (5) Methods-narrative scan: in every methods paragraph, verify that each sentence either describes a procedure or justifies a design choice, never both in the same sentence.

**BAD:**

> The system was designed to facilitate the utilization of sparse data structures. A very significant reduction in memory usage was achieved through the use of a basic and fundamental remapping technique. The evaluation was conducted on three benchmarks, which were selected because they represent real-world workloads, and the results showed a 30% improvement.

**GOOD:**

> The system uses sparse data structures to reduce memory usage. Remapping bytecodes to compact encodings cuts working set size by 30% (Table 3). We evaluated on three benchmarks chosen to span real-world workload characteristics (§5.1).
