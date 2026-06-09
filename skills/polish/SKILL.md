---
name: polish
description: |
  Two-pass prose polish: first `superpower-writing:humanizer` strips
  AI-writing tells, then `superpower-writing:writing-clearly-and-concisely`
  applies Strunk's rules for clarity and concision. Use when the user asks
  to "polish", "润色", "打磨", "refine", "clean up", "improve", or "rewrite"
  prose, or hands over a draft with an implicit ask for a stronger version
  ("make this better", "把这段话改好"). The two-pass discipline beats a
  single judgment-call rewrite. Skip for factual fixes, translations,
  structural rewrites, or single-sentence tweaks.
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Skill
  - AskUserQuestion
---

# Polish

## What this skill does

Polish runs a short pipeline over a piece of prose:

1. **Humanize** — invoke the `superpower-writing:humanizer` skill to remove
   AI-writing tells (em-dash overuse, inflated symbolism, rule-of-three,
   promotional language, formulaic connectors, uniform sentence length, AI
   vocabulary, throat-clearing openers, etc.).
2. **Sharpen** — invoke the `superpower-writing:writing-clearly-and-concisely`
   skill (Strunk's rules, vendored from `elements-of-style`): cut needless
   words, prefer active voice, prefer concrete over abstract, keep related
   words together, use parallel construction only when the ideas are parallel.

The output is a single revised version of the prose, not an explanation, not a
diff, not a checklist — unless the user explicitly asks for one.

## Why two passes, and why this order

The two skills attack different problems. Running them separately and in order
matters.

- **Humanizer first** is about *texture*: cadence, register, cliché, AI-brand
  punctuation. It does not make sentences shorter; it makes them sound less like
  a chatbot. If you run Strunk first, Strunk will happily shorten AI-inflected
  prose into *shorter AI-inflected prose* — clipped, but still hollow.
- **Strunk second** is about *discipline*: every word earns its place, verbs do
  work, specificity beats abstraction. Once the humanizer pass has killed the
  tells, Strunk's cuts land on real content instead of on decoration.

Doing them in a single pass tends to produce a watered-down rewrite that
addresses neither problem fully. The two-pass discipline is the point.

## When to use this skill

Trigger whenever the user asks for any of the following, in English or Chinese:

- "polish this", "clean this up", "make this tighter", "improve this paragraph"
- "润色", "打磨", "改得更好", "让这段更自然", "帮我改下这段"
- A pasted draft with an implicit ask — for example, the user shares a
  paragraph and says only "what do you think?" or "thoughts?" while the prior
  turn made clear they want a revised version.
- Any request to edit prose for *readability* rather than for factual
  correctness.

## When NOT to use this skill

- The user asks for a *factual* correction, a translation, a summary, or a
  structural rewrite (reorganize sections, change the argument, add/remove
  content). Those are different jobs. Polish preserves meaning.
- The user asks for LaTeX, code, tables, or bibliography fixes. Polish is for
  prose.
- The text is a single sentence and the user only wants a small tweak. The
  two-pass machinery adds more ceremony than value. Edit inline.
- The user has already rejected a humanizer or Strunk pass earlier in the
  conversation — respect that and don't re-apply it silently.

## Inputs the skill accepts

Polish handles whatever the user hands over:

- Prose pasted directly into the chat
- A file path (Read it first)
- A selection the user references implicitly ("this paragraph", "the intro")
- Mixed Chinese / English prose — both humanizer and the Strunk skill apply
  cleanly to English; for Chinese, keep the same *spirit* (cut AI tells, cut
  needless words, prefer active voice, prefer concrete nouns) rather than
  mechanically applying English punctuation rules

If the input is ambiguous (e.g., a long document and the user said only
"polish this"), ask once with `AskUserQuestion` which section to polish rather
than guessing and burning a full pass on the wrong text.

## The procedure

Follow these steps exactly. Do not skip, reorder, or merge them.

### Step 0: Build a canonical-term table (consistency anchor)

Before polishing, build a canonical-term table so both passes keep terminology stable. List each load-bearing term once with its single preferred surface form, then hold every rewrite to that form. This stops the humanizer pass from synonym-cycling a fixed term and stops the Strunk pass from collapsing a precise term into a bland one. See `skills/_shared/core/terminology-ledger.md` for the ledger format and rules. For a short input, a mental table is enough; for a section or longer, write the table down so it survives chunking.

### Step 1 — Capture the source text

Get the exact text to polish. Read from a file if needed. If the user gave a
file path, Read it and extract the relevant region. Keep the original around
unchanged until the end — the user may want to diff against it.

### Step 2 — Run the humanizer pass

Invoke the `superpower-writing:humanizer` skill via the Skill tool with the
source text as input. Ask humanizer to return revised text, not a report.
Save the result as `pass_1_humanized` (mentally — no need to write a file
unless the user wants intermediate artifacts).

If humanizer surfaces a question (e.g., "this phrase is ambiguous, keep or
cut?"), resolve it with a minimal edit rather than bouncing the question to the
user. The user asked for a polish, not a committee.

### Step 3 — Run the clarity/concision pass

Invoke `superpower-writing:writing-clearly-and-concisely` (Strunk's rules,
vendored from `elements-of-style`) with `pass_1_humanized` as input. Ask it
to produce a final revised version applying Strunk's rules. Save as
`pass_2_sharpened`.

If this pass wants to cut something that carries real meaning (a hedge the
author clearly wanted, a technical term, a named entity), keep it. Strunk is a
tool, not an oracle — concision is a means to clarity, not a value in itself.

### Step 4 — Verify the meaning is preserved

Compare `pass_2_sharpened` against the original text at the claim level, not
the sentence level. Every factual claim, every hedge the author meant to keep,
every named entity, every citation, every number — all must survive. If a
claim was lost or weakened, restore it. Polish must not silently change the
argument.

### Step 5 — Return the result

Default output format:

```
**Polished version:**

<pass_2_sharpened verbatim>
```

Nothing else. No explanation of what you changed, no list of tells you caught,
no self-congratulation. If the user wants a diff or a change log, they will
ask.

If the user set up the request with a specific frame (academic, rebuttal,
email, marketing copy, docstring), check one thing before returning: does the
register still fit? A Strunk pass will sometimes strip academic hedging too
aggressively for a peer-review context. Restore register-appropriate hedging
before returning.

## Self-Check

Before returning the polished text, confirm each item. Tags mark who can
confirm it. `[inspection]` the agent can confirm this from its own output;
`[attestation]` the agent ran the procedure but the user owns final
confirmation; `[user-attest]` a user-side rule the agent cannot confirm.

- [inspection] A canonical-term table exists and every load-bearing term keeps its single preferred surface form across the output (no synonym cycling, no bland collapse).
- [inspection] Both passes ran in order: humanizer first, then writing-clearly-and-concisely.
- [inspection] Every markup token, claim tag, citation, named entity, and number from the input survives verbatim in the output.
- [attestation] Meaning is preserved at the claim level; no factual claim or author-intended hedge was lost or weakened.
- [attestation] The register still fits the document's frame; register-appropriate hedging was restored where a Strunk cut stripped it.
- [user-attest] Any low-confidence override of an upstream pass was surfaced briefly so the user can spot-check it.

## A worked example — what each pass does

**Input** (AI-flavored marketing prose):

> In today's rapidly evolving technological landscape, observability stands as a
> testament to the maturity of modern engineering—nestled at the intersection of
> reliability and developer productivity, it marks a pivotal moment in how teams
> identify, diagnose, and remediate production incidents.

**After Step 2 — humanizer pass** strips inflated symbolism (`testament`,
`pivotal moment`), promotional language (`nestled at the intersection`),
em dashes, and the rule-of-three (`identify, diagnose, and remediate`):

> Observability has become core infrastructure for modern engineering. It
> changes how teams handle production incidents.

**After Step 3 — Strunk pass** cuts the copula (`has become` → `is now`)
and tightens the second sentence:

> Observability is now core engineering infrastructure. It changes how teams
> handle production incidents.

**Step 4 verify** confirms the claim ("observability changed how engineers
handle incidents") survives. No citation, named entity, or number was in the
original to lose. **Step 5** returns the two-sentence result, nothing else.

### Other humanizer cuts the example does not show

The worked example above demonstrates four cuts. The humanizer pass also
strips the following patterns — apply them whenever they appear, not only
when they happen to match the example:

- **Vague attribution** — "Industry observers report that…", "Critics argue…",
  "Experts believe…". Either name the source or drop the framing entirely.
- **False ranges** — "from hobbyist experiments to enterprise rollouts, from
  solo developers to cross-functional teams". The two endpoints are not on a
  meaningful scale; collapse to a plain claim.
- **Formulaic challenges** — "Despite challenges typical of X, the ecosystem
  continues to thrive." Either name a real obstacle and what was done about
  it, or drop the sentence.
- **Generic positive conclusions** — "The future looks bright. Exciting times
  lie ahead." These say nothing; cut them.

If your input has any of these, treat them as load-bearing tells and cut them
in Step 2 even though they are not in the worked example.

### Counter-example — academic input should be near-identity

**Input** (paragraph from a systems paper):

> The results show that compiling at family granularity cuts cold-cache
> compile time while preserving per-contract dispatch identity.

**Output** (correct polish — both passes recognize academic register):

> The results show that compiling at family granularity cuts cold-cache
> compile time while preserving per-contract dispatch identity.

The hyphenated compounds (`cold-cache`, `per-contract`) are domain-specific
and load-bearing; the scholarly verbs (`show`, `preserving`) are part of the
contract with the reader. Polish should return the input unchanged here. If
either pass touched these tokens, the verify step in Step 4 should restore
them.

## Edge cases and judgment calls

**Very short input (one or two sentences).** Run the two passes anyway, but
skip the intermediate artifacts. For one sentence, a full two-pass cycle is
usually overkill — consider editing inline and telling the user you did so.

**Very long input (a full section or chapter).** Process one logical chunk at
a time (paragraph or subsection). Running both passes over many thousands of
words in one shot produces uneven quality. Chunking also lets you preserve
structural markers (headings, lists, code blocks) by touching only the prose.

**LaTeX / Markdown with markup.** Preserve all markup exactly: `\cite{...}`,
`\ref{...}`, `% claim: ...` line comments, inline code, links, footnotes. Only
rewrite the surrounding prose. If in doubt, do not touch it.

**Claim-tagged scientific prose.** If the input has `% claim: id` comments
(superpower-writing convention), treat those comments as immovable anchors.
The claim tag must remain attached to the same sentence it was anchored to
originally.

**Register mismatch between the two passes.** If humanizer's output sounds
*too* casual for the document (e.g., it stripped academic register out of a
methods section), that's a signal to dial humanizer back on the next attempt
rather than letting Strunk compound the drift. Prefer one good polish over
iterative grinding.

**The user says "don't change meaning, just clean up grammar."** That is not a
polish request. Do a grammar pass only and skip this skill.

## Output philosophy

The polished text is the deliverable. The user does not need to see the
machinery. Keep user-facing commentary to one short line if anything at all —
for example, "I kept the hedging in the third sentence because it carries the
claim about sample size." That kind of note earns its place. Meta-commentary
about "I removed an em-dash and three rule-of-three constructions" does not.

If the two passes produced a result you are not confident in (e.g., you had to
override one of the upstream skills significantly), say so briefly. Do not
hedge for the sake of hedging, but do be honest about low-confidence edits so
the user can spot-check.
