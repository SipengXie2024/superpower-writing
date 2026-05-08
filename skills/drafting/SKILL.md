---
name: drafting
description: This skill should be used when the user asks to "写标书正文", "起草技术方案", "写实施方案", "写服务方案", "起草某个章节", "继续写 001", or wants to draft `.bid/chapters/*.md` files for a Chinese bid document.
version: 0.1.0
---

# Bid Drafting

Draft one or more bid sections as Markdown files. Use `.bid/outline.yaml` as the source of truth and keep each leaf section in its mapped file.

## Workflow

1. Read `.bid/outline.yaml`, `.bid/prompts/global.md`, relevant section prompt files, and referenced files under `.bid/inputs/`.
2. Select the requested section ID or a small batch. Avoid drafting a very large bid in one response.
3. Confirm the section has `file`, `must_cover`, `min_chars`, and `target_chars`. If key inputs are missing, ask before writing.
4. Write or continue the mapped Markdown file under `.bid/chapters/`.
5. Keep the style formal, concrete, and suitable for bid delivery.
6. After drafting, run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh` when practical.

## Writing Rules

Cover every item in `must_cover`. Use source priority in this order: user-provided input files, section prompt files, global prompt, then outline requirements. Do not invent qualifications, certifications, timelines, prices, staffing, legal commitments, or compliance promises.

Prefer concrete deliverables, implementation steps, measurable outcomes, and clear responsibility boundaries. Avoid inflated slogans, empty adjectives, unsupported guarantees, and repetitive transitions.

For naturalness, use `cn-bid-writing:humanizer` after drafting when the prose sounds formulaic or AI-generated.

## File Format

Use a single top heading matching the section title only when helpful. The export script adds headings from `outline.yaml`, so avoid duplicating many heading levels unless the section genuinely needs substructure.
