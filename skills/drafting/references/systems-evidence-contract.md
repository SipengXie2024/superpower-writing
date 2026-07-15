# Systems Evidence Contract

Use this reference in two layers:

- The structured `analysis` and `artifact` evidence rules apply to every paper, regardless of `writing_profile`.
- The Results, Discussion, and figure rules apply only when `.writing/metadata.yaml` sets `writing_profile: systems`.

Before using any profile-specific rule, read `.writing/metadata.yaml`. If `writing_profile` is missing or `TODO`, stop, ask the user to choose `systems` or `default`, write the answer back, and then continue. Do not infer the profile from `reporting_guideline: none` or from manuscript wording.

## Structured analysis evidence

Use `type: analysis` only for a computed statistic or a deterministic transformation of identified inputs.

```yaml
- type: analysis
  description: Median p99 latency reduction at 32 clients
  inputs:
    - .writing/figures/data/fig-latency.csv
  calculation: >-
    python .writing/figures/src/fig-latency.py --summary-only
  conditions:
    - workload: YCSB-F
    - hardware: 2x AMD EPYC 9654
    - load: 32 clients
    - aggregation: median over 5 independent runs
  unit: ms
  uncertainty:
    kind: 95% CI
    basis: bootstrap over 5 runs
```

Every entry requires:

- `description`: the result the analysis produces.
- `inputs`: a non-empty list of paths, dataset versions, or artifact identifiers.
- `calculation`: an executable command, formula, or explicit transformation. Phrases such as `analyzed data` are insufficient.
- `conditions`: a non-empty list covering the workload, hardware, model, range, baseline, aggregation, or other conditions that affect interpretation.
- `unit`: the reported unit. Use `dimensionless` for ratios without a unit and `count` for counts.
- `uncertainty`: a mapping that gives both `kind` and `basis`, or explicitly explains why uncertainty does not apply.

A deterministic complete count may use:

```yaml
uncertainty:
  kind: not_applicable
  reason: Exact count over the complete immutable snapshot
```

`kind: not_applicable` without a non-empty `reason` is incomplete. Any other `kind` requires a non-empty `basis`.

At `STATUS: stub`, an unknown source field may temporarily be the exact string `"[NEEDS-EVIDENCE]"`. Before a claim advances to `evidence_ready`, every required field must have its final value and no analysis source field may contain `[NEEDS-EVIDENCE]`, including values nested inside lists or mappings. Fresh claim verification applies the same rule to both new and legacy claims.

## Artifact evidence

Use `type: artifact` for a first-party implementation, specification, configuration, protocol, proof, or pseudocode source. Do not use it for a computed statistic or as a substitute for an external citation.

```yaml
- type: artifact
  ref: src/scheduler.rs
  locator: Scheduler::select
  role: implementation
```

Rules:

- `ref` is required and must identify a readable file or directory inside the paper project.
- Resolve relative `ref` values from the paper project root, which is the parent of `.writing/`. Normalize the path before checking it. A path that resolves outside that root fails, even if the target exists.
- URLs and other external identifiers fail. Use `type: citation` for external material.
- `role` is required and must be one of `implementation`, `specification`, `configuration`, `protocol`, `proof`, or `pseudocode`.
- `locator` may name a symbol, section, line range, configuration key, or artifact member. It is required when `ref` names a directory or a file too large to inspect as one focused read.
- For a text file, verification checks that the locator text occurs or that a stated line range exists. For a directory, verification checks that the named member exists. For other readable artifacts, verification records existence and leaves locator interpretation to manual review.

Artifact verification proves only that the first-party material and, when applicable, its locator are present. It does not prove that the material is correct or that it substantively supports the claim. Record that judgment as a manual review item before marking the claim verified.

## Systems Results paragraphs

A systems Results paragraph uses this order:

1. **Qualitative answer.** Answer the research question in the first sentence.
2. **Condition and evidence.** State the workload, platform, range, or other conditions, then give the figure or table reference and exact comparison.
3. **Boundary or exception.** State where the result holds, where it stops holding, or any negative result.
4. **Direct implication, optional.** Include only a local implication entailed directly by the reported data.

A direct implication is allowed when the measurement itself supports it:

> The invariant share is 93.06%, so treating these bytes as compile-time constants matches the common case in this corpus.

Do not put an unsupported mechanism claim in Results:

> The speedup occurs because cache reuse eliminates synchronization.

The second sentence needs mechanism evidence and belongs in Discussion.

## Systems Discussion interpretation paragraphs

An Interpretation paragraph uses this order:

1. **Result anchor.** Point to the relevant research question, figure, or table without repeating the full result set.
2. **Mechanism evidence.** Cite an ablation, diagnostic, trace, or prior study.
3. **Causal explanation.** Match the verb to the evidence strength: `shows`, `suggests`, or `we hypothesize`.
4. **Implication and boundary.** State the design consequence and the limit of the explanation.

Without mechanism evidence, keep the explanation as a hypothesis and state what evidence is still needed. Do not turn correlation into a cause.

## Systems figure brief

Create `.writing/figures/<fig_id>.brief.yaml` before drawing or dispatching any systems figure. The brief complements, rather than replaces, route-specific TikZ specifications or plotting scripts.

```yaml
figure_id: fig-scaling
question: How does throughput scale with worker count?
claim: res-c3
sources:
  - type: data
    ref: .writing/figures/data/fig-scaling.csv
conditions:
  workload: production trace snapshot 2026-06
  hardware: 2x AMD EPYC 9654
  range: 1-64 workers
  aggregation: median over 5 independent runs
family: scaling-small-multiples
order:
  - ours
  - baseline-a
  - baseline-b
encoding:
  primary: line style plus marker
  grayscale_redundancy: solid-triangle / dashed-square / dotted-circle
  semantic_color: none
caption_facts:
  - axes and units
  - method order
  - workload and hardware
  - n=5 and 95% CI
interpretation_location: body
route: scientific-visualization
```

Required fields are `figure_id`, `question`, `claim`, `sources`, `conditions`, `family`, `order`, `encoding`, `caption_facts`, `interpretation_location`, and `route`.

- `question` states one primary analytical question.
- `claim` names one primary claim ID.
- `sources` is a non-empty list. Each item has `type` in `data`, `artifact`, or `citation`, plus `ref`. A data figure includes at least one `data` source. A structural figure includes at least one `artifact` or `citation` source.
- `conditions` is a non-empty mapping. Record experimental conditions for data figures and scope, trust domain, or protocol phase for structural figures.
- `order` fixes the method, panel, stage, or lane order.
- `encoding` records the primary encoding and redundant grayscale encoding where methods are compared.
- `caption_facts` lists the facts the caption must define.
- `interpretation_location` is always `body`.
- `route` is one of `tikz-figures`, `scientific-visualization`, or `scientific-schematics`.

Built-in families and default routes:

| Analytical question | `family` | Default route |
|---|---|---|
| What is the architecture or trust boundary? | `layered-architecture` | `tikz-figures` |
| How do phases overlap over time? | `overlap-timeline` | `tikz-figures` |
| Where is time or cost spent? | `breakdown-bars` | `scientific-visualization` |
| How do methods scale across models or workloads? | `scaling-small-multiples` | `scientific-visualization` |
| Which parameter region works? | `parameter-heatmap` | `scientific-visualization` |
| How does cost grow across orders of magnitude? | `log-cost-curve` | `scientific-visualization` |

`family: other` requires `family_reason`. A route that differs from the family default requires `route_reason`. `scientific-schematics` is allowed only when the design direction is unresolved and needs exploration, or when the user explicitly chooses final PNG output.

Venue rules override reference widths, fonts, and colors. Record each override in an optional `venue_overrides` list.

Correctness and property-preservation tables remain editable LaTeX `booktabs` tables. They follow the same claim, conditions, units, sample-size, uncertainty, and caption-fact principles, but they do not receive a figure ID or figure brief.

## Visual and caption rules

For result comparisons, distinguish methods in grayscale before adding color. Use line style, marker, fill, or hatch redundantly. Small multiples share axis ranges, method order, and one legend. Heatmaps share a fixed normalization and colorbar and do not use rainbow palettes. Check every figure at its final single- or double-column size.

For architecture and timeline figures, use a left-to-right primary path unless the protocol requires another direction. Express structure through lanes, boundaries, labels, line styles, and spatial groups. Color may track a small number of semantic roles across stages. A clear, routine structural figure defaults to TikZ.

A caption must identify what is shown and define axes, units, conditions, sample size, uncertainty, symbols, abbreviations, and error bars as applicable. It may state a directly visible fact or exact comparison. Put causal explanations and broader implications in the body near the first substantive reference.

## Failure behavior and compatibility

- Missing analysis provenance keeps the claim at `stub` and blocks fresh verification. Report the exact missing fields; never fill them by inference.
- `uncertainty.kind: not_applicable` without `reason` is incomplete.
- Missing or out-of-root artifact references fail structural verification. Artifact presence never establishes content correctness.
- A missing required figure-brief field stops figure dispatch and reports the exact field.
- A data figure without source data stops. Placeholder data is allowed only for a user-requested layout mock-up and must be labeled prominently.
- `family: other` without `family_reason`, or a non-default route without `route_reason`, stops routing.
- Venue rules take precedence and are recorded in `venue_overrides`.
- Keep uncertain semantic judgments for manual review; do not convert them into a machine PASS.
- Do not rewrite legacy claim status in bulk. On fresh verification, an old `analysis` or `artifact` entry that fails this contract receives a failing current report. The historical status remains unchanged until the user approves a later valid transition.
- Existing figures gain a brief when next modified, redrawn, or reviewed. Do not delete an existing figure merely because its brief is absent.
