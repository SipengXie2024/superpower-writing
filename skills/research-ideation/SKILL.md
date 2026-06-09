---
name: research-ideation
description: Generates a full slate of research directions before outlining, then ranks them so one survivor hands off to a paper structure. Produces 15-20 candidate directions through named lenses, scores them with a FINER rubric, runs a cross-model adversarial pass for taste calls, and flags AI-typical wording. Use when a research area is chosen but the contribution is not yet decided, or the user asks to brainstorm or find a research idea.
---

# Research Ideation

This is the idea-generation phase, the step before outlining. Outlining assumes the contribution is already decided. This skill is where the contribution gets decided. It turns a research area into a slate of candidate directions, ranks them, and hands the single surviving direction to outlining.

The deliverables are two files under `.writing/`:

1. `.writing/ideation.md` holds the candidate slate, the FINER scores, the cross-model adversarial pass result, and the rejected list.
2. `.writing/ideation-brief.md` holds the research-direction brief for the selected direction, formatted for outlining Step 1.

**Iron rule:** Generate the full candidate list of 15 to 20 directions before critiquing any of them. Premature convergence is the failure this skill exists to defeat. The first three ideas are never the best three.

**Separation rule:** Generation breadth and the accept verdict are strictly separated. The executor may drop a candidate only on an objective budget fact. Quality, novelty, and impact are decided by FINER scores plus a cross-model adversarial pass, never by the executor's solo taste.

**Advisory rule:** Every verdict here is advisory. Surface scores and objections to the user and let the user pick the surviving direction. Never auto-reject a candidate and never auto-mutate `.writing/` state without the user's choice.

**Never fabricate.** Do not invent papers, arXiv IDs, DOIs, citations, or numbers to justify or to sink a candidate. Mark an unconfirmed reference `[UNVERIFIED]` and move on. Fabrication at ideation contaminates every downstream stage.

## When To Use

Trigger this skill when:

- The user has chosen a research area but has not decided the contribution.
- The user says "brainstorm ideas", "find a research idea", "what can we work on", or asks to explore a direction for publishable contributions.
- Outlining was invoked but the core contribution is still a one-line vague phrase, so outlining routed back here.

Do NOT use this skill for:

- Refining an already-decided contribution into structure. That is `superpower-writing:outlining`.
- Designing a software feature or system component. That is `superpower-writing:brainstorming`.
- Retrieving specific papers or synthesizing a landscape. That is `superpower-writing:literature-review` and `superpower-writing:research-lookup`, which this skill calls.

## Two Modes

The skill has two modes. The default is generate-and-evaluate. The opt-in alternative is Socratic coaching.

- **Generate-and-evaluate (default).** Generate candidates, score them, run the adversarial pass, and produce a scored brief for the survivor. This is the path described in the Process below.
- **Socratic coaching (opt-in).** Drive the user to derive their own direction through questions. This mode does NOT produce a brief and does NOT score FINER for the user. See the Socratic Coaching Mode section.

Offer the Socratic mode only when the user signals they want to think it through themselves ("help me figure out my question", "coach me", "ask me questions"). Otherwise run the default.

## Checklist (default mode)

Run in order.

- [ ] Confirm the area is specific enough; if it is a bare field name, narrow it first.
- [ ] Phase 1: survey the landscape and note structural gaps.
- [ ] Phase 2: generate 15 to 20 candidates through the lenses, before any critique (iron rule).
- [ ] Phase 3: apply the objective budget gate only; annotate everything else.
- [ ] Phase 4: score survivors with the FINER rubric.
- [ ] Phase 5: run the cross-model adversarial pass for the taste calls.
- [ ] Phase 6: run the wording-pattern advisory on the leading candidates.
- [ ] Phase 7: present scores and objections; the user picks the survivor.
- [ ] Phase 8: write the brief and the rejected list; hand off to outlining.

## Process (default mode)

### Phase 0: Scope The Area

Read the user's area. If it is a bare field name ("NLP", "computer vision", "distributed systems"), stop and ask the user to narrow it. A workable area is one or two sentences naming a problem, a setting, and a constraint. "Sample efficiency of offline reinforcement learning from image observations" is workable. "Reinforcement learning" is not.

Without enough specificity, the candidates come out too vague to score and the whole slate is wasted.

If `.writing/` does not exist, run `${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh` to create it with canonical templates.

### Phase 1: Landscape Survey

Map the area to find where the gaps are. Ground the survey in real prior work.

```
Skill(skill="superpower-writing:literature-review")
```

Use it to synthesize the landscape: what is known, what is contested, what is missing. Follow up with targeted retrieval for specific papers, canonical datasets, or recent preprints.

```
Skill(skill="superpower-writing:research-lookup")
```

Record findings in `.writing/findings.md`. As you read, note the five structural gap types, because they map directly to the generative lenses in Phase 2:

- a method that works in domain A but is untried in domain B,
- contradictory findings between papers,
- an assumption everyone makes but nobody has tested,
- a scaling regime nobody has explored,
- a diagnostic question nobody has asked.

Never fabricate a citation to fill a gap. Mark unconfirmed references `[UNVERIFIED]`.

### Phase 2: Generate Candidates Through Lenses (iron rule)

Generate 15 to 20 candidate directions before critiquing any of them. This is the iron rule. Hold back every judgment until the full slate exists.

Run the area through each named lens, retargeted to CS, systems, and ML. The full catalog with prompts and worked examples lives in `references/lens-catalog.md`. Read it now. The lenses are:

- **method-transfer**, a method that works in domain A, untried in domain B.
- **contradiction**, two papers with conflicting findings to resolve.
- **untested-assumption**, a premise everyone shares but nobody has tested.
- **scaling-regime**, a regime at the edges that nobody has explored.
- **diagnostic**, a why-question nobody has asked.

For each lens, generate several candidates before moving to the next. Tag each candidate with the lens that produced it. Add a domain-specific lens when the area warrants one; the five are a floor, not a ceiling.

Each candidate carries a one-sentence summary, a core hypothesis, the cheapest experiment that would test it, the contribution type (empirical finding, new method, theoretical result, or diagnostic), a rough effort estimate, and the lens of origin.

**Optional cross-model generation seed.** A single Codex call can widen the pool with directions the executor would not reach. This is a generator, not a judge, so a same-family seed is fine. Write the landscape and gap summary to a bundle file, then delegate one brainstorm via `superpower-writing:collaborating-with-codex` (run the bridge in the background per that skill's contract). Merge Codex's directions into the pool. Do not let Codex critique here; its judging role comes in Phase 5.

Do not critique while generating. Capture even the candidates that feel weak. Dropping a candidate now defeats the breadth the lenses exist to create.

### Phase 3: Objective Budget Gate Only

This phase does NOT judge quality, novelty, or impact. Those are decided in Phases 4 and 5. Here the executor may drop a candidate only on an objective, mechanical budget fact:

- estimated compute exceeds one week of the available budget, or
- the candidate requires a dataset that is provably unavailable.

These are resource facts, not taste. Do not drop a candidate because the implementation "looks complex"; record complexity as an effort note instead. Do not drop a candidate because it "might already be done"; that is a novelty signal for the literature pass and the adversarial pass, not a budget fact.

For each surviving candidate, attach two annotations rather than eliminating:

- a `prior_work` note from two or three targeted searches (what looks related, with real links, never fabricated), and
- a `so_what` note in one line (why the result would matter either way).

Every feasible, non-duplicate candidate proceeds carrying its annotations. Typically only the budget-infeasible drop here.

### Phase 4: Score With FINER

Score every surviving candidate with the FINER rubric in `references/finer-rubric.md`. Read it now. FINER is Feasible, Interesting, Novel, Ethical, Relevant, each on a 1-to-5 scale with behavioral anchors.

Apply the rubric's pre-score gate first: a candidate must imply a methodology. If no concrete experiment, dataset, proof technique, or measurement comes to mind, the question is too vague. Mark it `too-vague` and return it for a sharper restatement rather than scoring it.

The accept threshold is an average of at least 3.0 with no single criterion below 2. A lone 1 sinks a candidate even when the average is high; name the criterion that failed. The threshold ranks and explains. It does not auto-reject.

The FINER novelty score is a hypothesis to test against the literature, never a fabricated certainty. A high novelty score still owes the user a real prior-work check.

### Phase 5: Cross-Model Adversarial Pass

"Would a reviewer care?" is the central taste call. The executor must not answer it alone. The executor is one model judging its own generated ideas, which voids any independence. Route the taste calls through a different model.

Choose one of two routes:

- **Codex (preferred).** Write the full annotated candidate set plus FINER scores to a bundle file, then delegate the adversarial pass via `superpower-writing:collaborating-with-codex`. Run the bridge in the background per that skill's contract. Ask Codex, for each leading candidate: the strongest objection a reviewer would raise, the most likely failure mode, whether the prior-work note is a real novelty problem or a differentiable one, and which two or three it would actually pursue and why.
- **Fresh-context Claude jury.** When Codex is unavailable, spawn a fresh-context Claude reviewer that has not seen the generation. Hand it only the candidate set and the same adversarial prompt. A reviewer that watched the ideas being born inherits the generator's blind spots, so the context must be fresh.

The cross-model ranking is the authoritative quality verdict. The executor does not narrow on its own taste before or instead of this pass. Its output is advisory to the user, not a silent filter.

Verify the returned reasoning yourself before surfacing it. A delegated summary states intent, not proof.

### Phase 6: Wording-Pattern Advisory (non-blocking)

Scan the leading candidate questions for an AI-typical shell. The most common is the impact-or-effect frame: "the impact of X on Y" or "the effect of X on Y". This frame names no mechanism, no metric, and no comparison, which is exactly why it reads as generic.

When a candidate matches the shell, raise a non-blocking advisory. The advisory does NOT say the idea is generic or bad. It flags only the wording, and it asks what a specialist would say instead.

```markdown
[WORDING_PATTERN_ADVISORY]
The phrasing "[the candidate question]" matches a common AI-typical shell: the impact/effect frame. This is not a judgment of the idea, only of the wording. What term, mechanism, or measurement would a specialist in this subfield use instead?
```

List the acceptable user choices every time:

- Keep the phrasing as is, for instance because it matches a target venue's framing.
- Rephrase in domain-native terms naming a concrete mechanism and metric.
- Ask for help stress-testing the scope without rewording the question.

The advisory is a signal for the user's attention. It never blocks a candidate and never edits the question on its own.

### Phase 7: Present And Let The User Choose

Present the ranked candidates with their FINER scores, the cross-model objections, any wording advisories, and the rejected list. Use `AskUserQuestion` to ask which direction to carry forward.

The user picks the survivor. The executor's ranking is advice, not a decision. A candidate below the FINER threshold may still be the user's choice if they want to restate it to lift the failing criterion.

### Phase 8: Write The Brief And Hand Off

Write `.writing/ideation.md` with the full slate, FINER table, adversarial-pass result, and the rejected list. The rejected list gives every non-selected candidate a one-line "why not selected" reason, using the rubric's format. Objective reasons only: cite a real paper for a novelty rejection, name the missing resource for a feasibility rejection. Never write "weak idea" as a reason.

Write `.writing/ideation-brief.md` for the selected direction, using the Research-Direction Brief format in `references/finer-rubric.md`. The brief states the direction in one sentence, the method it implies in two to four concrete steps, the FINER table, the scope boundaries, and the lens of origin.

Update `.writing/progress.md` with a one-line summary of the round (candidates generated, survivors, the selected direction).

**Handoff to outlining (prose description only; this skill does not edit outlining).** The brief is the input to outlining Step 1, which captures the research idea. Outlining Step 1 asks for three things: the core contribution in one sentence, the target venue or venue class, and the unit of evidence. The brief already supplies all three. The direction sentence is the core contribution. The relevance justification and the venue community named in the FINER scoring give the venue class. The method-implied steps name the unit of evidence, whether a dataset, a benchmark, a simulation, or a proof. When the user is ready, tell them the surviving direction is ready for outlining and invoke it.

```
Skill(skill="superpower-writing:outlining")
```

Outlining then converts the decided contribution into IMRAD structure and claim stubs. This skill never writes that structure itself.

## Socratic Coaching Mode (opt-in)

This mode is the alternative to the default. Activate it only when the user wants to derive their own direction through dialogue.

In this mode the skill does NOT produce a research-direction brief and does NOT score FINER for the user. It drives the user with questions until they converge on their own direction. The full question-banks and strategies live in `references/socratic-question-banks.md`. Read it before running this mode.

The mode draws on six question types (clarification, probing assumptions, probing evidence, probing perspectives, probing implications, and questioning the question) and five strategies (Funnel, Mirror, Counterfactual, Analogy, and Strategic Silence).

Dialogue rules:

- Ask one or two precise questions per turn. Keep each reply short. Affirm or restate before the follow-up.
- Aim to converge within about 15 rounds. If the user stalls after several rounds, offer to switch to the default generate-and-evaluate mode.
- If the user asks for a direct answer, gently decline and explain the value of deriving the direction themselves. The user may always exit to the default mode if they would rather be handed candidates.

When the dialogue converges, compile the user's own insights into a short Direction Summary (the format is in the question-banks reference). The summary is a self-assessment the user wrote with you, not a scored brief. If the user then wants a scored brief, switch to the default mode, which reads this summary and starts from FINER scoring rather than a blank page.

## Key Principles

**Breadth before judgment.** The iron rule, the full slate of 15 to 20 before any critique, is the whole point. Free brainstorming stalls on the first obvious directions. The lenses and the deferred critique force the slate wide enough that the best direction has a chance to appear.

**Generation and verdict are different jobs.** The executor generates and gates on budget facts. A different model, or FINER plus a fresh-context reviewer, decides quality. Letting the executor narrow on its own taste collapses the two jobs and reintroduces the premature convergence the iron rule defeats.

**The rejected list is reusable.** Every dead end with a one-line objective reason saves a future re-ideation from regenerating it. Document why, not just what.

**Advisory, never gatekeeping.** Scores, objections, and wording advisories surface to the user. The user picks the direction. The skill never auto-rejects and never mutates `.writing/` state without the user's choice.

**Never fabricate.** No invented papers, arXiv IDs, DOIs, or numbers, on either side of a verdict. Mark unconfirmed references `[UNVERIFIED]`. A fabricated novelty rejection is as corrupting as a fabricated citation in a draft.

**One direction hands off.** The output is a single surviving direction in a brief outlining can consume. This skill decides the contribution; outlining structures it. Keep the boundary clean.
