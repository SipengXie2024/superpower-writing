# Evidence-led wording for systems papers

Use this reference only when `.writing/metadata.yaml` contains `writing_profile: systems`, or when the user explicitly identifies standalone prose as systems-paper prose.

Polish preserves the paper's evidential strength. It may make a supported claim clearer. It must not make an unsupported claim sound supported.

## Preserve unresolved evidence

`[NEEDS-EVIDENCE]` is an unresolved claim marker, not awkward prose.

- Preserve every `[NEEDS-EVIDENCE]` token verbatim and attached to the same claim.
- Do not replace it with a vague hedge, an unrelated number, a section reference, or smoother but more confident wording.
- Do not invent a comparator, condition, measurement, citation, figure, or table to make the sentence read cleanly.
- If required evidence is absent, keep the marker or return a neutral description that does not make the unsupported claim.

A number is not automatically evidence for the surrounding claim. It must measure the stated metric, compare the named alternatives, and come from the stated condition.

## Comparison contract

Words such as `faster`, `lower`, `higher`, `improves`, `reduces`, and `outperforms` require four parts:

1. **Comparator:** what system, baseline, version, or setting is compared.
2. **Metric:** latency, throughput, memory, cost, accuracy, or another named measure.
3. **Condition:** workload, hardware, scale, model, dataset, or tested range needed to interpret the comparison.
4. **Evidence anchor:** an exact number or a relevant figure, table, or citation.

Keep these parts in the same sentence when practical. A nearby figure or table reference is acceptable when the sentence names the comparator, metric, and condition and the display contains the exact comparison.

**Unsupported:**

> Our method is substantially faster.

**Supported:**

> At 32 clients on YCSB-F, our method reduces median latency by 21% relative to Baseline A (Figure~\ref{fig:latency}).

If one of the four parts is unknown, do not guess it. Preserve `[NEEDS-EVIDENCE]` and name the missing part when the user asks for a diagnostic rather than a clean rewrite.

## Magnitude words

`substantial`, `material`, and `considerable` interpret an effect's magnitude. Keep one only when the sentence or its evidence anchor gives the magnitude and the domain supplies a defensible threshold for that judgment.

Otherwise choose one of three actions:

- report the measured delta without the adjective;
- use a neutral observation such as `the measured latency was lower` when the exact delta is already clear nearby;
- preserve `[NEEDS-EVIDENCE]` if the magnitude itself is a load-bearing claim.

Do not strengthen `small`, `modest`, or neutral wording merely to improve cadence.

## Statistical significance

Use `significant` to mean statistically significant only. The claim must name or anchor the test result, such as a p-value, confidence interval, or a predeclared statistical decision rule.

- `statistically significant (p < 0.01)` is valid when the analysis supports it.
- `significantly faster` is invalid when `significantly` only means noticeably or substantially.
- Statistical significance does not establish practical importance. Keep effect size and uncertainty when they are present.

If no statistical test exists, replace `significant` with the measured effect or preserve `[NEEDS-EVIDENCE]`. Do not infer significance from a large sample or a visible gap in a plot.

## Efficiency claims

`efficient` must identify:

- the resource or cost, such as latency, throughput per watt, memory, network traffic, or monetary cost;
- the comparator;
- the tested condition;
- the measurement or evidence anchor.

Theoretical complexity alone does not establish practical efficiency. If the text claims runtime efficiency, retain wall-clock evidence and its hardware and workload conditions. If only asymptotic complexity is known, say that directly.

## Scalability claims

`scalable` must identify:

- the scaling dimension, such as workers, requests, data size, model size, or nodes;
- the tested range;
- the measured response metric;
- the condition and evidence anchor;
- any observed saturation point or untested range that bounds the claim.

Do not turn `performance increased from 1 to 64 workers` into `the system is scalable` unless the evidence supports the intended scaling behavior. State the tested range rather than extrapolating beyond it.

## Novelty claims

`novel`, `new`, `first`, and `unprecedented` are comparisons with prior work. Keep them only when the sentence identifies the specific difference and anchors it in relevant prior-work evidence.

Prefer a concrete contrast:

> Unlike prior systems that compile each contract independently, X shares compiled code across members while preserving per-contract dispatch identity \cite{...}.

Avoid an unsupported label:

> X is a novel compilation framework.

Polish must not create a novelty claim from a contribution claim. If prior-work coverage is incomplete, preserve `[NEEDS-EVIDENCE]` or state the mechanism without claiming novelty.

## Final evidence-preservation pass

After the de-AI and clarity passes, compare the result with the source and confirm:

- every number, unit, uncertainty statement, citation, figure/table reference, and `[NEEDS-EVIDENCE]` token survives verbatim;
- every comparison still names its comparator, metric, condition, and evidence anchor;
- causal and novelty verbs are no stronger than the source evidence permits;
- `significant`, `efficient`, and `scalable` still carry their required scope;
- no smoother sentence has converted an unknown fact into an asserted fact.

When clarity conflicts with evidential precision, preserve evidential precision.