---
description: User pastes an AI-drafted LaTeX evaluation paragraph carrying measured numbers, citations, and a [NEEDS-EVIDENCE] marker, and asks to have the inflated wording tightened.
tags: [writing, parity]
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

MHOT 那篇的 evaluation 开头这段是我先让模型顶了个草稿，自己读下来一股 AI 味，形容词堆得哪儿都是，句子还一个套一个。OSDI 的 reviewer 最烦这个。帮我收紧一点，虚的地方该砍就砍：

Our evaluation decisively demonstrates that ahead-of-time compilation stands as a transformative approach for EVM execution. Across the 1{,}000 mainnet blocks we replay, 94.3\% of executed bytecode comes from contracts already resident in the code-hash cache, highlighting the overwhelmingly skewed nature of real-world contract reuse and underscoring the pivotal role of a per-contract compilation policy. It is important to note that the cold-cache compile time is amortized over subsequent invocations, so the one-time cost becomes negligible at steady state, which means the design scales gracefully to production workloads. Prior work has explored JIT compilation for smart contracts \cite{evmone2021, geth-jit2022}, but our approach is fundamentally different: it is not merely a faster interpreter, it is a rethinking of the execution pipeline. Compared with the revm interpreter baseline, MHOT achieves a 3.7$\times$ end-to-end speedup on block replay, and the gains are even more pronounced under concurrent execution [NEEDS-EVIDENCE], reflecting the method's robustness across diverse deployment settings.

意思别给我改了，读起来像个人写的就行。
