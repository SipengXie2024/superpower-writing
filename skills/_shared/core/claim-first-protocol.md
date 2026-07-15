# Claim-first protocol

The shared contract behind evidence-backed drafting. `drafting` follows it when writing prose, `claim-verification` checks it mechanically, and `outlining` and `rebuttal` rely on its terms. This file is the single source of truth for the tag rules, the STATUS states, and the citation-placement rule.

## Paragraph tags

Every load-bearing paragraph in `.writing/manuscript/*.tex` carries a LaTeX line-comment marker at column 0 (leading whitespace allowed):

- `% claim: <id>` links to an entry in `.writing/claims/section_<NN>_<slug>.md` with fields `id`, `CLAIM`, `EVIDENCE`, `STATUS`.
- `% draft-only` marks scratch prose to be replaced before the next stage; it is exempt from claim tracking and must be gone before `claim-verification`.

`STATUS` runs `stub` -> `evidence_ready` -> `verified`:

- `stub`: created at outlining; EVIDENCE is a placeholder. Prose must not cite a stub.
- `evidence_ready`: drafting resolved every EVIDENCE item (DOI resolves, dataset accessible, figure drawn).
- `verified`: `claim-verification` confirmed the citation resolves and the source supports the claim.

## Claim-first discipline

Never write prose (Edit / Write / MultiEdit) into `**/manuscript/*.tex` when a `% claim: id` tag references a claim with `STATUS: stub`, when the claim file is missing, or when untagged load-bearing prose lands in a tagged section. In each case resolve evidence first: look the source up via `superpower-writing:literature` or `superpower-writing:citations` (Zotero-first when `zotero.enabled`), bump `STATUS` to `evidence_ready`, then write.

## Exempt sections

The paragraph-tag rule exempts any section stem whose slug is `abstract`, `references`, or `acknowledgments`, matched by slug-ending (`00_abstract` matches `_abstract`, `09_references` matches `_references`). Every other `manuscript/NN_*.tex` file requires each load-bearing paragraph to carry `% claim: id` or `% draft-only`.

Markdown files (`.md` under `manuscript/`) fall outside this discipline; the plugin operates on LaTeX only. Convert a stray `.md` to `.tex` before `claim-verification`.

## Citation placement

The abstract is **citation-free**: any stem ending in `_abstract` must contain no LaTeX citation command (`\cite`, `\citep`, `\citet`, `\nocite`, `\parencite`, `\textcite`, `\autocite`, `\footcite`, `\citeauthor`, `\citeyear`, or any `\*cite*` variant) and no `% claim: id` tag. The abstract summarizes the paper's own findings; references belong in the body.

Every body section (`01_introduction.tex`, `03_methods.tex`, `04_results.tex`, and so on) must back each load-bearing claim with a `\cite{citekey}` whose key resolves against `.writing/refs.bib`. Missing citations surface as failures in `claim-verification` Pass 2.

`drafting` and `claim-verification` both uphold this discipline and surface any violation to the user. The fix is always the same: resolve EVIDENCE first, bump `STATUS`, then write prose.
