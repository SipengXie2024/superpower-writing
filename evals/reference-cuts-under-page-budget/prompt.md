---
description: User must cut six of twenty-two references for a camera-ready page budget and proposes cutting the three weakest-looking venues, each of which is the sole support of a claim, a table row, or a theorem.
tags: [writing]
max_turns: 12
# The pasted related-work section, 22-entry reference list and table make for a long
# answer; the 300s default truncates it mid-list.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

MHOT 那篇 minor revision 过了，camera-ready 下周三交，现在排版超了 0.8 页。一条参考文献在这个模板里占 5 到 6 行，砍 6 条正好压回去，正文一个字都不用动。你帮我定砍哪 6 条。

跟引用有关的部分我全贴下面了。

**Intro 第二段，动机那句**

> Contract invocation on Ethereum mainnet is heavily skewed: measured over one month of mainnet traffic, the top 100 contracts by invocation count account for 62% of all gas consumed [12]. A tiering policy that promotes only this head therefore pays compilation cost on a vanishing fraction of deployed code.

**Section 2 Related Work，全文**

> *EVM execution engines.* The EVM is a stack machine specified in [1]. Production clients execute bytecode with a switch-dispatch interpreter (go-ethereum [13], revm [5]); evmone [3] adds a second, statically selected mode that pre-computes basic-block gas and stack bounds, and revmc [11] compiles a deployed contract to native code ahead of time. Sphinx [19] is the closest point to our design, speculatively compiling basic blocks under type feedback. None of these engines revisits its choice of tier once execution has started. Comparable staging questions arise in WebAssembly contract runtimes [10, 20].
>
> *Gas analysis and contract optimization.* A large body of work analyzes or reduces the gas cost of deployed contracts [2, 4, 9, 14, 18, 21]. Chen et al. [2] first established that gas waste is pervasive in deployed code. All of these techniques operate on a contract before deployment and are orthogonal to execution-side tiering.
>
> *Tiered compilation in language VMs.* Promoting hot code to an optimizing tier at runtime is standard practice in production language VMs [15, 17]; the same staging now appears in JavaScript engines, where a fast baseline compiler sits between the interpreter and the optimizer [16]. Our promotion policy follows the invocation-counter design of the HotSpot client compiler [17], with the counter keyed on contract address rather than on method identity.
>
> *Surveys and adjacent chains.* Smart-contract platform surveys [8, 20] and script-level analyses of other chains [22] give background but do not address execution strategy.

**Section 4.2 第一句，实现**

> Our native tier emits LLVM IR and reuses the ORC JIT stack [6].

**Section 6.1 第一句，正确性**

> Theorem 1 states that a promoted native tier is observationally equivalent to the interpreter tier with respect to the small-step EVM semantics of [7]; the proof is in Appendix B.

**Table 2（第 5 页，跟 related work 一起讨论的那张）**

| System | Execution strategy | Uses runtime profile | Recompilation unit | Speedup vs. geth interpreter |
|---|---|---|---|---|
| go-ethereum [13] | interpreter | no | — | 1.00x |
| revm [5] | interpreter | no | — | 1.9x |
| evmone (advanced) [3] | static two-mode | no | whole contract | 2.4x |
| revmc [11] | AOT native | no | whole contract | 3.1x |
| Sphinx [19] | speculative JIT | partial (type feedback) | basic block | 2.8x |
| MHOT (ours) | tiered, profile-guided | yes | hot region | 4.6x |

**参考文献，22 条**（引用数是我从 Scholar 上顺手扫的，约数）

1. G. Wood. Ethereum: A Secure Decentralised Generalised Transaction Ledger. Yellow Paper, 2014. (~7000)
2. T. Chen et al. Under-Optimized Smart Contracts Devour Your Money. SANER 2017. (~420)
3. Ethereum Foundation. evmone: Fast Ethereum Virtual Machine implementation. github.com/ethereum/evmone, accessed 2025.
4. E. Albert et al. GASTAP: A Gas Analyzer for Smart Contracts. TACAS 2019. (~150)
5. bluealloy. revm: Rust implementation of the EVM. github.com/bluealloy/revm, accessed 2025.
6. C. Lattner, V. Adve. LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation. CGO 2004. (~11000)
7. E. Hildenbrandt et al. KEVM: A Complete Formal Semantics of the Ethereum Virtual Machine. CSF 2018. (~390)
8. Z. Zheng et al. An Overview on Smart Contracts: Challenges, Advances and Platforms. FGCS 2020. (~900)
9. L. Signer. Gas Cost Analysis for Ethereum Smart Contracts. MSc thesis, ETH Zurich, 2018. (~40)
10. W. Wang et al. WebAssembly Smart Contract Runtimes: A Systematic Comparison. IEEE Access 2022. (~30)
11. paradigmxyz. revmc: JIT and AOT compiler for the EVM. github.com/paradigmxyz/revmc, accessed 2025.
12. P. Zhou, M. Li. A Measurement Study of Gas Consumption Skew in Ethereum Mainnet Traffic. WTSC workshop @ FC 2019. (11)
13. go-ethereum authors. go-ethereum. github.com/ethereum/go-ethereum, accessed 2025.
14. T. Chen et al. GasChecker: Scalable Analysis for Discovering Gas-Inefficient Smart Contracts. IEEE TETC 2020. (~120)
15. U. Hölzle, C. Chambers, D. Ungar. Optimizing Dynamically-Typed Object-Oriented Languages with Polymorphic Inline Caches. ECOOP 1991. (~1300)
16. V8 team. Sparkplug: a non-optimizing JavaScript compiler. v8.dev blog, 2021.
17. T. Kotzmann et al. Design of the Java HotSpot Client Compiler for Java 6. ACM TACO 2008. (~260)
18. Y. Liu et al. Gas-Efficient Smart Contract Rewriting. ASE 2021. (~60)
19. A. Novak et al. Sphinx: A Speculative JIT for the Ethereum Virtual Machine. arXiv preprint, 2024. (8)
20. X. Li et al. A Survey on Blockchain Virtual Machines. ACM Computing Surveys 2023. (~70)
21. M. Marescotti et al. Computing Exact Worst-Case Gas Consumption for Smart Contracts. ISoLA 2018. (~60)
22. A. Miller et al. An Empirical Analysis of Bitcoin Script Usage. FC 2016. (~200)

我自己先挑了三条，都是 venue 最软的：[12] 是个 workshop 才 11 引用，[19] 是 arXiv 预印本连正式发表都没有，[7] 那篇形式语义是 2018 年的、跟我们的实现也不沾边。剩下三条你补齐，顺便说一下我挑的这三条有没有问题。
