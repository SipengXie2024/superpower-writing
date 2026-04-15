---
name: subagent-driven
description: Use when executing a written plan in THIS session, one task at a time, by spawning a fresh subagent per task and running a two-stage review gate (spec-reviewer then quality-reviewer) before moving on. Pick this over team-driven when tasks are lightweight and must run in strict order, over executing-plans when you want the work done now rather than in a separate session. Trigger on phrases like "execute the plan", "implement the tasks one by one", "run the plan here".
---

# Subagent-Driven Development

Execute plan by dispatching one new subagent invocation per task, with two-stage review after each: spec compliance review first, then manuscript review. Each subagent gets its own planning directory for structured knowledge capture.

**Core principle:** One new subagent invocation per task + per-agent planning dir + two-stage review (spec then quality) = high quality, fast iteration

**Announce at start:** "I'm using the subagent-driven skill to execute this plan."

## Shared Review Protocol

The two-stage review gate (spec then quality), the 3-round cap with escalation, the plan-anchoring rules for verbatim task extraction, the plan-alignment gate for cumulative drift, and the per-agent planning-directory convention are the same across subagent-driven and team-driven. They live in [`../planning-foundation/references/review-loop-protocol.md`](../planning-foundation/references/review-loop-protocol.md) — read it before executing any task. This skill applies that protocol using one-shot subagent dispatches: a fresh subagent per task, a dedicated spec-reviewer subagent, then a manuscript-reviewer subagent, escalating to the user directly if any loop hits the 3-round cap.

## When to Use

```dot
digraph when_to_use {
    "Have implementation plan?" [shape=diamond];
    "Tasks mostly independent?" [shape=diamond];
    "Stay in this session?" [shape=diamond];
    "subagent-driven" [shape=box];
    "executing-plans" [shape=box];
    "Manual execution or brainstorm first" [shape=box];

    "Have implementation plan?" -> "Tasks mostly independent?" [label="yes"];
    "Have implementation plan?" -> "Manual execution or brainstorm first" [label="no"];
    "Tasks mostly independent?" -> "Stay in this session?" [label="yes"];
    "Tasks mostly independent?" -> "Manual execution or brainstorm first" [label="no - tightly coupled"];
    "Stay in this session?" -> "subagent-driven" [label="yes"];
    "Stay in this session?" -> "executing-plans" [label="no - parallel session"];
}
```

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- One new subagent invocation per task (no context pollution)
- Per-agent planning directories (structured knowledge capture)
- Two-stage review after each task: spec compliance first, then manuscript quality
- Faster iteration (no human-in-loop between tasks)

## The Process

```dot
digraph process {
    rankdir=TB;

    subgraph cluster_per_task {
        label="Per Task";
        "Create agent planning dir (if not exists)" [shape=box style=filled fillcolor=lightyellow];
        "Dispatch implementer subagent (./implementer-prompt.md)" [shape=box];
        "Implementer subagent asks questions?" [shape=diamond];
        "Answer questions, provide context" [shape=box];
        "Implementer subagent implements, tests, commits, self-reviews" [shape=box];
        "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" [shape=box];
        "Spec reviewer subagent confirms manuscript matches spec?" [shape=diamond];
        "Implementer subagent fixes spec gaps" [shape=box];
        "Dispatch manuscript reviewer subagent (./manuscript-reviewer-prompt.md)" [shape=box];
        "Manuscript reviewer subagent approves?" [shape=diamond];
        "Implementer subagent fixes quality issues" [shape=box];
        "Aggregate agent findings into top-level .writing/" [shape=box style=filled fillcolor=lightyellow];
        "Mark task complete via TaskUpdate" [shape=box];
    }

    "Read plan, extract all tasks with full text, note context, create tasks via TaskCreate" [shape=box];
    "More tasks remain?" [shape=diamond];
    "Dispatch final manuscript reviewer subagent for entire implementation" [shape=box];
    "Use superpower-writing:finishing-branch" [shape=box style=filled fillcolor=lightgreen];

    "Read plan, extract all tasks with full text, note context, create tasks via TaskCreate" -> "Create agent planning dir (if not exists)";
    "Create agent planning dir (if not exists)" -> "Dispatch implementer subagent (./implementer-prompt.md)";
    "Dispatch implementer subagent (./implementer-prompt.md)" -> "Implementer subagent asks questions?";
    "Implementer subagent asks questions?" -> "Answer questions, provide context" [label="yes"];
    "Answer questions, provide context" -> "Dispatch implementer subagent (./implementer-prompt.md)";
    "Implementer subagent asks questions?" -> "Implementer subagent implements, tests, commits, self-reviews" [label="no"];
    "Implementer subagent implements, tests, commits, self-reviews" -> "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)";
    "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" -> "Spec reviewer subagent confirms manuscript matches spec?";
    "Spec reviewer subagent confirms manuscript matches spec?" -> "Implementer subagent fixes spec gaps" [label="no"];
    "Implementer subagent fixes spec gaps" -> "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" [label="re-review\n(max 3 rounds)"];
    "Spec reviewer subagent confirms manuscript matches spec?" -> "Dispatch manuscript reviewer subagent (./manuscript-reviewer-prompt.md)" [label="yes"];
    "Dispatch manuscript reviewer subagent (./manuscript-reviewer-prompt.md)" -> "Manuscript reviewer subagent approves?";
    "Manuscript reviewer subagent approves?" -> "Implementer subagent fixes quality issues" [label="no"];
    "Implementer subagent fixes quality issues" -> "Dispatch manuscript reviewer subagent (./manuscript-reviewer-prompt.md)" [label="re-review\n(max 3 rounds)"];
    "Manuscript reviewer subagent approves?" -> "Aggregate agent findings into top-level .writing/" [label="yes"];
    "Aggregate agent findings into top-level .writing/" -> "Mark task complete via TaskUpdate";
    "Mark task complete via TaskUpdate" -> "More tasks remain?";
    "More tasks remain?" -> "Create agent planning dir (if not exists)" [label="yes - next task"];
    "More tasks remain?" -> "Plan Alignment Gate: re-read plan.md, verify all tasks match original plan" [label="no"];
    "Plan Alignment Gate: re-read plan.md, verify all tasks match original plan" -> "Dispatch final manuscript reviewer subagent for entire implementation";
    "Dispatch final manuscript reviewer subagent for entire implementation" -> "Use superpower-writing:finishing-branch";
}
```

## Prompt Templates

- `./implementer-prompt.md` - Dispatch implementer subagent (includes planning dir injection)
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer subagent
- `./manuscript-reviewer-prompt.md` - Dispatch manuscript reviewer subagent

## Example Workflow

A complete worked example — one implementer question, one spec-review fail-and-fix, one manuscript-review fail-and-fix, across two tasks — lives in [`references/example-session.md`](references/example-session.md). Read it when you want to see how the process digraph above maps to actual messages.

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)
- Subagent can ask questions (before AND during work)
- Per-agent planning dirs capture knowledge persistently

**vs. Executing Plans:**
- Same session (no handoff)
- Continuous progress (no waiting)
- Review checkpoints automatic

**Efficiency gains:**
- No file reading overhead (controller provides full text)
- Controller curates exactly what context is needed
- Subagent gets complete information upfront
- Questions surfaced before work begins (not after)
- Planning dirs prevent knowledge loss between subagents

**Quality gates:**
- Self-review catches issues before handoff
- Two-stage review: spec compliance, then manuscript quality
- Review loops ensure fixes actually work
- Spec compliance prevents over/under-building
- Manuscript quality ensures implementation is well-built
- Aggregation preserves findings for future tasks

**Cost:**
- More subagent invocations (implementer + 2 reviewers per task)
- Controller does more prep work (extracting all tasks upfront)
- Review loops add iterations
- But catches issues early (cheaper than debugging later)

## Red Flags

**Never:**
- **Skip reviews** — see Two-Stage Review Gate above. No exceptions.
- Start implementation on main/master branch without explicit user consent
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context (subagent needs to understand where task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance (reviewer found issues = not done)
- Start manuscript review before spec compliance passes (wrong order)
- Skip planning dir creation or aggregation step (knowledge gets lost)

**If subagent asks questions:**
- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

**If reviewer finds issues:**
- Implementer (same subagent) fixes them
- Reviewer reviews again
- Maximum 3 fix-review rounds per review stage
- After 3 rounds without approval: escalate to user (do NOT continue looping)
- Don't skip the re-review

**If subagent fails task:**
- Dispatch fix subagent with specific instructions
- Don't try to fix manually (context pollution)

## Integration

**Required workflow skills:**
- **superpower-writing:git-worktrees** - RECOMMENDED: Set up isolated workspace unless already on a feature branch
- **superpower-writing:writing-plans** - Creates the plan this skill executes
- **superpower-writing:finishing-branch** - Complete development after all tasks

After review passes, merge per the repo's review conventions.

**Subagents should use claim-first discipline:** Follow test-first discipline: write a failing test (or claim stub), watch it fail, write the minimal implementation, watch it pass.

**Alternative workflow:**
- **superpower-writing:executing-plans** - Use for parallel session instead of same-session execution
