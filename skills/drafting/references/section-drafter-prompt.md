# Section-drafter subagent prompt template (LaTeX)

This is the exact prompt body every section-drafter subagent receives, customized only with the section number, slug, the verbatim task text from `.writing/plan.md`, and the section-specific standard (if one applies). Copy it into the dispatch prompt exactly — do not paraphrase the claim-first warnings or the section-standard block; they are what makes the PreToolUse hook and the structural self-review survivable.

The orchestrator (`subagent-driven` / `team-driven` / `executing-plans`) wraps this template with whatever review gates that engine specifies. The template body itself stays identical across modes. Before dispatch, the orchestrator resolves two placeholders:

- `{INSERTED}` — the verbatim task text from `.writing/plan.md §Task-{NN}`.
- `{SECTION_STANDARD}` — resolved via two-level fallback (slug-ending match):
  1. try `references/section-standards/{NN}_{slug}.md` (exact-stem match — hits when the manuscript's stem number equals the standards file's canonical slot);
  2. if step 1 misses, scan `references/section-standards/` for any file whose name ends in `_{slug}.md`; exactly one match → use it; multiple → abort with configuration error (indicates a duplicate standards file);
  3. if both miss, substitute `No section-specific standard applies; use general IMRAD conventions from scientific-writing.`

  Canonical filenames: `00_abstract.md`, `01_introduction.md`, `02_background.md`, `03_methods.md`, `04_results.md`, `05_discussion.md`, `06_conclusion.md`, `07_related_work.md`, `08_motivation.md`. Examples of slug-ending resolution: `03_background` → `02_background.md`; `02_related_work` → `07_related_work.md`; `02_motivation` → `08_motivation.md`. See `references/section-standards/README.md` for the complete contract.

```
You are drafting section {NN}: {slug} of the manuscript.

Output format: LaTeX. Manuscript file is .writing/manuscript/{NN}_{slug}.tex.
All load-bearing metadata (claim tags, structural tags, draft-only markers) go
in LaTeX line comments (`%` at column 0). Do NOT produce Markdown — the hook
only intercepts .tex files and the submission gate expects LaTeX.

## Inputs (read before writing)
- Task text (verbatim from .writing/plan.md §Task-{NN}): {INSERTED}
- Claims file: .writing/claims/section_{NN}_{slug}.md
- Outline: .writing/outline.md
- Metadata: .writing/metadata.yaml
- refs.bib: .writing/refs.bib (may be empty at first; populated by submission)
- Any upstream sections already drafted in .writing/manuscript/*.tex

## Section standard (governs prose structure)
{SECTION_STANDARD}

The section standard above (when not the "no standard applies" fallback) is
binding. It dictates paragraph count, required structural tags (e.g.,
`% bpmrc: X` for an abstract under BPMRC), tense/voice rules, and length
budget specific to this section. Treat it as a second non-negotiable layer
on top of the claim-first protocol: the claim-first hook enforces
evidence→prose discipline; the section standard enforces skeletal shape.
If the standard conflicts with the outline or task text, STOP and surface
the conflict to the orchestrator rather than silently picking one.

## Claim-first protocol (NON-NEGOTIABLE)
You MUST resolve every claim's EVIDENCE (Step A) BEFORE writing any prose
(Step B). The PreToolUse hook will block your Write tool call otherwise — see
superpower-writing:main §Claim-First Protocol for the block rules. Do NOT
fight the hook: read the decision JSON on stderr, fix the claim file or the
prose tag, retry.

## Step A — Evidence resolution (required before any prose)
For each claim in .writing/claims/section_{NN}_{slug}.md with STATUS=stub:

  A.1 Check .writing/metadata.yaml for `zotero.enabled`.
  A.2 If zotero.enabled is true:
        Call the `zotero_search_items` MCP tool (provided by the `zotero`
        server in `.mcp.json`) with:
            query = <DOI>
            qmode = "everything"
        Then filter the returned items to those whose `data.collections`
        includes `collection_key`. On a single filtered hit:
            - Call `zotero_get_item_metadata(item_key=<key>)` to fetch
              the stored abstract.
            - Record in the EVIDENCE entry:
                source: zotero
                zotero_item_key: <key>
            - Advance claim STATUS to `evidence_ready`.
        Empty-filter or ambiguous-match is treated as a miss; fall through
        to A.3.
  A.3 Zotero miss, or zotero.enabled is false:
        Invoke Skill(skill="research-lookup") / Skill(skill="citation-management")
        to resolve. On network hit:
          - If zotero.enabled AND metadata.yaml's zotero.auto_push_new_citations
            is true:
              Call `zotero_add_by_doi(doi=<DOI>, collection_key=<key>)` from
              the `zotero` MCP server. The tool dedups by DOI. Record in the
              EVIDENCE entry:
                source: both
                zotero_item_key: <returned key>
                citekey: <returned citekey if present, else leave blank>
          - Else (zotero disabled or auto_push off):
              source: network only.

  A.4 Save the updated claims file. Do NOT edit manuscript/*.tex yet.

Only AFTER every claim for this section is STATUS ∈ {evidence_ready, verified}
may you proceed to Step B.

## Step B — Prose (LaTeX)
Write .writing/manuscript/{NN}_{slug}.tex.

Structure rules:
  - Every load-bearing paragraph MUST carry a LaTeX line-comment tag on its
    own line at column 0 (allowing leading whitespace):
      * `% claim: id` for paragraphs asserting a claim backed by EVIDENCE.
      * `% draft-only` for scaffolding / placeholder notes the hook should
        let through (remove these before claim-verification).
    Place the tag on the line immediately above the paragraph it applies to.
  - One primary claim per paragraph is the norm; if a paragraph genuinely
    asserts two claims, include two tag lines back-to-back:
      % claim: meth-c1
      % claim: meth-c2
      <paragraph prose>
  - Cite prior work using `\cite{citekey}` — the standard LaTeX citation
    command. The citekey MUST match an entry that will exist in
    .writing/refs.bib after `submission` runs the Zotero export. Do NOT
    invent citekeys. If the claim's EVIDENCE has no citekey, the claim is
    not evidence_ready — go back to Step A.
  - Multiple citations at the same site: `\cite{smith2019,chen2020,zhang2021}`
    (comma-separated inside a single \cite{}), NOT three separate \cite{}s.
  - Respect the upstream `scientific-writing` style rules: IMRAD voice, past
    tense for results, active voice where appropriate.
  - Respect the section standard supplied above:
      * Match the required paragraph count and ordering exactly.
      * Emit every required structural tag (e.g. `% bpmrc: B` through
        `% bpmrc: C` for an abstract under BPMRC). These tags are IN
        ADDITION to claim/draft-only tags, not a replacement. Stack them
        immediately above the paragraph:
          % bpmrc: B
          % claim: abs-b1
          <paragraph prose>
      * Honor the standard's tense/voice/length rules; they refine — never
        contradict — the upstream scientific-writing rules.
      * If the standard's tags appear in a section stem that is claim-enforced
        (anything whose slug is NOT `abstract` / `references` /
        `acknowledgments`), each paragraph still needs either `% claim: id`
        or `% draft-only` for the hook. UNPROTECTED slugs are exempt from
        claim-tag enforcement but must still emit the structural tags their
        standard requires.

LaTeX syntax rules:
  - Section headings: `\section{Title}`, `\subsection{Title}`. Do NOT use
    Markdown `#`/`##`/`###` — this is LaTeX.
  - Emphasis: `\textbf{bold}`, `\textit{italic}` or `\emph{italic}`. NOT
    `**bold**` or `*italic*`.
  - Lists: `\begin{itemize}\item ... \end{itemize}` or
    `\begin{enumerate}\item ... \end{enumerate}`. NOT Markdown `-` or `1.`.
  - Inline math: `$x^2 + y^2$`. Display math: `\[ ... \]` or
    `\begin{equation} ... \end{equation}` (number only what §Results
    references).
  - Figures:
      \begin{figure}[t]
        \centering
        \includegraphics[width=\columnwidth]{figures/pipeline.pdf}
        \caption{Pipeline overview.}
        \label{fig:pipeline}
      \end{figure}
    Refer with `Figure~\ref{fig:pipeline}` (use `~` to prevent line break).
  - Tables: `\begin{table}[t]` with `\begin{tabular}{lrrr}` inside. Refer
    with `Table~\ref{tab:main}`.
  - Pseudocode: `\begin{algorithm}` + `\begin{algorithmic}` (algorithmicx
    package). Refer with `Algorithm~\ref{alg:main}`.
  - Escape special characters: `\%`, `\&`, `\$`, `\#`, `\_`, `\{`, `\}`,
    `\^{}`, `\~{}`, `\textbackslash`. A bare `%` starts a line comment and
    will swallow the rest of the line — common source of silent errors.

## Step C — Bookkeeping (before returning)
  1. Self-review (claim-first): grep your file for tag patterns and confirm
     every id resolves to an entry in the claims file:
       grep -nE '^\s*% claim:' .writing/manuscript/{NN}_{slug}.tex
     Every matched id must appear in .writing/claims/section_{NN}_{slug}.md
     with STATUS ∈ {evidence_ready, verified}.
  2. Self-review (section standard): if the section standard above prescribes
     structural tags, grep the draft for each required tag and confirm the
     count and ordering match what the standard demands. For BPMRC abstracts:
       grep -nE '^\s*% bpmrc: [BPMRC]' .writing/manuscript/{NN}_{slug}.tex
     must return exactly 5 lines, one each for B, P, M, R, C, in that order.
     For CARS introductions:
       grep -nE '^\s*% cars: [TNO]' .writing/manuscript/{NN}_{slug}.tex
     must have at least 1 each of T / N / O in T → N → O order. Similar
     checks apply to the other frameworks (see each standards file's
     "Draft requirement" section). If any check fails, fix the draft and
     re-run before proceeding. Do not mark the section drafted with a
     structural mismatch.
  3. Self-review (citations): grep your file for \cite{} and confirm every
     citekey exists in the claims file as some claim's EVIDENCE citekey:
       grep -oE '\\cite\{[^}]+\}' .writing/manuscript/{NN}_{slug}.tex
     Expand comma-separated keys (e.g. `\cite{a,b,c}` → a, b, c). Any citekey
     not backed by an evidence-resolved claim is a hallucinated citation —
     fix by going back to Step A.
  4. Update .writing/progress.md Task Dashboard row for this section:
       | {NN}_{slug} | drafted | <claim-pass count>/<total> | pending | - | <key outcome> |
     Set "Citation Check" to "pending" (claim-verification skill fills it later).
  5. Append a one-line entry to the session log.
  6. Commit:
       git add .writing/manuscript/{NN}_{slug}.tex \
               .writing/claims/section_{NN}_{slug}.md \
               .writing/progress.md
       git commit -m "draft: section {NN} {slug}"

## Failure modes to escalate (do NOT silently fix)
  - A claim has no credible source after both Zotero and network lookup.
  - The section task text in .writing/plan.md conflicts with the outline.
  - A prior section's claims are needed but that section is still stub.
  - PreToolUse hook keeps blocking after 2 honest attempts to fix — the hook or
    the claim parser may be misconfigured; surface to the orchestrator.
  - The section standard conflicts with the outline or task text (e.g., BPMRC
    demands 5 bullets but the outline provides only 3). Do NOT pick one and
    proceed; surface the conflict so the user or orchestrator can resolve.
  - A \cite{} citekey cannot be resolved to a Zotero item and
    zotero.auto_push_new_citations is false. Surface so the user can either
    enable auto-push or manually add the reference to Zotero.
```
