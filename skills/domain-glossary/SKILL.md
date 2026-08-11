---
name: domain-glossary
description: Builds and maintains the project's shared vocabulary (ubiquitous language) in a repo-root CONTEXT.md that persists across papers. Use when pinning down terminology, when the same concept keeps drifting across names in conversation or notes, when a term turns ambiguous, or when idea, outlining, or drafting work names a new system, method, or concept. Pairs with the terminology ledger, which governs surface forms inside one manuscript. 中文触发：定术语、统一叫法、术语表。
---

# Domain Glossary

Maintain the project's ubiquitous language: one canonical term per concept, recorded in `CONTEXT.md` at the repo root, used consistently in conversation, notes, and prose.

Merely *reading* `CONTEXT.md` for vocabulary is not this skill; that is a habit every conversation should have. This skill is for when the vocabulary itself changes: a term is coined, sharpened, or found ambiguous.

## CONTEXT.md format

````md
# {Project Name}

{One or two sentences: what this project is.}

## Language

**Order**:
A request from a customer to buy specific items.
_Avoid_: purchase, transaction

**Invoice**:
A request for payment sent after delivery.
_Avoid_: bill, payment request

## Flagged ambiguities

- "backlog" meant both the tool and the work inside it. Resolved: the
  tool is the **Issue tracker**; "backlog" is no longer a domain term.
````

An optional **Relationships** section (how terms relate: "an **Order** holds many **Line items**") is worth adding once terms start referencing each other.

## Rules

- **Terms keep their code- or field-native form** (usually English). **Definitions are written in the working language of the conversation**: Chinese definitions if user and agent talk in Chinese.
- **Be opinionated.** When multiple words exist for one concept, pick the best and list the rest under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. Define what it IS, not what it does.
- **Project-specific terms only.** General programming and writing concepts (timeout, retry, baseline, ablation) don't belong, however often the project uses them.
- **Group terms under subheadings** when natural clusters emerge; otherwise a flat list.
- **A glossary and nothing else.** No implementation details, no specs, no decisions. Decisions and their rationale go to `.writing/findings.md`.

## How this relates to the terminology ledger

Three layers, one job each:

- **`CONTEXT.md` (repo root, this skill).** The project's concept vocabulary across papers and conversations. Survives archiving and context resets.
- **The terminology ledger (`../_shared/core/terminology-ledger.md`).** Per-paper surface-form control for the manuscript: canonical spelling, capitalization, first-use expansion. Scoped to one paper.
- **`.writing/glossary.md` (opt-in).** The define-before-use registry materialized from the ledger. An enforcement mechanism, not this glossary.

Direction of flow: when building the ledger, read `CONTEXT.md` first and reuse its concept names instead of re-deciding them. When a paper names a new load-bearing concept (the system, the contribution) and the user confirms the name, backfill it into `CONTEXT.md` so the next paper and the next conversation inherit it.

## During any design or writing conversation

- **Challenge against the glossary.** When the user's wording conflicts with `CONTEXT.md`, call it out immediately: "The glossary defines *cancellation* as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical term: "You said *account*. The Customer or the User? Those are different things."
- **Stress-test with concrete scenarios.** Invent edge-case scenarios that force precise boundaries between neighboring concepts.
- **Cross-reference with the source.** When the stated model contradicts the manuscript, the notes, or the code, surface the contradiction and resolve which side is right.
- **Update `CONTEXT.md` on the spot.** The moment a term is resolved, write it; don't batch glossary updates for later. Create the file lazily: only when the first term is resolved, not as empty scaffolding.
