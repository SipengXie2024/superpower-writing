---
name: idea
description: Turns a chosen research area into publishable directions through three internal phases. It generates candidates with named lenses and FINER scoring, adjudicates novelty per technical claim against prior work, then evaluates against a top-venue bar with a fatal-flaw short-circuit. All verdicts stay advisory. Use when a research direction is undecided, when choosing a topic, when evaluating an idea, or when checking novelty (查新).
---

# Idea

This is the idea phase, the step before outlining. Outlining assumes the contribution is already decided. This skill is where the contribution gets decided, sanity-checked, and handed off. It has three internal phases that compose into one flow but also trigger on their own.

1. **Generate candidate directions.** Turn a research area into a wide slate of candidates through named lenses, score them with FINER, and rank them. Output goes to `.writing/ideation.md`.
2. **Adjudicate novelty.** Decompose the leading idea into three to five core technical claims, search prior work per claim, and emit a per-claim HIGH/MED/LOW delta with an overall PROCEED / PROCEED-WITH-CAUTION / ABANDON call.
3. **Evaluate against a top-venue bar.** Audit fatal flaws first and short-circuit on any CRITICAL one, then read the idea on five framing dimensions and issue Strong Accept, Accept with Revisions, or Reject and Pivot.

Run all three in sequence for a fresh area, or jump straight to Phase 2 or Phase 3 when the user already has an idea in hand. Every verdict here is advisory. The user picks the surviving direction; this skill never auto-rejects and never proceeds to a downstream skill on its own.

## Shared Rules (all three phases)

**Advisory, never gatekeeping.** Scores, deltas, and verdicts surface to the user. The user chooses. This skill never auto-rejects a candidate, never flips claim STATUS, and never mutates `.writing/` state without the user's choice.

**Never fabricate.** Do not invent papers, arXiv IDs, DOIs, venues, years, or numbers to justify or to sink an idea. Mark an unconfirmed reference `[UNVERIFIED]` and keep it visible. Fabrication at the idea stage contaminates every downstream stage. Full protocol in [citation discipline](references/citation-discipline.md). This is the one mechanical line that stays hard: strong models still invent citations, so evidence integrity is checked, not trusted.

**Retrieval is delegated, not rebuilt.** This skill judges ideas. It does not run its own search backend. Whenever a phase needs prior work, a landscape survey, or a per-claim search, delegate to the merged retrieval skill:

```
Skill(skill="superpower-writing:literature")
```

That skill routes academic queries to scholarly backends and Zotero, and saves raw results under `sources/`. Read the returned candidates before recording any overlap. Overlap is judged on substance, not title similarity.

**State and persistence.** Phase 1 writes `.writing/ideation.md` and `.writing/ideation-brief.md`. If `.writing/` does not exist, run `${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh` first. Phases 2 and 3 are read-mostly. They surface their report in chat. On request, and only when a `.writing/` directory already exists, save the novelty report to `.writing/novelty-report.md`. Do not create `.writing/` just to hold an evaluation.

## When To Use

- The user has chosen a research area but has not decided the contribution ("brainstorm ideas", "find a research idea", "what can we work on", "选题").
- The user asks whether an idea is novel ("is this novel", "查新", "has anyone done this", "check novelty").
- The user asks to evaluate, score, or sanity-check an idea before committing scope ("evaluate this idea", "is this a good direction", "would a reviewer buy this").
- Outlining was invoked but the core contribution is still a vague one-liner, so it routed back here.

Do NOT use this skill for:

- Refining an already-decided contribution into structure. That is `superpower-writing:outlining`.
- Retrieving papers or synthesizing a landscape. That is `superpower-writing:literature`, which this skill calls.
- Verifying citations already in a manuscript. That is `superpower-writing:claim-verification`.

---

## Phase 1: Generate Candidate Directions

The goal is a wide slate, ranked, with one survivor briefed for outlining.

**Breadth before judgment (the core discipline).** Generate 15 to 20 candidate directions before critiquing any of them. Premature convergence is the failure this phase exists to defeat. The first three ideas are never the best three. Hold every quality judgment until the full slate exists. Capture even the candidates that feel weak; weakness is a downstream reading, not a reason to drop a candidate mid-generation.

### Step 1: Scope the area

Read the user's area. If it is a bare field name ("NLP", "distributed systems"), stop and ask them to narrow it. A workable area names a problem, a setting, and a constraint in one or two sentences. Without that specificity the candidates come out too vague to score.

### Step 2: Survey the landscape

Delegate a landscape survey to `superpower-writing:literature` to ground generation in real prior work. As you read, note the five structural gap types, since they map onto the generative lenses: a method untried in a new domain, contradictory findings, an untested shared assumption, an unexplored scaling regime, and an unasked diagnostic question. Record findings in `.writing/findings.md`. Never fabricate a citation to fill a gap.

### Step 3: Generate through the lenses

Run the area through each named lens, retargeted to CS, systems, and ML. Read the full catalog with prompts and worked examples in [lens catalog](references/lens-catalog.md). The lenses are method-transfer, contradiction, untested-assumption, scaling-regime, and diagnostic. Add a domain-specific lens when the area warrants one. For each lens generate several candidates before moving on, and tag each candidate with its lens of origin.

Each candidate carries a one-sentence summary, a core hypothesis, the cheapest experiment that would test it, the contribution type (empirical finding, new method, theoretical result, or diagnostic), a rough effort estimate, and its lens.

Drop a candidate here only on an objective, mechanical fact: its compute clearly exceeds the budget, or it needs a dataset that provably does not exist. Do not drop on taste ("looks complex", "might already be done"). Complexity is an effort note; possible prior work is a Phase 2 question.

### Step 4: Score with FINER and rank

Score every surviving candidate with the rubric in [FINER rubric](references/finer-rubric.md). FINER is Feasible, Interesting, Novel, Ethical, Relevant, each 1 to 5 with behavioral anchors. First read each candidate for a methodology: if no concrete experiment, dataset, proof technique, or measurement comes to mind, mark it `too-vague` and return it for a sharper restatement rather than pinning numbers on it.

The FINER numbers rank and explain. They are reading aids for the user, not a gate this skill enforces. A candidate that reads as low may still be the user's pick after a restatement that lifts the weak criterion. The Novel score here is a hypothesis, not a settled fact; the authoritative check is Phase 2.

### Step 5: Wording advisory (non-blocking)

Scan the leading candidate questions for an AI-typical shell, most often the impact-or-effect frame ("the impact of X on Y"). This frame names no mechanism, metric, or comparison, which is why it reads as generic. When a candidate matches, raise a non-blocking note: it flags only the wording, not the idea, and asks what term a specialist would use instead. Let the user keep, rephrase, or ignore it. The advisory never edits the question on its own.

### Step 6: Present, choose, and hand off

Present the ranked candidates with their FINER scores, any cross-model objections, and the wording advisories. Use `AskUserQuestion` to ask which direction to carry forward. The user picks; the ranking is advice.

Then write two files. `.writing/ideation.md` holds the full slate, the FINER table, any cross-model result, and a rejected list that gives every non-selected candidate a one-line objective reason (cite a real paper for a novelty rejection, name the missing resource for a feasibility one; never "weak idea"). `.writing/ideation-brief.md` holds the selected direction in the brief format from the FINER rubric: the direction in one sentence, the method it implies in two to four steps, the FINER table, scope boundaries, and the lens of origin. Update `.writing/progress.md` with a one-line round summary.

The brief is the input to outlining, which captures the contribution, the target venue, and the unit of evidence. When the user is ready, tell them the direction is ready and invoke `superpower-writing:outlining`. This skill decides the contribution; outlining structures it.

### Socratic coaching (opt-in alternative)

When the user signals they want to think it through themselves ("coach me", "ask me questions", "help me figure out my question"), run the opt-in Socratic mode instead of generate-and-evaluate. This mode drives the user to derive their own direction through questions. It does not score FINER and does not produce a brief. The question banks and strategies are in [socratic question banks](references/socratic-question-banks.md). When the dialogue converges, compile the user's own insights into a short Direction Summary. If the user then wants a scored brief, switch back to the default path, which reads that summary and starts from FINER scoring.

---

## Phase 2: Adjudicate Novelty

This is the verdict-and-positioning layer for novelty. Retrieval is delegated (see Shared Rules); the value added here is the judgment on top: closest prior work per claim, the delta, and how to frame the contribution. Be brutally honest. Surfacing a strong prior-work overlap early is the most valuable thing this phase does, because a false novelty claim wastes months.

### Step 1: Decompose into core claims

Extract three to five core technical claims that would each have to be novel for the idea to count as novel. Write each as a single assertion with a truth value, not a topic. "We apply contrastive pretraining to graph kernels" is a claim; "graph learning" is not. Keep claims atomic; do not bundle a method and a finding into one claim, split them. If the idea is too vague to yield testable claims, stop and ask the user to restate it.

### Step 2: Per-claim prior-work search

For each claim, delegate the search to `superpower-writing:literature`. Use at least three query formulations per claim, varying the method name, the problem framing, and the closest-baseline framing, because one phrasing misses papers a synonym would catch. Always cover the most recent six months of arXiv as a hard floor; a claim that looks novel against last year's papers can be dead against a recent preprint. When the idea spans several subfields, ask for one deeper multi-subfield sweep rather than repeating the shallow search. Verify every candidate paper before it enters the report, per the citation discipline.

### Step 3: Per-claim delta and overall verdict

For each claim, assign HIGH, MED, or LOW novelty against the closest prior work, using [novelty rubric](references/novelty-rubric.md). Two rules carry most of the weight. Applying X to Y is not novel unless the application reveals a surprising insight; naming a new pairing is not a contribution by itself. And if the method is not novel but the finding would be, say so explicitly and label which kind of contribution the idea is.

Aggregate the per-claim deltas to one advisory call: PROCEED when at least one core claim is HIGH and no load-bearing claim is LOW; PROCEED-WITH-CAUTION when the strongest claim is MED or a HIGH claim sits next to a load-bearing LOW; ABANDON when every core claim is LOW against recent prior work. The aggregation table is a reading aid, not a switch. An `[UNVERIFIED]` paper must not force an ABANDON on its own.
### Step 4: Emit the novelty report

Surface the verdict in the fixed structure from [novelty report template](references/novelty-report-template.md): the restated idea, the per-claim delta table, the closest-prior-work table, the overall verdict with method-vs-finding and reviewer risk, and suggested positioning. Deliver it in chat, or save it to `.writing/novelty-report.md` on request per the Shared Rules.

---

## Phase 3: Evaluate Against A Top-Venue Bar

Evaluate one idea the way a top systems or ML reviewer would (NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP). Novelty and significance are the axes that decide acceptance there; a competent application of a known toolkit is rejected even when well executed. The point is to kill a doomed idea cheaply, before weeks of drafting.

Before scoring, confirm the idea is concrete: a one-sentence contribution, a target venue or class, the closest prior work and what this idea adds, and the stated resources. If the user cannot state the contribution in one sentence, it is not ready to evaluate; route back to Phase 1 to sharpen it.

### Step 1: First impression

State whether the idea reads as a Novel Problem, a Novel Method, or a New Setting. Then force the contribution into one sentence: "We show that approach A improves baseline B on axis C, measured by metric M, which changes how the field does task Q." Each blank that cannot be filled names a specific gap. An empty baseline means no reference point; an empty metric means the win cannot be measured. A sentence with two empty blanks usually predicts a Reject and Pivot before any scoring.

### Step 2: Fatal-flaws audit (short-circuit)

Run the audit FIRST, before any scoring. Read [fatal flaws](references/fatal-flaws.md), which holds the ten canonical flaws with detection questions, defenses, and the time-based severity rule. Identify at most two flaws. For each, name it, apply its detection question, propose a concrete defense, and tag severity: CRITICAL if it cannot be defended within the project lifecycle or two or more MAJOR flaws stack, MAJOR if the defense needs two to four weeks, MINOR if it clears in under a week.

**Short-circuit.** If any flaw is CRITICAL, stop and emit the rejection directly: Reject and Pivot, with the first impression and the fatal-flaws table only. Do not score. A CRITICAL flaw is dispositive, so scoring around it is wasted motion that misleads the user about salvageability. If no flaw is CRITICAL, continue.

### Step 3: Read the five dimensions and the FINER gate

Read the idea on the Higher, Faster, Stronger, Cheaper, Broader framing axes, using [five dimensions](references/five-dimensions.md). Default every axis to 5 and earn each point upward with a specific sentence from the idea; scoring everything 7 or 8 destroys the signal the verdict rests on. Each score cites evidence from the stated contribution, never a gut feeling. Name the two or three axes with the highest ceiling; those become the paper's thesis.

Then read the idea on the FINER framing (Feasible, Interesting, Novel, Ethical, Relevant) to catch what the five dimensions miss: ethics, feasibility, and whether the question even implies a method. The must-imply-a-methodology read is the firm one: an idea that names no experiment or construction is too vague to reach Strong Accept, and routes back to Phase 1 to sharpen.

Also assess feasibility against the user's stated resources (compute, data, engineering, timeline), and propose a mitigation for any high risk. Feasibility claims reference the stated resources, not generic assumptions.

### Step 4: Verdict

Before emitting, sanity-check the evidence integrity: every score cites a sentence from the idea, novelty claims cite specific prior work or are marked `[UNVERIFIED]`, and the verdict matches the reading rather than contradicting it. Then issue one advisory verdict.

- **Strong Accept**: execute now. The idea dominates a couple of framing dimensions, has no CRITICAL flaw, clears the FINER methodology read, and feasibility is green.
- **Accept with Revisions**: reshape scope first. Some dimensions are weak, only fixable (MAJOR or MINOR) flaws remain, or a feasibility risk has a stated mitigation.
- **Reject and Pivot**: do not pursue this version. A CRITICAL flaw, an idea thin across every dimension, or more than two fatal flaws.

Present the verdict, the evidence behind it, and the top three actions. Then stop and let the user decide.

**Paradigm-shift note (framing lever, not a score).** A high-ceiling idea often challenges something the field takes for granted. Ask whether it overturns a hidden assumption, tackles an avoided elephant-in-the-room problem, rides a technology shift that just made an old approach feasible, or would change the field if solved. Two or more yes answers signal disruptive potential worth leading the introduction with. Cite which question was answered yes; do not assert disruption without it.

---

## How The Phases Connect

The phases compose but stay independently triggerable.

- A fresh area runs Phase 1, then Phase 2 on the surviving direction, then Phase 3 before committing scope, then hands the brief to outlining.
- "Is this novel" runs Phase 2 alone.
- "Evaluate this idea" runs Phase 3 alone, where the Phase 2 novelty delta feeds the F1 fatal-flaw check directly.

The verdicts do not chain automatically. Each surfaces to the user, who decides whether to proceed, restate, pivot, or abandon. One surviving direction, in a brief outlining can consume, is the clean output of the whole skill.

## Key Principles

**Breadth before judgment.** The full slate of 15 to 20 before any critique is the whole point of Phase 1. The lenses and deferred critique force the pool wide enough that the best direction has a chance to appear.

**Generation and verdict are different jobs.** The executor generates and gates only on objective budget facts. Quality, novelty, and taste are decided by the rubrics, the user, and an optional different model, never by the executor's solo taste mid-generation.

**Decompose before you judge novelty.** A novelty check on a whole idea is mush. A check on three to five atomic claims is auditable. The per-claim table is the artifact a user and a reviewer can both reason about.

**Short-circuit before scoring.** A CRITICAL fatal flaw is dispositive. Scoring around it wastes the user's reading time and implies salvageability that is not there. Stop at the first CRITICAL flaw and reject.

**Verdicts are advisory, evidence is checked.** Every recommendation surfaces to the user, who owns the decision. The one hard line is fabrication: no invented papers, IDs, or numbers on either side of a verdict. Mark unconfirmed references `[UNVERIFIED]` and keep them in view.
