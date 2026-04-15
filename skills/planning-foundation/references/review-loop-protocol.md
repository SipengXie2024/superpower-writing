# Review-Loop Protocol (shared by subagent-driven and team-driven)

This file is the single source of truth for the two-stage review gate, review-loop caps, plan anchoring, and the plan-alignment gate. Both `subagent-driven` and `team-driven` reference this file from their SKILL.md; the execution mechanics differ (one-shot subagent vs persistent teammate with peer DMs) but the protocol below is identical.

When you change anything here, every consumer picks up the change automatically. Do not duplicate this content into individual SKILL.md files.

## Why a two-stage gate

Spec compliance and writing quality fail in different ways and take different tools to detect. A task can be well-written prose that fails to cover the outline's claims; or it can cover every claim but read like a first draft. Running the two reviewers in sequence — spec first, quality second — means the quality reviewer only looks at manuscripts that are already on-spec, and the implementer never has to juggle two overlapping fix lists at once.

## The two reviewers

1. **Spec compliance review** — verifies the produced artifact matches the original plan. Nothing extra, nothing missing, no drift from the outline's claim set or the plan's file contract. In subagent-driven this is the `superpower-writing:spec-reviewer` subagent dispatched after the implementer returns. In team-driven it is the persistent `spec-reviewer` teammate that the implementer DMs directly.
2. **Manuscript quality review** — verifies the artifact is well-built: prose reads cleanly, files are organized, tests pass, no magic numbers or obvious smells. In subagent-driven it is the `superpower-writing:manuscript-reviewer` subagent dispatched only after spec review passes. In team-driven the lead DMs the persistent `manuscript-reviewer` teammate once the spec reviewer reports a pass.

A task is not complete until BOTH reviewers return APPROVED. No exceptions — not for "simple" tasks, config changes, or "I already self-reviewed thoroughly". The dashboard columns `Spec Review`, `Quality Review` (subagent-driven) or `Manuscript Review` (team-driven), and `Plan Align` must all show `PASS` before the task status flips to `complete`.

Manuscript review before spec review passes is always the wrong order — the quality reviewer will end up commenting on content that is about to be rewritten.

## Review loop caps

Each review stage is capped at **3 fix-review rounds** per task. The initial review does not count as a round. A round is one fix-then-re-review cycle: initial review → fix → re-review (round 1) → fix → re-review (round 2) → fix → re-review (round 3) → STOP.

After 3 rounds without approval, stop looping and escalate. In subagent-driven the orchestrator escalates directly to the user; in team-driven the reviewer DMs the lead with an escalation message that includes:

1. Which issues remain unresolved after three attempts
2. What was attempted in each round
3. Whether the issues are getting better, worse, or stuck

The user then picks one of three outcomes:

- **Override and approve** — accept the current state despite open issues (usually when the issue is genuinely contested or out of scope)
- **Provide guidance** — give specific direction for a targeted fix. This does NOT reset the round counter; the next attempt is still the fourth cycle
- **Abort the task** — stop work on this task entirely

Track the round count in the Task Status Dashboard with notation like `FAIL (round 2/3)` in the relevant review column. Visible round counts help the user decide whether to override early instead of watching the loop churn.

## Plan anchoring: extracting task text

Plan drift is the single biggest source of "the implementation passed review but doesn't match what was asked for." The fix is almost mechanical — when you extract task text from `.writing/plan.md` to dispatch to an implementer, follow these rules:

1. **Copy verbatim.** Use the exact text from `plan.md`. Do not paraphrase, summarize, or "clean up" the task description.
2. **Include the section reference.** Tell the implementer which heading in `plan.md` contains the task (e.g., `### Task 3: Recovery modes`). The reviewer needs the same anchor to verify against.
3. **Include cross-task constraints.** If `plan.md` or `design.md` specifies shared interfaces, naming conventions, performance targets, or file-boundary rules that apply to multiple tasks, include them in the context section of every task that might touch them.
4. **Pass plan file paths.** Mention that `.writing/plan.md` and `.writing/design.md` are available on disk so implementers and reviewers can cross-reference the originals instead of trusting the orchestrator's extraction.

Verbatim copying plus plan references let implementers and reviewers independently verify against the source of truth — which is what catches the orchestrator's own extraction errors.

## Plan Alignment Gate

Per-task reviews catch local failures but miss cumulative drift: individual tasks each pass spec review while the whole implementation walks slowly away from the plan's original intent. The plan alignment gate catches this.

**Subagent-driven triggers the gate once**, after all tasks complete and BEFORE the final manuscript review.

**Team-driven triggers the gate after each parallelism group** completes, before starting the next group. Drift is cheaper to correct between groups than at the end.

In both cases the gate is the same sequence:

1. Re-read `.writing/plan.md` completely — refresh the original requirements in context
2. Re-read `.writing/design.md` if present — refresh architectural constraints
3. For each completed task, verify:
   - Does the implementation match the plan's specification (not just the extracted task text)?
   - Were cross-task constraints respected — shared interfaces, naming, performance targets?
   - Did accumulated decisions drift from the plan's original intent?
4. Update the `Plan Align` column in the Task Status Dashboard for each checked task
5. If drift is detected, log it in `.writing/findings.md` with specific details
6. If the drift is significant, escalate to the user before continuing:
   - Describe what drifted and why
   - Propose corrective action
   - Let the user decide whether to fix or accept

This gate is cheap (a few minutes of re-reading) and catches failure modes that no single-task reviewer can see. Skipping it is the closest analog to "all tests pass but the feature is wrong".

## Per-agent planning directories

Both execution modes use the same convention: one directory per role, reused across all tasks, not one directory per task.

```bash
mkdir -p .writing/agents/implementer/         # subagent-driven
mkdir -p .writing/agents/implementer-1/       # team-driven (one per persistent teammate)
mkdir -p .writing/agents/spec-reviewer/
mkdir -p .writing/agents/manuscript-reviewer/
```

Each directory contains `findings.md` (discoveries, decisions, critical items — appended across tasks) and `progress.md` (step-by-step progress log — also appended). Do NOT create per-task directories like `implementer-task-1/`, `implementer-task-2/`; they fragment context and defeat the point of persistent knowledge capture.

After each task's reviews both pass, the orchestrator aggregates the agent's findings into the top-level `.writing/`:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/aggregate-agent-findings.sh "<role>" "Task N: <name>"
```

The script pulls out "Critical for Orchestrator" items and appends them to `.writing/findings.md` and `.writing/progress.md`. The orchestrator then updates the Task Status Dashboard row manually (table at top of `progress.md`) and appends a completion line to the session log at the bottom.
