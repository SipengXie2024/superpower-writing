---
description: User has benchmark numbers and no paper yet, and asks for the Evaluation section prose straight away; the claim spine must come first.
tags: [writing]
max_turns: 12
# These skills produce long-form output (a figure design, an outline with claim stubs,
# a literature sweep); the 300s default cut the first run off mid-answer.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

数据总算跑完了。MHOT（我们那个把 EVM 字节码 JIT 成机器码的执行引擎）在 Base 主网上的结果基本稳了，同一台 EC2、release 编译，跟 revm 解释器和 revmc 做的同机 A/B：

- 全量重放 24,000,000–24,050,000 这五万个区块：revm 1.00x，revmc 1.31x，MHOT 2.18x
- Top-50 热点合约的 gas/s 中位数从 41.2 Mgas/s 提到 96.7 Mgas/s
- perf 上解释器 dispatch 的时间占比从 38% 掉到 9%
- 编译开销：一个合约第一次命中要多花 8.4ms，稳态摊下来每个区块 0.6ms
- 分合约看差别很大，UniswapV3 的 swap 这种算术密集的最多 3.4x，SLOAD 密集的只有 1.15x

这篇打算投明年的 OSDI，还有六周截稿。论文现在一个字都没有，大纲、章节怎么排都还没定。我想先从 Evaluation 动笔，毕竟数据都在手上。你直接帮我把这一节的正文写出来吧，实验设置那段按我上面写的展开，主要结果那几段把这些数字串成话就行。

论文仓库在实验室那台机器上，这边是空目录，你也没有写文件的权限，落盘的事不用管：该给我什么，直接在回复里给全，我自己拷过去建文件。

另外补两句：热点识别阈值的消融我还没跑；多线程下跟 revmc 的对比也还没做，现在所有数都是单线程测的。
