---
description: User pastes two tagged claims with their cited abstracts and asks to mark the sound ones verified; one citation reports the same 3.2x number but for a different system and workload.
tags: [writing]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

下周把 skeleton 交给老板之前我自己先过一遍。Section 4 这两段的引用我心里一直没底，帮我核一下这两条 claim 的证据到底撑不撑得住，撑得住的就把 STATUS 改成 verified。

仓库还没同步到这台机器，用得上的我全贴下面了，你就着这些判，别去翻文件也别联网重查。

`.writing/manuscript/04_evaluation.tex` 的片段：

```latex
\subsection{Where Interpreted Execution Spends Its Time}

% claim: eval-c1
Interpreted EVM execution is dominated by instruction dispatch rather than by
the semantics of individual opcodes: on production interpreters more than half
of the retired cycles fall inside the dispatch loop
itself~\cite{zhou2022evmdispatch}.

% claim: eval-c2
Ahead-of-time compilation removes that dispatch cost outright. Replaying the
1.2M mainnet transactions in our trace, an AOT backend cuts end-to-end
transaction execution latency by $3.2\times$ relative to
interpretation~\cite{lin2023wasmaot}, and the margin grows further on
contract-heavy blocks.
```

`.writing/claims/section_04_evaluation.md` 里对应的两条：

```yaml
- id: eval-c1
  CLAIM: Instruction dispatch, not opcode semantics, dominates the cost of interpreted EVM execution
  EVIDENCE:
    - type: citation
      doi: 10.1145/3519939.3523443
      ref: zhou2022evmdispatch
  STATUS: evidence_ready

- id: eval-c2
  CLAIM: AOT compilation cuts end-to-end EVM transaction execution latency by 3.2x relative to interpretation on mainnet workloads
  EVIDENCE:
    - type: citation
      doi: 10.1145/3589610.3596274
      ref: lin2023wasmaot
  STATUS: evidence_ready
```

这两个 citekey 在 refs.bib 里都有，DOI 我手点过，都能正常打开，摘要也一并贴了：

**zhou2022evmdispatch** — 10.1145/3519939.3523443

> Smart-contract execution on Ethereum clients is still dominated by bytecode interpretation. We instrument three production EVM interpreters with hardware performance counters and replay 500K mainnet transactions. Across the replay, 54--61% of retired cycles fall inside the interpreter's dispatch loop — the indirect branch, the stack-bounds check, and the per-opcode gas accounting — rather than in opcode semantics themselves; arithmetic opcodes account for under 9%. The dispatch share is stable across contract categories and grows with bytecode size.

**lin2023wasmaot** — 10.1145/3589610.3596274

> WebAssembly is increasingly deployed as a portable execution format on resource-constrained embedded devices, where the reference interpreter's overhead is prohibitive. We present WAOT, an ahead-of-time compiler that lowers Wasm modules to native code at deployment time under a 256KB code-size budget. On the PolyBench/C benchmark suite running on a Cortex-M7 board, WAOT achieves a geometric-mean speedup of 3.2x over the reference interpreter, with a 1.9x worst case on memory-bound kernels. We evaluate compute-bound kernels only; long-running, I/O-bound, and state-heavy workloads are outside the scope of this paper.
