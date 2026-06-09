# Novelty output template

The fixed output structure for Phase D, plus a worked CS example. The output is advisory. It is surfaced to the user and, on request, saved as `.writing/novelty-report.md`. It never mutates claim STATUS or any existing `.writing/` file.

## 1. Required structure

```markdown
## Novelty Gap Check (<ISO-8601 timestamp>)

### Proposed idea
<1-2 sentence restatement of the idea in the skill's own words>

### Core claims and per-claim delta
| # | Claim | Novelty | Closest prior work | Delta |
|---|-------|---------|--------------------|-------|
| 1 | <atomic claim> | HIGH/MED/LOW | <paper, [UNVERIFIED], or none found> | <one-line difference> |
| 2 | ... | ... | ... | ... |

### Closest prior work
| Paper | Year | Venue | Overlap | Key difference |
|-------|------|-------|---------|----------------|
| <title or [UNVERIFIED]> | <year> | <venue or preprint> | <what it shares> | <what we differ on> |

### Overall verdict
- Verdict: PROCEED / PROCEED-WITH-CAUTION / ABANDON
- Method vs finding: <method contribution, finding contribution, or both>
- Key differentiator: <what makes this unique, if anything>
- Reviewer risk: <the prior work a reviewer would cite against the idea>
- Search coverage: <queries run per claim, recency window covered>

### Suggested positioning
<2-4 sentences on how to frame the contribution to maximize defensible novelty>
```

## 2. Field rules

- **Core claims table**: one row per claim from Phase A, three to five rows. Novelty is HIGH, MED, or LOW from the rubric. Closest prior work is a verified paper, an `[UNVERIFIED]` candidate, or `none found`. Never blank.
- **Closest prior work table**: one row per distinct paper named across all claims. Leave a cell blank rather than guessing a field. Use `[UNVERIFIED]` in the Paper cell for unresolved candidates.
- **Method vs finding**: always state which kind of contribution the idea is. This is the rubric's Rule 2 surfaced for the user.
- **Search coverage**: state the query formulations and the recency window so the user can judge confidence in a "none found" result.
- **Suggested positioning**: concrete framing advice. Name the axis that carries the novelty and the prior work to position against. Not "make it sound more novel".

## 3. Worked example (CS / systems)

This example is illustrative. The papers and numbers are placeholders to show structure, not real citations.

```markdown
## Novelty Gap Check (2026-06-09T14:20:00Z)

### Proposed idea
A key-value store that uses a learned index to place hot keys in
non-volatile memory and cold keys on SSD, cutting tail latency under
skewed workloads.

### Core claims and per-claim delta
| # | Claim | Novelty | Closest prior work | Delta |
|---|-------|---------|--------------------|-------|
| 1 | Learned index predicts key placement across an NVM/SSD tier | MED | LearnedTiering 2025 (OSDI) | shares learned placement; we add a tail-latency objective |
| 2 | Placement objective optimizes p99 directly, not mean | HIGH | none found | no prior tiered store optimizes the tail objective directly |
| 3 | Online retraining tracks workload skew shifts | LOW | DriftIndex 2026 (NSDI) [UNVERIFIED] | identical online-retraining loop; resolve citation |

### Closest prior work
| Paper | Year | Venue | Overlap | Key difference |
|-------|------|-------|---------|----------------|
| LearnedTiering | 2025 | OSDI | learned key placement across tiers | optimizes mean latency, not p99 |
| DriftIndex | 2026 | NSDI [UNVERIFIED] | online retraining under drift | identifier unresolved; confirm before relying |

### Overall verdict
- Verdict: PROCEED-WITH-CAUTION
- Method vs finding: method contribution (the p99-direct placement objective)
- Key differentiator: directly optimizing the tail objective, which no prior tiered store does
- Reviewer risk: LearnedTiering will be cited as the placement precedent; the online-retraining claim is likely dominated
- Search coverage: 3 query formulations per claim (method name, problem framing, baseline framing); arXiv recency window covered through 2026-06

### Suggested positioning
Lead with the p99-direct objective as the single thesis, since that is
the HIGH claim. Frame learned placement as adopted infrastructure, not
a contribution, and cite LearnedTiering up front. Drop or demote the
online-retraining claim once DriftIndex is confirmed, or reframe it as
an engineering detail rather than a contribution.
```

## 4. Reading the example

- Claim 2 is HIGH and load-bearing, so the idea is not ABANDON.
- Claim 3 is LOW against a paper that is still `[UNVERIFIED]`. The verdict does not let an unverified paper force ABANDON. It flags the citation for resolution and recommends demoting the claim rather than killing the idea.
- The mix of one HIGH, one MED, one LOW with a load-bearing LOW lands at PROCEED-WITH-CAUTION, matching the rubric aggregation table.
- The positioning advice names the carrying axis (p99 objective) and the prior work to cite up front (LearnedTiering), rather than vague reassurance.

## 5. Persistence

When the user wants the output saved and a `.writing/` directory exists, write it to `.writing/novelty-report.md`. This sits alongside `verify-report.md` as an advisory artifact. It adds no claim STATUS and edits no existing file. Ask before writing. Do not create `.writing/` solely to hold the file. When no project state exists, deliver the output inline.
