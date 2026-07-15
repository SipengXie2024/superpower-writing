# Citation Discipline For Prior-Work Claims (all phases)

Every paper this skill names as prior work must be real and resolvable. This rule holds in all three phases: a lens candidate grounded in a paper, a per-claim novelty overlap, or a fatal-flaw novelty judgment. A fabricated prior-work citation is the worst failure mode here. It produces a confident verdict built on a paper that does not exist. This file specifies the verification protocol and the `[UNVERIFIED]` marker. It aligns with the plugin's claim-first, never-fabricate rule.

## 1. The core rule

Never invent an arXiv ID, a DOI, a venue, a year, an author, or a title from memory. Not when you are confident. Not to fill a gap in a table. A plausible-looking citation that you did not resolve is a fabrication, even if it turns out to be approximately right. The same rule covers any number you attribute to a prior paper.

When you cannot verify a candidate paper, you have two honest options:

- Tag it `[UNVERIFIED]` and keep it visible in the output.
- Drop the specific unverified field and describe the overlap in prose, with one note that the citation needs lookup.

Never silently assert an unverified identifier as fact. Never withhold a whole finding because one field is unknown.

## 2. Verification protocol

A paper enters any verdict table only after it clears this gate.

1. **Source of truth is the retrieval result, not memory.** A candidate paper is admissible only if it came back from `superpower-writing:literature`, the merged retrieval skill, or the user named it. Do not add papers you merely recall.

2. **Resolve the identifier.** For each candidate, confirm its arXiv ID or DOI resolves to the title and authors you are about to record. The retrieval skill saves raw results under `sources/`. Cross-check the identifier against that saved result rather than retyping from memory.

3. **Confirm the year and venue.** Recency drives the novelty verdict, so a wrong year is load-bearing. Confirm the year from the resolved record. If the venue is not in the resolved record, record it as `preprint` or leave it blank rather than guessing.

4. **On a resolution miss, do not drop and do not invent.** When the identifier does not resolve, or the retrieval result is too thin to confirm the fields, tag the entry `[UNVERIFIED]` and surface it. The user can resolve it manually. Surfacing an uncertain overlap is more useful than hiding it.

## 3. The `[UNVERIFIED]` marker

Use `[UNVERIFIED]` inline wherever an unconfirmed paper appears.

- In a per-claim delta table: `| 2 | ... | MED | SomePaper 2026 [UNVERIFIED] | overlap unclear, identifier unresolved |`.
- In the closest-prior-work table: put `[UNVERIFIED]` in the Paper cell and leave unresolved fields blank rather than filled with guesses.
- In prose: "the closest prior work appears to be a 2026 preprint on X [UNVERIFIED]; resolve before relying on this".

The marker signals to the user that this entry needs a manual lookup before it carries weight. An `[UNVERIFIED]` paper must not, on its own, force an ABANDON or a Reject-and-Pivot. Flag the uncertainty and recommend resolving it first.

## 4. When no prior work is found

A claim with no overlapping prior work is a real and reportable outcome, not a blank. Record it as "none found" in the closest-prior-work column. Do not leave it empty, which reads as "not checked". Do not manufacture a weak match to fill the cell.

"None found" after three query formulations and a six-month recency pass is meaningful evidence toward HIGH novelty. State the search effort that backs it so the user can judge confidence: which queries ran, what window they covered.

## 5. Why this is strict here

This skill's verdict directly shapes whether a user spends months on an idea. A fabricated dominating paper triggers a false ABANDON and kills a good idea. A fabricated absence of prior work triggers a false PROCEED and walks the user into a scooped submission. Both failures are expensive and both are preventable by refusing to record anything unverified as fact.
