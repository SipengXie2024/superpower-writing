# Style cautions for section intros and argumentative prose

These patterns slip past outline compliance and prose-quality review because they look locally fluent but corrupt the paper's structure or invite reviewer attacks. Teach every drafter these before prose is produced, and have every reviewer flag them before the draft ships. They are additive to the prose-style guidance in `section-standards/*.md`: section standards shape paragraph count and structural tags; these cautions shape argumentative structure and term ordering.

Loaded by:

- `skills/drafting/SKILL.md` §Writing standards, a one-line summary per rule.
- `skills/drafting/references/claim-first.md` §Step B, read at write time before section intros.

Canonical rulebook: `_shared/core/house-style.md`. It states the rules; this file
is the drafting-time scan and the worked before-and-after pairs. On any conflict,
the house style wins, and a project `.claude/CLAUDE.md` wins over both.

## Contents

- **Overview paragraph discipline**: paragraphs that preview their own subsections, with the three rules against mechanism spoilers, prominence labels on peer subsections, and labels left inconsistent between peers.
- **Lesson 1, section responsibility discipline**: which IMRAD section each number belongs in, and the "could a third party compute this from raw data alone?" placement test.
- **Lesson 2, dataset pre-hedging**: why thesis and claim sentences must not name the corpus, and the two positions where naming it is allowed.
- **Lesson 3, claim-first section intros**: replacing "the remaining subsections do X, Y, Z" with a thesis plus parenthetical section pointers, with a before-and-after pair.
- **Lesson 4, forward references in intros**: terms an intro uses that its own section only defines later, and the scan that catches them.
- **Lesson 5, Results topic and closing sentences**: the three-zone paragraph discipline, qualitative answer first and design implication last, with a before-and-after pair.
- **Lesson 6, multi-corpus results**: listing corpora as peers in canonical order instead of anchoring on one and generalizing to the rest, with a before-and-after pair.
- **How to apply, at drafting time and at review time**: the seven-step scan to run before writing intros, overviews, theses, and contribution bullets, keyed to the lessons above.
- **Word- and sentence-level scans**: six passes over a finished draft covering abbreviations, hedging, nominalizations, passive voice, empty intensifiers, and redundant doublets.
- **Reviewer-facing hard rules**: what lives in `_shared/core/house-style.md` instead, including punctuation, claim form, inflated adjectives, and the accept/reject defaults of an aggressive polish.

## Overview paragraph discipline

Opening paragraphs that preview their own subsections must obey three rules.

1. **No mechanism spoilers.** If a subsection will formally introduce a concept, mechanism, or defined term, the overview must not name or describe that concept. Point to the subsection by the problem it tackles, not by the solution it will present. Reject phrasings like "introduces the X split" or "defines the Y mechanism" when X or Y is what the subsection itself opens with. Prefer "details how per-contract constants are handled across family members" over "introduces the invariant/variant split, SkelOT's central design insight."

2. **No prominence labels on peer subsections.** Strip both overselling labels ("central insight", "key contribution", "main result", "novel", "the core idea") and underselling labels ("extension", "auxiliary", "minor", "secondary", "not the main focus", "treated as an extension to the core mechanism") from descriptions of individual subsections. Describe every subsection by what it does, in parallel voice. Let ordering, subsection length, and content itself convey weight. Scope limitations that do belong in the paper go in the specific subsection, in a dedicated scope paragraph, or in limitations — never in the top-level overview, because at that position they read as the author handing reviewers a ready-made attack on the downgraded subsection.

3. **Sweep peer items on every fix.** When revising an overview, any fix on one item must propagate to all peer items in the same paragraph. If one subsection was overlabeled ("central insight"), re-inspect every peer for the mirror failure ("extension", "auxiliary"). If one spoiler was removed, scan the rest for other term leaks. A paragraph that calls one subsection "central insight" and another "extension to the core mechanism" has a consistency bug even if each label was written in a different revision pass.

## Lesson 1 — Section responsibility discipline

*Canonical rule: house style §4.*

Each IMRAD section in a systems paper has a narrow job, and numbers must not drift across section boundaries.

- **Ground / Workload section** (typically §3): dataset-independent observations the paper's system is *designed to exploit*. No system-definition premises.
- **Design section** (§4): mechanism definition only. Forward-point to §evaluation for numeric validation. Do NOT dump empirical percentages or distributional facts that depend on the system's definitions.
- **Results section** (§7): empirical findings that *use* the system's mechanism to be measurable.
- **Discussion section**: validity caveats only. Does not restate numbers already reported.

Placement test: "could a third party independent of our system compute this from the raw data alone?" Yes → ground. No → results. A 99.37% statistic that depends on the system's definition of "variant" (cross-member immediate disagreement) is a §Results fact, not a §Ground / Workload fact, no matter how much it looks like a distributional property of the dataset.

## Lesson 2 — Do not pre-hedge scope in argumentative prose

*Canonical rule: house style §3.3. The abstract may name the corpus scale (§8.19); argumentative prose still may not.*

Argumentative sentences must not annotate claims with the dataset name. Phrases like "on X dataset", "in our workload", "on Base mainnet" inside thesis sentences pre-narrow the claim and invite the "does this generalize?" reviewer attack.

Dataset naming is allowed at exactly two places:

1. The subsection where numbers are first reported ("observed across blocks X--Y of Base Mainnet").
2. The discussion section's external-validity block.

Elsewhere — intros, theses, claim sentences, contribution lists — prose is dataset-agnostic.

This rule is about dataset names, not about costs. Naming the failure scenario or workload class where the design pays (Dynamo's "sacrifices consistency under certain failure scenarios") is a property of the design and belongs in the abstract; see `skills/_shared/core/classic-moves.md`, override O3.

## Lesson 3 — Section intros foreground claims, not roadmaps

*Canonical rule: house style §5, section openings synthesize rather than enumerate.*

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

## Lesson 5 — Results topic and closing sentences carry qualitative conclusions

*Canonical rule: house style §6.4.*

Results paragraphs run a strict three-zone discipline. The first sentence states the qualitative answer to the research question. The last sentence states the design or scientific implication. The middle carries supporting numbers, table references, and methodology.

**Why it hurts.** Methodology-framing topic sentences ("a static scan of the filtered corpus answers RQ1", "this section reports compile-time savings", "we compute X over Y") tell the reader work was done but not what was found. Reviewers skim topic sentences; if they read process narration instead of conclusions, the paragraph reads as a process log rather than a result. Closing sentences that merely summarize the data ("the data shows Z") miss the chance to land the design implication, leaving the design choice un-anchored to its evidence.

**How to apply.** Replace methodology topic sentences with the qualitative answer itself. Push closing sentences from "the data shows Z" to "treating Z as ... therefore matches ...". Before submitting, read the first and last sentence of every Results paragraph in sequence; if the chain reads as a coherent standalone narrative without the body sentences, the discipline is in place. If the chain reads as a list of methodology pointers and data summaries, rewrite topic and closing sentences across the section.

**Before:**

> A static scan of the filtered corpus answers RQ1. The constants inside multi-member families are overwhelmingly stable. On Base, 93.06% of PUSH-immediate bytes hold the same value in every family member. The invariant subset that the system preserves as compile-time constants is therefore the dominant case, not a sparse side channel.

**After:**

> Most bytes inside multi-member bytecode families are invariant across members, answering RQ1. The invariant PUSH-immediate byte share is 93.06% on Base, computed over 428 multi-member families. Treating these invariant bytes as compile-time constants therefore matches the common case in deployed contracts, not a corner case.

## Lesson 6 — Multi-corpus results read as parallel evidence, not anchor + extension

*Canonical rule: house style §6.5.*

When a finding is supported by data from multiple corpora, list the corpora as peers in canonical order rather than anchoring on one and treating the rest as a generalization check.

**Why it hurts.** Anchor-and-extension framing implicitly privileges the anchor and invites the reviewer pushback "your result depends on the anchor corpus and may not generalize". The connector "the same comparison reproduces this structure on the other corpora" is a tell — it signals the prose was written single-corpus first and retrofitted, and reviewers parse the seams. Parallel framing answers the generalization pushback by construction; anchor-extension framing concedes it.

**How to apply.** Topic sentence names the corpora as a set ("on every studied chain", "across the four datasets"). Data sentence lists per-corpus numbers in canonical order with sample counts in matching order: "X% on A, Y% on B, ..., over n_A, n_B, ... families respectively". If one corpus has additional data the others do not (e.g., a longitudinal stat measured only on the primary chain), demote it to a chain-specific complement after the parallel listing rather than leading with it. The conclusion sentence frames the finding as "across the studied chains" rather than "on A, with similar results on B, C, D".

**Before:**

> On Base, the invariant share is 93.06% over 428 families. The same byte-level cross-member comparison on the Ethereum, BSC, and Arbitrum 10K-block windows reproduces this structure: 92.32% on Ethereum, 93.35% on BSC, and 93.23% on Arbitrum.

**After:**

> The invariant share is 93.06% on Base, 92.32% on Ethereum, 93.35% on BSC, and 93.23% on Arbitrum, over 428, 682, 168, and 99 multi-member families respectively.

## How to apply at drafting time

Before writing any section intro, overview paragraph, thesis sentence, or contribution-list bullet, run the following scan against the intended prose:

1. **Overview scan** — is this paragraph previewing its own subsections? If yes, check every peer item for (a) mechanism spoilers, (b) prominence labels, (c) inconsistency with other peers. Fix all three classes before moving on.
2. **Placement scan (Lesson 1)** — for every percentage or distributional number in Design: can an independent third party compute it from raw data alone? If no, move to Results and replace with a `\S\ref{sec:results}` forward-pointer.
3. **Dataset pre-hedge scan (Lesson 2)** — grep the draft for the dataset name in thesis / contribution / intro positions. Strip unless the sentence is inside the numbers-first subsection or the external-validity block.
4. **Roadmap scan (Lesson 3)** — does any section intro read "The remaining subsections..." or "§X.Y discusses..."? Rewrite as a claim-first thesis with parenthetical `\S\ref{...}`.
5. **Forward-reference scan (Lesson 4)** — for each section's intro paragraph, list the emphasized terms (`\emph{...}`) and defined-later nouns. Replace each with an upstream paraphrase, or relocate the definition.
6. **Topic-and-closing scan (Lesson 5)** — for each Results paragraph, read only the first and last sentence. If the topic sentence narrates methodology rather than answering an RQ, rewrite. If the closing sentence merely summarizes the data rather than stating a design or scientific implication, push it one step further.
7. **Parallel-corpora scan (Lesson 6)** — grep Results paragraphs for connectors like "the same comparison ... reproduces" or "this pattern also holds on". When found, restructure the surrounding prose to list all corpora as peers in one sentence, with sample counts in matching order.

## How to apply at review time

This reference is the canonical source for these patterns and their severities. `drafting` reads it at write time and `polish` reuses it, so keep the wording here authoritative.

## Word- and sentence-level scans

The lessons above govern where claims live and how intros are organized. These govern word and sentence level clarity, and they run over a finished draft.

1. **Abbreviation scan.** Define every non-standard abbreviation at first use, counting the abstract and the main text as separate sections. Standard ones (CPU, GPU, RAM, API, OS, VM) need none. Drop any abbreviation the paper uses fewer than three times and write the term out instead, and never abbreviate in a section title or a figure caption. Once the paper carries enough non-standard abbreviations that a reader would have to hunt for a definition, add a "Key abbreviations" table in an appendix or a footnote.
2. **Hedging scan.** A directly measured number takes minimal hedging or none ("reduces latency by 12% (Table 2)"). A claim that generalizes beyond the experiment takes one explicit hedge. Never stack two hedges on one claim.
3. **Nominalization scan.** "perform a comparison of", "make a determination", and "the optimization of" become "compare", "determine", and "optimizing".
4. **Passive scan.** Design and methods prose goes active, keeping the passive only where the receiver of the action is the paragraph's topic.
5. **Modifier scan.** Delete intensifiers that quantify nothing ("very", "really", "quite", "highly", and "significantly" without a p-value).
6. **Redundancy scan.** Delete one element of each redundant pair: "each and every", "basic and fundamental", "null and void". Coordinate doublets read as padding, and only one half ever carries meaning.

## Reviewer-facing hard rules: see the house style

The fixed conventions that govern punctuation, claim form, reviewer
self-containment, inflated adjectives, and the accept/reject defaults of an
aggressive editing pass now live in one place, `_shared/core/house-style.md`,
so every skill that writes or edits reviewer-facing prose reads the same rules.
Read it before drafting any section, and treat it as canonical wherever it
overlaps this file. The short version of what moved there:

- No em-dashes and no in-sentence colons, with the standard substitutions (§1).
- No low-level identifiers in argumentative prose, observation before name (§2).
- Goal-form, not precondition-form (§3.1); delete defensive negations (§3.2).
- Direct positive contrasts over stacked `rather than` tails (§6.2).
- Strip inflated adjectives and let the numbers carry the load (§6.6).
- The default-REJECT and default-ACCEPT lists for an aggressive polish (§7).

The lessons above stay here because they are the drafting-time application: what
to scan for, in which paragraph position, with the before-and-after pairs. The
canonical rule behind each is noted at its heading.
