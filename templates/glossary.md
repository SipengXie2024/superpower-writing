# Glossary (term-definition-before-use)
#
# Opt-in companion to the claim-first protocol. Copy this file to
# `.writing/glossary.md` (preserving the name) to activate the
# term-definition-before-use discipline.
#
# Format: YAML list. Each entry:
#   - id:         kebab-case token used inside `% define: <id>` and
#                 `% use: <id>` LaTeX line comments.
#   - term:       human-readable phrase as it appears in prose.
#   - definition: one-sentence meaning. Informational; not used by
#                 the ordering rule.
#   - defined_in: stem of the .tex file where the term is first
#                 introduced (no extension, no `.writing/manuscript/`
#                 prefix). Ordering is by numeric prefix, so
#                 `02_background` precedes `03_methods` regardless of
#                 alphabetical order of the slug.
#
# The define-before-use discipline requires:
#   1. Every `% define: <id>` appears in the file whose stem equals
#      glossary[id].defined_in.
#   2. Every `% use: <id>` appears in a section >= defined_in (numeric
#      prefix compare) and references an id that exists in this file.
#   3. Within a single file, the first `% define:` must precede the
#      first `% use:` for the same id.
#
# Sections whose stem matches `abstract`, `references`, or
# `acknowledgments` are fully exempt — abstracts reference terms
# defined later in the body.
#
# Example (delete and replace with real entries):
# - id: skeleton-family
#   term: skeleton family
#   definition: Structurally identical contracts differing only in a bounded set of embedded constants.
#   defined_in: 02_background

[]
