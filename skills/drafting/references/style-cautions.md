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
