---
name: literature
description: >-
  Find and review academic literature. Use when the user wants to search
  papers, survey the state of a research direction, look up a paper or
  dataset, find baselines or related work, enrich a related-work section or
  comparison table, screen weak citations, or verify that cited works exist.
  Routes through Zotero semantic search for in-library papers, parallel-cli
  web search, a deep-research fallback, and direct arXiv, DBLP, Semantic
  Scholar, and CrossRef access. Chinese triggers: 搜文献, 综述某方向,
  查论文或数据集, 找 baseline, 补充对比表, 文献核验.
allowed-tools: Read Write Edit Bash
---

# Literature

Find the papers a domain expert would point to, then turn them into something
more useful than a reading list. This skill covers three jobs that share one
search layer:

- **Look up** a paper, dataset, baseline, or fact (fast, default).
- **Survey** a research direction into cited synthesis or a review document.
- **Enrich or screen** the citations of a manuscript (related-work section,
  comparison table, weak-citation cuts) with adversarial existence checks.

Pick the job from what the user asked. Do not run the full systematic-review
pipeline for a one-paper lookup, and do not answer "find related work for my
paper" with a bare list.

## Search backends (authoritative routing)

One routing table for all three jobs. Pick a backend silently and search;
full command flags, API specs, and environment variables live in
`references/search-backends.md`.

| Situation | Backend |
|-----------|---------|
| Paper may already be in the user's Zotero library | Zotero MCP `zotero_semantic_search` FIRST |
| Any standard search (the default) | `parallel-cli search` (fast, two-search pattern) |
| User explicitly asks for deep or exhaustive research | Parallel Chat API (`core`, 60s to 5min); confirm once before launching |
| Query names papers, DOIs, or venues specifically | Perplexity `sonar-pro-search` (academic mode) |
| Need canonical venue, author list, citation graph, or DOI metadata | Direct arXiv / DBLP / Semantic Scholar / CrossRef / OpenAlex |

**Zotero first for in-library work.** When the user has a Zotero library
(the `zotero` MCP server in `.mcp.json`), call
`zotero_semantic_search(query=<topic or claim>, limit=5)` before hitting the
web. When the library was indexed with fulltext, this matches your query
against paper paragraphs, not just titles, and returns papers the user already
has. For each hit, `zotero_get_item_metadata(item_key=<key>)` returns markdown
or BibTeX. This is the fastest path and it reuses vetted sources.

**Default web search.** For a scientific query, run two `parallel-cli search`
calls so scholarly sources surface:

```bash
# 1. Academic-focused
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,semanticscholar.org,dblp.org,dl.acm.org,ieee.org,openreview.net,aclanthology.org" \
  -o sources/research_<topic>-academic.json

# 2. General (catches non-academic sources)
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>-general.json
```

Add `--after-date YYYY-MM-DD` for time-sensitive queries. Merge results,
academic sources first. A non-scientific query needs only one general search.
Use `parallel-cli extract "<url>" --json` to pull full content from a
promising paper URL before you commit to reading it.

## Output discipline

The user wants results, not a tour of the machinery.

- **Just search and deliver.** No routing rationale, no prerequisite recap, no
  "this query routes to X because" narration. Pick the backend and go.
- **Confirm only the slow path.** The Parallel Chat API deep-research backend
  (60s to 5min, higher cost) gets a one-line confirmation first. Fast
  parallel-cli, Zotero, and Perplexity searches run without asking.
- **Save every result to `sources/`.** Research is expensive to obtain and
  critical for reproducibility. Use the `-o sources/...` flag on every
  parallel-cli call. Before a new query, `ls sources/`; if a saved file
  already covers the topic, re-read it instead of re-querying. Saved files
  must preserve all URLs, DOIs, and citation metadata.
- **If you cannot search** (no parallel-cli, missing key, no network), say so
  in one line and give the best answer from your own knowledge, labeled as
  un-searched. Never stall, and never fabricate search output or DOIs.

## Fix scope before searching

Wasted rounds come from unstated scope, not from bad search. Before launching,
write the criteria into the search prompts themselves:

- **Domain scope**, stated tightly (for example "strictly LLM inference
  serving systems", not "ML systems").
- **Notability floor**: venue tier for academic work, deployment scale for
  industrial work. See the venue tiers below.
- **Year preference** and whether preprints count.
- **For a comparison table**: a candidate is admissible only if it takes a
  real value in every comparison column.

Ask once, up front. A mid-search scope correction from the user wastes the
whole round.

## Job A: look up

A fast, single-answer search. Route per the table (Zotero first if in-library,
else parallel-cli). Lead with the synthesized answer and inline citations,
academic sources first. For a "compare X vs Y" request the deliverable is the
trade-off and a recommendation, not two adjacent summaries. Save to `sources/`.

For a specific named paper ("the original", "the seminal"), find the
highly-cited primary publication that the follow-ups all cite, not a survey or
a blog post about it. Author names come from the retrieved record, never from
memory.

## Job B: survey / systematic review

A structured synthesis of a direction. Keep the rigor, drop the ceremony:
these are steps to work through, not gates that block. Collapse or skip steps
the user has already settled or explicitly waived.

1. **Scope.** State a focused question and break it into 2 to 4 concepts
   (problem, method, baseline, metric). Set the review type, date range, and
   inclusion criteria. Restate them to the user if consequential, then
   proceed.
2. **Search.** Start with the default backends above. Then chain citations:
   take the 2 or 3 most relevant hits and walk one step backward (their
   references, where the seminal paper surfaces) and one step forward (their
   cited-by, where newer and competing work surfaces). Neither direction shows
   up in a keyword sweep alone. Detail and database-specific query syntax:
   `references/search-strategy.md`.
3. **Screen.** Deduplicate by DOI then title. Screen title, then abstract,
   then full text against the criteria. Record the counts as a short flow
   (identified, deduplicated, screened, included).
4. **Extract and rate quality.** Per included study, pull metadata, method,
   scale, results, and stated limitations. Rate confidence from signals that
   travel with the paper: venue tier, artifact and reproducibility, evaluation
   rigor, influence. See venue tiers below.
5. **Synthesize thematically.** Organize by theme or question, not
   study-by-study. This is where a search becomes a review, and it fails
   quietly. Read `references/synthesis-writing.md` before writing prose: the
   first-sentence test, comparison over summary, prose over a bulleted
   bibliography, confidence calibrated to evidence.
6. **Verify citations** (see the verification section below).
7. **Produce the document.** For a full review, start from
   `assets/review_template.md`. Format references in one style throughout;
   see `references/citation-styles.md` for APA, ACM, IEEE, and Chicago.

## Job C: enrich or screen a manuscript's citations

Citation work fails two ways: hallucinated or mischaracterized references, and
silent budget blowups (page count, table scope, row sprawl). Both are prevented
structurally, not by care alone. This workflow was validated on a real IEEE
journal submission, where the verification layer caught fabrication risks,
metadata errors, and one factual error in the paper's own table.

### Finding references (three-stage adversarial pipeline)

Run per-category research agents, then one adversarial verifier per candidate,
then synthesis.

- **Research agents** get one category each and a hard rule: a candidate may
  only be returned together with a URL the agent actually fetched and read.
  This single constraint removes most hallucination risk at the source. Prefer
  recent top-venue papers and widely deployed industrial systems with official
  documentation.
- **Verifiers re-search from scratch** and do not trust the researcher's URL.
  Each verifier checks four things: the work exists with the claimed
  title/venue/year; it actually does what the summary claims; it genuinely
  fits the claim or table row it would support; the BibTeX metadata is correct.
  Have verifiers also audit the surrounding existing content while they are
  there, since independent verifiers catch the paper's own pre-existing errors
  for free.
- **Cite industrial systems** as `@misc` with the official docs URL, a
  double-braced corporate author, and an accessed-year note. Their citation
  value is proving that a design class is deployed, so the official page beats
  a third-party writeup.

Minimal Workflow-tool skeleton:

```js
const results = await pipeline(CATEGORIES,
  c => agent(`${CTX} Category: ${c.brief}. Return ONLY candidates whose URL you fetched.`,
             { schema: CANDIDATES }),
  (res, c) => parallel(res.candidates.map(cd => () =>
    agent(`${CTX} Independently verify (re-search, do not trust the given URL): ${JSON.stringify(cd)}.
           Check existence, claimed behavior, fit, BibTeX metadata. keep=true only if all hold.`,
          { schema: VERDICT }))))
```

### Screening references (cuts)

Judge each citation by the load it carries, not by its fame. Never cut the sole
support of a stated fact, the paper's foundational baseline or attack study,
systems compared in tables, or formal foundations actually used. Good cut
candidates: members of grouped citation lists (4+ keys on one clause),
references redundant with a stronger co-cite on the same subtopic, and weak
sources (blog or product page) duplicating an academic co-cite.

Verify every proposed cut adversarially before executing: would removal break a
claim, force deleting a phrase the sentence needs, or drop work a reviewer
expects? Then record a reserve tier, the cut-worthy candidates kept for now,
with the exact edit each cut entails. The reserve pays for future strong
additions via weak-for-strong swaps.

### Page-budget arithmetic

One reference entry costs roughly 4 to 6 lines in the rendered reference list.
Measure the final page's actual slack in the rendered PDF, then set a net-add
quota. When over budget, cut whole entries rather than compressing prose:
shortening a sentence mid-paragraph usually saves zero lines because no line
boundary is crossed, while deleting one reference reliably saves five or six.
Uncited BibTeX entries cost nothing, so verified-but-trimmed entries stay in
the `.bib` file as a ready reserve.

### Comparison-table admission

A row or citation enters a comparison table only if it takes a meaningful value
in every column. Building blocks the paper composes and attack literature that
motivates it stay in prose, because they take no values on solution-comparison
axes and bare-dash rows read as filler. Cell judgments come only from claims
the prose or a verified source supports; an unsupported cell gets an explicit
n/a marker, never an invented value.

### Novelty-risk scanning

Every literature search doubles as competitor discovery. When a found system
overlaps the paper's claims, re-read the paper's gap and novelty sentences and
check whether they remain accurate as scoped. Usually the fix is sharpening the
claim's scope, not ignoring the find. Surface such discoveries to the user
prominently, since finding the overlap before a reviewer does is the point.

### Mechanics

Append to bibliography files with absolute paths, since shell working
directories reset between calls. After every change, rebuild and check three
gates: undefined citations equal zero, page count matches the budget, no new
overfull boxes. Visually inspect the rendered page whenever a table or float
changed.

## Verify citations

Fabricated and mischaracterized references are a fact-integrity failure, so
this check is mechanical, not a matter of care. Every DOI you emit either
resolves to a real paper that says what you claim or it is a fabrication, and
the difference is checkable in seconds.

- **Zotero MCP path (preferred).** `zotero_add_by_doi(doi=<DOI>,
  collection_key=<key>)` auto-fetches correct metadata and an open-access PDF,
  and dedupes by DOI. To confirm a paper is genuinely in the library despite a
  slightly-off DOI (preprint versus publisher), fall back to
  `zotero_semantic_search(query=<title or claim>, limit=5)` and match by
  title.
- **CrossRef.** Resolve each DOI, confirm authors, title, venue, and year
  match, and check the `update-to` field for retractions and corrections.
- **Delegation.** For deeper claim-to-evidence checking, hand off to the
  `claim-verification` skill; for BibTeX generation and library hygiene, to the
  `citations` skill.

Never announce "verified" in prose. Verification lives in your tool trace.
Re-check until every citation passes, and correct the source document in place.

## Quality signals: prioritize high-impact work

Quality matters more than quantity. Prefer influential, highly-cited papers
from reputable authors and top venues.

**Citation thresholds** (surface these first):

| Paper age | Citations | Classification |
|-----------|-----------|----------------|
| 0 to 3 years | 20+ | Noteworthy |
| 0 to 3 years | 100+ | Highly influential |
| 3 to 7 years | 100+ | Significant |
| 3 to 7 years | 500+ | Landmark |
| 7+ years | 500+ | Seminal |
| 7+ years | 1000+ | Foundational |

**Venue tiers** (CS):

- **Tier 1 (always prefer):** NeurIPS, ICML, ICLR; OSDI, SOSP, NSDI, USENIX
  ATC; SIGMOD, VLDB; PLDI, POPL.
- **Tier 2 (strong preference):** ACL, EMNLP, CVPR, KDD, SIGCOMM, EuroSys,
  ASPLOS, ISCA, ICSE; top journals (JMLR, TOCS, TODS, PACMPL, TPAMI).
- **Tier 3 (include when relevant):** respected field-specific archival
  venues.
- **Tier 4 (use sparingly):** non-archival workshops and lower-tier venues.

Flag preprints as preprints. A single dataset, workload, or hardware platform
is not a general claim, so say so. When a high-profile finding was retracted or
failed to replicate, name it and say what happened rather than reaching for the
closest-matching citation.

## Figures (recommended for reviews)

A survey or systematic review reads better with one or two figures: a
PRISMA-style flow of the screening counts, a thematic-synthesis diagram, or a
research-gap map. Invoke `Skill(skill="superpower-writing:tikz-figures")`
for concept diagrams, or `Skill(skill="superpower-writing:scientific-visualization")`
for data plots (CDFs, bars, Pareto fronts). This is a recommendation, not a
gate.

## Pitfalls

- Single-source search: always search at least a couple of complementary
  backends.
- Study-by-study summary posing as synthesis: organize thematically.
- Unverified citations: resolve every DOI before finalizing.
- Too broad (thousands of hits) or too narrow (missing synonyms): pilot, then
  refine.
- Ignoring preprints: include arXiv, but flag them as not peer-reviewed.
- Undocumented search: save every query and result to `sources/` so the review
  is reproducible.

## References and assets

- `references/search-backends.md`: full backend routing, API specs,
  environment variables, Zotero MCP tools, direct academic-API access.
- `references/search-strategy.md`: query construction, database-specific
  syntax, citation chaining, snowball sampling, documentation template.
- `references/synthesis-writing.md`: turning a search into a synthesis that
  argues rather than lists.
- `references/citation-styles.md`: APA, ACM, IEEE, and Chicago formatting.
- `assets/review_template.md`: full systematic-review document template.
