# cn-bid-writing

Claude Code plugin for Chinese bid document writing. This file captures repo-specific guidance for sessions editing the plugin itself.

## Dev location

Edit in this repository root. This branch is intentionally being reshaped into the standalone `cn-bid-writing` plugin.

## Branch mapping

Local `master` tracks `origin/main`; there is no local `main`. Do not rename or retrack without asking. Work for the first cn-bid-writing MVP happens on `feature/cn-bid-writing`.

## Layout

| Path | Purpose |
|------|---------|
| `.claude-plugin/plugin.json` | plugin manifest |
| `commands/` | slash commands exposed by the plugin |
| `skills/` | bid-writing skills |
| `hooks/` | lightweight session dependency notices |
| `scripts/` | deterministic helpers for init/check/export |
| `templates/` | `.bid/` workspace templates |
| `tests/` | smoke tests |

## Core workflow

The plugin persists user project state in `.bid/`. Each leaf section in `outline.yaml` maps to one Markdown file under `.bid/chapters/`. Export builds `.bid/export/combined.md` and, when Pandoc is installed, a docx file.

## Verification

Before reporting the plugin ready, run:

```bash
bash tests/smoke.sh
```

The smoke test covers workspace initialization, missing chapter detection, minimum character checks, multi-level parent/leaf outline handling, combined Markdown generation, docx generation when Pandoc is available, component presence, absence of default MCP servers, and old product-surface terminology cleanup.

## Dependencies

Runtime checks use Python with PyYAML. DOCX export requires Pandoc. The SessionStart hook reports missing dependencies without blocking unrelated work.
