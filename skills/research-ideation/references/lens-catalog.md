# Generative Lens Catalog

These lenses generate candidate research directions. Each lens is an analytic angle on a research area. Running the area through every lens surfaces more independent candidates than free brainstorming, which tends to stall on the first few obvious directions.

The lenses produce breadth. They do not judge quality. A candidate's worth is decided later by the FINER rubric and the cross-model adversarial pass, never by the lens that produced it.

Run all five lenses before critiquing any candidate. Add a domain-specific lens when the area warrants one. The five are a floor, not a ceiling.

## The Five Core Lenses

### 1. Method-Transfer

A method works in domain A. No one has tried it in domain B. Ask what would happen if you ported it, and whether the port reveals a genuinely new insight rather than a routine application.

Plain "apply X to Y" is the weakest research move. Push the transfer until it exposes a mechanism, a failure, or a surprising result. The transfer earns a candidate only when the answer matters either way.

Prompts:

- What technique is standard in vision but untried in systems scheduling?
- What proof technique from cryptography has no analogue in this learning-theory question?
- What estimator from one subfield would break, and informatively, in another?

CS and ML examples:

- Speculative decoding moved from language models to a different autoregressive setting. What breaks?
- Mixture-of-experts routing applied to a database query planner. Does sparsity help or hurt tail latency?

### 2. Contradiction

Two papers report conflicting findings. The conflict is an opening. A direction that resolves it, by identifying the hidden variable that separates the two regimes, is publishable whichever way it lands.

Prompts:

- Which two recent results disagree, and what experimental difference might explain it?
- Where does folklore say one thing and a benchmark say another?
- Which ablation do two papers run differently, reaching opposite conclusions?

CS and ML examples:

- One paper finds longer context always helps; another finds it hurts past a length. What confound separates them?
- Two systems papers disagree on whether kernel-bypass networking wins under contention. Which workload assumption differs?

### 3. Untested-Assumption

Everyone in the subfield assumes something. No one has tested it directly. Naming the assumption and designing the test that could break it is a strong diagnostic contribution.

Prompts:

- What does every paper in this line take for granted in its setup?
- Which default hyperparameter, baseline, or metric has no one questioned?
- What would a skeptic from an adjacent field refuse to accept without proof?

CS and ML examples:

- Everyone evaluates retrieval-augmented generation on clean corpora. Does the assumed benefit survive noisy real-world indexes?
- Schedulers assume task durations are roughly predictable. What happens to the standard policy when they are heavy-tailed?

### 4. Scaling-Regime

A result holds at one scale. A regime at the edges, much larger, much smaller, much sparser, much noisier, is unexplored. The behavior at that regime is an open empirical question.

Prompts:

- Does the finding hold at 10x the model size, or 1/10 the data?
- What happens in the low-data, high-noise, or extreme-batch regime?
- Where does the curve that everyone extrapolates actually bend?

CS and ML examples:

- A scaling law is fit on dense models. Does it hold for a fixed sparse-activation budget?
- A consensus protocol is benchmarked at 5 nodes. How does its tail latency behave at 500 under geo-distribution?

### 5. Diagnostic

A question nobody has asked, aimed at understanding why something works rather than building something new. Diagnostic directions produce findings, not artifacts, and a clear negative result is as publishable as a positive one.

Prompts:

- Why does this method work? What is the actual mechanism, isolated by ablation?
- What does this model represent internally that explains its behavior?
- If we removed the part everyone credits, would performance actually drop?

CS and ML examples:

- A regularizer is credited for generalization. An ablation isolates whether it is the regularizer or an incidental learning-rate effect.
- A cache shows a surprising hit-rate gain. A diagnostic attributes it to workload locality rather than the policy itself.

## Adding A Domain-Specific Lens

When the area has its own recurring structure, add a sixth lens. Examples:

- Identification or causal-validity lens for empirical-measurement work.
- Hardware-bottleneck lens for systems and architecture, asking what is infeasible now but tractable with a new estimator or accelerator.
- Threat-model lens for security, asking which assumed adversary capability has shifted.

Name the lens, write two or three prompts in its voice, and run it alongside the five.

## How To Run The Lenses

For each lens, generate several candidate directions before moving to the next lens. Aim for the full pool of 15 to 20 candidates across all lenses combined. Tag each candidate with the lens that produced it; the tag feeds the brief's "lens of origin" field and helps spot when the pool leans too hard on one angle.

Ground the generation in real prior work. Run targeted searches per lens so candidates rest on actual papers, not memory. Never fabricate a paper, an arXiv ID, or a DOI to justify a candidate; mark an unconfirmed reference `[UNVERIFIED]` and move on.

Do not critique while generating. Capture every candidate, even the ones that feel weak. Weakness is a downstream verdict. Dropping a candidate at generation time defeats the breadth the lenses exist to create.
