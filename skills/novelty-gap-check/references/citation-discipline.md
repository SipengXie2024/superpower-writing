# Citation discipline for prior-work claims

Every paper this skill names as prior work must be real and resolvable. A fabricated prior-work citation is the worst failure mode here: it produces a confident novelty verdict built on a paper that does not exist. This file specifies the pre-search verification protocol and the `[UNVERIFIED]` marker. It aligns with the plugin's claim-first, never-fabricate rule and with the `% UNVERIFIED` convention in `citation-management`.

## 1. The core rule

Never invent an arXiv ID, a DOI, a venue, a year, an author, or a title from memory. Not when you are confident. Not to fill a gap in the table. A plausible-looking citation that you did not resolve is a fabrication, even if it turns out to be approximately right.

When you cannot verify a candidate paper, you have two honest options:

- Tag it `[UNVERIFIED]` and keep it visible in the report.
- Drop the specific unverified field and describe the overlap in prose, with one note that the citation needs lookup.

Never silently assert an unverified identifier as fact. Never withhold a whole finding because one field is unknown.

## 2. Pre-search verification protocol

A paper enters the report only after it clears this gate. Verification happens during Phase B, before the paper is recorded as closest prior work.

1. **Source of truth is the retrieval result, not memory.** A candidate paper is admissible only if it came back from `superpower-writing:research-lookup` or `superpower-writing:literature-review`, or the user named it. Do not add papers you merely recall.

2. **Resolve the identifier.** For each candidate, confirm its arXiv ID or DOI resolves to the title and authors you are about to record. The retrieval skills save raw results under `sources/`. Cross-check the identifier against that saved result rather than retyping from memory.

3. **Confirm the year and venue.** Recency drives the verdict, so a wrong year is load-bearing. Confirm the year from the resolved record. If the venue is not in the resolved record, record the venue as `preprint` or leave it blank rather than guessing.

4. **On a resolution miss, do not drop and do not invent.** When the identifier does not resolve, or the retrieval result is too thin to confirm the fields, tag the entry `[UNVERIFIED]` and surface it. The user can resolve it manually. Surfacing an uncertain overlap is more useful than hiding it.

## 3. The `[UNVERIFIED]` marker

Use `[UNVERIFIED]` inline wherever an unconfirmed paper appears.

- In the per-claim delta table: `| 2 | ... | MED | SomePaper 2026 [UNVERIFIED] | overlap unclear, identifier unresolved |`.
- In the closest-prior-work table: put `[UNVERIFIED]` in the Paper cell and leave unresolved fields blank rather than filled with guesses.
- In prose: "the closest prior work appears to be a 2026 preprint on X [UNVERIFIED]; resolve before relying on this".

The marker is a signal to the user that this entry needs a manual lookup before it carries weight in their decision. An `[UNVERIFIED]` paper must not, on its own, force an ABANDON verdict. Flag the uncertainty and recommend resolving it first.

## 4. When no prior work is found

A claim with no overlapping prior work is a real and reportable outcome, not a blank. Record it as "none found" in the closest-prior-work column. Do not leave it empty, which reads as "not checked". Do not manufacture a weak match to fill the cell.

"None found" after three query formulations and a six-month recency pass is meaningful evidence toward HIGH novelty. State the search effort that backs it so the user can judge confidence: which queries ran, what window they covered.

## 5. Numbers and quoted results

The same rule covers any number you attribute to a prior paper. If you cite a baseline's reported accuracy or speedup to argue overlap, that number must come from the resolved paper, not from memory. Mark an unconfirmed number `[UNVERIFIED]` exactly as a citation. A wrong attributed number can wrongly tank a claim to LOW.

## 6. Why this is strict here

This skill's verdict directly shapes whether a user spends months on an idea. A fabricated dominating paper triggers a false ABANDON and kills a good idea. A fabricated absence of prior work triggers a false PROCEED and walks the user into a scooped submission. Both failures are expensive and both are preventable by refusing to record anything unverified as fact.
