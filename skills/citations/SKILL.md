---
name: citations
description: Generate and verify BibTeX. Adds a paper by DOI or arXiv id through the Zotero library (it fetches the metadata and open-access PDF), then emits the BibTeX. Verifies a citation's authors, title, venue, and year against the real record to catch hallucinated or misattributed references, and audits a .bib for missing fields, missing DOI or arXiv id, and duplicates. Use when managing citations, generating BibTeX, verifying references, or cleaning up a .bib. 中文触发：管理引用、生成 BibTeX、核验参考文献、整理 bib。
license: MIT license
metadata:
    skill-author: superpower-writing (slimmed from citation-management, Zotero-MCP-first)
---

# Citations: BibTeX generation and reference verification

Turn a paper into a correct BibTeX entry, and prove an existing entry is real and accurate. A strong model still fabricates references and swaps authors, venues, and years between real papers, so the verification here is a mechanical check, not a matter of care.

Metadata comes from the Zotero library over the MCP connection (configured in `.mcp.json`), which pulls from CrossRef and arXiv. Web search is the fallback. The old skill's hand-scraping of Google Scholar, CrossRef, arXiv, and DBLP web pages is gone; do not reconstruct it.

## Output discipline (read first)

1. **Always ship the best available entry.** If Zotero is not reachable, the network is down, or it is a one-off conversion, do not defer to "run this later." Produce the BibTeX from the metadata you already have, then say which fields still need confirming.
2. **Label what you could not verify.** Any field you did not confirm against an authoritative source (a guessed page range, an unresolved DOI) gets marked inline once, e.g. `pages = {1--?}, % UNVERIFIED`. Never invent a value; never withhold the whole entry because one field is unknown.
3. **State an unknown field once, cleanly.** Either give the value with a `% UNVERIFIED` marker, or omit it with one note that it needs lookup. Do not assert a value and retract it in the same breath.
4. **Keep the machinery out of the output.** Deliver citations, not a tour of this skill. Do not name the skill, its rules, or its scripts as the reason for what you do.
5. **Confirm before any destructive .bib edit.** Dedup, auto-fix, and anything that overwrites the user's `.bib` write to a *new* file by default (`--output clean.bib`). When dedup or auto-fix would drop entries or pick a "best" version, show what will be removed and which stays, and ask before applying. The original stays untouched until the user approves.

## Getting a citation: Zotero first, web search fallback

Work down this ladder. Stop at the first rung that yields the entry.

| You have | Do this | Result |
|---|---|---|
| a DOI | `zotero_add_by_doi(doi=...)` | adds the item, fetches CrossRef metadata, attaches the open-access PDF when one exists |
| an arXiv id or a paper URL | `zotero_add_by_url(url=...)` | same, for arXiv URLs, DOI URLs, and general pages |
| a title or author, want to find it | `zotero_search_items(query="Author Year")` | matches in the library; keep the query short, it is substring matching, not web search |
| any of the above, added to Zotero | `zotero_get_item_metadata(item_key=..., format="bibtex")` | the BibTeX entry, ready to paste |

When Zotero is not reachable, fall back in order:

1. **Offline, with a DOI or arXiv id.** `python scripts/extract_metadata.py --doi 10.1145/3065386` (or `--arxiv 1706.03762`) hits CrossRef and arXiv directly and prints BibTeX. Batch a file with `--input ids.txt --output refs.bib`.
2. **No identifier yet.** Find it with web search (the `literature` skill, or `WebSearch` directly), then return to the Zotero or offline path. Do not hand-assemble an entry from a search-result snippet if a DOI is one lookup away.

Never scrape Google Scholar, CrossRef, or DBLP result pages by hand. Discovery and seminal-paper hunting belong to the `literature` skill; this skill takes an identifier or a library item and produces a verified entry.

## Every citation needs a DOI or an arXiv id

Treat this as required for any work published in 2000 or later. It is the anchor that lets verification resolve the real record.

- Journal and conference papers: `doi`.
- Preprints: the arXiv id in `note = {arXiv:1810.04805}` (and `doi` too if one was later assigned).
- Genuinely has neither (pre-2000, some industrial docs): a stable `url` plus a `note` saying why no DOI exists. Flag it rather than leaving the field silently blank.

## BibTeX generation rules

Distilled from the entry-type reference. Full worked examples for every type live in `assets/bibtex_template.bib`.

**Entry type by source:** journal article `@article`; conference paper `@inproceedings`; book `@book`; book chapter `@incollection`; PhD or master's thesis `@phdthesis` / `@mastersthesis`; tech report `@techreport`; preprint, dataset, software, industrial doc `@misc`.

**Required fields:**

| Type | Must have |
|---|---|
| `@article` | author, title, journal, year (plus volume, pages, doi) |
| `@inproceedings` | author, title, booktitle, year (plus pages) |
| `@book` | author *or* editor, title, publisher, year |
| `@incollection` | author, title, booktitle, publisher, year |
| `@phdthesis` / `@mastersthesis` | author, title, school, year |
| `@misc` | author, title, year, and one of doi or url |

**Formatting rules:**

- **Authors** separate with ` and `, never `;`, `,`, or `&`. Use `Last, First` order. For 10+ authors end with `and others`; do not hand-write `et al.`
- **Protect capitalization** with braces so title-case styles do not lowercase it: `{BERT}`, `{ImageNet}`, `{ResNet}`, `{GPU}`.
- **Page ranges** use a double hyphen: `pages = {123--145}`, never `123-145`, no `pp.` prefix.
- **DOI** is the bare identifier: `doi = {10.1145/3065386}`. No `doi:` prefix, no `https://doi.org/` URL, no trailing period.
- **Citation keys** follow `FirstAuthorYEARkeyword` (e.g. `Vaswani2017attention`), alphanumeric plus `-_.:`, no spaces, unique within the file.
- **Special characters** use LaTeX escapes (`M{\"u}ller`, `Garc{\'i}a`) or UTF-8 with the right LaTeX packages; math in `$...$`.
- **Industrial systems** cite as `@misc` with the official-docs URL, a double-braced corporate author (`{{Google}}`), and an accessed-year note; the citation value is proving the design is deployed.

## Verifying reference metadata (the mechanical defense)

Two layers. The first is per-citation reasoning; the second is a batch sweep over the whole file.

### Per citation: does it exist, and does it match?

For each reference, pull the authoritative record and compare field by field. This is what catches a hallucinated paper and a misattributed one, where a real title is pinned to the wrong authors, venue, or year.

1. Resolve the identifier: `zotero_add_by_doi` / `zotero_search_items` for the real metadata, or `scripts/extract_metadata.py --doi ...` offline.
2. Compare against the entry: **authors** (same people, same order), **title** (verbatim), **venue** (`journal` or `booktitle`), **year**, **DOI**. A mismatch is an error, not a warning.
3. If the reference will not resolve anywhere, treat it as likely fabricated until proven otherwise, and tell the user.

For the harder "does this work actually exist and say what the sentence claims" adversarial search (independent re-search, per-candidate existence checks), use the `literature` skill's citation-verification workflow. This skill owns the metadata-accuracy half; that skill owns the existence-and-relevance half.

### Whole .bib: batch mechanical check

Run the validator over the file for the deterministic checks a reader skims past across 150 entries:

```bash
python scripts/validate_citations.py references.bib                 # required fields, duplicates, syntax
python scripts/validate_citations.py references.bib --check-dois    # also resolve DOIs and compare CrossRef metadata
python scripts/validate_citations.py references.bib --report v.json --verbose
```

It flags: required fields missing for the entry type; DOIs that do not resolve or whose CrossRef metadata disagrees with the entry; duplicate DOIs and near-duplicate titles; unbalanced braces, missing commas, invalid or non-unique keys; page ranges with a single hyphen. It only reports, it does not touch the file. Fix errors first (missing fields, broken DOIs, duplicates, syntax), then warnings (missing recommended fields, formatting). The safe mechanical fixes (page ranges, author separators, field order) are applied by `format_bibtex.py` below, which cannot add missing information or choose which duplicate to keep, so review its diff.

**Duplicates worth a manual look:** the same paper under two keys, a preprint plus its published version (keep the published one), a conference paper plus its journal extension.

## Cleaning and formatting a .bib

```bash
python scripts/format_bibtex.py references.bib --output clean.bib                 # fix page ranges, separators, field order (on by default)
python scripts/format_bibtex.py references.bib --deduplicate --sort year --descending --output clean.bib
```

It fixes common issues by default; add `--no-fix` to only reformat. Without `--output` it overwrites the input in place, so always pass `--output`. Per output-discipline rule 5, dedup and any rewrite go to a new file and are confirmed first.

## Bundled resources

- `scripts/validate_citations.py` runs the batch metadata and format check, the mechanical defense above.
- `scripts/format_bibtex.py` formats, sorts, and deduplicates a .bib.
- `scripts/extract_metadata.py` converts a DOI or arXiv id to BibTeX offline, the no-Zotero fallback.
- `assets/bibtex_template.bib` holds correct worked examples for every entry type.

The scripts need `requests` (`pip install requests`). The Zotero path needs the `zotero` MCP server from `.mcp.json` running.
