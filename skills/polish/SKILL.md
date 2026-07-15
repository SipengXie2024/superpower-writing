---
name: polish
description: |
  Polish prose in three passes: strip AI-writing tells, apply Strunk's rules
  for clarity, then hold every research claim to its evidence. Two modes: edit
  in place, or diff-first where the original is untouched until the user
  approves each change. Use when the user asks to 润色 / 改写 / 精修 / 打磨 a
  draft, or says "polish", "refine", "tighten", or "improve". Preserves meaning,
  numbers, citations, and [NEEDS-EVIDENCE] markers; never smooths an unsupported
  claim into a supported-sounding one.
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Polish

Polish runs three passes over a piece of prose, in this order:

1. **De-AI**, strip the marks of machine-written text (inflated symbolism,
   em-dash overuse, rule-of-three, promotional language, vague attribution,
   causal-tail chains, filler). Read `references/ai-tells.md`.
2. **Strunk**, cut needless words, prefer active voice, prefer the concrete
   over the abstract, keep related words together. Read `references/strunk.md`.
3. **Evidence-led wording**, for research and systems-paper prose, hold every
   comparison, magnitude word, and novelty claim to its evidence, and preserve
   unresolved-evidence markers. Read `references/evidence-led-wording.md`.

The order matters. De-AI works on texture: cadence, register, cliché, AI-brand
punctuation. It does not shorten sentences; it makes them sound less like a
chatbot. Run Strunk first and it will happily shorten AI-inflected prose into
shorter AI-inflected prose, clipped but still hollow. Strunk second lands its
cuts on real content instead of on decoration. Evidence-led wording runs last so
that neither earlier pass has quietly turned an unknown fact into an asserted one
while smoothing the prose.

The output is a single revised version, not an explanation, not a checklist of
tells you caught, unless the user asked for one or chose diff-first mode.

## Two modes: pick one before you start

**In place** is the default for a pasted paragraph, a single section, or any time
the user just wants the better version back. Apply the three passes and return the
revised text. If the input was a file, Edit it directly.

**Diff-first** (`--diff`, or when the user says "show me the diff first",
"每一处改动先给我看", "先给 diff 再决定", "don't touch the files until I approve")
never edits the original. You polish a copy, present each change as a unified diff,
the user accepts, rejects, or partially accepts each one, and only then do you
apply the approved subset. See the procedure below.

Pick diff-first by default, even unasked, when the document is close to submission
(a paper, rebuttal, or camera-ready spanning multiple section files). The stakes
are high enough that a silent over-edit is worse than the review overhead. Pick in
place for everything smaller.

This is the one place a strong model should not improvise the orchestration: do
not spawn parallel subagents to polish sections. Work the sections yourself, one
at a time. The per-change review is the real control gate, not fan-out speed.

## The preservation contract (both modes)

Polish preserves meaning at the claim level, not the sentence level. Every factual
claim, every hedge the author meant to keep, every named entity, citation, and
number must survive. Polish must not silently change the argument.

Byte-exact, never rewritten:

- All markup: `\cite{...}`, `\ref{...}`, `\label{...}`, captions, inline code,
  links, footnotes, `% claim: id` line comments. Rewrite only the surrounding
  prose.
- Every measured number, percentage, unit, and uncertainty statement. Do not
  round, restate, or recompute.
- Sentence-level claim boundaries. Do not collapse two `% claim:`-tagged
  sentences into one.
- **`[NEEDS-EVIDENCE]` markers.** This is the load-bearing invariant. The marker
  is an unresolved claim, not awkward prose. Preserve it verbatim, attached to the
  same claim. Never replace it with a vague hedge, an unrelated number, a section
  reference, or smoother, more confident wording. Never invent a comparator,
  measurement, citation, figure, or table to make the sentence read cleanly. If
  the evidence is absent, keep the marker or return a neutral description that does
  not make the unsupported claim.

When clarity conflicts with evidential precision, keep the precision. A smoother
sentence that converts an unknown fact into an asserted fact is a regression, not
a polish. The third pass (`references/evidence-led-wording.md`) is the detailed
contract for `faster`, `significant`, `efficient`, `scalable`, and `novel`; run it
on research prose and honor it.

When does the evidence pass fully engage? When `.writing/metadata.yaml` has
`writing_profile: systems`, when the input is a LaTeX research manuscript, or when
the user says the prose is a paper. For an email or a blog post it is a light
touch, but the `[NEEDS-EVIDENCE]` rule above holds for any input that carries the
marker.

## Canonical-term table (consistency anchor)

Before polishing anything longer than a paragraph, build a canonical-term table.
List each load-bearing term once with its single preferred surface form, then hold
every rewrite to that form. This stops the de-AI pass from synonym-cycling a fixed
term and stops the Strunk pass from collapsing a precise term into a bland one. See
`skills/_shared/core/terminology-ledger.md` for the format. For a short input a
mental table is enough; for a section or longer, write it down so it survives
chunking.

## Diff-first procedure

### Step 1 : Find the sections, skip stubs

For a LaTeX manuscript, list the section files in deterministic order (default
`.writing/manuscript/*.tex`). Skim each before starting. A stub is a tiny file
whose body is a `% redirect ...` comment or an `\input{...}` shim; skip it,
polishing it is wasted work. If the user named specific sections, do only those.

Proceed decisively when discovery is unambiguous. If the path is named or `ls`
returns a clear set of section files, state the list and move on. The per-change
review is the control gate; a redundant "shall I proceed?" just adds friction. Ask
only when discovery is genuinely ambiguous.

### Step 2 : Polish a copy, never the original

Work section by section. For each, copy the original, run the three passes on the
copy, and generate a unified diff against the original. A convenient home for the
copies and diffs is `.writing/polish-patches/` (create it if missing), but for a
single pasted section you may hold the diff in memory and present it inline. The
invariant is only that the original file stays byte-unchanged until Step 4.

If a project style file (`.claude/CLAUDE.md`, `AGENTS.md`) sets prose rules, treat
them as hard constraints that override default polish heuristics, and surface any
rule the polish would have violated.

### Step 3 : Walk the diffs with the user, one change at a time

Present a short per-section summary (line count, change count), then walk every
change individually. Do not dump a long diff all at once.

Format for each change:

````
### Change N (paragraph location, brief subject)

```diff
- <full original prose, no ellipsis>
+ <full polished prose, no ellipsis>
```

判断: <one to three sentences: what changed and why>.
建议: 接受 / 拒收 / 部分接受 (具体哪些子改动), <reason>
````

Hard rules for this step:

- **Always use triple-backtick `diff` fenced blocks.** The terminal renders `-`
  red and `+` green; that visual signal is doing real work.
- **Never use `...` ellipsis** in the diff payload. The user needs the full prose
  to judge context. Show it all, even when long.
- **Walk every change,** not just the surprising ones. The user is doing the
  audit; your job is to present, not to filter silently.
- **Classify each as accept, reject, or partial.** Partial-accept is common in a
  long change where the polish made four sub-edits and only two are clean; spell
  out which sub-tokens to take.

### Step 4 : Apply the approved subset

After the user approves, apply via `Edit` with exact byte-strings. Do not
bulk-apply via `replace_all` unless the change is genuinely the same string
everywhere. If `Edit` rejects an `old_string`, the file diverged from the diff base
(a linter or the user touched it mid-review). Re-Read, find the surviving form, and
adjust. Never overwrite user edits silently.

Unapproved suggestions stay frozen on disk for later review. Report a short final
tally: sections processed, changes applied, rejected, partially accepted.

## Recurring over-edits: reject or accept by default

These patterns recur across manuscripts. In diff-first mode, flag them; in-place,
just do not make the rejected ones.

**Reject by default:**

- **Stripped parenthetical limiters at a term's first use.** The de-AI pass reads
  parens as defensive, but they often set the limited quantifier of a defined
  term. `Naive (per-hash) AOT` becoming `Naive per-hash AOT` loses the scope.
- **Modifier reordering that flips the argumentative subject.** When a modifier
  moves to a different head, check the head is still the same noun. If not, reject.
- **Deletion of editorial qualifiers that bind downstream.** "and most consequential
  in production", "above all", "crucially", "the central case" are often
  load-bearing signals the next paragraph relies on. If it does, keep them.
- **Semicolon-merge of two definition lines.** When two short sentences introduce a
  defined term, the rhythm break is intentional. Keep them separate.
- **Register downgrade.** Swapping an academic copula for a breezy phrasing (`is
  part of` becoming `falls out of`). Keep the original.

**Accept by default:**

- **Removal of self-deprecating qualifiers** around real design choices (`as an
  extension`, `albeit auxiliary`, `not a central experimental claim`), especially
  when a later section states the trade-off confidently.
- **Active-voice conversions that preserve meaning** (`is X by Y` to `Y X-es`).
- **Defensive-negation removal** where the negation guards against a critique no
  reviewer would raise (`rather than by an arbitrary modeling compromise`).

## When to use this skill

- "polish this", "clean this up", "make this tighter", "improve this paragraph".
- "润色", "打磨", "精修", "改写", "改得更好", "让这段更自然", "帮我改下这段".
- "整篇润色但每一处改动先给我看" (diff-first over a whole manuscript).
- A pasted draft with an implicit ask ("what do you think?", "thoughts?") when the
  prior turn made clear the user wants a revised version.
- Any request to edit prose for readability rather than factual correctness.

## When NOT to use this skill

- Factual correction, translation, summary, or structural rewrite (reorganize
  sections, change the argument, add or remove content). Those are different jobs.
  Polish preserves meaning.
- LaTeX, code, tables, or bibliography fixes. Polish is for prose.
- A single sentence the user wants nudged. The three-pass machinery is overkill;
  edit inline and say you did.
- The user already rejected a de-AI or Strunk change earlier in the conversation.
  Respect that; do not re-apply it silently.
- "Don't change meaning, just fix grammar." That is a grammar pass, not a polish.

## Edge cases

- **Mixed Chinese / English prose.** The passes apply cleanly to English. For
  Chinese, keep the same spirit (cut AI tells, cut needless words, prefer active
  voice, prefer concrete nouns) rather than mechanically applying English
  punctuation rules. Never translate or romanize either language.
- **Very long input.** Process one logical chunk at a time (paragraph or
  subsection). Running all three passes over thousands of words in one shot
  produces uneven quality, and chunking preserves headings, lists, and code blocks
  by touching only prose.
- **Register mismatch after the de-AI pass.** If it sounds too casual for the
  document (it stripped academic register from a Methods section), dial it back on
  the next attempt rather than letting Strunk compound the drift. Prefer one good
  polish over iterative grinding.
- **Academic input is often near-identity.** A clean systems-paper paragraph may
  come back unchanged, and that is the correct result. Hyphenated compounds
  (`cold-cache`, `per-contract`) and scholarly verbs (`shows`, `preserving`) are
  load-bearing; if a pass touched them, the preservation contract restores them.
- **A polish that renames a `\subsection{...}` or section title.** That is a
  semantic edit, not a stylistic one. Surface it separately with explicit
  confirmation; never bundle it into a prose batch.

## Output philosophy

The polished text is the deliverable. The user does not need to see the machinery.
In place, return the revised prose and nothing else, unless one short note earns
its place (for example, "I kept the hedge in the third sentence because it carries
the sample-size claim"). Meta-commentary about which tells you removed does not
earn its place.

In diff-first mode, keep user-facing text focused on the change under review: which
one, what changed, accept / reject / partial, a one-sentence reason. Do not narrate
the pipeline or the patterns being filtered.

If a pass produced a result you are not confident in, say so briefly so the user
can spot-check. Do not hedge for the sake of hedging, but be honest about
low-confidence edits.
