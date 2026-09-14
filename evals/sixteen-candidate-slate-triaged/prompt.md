---
description: User dumps 16 brainstormed research directions with his hardware, manpower and four-month deadline, and asks for a ranking he has to defend at next week's group meeting.
tags: [writing]
max_turns: 12
# A 16-candidate triage is long-form output; the 300s default truncates it mid-table.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

组会上大家把想做的方向一股脑甩出来了，我事后整理成 16 条，下周我得回去讲排序，所以先找你过一遍。

条件先摆着：一张 4090（24G 显存），一台 32 核 / 256G 内存的服务器，NVMe 上挂了一份到 block 21,000,000 的以太坊 archive 快照，另外 Base 主网有 RPC 可以随便调。人就我一个，加一个刚进组的本科生。时间上四个月内必须投出去，系统向投 EuroSys / ATC，ML 向投 MLSys。

1. 给 revmc 的 AOT 产物做按合约热度的分层缓存：只给调用频次前 1% 的合约编原生码，其余继续走解释器，量化编译开销和命中率的平衡点在哪。
2. 不训模型，纯拿历史冲突统计给 Block-STM 做交易静态重排，看 abort 率能压到多低。
3. 研究 gas 定价机制对以太坊生态的影响。
4. 给 revm 的状态访问做学习型预取：块执行开始前预测这一块要读哪些 trie 节点，提前从 NVMe warm 进内存。
5. 把各家 L2 sequencer 内部的私有 mempool 排序日志收集起来，分析跨 L2 的 MEV 传导路径。
6. 在 revm 里把 state expiry 那套提案实现掉，测状态体积随时间怎么变。
7. 从零预训练一个 7B 模型专做 EVM 字节码反编译，目标是把 heimdall 和 Dedaub 都比下去。
8. 用 eBPF 在 geth 上做细粒度剖析，量化真实区块回放里 state 访问 stall 占总执行时间多少。
9. 把 JVM 那套分层编译搬到 EVM 上：按运行时热度把合约从解释提升成原生码，冷下来再降级。
10. 研究 MEV 对普通用户体验的影响。
11. 用 MHOT 那套内存布局思路重写 revm 的 journal，把 revert 时的拷贝开销砍掉。
12. 拿主网历史区块做一次并行度上界测量：用真实 read/write set 算最优调度下的理论加速比。
13. 给 revm 做确定性 record/replay，拿来跟 geth、evmone 做差分测试，专门找共识分歧。
14. 用 LLM 给智能合约自动生成不变量，再用符号执行去验，在主网合约上统计能覆盖多少已知漏洞。
15. 顺着第 12 条再往前一步：把那个并行度上界按 DeFi 协议类别拆开，看是哪几类协议在拖后腿。
16. 把 revm 移植到 RISC-V 裸机上，量化 zkVM 场景下每条 EVM 指令的开销。

帮我排个序，我下周得讲清楚为什么是这个顺序。有几条是别人当场提的，我要是不做，回去总得给个说法。
