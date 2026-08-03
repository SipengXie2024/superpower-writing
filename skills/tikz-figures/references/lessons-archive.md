# 历史批次复审记录

> **何时加载**：默认不加载。只在追溯某条规则的来历、或复盘早期批次时查。
> 这里是逐批次的用户复审与元教训，其中已沉淀为规则的部分见 `lessons.md` 与 `tikz-global-rules.md`。

## 目录

<!-- toc -->

- **[E6 强化]**（1 条）
- **[T4 recurrence]**（1 条）
- **[E11 新增]**（1 条）
- **[E6 进一步]**（1 条）
- **[Batch 9]**（1 条）
- **[Batch 8 后续]**（1 条）
- **[Batch 13 用户复审 #2]**（1 条）
- **[Batch 13 用户反思]**（1 条）
- **[Batch 12 用户复审 #3]**（1 条）
- **[Batch 12 用户复审 #2]**（1 条）
- **[Batch 12 用户复审]**（1 条）
- **[Batch 11 用户复审]**（1 条）
- **[Batch 10 用户复审 #2]**（1 条）
- **[Batch 18 架构重思考]**（1 条）
- **[Batch 17 元教训 — TikZ 硬约束 + dark theme 禁忌]**（1 条）
- **[Batch 16 元教训 — 按需复杂度 + Module-First]**（1 条）
- **[Batch 15 元教训 — Philosophy First 重构]**（1 条）
- **[Batch 14 用户反馈]**（2 条）
- **[Batch 10 用户反馈]**（1 条）

---

#### [E6 强化] 任何 90° 弯折用 rounded corners，多 \draw 段共享坐标避免不连续
- **问题/发现 (R3-100 Batch 5, fig48 DETR)**：折线段在弯折处 sharp 90° 转角，看起来粗糙廉价；且多个 `\draw` 拼接的段之间出现**视觉不连续**（端点坐标手写，浮点误差致段间小空隙）
- **解决方案**：
  - **任何 90° 弯折**：`\draw[arrow, rounded corners=5pt]`（默认 0pt = sharp）
  - **多 `\draw` 段共享端点**：用 named coordinate (`\coordinate (mid) at (..., ...); \draw (A) -- (mid); \draw (mid) -- (B);`)，不要手写坐标拼接
  - **更优**：单 `\draw (A) -- (mid) -- (B)` 优于拆 2 个
- **E6 强化**：从"距离 ≥1.5cm 留 rounded"升级到"**所有 90° 必须 rounded + 段间共享坐标**"
- **发现日期**：2026-05-18

#### [T4 recurrence] 文字超出 box — 字符数算对了但 PNG 仍溢出
- **问题/发现 (R3-100 Batch 5, fig46 复现 Batch 2 fig15)**：T4 已强化为"对 < 3cm box 显式量字符数"，但 fig46 sub-agent 算 ✓ 后渲染仍溢出
- **应对**：T4 自评 = 算字符数 **+ 看 PNG 验证文字 visibility**。光算不够 — font 实际宽 / TeX padding / inner sep 都影响最终
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 6 用户复审发现（2026-05-18）

> Batch 6: Latex tip + rounded corners + hero no side-dep 等 Batch 5 规则全部被 sub-agent 主动应用。但用户红框点出 **9/10 张图**仍有问题，主要 3 类：重叠、路径不连续、虚线非 90°。**承认**：箭头末端规则迭代 4 轮（Stealth → scale → shape → ...）仍未根治，可能需要 concrete code template 而非更多 rules。

#### [E11 新增] 路径视觉连续性 — 多段 \draw 拼接出现断点
- **问题/发现 (R3-100 Batch 6, fig57 STARK)**：sub-agent 用多个 `\draw` 拼接 routing，端点坐标手写（浮点）→ 段间出现视觉断点；或路径被其它元素遮挡，没用 pgfonlayer 把路径放上层
- **解决方案**：
  - **方式 A (推荐)**：用 named coordinate (`\coordinate (mid) at (...);`)，所有段共享名字，浮点误差消失
  - **方式 B**：尽量用**单个 `\draw` 多段** `(A)--(mid)--(B)` 而不是拆 2 个 `\draw`
  - **方式 C**：路径若被其它元素遮挡 → `pgfonlayer{foreground}` 上层 OR 移动遮挡元素
- **E11 已加入 checklist**
- **发现日期**：2026-05-18

#### [E6 进一步] 虚线 routing 优先 90° 直角，禁用 Bezier 曲线
- **问题/发现 (R3-100 Batch 6, fig56 VQ-VAE)**：STE 虚线 arc 用 `to[bend left=45]` 或类似曲线 routing，本可用 90° L-bend with rounded corners. 用户："有些地方可以画 90 度，但是非要画了一个非 90 度的形状"
- **解决方案**：dashed leader / residual skip / reference 引线**首选 90° L-bend** (`\draw[dashed, rounded corners=5pt] (A) -| (mid) |- (B)` 或 `(A) -- (corner) -- (B)`)，**禁用** `to[bend left/right]` 或自由 Bezier
- **理由**：90° 直角 routing 视觉上"工整"，曲线 routing 在密集图中容易看起来"乱"
- **E6 强化**：从"90° 必须 rounded" 升级到 "**虚线 routing 默认 90° 直角，曲线只在明确语义场景用**"
- **发现日期**：2026-05-18

> Batch 6 元发现"箭头末端 4 轮迭代仍有问题，需要 concrete template" 已被 **2026-05-18 深度调研 resolved** — canonical pattern 落在 `tikz-template.tex`，详见上方 Batch 3 section 的 "[通用] 箭头/连线 — 深度调研后的 canonical 模板" lesson。

#### [Batch 9] 树状分叉 stub 和 spine 之间出现 1pt 视觉断裂
- **问题/发现 (R3-100 Batch 9, fig86 HiFi-GAN)**：MPD/MSD fan-in spine 上的 stub 用 `\draw[arrow]` 画——canonical `arrow/.style` 含 `shorten <=1pt`，导致 stub 起点离 spine **1pt** gap。300 DPI 下肉眼可见"分叉点处线断了"。用户在 PNG 一眼看出 4-5 张图都有这种断裂模式
- **根因**：`arrow/.style` 的 `shorten <=1pt` 是为节点 → 节点设计的（让线离 node 边 1pt 不贴边），但 spine → target 的 stub 起点**不是 node**而是 spine 上的精确点，shorten 把它向后挪 → 视觉 gap
- **解决方案**：`tikz-template.tex` 新加 `fan_stub/.style`：与 `arrow` 同 tip 但 **`shorten <=0pt`**（起点紧贴 spine）
  ```tex
  % spine 一条线，无 arrow 无 shorten
  \draw[line width=1.0pt, color=...] (left_x, y) -- (right_x, y);
  % 每条 stub 用 fan_stub
  \draw[fan_stub] (stub_x, y) -- (target.north);
  ```
- **避坑要点**：
  - ❌ 不要 `\draw[arrow] (x, spine_y) -- (target)` — 会有 1pt gap
  - ❌ 不要在 spine 中点放 `fill=white` 的 sum/junction 圆圈 — 圆圈截断 spine
  - ❌ 不要用多个独立 `\draw` 画主干+横杆 — 段间 shorten 制造间隙
- **E3 已加自评新增项**：每个 fan-out / fan-in 必须确认 "stub 起点和 spine **零 gap**" + "junction dot 颜色和 spine **一致** 或不放 dot"
- **发现日期**：2026-05-19

#### [Batch 8 后续] line-through-node 几何检测（pdf-overlap-checker 升级）
- **问题/发现 (R3-100 Batch 7+8, 用户复审)**：canonical 箭头模板上线后，箭头末端问题大幅改善；用户复审指出**剩余两类问题**：① 框/文字/线之间**重叠** ② **线穿过路径**（z-order + 路径绕路）。`visual-review-checklist.md` 的 S3 强枚举 + E11 共享 named coord 缓解了一部分，但**几何穿过仍要靠几何检测**——靠自评清单容易漏（fig80 apoptosis 红虚线穿过 3 个调控盒，35/35 自评 Y）
- **2026-05-19 全网调研 + 升级**：
  - 评估了 4 类技术路线：PGF graphdrawing (Lua) / libavoid (Inkscape 系) / GraphViz dot+spline-o-matic / PDF post-render bbox 检测
  - 前 3 项是 **graph-shape figure 才适用**，对我们的复合图（嵌入可视化 + sidebar + 中心 hub）无效
  - 选了 **post-render 几何检测路线**——升级 `pdf-overlap-checker.py` 加 **2 个新检测**：
    1. **line-through-node**：line segment 真穿过 filled rect 内部（不只是 bbox 相交）
       - 加 PyMuPDF 提取**真实 line endpoint**（pdfplumber 只给 bbox，丢失对角线方向）
       - 把"有 fill 的 path bbox"当作 node rect（TikZ 大量节点是 4-line + fill 而非 `re` 操作符）
       - **Liang-Barsky parametric clip** 判断 segment 是否真穿过 rect 内部
       - 4 类 false-positive 过滤：尺寸（6-140pt × 6-90pt 排除 zone）/ 自身 path / cluster suppression (≥4 segments 同 rect 视为收敛节点) / spine filter (line 在 rect 中线 ±3pt 视为 lifeline)
    2. **node-overlap**：两个 sibling node rect 几何重叠
       - 严格尺寸（10-140pt × 10-90pt 排除 glyph）
       - 跳过完全包含关系（parent-child OK）
       - **drop-shadow filter**（宽高近似 + 中心偏移 ≤5pt → TikZ drop shadow style 双绘）
       - 跳过同一 drawing path（同节点 outline + fill 复算）
  - **`--json` flag** 让 sub-agent 结构化消费 `{errors: [...], warnings: [...], summary: ...}`
- **实测命中**：
  - **line-through-node**：fig80 cell cycle 4 处全中（apoptosis 红虚线，坐标对得上）；Batch 7 fig62/63 spine filter 后 17→6；fig71/74/77/78 共 0 误报
  - **node-overlap**：drop-shadow filter 上线后 ex01-10 几乎全 0；剩下的 fig63/fig79/fig69/ex08 都是 1-4 处真问题（panel overflow / 紧密邻接节点）
- **已知边界**：
  - 矩阵密集图（heatmap cells 当作 rect）over-fire（ex10 GAT 报 121 处）—— 没办法纯几何分辨"语义 cell" vs "节点 rect"
  - 收敛节点（fan-in 多线汇聚）会被 cluster filter 误杀真问题，调高阈值又会暴出大量假阳
  - node-overlap 现在的 drop-shadow filter 假设 shadow 偏移 ≤5pt；如果 TikZ template 改了 shadow offset > 5pt 会出现假阳——记得同步更新 filter
  - **裁决依赖 sub-agent triage**：把检测结果当 **candidate report** 不是绝对 bug
- **使用方式**：
  - 编译后必跑 `python3 references/pdf-overlap-checker.py file.pdf --json > overlap.json`
  - sub-agent 在视觉自评 ④.5 时读 overlap.json：
    - `line-through-node` / `node-overlap` 类**逐条 triage**（不是绝对 bug——矩阵 cell、生物收敛节点常误报）
    - 其它 4 类（text-overlap / text-overflow / off-center / text-line）大概率是真 bug，直接修
  - 矩阵图、神经网络收敛图等**已知误报易发**的图，可在 prompt 中提醒 sub-agent "ignore line-through-node hits inside heatmap regions"
- **发现日期**：2026-05-19

---

#### [Batch 13 用户复审 #2] 步骤 ① 跳过 → 排版大块空白（fig126 Tacotron2）
- **问题/发现 (R3-100 Batch 13, fig126 Tacotron2 用户截图)**：图整体出现大块空白 — Encoder 列内容到 y≈-7 结束，WaveNet 在 y=-11.8 跨左→右整宽，Audio Waveform 在 y=-13.4。**Encoder 列下方 + WaveNet 中段 ≈ 5cm × 6cm 大块空白**。设计师一眼看到的问题，sub-agent 46 项 + Step 0 都没抓到
- **根因（步骤 ① 跳过 + 不可验证）**：
  ```
  grep 'ASCII|草图|10 项|Pre-flight|画图指令' fig126/figure.tex = 0 hits
  ```
  sub-agent 加载了 `step1-instructions.md` 但**没有按它要求实际输出 10 项 + ASCII 草图**——直接跳到编码。`step1-instructions.md` 写"必须以文字形式输出"，但 skill **没法验证** sub-agent 是否真的输出了。即使 ④.5 S6 "大块白色空带" 规则在，sub-agent 自评说 "Y, 0 处" 也漏过了
- **2026-05-21 修复（双锁 + 复杂图支持 narrative）**：
  - **锁 1：步骤 ① 产物物质化（双形式）**——SKILL.md ① 明文要求 10 项 + 草图**写进 figure.tex 头部注释块**：
    - 形式 A：ASCII 草图（极简/中等图）
    - 形式 B：**Narrative 设计文字**（复杂图 / 含 hero 子结构 / 嵌入 viz）—— 每列/每 zone 一段叙述，含 x/y 范围 + 内部子结构 + **预想"哪里可能空白"并写应对**
  - 复杂图（fig126 Tacotron2 类）**不能用 ASCII**——嵌入热力图/嵌入 mini-viz ASCII 画不出来；设计师真实思考是叙述性空间描述，不是 ASCII 字符画
  - **锁 2：Step 0 E 段验证**——sub-agent 在 ④.5 Step 0 时**必读 figure.tex 头部**确认有 form A 或 form B 注释块；若两种都没有 → critical blocker 回 ① 重做
- **设计哲学**：
  - 从"声明式纪律"（sub-agent 自报"我做了 step ①"）升级到"产物式纪律"（看 figure.tex 头部有设计文档注释 = 证据）。**可验证的纪律 > 不可验证的声明**
  - **不强制 ASCII** — ASCII 在复杂图上反而是限制（嵌入 viz / hero 子结构画不出来 → 用户反馈：会"影响画图复杂度和创新性"）。Narrative 形式允许复杂图保留设计自由度，同时保留"先想后画"的纪律
- **发现日期**：2026-05-21

#### [Batch 13 用户反思] 13 batches 加 70+ 规则但 bug 仍在 — meta 层缺失
- **问题/发现 (R3-100 Batch 13 用户反馈)**：13 batches 累积 46 项 checklist + 13 ⭐ + 7 类几何检测 + 6 canonical styles，每次用户复审仍能找出新模式 bug。**这不是"差几条规则"的问题，是反应式改进的天花板**
- **5 层根因**（深度诊断）：
  1. 规则是症状不是原理：sub-agent 不知道 "spine+stub 同色"、"tip 必落 anchor"、"label 间距 ≥0.3cm" 的共同底层是「**视觉连续性**」
  2. sub-agent 算法式写 TikZ：`spec → 选坐标 → 写 \draw → 编译`，缺"读者眼睛轨迹"视角
  3. self-eval 乐观偏差：即使写证据仍倾向 Y
  4. TikZ 自由度爆炸：每箭头 ~20 个独立选择，组合规则不可能覆盖
  5. text-only model 无 continuous visual feedback：盲写 → 编译 → 改，第一次盲写时埋的 bug 难修
- **承认现实**：原本 skill 散落 5 处类似"人类化"规则（tikz-global-rules.md 91/115/242/252/262, sequence-diagram.md 29），但**被埋在 specific rules 中没提升为 meta lens**
- **2026-05-21 修复（meta 层升级）**：
  - **SKILL.md 顶部加"视觉法则"段**（3 大法则：0.1 秒直觉 / 读者眼睛轨迹 / 删除测试），提升为所有规则之上的 lens
  - **④.5 加 Step 0：视觉直觉先行**——在 46 项 Y/N 之前必走 4 段证据（3 秒第一印象 / 主线轨迹 / 删除测试 / 审美退步测试）
  - **visual-review-checklist.md 强制流程同步**
- **为什么这有用**：把"读者视角"从可选规则提升为强制 step；从机械逐项检查变成**先视觉后机械**。设计逻辑：46 项是细节体检，Step 0 是整体心电图，缺一不可
- **发现日期**：2026-05-21

#### [Batch 12 用户复审 #3] T7 label 间距太小（fig116 WaveGlow）
- **问题/发现 (R3-100 Batch 12, fig116 用户截图)**：z_a / z_b bypass labels 与 bypass lines 间距仅 0.02-0.04cm — 视觉上 label "骑在线上"
  ```latex
  % bypass line at y = -2.0
  \coordinate (zb1_l) at (10.5, -2.0);
  \draw[arrow, ...] (split1.south) -- (zb1_l) -- ... ;
  % z_b label
  \node[font=\scriptsize, anchor=south] at (14.0, -1.98) {z_b (unchanged)};
  %                                              ↑↑↑↑
  %                                        只比 line 高 0.02cm
  ```
- **根因**：之前 T7 只规定 label 必须 `above`/`below`（方向对），**没规定最小间距 ≥ 0.3cm**。sub-agent 写 `anchor=south at (14.0, -1.98)` 自认为 above，技术上对，但 0.02cm 间距 = 视觉上压在线上
- **2026-05-20 修复**：T7 加最小间距铁律 — label 到 line ≥ 0.3cm（或等效 `yshift=8pt`）。**自评必须报具体数值，禁止印象判断**
- **正确写法**：
  ```latex
  \node[font=\scriptsize, anchor=south, yshift=8pt] at (14.0, -2.0) {z_b (unchanged)};
  % 或显式
  \node[font=\scriptsize, anchor=south] at (14.0, -1.7) {z_b (unchanged)};   % line at -2.0, label south at -1.7 → 0.3cm gap
  ```
- **发现日期**：2026-05-20

#### [Batch 12 用户复审 #2] tip 撞裸坐标 = "撞墙"视觉（fig118）
- **问题/发现 (R3-100 Batch 12, fig118 YOLOv8 用户截图)**：3 条 head feed arrows `\draw[arrow] (bu_p3.east) -- (14.5, 0.0);` —— tip 落在裸坐标 `(14.5, 0.0)`（spine 线上的点），不是任何 node。视觉上"箭头指向空气" / "撞 dashed zone border"。fig118 这是 "3 平行 pass-through with shared vertical spine" 模式，不是 fan-in/fan-out — sub-agent 画 spine 当"shared rail" 但 incoming 误用 `\draw[arrow]`
- **vs fig120 fan-in 不同点**：fig120 是真 N→1 汇合；fig118 是 3→3 平行流共享 visual rail。两者 sub-agent 都犯"incoming 带 tip"错，但触发模式不同
- **根因（E2 措辞漏洞）**：之前 E2 写"junction 不被 tip 戳"，sub-agent 不把 `(14.5, 0.0)` 当 "junction"（因为只有 1 incoming + 1 outgoing per row，不像"汇合"）
- **2026-05-20 修复（E2 重写）**：明文铁律 "**`\draw[arrow*]` 的 tip 终点必须是 node.anchor，禁止是裸坐标 / `\coordinate`**" — 不管是不是 junction，只要 tip 撞坐标就 ERROR。三类违规：(a) fan-out junction dot 被戳 / (b) fan-in 汇合点 / (c) spine 中间点
- **fig118 正确写法**（写进本 lesson 备查）：
  ```latex
  % 方案 A（推荐，无 spine）：3 条直接横向箭头
  \draw[arrow] (bu_p3.east) -- (det_head.west);
  \draw[arrow] (bu_p4.east) -- (seg_head.west);
  \draw[arrow] (bu_p5.east) -- (pose_head.west);

  % 方案 B（要保留 shared spine 的视觉象征）：
  \draw[line width=1pt, color=black!70] (14.5, 0.0) -- (14.5, -9.0);          % spine 仍画
  \draw[line width=1pt, color=black!70] (bu_p3.east) -- (14.5, 0.0);          % incoming NO tip
  \draw[line width=1pt, color=black!70] (bu_p4.east) -- (14.5, -4.5);
  \draw[line width=1pt, color=black!70] (bu_p5.east) -- (14.5, -9.0);
  \draw[fan_stub] (14.5, 0.0) -- (det_head.west);                             % outgoing 带 tip
  \draw[fan_stub] (14.5, -4.5) -- (seg_head.west);
  \draw[fan_stub] (14.5, -9.0) -- (pose_head.west);
  ```
- **发现日期**：2026-05-20

#### [Batch 12 用户复审] Fan-in canonical 缺失 + 颜色不一致 + 孤立 legend 点
- **问题/发现 (R3-100 Batch 12, fig120 consensus protocol 用户截图)**：
  1. **Y-junction "><绿尖"** (voteA + voteB → quorum)：两条 incoming 用 `\draw[arrow]` 都带 tip 在汇合点（"><"），且 incoming 蓝色 / outgoing 青色 — 颜色不一致 + 双 tip 对撞
  2. **fan-out spine 黑 + stub 彩** (leader → follower1 / follower2)：spine `color=black!70` 1.4pt vs stub `color=acaPurpleLine/acaGreenLine` 1.2pt → 折角处看上去断 + 颜色突变
  3. **4 个孤立彩色圆点漂浮**（蓝/橙/灰/红）无 label 无 leader — sub-agent 大概想画 legend 标记但忘了 label
- **根因（skill 5 处漏洞）**：
  - **E3 只有 fan-out canonical，没有 fan-in canonical** — sub-agent 不知道 N→1 怎么画，模仿 fan-out 反过来 → 错
  - **E2 没明文 "incoming 全部 no tip + 同色"** — sub-agent 给 incoming 加 tip
  - **没规则规定 spine + stub 颜色一致** — sub-agent 选 spine 黑 / stub 彩
  - **E7 没强制 legend dot 必有 label** — 孤立彩点放任
  - rounded corners 在 fan-in 折角处也漏（fig120 incoming 用 `++(0,-0.4) -- (combine)` sharp 90°）
- **2026-05-20 修复（5 处规则）**：
  - **E2 强化**：incoming 全部 no tip + 与 outgoing 同色（铁律）
  - **E3 重写**：(a) fan-out canonical + (b) **新增 fan-in canonical** + (c) 颜色铁律全同色 + (d) fan_stub style + (e) spine 中点禁放 white fill + (f) rounded corners 必加
  - **E7 强化**：legend dot 必紧贴 label < 0.3cm；禁止孤立彩色圆点
  - **lessons sample code**：fan-out / fan-in 两段 canonical TikZ 代码示例（本 lesson 上方 E3 中）
- **fan-in canonical 代码（写进 checklist E3 + 此 lesson 备查）**：
  ```latex
  % N sources → 1 target，所有 SAME COLOR
  \draw[line width=1pt, color=C, rounded corners=5pt] (src1.south) -- (src1.south |- Y);
  \draw[line width=1pt, color=C, rounded corners=5pt] (src2.south) -- (src2.south |- Y);
  \draw[line width=1pt, color=C] (src1.south |- Y) -- (src2.south |- Y);  % spine
  \draw[arrow, color=C] (midpoint, Y) -- (target.north);                   % 唯一带 tip
  ```
- **发现日期**：2026-05-20

#### [Batch 11 用户复审] residual / 标签位置 / 时序 annotation 三连击
- **问题/发现 (R3-100 Batch 11, fig101/107/108/110 用户截图)**：
  1. fig110 末端短箭头（~0.5cm）用 `\draw[arrow, shorten >=6pt]` 而非 `arrow short`，stem 被吃光剩 tip
  2. fig110 5'/3' label 用 `anchor=left/right` 在 y=0.5 → 与同 y 箭头压字
  3. fig108 ViT residual rail 离 addnorm1.east 仅 0.4cm → U-bend 形状回路怪
  4. fig107 MuSig2 B-N compute box 距 P1.x 仅 0.35cm，与 activation bar ±0.225cm 半宽几乎重合
  5. fig101 ConvNeXt residual 用了 `residual` style 自带 `rounded corners` → U-bend 视觉怪
- **根因**：
  - E13 短箭头规则 sub-agent 漏看 — 短距离箭头偶发回退 `arrow` 默认
  - skill 没规则规定水平箭头 label 必用 `above/below`
  - E14 只约束 `|-` pierce，没规则约束 residual rail 与 box 的最小间距
  - skill 没规则规定时序图 annotation box 与 lifeline 间距
- **2026-05-20 修复（4 处规则）**：
  - **T7 标签放置规范**：水平箭头 label 必用 `above`/`below` 不用 `left`/`right`
  - **S10 时序图 annotation 间距**：compute box 距 lifeline ≥ 0.5cm
  - **E14 扩充 residual rail 间距**：rail 距最近 box 边界 ≥ 0.5cm
  - **residual aesthetic 指南**（本 lesson 沉淀）：垂直 tap < 1.0cm（避免线下潜过深）；多 residual 共用 rail y（保持平行带）；residual `rounded corners` 默认值不变（5pt 软化），但 tap 长度小时**自动失效不显弧**——不必特意 `sharp corners`
- **发现日期**：2026-05-20

#### [Batch 10 用户复审 #2] `|-` / `-|` L-bend 穿 hero body + checker MAX_AREA 漏报
- **问题/发现 (R3-100 Batch 10, fig97 Pedersen Commitment 用户截图)**：`\draw[arrow] (msg.south) |- (ped_hero.west)` 中 msg 的 x 落在 hero box 的 x 范围内，TikZ 把横线**画在 hero 内部**——产生"箭头从 hero 内部出来"的视觉怪象。这种 bug 在 Batch 8/9/10 多次出现但未被 checker 抓到
- **根因双层**：
  1. **设计层**：PGF 不做 obstacle-aware routing（[官方手册](https://tikz.dev/base-nodes)），`|-` 只机械地"先垂直再水平"，**不考虑路径上有没有 obstacle**
  2. **checker 层**：`pdf-overlap-checker.py` 有 3 个 bug：
     - `MAX_AREA = 7500` 排除了 4.4cm × 2.2cm (=7750pt²) 的 Pedersen hero，hero-sized 节点被跳过
     - "endpoint inside rect → skip" 误判：`|-` 横线两端**都在 rect 内部**时也被 skip
     - "endpoint on boundary → skip" 把 stroke path 的 rect 边（top/bottom/left/right line）也算作"穿过"，cluster filter (≥4) 把真 bug 一起 drop
- **2026-05-19 修复（4 处）**：
  1. **`pdf-overlap-checker.py`**：(a) `MAX_AREA = 12500` 允许全 140×90 节点；(b) "both endpoints inside" 不再 skip 而是 flag；(c) "both endpoints on boundary" 仅当 seg 不沿 rect 4 条边时 flag
  2. **`SKILL.md` ③ 加 `|-` L-bend 安全条款**：✅/❌ 代码示例 + 用 named coordinate waypoint 绕开 obstacle
  3. **`visual-review-checklist.md` 加 E14**：自评每条 `|-`/`-|` source/target 投影是否重叠 + waypoint 数量
  4. **本 lesson 沉淀**
- **fig97 验证**：fix 后 checker 正确报 2 处 line-through-node — (62,165)→(39,165) 和 (130,165)→(152,165)，对应 msg/rand 进入 Pedersen 内部的两条横线
- **发现日期**：2026-05-19

#### [Batch 18 架构重思考] TikZ Snippet Library — 用乐高积木解决文本范式天花板

- **问题/发现 (R3-100 Batch 17, fig153 v2 TikZ)**：Philosophy First 重构后 sub-agent 把"嵌入 viz / panel / 公式 / 多色"4 个要素都做对了，但用户复审仍说"排版乱 / 大量空白 / 配色有问题"。
- **核心洞察**：Figure design 本质是 **multi-modal 任务**（visual perception + 结构组合 + 工程实现），当前 skill 是**纯 textual prompt engineering**：
  - ✅ 文本能做到 "嵌入 ≥ 1 个 viz" / "≥ 5 种 zone 颜色" / "无大空白"
  - ❌ 文本做不到 "嵌入 viz 看起来要有视觉重量" / "颜色要协调" / "留白要均匀"
  - **Batch 13-17 实质上在用文本逼近一个本质上需要 visual reference 的任务 = dead-end**
- **6 个候选方向**（A/B/C/D/E/F），选定 **A: TikZ Snippet Library**——给 sub-agent 高质量乐高积木拼装而不是从零写
- **解决方案（2026-05-22 Batch 18）**：创建 `references/tikz-snippets/` 含 6 个手工精雕的 TikZ 片段：
  - `attention-heatmap.tex`（N×N 热力图 + colorbar，硬编码 diagonal-dominant pattern + 紫色渐变）
  - `bar-chart.tex`（benchmark 柱状图 + grid + 数字标注）
  - `hyperparams-table.tex`（参数表 + 交替行 fill + bold value）
  - `multi-zone-palette.tex`（6 色 zone tone 标准模板 + 用色规则）
  - `pipeline-stages.tex`（N-stage 水平管线 + 自动 arrow 连接）
  - `formula-box.tex`（公式 box 3 variant：simple / with annotation / multi-line）
  - 每个 30-80 行 TikZ，独立可编译验证（6/6 PASS）
- **SKILL.md 改动**：Philosophy 段加"复杂档画图捷径"子段 + 加载索引加 `tikz-snippets/` 路径 + 明令禁简化 snippet 核心结构
- **预期效果**：sub-agent 在复杂档时**拼装 ≥ 3 个 snippet**（如 pipeline + heatmap + bar chart）—— 视觉重量自动达到 examples 标杆。N×M 组合让多样性保持。
- **元教训**：当文本范式触天花板，**不要再加规则，而是给 high-quality artifacts (snippets)**。这是 React 组件库思想应用到 TikZ。
- **发现日期**：2026-05-22

#### [Batch 17 元教训 — TikZ 硬约束 + dark theme 禁忌] sub-agent 用 Python 替代 TikZ

- **问题/发现 (R3-100 Batch 17, fig153 LLaMA-2)**：sub-agent 在执行 Module-First 子流程时**完全用 Python + matplotlib 生成 `.py` 文件**，没有 `figure.tex`。同时用了 **dark theme background**。
- **sub-agent 的动机推断**：
  - matplotlib 对复杂嵌入 viz (RoPE 旋转圆图 / GQA 头组示意 / benchmark bar chart) 比 TikZ 原生 API 方便
  - dark theme `plt.style.use('dark_background')` 一句话搞定，TikZ 反转全色工程量大
  - Module-First 多次编译时 Python (1-3s) 比 xelatex (5-30s) 快
- **核心问题**：Python 是**画起来更方便，不是画得更好**——
  - ❌ 不能 `\input{figure.tex}` 嵌入 LaTeX 论文（必须 `\includegraphics{.png}`，破坏 thesis-figure-skill 价值主张）
  - ❌ dark theme 与学术论文 light bg 风格断裂
  - ❌ 公式渲染：matplotlib mathtext 不如 LaTeX 原生
  - ❌ 风格不一致：fig153 (Python dark) 和 fig151/152/154 (TikZ light) 不能共存于同一 paper
- **解决方案（2026-05-22）**：
  1. **SKILL.md 硬约束**新加 🔴 工具铁律：**Module-First 子流程必须保持 TikZ**，禁 Python 替代；复杂嵌入 viz 用 TikZ 原生（`\foreach` / `pgfplots` / 手画 `\draw`）
  2. **SKILL.md 硬约束**新加 🔴 配色铁律：默认 light bg，dark theme 需用户明确请求
  3. **重画 fig153 v2 用 TikZ** 作为 case study，验证 TikZ 能否达到同质量
- **发现日期**：2026-05-22

#### [Batch 16 元教训 — 按需复杂度 + Module-First] Philosophy First 重构后剩余两个短板

- **问题/发现 (R3-100 Batch 16 用户反馈)**：Philosophy First 重构后，4 张复杂图（BERT/ResNet50/PPO/GAT）都达到了 examples 06-10 风格的方向（嵌入 viz + 信息 panel + 公式 + 多色），但用户反馈两个问题：
  1. **"都是画的很复杂的 但是也有些乱"**——sub-agent 默认套复杂档 examples 06 风格，用户实际可能只想要中等档清晰图 → 过度发挥 = 乱
  2. **"是不是应该先画一部分 一部分 然后每部分都画好了 再拼接"**——一次性写 800 行 TikZ 模块太多 → 整图局部混乱
- **核心洞察**：Philosophy First 解决了"审美方向"，但没解决：
  - **复杂度按需而定**（不是默认复杂 examples 06）
  - **Module-First 分块设计**（不是一次性整图）
- **解决方案（2026-05-22 加 2 条流程规则）**：
  1. **SKILL.md ①.5 改为"用户驱动 + 自动检测兜底"**：
     - 第 1 步：从用户原 prompt 关键词推断复杂度（"详细/含 benchmark" → 复杂；"概览/主架构" → 中等；"示意/几何" → 极简）
     - 第 2 步：如果不明确**主动询问用户**（A 极简 / B 中等 / C 复杂）
     - 第 3 步：用户确认后再画——禁止自作主张套复杂档
  2. **SKILL.md ③ 加 Module-First 子流程**（仅复杂档强制）：
     - ③.A 先画 hero（嵌入 viz + 公式）→ 单独编译验证
     - ③.B 再加主流（zones + connecting arrows）→ 拼接验证
     - ③.C 再加 panels（hyperparams / benchmark / legend）→ 拼接验证
     - ③.D 整体审查（→ 进入 ④.5）
- **关键原则**：**Prescriptive 流程规则 ≠ Defensive checklist 规则**。这 2 条是"应该 X"（流程），不是"不要 X"（防御）——加 2 条不算回到 47 项老路。
- **Batch 17 验证预期**：sub-agent 应该
  - 看到不明确 prompt 时**主动询问复杂度**
  - 复杂档时**分块画 + 单独验证**，整图更干净
- **发现日期**：2026-05-22

#### [Batch 15 元教训 — Philosophy First 重构] 47 项防御规则反而抑制了创造力

- **问题/发现 (R3-100 Batch 14/15 用户反馈)**：fig137 经历 v1 (大空白) → v2 (5 bug) → v3 (修 5 bug 但 fan-out 仍丑) 三代迭代，每轮都加新规则补漏洞，但**整体审美和 examples 06-10 的距离越来越远**。用户反馈："新的毛病还是会有"，"现在很少能画出 examples 06-10 那种风格"。
- **根因（最深层）**：13-15 批演化方向**完全错了**：
  - 47 项 checklist 是 **defensive 规则**（"不要 X"）—— 没有任何 **prescriptive 设计指导**（"应该 X"）
  - canonical 模板 + g1-g4 几何 + E15 anchor 等细则把 sub-agent 推向**统计中心的安全默认**（box+arrow only / 3 色单调 / 无嵌入 viz）
  - 全部规则可通过 = box+arrow figure，**审美天花板被规则地板压低**
- **全网调研发现**（2026-05-21）：
  - **Anthropic frontend-design** (277k installs)：42 行打败 800 行；Philosophy first；Naming gravitational pull；Permission for creativity；UNFORGETTABLE question
  - **PUA skill** (GitHub tanweai/pua)：corporate framing + L1-L4 pressure escalation + ownership mindset
- **解决方案（2026-05-21 Philosophy First 重构）**：
  1. **SKILL.md 顶部**新增 Philosophy 段（替代之前的"视觉法则"）：
     - The UNFORGETTABLE Question（审稿人 5 秒记住什么）
     - Naming Gravitational Pull（7 个统计中心默认明确列禁）
     - Permission for Creativity（NeurIPS/ICML investor framing + "Don't hold back"）
     - 创造空间词汇菜单（嵌入 viz / panel / 公式 / 配色 / 层级 / cross-zone / 学术 polish）
  2. **visual-review-checklist 精简 47 → 18 项**：保留编译保障 (T1/T3/T4) + 空间灾难 (S1/S6/S8/S9) + 语义 (M1/M2/M3/M8) + 连线 (E1/E2/E3/E9/E12) + 美学 (A1) + **新增 V1** (复杂档应有 ≥1 嵌入 viz/panel)
  3. **删除最近 5 个 commit 的防御细则**：E3 g1-g4 几何 / E15 同 anchor / T7 0.5cm 强化 / Step 0 E (1a)/(1b) / hero sub-layer 间距预算公式
  4. **Philosophy + 18 项双重门**：18 项过仅说明无明显 bug，Philosophy 通过才说明审美达标
- **Batch 16+ 验证预期**：sub-agent 应能在 Philosophy 引导下**主动考虑嵌入 viz/panel/公式嵌入**，不再 box+arrow only
- **反思**：13-15 批教训的最大价值不是规则本身，而是认识到"defensive 规则越多 → 创造力越少"。**少而精的 Philosophy 比繁多防御更释放潜力**。
- **发现日期**：2026-05-21

#### [Batch 14 用户反馈] fig137 v2 修一个 bug 引入 5 个 — 白盒规则被黑盒绕过

- **问题/发现 (R3-100 Batch 14, fig137 v2 用户复审)**：
  v2 修复 v1 的 11×5cm 大空白后，用户在新 PNG 中标出 5 处新问题：
  1. K/V 入口的"fork dot"：sub-agent 用 **2 条独立 `\draw[arrow]`**（不是 fan-out canonical spine + stubs）从 enc_an2.east 到 ca_k / ca_v；`line width=1.2pt + rounded corners=5pt` 在 90° 折角处渲染成可见 bulge，视觉像 fork dot
  2. Q 旁紫色方块：`\node[fill=white, inner sep=1pt, font=\scriptsize\bfseries, color=acaPurpleLine] {Q}` 在白背景 PDF 上，fill=white 不可见，紫色粗体单字符把 1pt inner sep 填满 → 视觉是紫色方块（fig120 孤立 dot 教训的变体）
  3. 紫橙撞车：紫色 `(dec_ca.west) -- (ca_q.east)` 和橙色 `... -- (dec_ca.west)` 两条 incoming arrow tip **都终止在 dec_ca.west 同一 anchor** → 同一像素点不同颜色重叠
  4. "Multitask Output" 标题离 spine 仅 0.3cm = T7 边界值视觉太紧
  5. v2 sub-agent 自评 0 blocker 仍漏检全部 5 处
- **元根因（最深层）**：规则用"if X then must Y"形式，sub-agent **可以"不用 X"绕开 Y**——白盒规则被黑盒绕过：
  - E3 自评只问"有没有 fan-out canonical 实施"，sub-agent 用 2 条独立 \draw 替代 spine + stub → E3 自评条件未触发
  - "多 tip 同 anchor 撞车" SKILL 没明文规则 → 规则空白
  - T7 报"0.3cm ✓"过 → 边界值通过 = 实质失败
- **解决方案（2026-05-21 fig137 v2 后三处修复）**：
  1. **`visual-review-checklist.md` E3 加"反绕过铁律"**：grep figure.tex，同一 node.anchor 出现 ≥2 次作为 `\draw[arrow]` 起点 → 必须重写为 canonical（即使是独立写法）
  2. **`visual-review-checklist.md` 新增 E15** ⭐：同一 anchor 不能被多条 incoming arrow 同时 tip；修复用换 anchor / anchor offset / routing 改道
  3. **`visual-review-checklist.md` T7 强化**：(a) 视觉默认从 0.3cm 提升到 0.5cm（0.3 是 compile fail 阈值不是视觉安全值）；(b) `fill=white` + 单字符 + bfseries label 警告（inner sep ≥ 3pt OR 不用 bfseries OR 加长 label）
  4. 总项数 46 → 47；⭐ 13 → 14
- **fig137 v3 验证预期**：sub-agent 应该写"E15 dec_ca anchor 检查：3 条 incoming（dec_an1.south + Q + Attn out），用了 .west / .north / [yshift=+3pt]dec_ca.west 三个不同 anchor offset 分开" 才能通过
- **发现日期**：2026-05-21

#### [Batch 14 用户反馈] Step 0 E 段"细线填充"自欺漏检 — fig126 教训再现

- **问题/发现 (R3-100 Batch 14, fig137 Whisper 用户复审)**：
  Encoder zone 右沿 x≈7cm，Decoder zone 左沿 x≈18cm，中间 ~11cm × 5cm 是大空白
  ——只有一条 orange cross-attention rail + "K, V" 标签穿过。
  sub-agent 在 ④.5 Step 0 E 段写"无 > 3×2cm 大块空白，Encoder 和 Decoder 之间由
  cross-attention rail 填充"——**自欺漏检**。
- **根因**：Step 0 E 段原条款只说"扫描大块空白"，没说**怎么算"已填充"**。
  sub-agent 把"有一条线穿过" = "已填充" 的 rationalization 顺利过了 self-check。
  fig126 是赤裸裸空白，fig137 是**伪装填充**——更狡猾，self-check 形式化通过。
- **解决方案（2026-05-21 三处修复）**：
  1. **`SKILL.md` Step 0 E 段加 (1a) 客观度量铁律 + (1b) 填充判定**：
     - (1a) 必须**写出怀疑区 x/y 范围 + 宽×高**（如"x=7-18 = 11cm × 5cm"），
       禁止抽象判断"无空白"
     - (1b) "已填充"定义：区域内有 ≥1 个 **box/text/嵌入 viz/标注块**；
       **细线（rail/leader/dashed/arrow）不算填充**，线占面积可忽略
     - 修复方向改为：**回 ① 重新规划布局**（拉近 hero / 中间加内容 / 改垂直）——
       **不是改 .tex**
  2. **`visual-review-checklist.md` Step 0 E 段同步 (1a)/(1b)**：阻止 sub-agent
     读 checklist 时漏新条款
  3. **本 lesson 沉淀**：未来 audit 关注"E 段判定标准是否客观可机械验证"
- **预期 Batch 15 验证点**：fig137 类布局（两个 hero 远距离 + 单条 rail）应该被
  Step 0 E blocker 并要求重新规划——不允许"rail 填充"过关
- **发现日期**：2026-05-21

#### [Batch 10 用户反馈] 短箭头 + rounded corners + 最小间距三连击
- **问题/发现 (R3-100 Batch 10, fig91-95 用户复审)**：canonical `arrow.style` 让短箭头出现"只有头的箭头"（tip 6.5pt + shorten 3pt 吃光 stem）；`rounded corners=5pt` 被 sub-agent 滥用在直线上产生"莫名其妙曲线"；重叠问题仍频繁（layout 时邻接间距没硬约束）
- **全网调研定位**：
  - [PGF/TikZ Arrows 官方手册](https://tikz.dev/tikz-arrows)：Stealth tip natural size 按 line width 0.4pt 时匹配 11pt x-height — 我们 1.0pt 线已是 natural 2.5x
  - [PGF Path Specifications](https://tikz.dev/tikz-paths)：「very short line segments → rounding may cause inadvertent effects」「lines suddenly extend over the other end」直接命中
  - [Node Overlap Removal (arxiv 2016)](https://arxiv.org/pdf/1608.02653)：业界 best practice 是 layout 时预防而非 detect-then-fix
- **解决方案（2026-05-19 三处修复）**：
  1. **`tikz-template.tex` 新加 `arrow short/.style`**：tip 3pt（`length=3pt 1.0`）+ line width 0.8pt + `shorten >=1pt, shorten <=0pt`。专用于 < 1.5cm 的短连接箭头
  2. **`SKILL.md` ③ canonical 表新增 `arrow short` 行 + "短箭头铁律"段 + "`rounded corners` 使用规则"代码示例**（✅ 多段折线 OK / ❌ 直线禁用）
  3. **`visual-review-checklist.md` 加 E13**（短箭头形状 + rounded corners 规范）和 **S9**（最小邻接间距强制扫描：同行 ≥ 0.8cm / 跨行 ≥ 0.6cm / text-box ≥ 0.3cm / 线-box ≥ 0.4cm）。计数 41 → 43
- **发现日期**：2026-05-19

---

## 写入指引

新发现满足以下任一条件时追加到本文件：
- 编译错误经过 2 次以上尝试才解决
- 发现某类图的有效布局技巧
- 渲染结果与预期差异大需要调整方案
- 用户反馈指出反复出现的问题
- 验证出比当前基线更优的参数（更新 Part 1 表格，**只升不降**）

不要写入：
- 已被 `tikz-global-rules.md` / Python checker **完全覆盖且无新 narrative** 的内容（checklist 项的 narrative 上下文允许在 lessons.md 留存——但不要复述 checklist 的具体 Y/N 语言）
- 一次性的 latex 语法错误（应改文档而非积累故事）
- 未确认的猜测
- **测试协议 / 落盘格式 / 状态追踪 / 主题选择策略**——这些是 test harness 而非 TikZ 知识，不写入

**lessons.md 范围**：TikZ/draw.io 渲染技巧、图层选择、布局规则、参数基线、踩坑教训。专注图本身的视觉/几何质量。

