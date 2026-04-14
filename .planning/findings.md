# Findings & Decisions — superpower-writing

## Requirements
- Orchestrate academic writing (IMRAD research papers) with the same rigor superpower-planning brings to code.
- Depend on scientific-agent-skills for domain content; zero vendoring.
- Enforce claim/evidence traceability to prevent citation hallucination.
- Persistent session-survivable state at `.writing/`.

## Research Findings
- **scientific-agent-skills (K-Dense-AI)** is an Agent Skills standard collection, NOT a Claude Code plugin. Install via `npx skills add K-Dense-AI/scientific-agent-skills`; distributed under agentskills.io open standard; works with Cursor, Claude Code, Codex, Gemini CLI.
- Skills install as top-level entries (no plugin prefix). They will appear as bare names (`scientific-writing`, `literature-review`, `peer-review`, `citation-management`, `research-lookup`, `scientific-schematics`, `pyzotero`, ...), not as `scientific-agent-skills:scientific-writing`.
- 133 skills shipped; subset needed by superpower-writing: `scientific-writing`, `literature-review`, `peer-review`, `citation-management`, `research-lookup`, `scientific-schematics` (mandatory graphical abstract per scientific-writing SKILL.md), `scientific-critical-thinking`, `scientific-brainstorming` (optional).
- Skill runtime dependency: `uv` must be installed (scientific skills use `uv pip install` for Python deps).
- `claude plugin` CLI does exist and supports marketplace management, but it is NOT how scientific-agent-skills installs — do not hardwire that path.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| New plugin `superpower-writing`, orchestration only | Content skills already exist upstream; scope stays focused on process glue |
| 7 core skills: main, outlining, writing-plans, drafting, claim-verification, revision, submission | Compact mapping from SP; utility skills (stashing, worktrees, parallel-agents) fold into main/drafting |
| Dependency check = SessionStart hook + main skill double-check | Hook catches early; main catches when hook is disabled |
| Install command: `npx skills add K-Dense-AI/scientific-agent-skills` | Confirmed from upstream README §Getting Started |
| Detection target = skill files on disk (e.g., `~/.claude/skills/scientific-writing/SKILL.md`) | Agent Skills standard installs to filesystem; plugin marketplace check would miss entirely |
| Hard-fail on missing deps | User confirmed: refuse to run, surface install command, don't degrade silently |
| Claim-first enforcement = PreToolUse hook | User chose strict mode; hook blocks Edit/Write on `manuscript/*.md` unless corresponding claim has `STATUS: evidence_ready` |
| Claim↔manuscript mapping = filename correspondence + HTML-comment tags | `manuscript/02_methods.md` ↔ `claims/section_02_methods.md`; `<!-- claim: id -->` binds paragraph to claim; `<!-- draft-only -->` escape hatch for early exploration, flagged at verification |
| Multi-author v1 = single-author only | YAGNI; multi-author git model deferred to v2 |
| Scientific-integrity state = `.writing/metadata.yaml` | Single YAML captures authors+COI+preregistration+data/code availability+reporting guideline; outlining fills it, submission verifies presence |
| Citation verification = strict (DOI resolve + semantic match) | User chose rigorous mode; calls `research-lookup`/`citation-management` for per-citation abstract check against claim |
| Zotero integration = deferred to v2 (manual refs in v1) | User manages refs manually; keeps scope small |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Initial assumption: scientific-agent-skills is a Claude plugin | Corrected after reading upstream README; use `npx skills add` and filesystem detection |
| Cross-plugin Skill invocation viability unclear | Moot once we realized upstream ships as bare skills, not a plugin — addressable directly by name |

## Resources
- Upstream README: `/home/ubuntu/sipeng/scientific-agent-skills/README.md`
- Agent Skills standard: https://agentskills.io/
- Key upstream SKILL.md files inspected: scientific-writing, scientific-brainstorming, scientific-critical-thinking, literature-review, peer-review

## Debugging Findings
<!-- Added by debugging skill -->

## Code Review Findings
<!-- Added by requesting-review skill -->
