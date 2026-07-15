# Cadence and Reviewer Independence

This file explains why a verdict-bearing skill must never run on a wall-clock timer and what may or may not reach either external critic.

## Why schedulers FIRE but never ACQUIT

External schedulers, meaning `/loop`, `/schedule`, `CronCreate`, and any "wake me every N minutes" mechanism, decide WHEN an agent wakes up. They do not, and must not, decide WHO judges the work or WHETHER a result is accepted.

External cadence is pure fire-control. It is never a jury.

A scheduler picks the firing moment. It points the agent at a task at a chosen time. It has no opinion on correctness, quality, novelty, or publishability, and it must never silently re-spawn an agent or drop a verdict step to stay cheap or finish faster.

Rule of thumb: cadence can DRIVE; it cannot ACQUIT. A goal or loop may keep an agent going, but the STOP or ACCEPT decision belongs to the acceptance gate. For a quality or correctness verdict, that gate is a different model family, and after the critic, the human.

### The known failure mode

External cadence is genuinely useful for one shape of work, waiting on the external world, and genuinely harmful for another, wrapping an internal semantic loop. The two look similar ("run this skill again later"), so people reach for `/loop` on both. The harmful case has a specific pathology.

Wrapping the review skill in `/loop 30m` re-runs a verdict-bearing skill on a clock that has nothing to do with whether the artifact changed. Zero new signal, full token cost. Worse, an external `/loop` re-enters the skill from the top each tick and loses provider-specific review history. "Did you fix the gap I named?" becomes unanswerable because the prior Codex session and Hermes handoff are not carried into the new tick.

The fix is a clean split: external cadence for the external-world wait, never for the internal semantic loop.

### The distinction

| | External-world wait (additive) | Internal semantic loop (harmful to wrap) |
|---|---|---|
| What it waits on | A fact in the outside world: job done, metric logged, file landed | A judgment the agent itself produces |
| What advances it | Reality changing: a GPU frees, an epoch logs, a PDF compiles | A model emitting a verdict |
| Owns its own loop? | No; without cadence a session blocks on sleep | Yes; the review skill already iterates across rounds, carrying Codex's session and Hermes's own structured handoff separately |
| Acceptance gate | Machine-checkable existence or completion, safe same-model | Quality or correctness, must be cross-model |

One-liner: schedule the wait, never the verdict.

### Cases where external cadence IS safe (additive)

These replace a session that would otherwise sit sleeping on an external event. The cadence is the only thing the agent waits on; no judgment is re-run.

- GPU or experiment-job completion polling: "is the job done? are the GPUs still busy?" The wake reads status and either reports done or sleeps again. The thing waited on is external and machine-checkable.
- Training-anomaly checks that read metrics every N minutes to catch divergence or idle GPUs early, so the agent need not hold a session open for the whole run.
- Daily literature watch: a once-a-day sweep for new papers in a tracked direction. The external fact is "the world published something new today."

In every additive case the acceptance gate is execution-completeness: exit code, file exists, metric logged. Those are machine-checkable, so the polling agent may judge them itself. The cadence never touches a quality verdict.

### The fence

A verdict-bearing skill, meaning one whose output is a judgment of quality, correctness, support, novelty, or satisfaction, must run on its own internal cadence with its own round-to-round state and must terminate in the cross-model critic and then the human. This review skill is such a skill. Never put it inside `/loop`, `/schedule`, or `CronCreate`.

If you find yourself wanting to schedule this skill, the thing you actually want to schedule is the external wait that precedes it. Schedule a poll on the training job; when the job exits, run this review once.

One-liner: a heartbeat may say "keep going," never "good enough."

## Reviewer independence: what reaches the critic

Cross-model review only works if the critic forms its own assessment from primary artifacts. If the executor pre-digests, summarizes, or interprets the work before passing it on, the critic evaluates the executor's framing, not the actual work. That re-introduces the correlated blind spots heterogeneous review is designed to remove.

### What you MAY pass to the critic

- Role or persona: "Review as a senior NeurIPS-level reviewer."
- Review objective: "Evaluate publishability", "Check whether the proof holds", "Score novelty and soundness."
- File paths: let the critic read file contents directly.
- Structural metadata: "The paper has 8 sections", "Experiments live under experiments/."
- Venue constraints: "ICLR format, 9-page limit, double-blind."

### What you MUST NOT pass (counts as subjective interference)

- Your summary or paraphrase of file contents.
- Your interpretation of results ("I think the problem is...", "This suggests...").
- Your recommendations or conclusions ("I suggest changing...", "The likely cause is...").
- Key findings or bullet points you extracted.
- Leading questions ("Is this publishable?", "Is this trade-off reasonable?").
- Statements asserting the current approach's strengths.

### Why it matters

| With filtering | Without filtering |
|---|---|
| Critic sees the executor's framing | Critic sees raw artifacts |
| Correlated blind spots persist | Genuinely independent assessment |
| Executor can coach a favorable review | Review probes real weaknesses |
| Defeats the purpose of cross-model | Achieves adversarial collaboration |

### Correct brief shape

```
Review the following research project as a senior reviewer for <venue>.

Files to read:
- Paper draft: <abs path>/.writing/main.tex and .writing/manuscript/*.tex
- Research synthesis: <abs path>/.writing/findings.md
- Claims under review: <abs path>/.writing/claims/section_*.md

Read all files yourself and provide a complete review. Score novelty,
soundness, evaluation, clarity, and significance. Be brutally honest.
```

### The multi-round exception

A follow-up round may give each critic its own previous feedback to check whether a concern was resolved. Codex may resume its session. Hermes receives its own structured handoff in a fresh oneshot prompt. Neither provider receives the other's feedback or the executor's interpretation. This provider-specific history must not be discarded and recreated by an external timer.
