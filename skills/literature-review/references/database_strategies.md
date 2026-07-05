# Literature Database Search Strategies

This document provides comprehensive guidance for searching multiple literature databases systematically and effectively for computer-science research.

## Available Databases

### Preprints and Core CS Coverage

#### arXiv
- **Access**: Direct API access or WebFetch tool
- **Coverage**: Preprints in computer science, mathematics, statistics, and physics
- **Best for**: Latest unpublished work in ML, systems, databases, PL, and theory
- **Categories**: cs.LG (Machine Learning), cs.CL (Computation and Language), cs.DC (Distributed Computing), cs.DB (Databases), cs.PL (Programming Languages), cs.OS (Operating Systems), stat.ML
- **Search format**: `cat:cs.LG AND ti:"attention"`
- **Note**: Preprints are not peer-reviewed. Check whether a later peer-reviewed version exists via CrossRef or DBLP.

#### DBLP
- **Access**: Direct API (free, no key required) or web
- **Coverage**: Comprehensive bibliographic index of CS conferences and journals
- **Best for**: Authoritative venue and author metadata, complete publication lists, disambiguating venues
- **Search by**: Author, venue, title keywords
- **Tip**: Use DBLP to confirm the canonical peer-reviewed venue for an arXiv preprint

### Cross-Disciplinary Search

#### Semantic Scholar
- **Access**: Direct API (free tier; API key raises limits)
- **Coverage**: 200M+ papers across all fields
- **Best for**: Cross-disciplinary searches, citation graphs, paper recommendations
- **Features**: Influential citations, paper summaries, related papers
- **Rate limits**: 100 requests/5 minutes with API key

#### Google Scholar
- **Access**: Web scraping (use cautiously) or manual search
- **Coverage**: Comprehensive across all fields
- **Best for**: Finding highly cited papers, conference proceedings, theses
- **Limitations**: No official API, rate limiting
- **Export**: Use "Cite" feature for formatted citations

### Citation and Reference Management

#### CrossRef
- **Access**: Direct API (free, no key required)
- **Coverage**: 150M+ records with DOIs and metadata
- **Best for**: DOI resolution, metadata verification, detecting published versions and retractions (via the `update-to` field)

#### OpenAlex
- **Access**: Direct API (free, no key required)
- **Coverage**: 250M+ works, comprehensive metadata
- **Best for**: Citation analysis, author disambiguation, institutional research
- **Features**: Open access, excellent for bibliometrics

---

## Search Strategy Framework

### 1. Define the Research Question

State a focused question, then break it into 2-4 core concepts you can turn into search terms. A useful decomposition for CS reviews:
- **Problem/setting**: What system or task is studied?
- **Method/technique**: What approach is proposed or evaluated?
- **Baseline/comparison**: What is it compared against?
- **Metric/outcome**: How is success measured?

**Example**: "How do attention-approximation methods (method) affect training throughput and accuracy (metric) versus full attention (baseline) for long-context transformers (problem)?"

### 2. Develop Search Terms

#### Primary Concepts
Identify 2-4 main concepts from your research question.

**Example**:
- Concept 1: transformer, self-attention, attention mechanism
- Concept 2: long context, sequence length, efficiency
- Concept 3: sparse attention, linear attention, approximation

#### Synonyms and Related Terms
List alternative terms, abbreviations, and related concepts. Terminology drifts fast in CS, so include both older and newer names for the same idea (for example "MoE" and "mixture of experts").

#### Boolean Operators
- **AND**: Narrows search (must include both terms)
- **OR**: Broadens search (includes either term)
- **NOT**: Excludes terms

**Example**: `(transformer OR "self-attention") AND ("long context" OR "sequence length") AND (sparse OR linear OR efficient)`

#### Wildcards and Truncation
- `*` or `%`: Matches any characters
- `?`: Matches a single character

**Example**: `quant*` matches quantize, quantization, quantized

### 3. Set Inclusion/Exclusion Criteria

#### Inclusion Criteria
- **Date range**: e.g., 2015-2024 (last 10 years)
- **Language**: English (or specify multilingual)
- **Publication type**: Peer-reviewed papers, surveys, preprints
- **Study type**: Empirical evaluations, systems papers, benchmarks, theory
- **Venue**: Peer-reviewed conferences and journals, or preprints with released artifacts

#### Exclusion Criteria
- Extended abstracts and posters without full text
- Non-archival workshop papers superseded by a full version
- Non-original work (editorials, opinion pieces) unless surveyed as such
- Duplicate publications (keep the most complete or most recent version)
- Retracted papers

### 4. Database Selection Strategy

#### Multi-Database Approach
Search at least 3 complementary sources:

1. **Preprint server**: arXiv
2. **CS bibliographic index**: DBLP (for canonical venues and author lists)
3. **Comprehensive database**: Semantic Scholar or Google Scholar
4. **Metadata and citation**: CrossRef or OpenAlex

#### Database-Specific Syntax

| Database | Field Tags | Example |
|----------|-----------|---------|
| arXiv | ti:, au:, cat: | ti:"attention" AND cat:cs.LG |
| Semantic Scholar | title:, author:, year: | title:"consensus protocol" year:2020-2024 |
| DBLP | title, author, venue | "query optimization" venue:VLDB |

---

## Search Execution Workflow

### Phase 1: Pilot Search
1. Run an initial search with broad terms
2. Review the first 50 results for relevance
3. Note common keywords and canonical venue names
4. Refine the search strategy

### Phase 2: Comprehensive Search
1. Execute refined searches across all selected databases
2. Export results in a standard format (BibTeX, RIS, JSON)
3. Document search strings and date for each database
4. Record the number of results per database

### Phase 3: Deduplication
1. Import all results into a single file
2. Use `search_databases.py --deduplicate` to remove duplicates
3. Identify duplicates by DOI (primary) or title (fallback)
4. Keep the version with the most complete metadata (prefer the peer-reviewed version over its preprint)

### Phase 4: Screening
1. **Title screening**: Review titles, exclude obviously irrelevant results
2. **Abstract screening**: Read abstracts, apply inclusion/exclusion criteria
3. **Full-text screening**: Obtain and review full texts
4. Document reasons for exclusion at each stage

### Phase 5: Quality Assessment
For CS work, judge quality from signals that travel with the paper rather than clinical checklists:
1. **Venue tier**: Was it peer-reviewed at a strong conference or journal? (see venue tiers below)
2. **Reproducibility**: Are code, data, and an artifact available? Did the venue run artifact evaluation (for example a "Results Reproduced" badge)?
3. **Evaluation rigor**: Realistic baselines, ablations, error bars or multiple seeds, honest reporting of limitations
4. **Influence**: Citation count relative to age (see thresholds below)

Prefer the strongest evidence, and note when a claim rests only on a preprint with no released artifact.

---

## Search Documentation Template

### Required Documentation
All searches must be documented for reproducibility:

```markdown
## Search Strategy

### Database: arXiv
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**:
  ```
  (ti:"self-attention" OR ti:transformer)
  AND (abs:"long context" OR abs:"sequence length")
  AND cat:cs.LG
  ```
- **Results**: 247 papers
- **After deduplication**: 189 papers

### Database: DBLP
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**: "efficient attention" (title), venues NeurIPS/ICML/ICLR
- **Results**: 34 papers
- **After deduplication**: 28 papers

### Total Unique Papers
- **Combined results**: 217 unique papers
- **After title screening**: 156 papers
- **After abstract screening**: 89 papers
- **After full-text screening**: 52 papers included in review
```

---

## Advanced Search Techniques

### Prioritizing High-Impact Papers (CRITICAL)

**Always prioritize papers based on citation count, venue quality, and author reputation.** Quality matters more than quantity.

#### Citation Metrics in Database Searches

Use citation counts to identify influential work:

| Paper Age | Citations | Classification |
|-----------|-----------|----------------|
| 0-3 years | 20+ | Noteworthy |
| 0-3 years | 100+ | Highly Influential |
| 3-7 years | 100+ | Significant |
| 3-7 years | 500+ | Landmark |
| 7+ years | 500+ | Seminal |
| 7+ years | 1000+ | Foundational |

**Database-Specific Citation Features:**
- **Google Scholar:** Sort by citation count, use the "Cited by" feature
- **Semantic Scholar:** "Highly Influential Citations" metric, citation velocity
- **OpenAlex:** Citation counts, citation context analysis
- **DBLP:** Confirm the canonical venue, then look up citation counts via Semantic Scholar or Google Scholar

#### Filtering by Venue Quality

Prioritize papers from higher-tier venues:

**Tier 1 (Always Prefer):**
- Top ML: NeurIPS, ICML, ICLR
- Top systems: OSDI, SOSP, NSDI, USENIX ATC
- Top databases: SIGMOD, VLDB
- Top PL: PLDI, POPL
- Search tip: `source:NeurIPS` or `venue:OSDI` in Google Scholar or DBLP

**Tier 2 (High Priority):**
- Strong specialized venues (for example EMNLP, CVPR, EuroSys, ICSE, JMLR, TOPLAS)

**Tier 3 (Include When Relevant):**
- Respected field-specific conferences and journals with archival proceedings

**DBLP / Google Scholar Venue Filtering:**
```
venue:NeurIPS OR venue:ICML OR venue:OSDI
```

#### Leveraging "Cited by" Features

**Finding Influential Work:**
1. Start with a known key paper
2. Click "Cited by" to find papers that cite it
3. Sort citing papers by their citation count
4. Highly-cited citing papers indicate important follow-up work

**Identifying Seminal Papers:**
1. Search your topic broadly
2. Note which papers appear repeatedly in reference lists
3. Papers cited by many of your results are likely seminal
4. Check citation counts to confirm influence

**Semantic Scholar Features:**
- "Highly Influential Citations" shows citations that significantly built on the paper
- "Citation Velocity" shows recent citation growth
- Paper recommendations based on citation networks

### Citation Chaining

#### Forward Citation Search
Find papers that cite a key paper:
- Use the Google Scholar "Cited by" feature
- Use OpenAlex or Semantic Scholar APIs
- Identifies newer research building on seminal work
- **Tip:** Sort by citation count to find the most influential follow-up work

#### Backward Citation Search
Review references in key papers:
- Extract references from included papers
- Search for highly cited references (500+ citations for older papers)
- Identifies foundational research
- **Tip:** Focus on references that appear in multiple papers' bibliographies

### Snowball Sampling
1. Start with 3-5 highly relevant papers **from Tier-1 venues**
2. Extract all their references
3. Check which references are cited by multiple papers
4. Review those high-overlap references, which are likely seminal
5. Repeat for newly identified key papers
6. **Prioritize papers with high citation counts** at each step

### Author Search
Follow prolific and reputable authors in the field:
- Search by author name across databases
- Check author profiles (ORCID, Google Scholar, DBLP) for h-index and publication venues
- Review recent publications and preprints
- **Prefer authors with multiple Tier-1 publications** and high h-index (>40)
- Look for senior authors who are recognized field leaders

### Related Article Features
Many databases suggest related articles:
- Google Scholar "Related articles"
- Semantic Scholar "Recommended papers"
- Use to discover papers missed by keyword search
- **Filter recommendations by citation count and venue quality**

---

## Quality Control Checklist

### Before Searching
- [ ] Research question clearly defined
- [ ] Core concepts and synonyms listed
- [ ] Inclusion/exclusion criteria documented
- [ ] Target databases selected (minimum 3)
- [ ] Date range determined

### During Searching
- [ ] Search string tested and refined
- [ ] Results exported with complete metadata
- [ ] Search parameters documented
- [ ] Number of results recorded per database
- [ ] Search date recorded

### After Searching
- [ ] Duplicates removed
- [ ] Screening protocol followed
- [ ] Reasons for exclusion documented
- [ ] Quality assessment completed
- [ ] All citations verified with verify_citations.py
- [ ] Search methodology documented in review

---

## Common Pitfalls to Avoid

1. **Too narrow search**: Missing relevant papers
   - Solution: Include synonyms, related terms, broader concepts

2. **Too broad search**: Thousands of irrelevant results
   - Solution: Add specific concepts with AND, use field tags

3. **Single database**: Incomplete coverage
   - Solution: Search a minimum of 3 complementary databases

4. **Ignoring preprints**: Missing latest findings
   - Solution: Include arXiv preprints

5. **No documentation**: Irreproducible search
   - Solution: Document every search string, date, and result count

6. **Manual deduplication**: Time-consuming and error-prone
   - Solution: Use the search_databases.py script

7. **Unverified citations**: Broken DOIs, incorrect metadata
   - Solution: Run verify_citations.py on the final reference list

8. **Publication bias**: Only including published positive results
   - Solution: Search preprint servers and contact authors for unpublished results

---

## Example Multi-Database Search Workflow

```python
# Example workflow using available sources

# 1. Search arXiv
search_query = "cat:cs.LG AND ti:\"efficient attention\""
# Query the arXiv API with search_query

# 2. Search DBLP for canonical venues and author publication lists
# Query DBLP with: "efficient attention" (title)

# 3. Search Semantic Scholar via API
# Use the Semantic Scholar API with the search query

# 4. Search Google Scholar for highly cited work and "Cited by" chaining

# 5. Aggregate and deduplicate results
# python search_databases.py combined_results.json --deduplicate --format markdown --output review_papers.md

# 6. Verify all citations (DOIs via CrossRef)
# python verify_citations.py review_papers.md

# 7. Generate final PDF
# python generate_pdf.py review_papers.md --citation-style acm
```

---

## Resources

### DBLP Computer Science Bibliography
https://dblp.org/

### arXiv (cs listings)
https://arxiv.org/list/cs/recent

### Citation Style Guides
See references/citation_styles.md in this skill

### PRISMA Guidelines
Preferred Reporting Items for Systematic Reviews and Meta-Analyses:
http://www.prisma-statement.org/
