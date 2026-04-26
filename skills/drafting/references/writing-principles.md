# Writing Principles

Reference for drafting and revising systems/ML prose. Covers principles only; section-specific tense rules live in `section-standards/*.md`, style anti-patterns in `style-cautions.md`, and venue conventions in `submission/references/venue-styles.md`.

## Three Pillars

### Clarity

Writing that is immediately understandable to the intended audience without ambiguity or confusion. Science is complex enough without unclear writing adding confusion. Readers should focus on understanding the science, not deciphering the prose.

**Use precise, unambiguous language:**

```
Poor: "The optimization seemed to help quite a few queries."
Better: "The optimization reduced p99 latency in 68% (32/47) of queries."
```

**Define technical terms at first use:**

```
"We measured tail latency at the 99th percentile (p99), the response time
below which 99% of requests complete."
```

**Maintain logical flow within and between paragraphs:**

- Each paragraph should have one main idea
- Topic sentence introduces the paragraph's focus
- Supporting sentences develop that focus
- Transition sentences connect paragraphs

**Use active voice when it improves clarity:**

```
Passive (less clear): "The traces were analyzed by the authors."
Active (clearer): "We analyzed the traces."
```

Passive voice is acceptable and often preferred in Methods when the action is more important than the actor:

```
"Request traces were collected at the load balancer over a 24-hour window."
```

**Break up long, complex sentences:**

```
Poor: "The results of our evaluation, which involved 200 queries executed
against three index configurations and measured over 12 hours with sampling
every 60 seconds using hardware performance counters, showed significant
improvements in the adaptive-index group."

Better: "Our evaluation involved 200 queries executed against three index
configurations. We measured performance over 12 hours, sampling every 60
seconds using hardware performance counters. The adaptive-index configuration
showed significant improvements."
```

**Use specific verbs:**

```
Weak: "The study looked at tail latency in microservices."
Stronger: "The study examined factors contributing to tail latency in
microservices."
```

### Conciseness

Expressing ideas in the fewest words necessary without sacrificing clarity or completeness. Concise writing respects readers' time. Every unnecessary word is a missed opportunity for clarity and impact.

**Eliminate redundant words and phrases:**

| Wordy | Concise |
|-------|---------|
| "due to the fact that" | "because" |
| "in order to" | "to" |
| "it is important to note that" | [delete] |
| "a total of 50 nodes" | "50 nodes" |
| "completely eliminate" | "eliminate" |
| "has been shown to be" | "is" |
| "in the event that" | "if" |
| "at the present time" | "now" or "currently" |
| "conduct an investigation into" | "investigate" |
| "give consideration to" | "consider" |

**Avoid throat-clearing phrases:**

```
Wordy: "It is interesting to note that the results of our evaluation
demonstrate that..."
Concise: "Our results demonstrate that..." or "The results show that..."
```

**Use strong verbs instead of noun+verb combinations:**

| Wordy | Concise |
|-------|---------|
| "make a decision" | "decide" |
| "perform an analysis" | "analyze" |
| "conduct an evaluation" | "evaluate" |
| "make an assessment" | "assess" |
| "provide information about" | "inform" |

**Eliminate unnecessary intensifiers:**

```
Wordy: "The results were very significant."
Concise: "The results were significant." (the p-value conveys the degree)
```

**Avoid repeating information unnecessarily:**

```
Redundant: "The results showed that queries in the optimized group, which
received the optimization treatment, had lower latency."
Concise: "The optimized group had lower latency."
```

**Favor shorter constructions:**

```
Wordy: "In spite of the fact that the dataset was small..."
Concise: "Although the dataset was small..."
```

Not all long sentences are bad. A sentence with many elements is fine when each element is necessary information (e.g., a full experimental setup description). The key question: can any word be removed without losing meaning or precision? If yes, remove it.

### Accuracy

Precise, correct representation of data, methods, and interpretations. Scientific credibility depends on accuracy. Inaccurate reporting undermines the entire scientific enterprise.

**Report exact values with appropriate precision:**

```
Poor: "The throughput was about 25K."
Better: "The throughput was 24.7K +/- 3.2K ops/s (SD)."
```

**Match precision to measurement capability:**

```
Inappropriate: "Mean latency was 45.237 ms" (implies false precision)
Appropriate: "Mean latency was 45.2 ms"
```

**Use consistent terminology throughout:**

```
Inconsistent: Introduction calls it "garbage collection," Methods call it
"memory reclamation," Results call it "automatic memory management."
Consistent: Use "garbage collection" throughout, or define explicitly:
"garbage collection (also termed GC)"
```

**Distinguish observations from interpretations:**

```
Observation: "Mean p99 latency decreased from 145 ms to 132 ms (p=0.003)."
Interpretation: "This suggests the optimization effectively reduces tail
latency."
```

**Be specific about uncertainty:**

```
Vague: "There may be some error in these measurements."
Specific: "Latency measurements have a standard error of +/-2.5 ms based
on clock granularity."
```

**Use correct statistical language:**

```
Incorrect: "The correlation was highly significant (p=0.03)."
Correct: "The correlation was statistically significant (p=0.03)."
(p=0.03 is not "highly" significant; that label is reserved for p<0.001)
```

**Verify all numbers:**

- Check that numbers in text match tables/figures
- Verify that sample sizes (n) sum correctly
- Confirm percentages are correctly calculated
- Double-check all statistics

**Avoid overgeneralization:**

```
Poor: "Caching eliminates latency spikes."
Better: "In our workload, the caching layer reduced p99 latency by 38%
compared to no cache (mean difference 54 ms, 95% CI: 31-77, p<0.001)."
```

**Avoid unwarranted causal claims:**

```
Poor (from correlational analysis): "Adding more shards reduces latency."
Better: "Shard count was inversely correlated with p99 latency in this
deployment (r=-0.72, 95% CI: -0.84 to -0.55)."
```

**Use precise numerical descriptions:**

```
Vague: "Many queries timed out."
Precise: "15/50 (30%) queries exceeded the 500 ms timeout threshold."
```

## Objectivity

Presenting information impartially without bias, exaggeration, or unsupported opinion.

**Present results without bias:**

```
Biased: "As expected, our superior method performed better."
Objective: "Method A showed higher accuracy than Method B (87% vs. 76%,
p=0.02)."
```

**Acknowledge conflicting evidence:**

```
"Our findings contrast with Smith et al. (2022), who reported no significant
effect. This discrepancy may result from differences in workload
characteristics or hardware configuration."
```

**Avoid emotional or evaluative language:**

```
Subjective: "The results were disappointing and concerning."
Objective: "The optimization did not significantly reduce latency (p=0.42)."
```

**Distinguish fact from speculation:**

```
"The observed decrease in tail latency was accompanied by increased batching
at the network layer, suggesting that batch coalescing may be the primary
mechanism behind the improvement."
(Uses "suggesting" and "may be" to indicate interpretation)
```

## Consistency

Maintain consistency throughout the manuscript.

**Terminology:**

- Use the same term for the same concept (not synonyms for variety)
- Define abbreviations at first use and use consistently thereafter
- Use standard nomenclature for algorithms, data structures, and protocols

**Notation:**

- Statistical notation (p-value format, CI presentation)
- Units of measurement (ms, GB, ops/s)
- Number formatting (decimal places)

**Tense:**

- Past tense for your specific study actions
- Present tense for established facts
- See section-specific tense rules in `section-standards/*.md`

**Style:**

- Follow venue guidelines consistently
- Citation format
- Heading capitalization
- Number vs. word for numerals

## Logical Organization

Create a clear "red thread" through the manuscript.

**Paragraph structure:**

1. Topic sentence (main idea)
2. Supporting sentences (evidence, explanation)
3. Concluding/transition sentence (link to next idea)

**Section flow:**

- Each section builds logically on the previous
- Questions raised in Introduction are answered in Results
- Findings presented in Results are interpreted in Discussion

**Signposting:**

```
"First, we examined..."
"Next, we investigated..."
"Finally, we assessed..."
```

**Parallelism:**

```
Not parallel: "Aims were to (1) measure throughput, (2) assessment of
latency, and (3) we wanted to evaluate memory overhead."

Parallel: "Aims were to (1) measure throughput, (2) assess latency, and
(3) evaluate memory overhead."
```

## Tense

General guidelines for verb tense in scientific prose. Section-specific rules live in the corresponding `section-standards/*.md` files.

**Present tense** for:

- Established facts and general truths
  - "Consensus protocols tolerate up to f faulty nodes."
- Conclusions you are drawing
  - "These findings suggest that..."
- Referring to figures and tables
  - "Figure 1 shows the distribution..."

**Past tense** for:

- Specific findings from completed research (yours and others')
  - "Smith et al. (2022) found that..."
  - "We observed a significant decrease..."
- Methods you performed
  - "We deployed the system across five clusters."

**Present perfect** for:

- Recent developments with current relevance
  - "Recent studies have demonstrated..."
- Research area background
  - "Several approaches have been proposed..."

## Word Choice

### Commonly Confused Words

| Often Misused | Correct Usage |
|---------------|---------------|
| **affect / effect** | Affect (verb): influence; Effect (noun): result; Effect (verb): bring about |
| **comprise / compose** | Comprise: to contain ("the suite comprises 12 benchmarks"); Compose: to make up ("12 benchmarks compose the suite") |
| **fewer / less** | Fewer: countable items ("fewer nodes"); Less: continuous quantities ("less memory") |
| **data is / data are** | Data are (plural); datum is (singular). In systems papers "data" is often a mass noun ("the data shows...") and that is widely accepted; be consistent within a paper |
| **i.e. / e.g.** | i.e. (that is): restatement; e.g. (for example): examples |
| **that / which** | That: restrictive clause; Which: nonrestrictive clause |

### Overloaded Adjectives

Systems papers routinely overuse these words to the point of meaninglessness. Use each only when the claim is quantified or the comparison is explicit.

**significant** -- Reserve for statistical significance (with p-value). Never use as a synonym for "large" or "important."

```
Poor: "We observed a significant improvement in throughput."
Better: "We observed a statistically significant improvement in throughput
(p=0.003, +15%)."
```

**novel** -- Every paper claims novelty. Only use when you can state precisely what is new relative to prior work. Prefer "to our knowledge, no prior work has..."

```
Poor: "We propose a novel scheduling algorithm."
Better: "To our knowledge, this is the first scheduling algorithm that
provides O(1) worst-case latency under adversarial load."
```

**important** -- Subjective. Replace with the specific consequence.

```
Poor: "Memory fragmentation is an important problem."
Better: "Memory fragmentation accounts for up to 40% of heap waste in
long-running server processes (Chen et al., 2021)."
```

**efficient** -- Meaningless without a baseline. State what metric, against what alternative, and by how much.

```
Poor: "Our protocol is more efficient."
Better: "Our protocol reduces round trips by 3x compared to TCP fast open
under high packet-loss conditions."
```

**scalable** -- All systems claim scalability. Specify the scaling dimension (nodes, data size, request rate) and the scaling behavior (linear, sublinear, logarithmic).

```
Poor: "Our system is scalable."
Better: "Throughput scales linearly with the number of worker nodes up to
64 nodes, beyond which the centralized scheduler becomes a bottleneck."
```

### Words and Phrases to Avoid

- "a lot of" -- use "many" or "substantial"
- "got" -- use "obtained" or "produced"
- "showed up" -- use "appeared" or "was evident"
- "some" -- specify how many
- "often" -- specify frequency
- "recently" -- specify timeframe or cite the year

## Numbers and Units

### When to Use Numerals vs. Words

**Use numerals for:**

- All numbers >= 10
- Numbers with units (5 ms, 3 GB)
- Statistical values (p=0.03, t=2.14)
- Version numbers, port numbers, hardware counts
- Percentages (15%)

**Use words for:**

- Numbers < 10 when not connected to units (five nodes)
- Numbers beginning a sentence (spell out or restructure)

**Examples:**

```
"Five nodes crashed" OR "There were 5 node failures"
(NOT: "5 nodes crashed")

"We tested 15 configurations across 3 data centers"
"Mean latency was 45 ms"
```

### Units and Formatting

- Space between number and unit (5 ms, not 5ms)
- No period after units (ms not ms.)
- Use SI prefixes consistently (ms, us, ns; KB, MB, GB, TB)
- Be consistent in decimal places across a table or paragraph
- Use commas for thousands in text (12,500 not 12500)

**Ranges:**

- Use en-dash (--) for ranges: 15--20 ms
- Include unit only after second number: 15--20 ms (not 15 ms--20 ms)

### Systems-Specific Unit Conventions

| Metric | Unit | Example |
|--------|------|---------|
| Latency | ms, us, ns | "p99 latency was 2.3 ms" |
| Throughput | ops/s, req/s, Kops/s | "peak throughput of 85 Kops/s" |
| Memory | KB, MB, GB, TB | "resident set size of 2.4 GB" |
| Storage | GB, TB, PB | "index size of 1.2 TB" |
| Bandwidth | Gbps, MB/s | "network throughput of 10 Gbps" |
| CPU | cores, % utilization | "16-core machine at 72% utilization" |
| Accuracy | %, F1, AUC | "F1 score of 0.87" |
| Speedup | n-fold, nx | "3.2x speedup over baseline" |
| Energy | Joules, Watts | "peak power draw of 250 W" |

## Paragraphs

### Ideal Paragraph Length

- 3--7 sentences typically
- One main idea per paragraph
- Too short (<2 sentences): may indicate the idea needs development or combining with an adjacent paragraph
- Too long (>10 sentences): may need splitting

### Paragraph Coherence

**1. Topic sentence:**

```
"Batching reduces per-request overhead by amortizing fixed costs across
multiple operations. [Following sentences explain this mechanism]"
```

**2. Transitional phrases:**

- First, second, third, finally
- Furthermore, moreover, in addition
- However, nevertheless, conversely
- Therefore, thus, consequently
- For example, specifically, particularly

**3. Repetition of key terms:**

```
"...this batching strategy. This strategy may explain..."
(Not: "...this batching strategy. This approach may explain...")
```

**4. Parallel structure:**

```
"Configuration A used FIFO scheduling. Configuration B used Round Robin.
Configuration C used Weighted Fair Queuing."
(Not: "Configuration A used FIFO scheduling. Round Robin was used by
Configuration B. The third configuration employed WFQ.")
```
