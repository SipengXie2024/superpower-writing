# Cadence, Reviewer Independence, and the Manual Fallback

This file holds the detail behind three rules the SKILL summarizes: why a verdict-bearing skill must never run on a wall-clock timer, what may and may not reach the critic, and how the optional zero-API-cost manual path works.

## Why schedulers FIRE but never ACQUIT

External schedulers, meaning `/loop`, `/schedule`, `CronCreate`, and any "wake me every N minutes" mechanism, decide WHEN an agent wakes up. They do not, and must not, decide WHO judges the work or WHETHER a result is accepted.

External cadence is pure fire-control. It is never a jury.

A scheduler picks the firing moment. It points the agent at a task at a chosen time. It has no opinion on correctness, quality, novelty, or publishability, and it must never silently re-spawn an agent or drop a verdict step to stay cheap or finish faster.

Rule of thumb: cadence can DRIVE; it cannot ACQUIT. A goal or loop may keep an agent going, but the STOP or ACCEPT decision belongs to the acceptance gate. For a quality or correctness verdict, that gate is a different model family, and after the critic, the human.

### The known failure mode

External cadence is genuinely useful for one shape of work, waiting on the external world, and genuinely harmful for another, wrapping an internal semantic loop. The two look similar ("run this skill again later"), so people reach for `/loop` on both. The harmful case has a specific pathology.

Wrapping this external-review skill in `/loop 30m` re-runs a verdict-bearing skill on a clock that has nothing to do with whether the artifact changed. Zero new signal, full token cost. Worse, an external `/loop` re-enters the skill from the top each tick and starts a fresh Codex session. The critic loses its memory of what it already flagged in round 1. "Did you fix the gap I named?" becomes unanswerable, because the critic that named it is gone.

The fix is a clean split: external cadence for the external-world wait, never for the internal semantic loop.

### The distinction

| | External-world wait (additive) | Internal semantic loop (harmful to wrap) |
|---|---|---|
| What it waits on | A fact in the outside world: job done, metric logged, file landed | A judgment the agent itself produces |
| What advances it | Reality changing: a GPU frees, an epoch logs, a PDF compiles | A model emitting a verdict |
| Owns its own loop? | No; without cadence a session blocks on sleep | Yes; the review skill already iterates across rounds, carrying state in the Codex session |
| Acceptance gate | Machine-checkable existence or completion, safe same-model | Quality or correctness, must be cross-model |

One-liner: schedule the wait, never the verdict.

### Cases where external cadence IS safe (additive)

These replace a session that would otherwise sit sleeping on an external event. The cadence is the only thing the agent waits on; no judgment is re-run.

- GPU or experiment-job completion polling: "is the job done? are the GPUs still busy?" The wake reads status and either reports done or sleeps again. The thing waited on is external and machine-checkable.
- Training-anomaly checks that read metrics every N minutes to catch divergence or idle GPUs early, so the agent need not hold a session open for the whole run.
- Daily literature watch: a once-a-day sweep for new papers in a tracked direction. The external fact is "the world published something new today."

In every additive case the acceptance gate is execution-completeness: exit code, file exists, metric logged. Those are machine-checkable, so the polling agent may judge them itself. The cadence never touches a quality verdict.

### The fence

A verdict-bearing skill, meaning one whose output is a judgment of quality, correctness, support, novelty, or satisfaction, must run on its own internal cadence with its own round-to-round state and must terminate in the cross-model critic and then the human. This external-review skill is such a skill. Never put it inside `/loop`, `/schedule`, or `CronCreate`.

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

Within the same Codex session, a follow-up round may reference the critic's own previous feedback to check whether a concern was resolved. That is the critic's memory of its own critique, which is why the session must persist across rounds and must not be re-spawned by an external timer. It still must not include your interpretation of that feedback.

## Optional manual fallback: zero API cost, any model

The Codex bridge is the core reviewer backend. The manual path below is OPTIONAL. It is not bundled with this plugin, and this skill never requires it. Mention it only when the user lacks Codex access or wants to choose the reviewing model each time.

The ARIS manual-review MCP server (`mcp-servers/manual-review/server.py` in the ARIS repo) is a human-in-the-loop bridge. Instead of calling an API, it opens a local browser page, or on headless Linux writes a prompt file, where the user copies the brief to a different-family model and pastes the response back. It works with any text model: ChatGPT, DeepSeek, Kimi, Gemini, a local model. Zero API cost.

The cross-model rule is identical here. The reviewing model must be a different family from the executor. If the executor is Claude, the brief must NOT be pasted into any Claude product (claude.ai, the Claude API, the Claude app); doing so collapses the family switch and defeats the review. The brief reaches the reviewer unfiltered, and the verdict stays advisory.

If the user wants this path, they install and register the server themselves, for example:

```bash
claude mcp add manual-review -s user -- python3 /path/to/mcp-servers/manual-review/server.py
```

Once registered, the server exposes `review` (new thread) and `review_reply` (follow-up in the same thread), mirroring the Codex bridge's session continuity. Pass the same brief content the Codex bridge would read. Remote web UIs cannot read local filesystem paths, so paste the brief contents inline rather than passing a path, or attach the brief file if the UI supports upload.

### Headless file mode

On an SSH or headless box with no browser, set `MANUAL_REVIEW_MODE=file`. The server writes the prompt, with a cross-model warning at the top, to a per-thread directory. Read the pending-state JSON the server writes: its `prompt_file` field points to the prompt to copy out, and its `response_file` field points to where you write the model's response back. The response file must be non-empty and stable, meaning unchanged across two reads, before the server accepts it.

MCP servers load at session start, so registering this server is invisible to the session that registered it. Defer any end-to-end manual-review test to a fresh session.
