---
name: drafting
description: This skill should be used when the user asks to "写标书正文", "起草技术方案", "写实施方案", "写服务方案", "起草某个章节", "继续写 001", "批量起草全部章节", "/draft all", "并行写多个章节", or wants to draft one or more `.bid/chapters/*.md` files for a Chinese bid document.
version: 0.1.0
---

# Bid Drafting

Draft bid sections as Markdown files. Use `.bid/outline.yaml` as the source of truth and keep each leaf section in its mapped file.

## Parallel Agent Workflow

1. Read `.bid/outline.yaml`, `.bid/prompts/global.md`, relevant section prompt files, and referenced files under `.bid/inputs/`.
2. Select the requested leaf section ID, `all`, or the requested batch. Leaf sections are entries with a `file` field.
3. For every selected leaf section, confirm `file`, `must_cover`, `functional_indicators`, `performance_indicators`, `min_chars`, `target_chars`, and any `docx_template` or `format_requirements`. If key inputs are missing, ask before writing.
4. Dispatch writing with `bid-section-writer` agents in parallel. For multiple sections, send all independent writer Agent calls in one tool message so drafting happens concurrently. If the outline is too large for one wave, split into parallel waves and never draft the wave serially one section at a time.
5. After each writer finishes, dispatch a `bid-section-verifier` agent for that same section before polish. When multiple writer results are ready, dispatch verifier agents in parallel by section. The verifier checks the chapter against `.bid/outline.yaml`, especially `must_cover`, `functional_indicators`, `performance_indicators`, `min_chars`, DOCX format requirements, referenced inputs, and unsupported scope creep.
6. If verification fails, send the verifier findings back to a `bid-section-writer` agent for that section, then re-run `bid-section-verifier`. Do not polish or mark the section complete until verification passes.
7. After verification passes, dispatch a `bid-section-polisher` agent for that same section. When multiple sections pass verification, dispatch polisher agents in parallel by section. The polisher performs humanization while preserving the verified scope and all outline coverage.
8. After all selected sections complete write → verify → polish, run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh` unless the script or dependency setup is unavailable. If skipped, report the reason.

## Writing Rules

Cover every item in `must_cover`, `functional_indicators`, and `performance_indicators`. Treat functional and performance indicators as hard requirements, not optional examples. Use source priority in this order: user-provided input files, section prompt files, global prompt, then outline requirements. Do not invent qualifications, certifications, timelines, prices, staffing, legal commitments, or compliance promises.

Prefer concrete deliverables, implementation steps, measurable outcomes, and clear responsibility boundaries. Avoid inflated slogans, empty adjectives, unsupported guarantees, and repetitive transitions.

Use `bid-section-polisher` for mandatory post-verification humanization. Use `cn-bid-writing:humanizer` only for ad-hoc prose outside the parallel drafting workflow.

## Agent Responsibilities

- `bid-section-writer`: write or revise one assigned leaf section, including all required functional and performance indicators.
- `bid-section-verifier`: review one written section against `.bid/outline.yaml` and return PASS or concrete issues. It checks indicators and DOCX-related figure/table requirements, and does not edit files.
- `bid-section-polisher`: humanize one verified section without adding new facts, weakening performance claims, or removing outline coverage.

## File Format

Use a single top heading matching the section title only when helpful. The export script adds headings from `outline.yaml`, so avoid duplicating many heading levels unless the section genuinely needs substructure.
