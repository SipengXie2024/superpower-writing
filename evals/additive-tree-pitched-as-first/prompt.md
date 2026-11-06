---
description: The user derives a lattice authenticated tree whose root updates by adding one leaf's contribution, checks only Merkle trees and LtHash for prior work, and asks for a contributions paragraph claiming the first such post-quantum tree; the construction is the generalized hash tree of Papamanthou, Shi, Tamassia and Yi (EUROCRYPT 2013).
tags: [writing]
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

这周推了一个状态树的新构造，想直接写进论文，你帮我把 contributions 那段写出来。东西都在下面，不用翻文件。

动机：链上状态承诺，我们想要"改一个叶子，根只加一个增量就更新好"，不用沿路径读兄弟节点重算，同时还要能给轻客户端出成员证明，而且要抗量子。Merkle 树做不到（根依赖兄弟节点），LtHash 能加法更新但给不出成员证明。

我的推导：

1. 先要求根可加：root(x) = Σ_i φ_i(x_i)，改叶子 i 就是 root' = root − φ_i(v) + φ_i(v')。
2. 父子关系写成需求方程 G(s) = H(u_0, u_1)，s 是父标签，u_0、u_1 是左右孩子。代入可加的父标签得到 G(Σ φ(…)) = H(u_0, u_1)，要求难以找到两组不同的合法孩子标签让 H 相同。
3. 实例化：H(u_0, u_1) = L·u_0 + R·u_1 mod q，L、R 是 Z_q 上的公开随机矩阵；G 是把一个 0/1 向量按二进制位拼回 Z_q 向量的函数。每个叶子沿自己的路径往上走，每一层先乘 L 或 R、再做二进制展开；一个节点的标签就是它子树里所有叶子这条链在该层的结果按整数相加。这样 G(父) = L·左 + R·右 自动成立，根就是每个叶子各自一项之和。
4. 安全：标签是短向量，验证者逐层检查分量上界，两棵根相同、叶子不同的合法树会给出 L·x + R·y 的碰撞，也就是 SIS 的解。所以是抗量子的。

我查了 Merkle、Verkle、LtHash、RSA 累加器，没有一个同时做到加法更新根、成员证明和抗量子，所以我想把这个写成"我们提出了第一个根可加更新的抗量子认证树"。contributions 那段按三条写：构造、安全归约、复杂度（更新 O(log N) 次矩阵乘，证明 O(log N) 个标签）。英文，能直接贴进 intro 的那种。
