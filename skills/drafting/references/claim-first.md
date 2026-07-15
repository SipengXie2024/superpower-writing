# Drafting protocol : claim-first, inline

You draft each manuscript section yourself, in outline order. No mode selection, no parallel subagents, no review pipeline. For each section: resolve evidence first, then write LaTeX prose tagged with its claim ids. Output goes to `.writing/manuscript/{NN}_{slug}.tex`.

All load-bearing metadata (claim tags, structural tags, draft-only markers) lives in LaTeX line comments (`%` at column 0). Do not emit Markdown, `claim-verification` expects LaTeX.

## Read before writing a section

- The section's claims file: `.writing/claims/section_{NN}_{slug}.md`
- `.writing/outline.md`, `.writing/metadata.yaml`
- `.writing/refs.bib` (may be empty at first; fills as citations resolve)
- Any upstream sections already in `.writing/manuscript/*.tex`
- The matching section standard (below) and `references/style-cautions.md`

## Claim-first (non-negotiable)

Resolve every claim's EVIDENCE before writing any prose for it. Prose written against a `STATUS: stub` claim violates the discipline. See [`../../_shared/core/claim-first-protocol.md`](../../_shared/core/claim-first-protocol.md) for the rules. `claim-verification` is the mechanical backstop that later confirms every tag resolves, but resolve evidence now, do not lean on the later check.

### Step A : Evidence resolution (before prose)

For each claim with `STATUS: stub` in the section's claims file:

1. Read `.writing/metadata.yaml` for `zotero.enabled`.
2. **Zotero-first** (when `zotero.enabled: true`): call `zotero_search_items` (from the `zotero` MCP server) with `query = <DOI>`, `qmode = "everything"`; keep items whose `data.collections` includes `collection_key`. On a single hit, call `zotero_get_item_metadata(item_key=<key>)`, record `source: zotero` + `zotero_item_key: <key>`, advance `STATUS: evidence_ready`. Empty or ambiguous match is a miss.
3. **Network fallback** (Zotero miss or disabled): use `superpower-writing:literature` or `superpower-writing:citations` to resolve. On a hit, if `zotero.enabled` and `zotero.auto_push_new_citations` are both true, call `zotero_add_by_doi(doi=<DOI>, collection_key=<key>)` (dedups by DOI) and record `source: both` + the returned key/citekey; otherwise record `source: network`.
4. Save the claims file. Do not touch `manuscript/*.tex` yet.

Only after every claim in the section is `STATUS ∈ {evidence_ready, verified}` may you write prose. A Zotero miss is normal, not a failure; the only hard failure is no credible source anywhere, which you escalate.

### Abstract exception (slug ends in `abstract`)

Abstracts are citation-free and have no claims file. Skip Step A. Emit no `\cite`/`\citep`/`\citet`/`\nocite`/any `\*cite*` command and no `% claim:` tag. Still emit the BPMRC structural tags (`% bpmrc: B/P/M/R/C`) the standard requires, those are not citations. Restate the body's findings in your own words.

## Step B : Prose (LaTeX)

Write `.writing/manuscript/{NN}_{slug}.tex`. Before writing the section intro, overview paragraph, thesis sentence, or contribution bullets, read `references/style-cautions.md` and clear its scans against your intended prose.

Tagging:
- Every load-bearing paragraph carries a tag line at column 0 immediately above it: `% claim: id` for a paragraph asserting an evidence-backed claim, or `% draft-only` for scaffolding (remove before `claim-verification`).
- Two claims in one paragraph → two back-to-back `% claim:` lines.
- Cite with `\cite{citekey}`; the citekey must match a `refs.bib` entry that will exist once resolved. Never invent citekeys, an unbacked citekey means the claim is not `evidence_ready`, so return to Step A. Multiple citations share one command: `\cite{a,b,c}`.

Structural tags: the section standard (below) may require tags such as `% bpmrc: B` or `% cars: T`. Stack them above the claim tag:
```
% bpmrc: B
% claim: abs-b1
<paragraph prose>
```
Unprotected slugs (`abstract`, `references`, `acknowledgments`) are exempt from claim tags but still emit their standard's structural tags.

LaTeX syntax essentials: `\section{}`/`\subsection{}` (not `#`); `\textbf{}`/`\emph{}` (not `**`); `itemize`/`enumerate` (not `-`); `$...$` inline, `\[...\]` or `equation` display; figures via `\includegraphics` inside `figure`, referenced `Figure~\ref{fig:x}` (use `~`); tables via `tabular` inside `table`; escape `\%`, `\&`, `\$`, `\#`, `\_`, a bare `%` starts a comment and silently eats the line.

## Section standard (readable guidance, not a gate)

For each section, read the matching file under `references/section-standards/` (resolve by slug: try `{NN}_{slug}.md`, else the single `*_{slug}.md`). It describes the section's shape, paragraph count, required structural tags, tense and length. Treat it as guidance that refines `references/writing-principles.md`, not a mechanical checkpoint. If the standard genuinely conflicts with the outline or the claim set (e.g. it wants 5 abstract bullets but the outline gives 3), stop and surface the conflict to the user rather than silently picking one.

When `.writing/metadata.yaml` has `writing_profile: systems`, also read `references/systems-evidence-contract.md` for structured `analysis`/`artifact` evidence and the Results/Discussion boundary.

## Step C : Bookkeeping

1. A quick self-read: does every `% claim: id` in the file match an `evidence_ready`/`verified` entry in the claims file, and does every `\cite{}` citekey trace to a resolved claim? Fix anything that does not. The exhaustive mechanical sweep is `claim-verification`'s job, run it after the section, do not rebuild it here.
2. Update the section's row in `.writing/progress.md` (Status `drafted`, claim ratio, key outcome) and append a one-line session-log entry.
3. Commit the manuscript file, its claims file, and `progress.md`.

## Escalate (do not silently fix)

- A claim has no credible source after Zotero and network lookup.
- The section task or standard conflicts with the outline.
- A prior section's claims are needed but still stub.
- A `\cite{}` citekey cannot resolve and `zotero.auto_push_new_citations` is false.
