---
section: introduction
stem: 01_introduction_examples
framework: CARS (companion examples)
---

# Introduction Examples: Annotated LaTeX Skeletons by Framing Strategy

Companion to `01_introduction.md`. The CARS standard fixes the Move skeleton (M1 Territory, M2 Niche, M3 Occupy). This file shows four concrete framing strategies for arranging that skeleton, each as an annotated LaTeX skeleton with inline example lines. Pick the strategy that fits the paper, then fill the slots. All examples target CS / systems / ML venues (NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP, VLDB). The example prose is illustrative scaffolding, not real claims; do not paste it verbatim and do not treat its numbers as data.

The strategies differ only in M1 framing and the M2→M3 hand-off. The `% cars:` and `% claim:` tags still apply exactly as in `01_introduction.md`: every load-bearing paragraph carries both. The contributions list still obeys the 3–5-item, noun-phrase-heading, section-pointer rules.

**One rule cuts across all four strategies.** Lead the `[O]` paragraph with the insight and the mechanism. Do NOT open it by sketching a naive baseline and framing the paper as a delta over it. The naive-solution-then-improvement move makes the work read as a low-score incremental patch (see `01_introduction.md` failure modes). The technical challenge and why a naive extension fails belong in `[N]`; `[O]` opens with what the paper actually does.

## Contents

- [Strategy 1: Task-then-application](#strategy-1-task-then-application)
- [Strategy 2: Application-first](#strategy-2-application-first)
- [Strategy 3: Novel task](#strategy-3-novel-task-challenging-for-three-reasons)
- [Strategy 4: Observation-driven](#strategy-4-observation-driven)
- [NOT recommended: abstract-only novelty illusion](#not-recommended-abstract-only-novelty-illusion)

## Strategy 1: Task-then-application

Use when the task itself is niche or unfamiliar. Define the task first, then its applications. Best for new task settings the reader has not seen named before.

```latex
\section{Introduction}
\label{sec:introduction}

% cars: T
% claim: intro-c1
% Define the task in one sentence: what output from what input.
\emph{Streaming join reordering} rewrites a multi-way stream join's operator
order at runtime to minimize intermediate-state size. It has applications in
real-time fraud detection, network telemetry, and clickstream analytics
\cite{ref-a,ref-b,ref-c}.

% cars: T
% claim: intro-c2
% Prior work review: the dominant approach, cited by name.
Prior engines fix the join order at query-compile time \cite{ref-d}. Adaptive
variants re-plan on a timer \cite{ref-e}, but treat the operator graph as static
between re-plans.

% cars: N
% claim: intro-c3
% Niche: name both T-side subjects whose mismatch is the gap (no demonstrative anaphor).
% This is the right place for the technical challenge and why naive extension fails.
The mismatch between compile-time join orders and the skew of live stream rates
has not been posed as a runtime-scheduling problem. Re-planning on a timer reacts
too slowly when a burst inflates one input's selectivity within a single window.

% cars: O
% claim: intro-c4
% Occupy: open with the insight and mechanism, NOT a strawman baseline.
We present \textsc{ReFlow}, which reorders join operators per window using a
state-size estimator computed from the prior window's cardinalities. The estimator
gives each candidate order a cost in one pass, so reordering tracks rate skew at
window granularity rather than on a fixed timer.

% cars: O
% claim: intro-c5
Our contributions are as follows:
\begin{itemize}
  \item \textbf{Per-window reordering:} a runtime scheduler that re-orders a
        multi-way stream join every window from observed cardinalities.
        (\S\ref{sec:method})
  \item \textbf{Single-pass cost estimator:} a state-size estimate computable
        in one pass over the prior window. (\S\ref{sec:estimator})
  \item \textbf{Evaluation on three workloads:} a substantial reduction in peak
        intermediate state over the timer-based baseline. (\S\ref{sec:results})
\end{itemize}
```

## Strategy 2: Application-first

Use when the task is already familiar to the venue's readers. Skip the formal definition and open with why the application matters, then narrow to the specific setting. Common at venues where the task is a known quantity.

```latex
% cars: T
% claim: intro-c1
% Open with application importance; the task needs no formal definition here.
Large-language-model inference now dominates the serving cost of deployed
assistants \cite{ref-f}. Batching requests raises throughput, but tail latency
governs whether an interactive deployment meets its service objective.

% cars: T
% claim: intro-c2
% Narrow to the specific setting and the dominant prior approach.
Continuous batching \cite{ref-g} admits new requests mid-batch to raise GPU
utilization. It schedules by arrival order and does not account for a request's
remaining decode length.

% cars: N
% claim: intro-c3
% Niche: name both T-side subjects (arrival-order scheduling vs. remaining length).
The mismatch between arrival-order admission and the heavy-tailed distribution of
remaining decode lengths inflates tail latency. A long generation admitted late
blocks short requests behind it for the rest of its decode.

% cars: O
% claim: intro-c4
% Lead with the mechanism.
We present \textsc{TailSched}, a length-aware admission policy that predicts
remaining decode length from the prompt and admits short requests preferentially
under load. The predictor is a small head over the prompt encoder, so admission
stays per-step without adding a model call.
```

## Strategy 3: Novel task, "challenging for three reasons"

Use for a genuinely new task with no direct prior methods. State the goal, then decompose the difficulty into independent challenge points with `First / Second / Finally`. Each point states an observable obstacle and its technical reason. This framing pre-empts the reviewer question "is this task even hard?" and seeds the one-to-one challenge→module mapping.

```latex
% cars: T
% claim: intro-c1
% State the goal and the real-world stakes.
We study \emph{single-trace kernel attribution}: identifying which GPU kernel
caused a latency spike from one production trace, without a controlled replay.
Operators need this to triage regressions on live clusters \cite{ref-h}.

% cars: N
% claim: intro-c2
% Novel-task niche: state the goal, then decompose into independent challenges.
% Each challenge names an observable obstacle AND its technical reason.
Attributing a spike from a single trace is challenging for three reasons.
First, we observe only one trace, so we cannot average out noise the way
replay-based profilers do; the signal per kernel is sparse. Second, kernels
overlap on independent streams, so wall-clock boundaries do not isolate a single
kernel's contribution. Finally, the attribution target is probabilistic: the same
kernel sequence yields different spike patterns across runs, so we must estimate a
distribution over causes, not a single label.

% cars: O
% claim: intro-c3
% Each challenge maps one-to-one to a module. Open with the mechanism.
We present \textsc{Attrib}, which addresses these three challenges with three
components: a sparse-signal estimator that pools evidence across the single
trace's repeated kernels, a stream-aware deconvolution that separates overlapping
kernels, and a probabilistic attribution head that returns a posterior over
candidate causes.

% cars: O
% claim: intro-c4
% Contributions mirror the modules one-to-one; each cites a section.
Our contributions are as follows:
\begin{itemize}
  \item \textbf{Single-trace attribution task:} a formulation that requires no
        controlled replay. (\S\ref{sec:problem})
  \item \textbf{Three-component attributor:} sparse-signal pooling,
        stream-aware deconvolution, and a probabilistic attribution head, one per
        challenge above. (\S\ref{sec:method})
  \item \textbf{Evaluation on production traces:} attribution accuracy well above
        the wall-clock-boundary baseline. (\S\ref{sec:results})
\end{itemize}
```

## Strategy 4: Observation-driven

Use when the contribution flows from one concrete empirical observation. State the key innovation first, then a listener-friendly observation that motivates it, then the mechanism. Best when the observation is intuitive once stated and the reader's reaction is "of course".

```latex
% cars: T
% claim: intro-c1
Mixture-of-experts layers cut inference FLOPs by routing each token to a few
experts \cite{ref-i}. Serving them is bottlenecked by expert load imbalance: a few
experts receive most tokens and stall the batch.

% cars: N
% claim: intro-c2
% Niche names both sides: static routing vs. shifting token distribution.
The mismatch between routing weights learned at training time and the shifting
token distribution at serving time concentrates load on a handful of experts.
Re-balancing by dropping tokens degrades quality.

% cars: O
% claim: intro-c3
% Lead with the innovation, then the observation that motivates it.
Our key idea is to replicate hot experts at serving time rather than reroute
tokens. We observe that the set of overloaded experts is stable across thousands
of consecutive steps, so a cheap replication decision amortizes over a long
horizon. \textsc{HotRep} tracks per-expert load and replicates an expert once its
load crosses a threshold, leaving routing untouched and quality intact.
```

## NOT recommended: abstract-only novelty illusion

The skeleton below is an anti-example. Do NOT write the `[O]` paragraph this way. It hides the concrete method behind abstract framing and a cloud of new terms, so the work sounds novel without the reader ever learning what it does. Reviewers read this as shallow or incremental.

```latex
% cars: O
% claim: intro-cX   % ANTI-EXAMPLE: do not ship this paragraph
% PROBLEM 1: no mechanism, only abstract insight.
% PROBLEM 2: coins new terms ("synergistic alignment", "holistic fusion")
%            without defining how any of them is computed.
% PROBLEM 3: a naive reader cannot re-derive even a sketch of the method.
We propose a novel paradigm-shifting framework that achieves synergistic
alignment between modalities through a holistic fusion mechanism, enabling
unprecedented generalization across tasks. Our approach reconceptualizes the
representation learning problem and delivers state-of-the-art results.
```

Why it fails:

- It presents only abstract insight with no concrete pipeline steps, so technical clarity collapses. A reader cannot tell what is actually computed.
- It introduces several new terms without any mechanism-level explanation, manufacturing a novelty illusion. Naming is not contributing.
- Marketing adjectives ("paradigm-shifting", "unprecedented") stand in for evidence. Strip them; let the mechanism and the numbers speak.

The fix is the rule that opens this file: lead `[O]` with the insight and the concrete mechanism, the way Strategies 1–4 do. A simple method described plainly beats a simple method dressed up as profound; reviewers reward clarity and punish the dress-up.

## Note on "to the best of our knowledge, this is the first ..."

Avoid the construction "To the best of our knowledge, this is the first work to ...". It is unverifiable and often false. Reviewers who know one prior counterexample will fixate on it, and the whole contribution paragraph loses credibility over one sentence. Position novelty against the specific prior work the paper actually improves on, not against the entire literature. Replace the blanket first-ever claim with a concrete differentiator:

- Weak: ``To the best of our knowledge, this is the first system to reorder stream joins at runtime.''
- Strong: ``Unlike timer-based adaptive engines \cite{ref-e}, \textsc{ReFlow} reorders per window from observed cardinalities.''

The strong form is checkable, survives a reviewer who knows the literature, and states exactly what changed. The same applies to "novel", "unprecedented", and "first-of-its-kind": a precise comparison to a named baseline is both more defensible and more informative than a superlative.
