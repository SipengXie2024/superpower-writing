# Terminology Ledger

A paper must use one name for one thing. The same system, model, dataset,
algorithm, module, metric, or concept must not drift across shifting names,
spellings, or capitalizations. Reviewers read inconsistent terminology as
careless work. A term that changes between sections forces the reader to
re-learn it. An OSDI or NeurIPS reviewer who re-learns a name twice soon
distrusts the rest of the paper.

Build the ledger **before** drafting or polishing prose. Treat it as the single
source of truth for naming across the whole job. Consistency against a standard
is impossible when the standard was never written down.

This is the **authoring** half of terminology control. It pairs with two
enforcement mechanisms already in the plugin. The `enforce-terms.py` glossary
gate is opt-in, activated by `.writing/glossary.md`. It enforces
define-before-use ordering at write time. The drafting skill's
locked-term-rename discipline turns any rename of a locked term into an audited
cross-file pass. The ledger feeds both. See the "Pairing" section at the end.

## What this is and is not

This file is a reference fragment, not a standalone skill. Sibling skills load
it to share one ledger format and one set of rules. Outlining loads it at
structure time, drafting at write time, polish before its two passes. It does
not own a PreToolUse hook and never mutates state on its own. Like every verdict
in this plugin, a flagged collision is **advisory**. Surface it to the user and
let the user choose the canonical form. Never auto-rename prose, never auto-edit
the glossary, never coin a name to fill a gap.

## 1. Build the ledger on first contact

When you first receive an outline, a draft, or notes, extract every recurring
load-bearing term into a ledger before editing prose. For CS, systems, and ML
papers the term categories are:

- systems, methods, models, algorithms, modules, frameworks, protocols
- datasets, benchmarks, corpora, workloads, traces
- metrics, units, statistical symbols, mathematical notation
- abbreviations and acronyms, each paired with its full form
- the named contributions and key concepts the paper defines or relies on
  repeatedly

For each term, record its canonical surface form, its first-use expansion when
it is an abbreviation, and any variants already present in the source. Do not
invent the canonical form. Read it off the source, off the user's stated
preference, or off the field's standard nomenclature.

## 2. Present the ledger to the user

Show a compact table before or alongside the first output. The four columns are
fixed.

| Canonical term | First-use definition | Variants seen | Decision |
|---|---|---|---|
| KV-cache | key-value cache (KV-cache) | "KV cache", "kv-cache", "key/value store" | spell out once, then use "KV-cache" |
| Pareto frontier | the set of non-dominated configurations | "Pareto front", "pareto-optimal set" | use "Pareto frontier" throughout |
| MoE | mixture-of-experts (MoE) | "Mixture of Experts", "mixture of expert" | expand at first use, then "MoE" |

Flag every collision explicitly. A collision is either the same concept under
two names, or one name reused for two different concepts. The second kind is the
more dangerous. It makes a sentence ambiguous about which thing it asserts.

Resolve the easy cases yourself. Adopt the form the source uses most often and
state that choice in the Decision column. Ask the user with `AskUserQuestion`
only when the decision is genuinely ambiguous or domain-sensitive. Two
field-standard names may compete, as with `self-attention` versus
`intra-attention`. Or the user named a contribution and the source spells it
three ways.

## 3. Lock and enforce the canonical forms

Once set, the ledger is fixed for the rest of the job. Three rules govern every
output.

**One name per thing.** Each concept gets exactly one canonical surface form.
Do not introduce synonyms to vary the prose.

**Terminology consistency outranks lexical variety.** Scientific writing is the
one register where repeating the same word is correct. A reader who sees
"throughput", "ingest rate", and "processing speed" in three sections cannot
tell whether they are one metric or three. Pick one and repeat it. This rule
overrides the usual prose advice against repetition. It also overrides the
humanizer instinct to swap a fixed term for a synonym.

**Never coin new names.** Do not invent a name for the author's system, module,
metric, or concept. A term may be missing, undefined, or used inconsistently in
a way you cannot resolve from the source. Then ask the user or mark it
`[NEEDS-EVIDENCE]` with a one-line note. Never fill the gap with a guessed name.
A fabricated system name is as corrupting as a fabricated citation.

Two operational corollaries follow from these rules:

- Define each abbreviation once, at its first use across the paper, then use the
  short form everywhere after. Keep units, symbols, and notation identical in
  every section.
- When drafting or polishing a later section, reference the ledger built from
  the earlier sections instead of re-deciding the name term by term. Re-deciding
  per section is how drift starts.

## 4. Renames are cross-file events

If the user renames a locked term after drafting has begun, the change is not a
single-passage edit. Change every occurrence across the manuscript, update the
ledger, and record the rename so the audit trail survives. This is the drafting
skill's locked-term-rename discipline. The ledger is the index that tells you
which sections to touch. Applying a locked-term rename as a one-file edit
silently desynchronizes the paper from its naming history. It reintroduces the
exact drift the ledger exists to prevent.

## Pairing with the enforcement halves

The ledger is authoring-time guidance. Two enforcement mechanisms turn it into
checked invariants when the project opts in.

**The `enforce-terms.py` glossary gate.** This opt-in PreToolUse hook activates
when `.writing/glossary.md` exists. The glossary is a YAML list of entries of
the form `{id, term, definition, defined_in}`. The `defined_in` field is the
stem of the `.tex` section file that first introduces the term. The hook then
enforces ordering across the manuscript:

- A `% define: <id>` comment must sit in the section whose stem equals
  `glossary[id].defined_in`.
- A `% use: <id>` comment must sit in a section at or after the define section.
  Numeric stem prefixes compare as integers, so `02_background` precedes
  `03_methods`.
- Within one file, the first `% define:` must precede the first `% use:` for the
  same id.
- Sections whose stem ends in `abstract`, `references`, or `acknowledgments` are
  exempt. Abstracts legitimately name terms the body defines later.

The ledger and the glossary are two views of the same naming decision. Each
ledger row that names a load-bearing term maps to one glossary entry. The
canonical term becomes `term`. The first-use definition becomes `definition`.
The section that introduces it becomes `defined_in`. Build the ledger first,
then materialize the glossary from it if the project wants the gate. The hook
checks ordering. It does not check whether the prose uses the canonical
spelling. That last mile is the ledger's job and the author's eye.

**The locked-term-rename discipline.** Described in section 4 above. The ledger
supplies the list of affected sections. The drafting skill supplies the one-pass
rename and the audit-trail entry.

Both enforcement halves are opt-in and advisory by design. The ledger never
forces them on. It records the canonical names, surfaces collisions to the user,
and leaves the decisions and the state changes to the user.
