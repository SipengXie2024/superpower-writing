# 图型专属踩坑教训

> **何时加载**：步骤②，按当前图型**按需**加载对应条目，不必整份读。
> 通用教训见 `lessons.md`，参数基线见 `baselines.md`。

## 目录

<!-- toc -->

- **[三栏映射图]**（2 条）
- **[时序图]**（2 条）
- **[draw.io]**（1 条）
- **[几何图]**（2 条）
- **[分层架构图]**（1 条）
- **[英雄模块]**（1 条）
- **[数据可视化]**（5 条）
- **[密集架构]**（1 条）
- **[fanout 拓扑]**（1 条）
- **[时序图 / 多方协议]**（1 条）
- **[多分辨率金字塔 / FPN]**（1 条）
- **[解剖图 / 机制图 / 编号图]**（1 条）
- **[Hero sub-panel]**（1 条）
- **[Bio 图 / 化学图]**（1 条）
- **[递归/折叠类协议]**（1 条）
- **[长虚线 routing]**（1 条）
- **[Hero panel]**（1 条）
- **[复杂图]**（2 条）
- **[嵌入 viz]**（3 条）
- **[数据流水线图]**（2 条）
- **[表格/矩阵]**（1 条）
- **[泳道/甘特图]**（1 条）

---

#### [三栏映射图] - zone style 在 pgfonlayer 内失效
- **问题/发现**：`\begin{pgfonlayer}{background}` 内的 `\node[zone, fit=...]` 如果 `zone` style 含 `inner sep` 等参数，可能导致 zone 框不显示。
- **解决方案**：pgfonlayer 内直接内联 style（`\fill[dashed, thick, rounded corners=8pt, inner sep=15pt, ...]`），不依赖预定义的 `zone` style。
- **发现日期**：2026-03-28

#### [时序图] - 生命线最后绘制避免被遮挡
- **问题/发现**：TikZ 按代码顺序绘制，后画的在上层。生命线虚线被阶段背景 fill、combo 框、注释框遮挡。
- **解决方案**：所有 `\draw[lifeline=...]` 移到 `\end{tikzpicture}` 前最后位置。
- **发现日期**：2026-03-29

#### [时序图] - 消息标签默认不加白色背景
- **问题/发现**：`tag` style 用 `fill=white` 在生命线上会产生突兀的白色方块。
- **解决方案**：`tag` 默认无背景。仅当标签确实与生命线重叠且影响可读性时，才加 `fill=white, fill opacity=0.85`（半透明）。多数消息标签放在箭头上方不需要白底。
- **发现日期**：2026-03-29

#### [draw.io] - 箭头线覆盖文字（z-order 问题）
- **问题/发现**：draw.io 蓝色箭头线显示在模块文字上方，文字被遮挡。
- **解决方案**：XML 中先定义 edge，后定义 vertex——背景 < 连线 < 框体/文字。
- **发现日期**：2026-03-29

### 几何/装饰精度

#### [几何图] - 大括号方向搞反
- **问题/发现**：注意力机制图中 Q/K^T/V 的大括号开口方向不对。
- **解决方案**：`{` 开口朝右标注右侧，`}` 开口朝左。不确定时直接去掉改用文字标注——少一个有问题的装饰比多一个好。
- **发现日期**：2026-03-29

#### [几何图] - 辅助标注箭头不要死板指向正中心
- **问题/发现**：Merkle 树"兄弟节点"标签的箭头从左下方斜着插上去看起来僵硬。
- **解决方案**：辅助标注箭头可以指向 `.south west` 或 `[xshift=-3pt]node.south`，不需要精确对准正中心。像人手画一样自然。
- **发现日期**：2026-03-29

#### [分层架构图] - 反馈虚线绝不能穿过文字
- **问题/发现**：反馈虚线穿过多个层的文字标签，审查 agent 未发现。
- **解决方案**：虚线/反馈线必须逐段检查路径上有没有文字。**哪怕只穿过一个标签也必须改路径绕开**——虚线穿文字是最明显的排版问题。
- **发现日期**：2026-03-29

#### [英雄模块] - 宽框出箭头不要用 .east
- **问题/发现**：很宽的 hero 模块到右上/右下方目标的箭头从 `.east` 出发水平拉很远，像被强行拉过去。
- **解决方案**：从 `.north east` 或 `.south east` 出发向上/下再转。判断：从 `.east` 出发的箭头水平段 > 模块宽度 1/3 就换锚点。
- **发现日期**：2026-04-02

### 数据可视化细节

#### [数据可视化] - 中文标签自动换行字间距异常
- **问题/发现**：text width 强制换行中文 → "本 文 / 方 法" 字间距异常。
- **解决方案**：中文标签用 `\\` 手动换行或缩短为英文（`Ours`），不依赖 text width。
- **发现日期**：2026-04-02

#### [数据可视化] - 旋转文字居中需要 anchor=center
- **问题/发现**：`rotate=90` 文字用 `anchor=south` 时不居中、有偏移。
- **解决方案**：旋转文字要居中时用 `anchor=center`，不用 `south/north`。
- **发现日期**：2026-03-31

#### [数据可视化] - 旋转 y 轴标签 + 长中文，bbox 检测不准
- **问题/发现**：旋转 90° 的"准确率(%)"和刻度值重叠，pdf-overlap-checker 因旋转 bbox 提取不准未检出。
- **解决方案**：(1) 旋转标题统一 `xshift=-18pt`；(2) 长中文标题（≥4 字）改为不旋转、放轴上方水平显示。
- **发现日期**：2026-04-02

#### [数据可视化] - 迷你可视化标注不要用插值定位
- **问题/发现**：GAT 图注意力小图中数值标签放 edge 中间点（0.5-0.7 插值），刚好落在圆圈边缘上。
- **解决方案**：标注用 anchor 定位放外侧（如 `anchor=east at (node)+(-0.18,0)`），不用插值定位——插值容易落在元素边缘。
- **发现日期**：2026-03-31

### 树状/复杂拓扑

#### [密集架构] - 密集子块禁用箭头，用视觉触底+堆叠表达"流"
- **问题/发现 (R3-1 ResNet, 5 轮收敛)**：ResNet 类密集架构图有 50+ 子块（4 stages × 多个 residual blocks）。相邻子块间用 `shorten >=6pt` 箭头表达"数据流"时，箭头几乎与边框重合或刺入框；整图被箭头噪音淹没，读者看到的是箭头海而非架构。
- **解决方案**：
  - **子块紧贴排列**（视觉触底，gap < 1pt 或无 gap），**不画箭头**。读者从空间相邻+从左到右的阅读顺序自然推断"流"。
  - 只在**阶段间**（stage1 → stage2 这种粗粒度边界）画箭头，最多 3-5 条。
  - 适用：ResNet、DenseNet、EfficientNet 等密集 backbone；不适用：Transformer encoder（block 数少，箭头清晰可读）。
- **关键认识**：箭头是表达连接的工具，不是"数据流"的唯一表达。**相邻+阅读顺序**本身就是流。
- **发现日期**：2026-05-17

#### [fanout 拓扑] - Zone 标题在垂直 fanout 时不能放 zone 顶部，必须挪左侧空白栏
- **问题/发现 (R3-35 Threshold BLS, 5 轮收敛)**：BLS threshold 签名图里，3 个签名者垂直 fanout 进 aggregator zone。zone 标题（"Aggregator"）默认放 zone 顶部 anchor=north，结果 fanout trunk + spine 从 zone 顶边进入时压在标题下方，dot 与文字垂直撞角。
- **解决方案**：fanout 主轴穿过 zone 顶/底时，zone 标题挪到 **zone 西侧外的空白栏**：
  ```latex
  \node[anchor=east, font=\small\bfseries, rotate=90]
      at ($(zone.west) + (-0.15, 0)$) {Aggregator};
  ```
  或正常水平排版在 zone 西侧（如果空间允许）。
- **判断规则**：fanout 主轴（trunk + spine）的垂直方向 ⊥ zone 哪条边，标题就不能在那条边上。
- **发现日期**：2026-05-17

#### [三栏映射图] - 跨栏箭头标签放起点一侧或紧贴线，不要默认居中
- **问题/发现 (R3-8 Pretrain→Finetune→Eval, 4 轮收敛)**：三栏映射图的跨栏箭头（如 "downstream task"、"frozen weights"）标签 `pos=0.5` 居中时，刚好落在下一栏的 zone 边框（橙色虚线 `acaOrangeLine`）上撞色重叠。3 次迭代调整 pos 才避开。
- **解决方案**：跨栏箭头标签默认放法：
  - **起点一侧同栏内部**：`node[midway, above, pos=0.2]` — 标签在起点栏的栏内白空间，远离任何 zone 边线
  - 或**紧贴箭头线上方/下方**：`above=2pt` / `below=2pt`，垂直离 zone 边线 ≥ 3mm
  - **禁止**：默认 `pos=0.5` 居中（极易撞分栏线）
- **预防**：标签放置后视觉评审必看"标签是否与任何 zone 边线/分隔线距离 < 3mm"。
- **发现日期**：2026-05-17

#### [时序图 / 多方协议] 多目标广播（1-to-N）不能用单条双箭头曲线
- **问题/发现 (R3-100 主 agent 复审, fig03 PSI)**：消息 3 "MPC 协同计算" 用一条横跨 Alice-Bob 的弧线，**两端都带箭头 tip**。读者无法分辨："Verifier 广播给 Alice+Bob"还是"Alice ↔ Bob 双向交互"
- **解决方案**：1-to-N 广播必须用以下两种之一：
  - **方式 A (fork)**：源画 fork dot → N 条独立单向箭头到 N 个目标
  - **方式 B (独立)**：源直接画 N 条独立单向箭头分别到 N 个目标
- **禁止**：单条双箭头曲线表达广播 — `{Stealth}-{Stealth}` 双头曲线**专属于 ↔ 双向交互**，不可挪用
- **发现日期**：2026-05-17

#### [多分辨率金字塔 / FPN] 索引命名必须一一对应或显式标注分辨率
- **问题/发现 (R3-100 主 agent 复审, fig01)**：ViT Stage 1..4 → F_1..F_4 → P_2..P_5（**P 跳过 P_1**）。读者要心算 F_n ↔ P_{n+1} 映射。即使原 FPN paper 用 P_2..P_5 命名（对应 ResNet C_2..C_5），混用两种索引体系会增加阅读负担
- **解决方案**：
  - **统一索引**：Stage_i → F_i → P_i（全 1-based 或全 0-based）
  - **保留差异时显式分辨率**：F_n 旁边/下方写 `1/2^{n+1}` 或 `H/4, H/8, ...` 让 mapping 可推
- **触发场景**：FPN、Hourglass、U-Net skip connections、Pyramid Vision Transformer、HRNet
- **发现日期**：2026-05-17

#### [解剖图 / 机制图 / 编号图] 步骤编号必须有 leader 引到对应特征
- **问题/发现 (R3-100 主 agent 复审, fig10 突触)**：右栏 1-6 步描述完整（"AP arrives"、"Ca²⁺ flows"等），但**没有任何 leader line** 把数字连到图中对应的 AP 波形、Ca²⁺、囊泡、NT、Na+、EPSP 位置。读者必须"读文字 → 找特征 → 心算匹配"，认知负担巨大
- **解决方案**：
  - **方式 A (推荐)**：每个编号有 dotted leader 到对应特征中心
  - **方式 B**：编号直接嵌在特征旁（≤ 0.3cm 距离），无需 leader
  - **方式 C (退化)**：右栏文字描述每条加上 "(see 红圈 X)" 这类显式定位
- **禁止**：编号在右栏文字描述，靠"文字描述 + 特征外观"让读者自己映射
- **触发场景**：解剖图、信号通路图、装配/分解图、考古示意、任何"按步骤索引特征"的图
- **发现日期**：2026-05-17

### R3-100 Pilot Batch 2 主 agent 复审发现（2026-05-18）

> Batch 2（fig11-20）⭐ 5 项 (E3/E7/E8/M8/M9) **100% 被 sub-agent 主动遵守**——E7/E8 用 endpoint dots、M8 用"通用展开"标题、M9 用 fork+独立箭头，模式全部对了。但 3 遍复审又找到 2 类新盲区，需要强化已有清单项。

#### [Hero sub-panel] 小盒子内连线穿过盒内文字（S2 盲区）
- **问题/发现 (R3-100 Batch 2 用户复审, fig11 YOLOv8 CSP Block)**：hero sub-panel 里有 "Split"、"Bottleneck"、"1×1 Conv" 等小盒子（宽 ~1.2cm），连线从 .east → 下一盒.west 时，**连线的 y 坐标和盒内 label 的 y 坐标重合**，渲染出来线段在 label 文字上压过去，视觉效果像 strikethrough（"Sp̶l̶i̶t̶"）。
- **根因**：小盒子文字 `anchor=center` 时 y = box.center.y；连线锚点 `.east` / `.west` 也在 box.center.y → 同 y 重叠。S2 自评时 sub-agent 把 S2 理解为"外部连线穿过 free-floating 文字"，没盯 hero sub-panel **盒子内部**——35/35 Y 漏检。
- **解决方案**（任选）：
  1. 加宽盒子至 ≥2cm，**或**降低 label 字号让 label 占盒高 <50%（留 padding 区让连线走 box.north 或 box.south 锚点）
  2. 连线锚点用 `.north east` / `.south west` 等**偏 y 的锚点**而非 `.east` / `.west`
  3. 连线 y 偏移：`($(box.east)+(0,0.3cm)$) -- ...`，避开盒中文字
  4. label 用 `anchor=south` 放盒顶 + label 字号缩小
- **S2 已强化**：sub-agent 自评必须显式"hero sub-panel 内每个小盒"逐一确认线不穿字
- **发现日期**：2026-05-18

#### [Bio 图 / 化学图] 功能性标签 vs 粒子符号区分对待
- **问题/发现 (R3-100 Batch 2 用户复审, fig20 光合作用 Z-scheme)**：图中有两类视觉上类似的文字标签，但语义不同：
  - **粒子符号** ("H⁺"、"Ca²⁺"、"O₂")：表示溶液里实际存在的离子/分子，散落在 lumen/stroma 空间。**不需要 leader**——它们是图的内容，不是注释
  - **功能性标注** ("H⁺ pump"、"H⁺ flow"、"oxidation"、"electron transport")：描述某个过程或方向的注释。**必须有 leader** 到对应的箭头/通道——否则就是 fig07/fig08 那种自由浮动 callout
- **fig20 漏检**：5 个 "H⁺" 符号无 leader（正确，是离子）但 "H⁺ pump" 和 "H⁺ flow" 也无 leader（错误，是功能性标注），sub-agent 把它们和粒子符号混为一类
- **判断规则**：
  - 含名词 + 动词（pump、flow、transport、release）→ 功能标注，要 leader
  - 纯化学式（H⁺、Na⁺、ATP、NADPH）→ 粒子符号，不要 leader
- **E7 适用扩展**：自评 E7 时要分类，不能简单"散落文字都不要 leader"
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 3 用户复审发现（2026-05-18）

> Batch 3 主 agent 3-pass audit 自评 0 盲区，但用户红框标出 5 张图（fig23/26/27/28/29）的同一类问题。我的 audit 看的是 "是否有 fanout/leader/hero 错误"，没逐对箭头量 "tip 离 box 边的实际像素距离"。本节是这个共同问题的沉淀。

#### [递归/折叠类协议] zone 中间出现大块空白——bottom info box 锁底 + 内容指数衰减
- **问题/发现 (R3-100 Batch 3 用户复审, fig22 Bulletproofs IPA)**：IPA 有 4 轮 (n=8 → 4 → 2 → 1)，向量盒数按 2^k 衰减。Round 1 占满，Round 4 只剩 2 个小盒。但 **折叠规则 + 通信复杂度 两个 info box 被锁在 zone 底部**，结果 Round 4 和 info box 之间出现 **>3cm 高的空白带**——明显违反 S6 "大块白色空带"，sub-agent 自评 Y 漏过
- **根因**：S6 抽象问题"有空白吗"自评不可靠；递归/折叠协议**天然内容衰减**，sub-agent 默认按最高那轮锁定 zone 高度，bottom info 锁底，中间空
- **解决方案**（任选）：
  - **方式 A (推荐)**：bottom info box **紧贴最末一轮内容**（不要锁 zone 底），整个 zone 高度自动压缩
  - **方式 B**：用空白区**补充半技术内容**——具体数值示例 / 中间 commitment 值 / 一轮的 step-by-step 计算细节，填补衰减留下的空间
  - **方式 C**：把 bottom info box **挪到 zone 外**（zone 紧贴最末一轮，info 在 zone 下方独立摆放）
- **判断规则**：递归类（IPA / Merkle fold / 二叉树聚合）+ 末尾节点远小于起始 → 强制检查"末尾内容到 zone 边距"
- **S6 已强化**：sub-agent 自评必须**显式量**每片连续空白的 width × height，> 3 × 2 cm 即 N，写出"在 X-Y 坐标范围有 W × H 空白"
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 4 用户复审发现（2026-05-18）

> Batch 4 用户红框找到的问题：tip 头大身子小（已合入上一节 E9 lesson 的 Batch 4 修订）+ 长虚线绕路。

#### [长虚线 routing] 不要绕图大半圈
- **问题/发现 (R3-100 Batch 4, fig36 Tacotron 2)**：residual skip 紫虚线从 Linear Projection.east 出发，**绕图大半圈**——上 → 右过 Stop Token → 上方过 PostNet → 下到 ⊕。路径长，转折 ≥3 次，与其它箭头多次交叉
- **判断信号**：同源同目标虚线**绕过 ≥3 个无关元素** 或 **转折 ≥3 次**
- **解决方案**：见 checklist **E10** — 缩短直连 / lane 归并 / coordinate 分段
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 5 用户复审发现（2026-05-18）

> Batch 5: tip 精度/大小/形状 已合入上节统一 E9 lesson。本节为 Batch 5 新独立发现。

#### [Hero panel] 拒绝 side-dependency — 不要把支线挂在 hero 边框外
- **问题/发现 (R3-100 Batch 5, fig41 Swin V2)**：Hero 主流（Q/K/V → cosatt → softmax → AV → W_O → post-norm → y）时，sub-agent 把 "log-spaced CPB" 作为独立 box **挂在 hero 右侧**，跨边框虚线连回 cosatt。结果：hero 视觉边界外溢，主流和支线纠缠
- **解决方案**（任选）：
  - **A (推荐)**：把支线 inline 进主流（cosatt 步骤里直接列公式，不另起 CPB box）
  - **B**：CPB 挪出 hero panel，在 hero 下方独立小框 + 引线到 cosatt，明确"展开细节"语义
  - **C**：hero 横向放，CPB 在 hero **内部**做 inset，仍在 hero 边框内
- **禁止**：主流在 hero 内 + 支线 box 在 hero 外 + 跨边框虚线 — 视觉边界破坏
- **发现日期**：2026-05-18

#### [复杂图] - 残差 skip 线必须走 zone 之间的间隙，不能走 zone 内部

- **问题/发现**：Batch 17 fig153 v2：residual skip 连线设定 x=4.25（在 attention subzone 内，zone 左边=4.15），导致竖线穿过 Q/K/V 节点 → `line-through-node` 8 处。
- **解决方案**：残差 skip 竖线的 x 坐标必须落在 **hero 外框与 subzone 之间的间隙**（如 hero.left=3.8, subzone.left=4.15，则 skip x=3.97，落在间隙 [3.8, 4.15] 中）。同理右侧 skip x 落在 subzone.right 和 hero.right 之间。
- **发现日期**：2026-05-22

#### [嵌入 viz] - `dashed` zone 边框在 `pdf-overlap-checker` 中会误报 line-through-node

- **问题/发现**：`\draw[dashed] (x0,y0) rectangle (x1,y1)` 的水平边段会穿过 zone 内所有节点，触发 line-through-node。
- **处理方式**：这是已知语义误报。批量 ignore：`"N 处 line-through-node 全部来自 dashed 子区背景框与其包含节点的几何相交，属于 zone 边界设计而非路由错误"`。
- **发现日期**：2026-05-22

#### [嵌入 viz] - RoPE / GQA embedded viz 放置坐标需精确预算防 node-overlap

- **问题/发现**：RoPE viz 中心=(4.75,5.2), width=2.8cm → x范围[3.35,6.15]；GQA viz 中心=(7.65,5.2), width=3.0cm → x范围[6.15,9.15]。两个 viz 的 x 范围在 6.15 重合 → node-overlap。
- **解决方案**：放置 embedded viz 前先算出 (center_x ± half_width) 范围，确保两个 viz 之间间隙 ≥ 0.3cm。
- **发现日期**：2026-05-22

#### [数据可视化] - 热力图格子在 background layer 被可视化框填充色覆盖

- **问题/发现**：在 `\begin{pgfonlayer}{background}` 中绘制热力图格子（`\fill[heatDeep] ... rectangle`），同时用 `\node[viz_box, fill=zoneBlueBg]` 定义可视化框，框的背景填充覆盖了热力图格子（TikZ background layer 按代码顺序绘制）。渲染结果：heatmap 区域一片空白。
- **解决方案**：不用 `\node[viz_box, fill=...]` 定义可视化框，改用 `\draw[fill=..., draw=...]` 手动绘制框轮廓（置于 main layer），然后热力图格子用普通代码（main layer）绘制在框轮廓之后。这样格子永远在框背景色上方。核心规则：**热力图/柱状图等嵌入可视化必须在 main layer 绘制，不要放入 background layer**。
- **发现日期**：2026-05-22

#### [数据流水线图] - 柱状图 y 轴 scale 需所有面板统一

- **问题/发现**：RLHF 图中 3 个 benchmark 面板用了不同的 y 轴 scale（0-60% 对应不同 bar 高度），数值标签出现在轴线上方甚至溢出到图外，导致 text-overlap 和 text-overflow 错误。
- **解决方案**：多个并排柱状图面板必须用**统一的 y 轴 scale**（如 0-80%，统一换算公式 `height = value/max_val * axis_height`）。这不仅消除溢出错误，也让面板之间的比较更直观。
- **发现日期**：2026-05-22

#### [嵌入 viz] - hero 框内嵌入迷你 bar chart 位置需避开 sub-node

- **问题/发现**：RM hero 框内放了嵌入迷你 bar chart，初始 y 坐标与 sub-node (rmScore, rmEnc) 重叠，导致 text-overlap 错误（bar 标签与 sub-node 文字撞在一起）。
- **解决方案**：hero 框内有多个 sub-node 时，嵌入可视化应放在 sub-node **之间的空白区域**（x 和 y 都错开）。提前规划 hero 框内各元素的 x/y 坐标，留出迷你图的位置。
- **发现日期**：2026-05-22

#### [数据流水线图] - 节点名包含小数点导致 "No shape named" 错误

- **问题/发现**：流水线底部摘要条用 `\foreach \xp in {0.6,4.1,16.0,...}` 生成节点，TikZ 把 `\xp` 值（如 `16.0`）直接用作节点名，创建名为 `pipe16.0` 的形状，之后引用时报 `! Package pgf Error: No shape named 'pipe16' is known`。
- **解决方案**：流水线节点名必须是合法标识符（字母/数字/下划线，无小数点、空格）。将循环改为逐个命名节点：`pipeA`、`pipeB`、`pipeC`、`pipeD`、`pipeE`、`pipeF`，用绝对坐标定位。或用 `\def\pipename{...}` 为每个位置单独定义名称。
- **发现日期**：2026-05-22

#### [复杂图] - hero 模块内部连线应绕边而非穿心

- **问题/发现**：AlphaFold Evoformer hero 框内 6 个 sub-node 堆叠（MSA Row Attention、MSA Col Attention、FFN、Triangular Attention、Triangular Mult Update、Pair FFN），连接 MSA 侧和 Pair 侧的内部反馈箭头直接垂直画，路径穿过中间 sub-node 的文字标签，pdf-overlap-checker 报 overlap WARNING。
- **解决方案**：hero 框内 sub-node 密集堆叠时，跨越多个 sub-node 的连线必须**从 sub-node 侧边绕行**（L 型路由）：先从起点 `.east` 或 `.west` 水平伸出 0.5-0.6cm（离开 sub-node 文字区），再垂直走到目标 y，再 `-|` 接回目标 `.east`/`.west`。不要直接 `.south` → `.north` 穿心连线。
- **发现日期**：2026-05-22

#### [表格/矩阵] - 对角相邻单元格的高亮框必然在角上重叠

- **问题/发现**：表格里要标出"第 2 行第 3 列写的槽"和"第 3 行第 2 列读的槽"是同一个，给两个单元格各画一个 `fit` 高亮框，两框在对角处的公共顶点必然叠出一小段双线，无论把 `inner sep` 调到多小都消不掉，因为相邻单元格本就共享边界。
- **解决方案**：三选一。（a）`inner sep=-1pt` 让框比单元格小一圈，向内缩开；（b）不画框，改画一条连线把两个单元格连起来，语义更明确；（c）只框其中一个，另一个用颜色或符号呼应。实践中 (a) 最省事，(b) 表达力最强但线太短时箭头会挤（见下一条）。
- **发现日期**：2026-08-03

#### [泳道/甘特图] - 泳道横铺满框宽时，跨泳道的连线无解

- **问题/发现**：画 k 条泳道占满框宽，想从第 2 条泳道的某个块引一条线到图上方的表格，试遍了从块顶垂直上去、从块侧面绕、走两条泳道之间的缝，每条路径都必须穿过第 1 条泳道上的块，因为第 1 条泳道横向没有空隙。
- **解决方案**：这是布局的结构性冲突，不是走线技巧能解决的，越调越乱。两个出路：（a）**换布局**，把"时间轴"和"要连过去的东西"从上下关系改成左右三列关系，连线变成短水平线；（b）**放弃连线**，用同色高亮 + 一句文字建立关联。判据是这张图是否同时在讲两件事，如果是，先拆职责再画（见 figure-rhetoric.md 的"一图一职责"）。
- **发现日期**：2026-08-03
