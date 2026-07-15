# Search Backends: Full Routing and Specs

> **When to load**: you need the exact command flags, API endpoints,
> environment variables, or Zotero MCP tool names behind the routing table in
> `SKILL.md`. The one-line decision rule ("Zotero first, else parallel-cli,
> deep-research only on request, Perplexity for named papers") lives in the
> skill body; this file is the detail.

The primary backend is `parallel-cli search`. Everything else is a fallback for
a specific situation: Zotero for papers already in the library, the Parallel
Chat API for explicit deep research, Perplexity for academic-specific paper
queries, and direct academic APIs for canonical metadata and citation graphs.

## Table of Contents

- [Zotero MCP (in-library, semantic)](#zotero-mcp-in-library-semantic)
- [parallel-cli search (primary)](#parallel-cli-search-primary)
- [Parallel Chat API (deep research)](#parallel-chat-api-deep-research)
- [Perplexity sonar-pro-search (academic)](#perplexity-sonar-pro-search-academic)
- [Direct academic APIs](#direct-academic-apis)
- [Save discipline](#save-discipline)

## Zotero MCP (in-library, semantic)

Registered as the `zotero` server in the plugin's `.mcp.json`. Try this first
whenever the paper might already be in the user's library, because it is faster
and reuses vetted sources.

- `zotero_semantic_search(query=<topic or claim>, limit=5)`: AI similarity
  search over the chunked library. When paper bodies are indexed with fulltext
  (`has_fulltext=True` chunks), this matches your query against paragraphs, not
  just titles and abstracts. Filter to one paper's chunks with
  `filters={"parent_item_key": <key>}`.
- `zotero_search_items(query=...)`: DOI, title, or author lookup.
- `zotero_get_item_metadata(item_key=<key>)`: returns markdown or BibTeX for a
  hit.
- `zotero_get_item_fulltext(item_key=<key>)`: server-side extracted PDF text.
  Use sparingly (often 70K+ chars); prefer `zotero_semantic_search` to find the
  relevant chunk first.
- `zotero_add_by_doi(doi=<DOI>, collection_key=<key>)`: auto-fetches metadata
  and an open-access PDF, dedupes by DOI. This is the citation-adding and
  metadata-verification path.
- Scite intelligence: `scite_enrich_item`, `scite_enrich_search`,
  `scite_check_retractions` for citation-context and retraction signals.

## parallel-cli search (primary)

Fast (2 to 10s), cost-effective web search with academic source
prioritization. This is the default for every standard query.

Install and authenticate:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
# or: uv tool install "parallel-web-tools[cli]"
parallel-cli auth
# or: export PARALLEL_API_KEY="your_parallel_api_key"
```

Two-search pattern for scientific queries (academic + general):

```bash
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,semanticscholar.org,dblp.org,dl.acm.org,ieee.org,openreview.net,aclanthology.org" \
  -o sources/research_<topic>-academic.json

parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>-general.json
```

Flags:
- `--after-date YYYY-MM-DD`: restrict to recent work for time-sensitive
  queries.
- `--include-domains d1,d2`: limit to specific sources (academic domains
  above).
- `--max-results`, `--excerpt-max-chars-total`: control breadth and excerpt
  budget.

Extract full content from a specific URL or PDF before committing to read it:

```bash
parallel-cli extract "https://arxiv.org/abs/XXXX.XXXXX" --json
```

Output is JSON with `title`, `url`, `publish_date`, and `excerpts` per result.

## Parallel Chat API (deep research)

The deep-research fallback, used only when the user explicitly asks for deep,
exhaustive, or comprehensive research. Much slower (60s to 5min) and more
expensive than parallel-cli, so confirm once before launching.

- OpenAI-SDK compatible; base URL `https://api.parallel.ai`, model `core`.
- Uses the same `PARALLEL_API_KEY`.
- Output: markdown with inline citations, a research basis of URLs, reasoning,
  and confidence levels. Rate limit 300 req/min.
- Python package: `openai`.

## Perplexity sonar-pro-search (academic)

Used only for academic-specific paper queries: when the request names papers,
DOIs, venues, or asks for "seminal/foundational/highly-cited" work.

- Model `perplexity/sonar-pro-search` via OpenRouter; needs
  `OPENROUTER_API_KEY`.
- Academic search mode (prioritizes peer-reviewed sources), high search
  context, 5 to 15s.
- Returns a summary plus 5 to 8 citations with authors, titles, venues, years,
  DOIs, citation counts, and venue-tier indicators.

## Direct academic APIs

Free, no-key (or free-tier) sources for canonical metadata, venue
disambiguation, and citation graphs. Reach for these when parallel-cli surfaces
a paper but you need authoritative structure.

- **arXiv**: direct API for cs.* preprints. Categories include cs.LG, cs.CL,
  cs.DC, cs.DB, cs.PL, cs.OS, stat.ML. Query form `cat:cs.LG AND ti:"attention"`.
  Preprints are not peer-reviewed; check for a later published version via
  CrossRef or DBLP.
- **DBLP**: free API or web. Authoritative CS venue and author metadata. Use to
  confirm the canonical peer-reviewed venue for a preprint and to pull complete,
  disambiguated author publication lists.
- **Semantic Scholar**: free API (key raises limits). 200M+ papers, citation
  graphs, "Highly Influential Citations", paper recommendations. Good for
  cross-disciplinary search and forward/backward citation chaining.
- **CrossRef**: free API. 150M+ DOI records. DOI resolution, metadata
  verification, and retraction detection via the `update-to` field.
- **OpenAlex**: free API. 250M+ works, strong for bibliometrics, author
  disambiguation, and citation analysis; exposes both citation directions.

## Save discipline

Every result is saved under `sources/` with `-o`. This is non-negotiable: it
makes citations traceable, survives context compaction, and lets multiple
sections reuse one query.

| Backend | Filename pattern |
|---------|------------------|
| parallel-cli (default) | `sources/research_<topic>.json` or `...-academic.json` |
| Parallel Chat API (deep) | `sources/research_YYYYMMDD_HHMMSS_<topic>.md` |
| Perplexity (academic) | `sources/papers_YYYYMMDD_HHMMSS_<topic>.md` |

Saved files must preserve every URL, DOI, and citation object. Before a new
query, `ls sources/`; re-read a covering file instead of re-querying.
