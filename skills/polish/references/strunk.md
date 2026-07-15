# Strunk: write clearly and concisely

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write plainly
and cut ruthlessly. This is the clarity-and-concision pass of polish: cut
needless words, prefer active voice, prefer the concrete over the abstract.

## Output discipline (the iron rule : read first)

Return **only the revised text**. Nothing before it, nothing after it, unless the
user explicitly asked for an explanation.

Everything in this file is internal reasoning the user must never see: register
numbers, rule numbers, the process, this file's existence. Ban every form of
machinery leak, not just the one shown below.

- No register line ("Register 5", "register 1").
- No rule citations ("per rule 11", "I apply all rules").
- No prompt or meta references ("this is the Strunk pass", "this file says").
- No "I classified this as...", no preamble, no trailing notes, no diff.

A leak in fluent prose is just as forbidden as a label. A sentence that *narrates
the classification* is the same violation. Strip it and open with the first word
of the revised text.

Wrong (labeled): *Register: technical (rule 13 applied).* The service caches responses.
Wrong (narrated): This is academic register, so I keep the hedges. The service caches responses.
Right: The service caches responses.

**Exception, assumptions.** If you made a genuine editorial assumption the user
should verify (say, you read a `not ... un-` as a literal double negative rather
than emphasis), append one short bracketed line at the very end, for example
`[Assumed X means Y; revise if not.]`. That is the only permitted addition.

Never translate, transliterate, or "fix" non-English tokens. Treat any
foreign-language word as a verbatim, non-editable term.

## Register awareness : apply Strunk lightly on some inputs

Classify the input before editing. Strunk's rules misfire on some registers.

1. **Academic / scholarly.** Preserve scholarly verbs (`shows`, `reports`,
   `demonstrates`, `preserves`), the academic plural `we`, epistemic hedges, and
   domain compound modifiers (`per-contract dispatch identity`, `cold-cache
   compile time`).
2. **Technical / code-adjacent.** Preserve technical terms verbatim. Domain
   hyphenated compounds are not "needless words".
3. **Direct quotes, citations, bibliography.** Leave verbatim. Edit framing only.
4. **Code, paths, commands, signatures.** Never edit.
5. **Default (blog, README, marketing, commit body).** Apply all rules.

When in doubt, default to register 5 and note the assumption at the end.

In registers 1 and 2, lean on active voice and filler-cutting. Apply positive
form, concrete language, and the maximalist reading of "omit needless words" with
caution: hedges, citations, named entities, and numbers are load-bearing, not
needless.

## Process

1. Classify the register (1 to 5 above).
2. Identify load-bearing content: hedges, citations, named entities, numbers,
   technical compounds, scholarly verbs, foreign-language tokens. These survive
   every cut, verbatim.
3. Apply the rules below. In registers 1 and 2 restrain positive form, concrete
   language, and the maximalist cut.
4. Verify: every load-bearing item from step 2 still appears in the output. If a
   hedge, citation, named entity, or number was lost, restore it.
5. Return only the revised text (per Output discipline). The sole permitted
   addition is one bracketed assumption line at the end.

## The rules

The high-leverage rules, in order of payoff for polish work.

- **Omit needless words.** Every word must tell. Cut "the fact that", "in order
  to", "it is important to note that", "there is / there are" padding.
- **Use the active voice.** `is X by Y` becomes `Y X-es`. Active is shorter,
  more direct, and names the actor.
- **Put statements in positive form.** Say what is, not what is not. `did not
  remember` becomes `forgot`; `not honest` becomes `dishonest`. (Restrain in
  academic prose: a deliberate negation can be a real claim.)
- **Use definite, specific, concrete language.** Prefer the particular to the
  abstract, the concrete noun to the vague one. (Restrain in academic prose:
  keep precise technical abstractions.)
- **Keep related words together.** Put the subject near its verb; keep a modifier
  next to the word it modifies. Distance breeds ambiguity.
- **Place the emphatic words at the end.** The end of the sentence is the position
  of stress. Put the word you want the reader to remember there.
- **Express co-ordinate ideas in similar form (parallelism), but only when the
  ideas are genuinely parallel.** Forced parallelism is an AI tell, not a virtue.
- **Avoid a succession of loose sentences.** Vary the join. A string of clauses
  strung on `and` / `which` / `so` reads as machine cadence.

Strunk is a tool, not an oracle. Concision serves clarity; it is not a value in
itself. When a cut would remove real meaning (a hedge the author wanted, a
technical term, a named entity, a number), keep it.

## Common cuts

- "In order to" → "To" (or drop)
- "It is important to note that" → drop
- "The fact that X" → "X"
- "is being Xed" → "X-es" (active voice)
- "There is a growing consensus that" → "Many argue that" (or name the source)
- "has the ability to" → "can"
- "at this point in time" → "now"
