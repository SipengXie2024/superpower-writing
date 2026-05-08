---
name: main
description: This skill should be used when the user starts, resumes, checks, drafts, polishes, or exports a Chinese bid, tender response, 投标文件, 响应文件, 技术标, or 商务标 with cn-bid-writing, including requests such as "写标书", "做投标文件", "初始化标书", "生成标书大纲", "逐章节写标书", "导出 Word", "导出 docx", or mentions a `.bid/` workspace.
version: 0.1.0
---

# cn-bid-writing Router

Route Chinese bid-document work through the `.bid/` workspace. Keep the process section-based and persistent because large bids can exceed a single conversation.

## Entry Protocol

Briefly say that the task will use the persistent `.bid/` workflow.

Then inspect the project root:

1. If `.bid/` is absent and the user is starting bid work, run `${CLAUDE_PLUGIN_ROOT}/scripts/init-bid-dir.sh`.
2. If `.bid/` exists, read `.bid/progress.md`, `.bid/findings.md`, `.bid/metadata.yaml`, and `.bid/outline.yaml` when present.
3. Route by intent and current artifacts.

## Routing

| User intent | Next skill or script |
|-------------|----------------------|
| Start a new bid workspace | Run `scripts/init-bid-dir.sh` |
| Build or revise the section tree | `cn-bid-writing:outlining` |
| Decide what each small section should contain | `cn-bid-writing:interview` |
| Draft one section or all planned sections | `cn-bid-writing:drafting` |
| Check structure, mappings, and minimum character counts | `cn-bid-writing:verification` |
| Export to combined Markdown or docx | `cn-bid-writing:export-docx` |
| Polish bid prose to remove AI-sounding writing | `cn-bid-writing:humanizer` |

## Workspace Rules

Use `.bid/outline.yaml` as the machine-readable source of truth. Use `.bid/outline.md` for human-readable planning notes. Store each leaf section in one Markdown file under `.bid/chapters/`.

Avoid writing a full large bid in one pass. Work in batches by section IDs. Preserve external prompts under `.bid/prompts/` and source materials under `.bid/inputs/` so later sessions can reproduce decisions.

## Completion Rule

Before reporting a bid package ready, run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh`. Before reporting a docx ready, run `${CLAUDE_PLUGIN_ROOT}/scripts/export-docx.sh` and verify whether Pandoc actually produced the docx file.
