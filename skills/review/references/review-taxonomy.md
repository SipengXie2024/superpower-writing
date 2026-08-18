# Review Taxonomy and Calibration

A shared issue taxonomy and calibration rules for both review modes. This file is a review *standard*, part of the output shape a brief may pass to either critic under the independence rules in `references/cadence-and-independence.md`. It never carries paper content, summaries, or the executor's interpretation.

Use it two ways:

- **In a venue brief**: name this file among the files the critic reads, and ask that each weakness carry the matching dimension id.
- **When triaging returned findings**: classify each issue, apply the leniency rules before keeping it, and set `root_cause_key` for the issue bundle (see `reviewer-deliverables.md`).

Adapted from the paper-audit skill's 16-dimension deep-review criteria.

## The 16 issue dimensions

| id | Dimension | What it catches |
|---|---|---|
| D1 | Formula / derivation error | A step in a proof or derivation that does not follow, or an equation that is wrong as written |
| D2 | Notation inconsistency | The same symbol meaning two things, or the same object carrying two symbols, across sections |
| D3 | Prose vs formal object mismatch | The text describes a theorem, algorithm, or definition differently from its formal statement |
| D4 | Numerical inconsistency | Numbers that disagree between abstract, body, tables, and figures |
| D5 | Missing justification | A load-bearing design choice or assumption stated without argument or citation |
| D6 | Overclaim / claim inaccuracy | A claim broader than what the method, proof, or evidence supports |
| D7 | Misleading ambiguity | Wording a careful reader can reasonably parse into a wrong conclusion |
| D8 | Missing information / reproducibility gap | Method or setup detail a reader needs to reproduce the work, absent from paper and appendix |
| D9 | Internal contradiction | Two passages that cannot both be true |
| D10 | Self-consistency of standards | The paper judges baselines by a standard it does not apply to itself |
| D11 | Table structure violation | Missing booktabs three-line format, vertical rules, inconsistent precision within a column, caption below instead of above |
| D12 | Abstract structural incompleteness | Missing element of background / objective / methods / results / conclusion, or a results sentence with no data |
| D13 | Contribution deficiency | Core concepts undefined, no substantive dialogue with prior work, or no identifiable increment: if the paper disappeared, nothing known disappears with it |
| D14 | Methodology opacity | Sampling, coding, or protocol rationale missing (chiefly qualitative or mixed-methods work; for systems/ML this folds into D8) |
| D15 | Pseudo-innovation / straw man | A fabricated research gap, mischaracterized prior work, or selective citation hiding overlap with existing methods |
| D16 | Paragraph-level argument incoherence | Logical jumps between adjacent paragraphs, causal inversions, or evidence that does not support the sentence it follows |

## Leniency rules: what not to flag

- Copy-editing trivia. One typo is not an issue; a pattern of language too poor to review is.
- OCR or extraction noise. If the most charitable reading of a garbled passage resolves the problem, drop it.
- Content answered later. Do not criticize a section for omitting what a later section clearly provides.
- Author-chosen scope. A deliberate, stated limitation is not an overclaim; judge whether the position is sustainable, not whether you would have chosen it.

## Calibration

- A strong paper can still carry several major issues if each threatens a different conclusion. Do not over-merge distinct problems into one.
- Prefer one well-developed finding over several shallow duplicates of the same root cause.
- Severity follows consequence, not effort: an easy fix to a headline-threatening gap is still `critical` until fixed.

## Reasoning style per finding

For each issue, the finding should state:

1. what first raised the concern,
2. what context was checked (the charitable reading),
3. what remains unresolved after that check,
4. the strongest single piece of evidence, quoted verbatim from the source.

Point 4 is enforced downstream: `scripts/verify_review_quotes.py` checks every issue's quote against the manuscript, and an unverifiable quote sends the finding back for re-anchoring, not into the report.
