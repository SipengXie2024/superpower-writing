---
name: claim-verification
description: Pre-submission verifier. Walks every % claim tag in LaTeX manuscript/*.tex, confirms \cite{} citekeys resolve against .writing/refs.bib (exported from Zotero), runs semantic match against research-lookup abstracts, checks numeric/table consistency, fails if any [NEEDS-EVIDENCE] or draft-only markers remain. Use at submission gate or on demand.
---

# Claim Verification

## Overview

Pre-submission gate that walks every tagged claim in `.writing/manuscript/*.tex` and proves it supportable. Four sequential passes: completeness, citation resolution (dual source of truth via Zotero + network), numeric/table consistency, and reporting-guideline checklist. Outputs `.writing/verify-report.md` per-claim PASS/FAIL and caches resolved DOIs in `.writing/verify-cache.json`.

**Core principle:** Evidence before claims, always. Violating the letter of this rule is violating the spirit.

**Iron law:** No `STATUS: verified` flip without fresh pass evidence recorded in the report.

**Relation to the PreToolUse hook:** the hook (see `superpower-writing:main` §Claim-First Protocol) already blocks prose writes against stub-status claims during drafting — drafting flips `STATUS` to `evidence_ready` when evidence is found. This skill is what flips `evidence_ready` → `verified` after the four passes succeed. Never edit `STATUS` to `verified` manually: the audit trail lives in `.writing/verify-report.md`.

## When to Use

- User declares paper ready to submit (always run before `submission` skill).
- User requests an interim verification ("check my claims", "verify citations", "run pre-submit checks").
- End of a `revision` round, before closing the round.
- On demand during drafting to check a single section.

Do NOT use during initial drafting to flip claims green — that is drafting's job (it flips stub → evidence_ready, not → verified).

## Checklist

Run in order. Stop at first failing pass only if the user requests fail-fast; otherwise collect all failures into the report.

- [ ] Confirm `.writing/` exists and `metadata.yaml` is populated (no `TODO` except YAGNI fields)
- [ ] Pass 1 — Claim Completeness
- [ ] Pass 2 — Citation Resolution (Zotero first, network fallback)
- [ ] Pass 3 — Numeric/Table Consistency
- [ ] Pass 4 — Reporting-Guideline Checklist (delegates to `peer-review`)
- [ ] Write `.writing/verify-report.md` with per-claim PASS/FAIL
- [ ] Update `.writing/verify-cache.json` with resolved DOIs
- [ ] Flip eligible claim `STATUS` from `evidence_ready` to `verified` (only when ALL four passes PASS for that claim)
- [ ] Update `.writing/progress.md` Verification Evidence row with command + exit status + report path

## Process

### Step 0: Preconditions

Before running any pass:

1. Confirm `.writing/` exists. If not, abort with instruction to run outlining/drafting first.
2. Read `.writing/metadata.yaml`. Fail if any top-level key is `TODO` (except the v1 YAGNI list: multi-author fields). Fail fast — verification is pointless against incomplete metadata.
3. Read `.writing/verify-cache.json` if present; treat as read-through cache keyed by DOI. Cache entries expire never within a session; user must manually delete to force re-resolution.
4. List all `.writing/manuscript/*.tex` files and their paired `.writing/claims/section_*.md` files.

### Step 1: Pass 1 — Claim Completeness

Goal: every load-bearing paragraph is tagged and backed.

For each `.writing/manuscript/*.tex`:

1. Parse all `^\s*%\s*claim:\s*(\S+)` tags (LaTeX line comments) → set of referenced claim ids.
2. Parse all `^\s*%\s*draft-only` markers → record as FAIL unconditionally (draft-only is a drafting escape hatch; it must be resolved before submission).
3. Parse all `[NEEDS-EVIDENCE]` literal strings → record as FAIL.
4. For each referenced claim id, locate the matching entry in `.writing/claims/section_<NN>_<slug>.md`, where `<NN>_<slug>` is the manuscript file's basename without extension (e.g., manuscript `03_methods.tex` pairs with claims `section_03_methods.md`):
   - **Missing entry** → FAIL: `claim '<id>' referenced in <file> but not defined in claims file`.
   - **STATUS: stub** → FAIL: `claim '<id>' still stub; drafting did not resolve EVIDENCE`.
   - **STATUS: evidence_ready** → PASS Pass 1 (it advances through Pass 2–4 to become `verified`).
   - **STATUS: verified** → PASS Pass 1 (already verified in prior run; Pass 2–4 may re-validate via cache).
5. For each paragraph that neither has `% claim:` nor `% draft-only`: check if section is allow-listed. The PreToolUse hook exempts any stem ending in `_<slug>` for slug ∈ `UNPROTECTED_SLUGS` (`abstract`, `references`, `acknowledgments`) from paragraph-tag enforcement. All other `manuscript/NN_*.tex` files require every load-bearing paragraph to carry `% claim: id` or `% draft-only`. Always-skipped within any file: LaTeX line comments (lines starting with `%`), blank lines, structural LaTeX commands (lines starting with `\section`, `\subsection`, `\begin`, `\end`, `\label`, `\caption`, etc. — the full list is in `hooks/enforce-claims.py` `STRUCTURAL_LATEX_CMDS`). Anything else fails with: `paragraph in <file>:<line> lacks % claim: id or % draft-only marker`.

**Allow-list is configurable.** Support `.writing/verify-config.yaml` with key `allowlist_sections: [<filename>, ...]` — if present, those filenames extend the hook's default exemption set for this skill's checks.

### Step 2: Pass 2 — Citation Resolution (dual source of truth)

This is the most consequential pass. Implements design.md §14.3 exactly.

For each claim that passed Pass 1 with `type: citation` EVIDENCE entries:

#### 2a. Zotero-first lookup (if enabled)

1. Read `metadata.yaml`. If `zotero.enabled: true`:
   - Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh` once per session to confirm credentials and the `zotero-mcp` binary. Cache result in `.writing/findings.md` as `zotero_verified_at: <ts>`.
   - For each citation DOI, call the `zotero_search_items` MCP tool (from the `zotero` server in `.mcp.json`) with `query=<DOI>`, `qmode="everything"`. If `zotero.collection_key` is set, filter results to items whose `data.collections` array contains that key; otherwise keep all hits.
   - **Zotero hit** (exactly one filtered match): call `zotero_get_item_metadata(item_key=<key>)` to retrieve the stored abstract. Record `source: zotero`, `zotero_item_key: <key>` in the claim EVIDENCE entry. Proceed to 2c (semantic match).
   - **Ambiguous** (multiple filtered matches for one DOI): log to `.writing/findings.md` under "Issues" and treat as a miss.
   - **Zotero DOI miss, semantic fallback:** before giving up on Zotero, call `zotero_semantic_search(query=<CLAIM text>, limit=5)`. When the library has been indexed with fulltext (has_fulltext=True chunks), this matches claim content against paper paragraphs, not just titles/abstracts — catching cases where the DOI in your bibliography is slightly off (preprint vs publisher, pre-print server vs final version) but the paper is actually in the library. For each hit whose `similarity_score >= 0.45`, call `zotero_get_item_metadata(item_key=<key>)` and verify by DOI / title match. Exactly one high-confidence match → treat as Zotero hit with `source: zotero-semantic`, `zotero_item_key: <key>`, `match_score: <float>`. Otherwise proceed to 2b.
   - **Zotero miss (DOI + semantic):** proceed to 2b.
2. If `zotero.enabled: false` or `zotero` section absent: skip directly to 2b.

#### 2b. Network fallback

1. Check `.writing/verify-cache.json` for the DOI. If present AND `source` field indicates successful prior resolution, use cached abstract_hash to confirm abstract still matches (re-fetch abstract only if hash mismatch or cache entry absent).
2. On cache miss / mismatch, invoke `Skill(skill="citation-management")` with the DOI. This resolves the DOI against Crossref and returns canonical metadata.
3. On failure or ambiguity, invoke `Skill(skill="research-lookup")` with the DOI and the CLAIM text. research-lookup queries Crossref/PubMed and returns abstract + metadata.
4. **Network hit:** record `source: network` in the claim EVIDENCE entry.
5. **`auto_push_new_citations: true` behavior:** if Zotero is enabled AND auto_push is true AND network (not Zotero) returned the hit, push the resolved item to `zotero.collection_key` by calling `zotero_add_by_doi(doi=<DOI>, collection_key=<key>)` from the `zotero` MCP server. The tool dedupes by DOI internally. Update EVIDENCE `source` to `both` and record the returned item key as `zotero_item_key`.
6. **Network miss AND Zotero miss:** FAIL: `DOI <doi> for claim '<id>' unresolvable via Zotero or Crossref/PubMed`.

#### 2c. Semantic match

Once an abstract is in hand (from Zotero or network):

1. Compute abstract hash and store in `.writing/verify-cache.json` keyed by DOI: `{source, resolved_at, abstract_hash, abstract_excerpt}`.
2. Perform an LLM-based semantic match: does the abstract plausibly support the CLAIM text? Use a strict rubric: the claim must not contradict the abstract; the abstract's findings/methods must overlap with the claim's substantive content.
3. **Match PASS:** record PASS in report with excerpt of supporting abstract sentence.
4. **Match FAIL:** record FAIL with reason (e.g., "abstract describes mouse model; claim is about human cohort"). This is a soft failure — surface to user for manual review rather than auto-rejecting (semantic match has known FP/FN issues). User confirms or overrides in report before submission proceeds.
5. **Abstract ambiguous, body lookup:** if the abstract neither clearly supports nor contradicts the claim AND `source: zotero*`, call `zotero_semantic_search(query=<CLAIM text>, filters={"parent_item_key": <key>}, limit=3)` to surface the three most-relevant chunks from the paper body. Re-run the semantic match against those chunks' `matched_text`. Only escalate to fetching full body via `zotero_get_item_fulltext(item_key=<key>)` if the chunk-level check remains ambiguous — fulltext returns the whole paper (often 70K+ chars) and must be read with narrow grep / offset-limit windows, not loaded wholesale into context.

#### 2e. Optional deep pass — `citation-auditor` agent

When the user requests a deep audit (`--deep` flag, or when submission gate is imminent), dispatch the `superpower-writing:citation-auditor` agent in a fresh context with the full manuscript and `.writing/verify-cache.json`. The agent adds six judgment layers Pass 2 does not: over-citation, under-citation, circular/self-citation, staleness, relevance drift (abstract supports claim but not *this* claim), and seminal-work omission. Its findings are advisory — they merge into `verify-report.md` under an "Advisory" block, and the user decides whether to act on each item before submission.

#### 2d. Non-citation EVIDENCE

For EVIDENCE entries with `type: dataset`, `type: figure`, `type: table`, etc.: Pass 2 only validates structural presence of the referenced artifact (dataset identifier exists, figure file exists under `.writing/figures/`, etc.). Content correctness is user's responsibility.

### Step 3: Pass 3 — Numeric/Table Consistency

Purpose: catch copy-paste drift between prose and tables.

1. For each `.writing/manuscript/*.tex`, extract candidate numeric tokens via regex. Default pattern:
   ```
   \b(?:n\s*=\s*)?(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(?:%|‰|p\s*[=<]\s*\d|\(\d+\.\d+[-–]\d+\.\d+\)|M|K)?
   ```
   Capture `n=`, percentages, p-values, confidence intervals, plain counts.
2. Build a ground-truth number pool from all tables (LaTeX `tabular` rows — cells separated by `&`, rows terminated by `\\`) across manuscript/*.tex and all figure captions (`\caption{...}` inside `figure` environments).
3. For each prose number, confirm it appears verbatim in the ground-truth pool. FAIL otherwise.
4. Support `.writing/verify-config.yaml` `numeric_overrides: [<number>, ...]` for narrative numbers that are not table-backed (e.g., round references like "a 2018 cohort"). Numbers in this list skip the check.
5. Per-claim attribution: a FAIL on number `1,247` inside a paragraph tagged `% claim: meth-c1` attaches to claim `meth-c1` in the report.

### Step 4: Pass 4 — Reporting-Guideline Checklist

1. Read `metadata.yaml.reporting_guideline` (CONSORT | STROBE | PRISMA | ARRIVE | none).
2. If `none`: SKIP this pass, record `n/a` in report.
3. Otherwise, invoke `Skill(skill="peer-review")` with arguments: `checklist: <guideline>`, `manuscript_dir: .writing/manuscript/`, `metadata: .writing/metadata.yaml`. peer-review walks the checklist and returns a per-item PASS/FAIL array.
4. Every checklist FAIL becomes a top-level FAIL in the report — does not attach to a single claim (these are document-level concerns).

### Step 5: Emit Report

Write `.writing/verify-report.md` with exact structure:

```markdown
# Verification Report — <ISO-8601 timestamp>

## Summary
- Pass 1 (Completeness): <N passed> / <M total> claims | <K paragraph-tag failures>
- Pass 2 (Citations): <N resolved> / <M citations> | Zotero: <x> | Network: <y> | Both: <z> | Failed: <f>
- Pass 3 (Numerics): <N verified> / <M numbers extracted> | Overrides: <o>
- Pass 4 (<guideline>): <N passed> / <M checklist items> | n/a if guideline=none

## Per-Claim

### claim '<id>' — <PASS | FAIL>
- Pass 1: PASS
- Pass 2: PASS (source: zotero, DOI: 10.xxxx/yyy, matched excerpt: "...")
- Pass 3: PASS (numbers 1247, 0.03 confirmed in Table 1)
- Pass 4: n/a

### claim '<id>' — FAIL
- Pass 2: FAIL — DOI 10.xxxx/zzz unresolvable via Zotero or Crossref/PubMed
- Action: add citation to Zotero collection '<key>' or fix DOI

## Document-Level Failures
(draft-only markers, [NEEDS-EVIDENCE] strings, reporting-guideline failures)

- <file>:<line>: `% draft-only` still present
- <guideline> item 7 FAIL: population flow diagram missing
```

### Step 6: Update Claim STATUS

For each claim where ALL four passes PASS (n/a counts as PASS for Pass 4 when guideline is `none`):

1. Locate the claim entry in its `claims/section_*.md` file.
2. Update `STATUS` from `evidence_ready` to `verified`.
3. Do **not** flip STATUS for any claim with a soft-failure semantic match — leave those as `evidence_ready` pending user confirmation in the report. Once the user edits the report to mark the soft failure as "overridden", re-run verification and the STATUS flip proceeds.

### Step 7: Record Verification Evidence

Per `superpower-writing:verification` discipline, if `.writing/` exists, append a row to the Verification Evidence table in `.writing/progress.md`:

```
| <timestamp> | claim-verification | .writing/verify-report.md | <pass/fail> | <N> claims verified, <M> failures |
```

## Key Principles

### Evidence before claims, always

This skill exists because of failure mode #1: a paper ships with a citation that does not say what the prose claims. Every `STATUS: verified` flip is an assertion that Pass 2's abstract plausibly supports the claim text. Never flip STATUS without the pass evidence in the report.

### Dual source of truth is not redundancy — it's correctness

Zotero stores what the user has vetted. The network stores what the world publishes. A DOI resolvable only on the network but not in Zotero is a citation the user has not personally confirmed — the `auto_push_new_citations: true` flow closes this gap by writing network hits back to Zotero for future vetting. A DOI present in Zotero but unresolvable on the network is a retracted or moved paper — surface as a warning, do not auto-fail (the user's vetted copy is authoritative).

### Cache aggressively, re-fetch cautiously

DOI resolution is expensive and rate-limited. `.writing/verify-cache.json` keyed by DOI with `{source, resolved_at, abstract_hash}` lets re-runs complete in seconds. Re-fetch only when: cache absent, abstract_hash mismatch on re-read, or user explicitly forces (e.g., deletes the cache file). Cache file is gitignored (see project `.gitignore`).

### Semantic match is advisory, not gatekeeping

LLM-based semantic match has FP/FN rates that make hard auto-rejection brittle (design.md §11). Treat Pass 2c failures as soft failures: surface in the report, require explicit user override before claim STATUS flips to `verified`. Do not hide these — a silent false negative is worse than a false positive the user sees.

### Fail-loud on missing metadata

The submission gate depends on `metadata.yaml` being complete. If claim-verification encounters `TODO` fields, abort immediately rather than running downstream passes. Verification against incomplete metadata produces a green report the user cannot trust.

### Never auto-edit the manuscript

This skill reads `.writing/manuscript/*.tex` and writes `.writing/claims/*.md` STATUS fields and the report. It does not touch manuscript prose. Manuscript changes go through drafting or revision, which pass the PreToolUse hook's claim gate.

### Report is the audit trail

The verify-report.md is the document-of-record for this verification round. It is the evidence submission cites ("all claims passed four-pass verification on <date>"). Keep one report per round; revision skill archives old reports under `.writing/archive/reports/` when starting a new round.

## Upstream Skill Contracts

This skill invokes these upstream skills by bare name via the Skill tool (no `plugin:` prefix — scientific-agent-skills is an Agent Skills collection):

| Skill | Invocation point | Expected I/O |
|-------|------------------|--------------|
| `zotero-mcp` (MCP) | Pass 2a, 2c body lookup, §5 push-back | `zotero_search_items` + `zotero_get_item_metadata` for query-by-DOI; `zotero_semantic_search` for claim-text similarity fallback (catches DOI-mismatched items and finds paragraph-level support when the abstract is ambiguous); `zotero_get_item_fulltext` for narrow passage reads when chunks alone are insufficient; `zotero_add_by_doi` for dedup-aware push. Registered in `.mcp.json`. |
| `citation-management` | Pass 2b primary | Resolve DOI → canonical Crossref record. |
| `research-lookup` | Pass 2b fallback / semantic match | DOI → abstract; optionally compare abstract ↔ claim text. |
| `peer-review` | Pass 4 | Input: checklist name + manuscript dir. Output: per-item PASS/FAIL. |

If any of these skills is missing, `main` skill's dep gate will have already hard-failed the session. Inside this skill, a missing upstream at invocation time is an unrecoverable error: halt verification and surface the install command.

## Integration Points

- **main skill:** routes here when user says "verify", "check claims", "pre-submit check", or when `submission` skill starts its gate.
- **drafting skill:** its sub-agents flip `stub → evidence_ready`. This skill flips `evidence_ready → verified`.
- **revision skill:** invokes this skill at the end of each review round (step 5 of the revision pipeline).
- **submission skill:** refuses to proceed unless `.writing/verify-report.md` exists, is newer than the youngest manuscript file, and shows zero failures.
