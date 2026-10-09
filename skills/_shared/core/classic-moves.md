# Classic Moves: What Pre-LLM Systems Papers Do in the Body

A rulebook of writing moves distilled from 16 close-read classics and 93 extension papers on systems, databases, programming languages, and consensus, published between 1978 and 2023. They are compared against a group of 112 recent papers (109 from 2025 and 2026, plus 3 from 2023 and 2024). Every quote below is verbatim from the paper named next to it.

The comparison changed what this file claims. Older papers are not uniformly cleaner. Trend openers (`In recent years ...`, `X has become increasingly ...`) and generic-importance openers appear in about two thirds of both groups. Missing limitation sections are about as common (33 percent against 37 percent). What separates the groups is a set of vocabulary words (the measured vocabulary table in the polish skill's AI-tells reference) and a set of moves in the body: how losses are reported, how a number is explained, how the obvious alternative is refuted, how one example carries a paper. Imitate the moves, not the era.

## Contents

- Precedence and scope
- Overrides of house style §3.2, §3.4, and style-cautions Lesson 2
- M1 Report losses next to wins
- M2 Give the expectation before the measurement
- M3 Refute the reader's obvious alternative
- M4 Carry one small example through the paper
- M5 State what a comparison can and cannot show
- M6 Check every absolute word against your own evaluation
- M7 Label each claim by the kind of evidence behind it
- M8 Write limitations with a trigger, a size, and what still holds
- M9 Criticize prior work with its own numbers
- M10 Define terms by a checkable condition
- M11 Match contribution verbs to evidence
- M12 Open on the problem, not on a trend
- Classic alternatives not adopted (house style §8 wins)

## Precedence and scope

1. A project style file (`.claude/CLAUDE.md`, `AGENTS.md`) wins, as in the house style.
2. House style §8 (the senior co-author's observed conventions) outranks this file everywhere. Where a classic move and §8 disagree, follow §8; the last section lists those cases.
3. This file outranks house style §1 to §7 only on the three points under Overrides. On every other point it adds to the house style and does not replace it.
4. Evidence rules outrank everything here. A move never licenses a claim the evidence does not support, and `[NEEDS-EVIDENCE]` markers survive.

`drafting` reads this file before the first section, alongside the house style. `polish` applies it in pass 3 (evidence-led wording), since most moves match a claim to its evidence.

## Overrides of house style §3.2, §3.4, and style-cautions Lesson 2

These three relaxations were approved by the user. Each states exactly what it permits; the rest of the overridden rule still holds.

**O1. A labelled belief with a reason is not defensive prose (relaxes §3.2 and §3.4).** `We believe ... because ...` marks a proposition as a judgment and gives the reader its ground. Keep it. Delete it only when no reason follows.

- PBFT (OSDI 1999): "We believe that Byzantine-fault-tolerant algorithms will be increasingly important in the future because malicious attacks and software errors are increasingly common and can cause faulty nodes to exhibit arbitrary behavior."
- Still banned: a belief with no reason, as in KILO TM (MICRO 2011), "We believe the area overhead of a transaction log unit is negligible."

**O2. A plain negative scope statement is not rebuttal register (relaxes §3.4).** A one-clause statement of what the paper does not model or claim is a fact about scope. §3.4 still bans prose that narrates the authors' own candor (`we state this honestly`, `our claim is narrow and defensible`).

- Paxos Made Simple (2001): "In an implementation, a single process may act as more than one agent, but the mapping from agents to processes does not concern us here."
- Determinator (OSDI 2010): "We make no claim that these are the only areas in which current operating systems introduce nondeterminism, but they are the aspects we found essential to address in order to build a working, pervasively deterministic OS."
- A priority claim stays bounded: `to our knowledge` plus the narrow category, as in DPJ (OOPSLA 2009), "We are not aware of any statically checked type system that provides this capability." An unbounded `first` is still rejected.

**O3. The cost of the design belongs in the abstract (clarifies style-cautions Lesson 2).** Lesson 2 bans dataset names in thesis sentences. It does not ban naming the failure scenario or workload where the design pays. That is a property of the design, not a dataset pre-hedge.

- Dynamo (SOSP 2007): "To achieve this level of availability, Dynamo sacrifices consistency under certain failure scenarios."
- Doppel (OSDI 2014): "Its throughput is up to 38× higher than conventional concurrency control protocols on microbenchmarks, and up to 3× on a larger application, at the cost of increased latency for some transactions."

## M1 Report losses next to wins

Put your number and the baseline's number in the same sentence, even when the baseline wins. Give the condition, the rival, the gap, and the component of your system that causes the gap. Report the crossover point, not only the maximum.

- Grace (OOPSLA 2009): "The average speedup for Grace is 6.2X, while the average speedup for pthreads is 7.13X."
- Plor (SIGMOD 2022): "Plor achieves 25% to 42% higher peak throughput than that of 2PL schemes, and only underperforms OCC-based approaches by 9% (for Silo) and 19% (for TicToc)."
- Detock (SIGMOD 2023), rival as subject, condition first, own component as cause: "When MP and MH are 0, SLOG scales better than Detock due to the overhead of the background thread in Detock which periodically scans the dependency graph for deadlocks."
- KILO TM (MICRO 2011), the loss against the strong baseline first in the abstract: "KILO TM captures 59% of the performance of fine-grained locking, and is on average 128× faster than executing all transactions serially".

Check: every evaluation subsection that reports a win either reports the configuration where the system loses or ties, or states that no such configuration was found in the tested range.

## M2 Give the expectation before the measurement

Before a result, give the reader something to judge it against: a model, a bound, a cost count from the design section, or a stated prediction. Then report the result as matching or departing from it, and explain any departure. Under house style §8.20, research questions stay plain questions; put the expectation in the setup or the subsection text.

- Crystal (SIGMOD 2020): "Given the general notion that database operators are memory-bandwidth bound, one would expect the maximum gain to be roughly equal to the ratio of the memory bandwidth of GPU to that of CPU."
- Revisions (OOPSLA 2010): "Thus, even if everything else took zero time our speedup could not be better than 2.6 ∗ 100/95.5 = 2.72."
- GPU MVB-tree (PACT 2022), the evaluation pointing back to the design's count: "We expect out-of-place insertion to be slower as it performs at least two writes instead of one for the typical case of inserting into a leaf node."
- An unexplained departure is labelled, Revisions again: "We are not sure why, but observe an unexpected slowness of the render task for which we believe some form of contention (outside of our runtime library) to be responsible."

Check: (a) the first number in each evaluation subsection has a reference point stated earlier; (b) every cost count or inequality in the design section is referred to at least once in the evaluation.

## M3 Refute the reader's obvious alternative

Before the first mechanism, name the simplest solution the reader is already thinking of, concede where it suffices, give its concrete cost, and name the root cause your design removes.

- Lotus (PVLDB 2022): "One might be tempted to shard the database into more partitions to get more concurrency. While it seems intuitive and simple, this has two major problems." Then: "The root cause of these problems is that the sharding approach tightly couples physical data distribution with concurrency control. Our approach decouples the two."
- Solythesis (PLDI 2020): "One naive approach to enforce the invariant is to just instrument the runtime checks at the end of each transaction."

Check: within three sentences of naming the alternative, the text gives a number, a complexity, or a counterexample. `Existing approaches are inefficient` does not pass.

## M4 Carry one small example through the paper

Pick one example small enough to compute by hand. Introduce the problem with it, instantiate each definition on it with concrete values, and show the naive rule failing on it.

- Transactional Boosting (PPoPP 2008): "Consider a set whose state is {1, 3, 5}. Transaction A is about to add 2 to the set and transaction B is about to add 4."
- Homeostasis (SIGMOD 2015), a definition instantiated at once: "In our example, the global treaty is the statement “the current minimal value in the top-k is 91”."
- Bounded Counter (SRDS 2015), a one-sentence correctness argument on the same numbers: "if the decrements of each replica are less or equal to 10, it follows that the total number of decrements does not exceed 30, and therefore the invariant is preserved."

Check: the introduction's example reappears in the design section and at each new definition.

## M5 State what a comparison can and cannot show

In the evaluation setup, answer: how the benchmarks were selected and what was dropped; where each baseline came from and whether it was tuned; why a well-known baseline is absent; which variables are held fixed; whether each key number is measured, estimated, an upper bound, or a lower bound. These are facts about the experiment, which §3.4 permits.

- Parrot (SOSP 2013): "We used complete software or benchmark suites to avoid biasing our results."
- Transactional Boosting: "Because they use the same base object, difference in throughput can be attributed entirely to differences in parallelism."
- Flash Boys 2.0 (S&P 2020): "They represent lower bounds on arbitrage behavior."
- DRP (EuroSys 2019): "Note that this is not a fair comparison because IC3 assumes full knowledge of the workload whereas DRP does not."

Check: every number reported against another paper's figures is labelled rough and lists the hardware or setup differences.

## M6 Check every absolute word against your own evaluation

List each absolute or universal word in the abstract and conclusion (all, every, always, never, without, no overhead, no loss, no degradation, negligible, seamless, consistently, in all cases). Search the evaluation for a counterexample. If one exists, replace the word with the condition or the measured range. Keep `negligible` or `minimal` only when a number follows.

- BEAT (CCS 2018) abstract: "all our BEAT instances significantly outperform, in terms of both latency and throughput, HoneyBadgerBFT". Its own evaluation: "when batch size is higher than 5000, all the three protocols have 20% to 30% lower throughput than HoneyBadgerBFT."
- Dynamic BFT (S&P 2022) abstract: "without incurring performance degradation". Its own evaluation: "the throughput downgrades from 50 ktx/s on average to around 30 ktx/s, a 40% degradation."

A hedging word does not repair an absolute one: `roughly all` is still all.

## M7 Label each claim by the kind of evidence behind it

Use a different word for a proved result, a measured result, an argued claim, a hypothesis, and an untested explanation, and keep the label identical wherever the claim recurs (abstract, introduction, conclusion).

- Not proven: "It is likely (but not proven in this work) that our model fits within an extension of their incentive compatibility framework." (Multidim Fee Markets, AFT 2023)
- Hypothesis tested later: "Therefore, our hypothesis is that the overhead of runtime validation, which is often too expensive for other domains, is in fact negligible for smart contracts." (Solythesis)
- Conjecture: "we conjecture that it cannot be provided efficiently without hardware support." (Kendo, ASPLOS 2009)
- Untested explanation: "We believe but have not yet verified … reason is false sharing." (Dthreads, SOSP 2011)

Check: a `first` or `to our knowledge` claim carries the same qualifier in every place it appears.

## M8 Write limitations with a trigger, a size, and what still holds

Each limitation names the workload or condition that triggers it, the size of the effect, and what the design still keeps. Under house style §8.27 the discussion carries no measured numbers, so put the measurement in the evaluation or an appendix and refer to it.

- Aria (PVLDB 2020) measures its own weakness: "In the extreme scenario when only a single transaction has a 20 ms delay (i.e., a single straggler), the slowdown is about 81%."
- Dthreads, what still holds: "D THREADS is unable to maintain high performance for some applications whose characteristics prevent it from amortizing its costs, but it still outperforms the previous state-of-the-art deterministic system by between 20% and 11.2×."
- Determinator separates fundamental from incidental: "None of these limitations are fundamental to Determinator’s programming model."

## M9 Criticize prior work with its own numbers

Under house style §8.27, related work gives one sentence on what a system does and one on how the paper differs. Make the second sentence carry a mechanism or a cost, computed from the rival's own reported figures where possible, and concede where the rival is stronger.

- LVMT (OSDI 2023): "RainBlock reports the average size of witnesses per transaction is 4 KB and their optimizations reduce the size of witnesses by 95% , so the additional network message per transaction is about 200 bytes, two times of a transaction."
- NCC (OSDI 2023): "When transactions are not naturally consistent, however, these techniques could outperform NCC."
- Rejected: "our techniques are different from and complementary to previous work" (Batching, PVLDB 2018), which names no mechanism.

## M10 Define terms by a checkable condition

Describe the phenomenon first, then name it. Give the definition as a condition the reader can test, or as `identical to <known construct>, except <one difference>`. Instantiate it on the running example (M4).

- Coordination Avoidance (VLDB 2015): "if an application’s operations are I-confluent, a database can correctly execute them without coordination."
- Chiller (SIGMOD 2020): "We refer to the time span between acquisition and release of a record lock as the record’s contention span".
- DPJ-nd (POPL 2011): "This construct is identical to foreach in basic DPJ [17], except it says explicitly that conflicting accesses, and therefore potential nondeterminism, are allowed between the loop iterations of foreach nd."

## M11 Match contribution verbs to evidence

Use a different verb for each kind of contribution, and let the verb's strength match the evidence: describe for examples, define for formal models, demonstrate for implementations, argue for benchmark-based applicability. A diagnosis can be a contribution; so can a negative finding.

- BoC (OOPSLA 2023): "We define it through a formal model. We demonstrate its practicality by implementing a C++ runtime. We argue its applicability through the Savina benchmark suite".
- Baldur (VDBS 2023), a modest gain reported as such: "These improvements are rather modest and the root cause is the high latency of the verification step on the accelerator."

## M12 Open on the problem, not on a trend

The first sentence of the abstract and of the introduction states an observable failure, a property readers assume but that does not hold, or a cost with its magnitude. It does not say that a field is growing, popular, critical, or recent. Measured across both groups, introductions are where this fails most: 43 of 93 introduction first sentences were specific in the extension group (against 65 of 93 abstract first sentences), and 47 of 112 in the recent group (against 68 of 112).

- Doppel (OSDI 2014): "Multicore main-memory database performance can collapse when many transactions contend on the same data."
- CoreDet (ASPLOS 2010): "The behavior of a multithreaded program does not depend only on its inputs."
- Rejected (TCHES 2023): "Zero-knowledge proof is a critical cryptographic primitive."

A heuristic with weaker support: human-written papers vary their density, with loose sentences that bring the reader in and tight sentences the reader must remember. If no sentence in a paragraph stands out as the one to remember, the paragraph is probably flat.

## Classic alternatives not adopted (house style §8 wins)

These classic patterns conflict with the co-author's conventions in house style §8. Follow §8. They are listed so a reviewer of the plugin can see the choice was deliberate.

| Classic pattern | Example | Follow instead |
|---|---|---|
| Evaluation ends with numbered takeaways, or each RQ closes with a results box | Batching (PVLDB 2018); SolType (POPL 2022) | §8.21: no Takeaways subsection; synthesis goes to the discussion |
| Research questions carry their expected answers | Peregrine (SOSP 2011) | §8.20: plain questions; expectations go in the setup or subsection text (M2) |
| Several sentences per closest rival in related work | LVMT, RapidChain (CCS 2018) | §8.27: one sentence each; the second carries the mechanism or cost (M9) |
| Limitations in the discussion carry their numbers | Aria | §8.27: numbers live in the evaluation or appendix (M8) |
| Conclusion keeps a conditioned negative finding or a usage recommendation | Bounded Counter (SRDS 2015); RTIndeX (VLDB 2023) | §8.12: about four sentences and one headline result |
