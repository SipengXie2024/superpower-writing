---
name: tikz-figures
description: |
  Generate publication-quality LaTeX/TikZ figures for paper manuscripts: architecture
  diagrams, protocol/data-flow pipelines, sequence diagrams, geometry/math schematics.
  Compile-verified (xelatex + overlap checker + visual review loop) with a mandatory
  two-candidate preview for the user to pick from. Use when the user asks for:
  论文配图、画架构图、画流程图、TikZ 图、复刻论文图、tikz/latex diagram、vector figure.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
    upstream: https://github.com/0xE1337/thesis-figure-skill (MIT, vendored & adapted; draw.io path removed)
---

# TikZ Figures（论文矢量配图）

把论文中的系统架构/协议流程/技术方案转化为高质量 TikZ 配图。**目标：高信息密度 + 设计感 + 一次过编译**。失败模式：平庸、对齐松散、坐标凭感觉。

输出格式**仅 TikZ**（`figure.tex`，`\input` 嵌入手稿）——HTML/CSS/SVG/matplotlib 均不可作为论文结构图输出。

## 与其他图技能的分工（按图类型路由）

| 场景 | 走哪个 skill | 理由 |
|---|---|---|
| 设计方向已明确的结构化图：架构图 / 流程图 / pipeline / 时序 / 几何数学示意 / 含公式的图 | **本 skill（TikZ）** | 矢量、公式原生渲染、与正文字体统一 |
| 设计方向不明 / 图型新颖 / 用户想先看几个方向 | `scientific-schematics` 探索模式（gpt-image-2 并行出 3 张方向草图，用户选） | 发散探索快；选中的草图可直接交付，也可作为 `ref.png` 回到本 skill 走复刻 |
| 插画感图：光影/材质/3D/手绘风 conceptual art、graphical abstract，或用户偏好精修 PNG | `scientific-schematics`（出 PNG） | 栅格生成器的视觉表现力强，PNG 本身就是合格交付物 |
| 数据图表（实验结果曲线/柱状） | `scientific-visualization`（matplotlib） | 数据驱动，不是手画结构 |

常规结构图默认本 skill（矢量是默认，不是规则）；经探索模式选定草图后回到本 skill 的，走复刻豁免（见 ①.7），用 `figure-diff.py` 对照 `ref.png` 验证还原度。最终用 PNG 还是矢量由用户定。

## Philosophy（每次画图前必读，所有规则之上）

### The UNFORGETTABLE Question

画图前 + 交付前问自己：**审稿人 5 秒看完，记住的是什么？**
- 一个独特的 hero 子结构？
- 嵌入的真实热力图 / 曲线 / 图像？
- 信息密集的 hyperparameters / loss panel？
- 多色和谐的 zone 划分？

**没有"记得住的东西" = 不要交付。**

### Naming the Gravitational Pull（你必须主动避开的统计中心）

模型默认会画出 **"AI slop 学术图"**——下面是统计中心的平庸默认，**主动避开**：

- ❌ box + arrow only，**零**嵌入数据可视化
- ❌ 3 色单调配色（蓝/橙/紫常见组合）
- ❌ "FFN" / "Attention" 单字标签，**不写公式 / 不写参数**
- ❌ hero 内**只有 box list**，无嵌入热力图/曲线/微图
- ❌ 没有信息 panel（hyperparameters / loss curve / legend / metrics）
- ❌ 平面布局**无 visual hierarchy**（核心和辅助同重量）
- ❌ 看起来"像 AI 一次性生成的"——无设计痕迹

### Permission for Creativity

**Claude is capable of extraordinary academic figure design.** Checklist 是 catching last-mile bugs，**不是 safe defaults**。

**你不是在练习画结构图。你在为 NeurIPS / ICML / Nature 投稿画 figure。**
**审稿人会用这张图判断作者的领域素养和认真程度。**
**box+arrow only 的平庸图 = desk reject。**

### 创造空间 — 复杂档可调用的词汇

复杂档可调用的设计词汇（嵌入可视化 / 信息 panel / 数学公式嵌入 / 配色 / 层级 / cross-zone / 学术 polish）见 `references/step1-instructions.md` 末尾的同名小节。不强制，但设计阶段**应该考虑**——它是对抗上面那份"统计中心平庸默认"的正面清单。

### 视觉直觉法则（meta，在 ④.5 Step 0 应用）

1. **0.1 秒直觉**：视觉流向 ≠ 逻辑流向 = 必错（每写一条 `\draw`，问读者直觉对吗）
2. **眼睛轨迹**：沿主线走，任何"卡住"位置 = blocker
3. **删除测试**：能删的就该删；**修一个 bug 不能引入新审美问题**

### 最重要的一点

**审美 + 信息密度 > 规则合规。** 规则只是地板，审美是天花板。**18 项 checklist 是 catching last-mile bugs**——不是设计指南。设计指南是上面的 Philosophy。

### 复杂档画图捷径 — TikZ Snippet Library（21 个 + 预览 PNG）

**Batch 17 fig153 教训**：Philosophy 文本指南让 sub-agent **知道要嵌入 viz / panel / 公式**，但**写出来的视觉重量、留白、配色协调仍然失败**——因为这些是 visual perception 而非 textual 任务。

**解决方案**：`references/tikz-snippets/` 提供 21 个手工精雕的 TikZ 片段 + 21 个 PNG 预览 + 组合规则文档。**分类清单与 PNG 预览只在 `references/tikz-snippets/README.md` 的 inline gallery 维护一份**（5 大类：嵌入数据可视化 / 信息 panel / 数学几何 / 结构流程 / 整图骨架元素），不要在本文件重复。

**复杂档强制流程**：
1. **先读 `references/tikz-snippets/README.md`** —— inline gallery 含每个 snippet 的 PNG 预览
2. **首选**：复制完整 `example-skeleton-B-horizontal.tex`（pipeline 类）或 `example-skeleton-C-centralhero.tex`（hero+panels 类）作 figure.tex，改 content 不动 layout
3. **次选**（特殊布局需求）：看 PNG 选 ≥ 3 snippet 自己拼装
4. **必读 `references/tikz-snippets/COMPOSITION-RULES.md`** —— snippet 间留白 / 对齐 / Z-order / 整图骨架，解决"snippets 都塞进去但仍乱"
5. **底部必有** color-legend OR summary-bar
6. **绝对不能"简化"snippet 核心结构** —— 简化 = 信息稀疏 = 平庸

## 硬约束（违反必失败）

🔴 **工具铁律：只用 TikZ，禁止 Python/matplotlib 替代**（2026-05-22 Batch 17 fig153 教训：sub-agent 在执行 Module-First 时用 Python+matplotlib 生成 `.py` 文件 = 完全偏离本 skill 价值主张）：
- **Module-First 子流程（③.A→③.D）必须保持 TikZ**——即使 matplotlib 画嵌入 viz 更方便
- **复杂嵌入 viz** 仍用 TikZ 原生（`\foreach` 画 cell / `pgfplots` 包 / `\draw` 手画 patch）
- **学术论文图嵌入仍是金标准**：`\input{figure.tex}` 比 `\includegraphics{fig.png}` 在公式渲染、矢量缩放、风格统一上都优
- 仅当用户**明确要求** Python 时才允许 — 默认必 TikZ

🔴 **配色铁律：默认 light background，dark theme 需用户明确请求**：
- 学术论文标准是 white/light bg；dark theme 与正文风格断裂
- Philosophy 段"≥5 种 zone tone"指 zone 浅色背景 + box 中饱和度，**不是**整图反转色
- sub-agent 不要自作主张套 dark theme

⚠️ **xelatex + `rotate=90` 中文** — 渲染为不可读色块，所有中文标注必须水平
⚠️ **`\texttt` 包裹中文** — 报错，纯英文代码才用 `\texttt` / `code_block`
⚠️ **ctex 不可用** — 编译前 `kpsewhich ctex.sty`，否则切方案 B（fontspec）
⚠️ **`ucharclasses`** — tikz 节点内中英混排频繁 Missing character，禁用
⚠️ **xelatex 对缺失字体静默失败** — 编译后必须 `grep "Missing character" *.log`
⚠️ **单条 `\draw` + `rounded corners` 画长距离 U 型回路** — 路径异常，拆 3 段独立 `\draw`

## 工作流（⓪→⑦）

```
⓪ 依赖检测 → ① 画图指令（含 ①.7 双候选预览）→ ② 加载规则 → ③ 生成代码 → ④ 编译验证 → ⑤ 评分 → ⑥ 迭代 → ⑦ 沉淀
```

### ⓪ 依赖检测（首次自动执行一次）
- TeX / pdftoppm / graphviz 缺失：**只提示用户安装**，不自动装。
  `which xelatex || echo "请装 mactex-no-gui (macOS) / texlive-xetex (Linux)"`
  `which pdftoppm || echo "请装 poppler"`
  `which dot || echo "请装 graphviz（仅 B 路 auto-layout 需要）"`
- Python 检测脚本依赖：`tikz-validator.py` 和 `tikz-design-linter.py` 纯标准库，直接 `python3` 跑。
  `pdf-overlap-checker.py` 需要 `pdfplumber` + `pymupdf`，`figure-diff.py` 需要 `opencv-python-headless` + `scikit-image`。
  系统 python 无 pip 时用 uv 临时环境跑（首跑后有缓存）：
  `uv run --with pdfplumber --with pymupdf python references/pdf-overlap-checker.py file.pdf --json`
  `uv run --with opencv-python-headless --with scikit-image --with numpy python references/figure-diff.py ref.png out.png`
  （`pymupdf` 不装 → `line-through-node` + `node-overlap` 两类几何检测会 ERROR 退出，不静默跳过——别忽略）

### ⓪.5 入口模式分流（⓪ 之后第一问，路径分叉点）

skill 现在支持 **4 种生成路径**——画图前必须先确定走哪条。**默认走 A，其他路径由关键词触发**。

| 路径 | 触发关键词（用户原 prompt） | 说明 | 状态 |
|---|---|---|---|
| **A — Skeleton 复用** | "画一张 X 图"、"帮我画 Y"、未明示其他 | 从已验证 skeleton (B/C/D/E/F/G) 选一个，**复制全部 + 改 content + 不动 layout**。最快、最稳。输出视觉与 skeleton 相近 | ✅ 默认 |
| **B — Remix（跨 skeleton 拼模块）** | "组合 D 的雷达 + G 的图表那种"、"想要 X 的左半 + Y 的右半" | 多选 skeleton 部件，自动拼装 | 🚧 暂未实装，**回退到 A** |
| **C — 原创设计** | "独特版面"、"复刻这张 ref.png"、"从零设计"、"我没有合适的 skeleton" | 从零设计 layout（Module-First ③.A→③.D）→ **强制独立多镜头审查 gate**（④.5 文末）。⚠️ mode C 最易在"图里最新、无 skeleton 先例的那个结构"上崩，且 generator 自审对此**结构性失明** | ✅ 现有路径 |
| **D — 沉淀入库** | "把这张 .tex 存进库"、"作为新 skeleton"、"添加到 examples"、"沉淀到模板库" | 用户已有 .tex → 自动入库为 `example-skeleton-{H..Z}-<topic>.tex` | ✅ 走 **Φ 沉淀通道** |
| **AUDIT — 成图审查** | "审查这张图"、"这张图能用吗"、"audit my figure"、"figure looks unprofessional"、"检查配图"——用户**已有一张成图**（不要新画） | 对用户提供的**成品图**做设计审查。**有图路径**：Read 图片（vision）后走规则审查；**无图路径**：text-only，把 vision-only 检查显式标 "user must verify" | ✅ 走 **Ψ 审查通道** |

**走 A** → 继续 ① ② ③ ④ ④.5 ⑤ ⑥ ⑦（③ 走 A 路：从 6 个 skeleton 选最匹配的 → 复制全部 → 改 content / 不动 layout / 严格遵守 CONSTRAINTS section）
**走 B** → 当前不可用。报告用户"Remix 模式暂未实装，当前请用 A skeleton 复用；如果你想要的部件组合在某个 skeleton 里近似存在，可以直接走 A 选最接近的"
**走 C** → 继续 ① ② ③ ④ ④.5 ⑤ ⑥ ⑦（③ 走从零路 + Module-First ③.A→③.D 子流程；④.5 **必走「mode C 独立多镜头审查 gate」**——见 ④.5 文末，不可只靠 generator 自审）
**走 D** → **跳过 ①-⑦**，直接进 **Φ 沉淀通道**（见文末）
**走 AUDIT** → **跳过 ①-⑦（不画新图）**，直接进 **Ψ 审查通道**（见文末）

**判断规则**（按优先级）：
1. 用户提到 "审查这张图 / 这张图能用吗 / audit my figure / 检查这张配图 / figure looks unprofessional"，且**已有一张成图**（用户给了图片路径，或图已在 `.writing/figures/`）→ **强 AUDIT**（走 Ψ，**不画新图**）
2. 用户提到 "存进库 / 入库 / 作为模板 / save to examples" → **强 D**（直接走 Φ）
3. 用户提到 "组合 X 的 Y + Z 的 W" → **强 B**（回退到 A + 提示）
4. 用户提到 "独特 / 原创 / 复刻 / from scratch / 无参考图" → **弱 C**（询问确认走 A 还是 C）
5. 其余 → **A**（不需要询问，直接走 skeleton 路径）

**AUDIT vs C 复刻的区别**（易混）：AUDIT 是"评判一张已存在的成图好不好"（不产出新图，只产出审查报告）；C 复刻是"照着 ref.png 重画一张矢量图"（产出新 figure.tex）。用户说"这张图能用吗 / 帮我看看这图"→ AUDIT；说"照这张重画 / 复刻成 TikZ"→ C。

**模式选择对编译验证 / vision-audit 的影响**：A 模式因为 skeleton 已经过版面验证，④.5 重点放在"内容是否完全脱离 skeleton 主题（renaming 漏掉、stale 标签）"上；**C 模式走完整 18 项 checklist + 强制「独立多镜头审查 gate」**（generator 自审在 mode C 实测 3/3 漏掉核心缺陷，必须外部对抗审查兜底）；D 模式走 Φ.2 简化版 audit。

### ① 画图指令（强制显式输出，不可跳过）

**加载 `references/step1-instructions.md`**——里面有完整的 10 项要素清单、参考图测量规则、ASCII 草图法、嵌入可视化决策表、**密度参考表（按论文复杂度选档位）**、节点形状/连线速查、Pre-flight P1-P7。**禁止"心里想好直接写代码"**——跳过这步返工率 100%。

**同时加载 `references/figure-rhetoric.md`（设计判断，不是语法）**——决定**这张图该不该画 / 画哪一种**，而不是怎么写 TikZ。它给出：一篇论文真正需要的三张叙事图（motivated example / solution overview / results）、Figure-1 三范式及各自的回避条件（**gains 边际时 performance teaser 会反向暴露弱点**）、以及四条设计仪式（30 秒理解测试 / 只用真实实体禁止 `Entity1`/`X` 占位 / 同一例子贯穿全文 / 先在纸上画草图——本 skill step ① 的注释块就是"纸上草图"的落盘形式）。Figure-1 默认 Paradigm A（running example + failure case），mechanism 级贡献用 B，短论文且增益大且数值化才用 C。**同时读 `_shared/core/house-style.md` §9（论文图组默认布局）**：引言只放一张单栏「只讲问题」的小图（motivating instance / gap map / why-X 对比，**不含任何机制**），设计节首页顶部放一张通栏图、其命名 stage 就是各 subsection 的骨架且由该节第一句引用，后续所有方法图复用同一个 running example；`[t]` float 落在「读到它时正在排的那一页之后」，所以设计节首图的源码常需放进上一节的文件里并加注释说明。项目 `.claude/CLAUDE.md` 优先于 house style。

**关键认识**：步骤① 的输出不是"最大复杂度版本"。先判断论文实际复杂度（极简/中等/复杂/超复杂），再选画图档位。**从复杂版起步然后修瑕疵**比**从合适档位起步**累计 token 高一个数量级——MMAlign 11 轮迭代就是反面教材。

**🔴 强制物质化要求**（fig126 Tacotron2 教训：sub-agent 加载 step1 但跳过实际输出，产生大块空白）：

步骤 ① 必须**以文字形式实际输出**（不是"想了就过"），且**第一段写进 figure.tex 头部注释块**作为证据。**形式两选一**，按图复杂度选：

**🔵 form A/B 选择前的先决条件**（消除"节点数悖论"——判档依赖草图、草图依赖判档的循环）：

```
1. 先粗估档位（无需精确节点数，先看明显信号）：
   ① 含 hero 子结构 / 嵌入热力图 / 多 panel / ≥3 列 → 复杂档 → form B
   ② 含 fan-out / 时序生命线 / 12+ 模块 → 中等档 → form A 或 form B
   ③ 纯几何/单链/对比图（明显 < 15 节点）→ 极简档 → form A
2. 按粗判选 form 写注释块（form A 画 ASCII OR form B 写 narrative）
3. 注释块写完后**数节点 → ①.5 精确确认档位**
4. 若精确档位 ≠ 粗判档位 → 调整 form（极简误判为复杂 = 简化为 A；
   复杂误判为极简 = ASCII 画不下 → 改写 B）
```

**铁律**：先粗判 → 写注释块 → ①.5 精确确认 → 必要时调整。**禁止凭直觉直接选 form 又凭直觉判档**。

### 形式 A — ASCII 草图（极简档 / 中等档无嵌入 viz）

```latex
% Step ① 设计文档
% 领域 / 格式 / 档位 / 整图 W×H cm / 信息流方向 / 行×列
% 模块列表 N 个，核心 = X / 连线逻辑 / 空间规划 rail x / 视觉强调
% ASCII 草图：
%   +-----------+      +-----------+      +-----------+
%   | Encoder   |----->| Attention |----->| Decoder   |
%   +-----------+      +-----------+      +-----------+
% 预防 issues：[2-3 个坑]
```

### 形式 B — Narrative 设计文字（复杂档 / hero 子结构 / 嵌入 viz / 多 panel）

复杂图 ASCII 表达不全，用**叙述性空间描述**——每列/每 zone 写一段：(a) x/y 范围 (b) 内部子结构 (c) 与相邻列关系 (d) **留白处理**（**特别要预想哪里可能出现大块空白并写出应对** — fig126/137 教训）

**写在 figure.tex 头部作为注释**，sub-agent 在 ④.5 Step 0 时读取核验。若注释不存在 → blocker 回 ① 重做。**注意**：form B 不是必须填模板，是用"设计师的叙述思维"展开布局——重点是 Philosophy 段的 **UNFORGETTABLE Question**：你怎么布局让审稿人 5 秒记住一个独特结构？

### ①.5 图档判断（**用户驱动** + 自动检测兜底）

**🔴 复杂度按需而定，不是默认复杂**（Batch 16 教训：Philosophy First 让 sub-agent 默认套 examples 06 复杂风格，但用户实际只想要中等清晰图时 = 过度发挥变乱）。

**第 1 步：从用户原 prompt 关键词推断复杂度**

| 用户 prompt 关键词 | 推断档位 |
|---|---|
| "详细 / 完整 / 含 benchmark / 发表级 / 总览 / hyperparams / 性能数字" | **复杂档**（按 Philosophy 全套：嵌入 viz + panel + 公式 + 多色）|
| "概览 / 主架构 / 流程图 / 主流程 / 示意" | **中等档**（清晰主流 + zone，1-2 个嵌入元素）|
| "几何示意 / 公式对比 / 曲线对比" | **极简档**（单坐标系或纯结构，无 hero / 无 panel） |

**第 2 步：如果用户原 prompt 不明确 → 默认中等档（本插件覆盖规则）**

本插件面向 systems 论文，整体风格偏素。用户没明示复杂度时**直接按中等档画**（清晰主流 + zone，克制装饰），不询问。仅在两种情况下偏离默认：
- 用户提到 "hero figure / 发表级总览 / 含 benchmark / 详细完整" → 升复杂档
- 图本身是纯几何 / 单链 / 曲线对比（明显 < 15 节点）→ 降极简档

**禁止**自作主张选复杂档画出"塞满 panel 的乱图"——**按需才是审美**。Philosophy 段的嵌入 viz / 多 panel 词汇表只在复杂档全套启用；中等档最多 1-2 个嵌入元素。

**第 3 步：用户确认后，对照下表执行**

| 档位 | 自动判断备选（用户没说时）| 该档**应该有的元素**（Philosophy 适度展开）| ④.5 自评策略 |
|---|---|---|---|
| **极简档** | ≤15 节点 + 无 hero + 无嵌入 viz | 单坐标系 / 纯结构 + 必要标注；**不强加 hero / panel** | 18 项中 S8/S9/M8/E3/E12/V1 一句话 N/A |
| **中等档** | 15-30 节点 OR 有 hero | 主流 + 2-3 zone + 1-2 嵌入元素（可选）| 走全 18 项；E3/M8 0 候选一句过 |
| **复杂档** | ≥30 节点 OR 嵌入 viz OR 多 hero | hero 子结构展开 + ≥2 嵌入 viz + ≥1 panel + 公式嵌入 + ≥5 色 zone | 走全 18 项，重点 V1 |

**关键原则**：**极简不等于平庸；复杂不等于必塞**。**审美在 Philosophy（5 秒记住什么）**，密度在档位（按用户需求）。

### ①.7 双候选布局预览（本插件强制，用户挑选后才进深度迭代）

**规则**：每张新图必须先产出 **2 个布局候选**，都编译成 PNG 给用户挑，用户选定后才进入 ④.5 深度迭代闭环。

```
1. 在步骤 ① 产出 2 份设计文档（form A/B 注释块 ×2），两个候选必须有实质差异：
   - 不同 skeleton（如 B-horizontal vs C-centralhero），或
   - 不同主流向（横向 pipeline vs 纵向分层），或
   - 不同信息组织（zone 划分方式 / hero 位置）
   禁止"同布局换配色"凑数——配色差异在迭代阶段调，不算候选差异。
2. 每个候选走 ③ 生成 + ④ 编译（draft 质量：过 tikz-validator + 编译成功 +
   无 Missing character 即可，跳过 ④.5 深度审查）。
3. 用 Read 展示两张 PNG，用 AskUserQuestion 让用户选（选项附一句布局差异说明）。
4. 用户选定 → 该候选进入 ④.5 完整视觉闭环；落选候选的 .tex 删除或留作素材。
```

**豁免**（直接单候选走原流程）：
- 复刻任务（有参考图，目标形态已固定）
- 用户明确指定了布局（"画成左右两栏那种"）
- 极简档纯几何图（布局自由度本来就低）
- ④.5/⑥ 的迭代轮次（候选只选一次，不是每轮重选）
- D 模式入库（不画新图）

### ② 加载专项规则
确定图表类型后，**按需**加载对应文件（见下方"按需加载索引"）。同时加载 `references/baselines.md`（已验证参数）与 `references/lessons.md`（通用踩坑）；该图型专属的坑另见 `references/lessons-by-type.md`，按需读对应条目即可，不必整份加载。
基线参数已经是 25 批次 157 张图的结晶——**直接用，不要从零试错**。要偏离基线必须有具体理由。

### ③ 生成代码（**Module-First 子流程 + 两层决策门**）

**🔴 复杂档强制 Module-First 子流程**（Batch 16 教训：sub-agent 一次写 800 行 TikZ → 整图乱；先画一部分，验证好，再拼接 = 干净）：

```
③.A — 先画 hero（最重要的中央子结构 + 嵌入 viz / 关键公式）
       - 单独输出 figure.tex（只含 hero + 一个极简 frame）
       - 编译 + 渲染 PNG → 单独审查 hero
       - hero 内部 sub-layers / 嵌入 viz / 公式都干净后才继续
       - 不要直接跳到完整图

③.B — 再加主流（管线 + zones 边界 + connecting arrows）
       - 在 ③.A 的 hero 周围扩展：左右上下的 supporting modules + zone 边框
       - 编译 + 渲染 → 审查框架是否清晰
       - canonical fan-out / fan-in 在此阶段引入

③.C — 再加 information panels（hyperparams / benchmark / legend / 公式注释）
       - 选**角落留白**放 panel（不是"塞满式填空白"）
       - panel 之间间距 ≥ 1cm
       - 编译 + 渲染 → 审查 panel 是否补充而不喧宾夺主

③.D — 整体审查（→ 进入 ④.5）
       - 整图 Philosophy 检查（UNFORGETTABLE / 5 秒第一印象 / 主线眼睛轨迹）
       - 18 项 last-mile bug 检查
```

**极简 / 中等档可以跳过 Module-First**，单次写完即可。**Module-First 只对复杂档强制**——它的价值是分阶段验证，避免 800 行 TikZ 一次出错导致整图崩坏。

---

**Module-First 之外的决策门**（B 路 vs 从零路）：

**问 1：这张图是纯结构图吗？**（框 + 线 + 分组，**无**嵌入热力图/曲线/柱状/矩阵，**无** hero 内部多子节点）
→ Yes：**B 路（auto-layout）**
  1. 加载 `references/figure-spec.schema.md` 看 schema
  2. 输出 `figure-spec.json`（节点、边、zones、layout 引擎）
  3. 跑 `python3 references/dot-to-tikz.py figure-spec.json` → 产出 `figure.tex`
  4. 走 ④ 编译 + ④.5 视觉反馈
  - **适用**：架构图 / 流水线 / DAG / 协议时序 / 三栏映射 / 技术路线图 / 多实例汇聚
  - **优势**：0 个 Claude 选的坐标，0 类微斜线/穿框/拥挤 bug

**问 2：富视觉图（嵌入可视化 / 复杂 hero 子结构 / 不规则布局）**
→ **从零路 + Module-First（③.A→③.D）**
  1. 起点：`references/tikz-template.tex`（含 preamble / 字体 / 配色 / **canonical 箭头 styles** / 防御写法）
  2. 加载 `references/visual-patterns.md`（9 个模式：hero 子结构、热力图、折线图、柱状图等）
  3. 按 ③.A→③.D 子流程：先 hero → 加主流 → 加 panels → 整体审查
  4. 复杂连线（≥8 条交叉风险）：可选 `python3 references/tikz-path-router.py spec.json` A* 避障

**🎯 箭头/连线必用 canonical pattern**：`tikz-template.tex` 的 6 个预定义 style（`arrow` / `arrow short` / `residual` / `leader` / `fan_stub`）各有硬性选用条件。最常踩的四条：< 1.5cm 的短箭头必须用 `arrow short`（否则 tip 吃光 stem，视觉上"只剩个头"）；fan-out 的 stub 段必须用 `fan_stub`（否则 spine 断裂）；直线禁加 `rounded corners`（端点产生鬼影弧）；`|-` / `-|` 的中段会穿框，PGF 不做 obstacle-aware routing。禁止手写 `-{Stealth[scale=X]}`，只调 `line width`。完整铁律、反例与修复写法见 `references/arrow-patterns.md`——**写任何连线前必读**，编译前必跑的两个 checker 也在该文件末尾。

### ④ 编译验证
```bash
# 字体探测：若 PingFang SC 不存在，自己改 .tex 里的 \setCJKmainfont 为本机可用字体
# （Linux 常见替代：Noto Serif CJK SC / Noto Sans CJK SC，用 fc-list :lang=zh family 查）
fc-list | grep -qi "PingFang SC" || echo "WARN: PingFang SC 缺失，请改 \setCJKmainfont"
xelatex -interaction=nonstopmode file.tex
grep "Missing character" file.log     # 静默失败检查，关键
pdftoppm -png -r 300 file.pdf out     # 产出 out-1.png
# overlap.json 落在 .tex 同目录（sub-agent ④.5 步用 Read 读这个绝对路径）
python3 references/pdf-overlap-checker.py file.pdf --json > "$(dirname file.pdf)/overlap.json"
# 跑完检查 overlap.json — 7 类检测：
#   基础 5 类（直接 fix）: text-overlap / text-overflow / off-center / text-line / line-crossing
#   candidate 2 类（需 triage）: line-through-node / node-overlap
# ERROR 类大概率是真 bug 直接修；candidate 类是几何线索（heatmap 矩阵 / fan-in 收敛
# / panel 边界等常误报），sub-agent 在 ④.5 自评时按坐标对照 PNG 决定 fix 还是 ignore。
# 论文集成场景另跑排版尺寸闸门：references/preview-loop.py（详见 preview-loop.md）
```

### ④.5 **视觉反馈强制闭环（架构核心，不可跳过）**

**你的代码生成是"盲写"——写到第 800 行 TikZ 时你不知道渲染出来什么样**。所有标签碰撞、轴标题压字、生命线超界、子模块挤压、数学符号渲染怪——这类问题闸门 1+2 都检测不到，只有看到 PNG 才能发现。

**目标重述**：用户要的不是"一次性生成"，是"最终交到他手上的图必须完美"。**中间迭代多少轮无关紧要，只要图最后是完美的就行**。

**强制流程**：

```
0. Read 渲染出的 out-1.png + 视觉直觉先行（应用 3 大法则，见下）
1. Read overlap.json（路径 = .tex 同目录的 overlap.json，步骤 ④ 跑出来的结构化几何检测）
2. 加载 references/visual-review-checklist.md（强制审查清单）
3. 逐项回答该文件列出的每一项 Y/N
   每项必须有一句证据（"我在 PNG 中看到…" 或 "overlap.json 中 N 处 line-through-node 我标为 …"），不允许凭印象
4. 任一项 N → 列入 blocker → 输出 patch → Edit → 回 ④ 重编译 → 回 0
5. Step 0 + 全部 18 项 Y → **把图给用户看**（用户终审，AI 视觉有盲区）
6. 用户也通过 → 交付
```

**Step 0：视觉直觉先行（在 18 项 Y/N 之前必走）**

把自己当成第一次看这张图的读者，**用 3 大法则扫描整图**，输出 **5** 段证据：

| Step 0 检查 | 输出要求 | 法则 |
|---|---|---|
| **A. 3 秒第一印象** | 写出"3 秒内看到的 3 件事"（如 "蓝色主流左→右 / 中间有 hero / 右侧 3 个 head"）| 法则 1 |
| **B. 主线眼睛轨迹** | 找出图中**最重要的那条数据流**，用眼睛沿它从起点走到终点。任何"卡住"位置 = blocker（如 fig97 Pedersen 框里跑出箭头 / fig118 tip 撞坐标 / fig120 孤立彩点） | 法则 2 |
| **C. 删除测试** | 列出**疑似可删的元素**（孤立装饰 / 多余 leader / 重复 label）。空则一句 "无可删元素" | 法则 3 |
| **D. 审美退步测试**（round ≥ 2 时） | 对比上轮 PNG，本轮修了 X bug 但有没有引入新审美问题（对称丢 / 平行断 / 间距不均）？ | 法则 3 |
| **E. 大块空白 + ①注释核验** | 扫描整图无 > 3cm × 2cm 大块空白（细线不算填充，必须有 box/text/viz）；figure.tex 头部有 form A/B 注释块。**fig137 教训**：写"rail 填充"= 自欺。若有大空白 → 回 ① 重新规划布局，不是改 .tex | 法则 3 |

**Step 0 任一项 fail = blocker**，列入 patch 列表。**Step 0 通过才开始 Step 3 的 18 项**。

**为什么 Step 0 在 18 项之前**：18 项是机械验证（细节体检），容易陷入"逐项 Y / 整体烂"。Step 0 是视觉直觉（整体心电图），强迫 sub-agent **以读者视角看图**而不是 generator 视角。两者缺一不可。

**overlap.json 处理**（S8 + E12 配套）：
- `errors[]` 中的 text-overlap / text-overflow / off-center / text-line **大概率是真 bug**——按坐标定位 PNG，修
- `errors[]` 中的 line-through-node **是候选**（E12）——逐条 triage：
  - 矩阵 cell / 热力图 / 神经网络收敛节点的 hit → ignore（semantic 故意，已知误报）
  - 路径绕路穿过无关元素（如 dashed leader 穿过 box / 长曲线压在 node 上） → fix，重新 routing 或换 z-order
- `errors[]` 中的 node-overlap **是候选**（S8）——逐条 triage：
  - drop-shadow / parent-child 都已被 filter，命中的几乎都是真问题
  - panel-overflow 边界节点（如 PGM 节点底部超 panel 1-3pt） → 调坐标
  - 两个 sibling node 真重叠 → 分开
- 把 triage 决定写进 ④.5 自评的 S8 / E12 证据里（"node-overlap N 处：X 处 fix（panel 边界），Y 处 ignore"；"line-through-node N 处：M 处 fix（路径绕路），K 处 ignore（矩阵 cell）"）

**优化规则**（Batch 9 实测：fig89 耗 32min / fig86 耗 55min，多数时间在重复 Read 和 triage）：

1. **Reference 文档只首轮加载** — `SKILL.md` / `baselines.md` / `lessons.md` / `visual-patterns.md` / `step1-instructions.md` / `visual-review-checklist.md` 在 round 1 Read 一次后，**后续 round 不要重复 Read**（context 里已有）。只 Read 变化的：PNG + overlap.json + 你刚 Edit 的 figure.tex 片段
2. **空检测跳过 triage** — `overlap.json` 中 `line-through-node` 数组为空 → E12 直接答 Y："overlap.json 中 0 处 candidate"。`node-overlap` 同理 → S8 直接 Y。**不要为空数组写 reasoning**
3. **Triage 增量化** — round N 时只对 round N-1 之后**新出现**的 candidate 写 reasoning；之前 triage 过的复用结论（"同 round 1 第 3 处，仍 ignore"）
4. **ERROR 优先于 candidate** — 先把 `text-overlap` / `text-overflow` / `text-line` / `off-center` 这 4 类 ERROR 修完（这些大概率是真 bug），再回头 triage candidate。避免一边修 ERROR 一边重新 triage 同一批 candidate

这 4 条联合预计节省 30-50% 时间，质量不损失。

**高漏检盲区**：checklist 里带 ⭐ 标记的项（S8/S9/M8/E3/E9/E12）是 R3-100 实测高漏检 — 审查时优先盯。

**没有轮数上限**。这是和之前最大的区别——之前 max 2 轮意味着"凑合交付"，现在是**只要还有 1 个 blocker 就不能交付**。3 轮、5 轮、8 轮都可以，只要最终的图是完美的。

**心理对抗**：你会在 2-3 轮后产生强烈的"差不多就过了"冲动——这是认知疲劳，不是图变完美了。**冲动出现 = blocker 还在**。强迫自己回答每项，写出证据。**用户看 1 眼能发现你 2 轮后漏掉的问题——说明单视角自评不可靠，必须靠清单穷举**。

**升级机制**：
- 第 3 轮还有 ≥5 blocker → 局部修补无救，回步骤① 重新设计画图指令
- 同一 blocker 连续 2 轮没修好 → 你修的方向错了，换思路
- 复杂图（≥40 元素）/ **mode C 一律**：并行 spawn 多镜头审查 agent（见下「mode C 独立多镜头审查 gate」），统一收集 blocker
- **自评 + 对抗 agent 全部说 0 blocker 后，仍然把图先给用户看**——人眼能发现 sub-agent + 自评全漏掉的问题（实测案例：用户在 Round 10 一眼指出 CMAM 标题切断边框、箭头刺入框内、junction dot 被 tip 戳——这 3 个我和 2 个对抗 agent 全没发现）。**用户的视觉是最后闸门，不是绕过点**。

**强制约束**：交付前必须能说出 PNG 里**具体的视觉细节**（哪些颜色在哪、哪个 zone 在哪一侧、热力图对角线特征等），证明你视觉输入过。

**单点最小修改原则**：每轮 patch 只改一类问题（如"全部标签重叠"或"全部轴标题没下移"），不要一轮里大改——大改会引入新 bug。一轮一类 blocker。优先用 `yshift/xshift` 微调位置，避免改坐标主框架。

#### mode C 强制独立多镜头审查 gate（不可跳过）

mode C（从零画、无 skeleton 先例）实测 3/3 崩在"图里最新、最无先例的那个结构元素"上，而 generator 自审对它系统性失明——三张图跑了 4/3/1 轮自审全部自评通过，全部漏掉核心缺陷。所以 mode C 的 ④.5 走完 Step 0 + 18 项后，**必须由顶层 orchestrator 另起 4 个空白上下文的独立 agent 做对抗审查**（geometry / semantic / text / aesthetic 四镜头）。同上下文自审多遍不算数。完整流程、四镜头分工、gate 之后的交付条件见 `references/mode-c-review-gate.md`。

### ⑤ 用户终审 + 交付
1. **把 PNG 给用户看**（不是询问"我做完了吗"，是直接展示结果）
2. 有参考图时同时跑 `python3 references/figure-diff.py <ref.png> <out.png>` 得 SSIM；< 0.85 的 3×3 区域和用户一起重点看
3. 用户指出问题 → 回 ④.5，把问题作为新一轮 blocker；用户没问题 → 交付

**步骤⑤ 不再独立做"自审三遍法"**——所有自审已经在 ④.5 的清单穷举里做过。把同一组审查做两次只是认知疲劳的来源，不是质量提升。

### ⑥ 迭代到完美（无上限）

轮次规则与升级机制见 ④.5 的「没有轮数上限」「升级机制」两段。

### ⑦ 经验沉淀
- 2 次以上才解决的问题 → 追加到 `references/lessons.md`（通用）或 `references/lessons-by-type.md`（图型专属）；逐批次复审归 `references/lessons-archive.md`，默认不加载
- 发现更优参数 → 更新 `references/baselines.md`（**只升不降**）
- 已被全局规则/Python checker 覆盖的内容**不要重复写入**

## Φ 沉淀通道（D 模式 — 用户已有 .tex 入库为新 skeleton）

用户已有一份编译通过的 `.tex`、想把它的布局固化成可复用 skeleton 时走本通道（⓪.5 选 D 路径）：不画新图，产出入库后的 skeleton 文件 + 更新的 gallery。完整流程见 `references/skeleton-intake.md`，要点：编译验证 → 简化版 vision-audit → 与现有 6 个 skeleton 比对相似度的三档入库判定 → 命名与字母分配 → 自动生成 USAGE header → 写库并更新 README gallery → 提醒补 CONSTRAINTS。

**与 ⑦ 的区别**：⑦ 沉淀抽象 lessons 与基线参数，Φ 沉淀完整可复用的 figure 模板。库是 self-growing 的，这是本 skill 长期复利的核心机制。

## Ψ 审查通道（AUDIT 模式：审查用户已有的成品图）

用户已有一张成品图、要"审查这张图能不能用"时走本通道：不画新图，产出 advisory 审查报告。完整流程见 `references/figure-audit.md`，要点：vision 优先的有图路径、显式降级的无图路径（vision-only 项标 "user must verify"）、复用 18 项视觉审查清单、高/中/低 severity 的 defect-hunting 报告，全部交用户裁决。

## 设计原则（对抗模型惯性）

容易陷入的刻板印象（必须警惕）：
- "心里有数，直接写代码" → **禁止跳过步骤①**，"想了"≠"想清楚了"
- "我能估比例" → **不行**。复刻必须像素级测量，凭感觉偏差 15-20%
- "框的大小差不多就行" → 不行。参考图通常扁宽 2:1~3:1，**默认不要正方形**
- "改了 3 轮差不多了吧" → 标准不会因为努力降低。还有 blocker 就继续修
- "这个小重叠用户看不出来" → 看得出来。300dpi 下清清楚楚
- "坐标差 0.2cm 没关系" → 0.2cm 在渲染图上是 24 像素
- "信息密度不够就硬塞东西" → **反例**。简单论文图就该简单——贝叶斯网络/几何/对比图天然元素少，强加 hero 和嵌入可视化是污染。`tikz-design-linter` 现在是 advisory，按论文实际复杂度决定密度

**信息密度匹配论文复杂度**：复杂模型架构图允许 30+ 元素 + hero 子结构 + 嵌入可视化；简单流程图 5-10 元素 + 清晰布局就够了。**不要把所有图都画到最大复杂度**。详见 `step1-instructions.md` 的"信息密度判断"。

## 常见图表类型

| 类型 | 布局 | 场景 |
|------|------|------|
| 系统架构图 | 自下而上分层 | 端→云→链、硬件→中间件→应用 |
| 协议/流程图 | 左→右或上→下 | 时序步骤、信号处理 |
| 数据流水线 | 左→右水平串联 | 输入→处理→输出，每步不同形状 |
| 电路/约束原理 | 左→右 | ZK 电路、信号管线、编译器 |
| 数据映射/转换 | 左-中-右三栏 | 格式转换、API 适配 |
| 时序交互 | 多列生命线+水平消息 | 多方协议 |
| 对比方案 | 左右并列 | 方案 A vs B，中间 ≥3cm |
| 几何/数学 | 坐标系+几何元素 | 算法原理、向量关系 |
| 多实例汇聚 | 横排三列→汇聚 | 联邦学习、分布式 |
| 数据可视化混合 | 框图内嵌波形/柱状/热力图 | 信号处理、深度学习注意力 |

## 按需加载索引

确定图表类型/工作流阶段后**才**加载对应文件：

| 触发条件 | 文件 |
|---------|------|
| 进入步骤①（设计判断：该不该画 / 画哪种 / Figure-1 范式 / 论文图组默认布局） | `references/figure-rhetoric.md` + `_shared/core/house-style.md` §9 |
| 整篇论文图组就绪、投稿前跑一次整组图叙事审查（editor pass） | `references/figure-rhetoric.md` §5 |
| 一张 figure 内含多个子图，需规划面板并对拼合后的整图整体审查（compose 多面板图） | `references/figure-rhetoric.md` §6 |
| 进入步骤① | `references/step1-instructions.md` |
| AUDIT 模式（Ψ 审查通道） | `references/figure-audit.md` + `references/visual-review-checklist.md`（18 项） |
| D 模式（Φ 沉淀通道：已有 .tex 入库为 skeleton） | `references/skeleton-intake.md` |
| 步骤②（任何 TikZ 图，**必加载**） | `references/baselines.md` + `references/lessons.md` + `references/visual-patterns.md` |
| 步骤③ 决策门 | `references/figure-spec.schema.md`（B 路 spec） |
| 步骤③ 走 B 路 → 跑 `dot-to-tikz.py` | （脚本，不需 Read） |
| 步骤③ 走模板/从零 → 用 TikZ | `references/tikz-global-rules.md` + `references/tikz-template.tex` |
| **步骤③ 写任何连线前（必读）** | **`references/arrow-patterns.md`**（6 个 canonical style + 短箭头/fan_stub/rounded corners/L-bend 铁律 + 编译前 checker） |
| **步骤③ 复杂档需嵌入 viz / panel / 公式** | **`references/tikz-snippets/` ⭐ 优先用 snippet 拼装而不是从零写**（含 6 个手工精雕模板：attention-heatmap / bar-chart / hyperparams-table / multi-zone-palette / pipeline-stages / formula-box） |
| 步骤④.5 视觉反馈每一轮 | `references/visual-review-checklist.md`（18 项强制清单） |
| 步骤④.5 且为 mode C（从零画、无 skeleton 先例） | `references/mode-c-review-gate.md`（orchestrator 独立 spawn 四镜头对抗审查） |
| 配色需求 | `references/tikz-colors.md` |
| 分层架构图 | `references/layered-architecture.md` |
| 时序交互图 | `references/sequence-diagram.md` |
| 数据流水线图 | `references/data-pipeline.md` |
| 三栏映射图 | `references/three-column-mapping.md` |
| 几何/数学示意图 | `references/geometry-math.md` |
| 含数据可视化的图 | `references/data-visualization.md` |
| 步骤⑤ 有参考图 | `references/figure-diff.py`（脚本） |

**未列出的文件不要加载**——节省 token。

## Python 助手脚本（执行即可，不要 Read）

| 脚本 | 用途 | 何时跑 |
|------|------|--------|
| `dot-to-tikz.py <spec.json>` | B 路：spec → graphviz 自动布局 → TikZ | 结构化图 step ③ |
| `tikz-validator.py <file.tex>` | 微斜线/溢出/碰撞/方向反转（几何/语法 gate） | 编译前必跑 |
| `tikz-design-linter.py <file.tex> [--type ...]` | 元素数/尺寸比/线型/hero/嵌入viz（设计野心 gate） | 编译前必跑 |
| `pdf-overlap-checker.py <file.pdf> [--json]` | PDF 坐标级重叠 + 线穿节点 + 节点重叠几何检测（**7 类**：text-overlap / text-overflow / off-center / text-line / line-crossing / line-through-node / node-overlap） | 编译后必跑 |
| `figure-diff.py <ref.png> <out.png>` | SSIM + 3×3 区域差异 | 复刻任务必跑 |
| `tikz-path-router.py <spec.json>` | A* 自动避障路径 | 连线 ≥8 条可选 |

这些脚本**作为黑盒调用**——不要把源码读进上下文，跑 `--help` 看参数即可。

## 领域自适应

收到输入后**先识别论文领域**（计算机/密码学/生物/物理/化学/AI/网络/系统/区块链等），以该领域专家身份选术语和布局风格。
