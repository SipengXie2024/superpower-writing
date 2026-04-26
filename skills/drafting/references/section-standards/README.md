# Section Standards

Section-specific writing conventions injected into `section-drafter` subagent prompts and referenced during outlining. One file per manuscript section; filenames follow a uniform `NN_slug.md` convention (numeric prefix + slug).

## Filename contract

All standards files use the canonical `NN_slug.md` naming scheme. The numeric prefix reflects the section's **canonical position** in a default CS paper layout — it is a sort-order aid for directory listings, NOT a binding stem the manuscript must adopt. Actual manuscripts are free to deviate (e.g., Background shifts from `02` to `03` when §Motivation takes the §2 slot; Related Work may be early `§2` or late `§N-1`). The match rule (next section) handles deviations via slug-ending scanning.

| Standards file        | Canonical slot | Governs                                        | Applies at                        |
|-----------------------|----------------|------------------------------------------------|-----------------------------------|
| `00_abstract.md`      | §0 (Abstract)  | any `manuscript/NN_abstract.tex`               | outline §Abstract + draft         |
| `01_introduction.md`  | §1             | any `manuscript/NN_introduction.tex`           | outline §Introduction + draft     |
| `02_background.md`    | §2             | any `manuscript/NN_background.tex`             | outline §Background + draft       |
| `03_methods.md`       | §3             | any `manuscript/NN_methods.tex`                | outline §Methods + draft          |
| `04_results.md`       | §4             | any `manuscript/NN_results.tex`                | outline §Results + draft          |
| `05_discussion.md`    | §5             | any `manuscript/NN_discussion.tex`             | outline §Discussion + draft       |
| `06_conclusion.md`    | §6             | any `manuscript/NN_conclusion.tex`             | outline §Conclusion + draft       |
| `07_related_work.md`  | §7 (late) or §2 (early) | any `manuscript/NN_related_work.tex`  | outline §Related Work + draft     |
| `08_motivation.md`    | §2 (opt-in)    | any `manuscript/NN_motivation.tex` (opt-in)    | outline §Motivation + draft       |

Canonical numbering assumes no §Motivation, late-placed §Related Work, and Abstract/Introduction/Background/Methods/Results/Discussion/Conclusion as contiguous §0–§6. When §Motivation is opted in, Background shifts to `03_background.md` in the manuscript while the standards file keeps its `02_background.md` name; the match rule reconciles the offset automatically.

### Match rule (two-level fallback, slug-ending match)

The orchestrator takes the manuscript file's **stem** (e.g., `02_background` from `.writing/manuscript/02_background.tex`) and resolves it to a standards file in `section-standards/` (which contains `.md` instruction files that the drafter agent reads verbatim). The scan target is **always the `section-standards/` directory, not `manuscript/`** — the `.md` extension below refers to the standards file's extension, not the manuscript's.

1. **Exact-stem match**: look for `section-standards/<NN>_<slug>.md` — used when the paper's stem number coincides with the canonical slot (e.g., a no-motivation CS paper with `manuscript/02_background.tex` matches `section-standards/02_background.md` directly).
2. **Slug-ending scan**: if step 1 misses, scan `section-standards/` for any file whose name ends in `_<slug>.md`. Exactly one such file → use it. Zero matches → step 3. **Multiple matches** → abort with a configuration error (should never happen given the canonical-one-per-slug convention; indicates accidental duplicate).
3. **No match**: substitute `No section-specific standard applies; use general IMRAD conventions from writing-principles.md.` as `{SECTION_STANDARD}`.

Practical outcomes (manuscript `.tex` stem → matched standards `.md` file):

- `manuscript/02_background.tex` → exact match `section-standards/02_background.md` (default CS layout, no motivation).
- `manuscript/03_background.tex` → step 1 miss (no `03_background.md` in section-standards), step 2 finds `02_background.md` (slug-ending match) → use it (motivation-opted-in CS layout).
- `manuscript/02_related_work.tex` → step 1 miss, step 2 finds `07_related_work.md` → use it (early-placement Related Work).
- `manuscript/07_related_work.tex` → exact match `07_related_work.md` (late-placement Related Work, canonical).
- `manuscript/02_motivation.tex` → step 1 miss, step 2 finds `08_motivation.md` → use it.

Renaming a file in this directory (e.g., creating a paper-specific `section-standards/02_methods_alt.md`) is the escape hatch for per-paper customization — step 1 will find it before step 2. Until you need that, the canonical files apply everywhere.

## How the standards file is consumed

1. **Outlining** — `superpower-writing:outlining` Step 3 applies the match rule above for each section and, if a file is found, reads it before drafting outline bullets for that section. The standards file dictates bullet structure, labels, and count. Bullets must pass the outline-level checks in the standards file before the outline is considered complete.

2. **Drafting** — `superpower-writing:drafting` orchestrator applies the same match rule when assembling the per-section `section-drafter` subagent prompt. The file content is inlined into the `{SECTION_STANDARD}` placeholder in `section-drafter-prompt.md`. If neither the exact-stem nor slug-ending match finds a file, `{SECTION_STANDARD}` is replaced with `No section-specific standard applies; use general IMRAD conventions from writing-principles.md.`

3. **Self-review** — Step C of the drafter template re-reads the same resolved standards file and greps the draft for the required structural tags (e.g., `% bpmrc: B`, `% cars: T`, `% background: D`). A missing tag blocks the section from being marked `drafted`.

## Required content in every standards file

Each file MUST contain the following H2 sections, in this order:

1. `## Framework` — short name + expanded form (e.g., "BPMRC: Background-Problem-Method-Result-Conclusion") and a one-paragraph rationale.
2. `## Role of each element` — table with columns *Element / Sentences / Purpose*. One row per structural element.
3. `## Outline bullet requirement` — exact bullet count, order, and labeling scheme for `.writing/outline.md`.
4. `## Draft requirement` — paragraph structure, required LaTeX comment tags (e.g., `% bpmrc: B`), ordering, and length budget for `.writing/manuscript/<stem>.tex`.
5. `## Style rules` — tense, voice, allowed citation forms, venue-specific caveats.
6. `## Common failure modes` — 3–5 concrete patterns reviewers flag, with a short diagnosis.

The `section-drafter` agent reads the file verbatim — do not use relative links that would break when the content is inlined into a subagent prompt.

## Frontmatter

```yaml
---
section: <human-readable name, e.g. abstract>
stem: <canonical filename stem, e.g. 00_abstract>
framework: <short framework name, e.g. BPMRC>
---
```

The orchestrator does not parse this frontmatter today, but keeping it stable future-proofs automation (e.g. a lint pass that checks every outline section has a matching standards file).

## Why this directory exists

The plugin's `writing-principles.md` reference specifies IMRAD voice and style at the whole-paper level. It does NOT prescribe the internal skeleton of each section. Different venues and subfields prefer different skeletons: structured abstracts with BPMRC vs. narrative abstracts; CARS-model introductions vs. funnel introductions; single-paragraph vs. multi-paragraph methods.

Rather than baking one opinionated skeleton into the drafting prompt, this directory lets us plug in the right skeleton per section. Add files here as the plugin learns new conventions; existing papers are unaffected because only sections with a matching standards file get constrained.
