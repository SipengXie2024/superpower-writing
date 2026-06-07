---
name: writing-clearly-and-concisely
description: Apply Strunk's timeless writing rules to ANY prose humans will read—documentation, commit messages, error messages, explanations, reports, or UI text. Makes your writing clearer, stronger, and more professional.
---

# Writing Clearly and Concisely

## Output Discipline (read first)

Return **only the revised text** — nothing before it, nothing after it — unless the user explicitly asked for an explanation. Everything in this skill (register numbers, rule numbers, the process, this file's existence) is internal reasoning the user must never see.

Ban every form of machinery leak, not just the one shown below: no register line ("Register 5", "register 1"), no rule citations ("per rule 11", "I apply all rules"), no prompt/meta references ("This is prompt 1"), no "I classified this as…", no preamble, no trailing notes, no diff.

A leak in fluent prose is just as forbidden as a label. A sentence that *narrates the classification* ("This is academic register, so I preserve the hedges…") is the same violation — strip it and open with the first word of the revised text.

Wrong (labeled form):
> *Register: technical (rule 13 applied).* The service caches responses.

Wrong (narrated form):
> This is a default-register README (register 5), so I apply every rule. The service caches responses.

Right:
> The service caches responses.

Exception — assumptions: if you made a genuine editorial assumption the user should verify (e.g. read a `not…un-` as a literal double negative vs. emphasis), append one short bracketed line at the very end, e.g. `[Assumed X means Y; revise if not.]`. This is the only permitted addition.

Never translate, transliterate, or "fix" non-English tokens — treat any foreign-language word as a verbatim, non-editable term (register 4).

## Overview

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write clearly and cut ruthlessly.

**WARNING:** `elements-of-style.md` consumes ~12,000 tokens. Read it only when writing or editing prose.

## When to Use This Skill

Use this skill whenever you write prose for humans:

- Documentation, README files, technical explanations
- Commit messages, pull request descriptions
- Error messages, UI copy, help text, comments
- Reports, summaries, or any explanation
- Editing to improve clarity

**If you're writing sentences for a human to read, use this skill.**

## Register Awareness — Apply Strunk Lightly Here

Classify the input before editing. Strunk's rules misfire on some registers.

1. **Academic / scholarly** — preserve scholarly verbs (`shows`, `reports`, `demonstrates`, `preserves`), academic plural `we`, epistemic hedges, and domain compound modifiers (`per-contract dispatch identity`, `cold-cache compile time`).
2. **Technical / code-adjacent** — preserve technical terms verbatim. Domain hyphenated compounds are not "needless words".
3. **Direct quotes, citations, bibliography** — leave verbatim; edit framing only.
4. **Code, paths, commands, signatures** — never edit.
5. **Default (blog, README, marketing, commit body)** — apply all rules.

When in doubt, default to register 5 and note the assumption.

In registers 1–2, lean on rule 10 (active voice), 13 (cut filler like "in order to"), 16, 18. Apply rule 11 (positive form), 12 (concrete), and the maximalist reading of 13 with caution: hedges, citations, named entities, and numbers are load-bearing, not needless.

## Process

1. **Classify the register** (1–5 above).
2. **Identify load-bearing content**: hedges, citations, named entities, numbers, technical compounds, scholarly verbs, foreign-language tokens. These survive every cut, verbatim.
3. **Apply Strunk's rules.** Defaults: prefer active voice (rule 10), cut filler ("in order to", "the fact that") per rule 13, keep related words together (rule 16), place emphatic words at end (rule 18). In registers 1–2 restrain rules 11/12 and the maximalist reading of rule 13.
4. **Verify**: every load-bearing item from step 2 must still appear in the output. If a hedge, citation, named entity, or number was lost, restore it.
5. **Return only the revised text** (per Output Discipline). The sole permitted addition is a single bracketed assumption line at the end when you resolved a genuine ambiguity.

When context is tight, dispatch a subagent with `elements-of-style.md` for the full ruleset.

## All Rules

The full 18 rules + the alphabetical "Words and Expressions Commonly Misused" section live in `elements-of-style.md`. The high-leverage rules referenced above:
10 active voice · 11 positive form · 12 concrete language · 13 omit needless words · 16 related words together · 18 emphatic words at end.

## Common cuts

- "In order to" → "To" (or drop)
- "It is important to note that" → drop
- "The fact that X" → "X"
- "is being Xed" → "X-es" (active voice)
