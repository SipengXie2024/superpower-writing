---
name: adversarial-review
description: Kill-argument adversarial pass that produces one committed strongest-rejection memo, then an independent adjudicator rules each atomic point answered_by_current_text, partially, or unresolved. A helper maps the rulings to an advisory PASS / WARN / FAIL verdict the adjudicator cannot self-grade. Use when a draft is stable and you want the single worst-case reviewer argument before submission.
---

# Adversarial Review

## Overview

Score-based reviews list weaknesses by severity and rarely commit. This skill runs the opposite pass. It forces one reviewer to write the single argument an area chair would reject the paper on. A fresh adjudicator then rules that argument point by point. The verdict is computed from the rulings by a helper, so the adjudicator never grades its own work.

The exercise surfaces one specific failure mode that balanced reviews miss: the headline-killing objection. A balanced reviewer files scope-overclaim as one major item among five and moves on. An adversarial reviewer must pick the most damaging line and develop it in about 200 words. That forced commitment produces sharper feedback than a ranked list.

**Core principle:** commit to one argument, then judge it externally. The attack must not hedge. The verdict must not be self-graded.

**This is detect-only.** The skill reads `.writing/manuscript/*.tex` and writes one memo plus a progress row. It never edits manuscript prose and never auto-mutates `.writing/` claim state. The verdict is advisory: surface it to the user and let the user decide what to fix.

**Relation to the two-stage review gate.** Drafting already runs spec review and manuscript quality review per section (see `skills/planning-foundation/references/review-loop-protocol.md`). Those gates check on-spec coverage and prose quality. This skill is different. It runs once on a whole stable draft and asks the headline-rejection question that per-section review cannot see.

## When to Use

- A full draft is stable and the headline claims are settled. Run one adversarial pass before submission.
- Rebuttal preparation: predict the strongest reviewer objection so the response is ready in advance.
- A theory or systems paper whose title or abstract may advertise more than the body proves.
- A paper where a reviewer could attack scope, assumption-versus-claim mismatch, a missing proof obligation, or an evidence-versus-headline gap.

Do NOT use this skill when:

- The headline is still moving. Fix the title and abstract first, then run one pass against the stable version.
- Experiments are still running. Wait until the evaluation numbers settle.
- A section needs routine spec or quality review. That is drafting's two-stage gate, not this skill.
- The paper has no theorems and no scope or generality claim. Standard review is more useful. Report this and stop rather than forcing a memo.

## The Type-B gate

This skill exists because its verdict needs taste, so it is a Type-B check by the plugin's gate.

> Could a script with no taste answer this gate? Yes -> Type-A: the model may self-judge (e.g. a claim tag is present, a DOI resolves, an abstract is citation-free, prose numbers match a table). No, it needs taste -> Type-B: route to an independent or cross-model reviewer thread and never reply in place. A loop may DRIVE its own iteration but may not ACQUIT its own Type-B verdict.

The attack memo and the adjudication are both Type-B: judging whether an argument kills a paper needs taste. So each runs in its own fresh thread and never replies in place. The count-to-verdict step is the one Type-A slice: a script with no taste maps the rulings to PASS / WARN / FAIL. The helper at `scripts/compute_verdict.py` owns that slice precisely so the adjudicator cannot acquit its own verdict. The full doctrine and the canonical wording live in `skills/planning-foundation/references/review-loop-protocol.md`.

## Two-Thread Design

Thread 1 attacks. A fresh Thread 2 adjudicates. Thread 2 is never a reply to Thread 1. Neither thread sees prior reviews, fix lists, or any context outside the current paper files. Zero shared context is the whole point: the adjudicator must read the paper as a cold reviewer would.

Each thread runs as a fresh cross-model call through the Codex bridge, or as a fresh single-use subagent. Either way, start a new thread per call. For the Codex bridge, invoke `${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py` in the background with no `--SESSION_ID`, once for the attack and once for the adjudication. Do not reuse the attack session for the adjudication.

### Step 0: Preconditions

1. Confirm `.writing/` exists. If not, there is no draft to attack. Stop and say so.
2. Inventory the source. List `.writing/manuscript/*.tex` and the `.bib`. Note the compiled PDF if present. If no `.tex` files exist, stop: there is nothing to review.
3. Applicability check. If the paper has fewer than two theorem-class environments AND the abstract makes no scope or generality claim, this skill adds little. Tell the user, recommend `claim-verification` or a standard review, and stop unless the user insists.
4. Headline-stability check. If the title or abstract is still in flux, the attack will chase a moving target. Ask the user to confirm the headline is settled before continuing.

### Step 1: Attack memo (Thread 1)

Run one fresh thread. Brief it to write the single strongest rejection argument in about 200 words, citing `file:line`, with no hedging. The full attack brief, the six attack axes, and the tone rules are in `references/attack-and-verdict.md`. Read that file now and paste the brief into the thread.

Key constraints, summarized here:

- About 200 words. Do not exceed 250.
- One argument, not a list. Pick the most damaging line and develop it.
- Cite specific `file:line` locations or equation numbers when accusing.
- Do not hedge. Do not acknowledge mitigations elsewhere in the paper. This is the rejection paragraph; the defense gets the next thread.
- Read only the current paper files. No prior reviews, no fix lists.

Save the returned memo verbatim. Both Thread 2 and the report use it.

### Step 2: Adjudication (Thread 2)

Run a second fresh thread, independent of Thread 1. Give it the paper files and the attack memo verbatim. Brief it to decompose the attack into 3 to 7 atomic rejection points and rule each one. The full adjudication brief and the per-point output shape are in `references/attack-and-verdict.md`.

Each point gets exactly one ruling:

- `answered_by_current_text` means the current source already refutes this point. Cite `file:line`.
- `partially` means the source has some response but not enough to refute the point as written.
- `unresolved` means the source has no effective response.

The label `answered_by_current_text`, not `fixed`, is deliberate. The word `fixed` implies a history of patching and biases the adjudicator toward optimism. The adjudicator reads the paper cold, so the neutral label keeps the ruling honest.

For each `partially` or `unresolved` point, the adjudicator also records a severity of `critical`, `major`, or `minor`. When the point is an evidence or empirical gap rather than a writing gap, it sets `needs_experiment` to true. An author-chosen position, such as a deliberate title-scope decision, is `partially` with a note that the position is intentional. It is not `answered_by_current_text` just because it was chosen on purpose. The adjudicator says whether that position is sustainable under the attack.

The adjudicator outputs per-point rulings only. It does NOT output a top-level verdict. That is the next step's job.

### Step 3: Compute the verdict (external, non-self-grading)

Collect the adjudicator's rulings into a JSON memo and pipe it to the helper:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/scripts/compute_verdict.py" < points.json
```

Input shape (one object per atomic point):

```json
{"points": [
  {"id": "P1", "ruling": "answered_by_current_text"},
  {"id": "P2", "ruling": "partially", "severity": "minor"},
  {"id": "P3", "ruling": "unresolved", "severity": "critical", "needs_experiment": true}
]}
```

The helper emits the verdict, a reason code, the recommended 3-way action, and the tallied counts. It exits 2 on malformed input, for example a point count outside 3 to 7 or a missing severity on a non-answered point. The mapping table is in `references/attack-and-verdict.md`. Do not hand-derive the verdict. The helper owns it so the adjudicator cannot grade its own outcome.

The recommended action is one of three, ported from the adversarial review workflow: `pass`, `needs revision`, or `needs NEW experiment`. The third matters: it tells the author the gap is an empirical one that prose edits cannot close, so a new experiment or measurement is the only real fix.

### Step 4: Write the memo

Write one committed memo to `.writing/adversarial-review.md` with this structure:

```markdown
# Adversarial Review (<ISO-8601 timestamp>)

**Reviewer threads:** attack <thread-or-session id>, adjudicator <thread-or-session id> (fresh, no shared context)
**Verdict:** <PASS | WARN | FAIL> (reason_code: <...>)
**Recommended action:** <pass | needs revision | needs NEW experiment>

## Attack memo (verbatim, Thread 1)

> <the ~200-word rejection memo>

## Adjudication (per-point, Thread 2)

### P1: <short label>
- Attack claim: <~30 words>
- Ruling: answered_by_current_text
- Evidence: <file:line, ~50 words>

### P2: <short label>
- Attack claim: <~30 words>
- Ruling: unresolved
- Severity: critical
- Needs new experiment: yes
- If unresolved, recommended fix: <one actionable sentence>

## Counts
- answered_by_current_text: <X>
- partially: <Y>
- unresolved: <Z>

## Net assessment
<one paragraph: would the paper survive a senior area-chair read of this attack, given only the current source? Be honest. If Y or Z hit the headline, say so.>

## Recommendation to the user
<advisory only. The user decides.>
If an unresolved point is research-level, record it as a known limitation. If it is writing-level, queue a targeted revision. Never auto-edit the manuscript.
```

One memo per run. When a new run starts, archive the old memo under `.writing/archive/` rather than overwriting blindly, so the audit trail survives.

### Step 5: Log and surface

1. If `.writing/progress.md` exists, append one row recording the run: timestamp, skill name, memo path, verdict, and a one-line summary of counts. Match the existing table format; do not invent a new schema.
2. Surface the result to the user in plain prose: the attack thrust in one sentence, the counts, the verdict and reason code, the recommended 3-way action, and the memo path. Then stop. The user decides what to act on.

## Key Principles

**The attack must commit.** One argument, about 200 words, no "consider also" hedge. The entire value is forcing the reviewer to pick the single most damaging line. A list dilutes it back into a balanced review and loses the signal.

**The adjudicator classifies, not minimizes.** `unresolved` is honest when the paper has no effective response. Do not downgrade to `partially` unless the supporting evidence is real and cited. A silent false negative here is worse than a flagged false positive the user can dismiss.

**The verdict is external.** The adjudicator emits rulings; the helper maps them. This separation is the non-self-grading guarantee. Never let the adjudicating thread state the top-level verdict, and never hand-derive it to skip the helper.

**Fresh threads, zero context.** Thread 2 is not a reply to Thread 1. Neither thread receives prior reviews, fix lists, or executor summaries. Cold reading is what makes `answered_by_current_text` trustworthy.

**Detect-only and advisory.** This skill produces one memo and one progress row. It never edits manuscript prose, never flips claim STATUS, and never auto-rejects. The verdict goes to the user, who owns the decision.

**Never fabricate.** Both threads cite `file:line` from the real source. If a thread cannot point to a location, it has not earned the claim. Do not invent line numbers, equation labels, citations, or numeric results. Mark anything unverifiable as `[UNVERIFIED]` and surface it.
