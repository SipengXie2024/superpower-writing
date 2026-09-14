---
description: User asks what prior work already exists on tiered, profile-guided recompilation for EVM bytecode before he keeps a "the first" novelty claim in an OSDI intro.
tags: [writing]
max_turns: 12
# These skills produce long-form output (a figure design, an outline with claim stubs,
# a literature sweep); the 300s default cut the first run off mid-answer.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

帮我把 EVM 执行层"分层编译"这个小方向已经有的工作摸一遍。方向我定了，不用再帮我挑题，现在是在写 intro，related work 那一节也得靠这个填。

intro 里现在这句是我最虚的：

> Existing EVM implementations commit to a single execution strategy: a plain interpreter (geth, revm) or an ahead-of-time native compiler (revmc, evmone's advanced mode). We present the first EVM execution engine with tiered, profile-guided recompilation, promoting hot contracts from interpretation to optimized native code at runtime based on on-chain invocation frequency.

"the first" 这三个字我心里没底。我自己能想到的就这么几个：revmc 是纯 AOT，编完就定了，运行时不会再提升；evmone 的 baseline 和 advanced 算两档，但走哪档是静态决定的，不看执行热度；Block-STM 那条线是并行调度，跟分层编译压根不是一回事。

想搞清楚两块。一是区块链虚拟机里边（EVM、Move VM、WASM 合约那些）到底有没有人真按热度做过运行时 JIT 分层或者重编译，学术论文和工业实现都算。二是 JVM、V8 那套经典 tiering，有没有已经被人搬到智能合约执行场景上发过文章的。

要是确实有人做过，这句 "the first" 我该怎么改，才不至于被 OSDI 的 reviewer 一枪打死。
