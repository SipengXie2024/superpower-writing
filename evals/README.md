# Eval suite

Run the whole suite against this plugin, both arms:

```bash
claude plugin eval . --ablation with-without --judge-model sonnet -j 4 --trust-plugin --no-publish
```

`--judge-model sonnet` is not optional if you want to compare against past
numbers. The CLI defaults to haiku, and every result under `results/` was scored
by sonnet. `--case <glob>` reruns one case, which is how you check a single fix
without paying for the full suite.

Exit 1 usually means a case scored below the `--threshold` default of 1.0, not
that the run broke. Read the scores.

## Two kinds of case

Cases tagged `parity` score 1.00 in both arms with the skill firing: the baseline
model already has that discipline, so they measure model regression, not plugin
value. They cost money every run and never move the delta. Exclude them from
routine runs and run them alone when the model version changes:

```bash
claude plugin eval . --ablation with-without --judge-model sonnet -j 4 --trust-plugin --no-publish --tag writing   # routine
claude plugin eval . --ablation none --judge-model sonnet -j 4 --trust-plugin --no-publish --tag parity             # after a model change
```

Why they cannot be made to discriminate is measured, not guessed: the cases that
do separate the arms are the ones where the right answer is a refusal (do not
write the optimization, do not draft against an unresolved claim, do not discard
the dead-end record), and the parity cases are the ones where the right answer
is noticing something (the polluted cache, the off-by-one, the swallowed
timeout). Adding pressure to a noticing case drove both arms to 0.00 in three of
twelve tries and improved none; those rewrites were reverted.

## Reading a two-arm result

`with` runs the model with this plugin loaded; `without` runs it bare. The
delta is the plugin's contribution. Two numbers must be read together:

- **the score**, and
- **`skill-fired`**, a `tool_used` grader excluded from scoring.

A delta of zero with `skill-fired` at 0/3 means the plugin never engaged, so the
two arms ran the same thing and the score measured nothing about the plugin. That
is a triggering defect in the skill's `description`, not a quality result. Six
cases sat in that state until 2026-09-14; fixing the descriptions moved every one
of them to 3/3 without touching any capability.

A delta of zero with `skill-fired` at 3/3 is a real finding: the case does not
separate the arms. The fix is a harder prompt, not a stricter rubric.

## Testing a rubric

Rubrics are graded by an LLM, so they can be wrong in both directions: they can
fail good answers, and they can pass the exact answer they were written to
reject. Both have happened here. Before trusting one, test it.

**Do not use `claude -p` to reproduce the judge.** Measured against the real
harness on six transcripts it disagreed on four, and it is systematically
lenient: a rubric that scores 5/5 under it can score 0/3 in the harness. It is an
agent with tools; the harness judge is a bare model call.

The technique that works is an **echo suite**. Build a scratch case whose prompt
asks the model to reproduce a canned reply verbatim, copy the real
`graders/result.md` into it, and run `claude plugin eval` on the scratch suite.
The harness judge sees only the rubric body and the reply, never the case prompt,
so the echo wrapper cannot leak into the verdict.

Two traps, both hit in practice:

- **Echo fidelity.** Verify each run's `last_message` against your canned text
  before counting the vote. Models refuse to echo first-person text that claims
  work they did not do, and they silently swap full-width punctuation. A tally
  over unverified echoes measures the wrong string.
- **Three votes is noisy.** One case's baseline arm was recorded FAIL FAIL FAIL
  by the harness while fifteen independent votes on the same text said PASS.
  Do not act on a one-run difference.

## Audit status

Every case whose score was 1.00 in both arms was audited on 2026-09-14 by
echoing a fluent, confident answer that violates its one discipline. All six
passed the audit: each rejected the bad answer and accepted a good one.

| case | discipline | bad answer |
|---|---|---|
| `ai-tells-removed-from-draft` | strip the puffery, invent no evidence | 0/15, 0/9 |
| `citation-must-be-verified` | unresolvable metadata is not confirmed | 0/15 |
| `data-plot-requested` | a single run gets no error bar | 0/15, 0/15 |
| `related-work-search-strategy` | press "the first" against real prior work | 0/15 |
| `research-idea-stress-tested` | find a specific flaw, do not agree and draft | 0/15 |
| `unbacked-claim-caught` | `eval-c2` may not be marked verified | 0/15 |

Known limit, not yet fixed: `ai-tells-removed-from-draft` passes the same
corrected paragraph 12/12 when it is followed by a note on what was cut, and
fails it 0/15 when the paragraph arrives bare, though the rubric says commentary
is ignored. A minimal patch to that sentence did not move it. Real answers always
explain themselves, so the arms both score 1.00 today; treat it as a latent
misjudgement risk if a future answer is terse.

`sixteen-candidate-slate-triaged` was rebuilt rather than patched. Its first
clause asked the judge to verify a sixteen-item enumeration inside a long
bilingual answer, and measurement showed it returned FAIL for an honest answer
and for one that silently dropped four candidates alike — it was not performing
the check. A regex cannot take the job either, because candidate numbers 1-5
collide with FINER scores in the same table cells. The case now grades only the
four planted disqualifiers, which the judge handles reliably, and says so in the
rubric.

## Write-enabled cases

Cases that judge what was written need `Write` and `Edit` in `allowed_tools` and
the operator grant `--allow-tools Write Edit` on the command line. Both halves are
required.

Do not add `Bash`. Granting a shell makes the harness demand a sandbox backend,
and on a machine without `socat` and `bubblewrap` it refuses the whole run rather
than running unconfined — every run comes back with zero turns and an error, which
is the correct behaviour but costs you the run.

**Reaching the file contents is the hard part.** Three graders look like they
would work and two of them do not:

- `focus: files` passes the judge a sorted list of created paths and nothing
  else. A rubric asking about content under this focus can never pass. One case
  scored 0.00 in both arms this way before the cause was found.
- `focus: trace` passes the conversation, but once it runs past 24 messages only
  the first 12 and last 12 survive. A mid-run write becomes invisible. Keeping
  the prompt self-contained, so the model does no exploration, pushes the writes
  into the visible tail, but that is mitigation rather than a guarantee.
- `focus: {source: file, path: <path>}` does pass real file contents. It needs a
  literal path, so it rewards knowing the plugin's convention; mark it
  `arm: with-only` and keep the score on path-agnostic graders, or the no-plugin
  arm is being failed for not knowing a convention nobody told it.

The path-agnostic way to reach content is `type: tool_used` with `input_match`,
which is a regex over the tool call's own input, file body included. It is free
and deterministic, and it checks presence rather than quality — good for "the
saved text names the constraint", useless for "the plan is any good".
