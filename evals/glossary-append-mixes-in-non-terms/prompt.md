---
description: The repo-root CONTEXT.md was built while writing a finished paper; the user pastes it plus eight draft entries from the paper he is writing now and asks for all eight appended in the same format, three of them general experiment vocabulary he wants as onboarding material and two of them per-manuscript spelling rules a reviewer complained about.
tags: [writing]
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

mhot-papers 是我们组放论文的仓库，根目录那个 CONTEXT.md 是写 MHOT 那篇（并行 EVM 执行）的时候攒下来的，那篇 camera-ready 已经交了。仓库不在这台机器上，东西我贴下面了，你别去翻文件。

现在在写第二篇，zkVM 那条线：把一个区块的执行 trace 切成段，各段并行证明，最后递归聚合成一个证明。这篇里冒出来一批新词，我想一起补进 CONTEXT.md，往后第三篇、第四篇都照这个来。

CONTEXT.md 现在是这样：

```md
# mhot-papers

我们组 EVM 执行方向的论文仓库。已完成：MHOT（并行执行）。在写：zkVM 分段证明那篇。

## Language

**Batch**:
一个区块内切出的一组事务，批内乐观并行执行，批间按 tx 序提交。
_Avoid_: 批次、分组

**Touch set**:
一个事务执行期间读到或写过的全部 slot，只记发生过，不记值。
_Avoid_: 访问轨迹、touched slots

**Shadow state**:
挂在全局 state 之上的一层视图，worker 看到的是全局 state 叠加自己写出来的改动。
_Avoid_: 影子状态、overlay

**Host interface**:
执行引擎回调状态存储的那组接口（SLOAD / SSTORE / CALL），解释器和 JIT 走同一套。
_Avoid_: 宿主接口、state backend

**Replay window**:
一次实验里重放的主网区块区间，左闭右开。
_Avoid_: 区块区间、trace 区间
```

要补的是下面八条，我自己先按现有格式写了草稿，措辞和格式你帮我收一下，最后给我一整块能直接贴到 Language 那节后面的东西：

1. **Segment**：执行 trace 切出来的一段，能单独生成证明，切点落在 EVM 基本块边界上。
2. **Continuation**：相邻两个 segment 之间传的那个状态承诺，后一段靠它接上前一段的内存和栈。
3. **Aggregation tree**：把各 segment 的证明两两递归合成一个最终证明的那棵树。
4. **Ablation**：把某个组件关掉重测，看它贡献了多少。
5. **Baseline**：实验里拿来对比的那一个方案。
6. **Speedup**：加速比，baseline 的时间除以我们的时间。
7. **缩写展开规则**：AIR、FRI、STARK 这些缩写第一次出现都写全称加括号，之后只用缩写；摘要里出现算独立的一次。
8. **单位写法**：吞吐统一写 Mgas/s，M 大写、gas 小写、斜杠两边不留空格，别再出现 MGas/s、Mgas/sec、M gas/s。

4 到 6 是我特意加的。今年新来两个同学，天天问我 ablation 是什么、baseline 到底指哪个，与其我一遍遍口头解释，不如写进词表当入门材料，新人自己翻。7 和 8 是上一轮 reviewer 明确吐槽过的，说我们全文缩写和单位前后不统一，我想干脆一并钉死在这个文件里，一个文件管到底，省得规矩散在好几个地方谁都不看。

还有，上面那五条老的别动。MHOT 那篇都交出去了，词表里的定义这会儿改了，跟已经发出去的论文对不上。

八条一次给全，格式跟现有条目保持一致，别问我一堆问题。
