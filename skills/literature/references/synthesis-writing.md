# Synthesis Writing: Turning a Search into a Review

> **When to load**: the survey / systematic-review job's synthesis step, and
> any time you write a related-work section or a survey paragraph from
> retrieved sources.
> **What this is**: domain-neutral writing diagnostics for turning a pile of
> retrieved papers into a synthesis that *argues* rather than a bibliography
> that *lists*. Retargeted to CS venues and this plugin's tools. The
> systematic-search machinery (screening flow, quality signals) stays in
> `SKILL.md`; this file is about grounding and prose.

A literature question has two halves: finding the papers a domain expert would
point to, and turning them into something more useful than a reading list. Both
fail quietly and look like competent output until someone checks.

---

## 1. Retrieve first, then write, even when you know the answer

A DOI you emit either resolves to a real paper that says what you claim, or it
is a fabrication, and the difference is checkable in seconds. Resolving the DOI
for a paper you are certain of (the Transformer paper, a landmark benchmark
result) is one tool call, and it is the difference between a citation and a
claim about a citation. Author names come from the retrieved record, never from
memory: memory supplies plausible names, not the paper's. Route search through
this skill's backends and DOI-to-BibTeX through the `citations` skill or Zotero
MCP; verification lives in your tool trace, not in a sentence that announces
"verified."

For a *specific* paper ("the original," "the seminal," a named method), find
the highly-cited primary publication that the follow-ups all cite, not a survey
or a blog post about it.

## 2. Walk the citation graph both ways

A keyword sweep alone misses two things: the foundational paper a field is
built on, and the recent work that extends or contests your top hits. After the
first search, take the two or three most relevant papers and walk one step in
each direction:

- **Backward (references).** Pull their reference lists. The seminal paper the
  field cites surfaces here.
- **Forward (cited-by).** Pull their cited-by lists. The newer work that
  supersedes or challenges them surfaces here.

Fold anything new and on-topic into the set before you start writing. OpenAlex
and Semantic Scholar expose both directions, and this skill's backends can
fetch them. Neither direction reliably appears in a keyword search on its own.

## 3. Check for retractions and the null result

Sensational papers are findable *because* they were sensational, and some were
later retracted or failed to replicate. CrossRef's `update-to` field flags
retractions and corrections; for any high-profile or surprising finding the
check takes seconds, and `claim-verification`'s research-integrity gate runs
it. The related trap is the question whose honest answer is "no such paper
exists": when asked for "the paper showing X" and X fell apart or was never
established, name the claim, say what happened to it, and point to what the
actual evidence shows. Do not reach for the closest-matching citation.

## 4. Synthesis is comparison, not summary

A list of papers with one-sentence summaries is a bibliography. The review is
the layer on top: this result replicated, that one did not; these three agree
on the effect but disagree on the mechanism; this method wins on throughput,
that one on tail latency; this 2019 result was superseded by this 2023 one.
Organize by theme or question, not by paper. For a compare-methods request the
deliverable is the trade-off and a recommendation, not two adjacent summaries.

**The first-sentence test.** Read only the first sentence of each paragraph, in
order. If they form your argument, you wrote a synthesis. If they form a list of
author names ("Chen 2019 reported...", "Park 2020 showed..."), you wrote an
annotated bibliography in paragraph costume. A review paragraph opens on *your*
synthetic claim and then spends citations to back it: not "Chen 2019 reported a
40% reduction; Park 2020 reported 35%" (two index cards) but "the reduction is
real but modest, clustering at 35 to 40% (Chen 2019; Park 2020)" (a review).

## 5. Prose, not a bulleted bibliography

The synthesis itself is prose: paragraphs of connected argument, each making
one claim and anchoring it with an inline citation, transitioning to the next.
A page that is 80% bullet points tells the reader *that* papers exist, not what
they collectively show. Reserve bullets for where a list is genuinely the right
structure: a reference appendix, a head-to-head comparison table, an enumerated
set of named methods. If you find consecutive lines starting with "- Author
Year showed...", that is a paragraph you have not written yet.

## 6. Calibrate confidence to evidence

Say which findings are landmark and which are recent; flag preprints as
preprints; note when an older result was refined or overturned. Match the verb
to the evidence: a single-benchmark result is "one paper reports X," a result
reproduced across independent groups is stated plainly, a contested area gets
both sides and an honest "unresolved." For CS specifically, one dataset, one
workload, or one hardware platform is not a general claim, so say so rather than
letting the prose imply generality. When the request is about gaps, name
specific ones and anchor each to what establishes it as a gap; "more research is
needed" means you have not found the actual hole yet.
