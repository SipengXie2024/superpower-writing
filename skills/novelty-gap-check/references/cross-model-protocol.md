# Cross-model second-opinion protocol

How to get an independent novelty read from a second model during Phase C. This step is optional. Use it for a contentious or high-stakes idea where one model's judgment does not settle the question. Skip it for a clearly novel or clearly dominated idea.

The cross-model channel in this plugin is `superpower-writing:collaborating-with-codex`. That skill drives Codex CLI through a bridge. Do not call any other model endpoint here.

## 1. When to run it

Run the second opinion when:

- The per-claim deltas are mixed and the overall verdict sits on a boundary (a MED that could be HIGH, a load-bearing LOW the user disputes).
- The idea is high-stakes: a thesis direction, a months-long commitment, a funded milestone.
- The user explicitly asks for a second model, or for a "brutal" or "adversarial" novelty read.

Skip the second opinion when one model already settles the question. A claim with an exact published precedent does not need a second vote to call LOW. A claim with no precedent after a thorough search does not need one to call HIGH.

## 2. Write a dossier file, do not paste inline

The idea description, the core claims, and the candidate-paper list are usually too large to paste into a bridge prompt cleanly. Write a dossier file first, then send the bridge only the path. This keeps the prompt small and gives the second model a stable artifact to read.

Recommended location: `.writing/novelty-dossier.md` when a project state directory exists, otherwise a temp path such as `/tmp/novelty-dossier-<slug>.md`. The dossier is a working artifact. It is not a manuscript file and carries no claim STATUS.

Dossier contents:

```markdown
# Novelty dossier (<idea slug>)

## Proposed idea
<1-2 sentence description>

## Core technical claims
1. <claim 1>
2. <claim 2>
...

## Candidate prior work found in Phase B
| # | Paper | Year | Venue | arXiv/DOI | one-line overlap |
|---|-------|------|-------|-----------|------------------|
| 1 | ... | ... | ... | ... | ... |

## Our per-claim deltas (for the reviewer to challenge)
1. <claim 1>. Delta <HIGH/MED/LOW>. Closest <paper>.
...

## Questions for the reviewer
1. Is this idea novel? Judge per claim.
2. What is the closest prior work for each claim? Name papers you can verify.
3. What is the delta between each claim and its closest prior work?
4. Did our search miss an obvious recent preprint? Name it if so.
```

Include the three core questions verbatim: is this novel, what is the closest prior work, and what is the delta. Add the fourth question to catch a recent paper the first-pass search missed.

## 3. Brief the bridge

Invoke the bridge via `superpower-writing:collaborating-with-codex`. Read that skill for the exact bridge command, the `--cd` requirement, and the background-execution convention. Brief it like a senior peer, not a search box:

- Point it at the dossier path. Tell it to read the dossier and answer every question in it.
- State the constraint plainly: name only papers it can verify, never fabricate an arXiv ID or DOI, and tag anything unverifiable `[UNVERIFIED]`. The same never-fabricate rule binds the second model.
- Ask for a per-claim HIGH/MED/LOW verdict and a one-line delta for each, so its output merges directly into the report table.

Run the bridge in the background per the collaborating-with-codex convention. Do not poll. Continue when its result returns.

## 4. Reconcile the two reads

The second opinion is advisory input, not an override. Reconcile it against your own Phase C deltas:

- **Agreement** raises confidence. Record the verdict as is and note the second model concurred.
- **Disagreement on a claim** is a signal to look again. Re-read the disputed paper's abstract before deciding. The model that read the paper more carefully wins, not the more recent one.
- **A new paper from question 4** must clear the same pre-search verification gate before it enters the report. Resolve its identifier. If it does not resolve, tag it `[UNVERIFIED]`.

Surface both reads to the user when they diverge on a load-bearing claim. A disagreement the user can see is more useful than a single smoothed-over verdict. The user owns the final call.

## 5. Tracing

Keep the dossier file and the bridge's returned answer for the record, the same way `claim-verification` keeps its report as an audit trail. When `.writing/` exists and the user wants the novelty report persisted, the dossier sits alongside it. When no project state exists, the dossier is a temp artifact and the reconciled verdict goes inline into the conversation.
