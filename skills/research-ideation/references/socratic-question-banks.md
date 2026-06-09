# Socratic Question-Banks And Strategies

This reference powers the opt-in Socratic coaching mode. In that mode the skill does NOT produce a research-direction brief and does NOT score FINER for the user. It drives the user to derive the direction themselves through questions.

Use these banks as a toolkit, not a script. Pick the questions that fit the natural flow of the dialogue. Ask one or two precise questions per turn, keep each reply short, and let the user do the thinking.

The mode follows a convergence limit. Aim to converge within about 15 rounds. If the user cannot converge after several rounds in problem framing, you may offer to switch to the default generate-and-evaluate mode rather than looping forever.

## Six Question Types

### Type 1: Clarification

Make sure the user actually means what they say.

- What do you mean by "X"?
- Can you give a concrete example?
- Can you state that another way?
- How is this different from Y?
- What does X include, and what does it exclude?

### Type 2: Probing Assumptions

Surface hidden premises.

- What are you assuming here?
- Is that assumption justified?
- What if the assumption does not hold?
- Why do you take that for granted?
- Does anyone in the field disagree with that premise? Why?

### Type 3: Probing Evidence

Test the basis for a claim.

- What is your evidence?
- How do you know that is true?
- What other result supports or contradicts it?
- Is that evidence sufficient for the claim?
- How would you answer a reviewer who doubts the measurement?

### Type 4: Probing Perspectives

Break a single viewpoint.

- How would this look from another angle?
- What would someone who disagrees say?
- If you were a systems person rather than an ML person, how would you frame it?
- Why might others read this differently?
- Does an adjacent subfield frame the same phenomenon differently?

### Type 5: Probing Implications

Trace consequences.

- If this is correct, what does it imply?
- What is the practical consequence for a system or a user?
- What are the best and worst cases?
- Who benefits, and who is harmed or excluded?
- Where does this trend lead at the next scale?

### Type 6: Questioning The Question

Examine whether the question is the right one.

- Why does this question matter?
- Is there a better way to frame it?
- What is the question behind the question?
- What if this is the wrong question?
- What must be true before the question can be answered at all?

## Topic Question-Banks (CS And ML)

### Direction Clarification

1. Are you asking a "whether" question, a "how much" question, or a "why" question?
2. Can you state the direction in one sentence? If it needs more than one, it may be two directions.
3. If you could run exactly one experiment, what would it measure?
4. Does the direction already assume its answer? If so, that is a hypothesis, not yet a question.
5. A year from now, what do you hope this work will have settled?

### Method Probing

1. Did you pick this method because it fits the question, or because you know it best?
2. What alternative explanations can your design rule out, and which can it not?
3. Would the conclusion survive at half the compute or half the data?
4. Does your metric actually measure what you care about, or a convenient proxy?
5. Would another group reach the same result with the same setup?

### Literature Positioning

1. What is the dominant approach in this line? Are you extending it or challenging it?
2. If this work is a reply, who are you replying to?
3. Which once-standard result in this area is now considered wrong, and why?
4. Do the papers you lean on share a blind spot?
5. Have you deliberately searched for work that contradicts your view?

### Analytical Reasoning

1. Is the effect you expect correlation or causation, and how would you tell them apart?
2. Where does your evaluation protocol come from? Has it been criticized?
3. If a colleague saw your results without your hypothesis, what would they conclude?
4. Are there cases that break your expected pattern? How would you handle them?
5. Have you tried to design the experiment that would disprove your own hypothesis?

### Contribution And Significance

1. If this work were never published, what would the field lose?
2. Can you explain why it matters in three sentences to someone outside your subfield?
3. Is this "filling a gap" or "changing how we understand the problem"? These differ in value.
4. Will this still be cited in five years? Why?
5. Which pressing problem in the field does this connect to?

## Five Questioning Strategies

### Funnel

Move from open to focused, narrowing scope each turn.

```
Q1: "What part of efficient inference interests you?"        (open)
Q2: "You mentioned KV-cache memory. What about it?"          (focused)
Q3: "Where exactly does the standard eviction policy fail?"  (more focused)
Q4: "So you are asking: can a learned policy beat it under a memory cap?" (precise)
```

### Mirror

Restate the user's words, then follow up.

```
User: "Bigger models always reason better."
Mentor: "You are saying scale and reasoning rise together. Is there a regime where they decouple? Have you seen a small model beat a large one on a reasoning task?"
```

### Counterfactual

Imagine the opposite outcome to test the reasoning.

```
User: "Retrieval augmentation always improves factuality."
Mentor: "Suppose a system with no retrieval scored higher on factuality than one with it. How would you explain that, and would it change your question?"
```

### Analogy

Borrow a pattern from another domain.

```
User: "I want to study whether merging two models helps."
Mentor: "In databases, merging indexes often hurts before it helps, because of contention. Could model merging follow a similar curve? What is the analogue of contention here?"
```

### Strategic Silence

Sometimes the best move is to wait and let the user finish a half-formed thought.

```
User: "I think... maybe... actually I am not sure."
Mentor: "Take your time. You said you are not sure. Is it the question itself, or your stance on it?"
```

## Dialogue Management Rules

- Keep each reply short. One or two precise follow-up questions per turn.
- Affirm or restate in a sentence before the follow-up, so the user feels heard.
- Let the user request a jump to the next topic at any time.
- Extract a short insight note after each exchange, so the thread accumulates the user's own reasoning.
- Aim to converge within about 15 rounds. If the user stalls after several rounds, offer to switch to the default generate-and-evaluate mode.
- If the user asks for a direct answer, gently decline and explain that the value here is in deriving the direction themselves. The user may always exit to the default mode if they prefer to be handed candidates.

## What The Coaching Mode Produces

When the dialogue converges, compile the user's own insights into a short summary the user wrote with you. This summary is a self-assessment, not a scored brief.

```markdown
## Direction Summary (Socratic Mode)

### Direction (in the user's words)
[The direction the user converged on, in one sentence.]

### User's Own FINER Read (self-assessment, unscored)
- Feasible: [what the user said about data, compute, time]
- Interesting: [who the user thinks would care, and why]
- Novel: [where the user thinks the gap is]
- Ethical: [any concern the user raised]
- Relevant: [the practice or theory the user thinks it informs]

### Scope The User Chose
- Focus: [the scope the user picked]
- Excluded: [what the user decided to leave out]
- Still open: [scope questions not yet resolved]
```

If the user then wants a scored brief, they can switch to the default mode. The default mode reads this summary and starts from FINER scoring rather than from a blank page.
