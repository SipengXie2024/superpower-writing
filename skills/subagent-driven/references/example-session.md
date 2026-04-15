# Example session (subagent-driven)

Concrete walkthrough of one serial plan execution. Use this to see how the digraph in SKILL.md maps to actual messages and tool calls — especially how the two-stage review gate looks in practice.

```
You: I'm using Subagent-Driven Development to execute this plan.

[Read plan file once: .writing/plan.md]
[Extract all 5 tasks with full text and context]
[Create all tasks via TaskCreate]

Task 1: Hook installation script

[Create .writing/agents/implementer/ (if not exists)]
[Dispatch implementation subagent with full task text + context + planning dir]

Implementer: "Before I begin - should the hook be installed at user or system level?"

You: "User level (~/.config/superpowers/hooks/)"

Implementer: "Got it. Implementing now..."
[Later] Implementer:
  - Implemented install-hook command
  - Added tests, 5/5 passing
  - Self-review: Found I missed --force flag, added it
  - Committed
  - Logged findings to .writing/agents/implementer/findings.md

[Dispatch spec compliance reviewer with its own planning dir]
Spec reviewer: Spec compliant - all requirements met, nothing extra

[Get git SHAs, dispatch manuscript reviewer]
Manuscript reviewer: Strengths: Good test coverage, clean. Issues: None. Approved.

[Aggregate: read agent findings, append to .writing/findings.md and progress.md]
[Mark Task 1 complete]

Task 2: Recovery modes

[Reuse .writing/agents/implementer/ (already exists from Task 1)]
[Dispatch implementation subagent with full task text + context + planning dir]

Implementer: [No questions, proceeds]
Implementer:
  - Added verify/repair modes
  - 8/8 tests passing
  - Self-review: All good
  - Committed

[Dispatch spec compliance reviewer]
Spec reviewer: Issues:
  - Missing: Progress reporting (spec says "report every 100 items")
  - Extra: Added --json flag (not requested)

[Implementer fixes issues]
Implementer: Removed --json flag, added progress reporting

[Spec reviewer reviews again]
Spec reviewer: Spec compliant now

[Dispatch manuscript reviewer]
Manuscript reviewer: Strengths: Solid. Issues (Important): Magic number (100)

[Implementer fixes]
Implementer: Extracted PROGRESS_INTERVAL constant

[Manuscript reviewer reviews again]
Manuscript reviewer: Approved

[Aggregate agent findings into .writing/]
[Mark Task 2 complete]

...

[After all tasks]
[Dispatch final manuscript reviewer]
Final reviewer: All requirements met, ready to merge

Done!
```

Observations worth noticing when you read this:

- The implementer subagent is welcome to ask questions before starting (Task 1). Answer clearly; don't rush them.
- Self-review inside the implementer (Task 1's `--force` flag, Task 2's "all good") is normal but not sufficient — both reviewers still run.
- Spec review caught both a missing requirement AND an added-scope item on Task 2. Those are distinct failure modes and a good reviewer will flag both.
- The reviewer re-runs after each fix. This is the "round" that gets counted against the 3-round cap.
- Between tasks, the implementer planning dir is reused — the same subagent identity, fresh invocation, persistent `findings.md`.
