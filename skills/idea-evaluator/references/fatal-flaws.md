# Fatal Flaws in Research Ideas

Reference for `idea-evaluator` Step 2. Ten canonical fatal flaws, each with a question-style detection rule and a concrete defense, plus the time-based severity rule that drives the short-circuit.

## What counts as fatal

A fatal flaw causes rejection from a top venue regardless of how well the rest of the paper is executed. The bar is deliberately high. Not every weakness is fatal. Calling an idea fatally flawed stops the user from pursuing it, so this list stays conservative.

A fatal flaw has three signatures. It is visible in the idea description itself, not only discovered during experiments. It cannot be fixed by stronger baselines or better writing alone. And reviewers will flag it in the first review round.

The cap is at most two fatal flaws per idea. If the list runs past two, the direction itself is wrong and the verdict is Reject and Pivot.

## The ten flaws

Each flaw below carries a detection question. Ask the question of the idea. If the red flag fires, the flaw is present.

### F1: No novelty versus the closest prior work

The idea barely varies a published baseline in the same subfield. Reviewers frame it as "dominated by prior work X".

- Detection: what does this idea add over the single closest prior work, in one sentence?
- Red flag: the user cannot name a specific contribution in one sentence, or the contribution is "we use a bigger model" or "we combine two existing methods".

### F2: Wrong venue fit

The contribution matches a different venue than the one targeted. A systems contribution sent to ICML is often rejected even when strong; a pure-theory result sent to OSDI meets the same fate.

- Detection: what is the target venue, and what are three representative papers from its most recent edition?
- Red flag: the idea's contribution type does not appear in those three papers.

### F3: Baseline is not the real baseline

The chosen baseline is weak or outdated. Beating a 2023 method in 2026 convinces no one; reviewers demand the current strongest public result.

- Detection: what is the strongest public result on the target benchmark within the last three months?
- Red flag: the user's baseline is more than twelve months old, or it does not cite a current-year result. Do not invent a SOTA number to fill this gap; if the user has not checked, mark the recency claim `[UNVERIFIED]`.

### F4: No compelling motivation

The real-world usefulness is unclear. The idea cannot answer "who cares, and why now"; reviewers call this "not motivated".

- Detection: if this problem were solved tomorrow, who benefits, and how much?
- Red flag: the answer is "other researchers studying this narrow problem" with no external beneficiary named (a user, a deployed system, a downstream task).

### F5: Resource or capability mismatch

The idea is valid, but the stated resources cannot execute it within its lifecycle. Wrong skill stack, too little time, or missing hardware causes a missed deadline or an incomplete paper.

- Detection: do the stated compute, data, skills, and timeline cover the full idea, including experiments, writing, and revision?
- Red flag: two or more of those four are clearly short of what the idea demands.

### F6: Unverifiable claim

The idea rests on an empirical claim no planned experiment can test. Example: "our method generalizes across domains", but no cross-domain experiment is in scope.

- Detection: what single experiment, if it produced a specific result, would prove the main claim?
- Red flag: the user cannot design that experiment, or it falls outside the stated scope and resources.

### F7: Ethical or data-access blocker

The idea needs data, human subjects, or infrastructure the user cannot access. Missing IRB approval, proprietary data, a privacy constraint, or unavailable compute makes execution impossible.

- Detection: is every required resource currently accessible, including IRB approval where human subjects are involved?
- Red flag: any required resource is missing and cannot be secured within the idea's lifecycle.

### F8: Overly ambitious scope

The contribution list promises too much. Example: "a new benchmark, a new method, a theoretical analysis, and a deployed system" in one paper. Each contribution undercuts the others; reviewers flag "unfocused".

- Detection: count the contribution bullets in the proposed introduction.
- Red flag: more than four bullets, or the bullets span distinct paper types (benchmark plus method plus theory plus system).

### F9: Solution hunting for a problem

The idea starts from a technique the user wants to apply and searches for a problem it fits. This produces contrived problems and indecisive experiments. This flaw inverts the generative discipline the scoring uses. Disciplined idea generation starts from a baseline and asks what to improve. It never starts from a solution and hunts for somewhere to use it.

- Detection: did the user hit this problem in practice, or start from a technique they wanted to use?
- Red flag: the user cannot name a concrete real-world failure that motivated the work.

### F10: No failure case considered

The idea treats the method as a silver bullet. There is no account of where it fails, under what conditions, or what its limits are. Reviewers flag overclaiming.

- Detection: under what conditions does the method fail, and what goes in the Limitations section?
- Red flag: the user cannot name two failure modes.

## Defenses

For each flaw, a concrete defense. If the defense cannot run within the idea's lifecycle, the flaw stays fatal.

| Flaw | Defense |
|---|---|
| F1 | Position against the closest prior work in one sentence. Name the specific axis on which this idea dominates |
| F2 | Either retarget the venue to match the contribution type, or reshape the contribution to fit the original venue |
| F3 | Identify the current strongest public result and add it as the primary baseline. If unavailable, document the recency cutoff and justify it |
| F4 | Name a concrete external beneficiary (a user, a deployed system, a downstream task) in the first paragraph of the introduction |
| F5 | Narrow the scope, find a collaborator for the missing skill, or pivot to a category the resources can execute |
| F6 | Design the decisive experiment explicitly and put it first in the experiments plan. If infeasible, pivot the claim |
| F7 | Secure access before proceeding. File IRB early; secure a data partnership; reserve the compute |
| F8 | Cut the contribution list to two or three items. Split the rest into a follow-up paper |
| F9 | Restart from the problem side. Document a real failure, run a pilot, or pick a baseline and ask which axis to improve |
| F10 | Name two failure modes and plan a Limitations section before experiments. Include failure cases in the evaluation |

## Severity rule (drives the short-circuit)

After listing flaws and defenses, tag each flaw by how long its defense takes. The time anchors are deliberate, because "how fixable is this" is the only question that matters for the verdict.

- **CRITICAL**: the flaw cannot be defended within the project lifecycle given current resources, OR two or more MAJOR flaws are present together.
- **MAJOR**: the defense needs two to four weeks of dedicated work.
- **MINOR**: the defense clears in under a week of writing or literature work.

Verdict implications:

- **Any CRITICAL flaw**: Reject and Pivot. Stop the evaluation and emit the rejection. Do not score. This is the short-circuit the main skill enforces in Step 2.
- **Two or more MAJOR flaws**: Accept with Revisions. Defend every flaw before experiments start.
- **At most one MAJOR flaw, plus any MINOR flaws**: compatible with Strong Accept, subject to the rest of the evaluation.

The lifecycle is the project's own horizon, not a fixed number. A flaw that takes three weeks is MAJOR for a three-month project and CRITICAL for a two-week deadline. Judge "unfixable" against the lifecycle the user stated, not against a generic calendar.
