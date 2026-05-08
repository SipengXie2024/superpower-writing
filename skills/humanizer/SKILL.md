---
name: humanizer
version: 0.1.0
description: This skill should be used when the user asks to "润色标书", "去 AI 味", "去模板化", "让标书更像人写的", "改掉套话", "中文投标文件润色", or wants to polish Chinese bid prose while keeping a formal delivery tone.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# 中文标书 Humanizer

Polish Chinese bid prose so it reads like careful human-written delivery material, not generated filler. Keep the tone formal, steady, specific, and suitable for review by bid evaluators.

## Use Cases

Use this skill after drafting `.bid/chapters/*.md`, when a paragraph sounds formulaic, promotional, vague, repetitive, or too much like generic AI output.

## Editing Priorities

1. Preserve factual meaning, commitments, section scope, and required terms.
2. Remove empty slogans, broad statements, and inflated adjectives.
3. Replace vague statements with concrete deliverables, mechanisms, boundaries, or outcomes when the source text supports them.
4. Shorten repeated sentence patterns.
5. Keep the register formal. Do not make the text casual, humorous, or conversational.
6. Keep Chinese punctuation and paragraph flow natural.

## Common Problems to Fix

- "全面赋能", "深度融合", "持续优化", "高质量推进" without concrete content.
- Repeated frames such as "通过……，实现……，提升……" in every sentence.
- Overpromising statements such as "确保绝对安全" or "全面领先" without support.
- Long stacked modifiers before the main verb.
- Paragraphs that list benefits but do not say what will actually be delivered.
- Mechanical transitions such as "综上所述", "与此同时", "值得注意的是" when they add no meaning.

## Workflow

1. Read the target text and any relevant `.bid/outline.yaml` section entry.
2. Identify the section's purpose, required points, and minimum character target.
3. Edit only the prose that needs polishing.
4. Keep required headings, IDs, numbers, names, product terms, legal terms, and user-provided wording unless clearly broken.
5. If a claim is unsupported, soften it instead of inventing source support.
6. Return either a direct rewrite or an applied file edit, depending on the user's request.

## Rewrite Style

Prefer:

- concrete nouns and verbs;
- clear subject-verb structure;
- measurable or checkable statements;
- stable commitments like "建立", "形成", "提供", "完成", "支持";
- direct transitions tied to the section logic.

Avoid:

- internet marketing style;
- exaggerated certainty;
- vague policy-slogan stacking;
- unnecessary English abbreviations when a clear Chinese term exists;
- changing numbers, scope, timelines, names, or obligations without source support.

## Output

When editing a file, summarize the main style changes and mention any unsupported statements that were softened. When rewriting inline text, provide only the polished version unless the user asks for a diff.
