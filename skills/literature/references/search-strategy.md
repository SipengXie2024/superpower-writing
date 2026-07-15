# Search Strategy: What to Query

> **When to load**: the survey / systematic-review job, when you are building
> search terms, chaining citations, or documenting a search for reproducibility.
> Which backend to run lives in `search-backends.md`; this file is about the
> query itself. Venue tiers and citation thresholds live in `SKILL.md`.

## Table of Contents

- [Decompose the question](#decompose-the-question)
- [Build search terms](#build-search-terms)
- [Database-specific syntax](#database-specific-syntax)
- [Citation chaining](#citation-chaining)
- [Snowball sampling](#snowball-sampling)
- [Author and related-article search](#author-and-related-article-search)
- [Document the search](#document-the-search)

## Decompose the question

State a focused question, then break it into 2 to 4 concepts you can turn into
search terms. A useful decomposition for CS reviews:

- **Problem / setting**: what system or task is studied?
- **Method / technique**: what approach is proposed or evaluated?
- **Baseline / comparison**: what is it compared against?
- **Metric / outcome**: how is success measured?

Example: "How do attention-approximation methods (method) affect training
throughput and accuracy (metric) versus full attention (baseline) for
long-context transformers (problem)?"

## Build search terms

For each concept, list synonyms, abbreviations, and related terms. Terminology
drifts fast in CS, so include both older and newer names for the same idea
(for example "MoE" and "mixture of experts").

- Concept 1: transformer, self-attention, attention mechanism
- Concept 2: long context, sequence length, efficiency
- Concept 3: sparse attention, linear attention, approximation

Combine with Boolean operators:

- **AND** narrows (must include both): `transformer AND "long context"`
- **OR** broadens (either term): `(sparse OR linear OR efficient)`
- **NOT** excludes.
- Wildcards: `quant*` matches quantize, quantization, quantized.

Full query: `(transformer OR "self-attention") AND ("long context" OR
"sequence length") AND (sparse OR linear OR efficient)`.

Set inclusion and exclusion criteria before screening: date range, language,
publication type (peer-reviewed, survey, preprint), study type (empirical,
systems, benchmark, theory). Exclude extended abstracts and posters without
full text, non-archival workshop papers superseded by a full version,
editorials, duplicate publications, and retracted papers.

## Database-specific syntax

| Database | Field tags | Example |
|----------|-----------|---------|
| arXiv | `ti:`, `au:`, `cat:`, `abs:` | `ti:"attention" AND cat:cs.LG` |
| Semantic Scholar | `title:`, `author:`, `year:` | `title:"consensus protocol" year:2020-2024` |
| DBLP | title, author, venue | `"query optimization" venue:VLDB` |
| Google Scholar | `source:`, "Cited by" | `source:NeurIPS` then sort by citations |

arXiv categories worth knowing: cs.LG (ML), cs.CL (language), cs.DC
(distributed), cs.DB (databases), cs.PL (programming languages), cs.OS
(operating systems), stat.ML.

## Citation chaining

A keyword sweep misses two things: the foundational paper a field is built on,
and the recent work that extends or contests your top hits. After the first
search, take the 2 or 3 most relevant papers and walk one step each way.

**Forward (cited-by)**: papers that cite a key paper. Surfaces newer work that
supersedes or challenges it. Use Semantic Scholar or OpenAlex APIs, Google
Scholar "Cited by", or a parallel-cli search:

```bash
parallel-cli search "papers citing [Author et al. Year] [paper title]" \
  -q "citing" -q "[key author]" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,semanticscholar.org,arxiv.org,dblp.org" \
  -o sources/research_forward_citations.json
```

Sort citing papers by their own citation count; highly-cited citing papers are
the important follow-ups.

**Backward (references)**: the reference lists of key papers. Surfaces the
seminal work the field cites. Use `parallel-cli extract` to fetch a key paper
and read its references, and focus on references that appear in multiple
papers' bibliographies.

## Snowball sampling

1. Start with 3 to 5 highly relevant papers from Tier-1 venues.
2. Extract all their references.
3. Find references cited by multiple of your papers; high overlap signals
   seminal work.
4. Review those, then repeat for newly identified key papers.
5. Prioritize high citation counts at each step.

## Author and related-article search

Follow prolific, reputable authors: search by name, check ORCID / Google
Scholar / DBLP profiles for h-index and venues, and prefer senior authors with
multiple Tier-1 publications. Use "Related articles" (Google Scholar) and
"Recommended papers" (Semantic Scholar) to catch papers keyword search missed,
filtered by citation count and venue quality.

## Document the search

Record every search so the review is reproducible:

```markdown
## Search Strategy

### Database: arXiv
- Date searched: 2024-10-25
- Date range: 2015-01-01 to 2024-10-25
- Search string: (ti:"self-attention" OR ti:transformer) AND (abs:"long context") AND cat:cs.LG
- Results: 247 papers
- After deduplication: 189 papers

### Total unique papers
- Combined: 217 → title screen: 156 → abstract screen: 89 → full-text: 52 included
```

Deduplicate by DOI (primary) or title (fallback), keeping the most complete
version (prefer the peer-reviewed paper over its preprint).
