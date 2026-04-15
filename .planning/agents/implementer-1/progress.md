# implementer-1 progress

## Task 5: skills/main/SKILL.md — DONE
- Wrote /home/ubuntu/sipeng/superpower-writing/skills/main/SKILL.md (213 LOC)
- Commit: c004700 "feat: main router skill"
- Covers all 9 mandatory body sections from plan.md §Task 5:
  1. Announce on entry
  2. Hard dep gate (check-deps.sh)
  3. Zotero gate (check-zotero.sh, conditional on metadata.yaml zotero.enabled)
  4. .writing/ detection + init-writing-dir.sh
  5. Stage routing table (outlining → writing-plans → drafting → claim-verification → revision → submission)
  6. Planning Approach Routing (4 options via AskUserQuestion)
  7. Execution Routing (3 options delegating to superpower-planning engines)
  8. Stash/Resume Routing (.writing/stash/<paper-name>/)
  9. Skills inventory table (7 local + 7 upstream)
- Style mirrors /home/ubuntu/sipeng/superpower-planning/skills/main/SKILL.md
- Upstream skills called by bare name (no plugin: prefix) per plan requirement
- Claim-first protocol + PreToolUse hook reference included for drafting/claim-verification handoff
