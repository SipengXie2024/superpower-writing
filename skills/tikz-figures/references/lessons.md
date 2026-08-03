# 通用踩坑教训

> **何时加载**：步骤②，任何 TikZ 图必加载。
> **写入规则**：只追加经过验证的事实，不写未确认猜测。按经验操作失败就更新或删除该条。
> 参数基线见 `baselines.md`，图型专属教训见 `lessons-by-type.md`，历史批次复审见 `lessons-archive.md`。

> （原 `evolution.md` + `experience-log.md` 已于 2026-03 合并，2026-08 按性质拆分为本组四个文件。）

---

#### [通用] - pgfonlayer 环境名
- **问题/发现**：背景层环境名是 `\begin{pgfonlayer}{background}`，不是 `\begin{pgfonbackgroundlayer}`。后者会编译报错但仍生成异常 PDF。
- **解决方案**：始终用 `\pgfdeclarelayer{background}` + `\pgfsetlayers{background,main}` + `\begin{pgfonlayer}{background}`。
- **发现日期**：2026-03-28

#### [通用] - 双方括号符号需 stmaryrd
- **问题/发现**：`\llbracket` / `\rrbracket`（⟦⟧）需要 `\usepackage{stmaryrd}`，否则报 "Undefined control sequence"。
- **解决方案**：密码学/形式化验证领域含 ⟦⟧ 时在 preamble 加 `\usepackage{stmaryrd}`。
- **发现日期**：2026-03-29

### 视觉层次/绘制顺序

#### [通用] - 同类线条共出发点更优雅
- **问题/发现**："强制不同锚点出发"规则反而让同色同型同方向的两条线变扭曲。
- **解决方案**：同类型线可以共享出发点——看起来更像"有意分发"。只有不同类型线（实 vs 虚）才需分开。规则不是死的，美感才是最终裁判。
- **发现日期**：2026-03-29

### 连线路径

#### [通用] - "能直就直"——对齐节点不要加不必要弯折
- **问题/发现**：源和目标完全垂直对齐，但箭头还是画了 L 型弯折。人一看就觉得多余。
- **解决方案**：画连线前先看源/目标 x/y 是否对齐。对齐则直线，不对齐才弯折。**每次弯折必须有理由（绕障碍物）**。
- **发现日期**：2026-03-29

#### [通用] - 弯折后线段太短导致箭头断在弯角
- **问题/发现**：弯折点紧挨着箭头尖，看起来像箭头断在了弯角。
- **解决方案**：弯折点到箭头尖之间 ≥ 0.8cm。空间不够则提前弯折让最后一段够长。
- **发现日期**：2026-03-29

#### [通用] - 标签有空间却还是重叠放置
- **问题/发现**：Yes/No 标签和线重叠、hub-spoke 标签和框重叠——明明旁边有空白。
- **解决方案**：放每个标签时必须看周围——有空白就挪过去。"有空间却重叠"是不应该的错误。
- **发现日期**：2026-03-29

#### [通用] - 箭头指向空气（没"够到"目标）
- **问题/发现**：自调用弧太短，终点在激活条外。
- **解决方案**：箭头终点必须落在目标元素边框上。目标太小则**扩大目标**（加宽激活条、加长框体），不要缩短箭头。
- **发现日期**：2026-03-29

#### [通用] - 树状分叉处线段断连和"空心方块"
- **问题/发现**：树状一分多用多个独立 `\draw` 时，每段继承全局 `shorten >=2pt`，交叉点出现可见间隙。分叉点用 `\node[circle/rectangle]` 会渲染为"空心方块"。
- **解决方案**：(1) 主干+横杆用**一条连续** `\draw[thick]`（不带 arrow、不带 shorten）；(2) 只有最终分支用 `\draw[arrow]`（继承 shorten）；(3) 分叉点用 `coordinate` 而非 `\node`——coordinate 不渲染任何形状。
- **发现日期**：2026-04-03

#### [通用] - 跨层连接区域拥挤
- **问题/发现**：树状分叉区多条线（gRPC、背书、准入验证）挤同一通道交叉重叠。
- **解决方案**：(1) 同一通道最多 3 条线；(2) 多条线同方向时用不同 x 的 rail（间距 ≥ 1.0cm）；(3) 同类连接（都是 gRPC）合并为一条线 + 标签。
- **发现日期**：2026-04-03

#### [通用] - 旋转文字侵入相邻区域
- **问题/发现**：联邦学习图 "Broadcast w_global" 竖排文字碰到右侧雷达图区域。旋转文字实际宽度难预估。
- **解决方案**：放置后检查旋转文字的四角是否侵入相邻元素。宁可多留 0.5cm 间距。
- **发现日期**：2026-03-31

### 信息密度

#### [通用] - 小标注过多导致全图重叠（设计野心过度）
- **问题/发现**：为追求信息密度在每个框旁加协议标注（.sol、sDfx invoke、inter blockchain 等），导致 7 处以上重叠。
- **解决方案**：(1) 小标注只在 ≥ 0.5cm 空白区添加；(2) 一个框旁最多 1 个外挂标注；(3) 自问"删掉所有小标注读者能理解吗？"——能就说明标注是可选的；(4) **干净 > 塞满**。
- **发现日期**：2026-04-03

#### [通用] - 同类功能箭头粗细不一致
- **问题/发现**：zkSNARK 图三个功能相似的箭头（Commit、Prove、Prover→Verifier）分别用 scale=1.2/1.5/0.8。
- **解决方案**：同类功能箭头**必须**统一 scale 和 line width——全局 style 中的 scale 值要适配最短的那条箭头。
- **发现日期**：2026-03-31

### 美感守恒

#### [迭代] - 修复一处不能破坏其它对齐/平行
- **问题/发现**：迭代修改中红色虚线和蓝色实线原本平行（美观），修改后不再平行（退步）。审查 agent 未发现这种退步。
- **解决方案**：每次迭代后检查修改是否破坏了已有的好效果（对称性、平行、间距均匀度）。**不允许修复一个 bug 引入另一个审美问题**。
- **发现日期**：2026-03-29

### 连线/箭头精度（Round 11 用户实测发现）

#### [通用] - Fan-out 多线必须用 tree pattern，禁止"扫帚式"散射
- **问题/发现**：MLP 节点扇出 3 条线到 3 个 task heads，3 条线从 `(fanout)` 同一点用 `(fanout) -- ++(0.55, 0) -- (target_y) -- (target.west)` 写，结果在 junction 附近 3 条线以不同角度散开，视觉上像"扫帚"——线段相互交叉、近距离干扰，读者要费力分辨。
- **禁止模式**：`(fanout) -- ++(0.55, 0) -- (target_y) -- (target.west)` 这种单 `\draw` 隐式斜线，3 条会撞角。
- **解决方案**：tree pattern (trunk + spine + stubs)。**完整代码模板和细则见** `tikz-global-rules.md` §"一对多分叉连线（树状扇出）" 和 §"多源汇聚→多目标扇出（沙漏树）"。
- **发现日期**：2026-05-16（MMAlign Round 11 用户视觉反馈）

#### [通用] - Junction dot 不被箭头 tip 戳——所有 dot-as-connector 场景
- **问题/发现 (Round 11, fan-in 场景)**：MLP → fanout dot 段用了 `arrow_main` 自带 `-{Stealth}` tip，箭头尖戳进 dot，视觉打架。
- **问题/发现 (R3-100 Batch 3, fan-out 起点)**：fig28 Mask R-CNN Box head 的 Y-fork: FC → dot → {class, bbox}，FC 出来那段水平箭头的 tip 戳进 dot——sub-agent 把 "junction dot 不被 tip 戳" 仅理解为 fan-in，忽略了 fan-out 起点也是同一规则
- **核心规则**：dot 周围**所有相邻线**都用 `\draw[thick, color=..., line width=...]` **不带** `-{Stealth}` tip，**无论 dot 是 fan-in 汇合还是 fan-out 起点**。tip **只**画在最终到达可见 target box (有 border) 的那一段。
- **dot 本身**：`\node[circle, fill=..., minimum size=4pt]`
- **适用**：fan-in、fan-out、Y-fork、T-junction、双向分流、所有 dot-as-connector 场景
- **E2 已强化**：覆盖 fan-out 起点的 dot（见 checklist）
- **发现日期**：2026-05-16 / 2026-05-18（Y-fork case 补充）

#### [通用] - 容器标题不能用 fill 嵌在容器边框上
- **问题/发现**：Hero 框标题用 `fill=acaOrangeFill!50, inner sep=2pt` 嵌在 hero 顶部边框处，白底盖住了橙色边框圆角，视觉上像 hero 框被"咬了一口"。
- **解决方案**：容器（zone/hero）标题**完全挪到容器外的白空间**（如 `at (center_x, top_y + 0.15)` anchor=south），**不要 fill**。这样：
  - 容器边框完整闭合
  - 标题可读性更好
  - 不破坏容器视觉完整性
- **发现日期**：2026-05-16

#### [通用] - 箭头 tip 刺入目标框：shorten 数值取决于端点类型

> ⚠️ **以下表格是 2026-05-16/17 历史经验值，已被 canonical template 取代**。
> 当前 `tikz-template.tex` 的 `arrow/.style` 使用 `shorten >=2pt`（TeX Live 2024 实测，
> 配合 `bending` library + `length=⟨dim⟩ ⟨line_width_factor⟩` 自动跟随 line width，
> 不再按端点类型分挡）。**冲突时以 `tikz-template.tex` 为准**——
> 不要回到手调 shorten >=6pt 的旧路径。本表保留作为历史教训背景，不作为执行依据。

- **问题/发现 (Round 1, 2026-05-16)**：节点图里 `shorten >=2pt` 配合 `Stealth[scale=1.1]` 端点指向 `node.west` 时，tip 出现在节点框内部。
- **问题/发现 (Round 2, 2026-05-17)**：Sequence 图里 `shorten >=6pt` 又**反过来**：指 Prover 等裸生命线时 tip 在生命线左侧 6pt 处悬空，看着像断线"线不够长"。
- **历史解决方案——按端点类型分**（已被 canonical template 取代）：
  | 端点类型 | shorten >= | 端点表达 |
  |---|---|---|
  | **节点图：node.west / node.east**（节点有可见边界）| **6pt** | `(target.west)` |
  | **Sequence: 激活条边缘**（命名节点的可见边）| **2pt** | `(actvVAuth.west &#124;- 0, y)` |
  | **Sequence: 裸生命线**（dashed 线无填充）| **2pt** | `(P.south &#124;- 0, y)` |
- **关键认识**：`shorten >=` 不是万能值。**端点是否有可见边界**决定数值——有边界（节点边、激活条边）需要更大 shorten 让 tip 在边外；无边界（裸生命线）小 shorten 让 tip 紧贴线。
- **当前 canonical 行动**：用 `tikz-template.tex` 的 `arrow/.style`，不要手写 shorten 数值。Sequence 图特殊端点（裸生命线）已被 `arrow short/.style` 覆盖（tip 3pt + shorten >=1pt）。
- 模板里 01/02/04/05/06 用 6pt（节点端点）；03-sequence 用 2pt（激活+生命线混合，端点用 `actv.east/.west` 或 `lifeline.south`）。
- **发现日期**：2026-05-16 / 2026-05-17（Round 2 细化）

#### [通用] - 双向箭头（contrastive、bidirectional flow）必须两端都有 tip
- **问题/发现**：MMAlign 对比损失 L_con 用 `arrow_contrast/.style={-{Stealth[scale=0.8]}, ...}` 只在一端有 tip，但 contrastive loss 语义上是双向的。视觉上看像单向流，误导读者。
- **解决方案**：表示双向/对称关系的箭头用 `{Stealth[scale=0.8]}-{Stealth[scale=0.8]}` 两端都画 tip。或者画两条独立单向箭头形成 ↔ 形式。
- **发现日期**：2026-05-16

### 并行 100 张测试发现（R3-100 批次，2026-05-17）

> 10 轮 × 10 并行 sub-agent 测试中浮现的新教训。命名 R3-XX 对应批次内第 XX 张图。

#### [元 / 语义核查] - 数学/几何图：Agent 应核查文案坐标是否满足方程
- **问题/发现 (R3-38 椭圆曲线点加, 2 轮，质量超预期)**：椭圆曲线点加 P+Q=R 示意图，原文案给的 P/Q/R 坐标**不在指定曲线上**（数学错误）。Agent 在第二轮绘制前发现坐标与方程 `y²=x³+ax+b` 不一致，重新计算了曲线上的真实点。
- **解决方案**：画数学/几何/密码学示意图时，agent 在绘制前**必须核查**：
  - 文案给的坐标/参数**是否满足声明的方程或约束**
  - 几何关系（"垂直"、"切线"、"中点"等）**是否成立**
  - 不一致时**先纠正再画**，并在交付时说明：例如 "原文案 P=(2,1) 不在 y²=x³+x+1 上（实际 y²=11 而非 1），已改为 P=(0,1)"
- **关键认识**：这不是"超出任务范围"，是**质量保证的一部分**。复刻一张错误的图等于扩散错误。
- **适用**：几何示意、椭圆曲线、复平面图、向量空间、相图、力学示意等"坐标/参数必须满足某方程"的场景。
- **发现日期**：2026-05-17

### R3-100 Pilot 主 agent 三遍复审发现（2026-05-17）

> 主 agent 对 10 张 sub-agent 自审通过的图做 3 遍审查后发现的盲区。这些问题 sub-agent 的 ④.5 视觉评审**全部漏过**，但用户/主 agent 一眼能看出来 — 提示视觉评审清单需要加强。

#### [通用] 自由浮动 annotation / callout 必须有 leader line 引到具体元素
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig07 ASR "Masked Self-Attn + Cross-Attn + FFN" callout 浮在 decoder 右边没引线
  - fig08 ECDSA 右栏 "Shamir SSS:" / "Paillier HE:" / "ECDSA combine:" 三段说明仅靠 y 对齐隐式关联
  - fig10 突触图 1-6 步骤编号在右栏纯文字描述，没有任何 leader 连到 anatomical 特征
- **解决方案**：所有**不直接相邻**的 annotation / callout / step number 必须用 dotted 或 dashed leader line 引到具体元素：
  - Hero substructure 展开 → dotted leader 从原模块 `.south` 到展开 panel `.north`
  - 多步骤解剖图 → 每编号 leader 连到对应特征，或编号直接放特征旁（≤ 0.3cm）
  - 右栏说明文字 → dotted leader 到对应模块
- **禁止**：自由浮动文字 + "靠 y 对齐推测关联"。这是读者认知负担最大的失败模式
- **发现日期**：2026-05-17

#### [通用] Hero substructure 必须真正"独一无二"，不要选通用结构做 hero
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig01 ViT 选 Stage 3 做 hero 展开 W-MSA — 但 4 个 stage 的 W-MSA 内部**完全一样**
  - fig07 ASR 选 "Layer 1 expanded" — 但 6 层 Transformer encoder 内部**全都一样**
- **错误模式**：从一组相同结构的多个 instance 里随机选一个标"Stage N 内部"或"Layer N expanded"
- **解决方案**：
  - 内部对所有 instance 都一样 → **不要绑定具体 instance**。标题写 **"通用展开 (Per-stage detail)" / "Layer internal (typical)"**
  - 某 instance 真有独特性（如 Stage 1 是 Patch Embed 而 Stage 2-4 是 Patch Merge；或 decoder 比 encoder 多 cross-attn）→ 选有独特性的那个，并在标题指出区别
- **触发场景**：Transformer encoder/decoder layers、Residual/Dense stages、序列里多个相同 block
- **发现日期**：2026-05-17

#### [通用] 多步骤被压缩成单一视觉元素时必须显式标注
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig05 糖酵解：第 4-5 步 (aldolase 拆糖 + TPI 异构) 被压缩成一个箭头段标 "aldolase / TPI"，丢失了"两个酶两步催化"的事实
  - fig06 Diffusion CFG："apply ε̂" 箭头从 CFG 公式只指向 x_t 一个 reverse 步骤 — 实际**每个**反向步骤都要 apply
- **解决方案**（优先级降序）：
  - **不压缩**：按真实步骤数全画
  - **必须压缩**：箭头/标签上**显式标注** `{4,5}` / `(2 substeps)` / `∀t` / "(applied at every reverse step)"
  - **配图注**：图 caption 写 "step 4-5 merged for clarity"
- **关键认识**：压缩节省视觉空间但丢失语义。**显式标注是必要补偿**，不标 = 视觉撒谎
- **发现日期**：2026-05-17

#### [通用] 箭头方向自评必须显式写 "tip 在哪一端"
- **问题/发现 (R3-100 Batch 2, fig18 NeRF)**：MLP 块的 input (x,d) → MLP 箭头和 MLP → output (σ,c) 箭头**两端 tip 都画反了**——tip 在 source 端而非 destination 端，视觉上像 "MLP 在往输入框送数据"。Sub-agent 自评 M3 "方向一致" 给的是 Y，但实际反了。
- **根因**：M3 原文 "源/目标方向和指令一致（不是反过来的）" 是抽象问题，自评容易脑补成 "数据流方向对吧"——但**箭头 tip 的实际几何位置**才是关键。
- **解决方案**：M3 强化为**强制 enumeration**——逐条线显式写 "input→MLP: tip at MLP.west ✓"。这种 "tip-at-which-end" 的具体语言让自评无法跳过。已更新 visual-review-checklist.md M3 语言。
- **发现日期**：2026-05-18

#### [通用] 窄 box 内的多词标签必须量字符数 vs 宽度
- **问题/发现 (R3-100 Batch 2, fig15 transformer block 面板)**：4 个标签 "multi-head attention" / "position-wise FFN" / "residual + layer norm around sublayer" / "dropout (p=0.1)" 在 ~2-2.5cm 宽的色块标签内**明显被切断**（PNG 渲染看得清清楚楚），但 sub-agent 自评 T4 "标签不被截断" 给的是 Y，35/35 全 Y。
- **根因**：T4 抽象问题"被截断吗"对长标签的自评不可靠——视觉上看 box，文字"看起来差不多塞进去了"。**实际溢出在 PDF 边界外，PNG 渲染时被裁掉**。自评看不到溢出部分。
- **解决方案**：T4 强化为**强制度量**——对每个 text width < 3cm 的标签盒，自评必须写 "label X (Ncm) in box (Mcm) → fit ✓/✗"。中文每字 ~0.4cm，英文每字 ~0.2cm。已更新 visual-review-checklist.md T4 语言。
- **触发场景**：右栏 annotation 标签盒、legend 项、emoji-style 色块标签
- **发现日期**：2026-05-18

#### [Legend] 多个 legend 框间距不足看起来像被分割的大框（A5 盲区）
- **问题/发现 (R3-100 Batch 2 用户复审, fig17 Merkle tree)**：图底部有两个 legend 框紧贴放置——左框"Authentication path (target → root)"，右框"Target/path node + Sibling (proof element)"。两框间距 < 0.3cm，视觉上**像一个被竖线分割的大框**而不是两个独立 legend 组。
- **解决方案**（任选）：
  1. **合并为单个 legend 框**：所有 legend 项放进一个框内，用 column 分隔
  2. **两个独立框 + 横向间距 ≥1cm**：明显分离，让读者识别为两组
- **A5 已加入 checklist**
- **发现日期**：2026-05-18

#### [通用] 箭头/连线 — 深度调研后的 canonical 模板（替代 4 轮迭代规则）
- **背景**：Batch 3-6 用户连续复审中箭头末端问题反复出现，4 轮规则迭代（distance → size → shape → ...）治标不治本。2026-05-18 做深度调研（PGF/TikZ 官方文档 + PlotNeuralNet 实测 + arrows.meta + bending library），发现 **5 个根因** 都是我原规则没覆盖的：
  1. **`bending` library 没加载** — 不加载时 arrow tip 在曲线/弯折路径上用 `quick` 模式，几何上必然 mis-align（这是 fig58/60 箭头末端怪的根因之一）
  2. **scale 是错的调节量** — TikZ 原生设计是 `length=⟨dim⟩ ⟨line_width_factor⟩` 让 tip **跟着 line width 自动缩放**。我之前的 "scale 0.7-0.9 短箭头 / 1.0-1.3 长箭头" 跟原生设计反着来
  3. **`width'` (带 prime) 让 tip 宽 = 长的比例** — 不是固定值。`width'=0pt 0.6` 保持完美三角比例
  4. **`sep` 参数处理 tip-to-border 间距** — 比 shorten 更精确，我之前完全没用
  5. **PlotNeuralNet (业界标杆) 用粗线 + 默认 tip** — `line width=0.8mm` + default Stealth。我推荐的细线 + 缩放 tip 路线反了
- **修订**：丢弃 4 轮迭代规则，用 **canonical pattern**（见 `tikz-template.tex` `arrow/.style`）：
  ```latex
  \usetikzlibrary{arrows.meta, bending}     % bending 必加
  arrow/.style={
      -{Stealth[length=5pt 1.5, width'=0pt 0.6, sep=0pt 0.5]},
      line width=1.0pt,
      shorten >=0pt 0.5,                    % 0.5×line_width
      color=black!70,
  }
  arrow thick/.style={arrow, line width=1.6pt}    % 主流
  arrow thin/.style={arrow, line width=0.6pt}     % 细节
  ```
- **关键认识**：**调 line width**（0.6 / 1.0 / 1.6 pt 三档），不调 tip scale；tip 通过 `<dim> <line_width_factor>` 语法自动跟随。这跟前 4 轮规则根本路线不同
- **E9 简化**：不再要求"分类箭头长度 → 选 scale → 选形状"。改为：**所有箭头一律用 canonical pattern，自评只检查 line width 选档是否合理**
- **发现日期**：2026-05-18（深度调研产物，前 4 轮 Batch 3-6 教训汇入）

#### [重叠] S3 自评不可靠 — 必须强制枚举每处重叠
- **问题/发现 (R3-100 Batch 6, fig55 cache hierarchy / fig58 CLIP / fig60 MapReduce)**：3 张图 sub-agent 自评 S3=Y，用户全部能看到重叠。S3 "节点框不重叠" 是抽象问题，被印象判断滑过
- **重叠类型**：(a) box vs box，(b) text vs line，(c) leader vs unrelated element，(d) annotation vs background zone
- **S3 强化**：sub-agent 自评必须**逐一扫描整图标出每处视觉重叠**，写出 "N 处重叠：位置 / 类型" 或 "0 处重叠"。禁止"看起来没重叠"印象判断
- **发现日期**：2026-05-18

#### [通用] - `\foreach` 内使用 xcolor 颜色名变量必定失败

- **问题/发现**：AlphaFold 图中氨基酸序列条用 `\foreach \col in {barBlue,...}` 循环，xcolor 无法在 `\foreach` 展开中解析多 token 颜色名（如 `barGreen`、`acaBlueLine`），触发 `! Package xcolor Error: Undefined color 'barGreen '`（注意末尾有空格）。同样问题出现在分子图原子颜色循环中。
- **解决方案**：凡是需要逐元素使用不同颜色的场合，**放弃 `\foreach` 循环，改为每个元素单独写 `\fill[barBlue!70,...] ... \node[...] {M};`**。代码量增加但编译稳定。共用颜色的循环（所有元素同色）不受影响。
- **发现日期**：2026-05-22

#### [通用] - `matrix` 实际行高大于 `minimum height`，手算坐标必然累积偏移

- **问题/发现**：用 `matrix of nodes` 画表格并设 `nodes={minimum height=3.4mm}`，按 3.4mm 手算第 n 行的 y 坐标去放箭头端点、高亮框、下方元素，结果越往下偏得越多。实测含下标的单元格（如 `$s_1$@$v_1$`）把行撑到约 3.95mm，四行下来累积偏移 0.22cm，箭头明显不在目标行的垂直中心，下方的框被压。`minimum height` 只是下限，内容更高时节点跟着长。
- **解决方案**：**任何依赖 matrix 行位置的元素一律用锚点，不要手算**。指向某一行用 `(mbox.east |- m-6-2)`，让 TikZ 自己取那一行的 y。相对某一行放节点用 `at (0.75,0 |- m-6-2)`。需要两行的中点用 `($(m-2-1)!0.5!(m-7-1)$)`（calc 库）。同理，`fit` 出来的外框底部也比按行高算的低，框下方的标题要用 `($(mbox.south)+(0,-0.2)$)` 而不是绝对 y。
- **发现日期**：2026-08-03

#### [通用] - `brace` 装饰的尖端画在路径行进方向的左手边

- **问题/发现**：想在图左侧画一个 `{` 把上下两行框起来，写 `\draw[decorate,decoration={brace}] (x,上) -- (x,下);`，渲染出来是 `}`（尖端朝右、开口朝左），方向正好相反。
- **解决方案**：brace 的尖端永远在**路径行进方向的左手边**。从上往下画时左手边是东（右），所以得到 `}`；把路径写成从下往上 `(x,下) -- (x,上)` 就得到 `{`。横向同理：从左往右画，尖端朝上。记不住方向时加 `mirror` 翻一次也可以，但改路径方向更直观。
- **发现日期**：2026-08-03

#### [通用] - 节点净间距小于箭头 tip 长度时，箭头被压成一个点

- **问题/发现**：两个圆节点圆心距 0.40cm、半径各 0.16cm，净线长只剩 0.08cm ≈ 2.3pt，而 `Stealth[length=4pt]` 的 tip 本身就要 4pt。渲染出来箭头挤成一个色块，完全看不出是箭头。表格单元格之间、小 DAG 的相邻节点之间最容易踩。
- **解决方案**：**净间距（圆心距减两个半径）至少留 3 倍 tip 长度**，即 `Stealth[length=4pt]` 要留 ≥ 0.4cm 净线长。空间实在不够时不要硬塞箭头，改布局：把目标节点挪到斜向（净距离变长），或者改用无箭头的连线表示关联。这次是把结算节点从正下方挪到右侧，净线长从 0.08cm 涨到 0.43cm。
- **发现日期**：2026-08-03

#### [通用] - 多行说明不套 `text width` 会把整张图的宽度撑爆

- **问题/发现**：在框里写 `\node[align=left] {placement drops a task into an interior gap, not only at a lane tail};`，以为 `align=left` 会折行，实际不会：这句 59 个字符在 `\scriptsize` 下排成一行 7.7cm，而框只有 3.5cm 宽，整张图从 504pt 撑到 531pt。`align=left` 只管已经分行的内容怎么对齐，不负责自动折行。
- **解决方案**：**凡是超过一个短语的说明文字，必须写 `text width=<框内宽>`**，让 TikZ 自动折行。框内宽取框宽减去两侧 padding，例如 3.5cm 的框配 `text width=31mm`。同时在 `tikzpicture` 上加 `every node/.append style={execute at begin node={\hyphenpenalty=10000\relax}}` 关掉断词，否则窄栏里会出现 `roll-back` 这种难看的折断（注意值要用花括号包起来，`execute at begin node=\hyphenpenalty=10000\relax` 会报 `Missing number`）。
- **发现日期**：2026-08-03

#### [通用] - `anchor=east` 的标签把 bounding box 向左扩，宽度超标却找不到源头

- **问题/发现**：图宽超预算 0.8cm，逐个检查右边所有元素都在范围内，怎么算都对不上。真正的原因在左边：泳道左侧的 `\node[anchor=east] at (-0.06,y) {core 1};` 让文字从 -0.81 延伸到 -0.06，画布左边界被拉到负数，总宽 = 右边界 - (-0.81)。
- **解决方案**：查宽度不要只看右边。`anchor=east` / `anchor=north east` 的标签、旋转过的节点、`amplitude` 较大的 brace 都会向负方向扩边界。习惯做法是让最左侧元素的左边缘落在 x=0：标签写成 `anchor=east at (0.80,y)`，主体从 0.86 开始。另外预览用 standalone 的 `border=Npt` 会给报告的尺寸多算 2N，脚本里要减掉再和栏宽比。
- **发现日期**：2026-08-03

