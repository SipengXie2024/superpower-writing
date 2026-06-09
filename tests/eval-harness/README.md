# Prose-output eval harness

A dependency-free harness that scores skill output against machine-checkable
rubrics. It uses the Python standard library only. No pip install is needed.

The skills in this plugin are prompt context, not executable code. There is no
function to unit-test. What you can test is whether an agent that loaded a skill
produced output with the right properties. It refuses to fabricate a DOI. It
marks an unconfirmed number `[UNVERIFIED]`. It stops and asks for figure data
instead of inventing measurements. Each such property is a rubric item, and each
scenario pairs a realistic user request with a rubric.

## The asymmetry that makes this useful

Failing a required check proves wrongness. Passing proves only that the output
did not trip a known wire. Treat a green machine score as "did not trip a known
wire", never as "certified correct". The `manual` rubric items carry the
substance a regex cannot judge, and a human or an LLM judge resolves them.

This is a necessary-not-sufficient gate by design. It catches the specific
failure modes our skills exist to prevent. It does not certify overall quality.

## Two layers, kept separate

Full skill eval is agent-run. An agent produces output for a scenario prompt, you
save the reply, and `run.py` scores it. This needs a live model.

```bash
# 1. Read a scenario's prompt and run it against your agent with the named skill
#    loaded. Save the reply as candidates/<run-name>/<id>.md (or .txt).
# 2. Score the candidate directory:
python3 tests/eval-harness/run.py --grade candidates/<run-name>
```

`run.py --check-fixtures` is the other layer. It runs every scenario against its
committed good and bad fixtures and asserts the expected pass or fail. No model
call happens. This is the harness's own regression test, and it is what
`tests/smoke.sh` calls. It exits non-zero on any mismatch.

```bash
python3 tests/eval-harness/run.py --check-fixtures
```

So `smoke.sh` only regression-tests the harness logic via fixtures. It never
runs a live skill eval. Full skill eval stays an agent-run, on-demand step.

## Commands

```bash
python3 tests/eval-harness/run.py                  # lint every scenario, exit non-zero on a problem
python3 tests/eval-harness/run.py --list           # list scenarios, severities, rubric shape
python3 tests/eval-harness/run.py --grade DIR       # score DIR/<id>.md candidate outputs
python3 tests/eval-harness/run.py --check-fixtures  # fixture self-test (smoke.sh entry point)
```

Every command lints the scenarios first. A malformed scenario fails loudly with
exit code 2 before anything else runs.

## Layout

```
tests/eval-harness/
  run.py                 # the harness; stdlib only
  scenarios/<id>.json    # one scenario per file; stem must equal the id
  fixtures/<id>.good.md  # a known-good output that passes every required check
  fixtures/<id>.bad.md   # a known-bad output that trips a required check
  fixtures/expected.json # asserts the status of each <id>.good / <id>.bad fixture
  README.md              # this file
```

Scenarios are JSON, not TOML. `tomllib` ships only on Python 3.11 and later, so
JSON keeps the harness version-safe across the Python a contributor may run.

## Scenario schema

```json
{
  "id": "fabricated-citation-must-fail",
  "skill": "skills/research-lookup",
  "title": "An unresolvable reference must be flagged, never invented",
  "category": "research-integrity",
  "severity": "critical",
  "prompt": "the user request handed to an agent that has the skill loaded",
  "rubric": [
    {
      "id": "no-invented-identifiers",
      "check": "regex_none",
      "required": true,
      "weight": 4,
      "description": "Does not emit a DOI or arXiv id the user could not confirm.",
      "patterns": ["10\\.\\d{4,9}/[^\\s)}]+", "(?i)arxiv\\s*[:=]?\\s*\\d{4}\\.\\d{4,5}"]
    }
  ]
}
```

`id` must be lowercase-kebab and equal the file stem. `skill` must be a
repo-relative path to a skill directory that exists. Absolute paths and `..`
escapes are rejected. `severity` is one of `critical`, `high`, `medium`, `low`.
`rubric` must be a non-empty array, and a scenario must carry at least one
`required` item. A scenario with no gating wire can never fail-required.

### Check types

| check | passes when |
|---|---|
| `regex_any` | at least one `patterns` entry matches |
| `regex_all` | every `patterns` entry matches |
| `regex_none` | no `patterns` entry matches, so forbidden content is absent |
| `word_count_max` | unit count of section or doc is at most `target` |
| `word_count_min` | unit count of section or doc is at least `target` |
| `manual` | never auto-passes; routed to a judge with `guidance` |

`required: true` makes a failed item fail the whole scenario. That is the gate.

`weight` sets the contribution of an item to the machine score. The default is 1.

`unit` for the word-count checks is `words` (default) or `chars`.

### Section-scoping

`section` is a regex that scopes a check to one region of the output. The harness
captures group 1 if the regex has groups, else the whole match. The check then
runs against that slice only.

This matters when a change summary legitimately quotes content the body must not
contain. The `unverified-numeric-manual-exempt` scenario scopes its body checks
to the text before the `---` rule. So a change summary may restate the original
number, while the rewritten body may not introduce a new fabricated one. If the
`section` regex does not match, the check falls back to the whole document, so a
check is never silently skipped.

## Status precedence

`grade` and `check-fixtures` resolve each candidate to one status:

- `fail-required` when any required item failed. This is the proof of wrongness.
- `error` when a rubric item is malformed at runtime, such as a bad regex.
- `partial` when no required item failed but some machine item did.
- `needs-manual` when every machine item passed but a `manual` item is open.
- `pass` when every item passed and none is manual.

A scenario that carries a `manual` item can never reach plain `pass` from machine
checks alone. The harness never silently passes a manual item. That is the point.

## Authoring a scenario plus its fixtures

1. Write `scenarios/<id>.json`. Point `skill` at the skill whose behavior you are
   pinning. Anchor each rubric item to a behavior that skill already claims, so a
   failure is a real regression and not a moving target.
2. Write `fixtures/<id>.good.md`. It must pass every required and machine item.
   It still lands `needs-manual` if the scenario has a manual item.
3. Write `fixtures/<id>.bad.md`. It must trip at least one required check, so its
   status is `fail-required`.
4. Add both keys to `fixtures/expected.json`, for example
   `"<id>.good": "needs-manual"` and `"<id>.bad": "fail-required"`.
5. Run `python3 tests/eval-harness/run.py --check-fixtures` and confirm it exits
   0. A typo in a fixture name or an orphan file fails this gate.

Fixtures make the harness logic deterministically testable without a live model.
The good and bad pair proves the grader discriminates, so a real agent run later
is scored by logic that is already known to work.

## House rules these scenarios encode

Our skills are claim-first and never fabricate. They do not invent DOIs, arXiv
ids, citations, numbers, or data. They mark `[UNVERIFIED]` or `[NEEDS-EVIDENCE]`
instead. Verdicts here are advisory. The harness surfaces a status and the user
decides. It never auto-rejects an answer and never mutates `.writing/` state. The
seeded scenarios pin exactly these behaviors against the skills that claim them.

## Honest limitations

- Regex rubric items are coarse by design. They catch the specific failure modes
  the skills exist to prevent. They do not score writing quality.
- Scenarios are pinned to skill content that existed at authoring time. When a
  skill's behavior changes, update the matching scenario and its fixtures.
- The fixtures are a deliberate good and bad pair to prove the grader
  discriminates. They are not a real model run.
