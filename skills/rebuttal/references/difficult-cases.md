# Difficult Cases

Use this file when a comment cannot be handled by straightforward acceptance and a text edit. Each case names a strategy and gives a template. All templates are CS / systems / ML targeted. Adapt the bracketed slots to the paper.

## Impossible or out-of-scope experiment

The reviewer asks for work that needs a new system, a new dataset, a cluster you do not have, a longitudinal study, or a different evaluation design.

Strategy:

1. Acknowledge the scientific value of the request.
2. Give a study-design or scope reason for declining. The reason is about what the paper measures, not about your resources.
3. Offer alternative evidence already in the paper if it exists.
4. Soften the affected claim or add a limitation so the paper does not overstate.
5. Never plead time, budget, hardware access, or ability. Those reasons invite the reviewer to insist.

The action label is `OUT_OF_SCOPE` or `PARTIAL`, usually paired with `SOFTEN_CLAIM`.

Template:

```text
We agree that [requested experiment, e.g. a 1000-GPU scaling run] would provide an
additional test of [claim]. However, the central result of this paper rests on
[existing evidence in Section X], and the requested experiment would require
[a new cluster / a different benchmark suite / a multi-month deployment] that defines
a separate study rather than a revision of this one. To avoid overstatement, we have
revised [Section / Abstract] to bound the claim and now state that [revised text].
```

Why the study-design framing works. A reviewer who hears "we lack the GPUs" reads it as a fixable excuse and asks again. A reviewer who hears "that experiment answers a different question than this paper poses" has to argue about scope, which is the author's ground. Lead with the question the paper answers, not the constraint you face.

Example retargets:

- ML method paper, reviewer asks for ImageNet-scale validation of a method evaluated on CIFAR: frame the contribution as the mechanism, not the scale, and add a scope sentence.
- Systems paper, reviewer asks for a production deployment: frame the contribution as the design and the controlled benchmark, defer deployment to future work.
- Theory paper, reviewer asks for an empirical study: state that the contribution is the bound, and that an empirical validation is a complementary separate effort.

## Reviewer factual error

The reviewer missed existing data, misread a figure, or stated something the paper contradicts.

Strategy:

1. Do not accuse the reviewer. Never write "the reviewer misunderstood" or "the reviewer is wrong".
2. Cite the exact manuscript location where the data already are.
3. Treat the error as a presentation signal. If the manuscript invited the confusion, clarify the wording.
4. Consider a small revision even when the reviewer is strictly wrong; a one-line clarification costs little and removes the friction.

The action label is usually `DISAGREE` with a clarification, or `ACCEPT_TEXT` if you revise wording.

Template:

```text
We thank the reviewer for raising this point. The relevant result is reported in
[Table 3 / Figure 4 / Section 5.2], where we show [the specific number or finding].
We have revised [location] to surface this more prominently so it is not missed.
```

The move is to point, not to correct. "The data are in Table 3" lets the reviewer find the answer without being told they erred. Adding a clarifying edit signals good faith and pre-empts the same misread by the meta-reviewer.

## Conflicting reviewers

Two reviewers ask for incompatible changes. One wants stronger causal language; another wants it softened. One wants Section 4 expanded; another wants the paper shorter.

Strategy:

1. Surface the conflict in the strategy summary inside `ISSUE_BOARD.md` so it is visible, not buried.
2. Prioritize the editor or meta-reviewer instruction if one exists. The editor breaks ties.
3. Find the minimal revision that satisfies both concerns. Often a single calibrated sentence answers both: state the association precisely and bound the causal reading.
4. Never make incompatible promises. Do not promise Reviewer 1 stronger causal language and Reviewer 2 softened causal language in the same response. The reviewers read each other.
5. If a true balancing choice is unavoidable, explain it briefly in both replies so each reviewer sees the reasoning.

Worked resolution. Reviewer 1 wants "X causes Y"; Reviewer 2 says the evidence is correlational. The minimal satisfying edit is one sentence: "X is associated with Y (Section 5); we do not claim a causal mechanism, and we note the alternative explanation Reviewer 2 raises." This concedes nothing false to either side and contradicts neither reply.

When the editor instruction conflicts with a reviewer, follow the editor and note in the reviewer reply that the change reflects the editor's guidance.

## Reviewer-requested citation

A reviewer asks you to cite a specific paper or to broaden the literature coverage.

Strategy:

1. Evaluate relevance honestly. Add the citation only if it is genuinely relevant.
2. Verify the citation before adding it. Route through `superpower-writing:citation-management`; never invent a DOI, arXiv ID, year, or author list.
3. Use neutral positioning language. Do not imply coercion and do not assume the requested work is the reviewer's own.
4. If the citation metadata is missing and you cannot verify it, mark the row `AUTHOR_INPUT_NEEDED` rather than guessing the reference.

The action label is `ACCEPT_TEXT` when the citation is added, or `DISAGREE` with a relevance reason when it is not.

Template (adding):

```text
We thank the reviewer for pointing to this work. We have added [verified citation] in
[related-work location] and clarified how our approach differs: [exact delta].
```

Template (declining):

```text
We appreciate the suggestion. We found [the suggested work] addresses [adjacent
problem], which differs from our setting in [specific way], so we did not add it as a
primary comparison. We are happy to include it as related context if the reviewer
prefers.
```

## Major statistical or empirical-rigor critique

The reviewer challenges the evaluation: missing variance, no significance test, an unfair comparison, an unreported seed protocol.

Treat this as high risk until the author supplies details. Request, before drafting:

- the metric and its exact definition
- the number of runs or seeds and how variance is reported
- the comparison protocol (compute-matched, epoch-matched, wall-clock)
- the hardware and software versions when they affect the result
- the table or figure location for any new number

Do not invent variance, p-values, seed counts, or effect sizes. If the author cannot supply them, the label is `AUTHOR_INPUT_NEEDED`, not a fabricated statistic.

## Reproducibility or artifact critique

The reviewer asks for code, a missing hyperparameter, a dataset split, or an artifact for the artifact-evaluation track.

Strategy:

- Map to `ACCEPT_TEXT` (add the missing detail to the paper or appendix), `CLARIFY_EXISTING` (point at where it already is), or `AUTHOR_INPUT_NEEDED` (the author must supply the repo URL, license, or access route).
- Request the repository link, the exact commit or release, the license, and the access route when the author claims an artifact exists.
- Do not fabricate a repository URL, a commit hash, or a license. If the artifact is not ready, defer it as `future_work_only` in the revision plan and say so plainly.

## Appeal-like case: route it out

An appeal is not a revision response. It challenges a rejection rather than improving the paper.

Route the task OUT as a separate effort when any of these holds:

- the user wants to contest a reject decision rather than revise;
- the decision letter invites an appeal path;
- the author alleges reviewer bias, a factual error in the decision, or a process failure;
- no revised manuscript is being prepared.

Do not draft an appeal as the default rebuttal path. The stance, the audience (the editor or program chair, not the reviewers), and the venue rules all differ.

Default response when an appeal is detected:

```text
This reads as an appeal of the decision rather than a point-by-point revision response.
This skill can identify the disputed points and the reviewer concerns behind them, but a
full appeal letter should be handled as a separate task under the venue's appeal rules
(program-chair contact, deadline, and required form). Do you want me to extract the
disputed points now, or set the appeal up as its own task?
```

Surface the routing decision to the user. Do not silently convert a revision request into an appeal or vice versa.
