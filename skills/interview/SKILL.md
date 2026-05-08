---
name: interview
description: This skill should be used when the user asks to "逐章节确认标书内容", "采访我写标书", "确定每个小节写什么", "设置每节最低字数", or wants to refine `.bid/outline.yaml` section requirements through dialogue.
version: 0.1.0
---

# Bid Section Interview

Turn a broad outline into section-level writing instructions. Capture concrete requirements so drafting can happen later without re-asking the same questions.

## Workflow

1. Read `.bid/outline.yaml`, `.bid/outline.md`, `.bid/findings.md`, and `.bid/prompts/global.md`.
2. Pick a small batch of sections. Prefer 3 to 8 leaf sections per interview round.
3. Ask one clear question at a time when requirements are missing.
4. For each leaf section, record:
   - what the section must say;
   - minimum and target character counts;
   - source files under `.bid/inputs/`;
   - prompt files under `.bid/prompts/`;
   - open questions.
5. Update `.bid/outline.yaml` and `.bid/findings.md` after decisions are made.

## Interview Prompts

Ask for concrete content, not vague preferences. Examples:

- "这一节面向评标专家最需要证明什么？"
- "这一节至少需要覆盖哪些业务、技术或实施要点？"
- "这节的最低字数和目标字数分别是多少？"
- "有哪些外部材料应该作为输入？"
- "有没有不能写、必须弱化或必须强调的表述？"

## Status Updates

Set section status to `planned` when enough information exists to draft. Use `needs_input` when a source file, figure, policy text, or user decision is missing.
