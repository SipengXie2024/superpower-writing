---
name: external-review
description: Cross-model critical review of a paper, idea, or result by a different-family critic that catches blind spots a same-model reviewer shares. Routes the review brief through the Codex bridge and asks for concrete deliverables (mock venue review, results-to-claims matrix, minimal-experiment plan). Use when the user says "review my paper", "get an external review", "stress-test this idea", or wants brutally honest pre-submission feedback.
---

# External Review

## Overview

A same-family reviewer shares the author's blind spots. This skill sends the work to a critic from a different model family so the gaps one model misses, the other can name. The critic reads the primary artifacts itself and returns a brutally honest, venue-calibrated critique plus concrete deliverables the author can act on.

This skill does not reinvent a reviewer backend. It routes the review brief through the Codex bridge documented in `superpower-writing:collaborating-with-codex`. A different-family critic is the point: Claude drafts the paper, Codex reviews it.

**Core principle:** The critic forms its own assessment from primary files. Never pre-digest, summarize, or pre-judge the work for it. A filtered brief re-introduces the very blind spots cross-model review exists to remove.

**Advisory, never autonomous.** Every verdict, score, and matrix this skill returns is advisory. Surface it to the user and let the user decide. Never auto-reject a paper, never flip a claim STATUS, never mutate `.writing/` state on a review verdict. The review is input to a human decision, not a gate that fires by itself.

**Never fabricate.** Do not invent the critic's verdict, scores, or quotes when a backend is unavailable. If no reviewer backend can be reached, say so and stop. A made-up review is worse than no review.

## When to Use

Trigger this skill when:

- The user says "review my paper", "get an external review", "external critique", "second opinion on this", or "stress-test this idea".
- A draft skeleton is ready and the user wants a venue-calibrated read before handing it to a co-author.
- The user wants a mock conference review with a score and confidence.
- The user wants to know which experiment to run next, or which claims a set of results can support.

Do NOT use this skill for:

- Citation or evidence verification against the bibliography. That is `superpower-writing:claim-verification`.
- Plan-conformance review of a finished implementation task. That is the planning plugin's `requesting-review`.
- Copy-editing prose. That is `polish` or `polish-by-diff`.
- A same-model self-review. The whole value here is the family switch.

## Cadence: schedulers FIRE, they never ACQUIT

This skill is verdict-bearing. It produces a cross-model review verdict, multi-round, with reviewer continuity carried in the Codex session. Do NOT wrap it in `/loop`, `/schedule`, or `CronCreate`.

External cadence is pure fire-control. It is never a jury.

A scheduler picks the firing moment. It points an agent at a task at a chosen time. It has no opinion on correctness, quality, novelty, or publishability, and it must never silently re-spawn an agent or drop a verdict step to stay cheap or finish faster.

Rule of thumb: cadence can DRIVE; it cannot ACQUIT. A loop may keep an agent going, but the STOP or ACCEPT decision belongs to the cross-model critic and, after it, the human.

Wrapping this skill in `/loop 30m` does not produce thirty-minutes-better review. It re-runs a verdict on a wall-clock timer that has nothing to do with whether the paper changed. The external `/loop` also re-enters the skill from the top each tick. Each tick starts a fresh Codex session, so the critic loses the memory of what it already flagged. "Did you fix round 1's gap?" becomes unanswerable. Zero new signal, full token cost.

What you may schedule is the external wait that precedes the review, never the verdict itself. If the review must wait on a training job, schedule a status poll on the job, then run this skill once after the job exits. The full rule, including the additive cases where external cadence is safe, lives in `references/cadence-and-independence.md`.

## Process

### Step 1: Gather the review context

Compile a self-contained brief before calling the critic. Read the project's own files:

1. The paper draft under `.writing/manuscript/*.tex` and `.writing/main.tex`, or the idea or result the user named.
2. `.writing/findings.md` for the research synthesis and prior decisions.
3. `.writing/outline.md` and the relevant `.writing/claims/section_*.md` for the claims under review.

Identify the core contribution, the methodology, the headline results, and the known weak points. You write down what to review and which files hold it. You do NOT write down your opinion of the work.

### Step 2: Write the brief file, do not pre-digest

Write the brief to a file the critic can read directly, for example `.writing/reviews/review-request.md`. Keep the bridge prompt itself short and point Codex at the absolute path.

The brief may contain: the reviewer role, the review objective, the target venue and its constraints, the absolute file paths to read, and structural metadata such as the section count. The brief must NOT contain your summary of the files, your interpretation of the results, your recommendations, leading questions, or any statement asserting the work's strengths. Let the critic read the raw artifacts and judge.

The boundary between safe context and subjective interference is detailed in `references/cadence-and-independence.md`. Read it before writing the first brief.

### Step 3: Initial review through the Codex bridge

Route the review through the Codex bridge. Follow the four-step workflow in `superpower-writing:collaborating-with-codex`: brief, invoke in the background, capture the `SESSION_ID`, verify the deliverable. The bridge script lives at `${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py`.

Invoke it in the background. This is mandatory; a foreground bridge call freezes the session.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "<absolute project root>" \
  --PROMPT "Read the review brief at <abs path>/.writing/reviews/review-request.md. \
Read every artifact it cites before judging; executor notes are not evidence beyond \
the files they reference. Act as a senior reviewer for <venue, e.g. NeurIPS / OSDI>. \
Be brutally honest. Identify: (1) logical gaps or unjustified claims; (2) missing \
experiments that would strengthen the story; (3) narrative weaknesses; (4) whether \
the contribution clears the bar for this venue."
```

When the JSON returns, check `success`. On `false` or a set `error`, read the error and re-brief. Save the `SESSION_ID` for follow-up rounds so the critic keeps context instead of re-reading the paper cold.

Ask for `gpt-5.5`-class reasoning depth only if the user names a model. The bridge `--model` flag is reserved for explicit user direction.

### Step 4: Iterative dialogue and the three deliverables

Reuse the `SESSION_ID` for follow-up rounds via the bridge. Each round, respond to criticisms with evidence, push back on points you disagree with, accept the valid ones, and ask for the concrete deliverables that turn critique into action. The three highest-value asks:

1. **Mock venue review.** "Write a mock <venue> review with Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."
2. **Results-to-claims matrix.** "Give me a results-to-claims matrix: which claim is allowed under each outcome of experiments X and Y."
3. **Minimal-experiment plan.** "Design the minimal additional experiment with the highest acceptance lift per GPU-week. State our compute budget and be specific about configurations."

The exact prompt text for each, plus the mock-review rubric and report skeleton, lives in `references/reviewer-deliverables.md`. Copy the prompts verbatim; they are tuned to produce structured, gradeable output.

Stop iterating when both sides agree on the core claims and their evidence requirements, a concrete experiment plan exists, and the narrative structure is settled.

### Step 5: Verify, then surface to the user

Verify the deliverable yourself before reporting. The bridge summary states the critic's intent, not proof. Read the returned review, confirm the matrix covers the outcomes you asked about, and confirm any cited file path actually exists. A critic can hallucinate a file or a number just as a drafter can.

Then surface the review to the user. Present the verdict, the score and confidence, the actionable weaknesses, and the deliverables. State plainly that the verdict is advisory. Do NOT act on it without the user. The user decides whether to revise, to run the recommended experiment, or to disagree with the critic.

### Step 6: Persist the review

Save the full interaction to `.writing/reviews/external-review-<ISO-date>.md`: a round-by-round summary of criticisms and responses, the final consensus on claims, the results-to-claims matrix, the prioritized TODO list with compute estimates, and the mock-review verdict. The document must be readable without the conversation.

If `.writing/` exists, append a row to the progress log noting the review ran, the backend used, the verdict, and the report path. Do NOT flip any claim STATUS and do NOT edit manuscript prose. Those are the jobs of `claim-verification` and `drafting`. This skill only writes its own review document and a progress row.

## Optional fallback: manual zero-API-cost review

The Codex bridge is the core path. An optional human-in-the-loop fallback exists for users with no Codex access, or who want to pick the reviewing model each time: the ARIS manual-review MCP server (`mcp-servers/manual-review/server.py` in the ARIS repo). It opens a local page where the user pastes the brief into any non-Claude model and pastes the response back. On headless Linux it writes a `prompt.md` instead. Zero API cost, any text model: ChatGPT, DeepSeek, Kimi, Gemini, or a local model.

This is OPTIONAL and not bundled with this plugin. If the user wants it, they install and register it themselves; this skill does not ship or require it. The cross-model rule is identical on the manual path. The reviewing model must be a different family from the executor, the brief reaches the reviewer unfiltered, and the verdict stays advisory. The same family as executor defeats the purpose. Setup and the headless file-mode protocol are summarized in `references/cadence-and-independence.md`.

## Key Principles

**Different family, or it is not external.** The single load-bearing requirement is that the critic comes from a different model family than the author. Claude drafts, Codex reviews. A Claude-on-Claude review shares the blind spots and is theater.

**The critic reads, the executor points.** Pass the role, the objective, the venue, and the file paths. Withhold every summary, interpretation, and recommendation. The moment you pre-chew the work, the critic reviews your framing, not the paper.

**Verdicts are advisory.** This skill never rejects a paper, never flips a claim, never mutates state on its own. It surfaces a cross-model opinion and hands the decision to the user. Advisory verdicts are the plugin ethos, not a limitation.

**Schedule the wait, never the verdict.** This is a verdict-bearing skill. It runs on its own multi-round cadence inside one Codex session and terminates in the human decision. It does not belong inside `/loop`, `/schedule`, or `CronCreate`.

**Never fabricate the review.** If the backend is down, report it and stop. Inventing a score, a quote, or a matrix to fill the gap corrupts the one thing this skill exists to provide: an honest outside read.

## Integration Points

- **collaborating-with-codex:** the reviewer backend. This skill writes the brief and reads the verdict; the bridge skill owns the Codex invocation, the `SESSION_ID` lifecycle, and the background-run rule.
- **claim-verification:** complementary, not overlapping. claim-verification proves citations resolve and abstracts support claims. external-review judges whether the contribution is novel and sufficient. Run claim-verification on evidence reliability; run external-review on research substance.
- **drafting:** the critic's weaknesses and minimal-experiment plan feed back into a revision the author drives through drafting. This skill never edits prose itself.
- **main skill:** routes here when the user asks for an external review, a second opinion, or a mock venue review.
