# FINER Candidate-Comparison Rubric

This rubric scores research-direction candidates so the surviving idea can hand off to outlining Step 1. The score is advisory. It ranks candidates and explains rejections. It never auto-drops a candidate on its own.

FINER stands for Feasible, Interesting, Novel, Ethical, Relevant. Score every candidate on all five criteria on a 1-to-5 scale. Use the behavioral anchors below so two passes on the same candidate land near the same number.

## Pre-Score Gate: Methodology Implication

Before scoring, apply one hard gate to each candidate.

A candidate must imply a methodology. If no concrete experiment, dataset, proof technique, or measurement comes to mind when you read the question, the question is too vague to score. Mark it `too-vague` and return it for a sharper restatement. Do not assign FINER numbers to a question that names no method.

Concrete enough to pass the gate:

- "Does activation steering transfer across model families at a fixed layer fraction?" implies a steering-vector extraction, a transfer test, and a layer sweep.
- "Can a learned cache-replacement policy beat LRU on production OLTP traces under a 2x memory budget?" implies a trace corpus, a baseline, and a memory cap.

Too vague to score, return for restatement:

- "What is the impact of attention on model performance?" names no mechanism, no metric, no comparison.
- "How does data quality affect training?" names no quality measure and no training regime.

## The Five Criteria With Behavioral Anchors

### Feasible

Can the work be done with available data, methods, compute, and time?

| Score | Behavioral anchor |
|-------|-------------------|
| 1 | Cannot be answered with any method or data the author can reach. Needs a dataset that does not exist or compute far past budget. |
| 2 | Answerable only with a major new system build or data-collection effort before any result lands. |
| 3 | Answerable with known methods and reachable data, but the pipeline is involved and risky. |
| 4 | Answerable with standard methods on accessible datasets; the main risk is engineering effort. |
| 5 | A clear pipeline exists end to end. Data, baselines, and compute are all in hand or one download away. |

### Interesting

Would the answer surprise someone, or settle a real puzzle?

| Score | Behavioral anchor |
|-------|-------------------|
| 1 | The answer is already common knowledge in the subfield. No one would change a decision. |
| 2 | The answer is mildly informative but expected either way. |
| 3 | The answer resolves a question some practitioners actually argue about. |
| 4 | The answer would change how a group designs systems or runs experiments. |
| 5 | The answer settles a live contradiction or overturns a widely held assumption. A specific reader would change their mind. |

### Novel

Does the direction offer a new method, new evidence, or a new framing?

| Score | Behavioral anchor |
|-------|-------------------|
| 1 | Fully duplicates published work the author can already cite. |
| 2 | A minor variation on an existing paper with no new mechanism. |
| 3 | A new combination of known parts, or known method applied to a genuinely untried setting. |
| 4 | A new method, a new measurement, or first evidence on an open question. |
| 5 | A new framing that reorganizes how the subfield states the problem. |

Novelty here is a signal, not a verdict. The authoritative novelty check is a literature pass plus the cross-model adversarial pass described in the SKILL. Do not score 5 on memory alone; a high novelty score is a hypothesis to test against the literature, never a fabricated certainty.

### Ethical

Does the work raise harm, dual-use, consent, or data-provenance concerns?

| Score | Behavioral anchor |
|-------|-------------------|
| 1 | Significant harm or clear dual-use risk with no mitigation in sight. |
| 2 | Notable concern that needs an explicit mitigation plan before the work proceeds. |
| 3 | Minor concern, addressable with a standard statement or a data-use check. |
| 4 | Low concern; uses public data or simulation with clear provenance. |
| 5 | No discernible ethical issue; benefits clearly outweigh negligible risk. |

For most CS, systems, and ML work this scores 4 or 5. Score lower for human-subjects data, scraped data of unclear provenance, capability work with obvious misuse paths, or energy-intensive training the author cannot justify.

### Relevant

Does answering the question inform practice, theory, or a real community need?

| Score | Behavioral anchor |
|-------|-------------------|
| 1 | No practical or theoretical consequence; answers a question no one asked. |
| 2 | Narrow relevance to a single niche with no wider pull. |
| 3 | Relevant to one active research line or one class of systems. |
| 4 | Relevant across several research lines or to a deployed-systems concern. |
| 5 | Directly informs a pressing problem a target venue's community cares about now. |

Anchor relevance to a concrete venue community when one is known: NeurIPS, ICML, ICLR for ML; OSDI, NSDI, SOSP, EuroSys for systems; POPL, PLDI, CAV for programming languages and verification; S&P, USENIX Security, CCS for security; SIGMOD, VLDB for databases.

## Accept Threshold

A candidate clears the FINER bar when both hold:

- average score across the five criteria is at least 3.0, and
- no single criterion scores below 2.

A single 1 sinks a candidate even if the average is high. A direction that is brilliant but provably infeasible, or important but unethical, does not survive. State which criterion failed.

The threshold ranks and explains. It does not auto-reject. Surface every candidate's scores and let the user decide which surviving direction to carry forward. A candidate below threshold may still be worth a restatement that lifts the failing criterion.

## Output: Brief Plus Rejected List

Produce two artifacts.

### Research-Direction Brief (for the selected candidate)

```markdown
## Research-Direction Brief

### Direction
[The selected direction in one sentence, ending in a question or a falsifiable claim.]

### Method Implied
[2 to 4 concrete steps: what we build, train, run, or prove. Plain language, no jargon.]

### FINER Assessment
| Criterion | Score | Justification |
|-----------|-------|---------------|
| Feasible    | X/5 | ... |
| Interesting | X/5 | ... |
| Novel       | X/5 | ... |
| Ethical     | X/5 | ... |
| Relevant    | X/5 | ... |
| **Average** | **X.X/5** | |

### Scope Boundaries
- In scope: [datasets, regimes, baselines, the one core comparison]
- Out of scope: [excluded directions with one-line rationale]
- Key assumptions: [what the direction rests on]

### Lens Of Origin
[Which generative lens produced this: method-transfer / contradiction / untested-assumption / scaling-regime / diagnostic / domain-specific.]
```

### Rejected List (for every candidate not selected)

Every candidate that does not carry forward gets a one-line "why not selected" reason. This is the most reusable artifact: it documents dead ends so a later re-ideation does not regenerate them.

```markdown
## Candidates Considered

| # | Candidate (one line) | FINER Avg | Why not selected |
|---|----------------------|-----------|------------------|
| 1 | [selected] | X.X | Selected |
| 2 | ... | X.X | Feasible=1: needs a dataset that does not exist |
| 3 | ... | X.X | Novel=2: subsumed by [paper or preprint, cited, not fabricated] |
| 4 | ... | too-vague | Implies no methodology; returned for restatement |
```

Reasons must be objective and specific. Cite a real paper for a novelty rejection, or name the missing resource for a feasibility rejection. Never write "weak idea" or "a reviewer would not care" as a reason. Those are taste calls that belong to the cross-model adversarial pass, not to the executor's solo judgment.

## Quality Criteria For The Selected Direction

- States as a single clear sentence, ending in a question mark or a falsifiable claim.
- No compound question. Avoid "and" or "or" joining two separate inquiries.
- Implies a methodology. If no method comes to mind, the direction is too vague.
- Answerable within realistic constraints on time, data, and compute.
