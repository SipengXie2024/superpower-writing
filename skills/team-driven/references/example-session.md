# Example session (team-driven)

Concrete walkthrough of a parallel plan execution across three groups with a fixed pool of three implementer teammates plus persistent spec- and manuscript-reviewers. Use this to see how the process digraph in SKILL.md maps to actual team messaging.

```
You: I'm using Team-Driven Development to execute this plan.

[Read plan: .writing/plan.md]
[Identify groups: Group A (Tasks 1,2,3), Group B (Tasks 4,5), Group C (Task 6)]
[MAX_PARALLEL = 3]

[TeamCreate: "plan-execution"]
[Spawn: implementer-1, implementer-2, implementer-3, spec-reviewer, manuscript-reviewer]
[Create all 6 tasks via TaskCreate with group dependencies]

=== Group A (parallel) ===

[Assign Task 1 → implementer-1, Task 2 → implementer-2, Task 3 → implementer-3]
[Send full task text to each implementer]

[implementer-1 working on Task 1...]
[implementer-2 working on Task 2...]
[implementer-3 working on Task 3...]

implementer-2 → spec-reviewer: "Task 2 done. [report]"
spec-reviewer → implementer-2: "Missing error handling for edge case X (spec requires it)"
implementer-2: fixes issue
implementer-2 → spec-reviewer: "Fixed. [updated report]"
spec-reviewer → lead: "Task 2 spec review passed"
lead → manuscript-reviewer: "Please review Task 2 for manuscript quality"
manuscript-reviewer → lead: "Task 2 manuscript review passed"

implementer-1 → spec-reviewer: "Task 1 done. [report]"
spec-reviewer → lead: "Task 1 spec review passed"
lead → manuscript-reviewer: "Please review Task 1 for manuscript quality"
manuscript-reviewer → implementer-1: "Magic number on line 42, extract constant"
implementer-1: fixes
implementer-1 → manuscript-reviewer: "Fixed."
manuscript-reviewer → lead: "Task 1 manuscript review passed"

implementer-3 → spec-reviewer: "Task 3 done. [report]"
spec-reviewer → lead: "Task 3 spec review passed"
lead → manuscript-reviewer: "Please review Task 3 for manuscript quality"
manuscript-reviewer → lead: "Task 3 manuscript review passed"

[Lead: aggregate findings, update progress.md, unblock Group B]

=== Group B (parallel, after A) ===

[Assign Task 4 → implementer-1, Task 5 → implementer-2]
[implementer-3 is idle — can be shut down or held for Group C]

... same pattern ...

=== Group C ===

[Assign Task 6 → implementer-1]
... spec-reviewer approves, manuscript-reviewer approves ...

[All tasks complete]
[Shutdown team]
[Use finishing-branch skill]
```

Observations worth noticing when you read this:

- Implementer teammates finish in a different order than they start (Task 2 before Task 1). The lead must not block on a particular task; react to whichever finishes first.
- Implementer ↔ spec-reviewer DMs are peer-to-peer. The lead is only pulled in once spec review passes, because that is the moment the manuscript-reviewer needs to be activated.
- Manuscript-reviewer DMs the implementer directly for quality fixes (Task 1's magic number) — the lead is not a relay for fix loops.
- Idle teammates are normal between groups. Do not shut them down unless the next group genuinely has fewer tasks than teammates; team spin-up cost is real.
- Aggregation and plan alignment run once per group, not once per task. The cumulative-drift check is cheaper here than at the very end.
