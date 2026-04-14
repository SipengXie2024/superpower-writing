# superpower-writing Implementation Plan

> **For Claude:** Execute this plan using the skill chosen during Execution Handoff (see end of plan).
> Planning dir: `.planning/`

**Goal:** Scaffold a Claude Code plugin `superpower-writing` that ports the superpower-planning lifecycle to IMRAD academic writing, with hard dependency on the upstream scientific-agent-skills Agent Skills collection and hard enforcement of a claim-first writing protocol via hooks.

**Architecture:** Seven skills (main, outlining, writing-plans, drafting, claim-verification, revision, submission) + two hooks (SessionStart dep check, PreToolUse claim enforcement) + shared scripts for `.writing/` init and dep detection. Skills call upstream scientific-agent-skills via the Skill tool by bare name. Persistent state lives in `.writing/` mirroring superpower-planning's `.planning/` pattern.

**Tech Stack:** Claude Code plugin spec (`.claude-plugin/plugin.json`), bash scripts, optional Python helpers for claim parsing, YAML for metadata, standard Markdown SKILL.md frontmatter.

**Repo layout (locked):**
```
superpower-writing/
  .claude-plugin/
    plugin.json
    marketplace.json         # for local dev/install via `claude plugin marketplace add`
  README.md
  hooks/
    hooks.json
    check-deps.sh            # SessionStart
    enforce-claims.sh        # PreToolUse wrapper
    enforce-claims.py        # parser logic
  scripts/
    init-writing-dir.sh
    check-deps.sh            # shared with hook; single source of truth
  commands/
    outline.md
    draft.md
    revise.md
    submit.md
    check-deps.md
    stash.md
    archive.md
  skills/
    main/SKILL.md
    outlining/SKILL.md
    writing-plans/SKILL.md
    drafting/SKILL.md
    claim-verification/SKILL.md
    revision/SKILL.md
    submission/SKILL.md
    planning-foundation/
      templates/
        progress.md
        findings.md
        metadata.yaml
  tests/
    smoke.sh                 # end-to-end check
```

---

## Evidence Gap Summary

| # | Decision | Evidence Needed | Timing | Task |
|---|----------|----------------|--------|------|
| 1 | PreToolUse hook intercepts Edit/Write/MultiEdit/NotebookEdit reliably | Local smoke test running all tool variants against `manuscript/*.md` | During impl | Task 4 |
| 2 | Claim-first actually slows drafting less than the quality gain | Pilot on one short paper after MVP | After MVP | (deferred; note in README) |
| 3 | research-lookup semantic citation match has acceptable FP/FN | Test set of 20 known-good and 5 fabricated citations | After MVP | (deferred; note in claim-verification SKILL.md) |
| 4 | Agent Skills install path varies by OS | Probe all candidate paths; log what's found | During impl | Task 3 |

---

## Tasks

### Task 0: Scaffold plugin manifest and directory tree (serial, blocks everything)

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `README.md`
- Create (empty dirs, tracked via `.gitkeep`): `hooks/`, `scripts/`, `commands/`, `skills/`, `tests/`

- [ ] **Step 1: Write `.claude-plugin/plugin.json`**

```json
{
  "name": "superpower-writing",
  "description": "IMRAD academic-writing lifecycle plugin. Brings persistent state, stage gates, claim-first verification, subagent execution, and review loops to research-paper drafting. Depends on scientific-agent-skills (agentskills.io) for domain content.",
  "version": "0.1.0",
  "author": { "name": "sipeng" },
  "repository": "https://github.com/SipengXie2024/superpower-writing",
  "license": "MIT",
  "keywords": ["skills", "academic-writing", "imrad", "claim-first", "scientific-agent-skills"]
}
```

- [ ] **Step 2: Write `.claude-plugin/marketplace.json`** (mirrors SP's pattern)

```json
{
  "name": "superpower-writing",
  "description": "Local marketplace for superpower-writing IMRAD academic-writing plugin",
  "owner": { "name": "sipeng" },
  "plugins": [
    {
      "name": "superpower-writing",
      "description": "IMRAD academic-writing lifecycle plugin",
      "version": "0.1.0",
      "source": "./"
    }
  ]
}
```

- [ ] **Step 3: Write `README.md`**

Must include: one-paragraph pitch, install instructions (`claude plugin marketplace add ./` + `claude plugin install superpower-writing`), upstream dependency note (`npx skills add K-Dense-AI/scientific-agent-skills`), skill inventory table (copy from design.md §5), link to `.planning/design.md` for architecture, "YAGNI v1 scope" section (copy from design.md §12).

- [ ] **Step 4: Create empty dirs with `.gitkeep`**

```bash
cd /home/ubuntu/sipeng/superpower-writing
for d in hooks scripts commands skills tests skills/planning-foundation/templates; do mkdir -p "$d" && touch "$d/.gitkeep"; done
```

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/ README.md hooks/.gitkeep scripts/.gitkeep commands/.gitkeep skills/.gitkeep tests/.gitkeep skills/planning-foundation/templates/.gitkeep
git commit -m "chore: scaffold plugin manifest and directory tree"
```

> Log to `.planning/findings.md`: note any divergence from SP's `.claude-plugin/` layout.

---

### Task 1: `scripts/init-writing-dir.sh` — initialize `.writing/`

**Files:**
- Create: `scripts/init-writing-dir.sh`
- Create: `skills/planning-foundation/templates/progress.md`
- Create: `skills/planning-foundation/templates/findings.md`
- Create: `skills/planning-foundation/templates/metadata.yaml`

- [ ] **Step 1: Write template `progress.md`**

Content identical in structure to superpower-planning's `skills/planning-foundation/templates/progress.md` but adapted vocabulary: tasks → sections/figures, phases → outlining/drafting/revision/submission. Include: Task Status Dashboard (columns: Section, Status, Claim Verification, Citation Check, Reviewer Cycle, Key Outcome), Session log, Verification Evidence, 5-Question Reboot Check.

- [ ] **Step 2: Write template `findings.md`**

Sections: Requirements / Research Findings / Decisions / Issues / Resources / Reviewer Context / Debugging Findings / Code Review Findings.

- [ ] **Step 3: Write template `metadata.yaml`** (exact content from design.md §10)

```yaml
authors: []
preregistration:
  registry: TODO
  url: TODO
  deviations: []
data_availability:
  statement: TODO
  access: TODO  # open | restricted | on-request | none
code_availability:
  url: TODO
  license: TODO
reporting_guideline: TODO  # CONSORT | STROBE | PRISMA | none
```

- [ ] **Step 4: Write `scripts/init-writing-dir.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-.writing}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
TEMPLATE_DIR="$PLUGIN_ROOT/skills/planning-foundation/templates"

if [[ -d "$TARGET" ]]; then
  echo "$TARGET already exists; refusing to overwrite." >&2
  exit 1
fi

mkdir -p "$TARGET"/{manuscript,claims,figures,reviews,archive}
cp "$TEMPLATE_DIR/progress.md" "$TARGET/progress.md"
cp "$TEMPLATE_DIR/findings.md" "$TARGET/findings.md"
cp "$TEMPLATE_DIR/metadata.yaml" "$TARGET/metadata.yaml"
: > "$TARGET/outline.md"

echo "Initialized $TARGET/"
echo "  progress.md, findings.md, metadata.yaml, outline.md"
echo "  subdirs: manuscript/, claims/, figures/, reviews/, archive/"
```

- [ ] **Step 5: Make executable and smoke-test**

```bash
chmod +x scripts/init-writing-dir.sh
(cd /tmp && rm -rf sw-smoke && mkdir sw-smoke && cd sw-smoke && CLAUDE_PLUGIN_ROOT=/home/ubuntu/sipeng/superpower-writing bash /home/ubuntu/sipeng/superpower-writing/scripts/init-writing-dir.sh)
ls /tmp/sw-smoke/.writing/
```
Expected output: `archive claims figures findings.md manuscript metadata.yaml outline.md progress.md reviews`

- [ ] **Step 6: Commit**

```bash
git add scripts/init-writing-dir.sh skills/planning-foundation/templates/
git commit -m "feat: init-writing-dir.sh and templates"
```

---

### Task 2: `scripts/check-deps.sh` — detect scientific-agent-skills

**Files:**
- Create: `scripts/check-deps.sh`

- [ ] **Step 1: Write the script**

Required skill names (bare, per Agent Skills standard): `scientific-writing`, `literature-review`, `peer-review`, `citation-management`, `research-lookup`, `scientific-schematics`.

```bash
#!/usr/bin/env bash
set -euo pipefail

REQUIRED=(scientific-writing literature-review peer-review citation-management research-lookup scientific-schematics)

CANDIDATE_ROOTS=(
  "$HOME/.claude/skills"
  "$HOME/.claude/plugins/cache"
  "$HOME/.cursor/skills"
  "$HOME/.config/claude-code/skills"
  "$HOME/Library/Application Support/Claude/skills"
)

found_root=""
missing=()
for skill in "${REQUIRED[@]}"; do
  hit=""
  for root in "${CANDIDATE_ROOTS[@]}"; do
    [[ -d "$root" ]] || continue
    if find "$root" -maxdepth 4 -type f -path "*/$skill/SKILL.md" -print -quit 2>/dev/null | grep -q .; then
      hit="$root"
      [[ -z "$found_root" ]] && found_root="$root"
      break
    fi
  done
  [[ -z "$hit" ]] && missing+=("$skill")
done

if (( ${#missing[@]} > 0 )); then
  cat >&2 <<EOF
[superpower-writing] Missing required upstream skills: ${missing[*]}

Install scientific-agent-skills (K-Dense-AI) with:

    npx skills add K-Dense-AI/scientific-agent-skills

If 'uv' is not installed (required by upstream):

    curl -LsSf https://astral.sh/uv/install.sh | sh

Searched roots: ${CANDIDATE_ROOTS[*]}
EOF
  exit 1
fi

echo "[superpower-writing] deps OK (found at: $found_root)"
exit 0
```

- [ ] **Step 2: Make executable and run locally**

```bash
chmod +x scripts/check-deps.sh
./scripts/check-deps.sh || echo "(exit non-zero is expected if upstream not installed)"
```

- [ ] **Step 3: Commit**

```bash
git add scripts/check-deps.sh
git commit -m "feat: check-deps.sh detects scientific-agent-skills"
```

> Log to `.planning/findings.md`: which candidate root actually contained the skills on this machine.

---

### Task 3: `hooks/check-deps.sh` wrapper + SessionStart wiring

**Files:**
- Create: `hooks/check-deps.sh`
- Create: `hooks/hooks.json`

Depends on: Task 2.

- [ ] **Step 1: Write thin wrapper `hooks/check-deps.sh`**

```bash
#!/usr/bin/env bash
# SessionStart hook. Injects a system-reminder describing dep status.
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT="$("$PLUGIN_ROOT/scripts/check-deps.sh" 2>&1)"
STATUS=$?

if [[ $STATUS -ne 0 ]]; then
  cat <<EOF
<system-reminder>
superpower-writing dependency check FAILED:

$OUTPUT

Do not invoke any superpower-writing skill until deps are installed.
</system-reminder>
EOF
else
  cat <<EOF
<system-reminder>
superpower-writing deps OK. Scientific-agent-skills found.
</system-reminder>
EOF
fi
exit 0  # never block session start; reminder-only
```

- [ ] **Step 2: Write `hooks/hooks.json`**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/check-deps.sh" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh" }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: chmod + commit**

```bash
chmod +x hooks/check-deps.sh
git add hooks/check-deps.sh hooks/hooks.json
git commit -m "feat: SessionStart dep check hook"
```

---

### Task 4: `hooks/enforce-claims.{sh,py}` — PreToolUse claim enforcement

**Files:**
- Create: `hooks/enforce-claims.sh`
- Create: `hooks/enforce-claims.py`

Depends on: Task 0, 3 (hooks.json wiring). Parallel-safe with Tasks 1, 2, 5-13.

- [ ] **Step 1: Write `hooks/enforce-claims.py`**

Behavior:
1. Read JSON input from stdin (Claude Code PreToolUse contract: `{tool_name, tool_input: {file_path, content|new_string|edits}}`).
2. Exit 0 (allow) unless `tool_name` ∈ {Edit, Write, MultiEdit, NotebookEdit} AND `file_path` matches `**/manuscript/*.md`.
3. Resolve sibling claim file: `$(dirname $(dirname file_path))/claims/section_<same-basename>.md` — e.g. `.writing/manuscript/02_methods.md` → `.writing/claims/section_02_methods.md`.
4. Extract full post-edit content (for Write: `content`; for Edit: apply `new_string` to the existing file; for MultiEdit: apply each edit). Tolerate preview-only calls.
5. Regex-find all `<!-- claim: (\S+) -->` tags in new content. Also collect `<!-- draft-only -->` markers.
6. For each claim id, parse the YAML claim file (PyYAML) and check `STATUS` ∈ {`evidence_ready`, `verified`}.
7. If any claim is missing or has STATUS=`stub`, emit JSON to stdout:
```json
{"decision": "block", "reason": "[superpower-writing] claim '<id>' has STATUS=stub; resolve EVIDENCE before writing prose."}
```
and exit 2. Otherwise exit 0.
8. If claim file does not exist at all AND the content contains claim tags, block with `reason: "claim file <path> missing"`.
9. If NO claim tags AND NO draft-only tags AND the file is in a protected section (configurable, default: all except `00_abstract.md`), block with `reason: "every load-bearing paragraph in <file> must be tagged <!-- claim: id --> or <!-- draft-only -->"`.

Include at top:
```python
#!/usr/bin/env python3
"""PreToolUse hook enforcing claim-first writing protocol.
Reads Claude Code PreToolUse JSON on stdin, writes decision JSON on stdout."""
import json, sys, re, os
from pathlib import Path
try:
    import yaml
except ImportError:
    print(json.dumps({"decision": "block", "reason": "superpower-writing requires PyYAML: pip install pyyaml"}))
    sys.exit(2)
```

Write the full function bodies — no stubs. Keep the file under 200 LOC.

- [ ] **Step 2: Write `hooks/enforce-claims.sh` (thin wrapper to invoke python)**

```bash
#!/usr/bin/env bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
exec python3 "$PLUGIN_ROOT/hooks/enforce-claims.py"
```

- [ ] **Step 3: Smoke test against 4 synthetic cases**

```bash
chmod +x hooks/enforce-claims.sh hooks/enforce-claims.py
mkdir -p /tmp/sw-enf/.writing/{manuscript,claims}
cat >/tmp/sw-enf/.writing/claims/section_02_methods.md <<'EOF'
- id: meth-c1
  CLAIM: Cohort of 1247 T2D patients
  EVIDENCE: [NHANES-2018]
  STATUS: stub
EOF

# Case 1: Write with stub-status claim tag -> BLOCK
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sw-enf/.writing/manuscript/02_methods.md","content":"<!-- claim: meth-c1 -->\nprose"}}' | CLAUDE_PLUGIN_ROOT=/home/ubuntu/sipeng/superpower-writing bash hooks/enforce-claims.sh
# expect exit 2, decision=block

# Case 2: same but STATUS=evidence_ready -> ALLOW
sed -i 's/STATUS: stub/STATUS: evidence_ready/' /tmp/sw-enf/.writing/claims/section_02_methods.md
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sw-enf/.writing/manuscript/02_methods.md","content":"<!-- claim: meth-c1 -->\nprose"}}' | CLAUDE_PLUGIN_ROOT=/home/ubuntu/sipeng/superpower-writing bash hooks/enforce-claims.sh
# expect exit 0

# Case 3: draft-only marker -> ALLOW
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sw-enf/.writing/manuscript/02_methods.md","content":"<!-- draft-only -->\nrough notes"}}' | CLAUDE_PLUGIN_ROOT=/home/ubuntu/sipeng/superpower-writing bash hooks/enforce-claims.sh
# expect exit 0

# Case 4: untagged prose in protected section -> BLOCK
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sw-enf/.writing/manuscript/02_methods.md","content":"unmarked prose"}}' | CLAUDE_PLUGIN_ROOT=/home/ubuntu/sipeng/superpower-writing bash hooks/enforce-claims.sh
# expect exit 2
```

All four must produce the expected outcome. If not, fix the python logic.

- [ ] **Step 4: Commit**

```bash
git add hooks/enforce-claims.sh hooks/enforce-claims.py
git commit -m "feat: PreToolUse claim enforcement hook"
```

> Log to `.planning/findings.md`: results of the 4 smoke cases, plus any edge cases discovered (e.g., MultiEdit semantics).

---

### Tasks 5–11: Write the seven SKILL.md files (all parallel)

Each skill follows the same shape: YAML frontmatter (`name`, `description`) + body structured with Overview / When to Use / Checklist / Process / Key Principles sections, mirroring superpower-planning's patterns. Skills invoke upstream via the Skill tool by bare name (`Skill(skill="scientific-writing")` etc.) — no `plugin:` prefix because scientific-agent-skills is an Agent Skills collection, not a Claude plugin.

**Shared requirement for all seven tasks:** the `description` in frontmatter must be specific enough to trigger reliably. Use second-person present voice ("Use when ..."). Keep each SKILL.md under 700 LOC (CLAUDE.md rule).

#### Task 5: `skills/main/SKILL.md`

**Files:** Create `skills/main/SKILL.md`

**Frontmatter:**
```yaml
---
name: main
description: Router and dependency gate for superpower-writing. Loaded at session start. Verifies scientific-agent-skills is installed, routes between outlining/writing-plans/drafting/claim-verification/revision/submission based on stage in .writing/progress.md. Use when the user starts an academic-writing task (paper, manuscript, IMRAD draft, rebuttal).
---
```

**Body sections (mandatory):**
1. Announce: `"I'm using the superpower-writing main skill to route this task."`
2. Dep check: run `${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh`. On non-zero, refuse all further writing skills and surface install command. This is a **hard gate**, not advisory.
3. `.writing/` detection: if absent AND task looks writing-related, run `${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh`.
4. Routing table (mirror SP main.md): Stage in progress.md → skill to invoke next (outlining → writing-plans → drafting → revision → submission).
5. Planning Approach Routing: mirror SP's four-option AskUserQuestion (Quick Plan / Lightweight / Structured Brainstorming / Stash), adapted to writing vocabulary.
6. Execution Routing: 3 options (Subagent-Driven serial, Team-Driven parallel, Parallel Session) — same as SP but invoking superpower-planning skills since those are still the execution engines; this plugin only provides writing-specific content skills.
7. Stash / Resume Routing: `.writing/stash/<paper-name>/`.
8. Skills inventory table (all 7).

- [ ] Write file, verify ≤ 700 LOC, commit `git add skills/main/SKILL.md && git commit -m "feat: main router skill"`.

#### Task 6: `skills/outlining/SKILL.md`

**Frontmatter:**
```yaml
---
name: outlining
description: Converts a research idea into a complete IMRAD outline plus per-section claim list. Combines design-exploration and spec-writing into one chain. Output is .writing/outline.md (structure + key claims), populated claims/section_*.md files, and .writing/metadata.yaml filled. Use when starting a new paper or when outline is missing.
---
```

**Body sections:**
- Iterative retrieval from literature via upstream `literature-review` + `research-lookup`.
- Produce `outline.md`: I / M / R / A / D sections, each with 3-7 bullet key claims.
- For every bullet produce an entry in `claims/section_<NN>_<slug>.md` matching the design.md §6.1 YAML format, initial STATUS=stub.
- Fill `.writing/metadata.yaml` — block progression if any field left TODO (except YAGNI ones).
- Spec self-review: placeholder scan, I↔D narrative consistency, scope check.
- Hand off to writing-plans skill.

- [ ] Write, commit.

#### Task 7: `skills/writing-plans/SKILL.md`

**Frontmatter:**
```yaml
---
name: writing-plans
description: Decomposes an approved outline into executable per-section/per-figure/per-table tasks with dependency graph. Output is .writing/plan.md. Use after outlining produces .writing/outline.md and before drafting begins.
---
```

**Body sections:**
- Read `outline.md`, `metadata.yaml`, `claims/*.md`.
- Produce `.writing/plan.md` with: per-section tasks (draft, verify-claims, internal-review), figure tasks (route to `scientific-schematics`), table tasks, and a dependency table (Methods blocks Results; Intro ≥ shadow of Discussion).
- Parallelism groups analysis.
- Self-review, hand off to drafting.

- [ ] Write, commit.

#### Task 8: `skills/drafting/SKILL.md`

**Frontmatter:**
```yaml
---
name: drafting
description: Orchestrates prose drafting section-by-section, in serial (subagent + 2-stage review) or parallel (Agent Team) mode. Each section subagent must resolve claim EVIDENCE via research-lookup before writing prose (claim-first protocol; PreToolUse hook enforces this). Use after writing-plans produces .writing/plan.md.
---
```

**Body sections:**
- Mode selection via AskUserQuestion: serial vs parallel vs session-handoff.
- Per-section subagent prompt template includes: load claims file, resolve each EVIDENCE via `research-lookup`/`literature-review`/`citation-management`, only then write `<!-- claim: id -->`-tagged paragraphs. Remind the agent the PreToolUse hook will block writes to prose with stub-STATUS claims.
- Delegate graphical abstract to `scientific-schematics` (upstream mandates one graphical abstract + ≥1 schematic).
- After each section completes, update `progress.md`.

- [ ] Write, commit.

#### Task 9: `skills/claim-verification/SKILL.md`

**Frontmatter:**
```yaml
---
name: claim-verification
description: Pre-submission verifier. Walks every <!-- claim: id --> in manuscript/*.md, confirms DOI resolution via citation-management, runs semantic match against research-lookup abstracts, checks numeric/table consistency, fails if any [NEEDS-EVIDENCE] or draft-only markers remain. Use at submission gate or on demand.
---
```

**Body sections:** exact three-pass check from design.md §6.4, plus fourth pass (reporting-guideline checklist via upstream `peer-review`). Emit `.writing/verify-report.md` with per-claim PASS/FAIL; cache DOI/abstract results in `.writing/verify-cache.json` keyed by DOI.

- [ ] Write, commit.

#### Task 10: `skills/revision/SKILL.md`

**Frontmatter:**
```yaml
---
name: revision
description: Unified review-loop handler for internal co-author review and external journal reviewer comments. Intake -> classify (Major/Minor/OutOfScope/Factually-wrong) -> per-item response draft -> apply diff -> re-run claim-verification. Use when review comments are received.
---
```

**Body sections:** 5-step pipeline from design.md §9. Per-review file at `.writing/reviews/<id>.md`. Template for reviewer response letter.

- [ ] Write, commit.

#### Task 11: `skills/submission/SKILL.md`

**Frontmatter:**
```yaml
---
name: submission
description: Final gate before journal submission. Verifies claim-verification PASS, metadata.yaml complete, graphical abstract present, no draft-only tags remain, no [NEEDS-EVIDENCE] unresolved, then freezes a copy to .writing/archive/<date>/. Use when the user declares the paper ready to submit.
---
```

**Body sections:** freeze checklist, archive procedure, post-archive reset that keeps `metadata.yaml` + `outline.md` but resets `progress.md` for the next revision round.

- [ ] Write, commit.

---

### Tasks 12–18: Slash commands (all parallel)

Each command is a Markdown file with YAML frontmatter (`description:`, optional `argument-hint:`) and a one-liner invoking the corresponding skill via the Skill tool.

#### Task 12: `commands/outline.md`

```markdown
---
description: Start or resume the outlining phase of a research paper.
argument-hint: "[topic or working title]"
---
Invoke the `superpower-writing:outlining` skill. Topic/title (if any): $ARGUMENTS.
```

#### Task 13: `commands/draft.md`
Invokes `superpower-writing:drafting`. Argument = section name (optional).

#### Task 14: `commands/revise.md`
Invokes `superpower-writing:revision`. Argument = path to review file (optional).

#### Task 15: `commands/submit.md`
Invokes `superpower-writing:submission`. No argument.

#### Task 16: `commands/check-deps.md`
Runs `${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh` and reports status. No argument.

```markdown
---
description: Verify scientific-agent-skills is installed and superpower-writing can run.
---
Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh`. If it exits non-zero, surface the install command and stop. If it exits zero, say "deps OK".
```

#### Task 17: `commands/stash.md`
Moves current `.writing/` (except `archive/`) into `.writing/stash/<name>/`. Invokes `superpower-writing:main` skill's stash routing.

#### Task 18: `commands/archive.md`
Moves current `.writing/` snapshot into `.writing/archive/<date>/` after submission. Invokes `superpower-writing:submission` post-archive flow.

- [ ] For each command: write file, `git add commands/<name>.md && git commit -m "feat: /<name> command"`.

---

### Task 19: Integration smoke test

**Files:**
- Create: `tests/smoke.sh`

- [ ] **Step 1: Write end-to-end smoke test**

```bash
#!/usr/bin/env bash
set -euo pipefail
PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT"
cd "$WORK"

echo "== init =="
bash "$PLUGIN_ROOT/scripts/init-writing-dir.sh"
test -f .writing/outline.md
test -f .writing/metadata.yaml
test -d .writing/manuscript

echo "== deps check (may fail if upstream not installed; that's OK here) =="
bash "$PLUGIN_ROOT/scripts/check-deps.sh" || echo "  (missing upstream is expected in CI)"

echo "== claim enforcement: stub blocks =="
cat >.writing/claims/section_02_methods.md <<EOF
- id: meth-c1
  CLAIM: test
  EVIDENCE: []
  STATUS: stub
EOF
out=$(echo '{"tool_name":"Write","tool_input":{"file_path":"'$WORK'/.writing/manuscript/02_methods.md","content":"<!-- claim: meth-c1 -->\nbody"}}' | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q "block" || { echo "FAIL: stub claim did not block"; exit 1; }

echo "== claim enforcement: evidence_ready allows =="
sed -i.bak 's/stub/evidence_ready/' .writing/claims/section_02_methods.md
echo '{"tool_name":"Write","tool_input":{"file_path":"'$WORK'/.writing/manuscript/02_methods.md","content":"<!-- claim: meth-c1 -->\nbody"}}' | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh"

echo "ALL SMOKE TESTS PASSED"
```

- [ ] **Step 2: Run it**

```bash
chmod +x tests/smoke.sh
bash tests/smoke.sh
```

Expected final line: `ALL SMOKE TESTS PASSED`.

- [ ] **Step 3: Commit**

```bash
git add tests/smoke.sh
git commit -m "test: end-to-end smoke test"
```

> Log to `.planning/findings.md`: any test failures, missing edge cases, or OS-specific quirks.

---

### Task 20: Final integration review

- [ ] **Step 1: Run the whole smoke suite one more time**

```bash
cd /home/ubuntu/sipeng/superpower-writing && bash tests/smoke.sh
```

- [ ] **Step 2: Install the plugin locally and verify skills load**

```bash
claude plugin marketplace add /home/ubuntu/sipeng/superpower-writing
claude plugin install superpower-writing
# then in a new Claude session: invoke /writing:check-deps and observe dep-check output
```

- [ ] **Step 3: Update `.planning/progress.md` with completion status**

Set every dashboard row to ✅. Append a Session log describing what was built, what tests ran, and any follow-ups deferred to v2 (multi-author, Zotero, non-IMRAD formats).

- [ ] **Step 4: Final commit + tag**

```bash
git add .planning/progress.md .planning/findings.md
git commit -m "chore: v0.1.0 scaffolding complete"
git tag v0.1.0
```

---

## Parallelism Groups

- **Group A** (serial, 1 task): Task 0 (scaffold) — blocks everything else.
- **Group B** (parallel, 3 tasks after A): Task 1 (init-writing-dir), Task 2 (check-deps.sh), Task 4 (enforce-claims.py is self-contained, depends only on Task 0).
- **Group C** (serial, 1 task after B): Task 3 (hooks/hooks.json + SessionStart wrapper) — depends on Task 2 existing and Task 4's hook script path.
- **Group D** (parallel, 7 tasks after C): Tasks 5–11 (seven SKILL.md files). Fully independent.
- **Group E** (parallel, 7 tasks after D): Tasks 12–18 (slash commands). Independent of each other; each depends only on its corresponding skill existing (Group D).
- **Group F** (serial, 1 task after E): Task 19 (smoke test).
- **Group G** (serial, 1 task after F): Task 20 (final integration + tag).

**Parallelism score:** maximum 7-way parallelism in Groups D and E; overall 17 of 20 tasks run in parallel phases, 3 serial gates.

---

## Self-Review (inline)

1. **Spec coverage:** design.md §1–12 each map to at least one task. §2 deps → Tasks 2, 3, 16. §4 `.writing/` → Task 1. §5 skill mapping → Tasks 5-11. §6 claim-first → Task 4 (hook) + Task 8 (drafting) + Task 9 (verify). §7 stage gates → Task 5 (main routing). §8 exec strategies → Task 8. §9 review loop → Task 10. §10 metadata.yaml → Task 1 template + Task 6 population + Task 11 gate. §11 [NEEDS-EVIDENCE] → Evidence Gap Summary. ✅
2. **Placeholder scan:** Every "copy from design.md §X" is a concrete cross-reference, not a TODO. Hook python body is spec-described but not inlined; this is acceptable because the spec is exhaustive (inputs, outputs, regex, exit codes, error messages). Commands are 2-line files shown inline. No red flags.
3. **Type consistency:** Claim YAML fields (`id`, `CLAIM`, `EVIDENCE`, `STATUS`) used consistently across Task 1 template, Task 4 parser, Task 6 generation, Task 9 verification. File-naming convention (`section_NN_slug.md`) used consistently. ✅
4. **Evidence gaps:** 4 items tracked; 1 addressed during impl (Task 4), 1 during impl (Task 3), 2 deferred to post-MVP with an inline note. ✅

---

## Execution Handoff

Ready for execution. Present the 3 standard execution-strategy options below.
