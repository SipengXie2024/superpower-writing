---
name: academic-citation-workflow
description: Reliable literature workflow for academic papers — multi-agent reference search with mandatory URL verification, per-candidate adversarial existence checks, weak-citation screening under page budgets, and comparison-table citation management. Use whenever the user asks to find or add references, enrich a related-work section or comparison table, cut/screen weak citations, fit a page limit by trimming references, or verify that cited works actually exist — including Chinese phrasings like 找文献、筛引用、删弱引用、补充对比表、文献核验. Trigger even when the user just says references "feel thin" or "feel bloated" for a manuscript.
---

# Academic Citation Workflow

Citation work has two dominant failure modes: hallucinated or mischaracterized references, and silent budget blowups (page count, table scope, row sprawl). Both are prevented structurally, not by care alone. This skill encodes a workflow validated on a real IEEE journal submission (one screening round cutting 17 weak references, one enrichment round admitting 8 web-verified references; the verification layer caught fabrication risks, metadata errors, and one factual error in the paper's own table).

## Fix admission criteria before any search

Write the criteria into the search prompts themselves, before launching: domain scope (e.g., "strictly LLM/AI-traffic systems"), a notability floor (venue tier for academic work, deployment scale for industrial), year preferences, and, for comparison tables, the rule that a candidate is admissible only if it takes a real value in every comparison column. Mid-flight scope corrections from the user mean a wasted round; ask once up front.

## Finding references (enrichment)

Run a three-stage pipeline: per-category research agents, then one adversarial verifier per candidate, then synthesis.

- Research agents get one category each and a hard rule: a candidate may only be returned together with a URL the agent actually fetched and read. This single constraint removes most hallucination risk at the source. Prefer recent top-venue papers and widely deployed industrial systems with official documentation.
- Verifiers re-search from scratch and do not trust the researcher's URL. Each verifier checks four things: the work exists with the claimed title/venue/year; it actually does what the summary claims; it genuinely fits the claim or table row it would support; the BibTeX metadata is correct (authors, venue, year). Have verifiers also audit the surrounding existing content while they are there — independent verifiers catch the paper's own pre-existing errors (a mischaracterized system, a wrong table cell), which is free review.
- Cite industrial systems as `@misc` with the official docs URL, a double-braced corporate author, and an accessed-year note. Their citation value is proving that a design class is deployed in practice, so the official page beats a third-party writeup.

Minimal Workflow-tool skeleton for the pipeline:

```js
const results = await pipeline(CATEGORIES,
  c => agent(`${CTX} Category: ${c.brief}. Return ONLY candidates whose URL you fetched.`,
             { schema: CANDIDATES }),
  (res, c) => parallel(res.candidates.map(cd => () =>
    agent(`${CTX} Independently verify (re-search, do not trust the given URL): ${JSON.stringify(cd)}.
           Check existence, claimed behavior, fit, BibTeX metadata. keep=true only if all hold.`,
          { schema: VERDICT }))))
```

## Screening references (cuts)

Judge each citation by the load it carries, not by its fame. Never cut the sole support of a specific stated fact, the paper's foundational baseline or attack study, systems compared in tables, or formal foundations actually used. Good cut candidates: members of grouped citation lists (4+ keys on one clause), references redundant with a stronger co-cite on the same subtopic, and weak sources (blog or product page) duplicating an academic co-cite.

Verify every proposed cut adversarially before executing: would removal break a claim, force deleting a descriptive phrase the sentence needs, or drop work a reviewer would expect to see? Then record a reserve tier — cut-worthy candidates kept for now, with the exact edit each cut entails. The reserve pays for future strong additions via weak-for-strong swaps.

## Page-budget arithmetic

One reference entry costs roughly 4 to 6 lines in the rendered reference list. Before deciding how many references can be added or must go, measure the final page's actual slack in the rendered PDF, then set a net-add quota. When over budget, cut whole entries rather than compressing prose: shortening sentences mid-paragraph usually saves zero lines because no line boundary is crossed, while deleting one reference reliably saves five or six. Uncited BibTeX entries cost nothing (BibTeX prints cited keys only), so verified-but-trimmed entries stay in the `.bib` file as a ready reserve for the next round.

## Novelty-risk scanning

Every literature search doubles as competitor discovery. When a found system overlaps the paper's claims, immediately re-read the paper's gap and novelty sentences and check whether they remain accurate as scoped; usually the fix is sharpening the claim's scope, not ignoring the find. Surface such discoveries to the user prominently and flag them for co-authors — finding the overlap before a reviewer does is the point.

## Comparison-table admission

A row or citation enters a comparison table only if it takes a meaningful value in every column; building blocks the paper composes and attack literature that motivates it stay in prose, because they take no values on solution-comparison axes and bare-dash rows read as filler. Cell judgments come only from claims the prose or a verified source supports; unsupported cells get an explicit n/a marker, never an invented value. When citation lists are the table's first appearance of a key in source order, the numbers stay consecutive and compress into ranges, which keeps wide cite lists cheap.

## Mechanics

Append to bibliography files with absolute paths, since shell working directories reset between calls. After every change, rebuild and check three gates: undefined citations equal zero, the page count matches the budget, and no new overfull boxes; visually inspect the rendered page whenever a table or float changed.
