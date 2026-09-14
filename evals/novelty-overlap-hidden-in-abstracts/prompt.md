---
description: User pitches a learned state prefetcher for revm with three core claims, pastes six abstracts he collected, and asks for a sanity check on his own conclusion that none of them conflicts.
tags: [writing]
max_turns: 12
# Per-claim prior-work adjudication over six abstracts is long-form output; the 300s default truncates it.
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

下个月想投 MLSys，赶不上就转 EuroSys，动笔之前先跟你把查新这一步做掉。

我的东西是这样：revm 在磁盘后端上跑真实主网区块，时间大头是打 MPT 的随机读，执行一停就是在等 IO。我想在块执行开始之前，用一个很轻的模型（输入是 tx 的 to 地址、calldata 前四字节的函数选择器、再加这个合约的历史访问统计）预测这一块会碰到哪些 storage slot，对应的 trie 节点提前并行 warm 进内存，把执行期的 stall 砍掉。

我自己拆出来三条核心 claim：

- C1：主网交易碰哪些 state，在交易执行之前就能从 to + selector + 历史统计里预测出来，precision/recall 够高到能拿来做预取。
- C2：把这个预测器接进 revm 的磁盘后端，端到端块执行时间能降 20% 以上。
- C3：这个预测器对训练里没见过的新合约也能泛化，走 bytecode 相似度回退。

相关工作我自己扒了一轮，六篇摘要贴在下面，原文我都翻过：

**[1] Learned Prefetching for Buffer-Pool Managed OLTP Databases (VLDB 2023)**
Buffer pool misses dominate tail latency in disk-resident OLTP engines. We train an LSTM over page-access deltas observed in the in-flight transaction stream and issue prefetches for the next k pages. On TPC-C and one production trace the model raises buffer hit rate by 11 points over a tuned LRU-k baseline and cuts p99 latency by 18%. The predictor runs inside the storage engine and adapts online.

**[2] Reconstructing Storage-Slot Access Sets of Ethereum Transactions at Scale (workshop, 2024)**
We replay 1.2B mainnet transactions and extract, for each one, the exact set of storage slots read and written. The resulting corpus supports gas-accounting audits, state-growth analyses, and scheduler studies. Extraction is offline and requires full execution; we make no attempt to obtain an access set without executing the transaction.

**[3] Caching in Blockchain Full Nodes: A Survey (2025)**
We survey trie-node caches, flat state layouts, snapshot designs, and their interaction with pruning across geth, erigon, reth, and two Move-based clients. We taxonomize the design space and report published numbers side by side. We propose no new mechanism and run no new experiments.

**[4] Anticipatory State Warming for a Disk-Resident BFT Transaction Runtime (preprint, 2025)**
Execution in our deployment is dominated by random reads against a disk-resident authenticated store. We observe that the footprint a transaction touches is largely determined by its entry function and the shape of its arguments. A gradient-boosted classifier over those features, trained on 40M historical transactions, names the storage keys a transaction will touch before the transaction is scheduled, at 0.87 precision and 0.91 recall. Those keys are fetched from the store in parallel with consensus. End to end, warming removes 31% of execution stalls. The classifier retains 0.81 recall on modules never seen during training by backing off to bytecode n-gram features.

**[5] Access Lists in Block Building: Measuring EIP-2930 Adoption (2024)**
We measure how often senders and builders attach optional access lists to mainnet transactions, how accurate those declared lists are, and what the gas refund structure implies for adoption. Declared lists come from the sender; we study adoption and accuracy, not how a list could be inferred.

**[6] Contract-Level Conflict Tagging for Parallel Execution in an EVM Sidechain (2024)**
We tag each deployed contract with a static conflict class derived from its storage layout, then bucket transactions so that two transactions touching the same class never run concurrently. Tagging is contract-granular: we never resolve which individual slots a transaction touches, and no state is fetched ahead of execution.

我自己的判断是：[1] 是数据库不是链，而且它是执行过程中看已发生的访问再往后猜；[2] 是执行完之后事后重建的，正好能给我当标注工具用；[3] 是综述；[5] 是发送方自己声明 access list，不是预测；[6] 只做到合约粒度，也不预取。[4] 是 Move 那套 resource/module 模型加他们自研的 BFT 链，跟以太坊的 storage slot 加 MPT 根本不是一个数据模型，标题讲的还是 consensus 那边的事，我觉得不算撞。

所以我的结论是这三条 claim 都还立得住。你帮我把把关，看我这个判断站不站得住，站得住我这周就开始写 proposal。
