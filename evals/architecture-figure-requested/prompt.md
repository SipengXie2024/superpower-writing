---
description: User pastes the structure of an EVM JIT engine and asks for a ready-to-include vector architecture figure for his paper, telling the assistant not to discuss layout first.
tags: [writing]
max_turns: 12
# These skills produce long-form output (a figure design, an outline with claim stubs,
# a literature sweep); the 300s default cut the first run off mid-answer.
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

我们那篇 EVM 执行引擎的论文准备投 EuroSys，Section 4 开头缺一张系统总体架构图，通栏的。之前拿 draw.io 拼了一版，太丑，导出 PDF 之后字体还跟正文对不上，这次想要能直接 `\input` 进 main.tex 的矢量图。代码仓库在另一台机器上，这边是空目录，我把结构贴给你：

执行侧（数据流大致左→右）：

- **Block executor** 逐笔取交易，把 calldata 和目标合约的 code hash 交给 **Dispatcher**
- Dispatcher 查 **Code cache**（code hash → native code 指针）：命中就跳到编译好的 native code 执行；未命中回退到 revm 的 **Interpreter** 解释执行，同时给该 code hash 的调用计数器 +1
- **Profiler** 盯着这些计数器，过阈值（累计 64 次调用，或者单次执行 gas > 2M）就把该合约丢进编译队列

编译侧（后台线程，异步，跟上面两条不在同一个时间轴上）：

- 从队列取 EVM bytecode → 基本块切分 → 降到我们自己的 **SSA IR**（每个基本块带 gas 消耗和栈深度注解）→ 三个 pass：常量栈折叠、gas 计量合并（块内逐条扣 gas 合成一次）、内存越界检查消除 → 丢给 LLVM ORC JIT 出 native code → 回填 Code cache

两条执行路径共享同一份状态：native code 和解释器都走同一套 **Host interface**（SLOAD / SSTORE / BALANCE / CALL 这些回调）打到 revm 的 `Database` trait，底下是 MDBX。

想强调的：解释器慢路径、JIT 快路径、后台编译路径这三条线要一眼分得开；IR + 三个 pass 那段是我们的主要贡献，希望是整张图里最重的一块。右边有空位的话把数字也标上，热合约单测 3.7x，整块重放 1.9x。

你直接把 figure.tex 给我，能编过就行，别一上来先跟我讨论布局。
