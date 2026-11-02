# Full-text relevance: read the cited passage

A citation is relevant only when a passage in the cited paper says what our sentence uses it for. Abstracts compress, round numbers, and omit the limits that decide whether our sentence is fair to the work; the body holds those limits, and a reviewer who wrote the cited paper checks it. This procedure is shared by claim-verification Pass 2c, the literature skill's citation verifiers, the PC-paper admission check, and the citation-auditor agent.

## The record every citation ends with

```yaml
- type: citation
  citekey: Kwon2023vllm
  doi: 10.1145/3600006.3613165
  fulltext: .writing/papers/Kwon2023vllm.txt   # or zotero:<item_key>
  version: arXiv preprint                      # published | arXiv preprint | local file
  quote: "This design alleviates internal fragmentation by using relatively small blocks and allocating them on demand."
  page: 2
  quote_verified: true                         # written by find_passages.py, never by hand
  supports: "<our sentence, verbatim>"
  relevance: supported                         # supported | partial | not-supported | unverified-relevance
```

`quote_verified` is a mechanical fact: the script found the quote in the text. `relevance` is a judgment about whether that quote carries our sentence, and the agent that wrote the sentence does not make it (see the last section).

## Step 1: get the full text

Work down the ladder; stop at the first rung that yields text.

1. **Zotero, when enabled.** `zotero_add_by_doi` attaches the open-access PDF when one exists. For a library item with an attachment, `zotero_semantic_search(query=<our sentence>, filters={"parent_item_key": <key>}, limit=3)` returns the best-matching body chunks directly; read their `matched_text`. Use `zotero_get_item_fulltext(item_key=<key>)` only for a narrow follow-up read; it returns the whole paper, so search it for the passage.
2. **Open access on the network.** `python3 scripts/fetch_fulltext.py --doi <DOI> --key <citekey> --out-dir .writing/papers`, or `--arxiv <id>`. It tries the published open-access PDFs OpenAlex lists, then the arXiv preprint, checks the file really is a PDF, and writes `<citekey>.txt` with pages separated by form feeds plus a provenance `<citekey>.json`. Every attempted URL is in the output.
3. **Open, but blocked for scripts.** Publishers behind Cloudflare (ACM Digital Library among them) answer a server with HTTP 403 even for open-access PDFs; the script lists those URLs under `blocked_for_scripts`. A real desktop browser on a home network passes the same check. When the environment has one (the user's own workstation reachable over ssh), open the PDF URL there, copy the saved file into a fresh empty directory, and run `fetch_fulltext.py --pdf <path> --key <citekey>`. Do this also when the script fell back to the arXiv preprint and the citation needs the published version's numbers.
4. **Paywalled, no preprint.** The script exits 1 and prints the landing page. Ask the user once for the PDF: they attach it to the Zotero item, or drop it anywhere and you run `fetch_fulltext.py --pdf <path> --key <citekey>`. Until then the citation is `unverified-relevance`.

`.writing/papers/` holds copyrighted PDFs; `init-writing-dir.sh` adds it to `.gitignore`. Never commit it.

**Version.** When the text came from an arXiv preprint and the bib entry cites the published version, record `version: arXiv preprint`. A number or claim that matters (a speedup, a bound, a dataset size) must be confirmed against the published version, because camera-ready revisions change them; get it through rung 3 when the publisher blocked the script, and if only the preprint is reachable, say so next to the citation.

## Step 2: find the passage

Never read a paper whole into context. Rank its paragraphs against our sentence:

```bash
python3 scripts/find_passages.py .writing/papers/<citekey>.txt --query "<our sentence>" --top 5
```

Read the top passages with their page numbers. When none of them touches the sentence, rephrase the query with the paper's own vocabulary (its system name, its metric names) and run again before concluding it does not support us. Also read the paper's limitations or threats-to-validity paragraph when our sentence generalizes its result: `--query "limitation assume only evaluated"` usually finds it.

## Step 3: pin the quote

Pick the shortest passage (at least eight words) that carries the support, copy it verbatim, and confirm it exists:

```bash
python3 scripts/find_passages.py .writing/papers/<citekey>.txt --quote "<passage>" --json
```

Exit 0 gives `quote_verified: true` and the page; write both into the record. Exit 1 means the quote is not in the paper: it was paraphrased or remembered, which is exactly the failure this step exists to catch. Copy the quote again from the text and rerun the check.

## Step 4: judge support

Compare the quote with our sentence on four points. Any failure downgrades the verdict.

| Check | Fails when |
|---|---|
| Same claim | the quote describes a neighbouring result (a different workload, model, or metric) |
| Same strength | our sentence says "eliminates" and the paper says "reduces"; "always" against "in our experiments" |
| Same numbers | our number differs from the paper's, or drops its condition (the speedup was "up to", or on one dataset) |
| Same scope | the paper states a limit our sentence ignores |

Verdicts:

- `supported`: all four hold.
- `partial`: the paper supports a weaker or narrower version. Report the exact narrower wording that the quote would carry.
- `not-supported`: the quote does not carry the sentence, or the body contradicts it. The citation leaves this sentence (it may still fit another one).
- `unverified-relevance`: no full text could be obtained. Abstract-level agreement is recorded as a note on this verdict.

## Who judges

Steps 1 to 3 are mechanical and the agent doing the verification runs them. Step 4 is a judgment, and the agent that drafted the sentence or proposed the citation must not acquit its own choice. Hand the judgment to a fresh-context reviewer with the paper text path, the page, the quote, and our sentence, and let it read the passage itself; do not pass along the drafter's summary of why the citation fits. The reviewer's verdict goes into the record.
