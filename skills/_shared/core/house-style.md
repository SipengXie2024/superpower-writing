# House Style: Reviewer-Facing Prose and Figures

The plugin's default style guide for every piece of prose a reviewer will read: abstract, introduction, related work, background, methods, results, discussion, threat model, limitations, conclusion, rebuttal, response letter, and peer review. It also fixes the paper's figure pattern (§9).

This guide is project-agnostic and migrates between papers. Rules are stated generically; the quoted sentences are illustrations drawn from real papers, not bindings on your project's wording. Keep the examples when you apply a rule, they are what makes it applicable.

## Contents

- Precedence, and which skills load this file
- Core principles (quick reference)
- §1 Punctuation (no em-dashes, no in-sentence colons)
- §2 Reviewer-facing self-containment
- §3 Argument form
- §4 Section responsibility (generic IMRAD)
- §5 Term economy and section register
- §6 Prose preferences
- §7 Editing-pass defaults
- §8 Senior co-author editing conventions
- §9 The paper's figure pattern

## Precedence

1. **A project style file wins.** When the paper repo carries `.claude/CLAUDE.md`, `AGENTS.md`, or an equivalent project rulebook with prose rules, those are hard constraints that override everything here. Surface any house-style rule the project file contradicts rather than silently applying both.
2. **This file is the default** when no project file speaks to the point.
3. **Inside this file, §8 wins.** §8 records one senior co-author's observed editing conventions. Where §8 contradicts §1 through §7, follow §8.
4. **Nothing here weakens an evidence rule.** The claim-first protocol, `[NEEDS-EVIDENCE]` preservation, and the no-fabrication rule outrank every stylistic preference in this file. A smoother sentence that turns an unknown fact into an asserted one is a regression, not a polish.

## Loaded by

- `polish` as its fourth pass, after de-AI, Strunk, and evidence-led wording.
- `drafting` before the first section, and again before any section intro, overview paragraph, or thesis sentence.
- `outlining` when naming sections and framing claim bullets.
- `rebuttal` for the response letter's register.
- `claim-verification` as an advisory wording sweep.
- The figure skills (`tikz-figures`, `scientific-visualization`, `scientific-schematics`) for §8.4, §8.8, §8.18, and §9.

---

## Core Principles (quick reference)

1. **Plain and concise by default**. Prefer the plainest word and the shortest sentence that still carries the argument. This is the standing register for every edit, applied without being asked, not a mode the user must request each time. Cut filler, merge sentences that share a subject, and drop mechanism detail already covered elsewhere.
2. **Reviewer self-containment**. Any reader who has never seen the implementation must be able to follow the argument.
3. **Observation before name, general before specific, claim before evidence**.
4. **Goal-form, not precondition-form**. Design enforces properties by construction; it does not check at runtime.
5. **Numbers carry the load**. Strip adjectives that wrap quantitative evidence in advocacy.
6. **Compress before polishing**. Delete redundancy, defensiveness, and self-weakening qualifiers first.
7. **Each rule applies on the first pass**. Do not wait for a second round of feedback to offer substitutions.
8. **Senior co-author conventions win on conflict**. §8 records his observed editing conventions; where they contradict these defaults, follow §8.

---

## 1. Punctuation

**Never use em-dashes (`---`, `--`, or a single em-dash) in prose. Never use in-sentence colons.** Both are stylistically permitted in academic English; the preference is fixed.

Standard substitutions:

- `X --- appositive list --- verb ...` becomes `X, including Y, Z, and W, verb ...`
- `general claim: specific elaboration` becomes two independent sentences, or `general claim, so specific elaboration`
- `... main clause --- trailing elaboration.` becomes `..., and/but/so trailing elaboration.` or a sentence break

**Exceptions**: the colon introducing a LaTeX `\begin{itemize}` list, and a colon inside a section title (§8.1). Inside `\item` bodies, em-dashes must still be replaced.

When the user highlights a region containing `---` or a mid-sentence `:`, treat it as an implicit ask to replace.

---

## 2. Reviewer-Facing Self-Containment

Any text reaching a reviewer must read standalone to someone who has never seen the implementation.

**No low-level identifiers in argumentative prose.** Function names, struct or enum names, field identifiers, file paths, line numbers, raw byte-layout phrases, and hex literals belong in an Implementation section or supporting material, never in claim text.

**Define every technical term at first use.** Do not rely on "as defined earlier" across sections, since reviewers skim. Expand acronyms at first mention per section (CFG, AOT, GC, IR, and so on).

**Observation, then name.** Describe what a thing does or is, then attach the term. Naming then feels earned rather than stipulated.

The Implementation section is the one place where named components are appropriate. Even there, name a component once, define what it does, then use the descriptive name in subsequent prose.

**Appendix as a separate supplementary file** (venues that require it). Body sections never write `Appendix~\ref{...}`; point with the fixed phrase "the supplementary material". Appendix-internal references keep `\ref`; appendix-to-body references render as plain section numbers. Keep a `\clearpage` between the bibliography and the appendix so the PDF cut stays page-aligned. When the venue allows an in-paper appendix, §8.18's short-appendix rule applies instead and `Appendix~\ref{...}` is fine.

**Draft scan checklist.** If any of these is present, rewrite:

- Any CamelCase identifier
- Any snake_case identifier
- Any `0x[0-9a-f]+` hex literal
- Any acronym not expanded in the same paragraph
- Any term used before its first-use definition
- Any `Appendix~\ref` in a body section, when the venue splits the appendix out

---

## 3. Argument Form

### 3.1 Goal-form, not precondition-form

- Good: "The system's goal is X; the design enforces this by construction." Reads as a correctness commitment.
- Bad: "The system does Y only when X holds." Reads as a runtime check, often unverifiable at the stated time, and misrepresents the causal arrow.

Reuse boundaries, admission filters, and sharing rules are *designed to guarantee X by construction*, not to verify X at runtime.

### 3.2 Delete defensive negations; keep substantive disambiguations

Test: would a careful reviewer produce the negated reading on their own?

- **No.** Defensive. The reader was never going to read it that way, and rebutting a misreading makes prose self-conscious. Delete it and state the positive form alone (Strunk §15).
- **Yes.** Two plausible readings, and the paper must actively reject one. Keep it, this is disambiguation, not defense.

### 3.3 Argumentative prose does not name the dataset or corpus

Bad: "on Base Mainnet," "on our corpus," "in our workload," "for our benchmark suite" inside thesis or claim sentences.

These signal overfitting and invite the "does this generalize?" attack. State conditions, claims, and theses in general form.

The corpus name appears at exactly two canonical places:

1. The evaluation-setup section, or wherever measurement numbers are first reported.
2. The discussion section's external-validity block.

Per-section scope footers may also bound the corpus. Everywhere else, argumentative prose stays dataset-agnostic. §8.19 carves out one exception: the abstract may name the corpus scale.

### 3.4 No rebuttal register; positive framing in the manuscript

The manuscript is not a response letter. Performative honesty and self-justification belong in a rebuttal, never in the abstract, introduction, or related work. Strip meta-commentary that narrates the authors' own fairness or candor; state the substance plainly.

**Performative-honesty framing, all bad.** "we never let that gap hide," "we state X up front," "we cite and differentiate it rather than bury it," "stated honestly," "our claim is narrow and defensible," "is explicit that." These describe the authors' conduct instead of making a claim, and read as a writer defending themselves to a reviewer.

**Novelty as gap, not as disclaimer.** Introduce prior work by naming the concrete gap it leaves, then state how the design closes that gap by construction. The novelty claim becomes the natural result of closing the gap.

- Bad: "We do not claim to be the first to run a router in an enclave. Our claim is narrower and defensible. Two properties separate it from prior art."
- Good: "Prior attested gateways leave two gaps. First, ... Second, ... \sys closes both by construction. It ... and it ..."

**Caveats as plain scope, not confession.** Title scope statements neutrally (Scope of the claim), and state each boundary as a fact. Drop the self-conscious wrapper that announces the authors are being forthcoming.

- Bad: "Two caveats we keep in view throughout. ... we never let that gap hide. We state two boundaries up front."
- Good: "Scope of the claim. Attestation proves code identity, not benignity. Two boundaries delimit the claim."

Related to 3.2: defensive negation rebuts a misreading, rebuttal register defends the authors. Both make prose self-conscious; delete both and state the positive form.

---

## 4. Section Responsibility (Generic IMRAD)

Each chapter has a narrow job. Cross-section drift is a recurring correction target.

| Section | Job | Forbidden |
|---|---|---|
| **Workload / Motivation** | Properties of the studied artifact, independent of the proposed system | Mechanism premises, system-defined metrics |
| **Design / Method** | Define the proposed mechanism; mention-and-forward to numeric findings | Dumping quantitative results |
| **Results / Evaluation** | Numbers that depend on the system's definitions or demonstrate its effect | (none) |
| **Discussion** | External validity, generalization caveats, deployment implications | Restating workload or results numbers |

**Test for ambiguous numbers.** Does this value require the proposed system's definitions to be measurable, or could any researcher with the raw data compute it?

- System-dependent, so Results.
- Definition-independent, so Workload.
- A value that uses a proposed concept to be measurable is system-dependent even if the underlying data is neutral.

---

## 5. Term Economy and Section Register

**Each technical term is introduced (with definition) at exactly one canonical position.** Other positions reference but do not redefine. Cross-section redundant definitions are a structural error, even if each individual definition reads correctly.

**Section openings synthesize, not enumerate.** Open with a claim or thesis that frames the section. Avoid "this section first describes X, then Y, then Z", and reserve roadmaps for survey-style chapters where they are genre-appropriate.

**Do not frame core mechanisms with self-deprecating qualifiers.** Avoid "an extension of the core mechanism," "albeit a side concern," "though only auxiliary." Lead with the design, let it stand on its own merits, and place qualification, if needed, in Discussion.

**Name a repeated entity once, then refer back lightly.** When a paragraph keeps pointing at the same thing, a study, a system, or a named artifact such as an enclave image or component, name it once and afterward use a pronoun or a short demonstrative. Do not repeat the full noun phrase in nearby sentences ("The study tests ... The study concludes ...", or "a microbenchmark image ... This microbenchmark image ..."). Keep an explicit re-attribution only where the paper then builds on that specific claim.

---

## 6. Prose Preferences

### 6.1 Compress before polishing

Delete redundant setup, defensive explanation, and self-weakening qualification before trying to make it sound better.

### 6.2 Prefer direct positive contrasts

Delete a `rather than` or `instead of` contrast tail when the positive clause already implies it. "reach providers through an intermediary rather than directly" becomes "reach providers through an intermediary", since an intermediary already means not directly. This applies to a single occurrence, not only to repeated ones. Keep the contrast when it is load-bearing, such as a thesis or research-question framing ("Rather than detect a malicious router after the fact, can we remove the operator's ability to misbehave?"). State the positive claim first, and reserve an explicit contrast for a real one.

### 6.3 Evaluation prose

- Pair setup and result when that makes the research question easier to read.
- Use manuscript prose for the main interpretation. Put dense numbers, including grids, slopes, coefficients, percentiles, and long distributions, in figures, tables, captions, or supporting material.
- If a table or figure already carries the quantitative detail, the body can stay qualitative.
- If a broad correctness gate is stronger than a representative sanity check, lead with the broad gate; do not give the small check table-level prominence.
- Report runtime speedups as measured systems effects. If the microscopic cause was not isolated, leave it to future work without weakening the measured result.

### 6.4 Topic and closing sentences carry qualitative conclusions, not methodology narration

- First sentence of a Results paragraph: the answer to the research question.
- Last sentence: the design or scientific implication.
- Middle: supporting numbers, table references, methodology.

Reading only the first and last sentences of every Results paragraph should yield a defensible standalone narrative.

- Bad, methodology-framing topic sentences: "a static scan answers RQ1," "we report results in this section."
- Good: qualitative answers as topic sentences.

### 6.5 Multi-corpus results read as parallel evidence, not anchor plus extension

List corpora as peers in canonical order with sample counts in matching order:

> "X% on A, Y% on B, ..., over n_A, n_B, ... families respectively."

Bad: "the same comparison reproduces this structure on the other corpora". It signals the prose was written single-corpus first and retrofitted, and invites the "your result depends on the anchor corpus" pushback.

If one corpus has additional data the others do not, demote it to a corpus-specific complement after the parallel listing rather than leading with it.

### 6.6 Strip inflated adjectives, the numbers carry the load

A 90-plus percent number already establishes the claim. Inflated adjectives wrap it in advocacy and read as compensation for weak evidence rather than confidence in strong evidence.

**Remove**: overwhelmingly, dominant, captures, sparse side channel, settling RQ in the affirmative, highly, extensively, robustly, comprehensively.

| Inflated | Direct |
|---|---|
| overwhelmingly invariant | most bytes are invariant, or the percent alone |
| dominant case, not a sparse side channel | common case, not a corner case |
| settling RQ in the affirmative | answering RQ |
| captures the dominant structure | matches the structure, or a factual description |

"Common case / corner case" is the systems-paper-native contrast: it preserves the rebuttal-of-objection function without promotional language.

### 6.7 Discussion register

- Neutral-positive tone. Do not over-criticize the paper.
- Prefer: scope, transfer, follow-on evaluation, natural extension, falls back toward fine-grained compilation, intentionally precise boundary.
- Avoid: apologetic limitation language.
- Default: one paragraph per subsection.
- Discussion explains implications, when the method helps, evaluation scope, and future opportunities. It is not a provenance log.

### 6.8 Local revisions

- When asked whether a paragraph is necessary, bias toward deletion if it is redundant, defensive, or already covered by a table, figure, or another section.
- Do not add broad strategy when the task is a local prose edit.

### 6.9 Abstract and introduction foreground main-body contributions

The evidence named in the abstract and introduction should follow the paper's own prominence ordering. Do not headline an appendix-only supporting analysis, and do not name a specific appendix artifact while a main-body contribution it supports goes unmentioned. Name main-body validation directly. For appendix-only support that overlaps a stronger main-body result, fold it into a general phrase or drop it.

### 6.10 Pattern-density rhythm passes

Two grammatical constructions read as model cadence when dense. Judge them per section with counts, not per instance, and cut to roughly half, never to zero.

- **Causal tails** (`..., so ...`). Keep one where the inference is non-obvious or the sentence closes a paragraph; otherwise split into juxtaposed sentences, fold the consequence into a relative clause, or prepose with "Because".
- **Contrast scaffolds** (`rather than`, `X, not Y`, `instead`). Delete tails the positive clause already implies ("paid once per session rather than per request"). Keep substantive disambiguations ("application-layer, not network-layer") and thesis contrasts ("removes the capability rather than detecting its use").
- **Replacement variety.** When rewriting many instances of one pattern, vary the substitute shapes: sentence split, relative-clause fold, preposed cause, plain deletion. If over a third of the fixes share one shape, the pattern has only changed clothes.

---

## 7. Editing-Pass Defaults

When aggressive polish on long sections returns many paragraph-pair replacements, 70 to 90 percent are typically correct. The remaining patterns recur and have stable defaults.

### 7.1 Default REJECT

**Stripping parenthetical limiters that establish term scope at first use.**
Example: `Naive (per-hash) AOT` becoming `Naive per-hash AOT` loses the scope marker.

**Modifier reordering that flips the argumentative subject of a sentence.**
Example: `compilability filter (...) identically to Naive AOT` becoming `compilability filter used by Naive AOT` changes whose filter it is.

**Deletion of mid-sentence editorial qualifiers that bind to a downstream argument.**
Example: `Third, and most consequential in production` losing the qualifier.

**Semicolon-merge of two short sentences when one is a term-definition statement.**
Definition lines like `We call these positions invariants.` remain standalone sentences.

**Register downgrades.**
Example: replacing neutral academic phrasing like `is part of` with breezy phrasing like `falls out of`.

**Synonym swaps that blur a domain-precise term.**
Example: `has a different measurement` becoming `is measured differently` loses the attestation meaning (a different measurement value, not a different measurement method). Keep the precise term even when the swap reads smoother.

### 7.2 Default ACCEPT

**Removal of self-deprecating qualifiers wrapped around a real design choice.**
Example: `Admission as an extension` becoming `Admission`. When the Discussion section already articulates the trade-off confidently, design-section self-deprecation should go. Optionally add a forward-reference into Discussion to preserve scope visibility.

**Active-voice conversions that preserve meaning** (`is X by Y` becoming `Y X-es`).

**Defensive-negation removal** where the negation guards against a critique no reviewer would raise (`rather than by an arbitrary modeling compromise`), per §3.2.

---

## 8. Senior Co-author Editing Conventions

Observed across one senior co-author's direct editing passes and revision lists. These conventions are person-bound, not project-bound: carry them to the next paper with him. Where they conflict with the defaults above, they take precedence.

### 8.1 Headings name their narrative role

Generic IMRAD labels and bare system names become titles that state the section's job in the argument:

- `Background` becomes `Technical Warm-Ups`
- `\section{\sys}` becomes `Our Solution: \sys`
- `Adversary` becomes `Threat Model` (use the standard security-paper term where one exists)

A colon is acceptable inside a section title; the §1 colon ban covers prose only.

Run-in `\heading{}` names stay short, about three words; five words is too long. Echoing the paper title is welcome.

All section and subsection titles use Title Case (IEEE style: capitalize words of four or more letters and all major words; articles, coordinating conjunctions, and short prepositions stay lowercase). Run-in `\heading{}` paragraph labels stay sentence case.

### 8.2 Keywords: Title Case, broad field terms

Title Case every keyword (`LLM API Router`). Keep the list short and built from field-recognizable area terms (`Agentic Security`, `Trusted Hardware`); drop paper-specific coinages (`faithful passthrough`) and near-synonyms of a term already present (`confidential computing` next to trusted hardware).

### 8.3 A bullet list gets a lead-in sentence

`\heading{Contributions} We summarise our contributions as below.` A short lead-in sentence, even a formulaic one, beats a bare heading followed directly by `itemize`; this overrides the cut-filler default at this one position. Leave his fresh edits as written during review rounds, including British spellings (`summarise`) in an otherwise American-English body; harmonize spelling paper-wide only as a deliberate camera-ready pass.

### 8.4 Floats and figure styling

- Keep consecutive argument paragraphs contiguous in the source; place the figure environment after the prose block it illustrates, not between two related paragraphs.
- Prefer single-column `figure` over `figure*` when the panels can stack vertically inside one column. After converting, update any left/right wording in the caption to the new geometry.
- Color-code contrast panels including their titles: a red family for the insecure side, a teal or green family for the secure side.
- Captions stay short, one identifying sentence plus at most a clause per panel; first drafts tend to run about twice too long. Methodology and interpretation live in the body; keep a number in the caption only when it appears nowhere else. Before cutting a caption, confirm the dropped methodology and numbers survive in the body or on the figure.
- Every table's header row is centered, one `\multicolumn{1}{c}{\textbf{...}}` per cell. With `@{}`-trimmed edge columns, the first header cell uses `\multicolumn{1}{@{}c}` and the last `\multicolumn{1}{c@{}}`, so the header keeps the same outer edges as the body rows.

### 8.5 Scheme interfaces list one algorithm per line

When a construction or hardware scheme is defined as a tuple of algorithms, display the tuple, then give each algorithm its own bullet line with its job. Do not run the per-algorithm semantics together in one prose paragraph.

### 8.6 Red `XXXX` is a co-author TODO

`\textcolor{red}{XXXX}` is his inline marker for "replace this text". Treat every red `XXXX` as an open action item to resolve in the next pass, and never leave one in a submitted PDF.

### 8.7 Parallel structures get uniform treatment

When one member of a parallel structure carries a feature, every member carries it. One contribution item with a section ref means every item gets its ref (and the now-duplicate ref in the trailing sentence goes). One annotated cross cell in a table means every cross cell gets a one-to-three-word reason. One Title Case heading means all headings. Check uniformity before he does.

### 8.8 Related-work comparison table

Full-width `table*` parked on the last body page, above the references. Rows are approach classes grouped by `\midrule`, 5 to 8 rows; `\sys` is bold in the last row, its name cell centered (`\multicolumn{1}{c}{\textbf{\sys}}`) while other rows' first cells stay left-aligned. Each row's cite list covers its entire category; consecutive numeric cites compress to ranges, so breadth is cheap. Cell judgments come only from claims the prose already makes; cells the prose does not support get `--`. Judgment dots use high-contrast shades of the paper palette: yes `green!75!black`, partial `orange!85!black`, no `red!70!black`. Building blocks and attack literature do not become rows, they are not competing approaches and take no values on the comparison columns.

### 8.9 Security definitions display brace-form bounds

Each security goal is a displayed formula `\Adv = \Pr\{\,\text{event}\,\} \le \negl(\lambda)` with the winning event written compactly inside the braces, not `Pr{event : steps}` or `Pr{G=1}`; the prose explanation follows the display. Guessing games use the distinguishing form `|\Pr\{\beta'{=}\beta\}-\tfrac12|`. Write `\negl(\lambda)` with the explicit argument in these displays.

### 8.10 Algorithms sit with their subsections

Each algorithm environment goes after the prose block that walks through it, placement `[t]` or `[!ht]`, so it renders inside or adjacent to its subsection rather than drifting. Prose cites algorithm lines in parentheses, `(line~\ref{...})` or `(lines~\ref{...}--\ref{...})`; label every line the prose names.

Steering: a `[t]` float whose source position is reached while a column is being typeset lands at the top of the next column, so the source position picks the landing column. When a full-width `table*` owns a page top, every `[t]` column float on that page glues directly under it; break the wall by switching the column float to `[!ht]` so it embeds after its walkthrough paragraph, or steer it to the next page's column top with `[t]` plus source position.

### 8.11 Word preferences

Avoid `itself` (`it itself` is always wrong, write `it issued`) and `together` or `together with` (use a plain list or `and`). `is itself a confidential router` becomes `is another confidential router`. Drop `itself` everywhere, including the abstract.

### 8.12 Conclusion stays minimal

About a third of a natural first draft, roughly four sentences: a blunt one-line problem verdict ("Malicious LLM API routers are dangerous."), the position or mechanism that enables the problem, `We propose \sys, <noun-phrase characterization>`, and `We empirically demonstrate <headline result> with low overhead`. Announcement verbs carry the paragraph; the thesis contrast does not reappear here. Details the abstract already states (overhead numbers, TCB size, no provider cooperation) do not reappear either. A closing generalization or transfer note (the "this extends beyond the studied setting" outlook) also stays out when the abstract's last line or the discussion already carries it, so the paragraph ends on the demonstrated result rather than a restated thesis. Keep only the single headline result, not a recap of mid-paper numbers; secondary findings the body already reports (a second elimination or reduction figure, an ablation delta) are cut here.

### 8.13 Triadic parallelism is capped

Runs of three parallel verb or noun phrases read as model prose ("rewrite tool calls, evade auditing, and read secrets"). Keep about 30 percent, only the load-bearing triads: announced enumerations ("three ends"), structural mappings (three goals to three games), factual artifact lists (three provider APIs, three transparency-log proofs). Rewrite the rest by splitting, 2-plus-1 grouping, absorbing one item into a hypernym, or deleting a redundant re-enumeration. A triple family recurring across sections is the strongest tell; keep one canonical instance and vary the others. Factual enumerations of concrete artifacts do not count toward the cap, and a sentence carrying two triads always gets rewritten.

### 8.14 No dangling words; fix by prose, not layout

No justified paragraph may end with a single-word last line, and very short two-word tails under about a quarter of the column width get the same treatment. The same rule covers page-break widows: a subsection's last one or two lines stranded at the top of the next column get condensed away, so the column opens with a heading or a full paragraph.

Fix by condensing prose inside the offending paragraph, never by touching format parameters. Each cut must remove at least the orphan's width or the break merely moves one word. Reliable fix shapes are clause deletion and two-word insertions near the paragraph tail; single-word insertions tend to be absorbed by justification. For a two-line bullet, lengthening the tail with true content often beats cutting. Shortening an overlong run-in `\heading{}` (8.1) is the cheapest dangler fix for its own paragraph.

After any pass that reflows text: rebuild, scan the built PDF's body pages for danglers, fix flags by prose, rebalance the references (8.15), and regenerate any venue-required PDF split last. Iterate, since fixes relocate breaks. A dangler scan runs on `pdftotext -bbox -f 1 -l <last body page> main.pdf /tmp/bbox.xml` plus a script over the XML that flags short last lines; the project keeps that script beside its own rulebook so the two migrate as one toolkit. Expect false positives from figure panel titles, table captions, headings at a column top, and itemize continuation lines; check the source before believing a flag.

### 8.15 Reference-list format

Every venue in `refs.bib` is the official full name plus its parenthetical abbreviation, as in `ACM SIGOPS/EuroSys European Conference on Computer Systems (EuroSys)`. No `Proceedings of the`, no ordinal, no year inside the booktitle; the year field prints separately. Journals get the abbreviation too (`TON`, `TIFS`). The abbreviation is the shortest field-common form, even when it truncates a word of the full name (`USENIX Security Symposium (USENIX Sec)`). Venues whose name is its own abbreviation (IEEE Access) and venues without a standard abbreviation stay as-is. Under IEEEtran, the last body page's two reference columns are balanced with `\IEEEtriggeratref{N}`; retune N after any bibliography change or body reflow that moves where the references start.

### 8.16 Author block: superscript indices, one affiliation line

Names sit on one comma-separated line with superscript indices (`First~Author$^{1}$, Second~Author$^{1}$, Third~Author$^{2}$`), then `\smallskip` and a single italic affiliation line joined by `$|$` separators (`$^{1}$\textit{University A} $|$ $^{2}$\textit{University B}`). Affiliation wording is minimal (`Independent`, not `Independent Researcher`); no `Member, IEEE` tags. Superseded blocks (an old author block, a `\thanks` footnote) stay commented out during review rounds and are removed only in a camera-ready cleanup pass.

### 8.17 Abstract: we-propose opener, direct capability list

- The solution paragraph opens `We propose \sys, <noun-phrase characterization>`, not a thesis-verb opener (`We make the router an attested trust boundary` was replaced this way). Evidence sentences use announcement verbs (`We show that ...`, `We empirically demonstrate ...`).
- The threat gets its standard field name (`application-layer man-in-the-middle`), introduced with a definition colon followed by the capability list. His own prose may use an in-sentence colon; the §1 ban governs our drafting, and his fresh edits stay as written (8.3).
- Attribution narration goes. No `A recent measurement study shows ...` framing, and no harness name in the abstract; state the attacker capabilities directly and close the problem paragraph with a short verdict (`Existing client-side defenses are evadable.`).
- A factual capability list may exceed three items when it maps to a real artifact or attack-class count (8.13's factual-enumeration exemption), and lists of system functions are given in full, not elided.
- Prefer mechanism-precise wording over shorthand (`plaintext leaves only toward destinations fixed by the measured image` over `an enclave-owned allowlist`).

### 8.18 Review-round conventions (first full read)

Six asks from his first full read of a draft, each worth applying before he asks:

- **A main algorithm frames the method.** One top-level procedure with its subroutines in a single algorithm float, Block-STM style, so the method section has a spine. The data-plane loop is a named subroutine, not prose. The float is the two-column `algorithm*` (the `float` package gives it for free): input and output lines span the full width, then two `minipage`s side by side with the line counter carried over so numbering runs on, and the source sits where the page before the section is typeset (if need be inside the previous section's file, with a comment saying so), since a `[t]` float lands on the page after the one where it is met; that puts it on the section's first page top. Pseudocode is set notation and assignments, not sentences (sets are differenced, edges are comprehensions, waits are predicates on a done flag); no circled stage marks, since the lines are numbered and the prose cites them as `(line~\ref{...})`. Every line the prose cites carries a label. Before the pseudocode is written, have a subagent re-derive each mechanism from the source with file and line numbers; one first draft here had four wordings the code contradicted.
- **Fewer schematics, hand-drawn.** Five TikZ method figures were too many; cut to three and redraw them in PowerPoint or OmniGraffle for him to touch up, with no shadows. The first author sees the drafts before he does.
- **Result-figure palette and captions.** Use a published top-venue palette (Paul Tol Vibrant here), keep one colour per entity across figures, and cut captions to one identifying sentence in plain words. Small single-column plots that belong to one research question stack as (a) and (b) panels of one figure at about 1.5in each, with the axes pinned to one rectangle so the panels align; a legend goes above the plot or in an empty corner, never on a curve.
- **No crowded tables.** A table that needs `\resizebox` has too many columns. Split the dense block into a figure and keep the rest as a narrow table. Table captions are title-only; any explanation goes in a one-line note under the bottom rule, typeset-checked to fit one line.
- **A positioning table in the introduction.** Full-width, rows are approach classes with their cite lists, columns are the decisions the method makes differently, cells are one-line phrases so every row is one line high, icons with a one-line legend where a cell holds a set. It lands on page 2 and a five-sentence paragraph walks the rows.
- **Appendix short and in-paper.** A little appendix after the references signals depth; a long one no longer does ("in the AI era, more pages do not add credit"). Keep the full proofs plus one supporting breakdown, compress mechanism restatement out of proofs, and make the last appendix page end with content rather than a lone table.

### 8.19 Abstract, his rewrite (worked example)

He replaced an abstract wholesale and left the draft version commented out above it. What his version does differently, each worth applying before he asks:

- **Open on the named prior systems with venue tags, not on a grand claim.** The field is established by naming who is in it. The trend narrative leaves the abstract and stays in the introduction.
- **State the premise as a condition and the problem as one challenge sentence.** No `We argue that`; the reframing arrives as the approach instead.
- **Explain the mechanism causally in plain words a non-specialist can follow.** Compressed jargon like "keeps read-after-write visibility while removing write-after-read false serialization" and "removes the false edges by construction" gets replaced by a sentence that says why.
- **No slogan close, no co-design cleverness.** `only because ... only because` constructions and "X replaces Y as the design center" go. The abstract ends on the most bounded number.
- **Name the corpus scale and the fairness condition in the abstract.** This overrides the no-corpus-in-the-abstract rule (§3.3, §8.17) for evaluation scale: keep the harness name out, put the scale in, and name the condition that makes the comparison fair.
- **Report the honest end-to-end number next to the headline**, and hedge precisely ("near the model's critical-path lower bound", not "reaches the optimum").
- **`We present \sys, which ...` is as acceptable as `We propose \sys, <noun phrase>`** (§8.17); do not rewrite one into the other.
- **Comment out, do not delete**, superseded prose during review rounds (as with author blocks, §8.16).

**Before** (the draft he replaced, three paragraphs, quoted):

> For modern blockchains, sequential transaction execution is the throughput ceiling, and parallel block execution is dominated by optimistic concurrency control, which speculates, validates reads, and rolls back on conflict. This assumes dependencies are unknowable before execution, an assumption now eroding. Solana requires declared access lists natively and EIP-7928 is bringing enforced block-level access lists to the EVM, so access metadata is becoming a protocol input. Once that metadata is precise, speculation redoes work the input already did and is costly on hot keys.
>
> We argue that under precise access sets, parallel block execution is an offline weighted-DAG scheduling problem. We propose Octopus, a schedule-first execution engine built from a list scheduler that produces a static $k$-core schedule, a multi-version cache that keeps read-after-write visibility while removing write-after-read false serialization, and access tables that bind every read and write to a version before execution. The cache needs no runtime validation because the access sets and the block order fix every read's source in advance, and the schedule works on a smaller graph because the cache removes the false edges by construction.
>
> In a REVM prototype, we show that Octopus removes 40.8\% of dependencies, reaches the dependency-bounded optimum by six cores, and delivers up to 4.4$\times$ execute-phase speedup over serial, ahead of a Block-STM baseline and an oracle-fed replay baseline. When access metadata is accurate, schedule-first execution replaces speculation as the design center.

**After** (his version, quoted):

> Parallel blockchain executors commonly discover transaction dependencies through runtime speculation (Block-STM, PPoPP'23; ParallelEVM, EuroSys'25) or pre-execution for later replay (BlockPilot, ICPP'23; Vegeta, NSDI'25). When precise per-transaction read and write sets are available before execution, these dependencies can instead be determined in advance. Yet existing executors still incur coordination overhead or unnecessary serialization. The challenge is to turn precise access sets into efficient parallel schedules.
>
> We present Octopus, which treats this task as offline scheduling of a dependency graph weighted by transaction execution costs. Its multi-version cache and precomputed access tables bind each read to the state version it must observe in block order and store each transaction's writes in separate versions. Later writes therefore cannot overwrite values that earlier reads still need, removing unnecessary reader--writer ordering constraints. A cost-aware scheduler uses the remaining dependencies and estimated execution costs to assign transactions to cores. Workers follow this static schedule without runtime conflict validation or re-execution, while preserving serial block semantics.
>
> We evaluate a REVM-integrated prototype using a corpus of 10{,}000 Base mainnet blocks containing 3.52M transactions. Octopus removes 40.8\% of dependency edges on average and produces schedules near the model's critical-path lower bound with six cores. It achieves up to 4.4$\times$ execute-phase speedup over serial execution and outperforms Block-STM and a replay baseline supplied with the same precise access sets. Including preparation and finalization, speedup is 2.8$\times$ at six cores without pipeline overlap.

Read the pair as one lesson: the problem paragraph names competitors and ends on a challenge sentence, the solution paragraph explains the mechanism causally, and the evidence paragraph gives corpus scale, the fairness condition, and the honest end-to-end number.

---

## 9. The Paper's Figure Pattern

Two figures carry structural duty in his group's papers, and everything else supports them. Apply this as the default figure plan before drawing anything.

**The introduction carries one small single-column figure that shows only the problem.** A motivating instance, a gap map, or a "why X?" contrast. It is cited from the introduction's thesis or contributions paragraph. It contains no mechanism: no module boxes from the design, no named component of the proposed system, no pipeline stage. A reader who has read only the abstract must understand it. Keeping mechanism out is what makes the design figure land later, and a mechanism preview here is the figure-level form of the overview-paragraph spoiler ban (§5).

**The design section opens with one full-width figure at the top of its first page.** Its named stages are the subsection spine: each stage in the figure has a subsection under it, in the same order and under the same name, so the figure doubles as the section's table of contents. It is cited from the section's first sentence, and its caption points back at the subsections. This is the same spine role the main algorithm plays for the method (§8.18); the figure and the algorithm float agree on the stage names.

**One running example, reused by every later method figure.** Build it from the paper's own semantics and keep it consistent across figures: same entities, same identifiers, same schedule or trace. A reader who follows the example in one figure should not have to reload context at the next. Three figures with three different examples cost the reviewer the same as three unrelated demos.

**Float placement is a source-position decision.** A `[t]` float lands on the page after the one being typeset when its source position is reached, so the source line for the design figure often has to sit in the *previous* section's file to land on the design section's first page. When it does, leave a LaTeX comment at the source line saying which section the float belongs to, or the next person moves it back. The same mechanics govern algorithm floats (§8.10) and full-width tables (§8.8).

**Everything else is supporting.** A figure that is neither of these two and backs no tagged claim does not earn its page. Result figures follow §8.18's palette and caption rules: one published top-venue palette, one colour per entity across the whole deck, captions cut to one identifying sentence in plain words.
