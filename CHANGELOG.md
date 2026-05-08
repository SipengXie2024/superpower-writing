# Changelog

All notable changes to cn-bid-writing are documented here.

## [0.1.0] — 2026-05-08

### Added

- Initial MVP for Chinese bid document writing.
- `.bid/` workspace initialization with metadata, outline, progress, findings, prompt, input, chapter, export, archive, and stash directories.
- Section outline model with parent sections and leaf sections.
- One Markdown file per leaf section under `.bid/chapters/`.
- `check-bid.sh` validation for required files, outline parsing, missing chapters, and minimum character counts.
- `export-docx.sh` aggregation to `.bid/export/combined.md` and optional Pandoc docx output.
- Core commands: `init`, `outline`, `interview`, `draft`, `check`, and `export-docx`.
- Core skills: `main`, `outlining`, `interview`, `drafting`, `verification`, `export-docx`, and Chinese bid-prose `humanizer`.

### Removed

- Old academic-paper workflow components and external research/citation integrations from the active plugin surface.
- Default MCP server configuration.
