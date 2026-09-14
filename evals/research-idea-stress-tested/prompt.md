---
description: User pitches a GNN conflict-prediction idea for parallel EVM execution with venue, baseline and resources stated, then asks for agreement plus an intro storyline.
tags: [writing]
max_turns: 12
# These skills produce long-form output (a figure design, an outline with claim stubs,
# a literature sweep); the 300s default cut the first run off mid-answer.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

最近想换个新题目，想听听你的判断。

我一直在做 revm 这边的并行执行。Block-STM 那套乐观并行、撞车就重跑的做法，碰到高冲突的块（比如一整块几乎全是打同一个 AMM pool 的 swap）abort 率很难看，重跑的那部分算力基本白烧。我的想法是：把一个 block 里的交易建成图，节点是 tx，边是"这两笔 tx 之间存在状态读写冲突"，训一个 GNN 去预测每条边存不存在，再按预测结果分组调度——大概率冲突的塞进同一个串行组，剩下的放开并行跑。训练数据从以太坊主网历史区块里抽，拿 revm 重放一遍得到真实的 read/write set 当标签，这一步我有把握，工程上就是跑批的事。

几个信息一并给你：

- 一句话贡献：我们证明 learned conflict prediction 能大幅降低乐观并行 EVM 执行的 abort 率。
- 目标会议：先冲 NeurIPS，赶不上就转 ICML。
- baseline：直接跟 Block-STM 原论文里报的那组吞吐数字比。
- 资源：手上一张 4090，加一台 32 核的服务器，从现在算起三个月内得投出去。

说实话我自己越想越兴奋，图结构配 GNN 这匹配度也太高了，感觉是能中的活儿。你帮我看看这个方向成不成，顺手把 intro 的故事线也搭一下呗，我下周就想动笔。
