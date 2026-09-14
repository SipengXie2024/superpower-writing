# mode C 独立多镜头审查 gate

mode C（从零画、无 skeleton 先例）的 ④.5 走完 Step 0 + 18 项自审后，**必须再过这道 gate**，不可跳过。

## Contents

- 为什么强制（实测证据）
- 「独立」的严格含义，以及谁来跑
- 四个镜头分工
- gate 之后仍不能直接交付
- 机制

## 为什么强制

mode C 测试（2026-05-29，同心圆 / Sankey / RLHF 闭环，3 张从零图）实测 **3/3 都崩，且每次崩在不同轴上**，但有统一规律，**图里最"新"、最无 skeleton 先例的那个结构元素，就是崩点**：

- 同心圆 → 现编的多面板**数字叙事自相矛盾**（核心层在威胁锥里没削弱却号称拦 99%）
- Sankey → 数字反而对了，但**新的变宽汇聚几何崩**（合并节点渲染成空心白框、sink 失比例）
- RLHF 闭环 → 语义对，但**新的环形闭合几何崩**（不成环、3/4 弧 + 横弦、空角）

**而 generator 自审对这个核心缺陷系统性失明**：三张分别跑了 4 / 3 / 1 轮自审，全部自评"发表级 / closes cleanly"，**全部漏掉了最核心的那个缺陷**。**自审轮数多少都救不了，失明是结构性的**（generator 看不见"我想画的"↔"实际渲染的"差距）。**每一次，只有独立对抗式多镜头审查抓到了核心缺陷。**

## 「独立」的严格含义，以及谁来跑

> 🔴 **"独立"严格指：另起的全新 agent / 空白上下文，不是 generator 自己在同一上下文里"审 4 遍"。** 同上下文自审与 generator 共享同一套盲区，等于没审。**实测（fig4 复杂图）：generator 按本 gate 跑、却跑成"同模型 self-pass 4 遍"，照样漏掉 Sankey 断裂+失比例的重崩；是独立 spawn 的 agent 才抓到。self-pass ≠ gate。**
>
> ⚙️ **谁来跑这道 gate**：是**顶层 orchestrator（带 Agent/workflow 工具的主循环）**的职责，**不是 generator 的**。generator / implementer 子 agent 通常 **spawn 不出独立子 agent**（环境常只暴露重量级 team 工具、无轻量 spawner），把 gate 交给它只会退化成 self-pass（实测 fig4 + fig5 两次都如此）。正确流程：generator 做完自己的 ④.5 自审并交付 → **控制权回到 orchestrator → 由 orchestrator 独立 spawn 4 个审查 agent 跑 gate**。

由 orchestrator 独立 spawn 4 个全新审查 agent（各自空白上下文），各 Read 渲染出的 PNG，**对抗式**找问题（默认"图里有 bug，去找"），各自返回 blocker（含 severity + 位置 + **具体视觉证据**，证明它真看了图）。

## 四个镜头

| 镜头 | 专盯 | mode C 高发崩点 |
|---|---|---|
| **geometry** | 新布局几何是否真画对（同心是否真同心、环是否闭合、Sankey band 宽是否 ∝ 量、节点是否被填充非空心、穿框/裁切/大空白） | **最高发，新结构的几何** |
| **semantic** | 信息流 / 顺序 / 方向是否对；**独立重算图里所有数字/公式**，查跨面板一致性 | 现编数据自相矛盾 |
| **text** | 中文全水平、missing char、stale 标签、小字可读性 | 较低（自审多能覆盖） |
| **aesthetic** | NeurIPS 级 vs AI slop、配色层级、留白、**"5 秒第一印象"是否真成立** | hero idea 名义存在但视觉不成立 |

## gate 之后仍不能直接交付

1. **你（orchestrator）必须亲自 Read PNG**，多镜头 agent 也有盲区。实测：orchestrator 自己修完一张图后亲眼自审，仍漏掉了自己引入的"公式出框"回归，是再跑一轮独立审查才抓到。**④.5 的"用户的视觉是最后闸门 / 单视角自评不可靠"对你（orchestrator）同样成立。**
2. triage checker 误报（见 SKILL.md ④.5 的"overlap.json 处理"规则 + 步骤 ④ 的 `pdf-overlap-checker.py`：数学 glyph text-overlap、heatmap/matrix line-through-node、Sankey 汇聚、锥穿环边界，均为已知 FP）。
3. 综合 = 你的眼 + 4 镜头 + checker triage → 真 blocker 列表 → 回 ④ 修 → **改完再跑一轮 gate**（改动常引入新 bug）。
4. gate + 你 + checker 全 0 真 blocker 后，**仍把图先给用户看**（用户是最后闸门）。

## 机制

用 Agent 工具 / workflow **真正并行 spawn 出 4 个独立子 agent**（每镜头喂 PNG 路径 + 该图"应有模型"让 semantic 独立重算）。**关键是"另起 agent + 空白上下文 + 对抗 + 多视角"，这是 mode C 唯一奏效的兜底；同上下文自审多遍不算数（实测会连同 generator 一起漏）。**
