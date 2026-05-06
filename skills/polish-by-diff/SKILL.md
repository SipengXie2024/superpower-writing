---
name: polish-by-diff
description: |
  Multi-section manuscript polish via parallel subagents that produce unified
  diffs instead of in-place edits. Main agent walks the user through each
  hunk for accept / reject / partial-accept before any change lands. Use when
  polish spans multiple section files, when project style rules in CLAUDE.md
  or AGENTS.md must override default polish heuristics, or when the document
  is high-stakes (submission, rebuttal, camera-ready). Triggers include
  "polish each section", "polish the whole paper", "polish but show me the
  diff first", "整篇润色", "逐章polish", "diff-mediated polish".
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
  - Agent
  - AskUserQuestion
---

# Polish by Diff

## What this skill does

`polish-by-diff` turns the destructive in-place behavior of the `polish` skill
(humanizer + writing-clearly-and-concisely) into a review-and-apply pipeline.
The original manuscript files are never edited until the user explicitly
approves each change. Parallel subagents do the polish work in isolation;
the main agent collects diffs, walks the user through them, and only then
applies the approved subset.

The pipeline has four stages:

1. **Discovery** — list the section files, skip stubs.
2. **Parallel dispatch** — one subagent per section, all in a single tool-call
   message. Each subagent runs polish on a *copy*, never on the original,
   and writes a unified diff to disk.
3. **Diff-review** — main agent reads each diff, presents it to the user in
   triple-backtick `diff` fenced blocks, classifies each change as accept,
   reject, or partial with a one-sentence judgment, and surfaces project
   style-rule violations the polish smuggled in.
4. **Application** — main agent applies the approved subset via `Edit`, then
   verifies via `grep -n` that polish trigger phrases were eliminated.

The output is the manuscript itself, modified in line with user-approved
edits. Unapproved suggestions stay frozen on disk in `.writing/polish-patches/`
for later review.

## Why this skill exists

The `polish` skill is aggressive by design — humanizer strips AI tells and
Strunk cuts needless words. Both passes are correct most of the time. On long
academic-prose sections (200+ words per paragraph), each polish run typically
returns 4 to 18 paragraph-pair replacements. Empirically, around 70 to 90
percent are accept-by-default; the rest split between reject (over-edit) and
partial-accept (one good token in a hunk that otherwise breaks something).

Running polish in-place on a multi-section manuscript without that filter
produces several recurring regressions:

- Stripped parenthetical limiters that establish term scope at first use
  (for example, `Naive (per-hash) AOT` becoming `Naive per-hash AOT`).
- Modifier reordering that flips the argumentative subject of a sentence.
- Deletion of mid-sentence editorial qualifiers that bind to a downstream
  argument (for example, `Third, and most consequential in production`).
- Semicolon-merge of two short sentences when one is a term-definition
  statement (the rhythm break is intentional in definition paragraphs).
- Register downgrades that swap neutral academic copulae for breezy
  phrasings (for example, `is part of` becoming `falls out of`).

The user wants these caught before they land. This skill is the workflow
that catches them.

## When to use this skill

Trigger whenever the request implies polishing a multi-section document
*and* the user wants visibility into what changes:

- "Polish each section of my paper but show me the diff first"
- "整篇polish一下，但每一章给我汇报 diff 再决定改不改"
- "Polish 全文，结果以 unified diff 形式给我"
- "我想看到每一处改动再决定接受还是拒绝"
- "Run polish on the whole manuscript but don't touch the files until I approve"
- The user is working on a paper close to submission and asks for any kind
  of "polish", "润色", or "打磨" — the stakes are high enough that
  diff-review is the safer default even when the user did not ask for it
  explicitly.

## When NOT to use this skill

- Single-paragraph polish — call `superpower-writing:polish` directly and edit
  inline. The diff-review machinery is overhead.
- Single-file polish for a non-manuscript artifact (commit message, README
  paragraph, email) — call `superpower-writing:polish` directly.
- Translation, factual correction, structural rewrite, or argument
  reorganization — those are different jobs.
- The user already gave a clear directive to apply polish in-place. Respect
  that.

## Inputs the skill needs

- A directory of manuscript section files. Default convention:
  `.writing/manuscript/<NN>_<name>.tex`. Other layouts (numbered Markdown
  files in `chapters/`, etc.) work as long as each section is a separate
  file.
- An output directory for diffs and polished copies. Default:
  `.writing/polish-patches/`. Create it if missing.
- Optionally, a project style-rule file (`.claude/CLAUDE.md`, `AGENTS.md`,
  or both). Pass the relevant style rules into each subagent prompt as
  hard constraints.

## The procedure

### Step 1 — Discover sections, skip stubs

List section files in deterministic order. For LaTeX manuscripts under
`.writing/manuscript/`:

```bash
ls .writing/manuscript/*.tex
```

Open and skim each file before dispatching. A stub file is a small file
(say, under 200 bytes) whose body is a `% redirect ...` comment or a
`\input{...}` shim. Skip those — polishing them is wasted budget.

If the user named specific sections (`only the introduction and discussion`),
respect that and only dispatch for those.

### Step 2 — Create output directory

```bash
mkdir -p .writing/polish-patches
```

### Step 3 — Dispatch parallel subagents

Spawn one `general-purpose` (or comparable) subagent per section, **all in a
single tool-call message** so they run concurrently. Use the prompt template
below.

#### Subagent prompt template

The prompt must be self-contained because the subagent inherits no
conversation context. Fill in the placeholders.

```
You are polishing one LaTeX section of an academic paper.
**Do NOT modify the original file.** Your sole deliverable is a unified
diff written to a specified path.

## Inputs
- Original (read-only): {ABSOLUTE_PATH_TO_ORIGINAL_TEX}

## Outputs
- Polished version: {ABSOLUTE_PATH_TO_POLISHED_COPY}
- Unified diff: {ABSOLUTE_PATH_TO_DIFF}

## Procedure
1. Read the original.
2. Copy it to the polished path: `cp <original> <polished>`.
3. Invoke the `superpower-writing:polish` skill on the polished file. The
   polish skill runs two passes: first `superpower-writing:humanizer` to
   strip AI-writing tells, then
   `superpower-writing:writing-clearly-and-concisely` to apply Strunk's
   rules. Edit only the polished copy, never the original.
4. Generate the diff: `diff -u <original> <polished> > <diff_path>`.
5. Verify the original is byte-unchanged (capture md5 or mtime before and
   after; report both).

## Constraints (from project CLAUDE.md / AGENTS.md — must respect)
{INSERT_RELEVANT_PROJECT_STYLE_RULES_HERE}

Common ones to forward verbatim:
- No em-dashes (`---`, `--`, `—`) and no in-sentence colons in prose.
  Substitute with commas, sentence breaks, or "including" / "so".
  Only allowed colon: lead-in to a LaTeX `\begin{itemize}` list.
- No code-artifact names in reviewer-facing prose (no CamelCase
  identifiers, snake_case identifiers, hex literals, file paths, or
  function/struct names) except in §implementation, where named
  components are appropriate.
- No dataset name (for example, "Base mainnet") in argumentative or
  thesis sentences. Reserve dataset name for canonical measurement-setup
  or external-validity points.
- State design intent in goal-form, not precondition-form. Defensive
  negations should be deleted; substantive disambiguations kept.
- Preserve all LaTeX commands, citations, labels, refs, captions, and
  `% claim:` line comments byte-exact. Polish prose only.
- Preserve every measured number, percentage, and unit exactly. Do not
  round, restate, or recompute.
- Preserve sentence-level claim boundaries. Do not collapse two
  `% claim:`-tagged sentences into one.
- {SECTION_SPECIFIC_RULES_IF_ANY}

## Reporting
Reply with under 100 words: confirm the diff path, line counts (added /
removed), and any sentences you chose NOT to alter and why
(terminology lock, claim-evidence boundary, load-bearing hedge).
Do not paste the diff content; the main agent will read it from disk.
```

#### Section-specific rule snippets to inject

| Section | Inject as `{SECTION_SPECIFIC_RULES_IF_ANY}` |
|---|---|
| Abstract | "Dataset name may appear once if numbers are reported. Preserve every measured number byte-exact." |
| Intro | "Avoid roadmap signposts ('this section first describes X, then Y'). Preserve thesis sentences." |
| Background | "Workload chapters report properties independent of the proposed system. No mechanism premises, no system-defined metrics." |
| Design | "State design intent in goal-form. Mention-and-forward to numeric findings; do not dump quantitative results. Avoid self-deprecating qualifiers ('an extension', 'albeit auxiliary')." |
| Implementation | "This is the ONE place where named code components are appropriate. Each component named once + defined, then referred to descriptively. Do not strip these names." |
| Evaluation | "This is one of the canonical places where the dataset name is appropriate. Body should be interpretive prose; dense numbers belong in figures, tables, or captions." |
| Discussion | "Tone is neutral-positive. Prefer 'scope', 'transfer', 'follow-on evaluation', 'natural extension' over apologetic limitation language. One paragraph per subsection is the default rhythm." |
| Related work | "Stay at the increment-articulation level. Do not change which works are cited or the order/grouping of citation clusters." |
| Conclusion | "Should not introduce new claims, datasets, numbers, or mechanism details. Polish wording only." |

### Step 4 — Receive subagent reports

Each subagent returns a short status (diff path, hunk count, sentences kept).
Do not Read or tail the subagent transcripts; trust the completion message.

After all subagents finish, verify the diff files exist and the originals
are byte-unchanged:

```bash
md5sum .writing/manuscript/*.tex
ls -la .writing/polish-patches/*.diff
wc -l .writing/polish-patches/*.diff
```

Compare md5 hashes against pre-dispatch values if you captured them. Any
changed original is a contract violation — flag the offending subagent,
restore the original from git or the polished copy's pre-image, and re-run
that section.

### Step 5 — Walk the diffs with the user, one section at a time

For each section's diff, present a short summary first (line count, hunk
count), then walk through every hunk individually. **Do not show the diff
file all at once for long sections** — that overwhelms the review.

Format for each hunk:

````
### Hunk N (paragraph location, brief subject)

```diff
- <full original prose, no ellipsis>
+ <full polished prose, no ellipsis>
```

判断: <one to three sentences explaining what changed and why>.
建议: 接受 / 拒收 / 部分接受 (具体哪些子改动) — <reason>
````

Hard rules for this stage:

- **Always use triple-backtick `diff` fenced blocks**, not generic code blocks
  or plain text. The terminal renders `-` red and `+` green; that visual
  signal is doing real work.
- **Never use `...` ellipsis** in the diff payload. The user explicitly needs
  to see the full prose to judge context. Even if the prose is long, show
  it all.
- **Walk through every change**, not just the surprising ones. The user is
  doing the audit; main-agent's job is to present, not to filter silently.
- **Classify into accept / reject / partial-accept.** "Partial accept" is
  common in long hunks where polish made 4 sub-edits and only 2 are clean —
  spell out which sub-tokens to take.

#### Recurring patterns to flag and reject by default

Lift these from the polish session that produced this skill — they have
been observed in multiple papers:

- **Stripped parenthetical limiters at first-use term definition.** Polish
  treats parens as "defensive parentheticals" but the parens often establish
  the limited quantifier of a defined term. Reject.
- **Modifier reordering that flips the argumentative subject.** When
  polish moves a modifier to a different head, check whether the head is
  still the same noun. If not, reject.
- **Deletion of editorial qualifiers that bind to downstream argument.**
  Phrases like "and most consequential in production", "above all",
  "crucially", or "the central case" are often load-bearing argumentative
  signals. Check whether the downstream paragraph relies on them. If yes,
  reject the deletion.
- **Semicolon-merge of definition lines.** When two short sentences
  introducing a defined term are joined with a semicolon, reject. The
  rhythm break is intentional.
- **Register downgrade.** When polish swaps an academic copula for a
  breezy phrasing, reject and keep the original.

#### Recurring patterns to accept by default

- **Removal of self-deprecating qualifiers around real design choices.**
  When polish strips `as an extension`, `albeit auxiliary`, `not a central
  experimental claim`, accept it — especially when the discussion section
  already articulates the trade-off confidently. Optionally propose a
  forward-reference into the discussion section so scope visibility is
  preserved.
- **Active-voice conversions that preserve meaning.** `is X by Y` to
  `Y X-es`. `is keyed by Z and stores W` to `, keyed by Z, stores W`.
- **Defensive negation removal.** When polish deletes "rather than by an
  arbitrary modeling compromise" — that's defensive against a critique
  the reviewer would never have raised. Accept.

### Step 6 — Apply the approved subset

After the user approves edits, apply via `Edit` with exact byte-strings.
Do not bulk-apply via `replace_all` unless the change is genuinely the
same string everywhere — single-spot Edits are safer.

Common pitfall: the user-modified state of a file may diverge from the
diff base if the user edited the file mid-review (linters, IDE auto-save,
manual touchup). If `Edit` rejects an `old_string`, re-Read the file,
identify the surviving form of the original prose, and adjust the
`old_string` to match. Never overwrite user edits silently.

### Step 7 — Verify polish triggers were eliminated

After applying, grep for the polish trigger phrases that should no longer
appear:

```bash
grep -n "is implemented by\|today's\|is shaped by\|What X supplies separately is Y" .writing/manuscript/*.tex
```

The exact list depends on the polish hunks. Build a regex from the
specific `-` lines that the user accepted and confirm none survive in
the final manuscript.

If a partial-accept left a hybrid form (some polish tokens taken, others
left at original), grep for both forms and confirm the surviving form
matches the user's intent.

### Step 8 — Report final state

A single short summary in user-facing text:

- Sections processed: N
- Hunks applied: M (across N sections)
- Hunks rejected: K
- Hunks partially accepted: J
- Patches preserved on disk for re-review: `.writing/polish-patches/`

That is the end of the skill.

## Project-style-rule integration

This skill is most useful when paired with a project's `CLAUDE.md` or
`AGENTS.md` style rules. Common ones to surface in subagent prompts:

- Punctuation: em-dash and in-sentence colon bans.
- Term economy: each term defined at one canonical position.
- Argument form: goal-form vs precondition-form; defensive-negation deletion
  vs substantive-disambiguation preservation.
- Section responsibility: which numbers belong in which section.
- Code-artifact-name discipline: which sections allow named components and
  which do not.
- Opcode mnemonic case (or analogous domain conventions): for example,
  EVM opcodes are uppercase project-wide.

When the user adopts a project-wide convention on one section during the
review (for example, capitalizing all opcode references), propagate it
to all sections in the same edit pass rather than asking section by
section. Internal inconsistency between adjacent paragraphs is worse than
slight scope creep.

## Edge cases

**File modified mid-review.** If `Edit` rejects an `old_string`, the user
or a linter probably touched the file. Re-Read, locate the current prose,
adjust the `old_string`. Never assume the file is in the state the diff
was generated against.

**Subagent returns no diff.** Either the section was already clean (rare on
manuscripts being polished) or the subagent failed silently. Read the
empty diff file to confirm; if empty, re-dispatch with a more directive
prompt.

**Subagent returns a diff but the original was modified.** Contract
violation. Restore the original from git (`git checkout HEAD -- <path>`)
or from the polished copy's pre-image (the polished file's first byte
sequence before its own polish edits). Re-dispatch.

**User wants to apply all hunks without per-hunk review.** Honor that, but
ask once whether they want a final summary of which hunks landed.
Auto-applying is faster but loses the audit surface that justifies the
skill in the first place.

**Polish suggested a section title rename.** Section title changes are
semantic, not stylistic. Surface separately with explicit user
confirmation. A polish hunk that renames a `\subsection{...}` should
be classified as a semantic edit, never bundled into a "polish prose"
batch.

**Long diffs (>200 lines).** Split into review chunks of at most ~10 hunks
per response. The user's audit attention is the bottleneck.

## Output philosophy

The polished manuscript is the deliverable. The diff files on disk are the
audit trail. User-facing commentary should focus on:

- Which hunk we are looking at.
- What changed.
- Whether to accept, reject, or partially accept.
- A one-sentence reason.

Avoid meta-commentary about the polish process, the parallel subagents, or
the over-edit patterns being filtered. The user does not need to see the
machinery; they need to see and decide on prose.
