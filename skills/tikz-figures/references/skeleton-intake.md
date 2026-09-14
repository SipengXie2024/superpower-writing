# Skeleton 入库通道（Φ，D 模式）

用户已有一份编译通过的 `.tex`，想把它的布局固化成可复用的 skeleton 时走本通道。在 ⓪.5 选 D 路径后进入。本通道不画新图。

本文件内的相对路径都从 `references/` 算起（本文件所在目录）。

## Contents

- 前置条件
- Φ.1 接收 + 编译验证
- Φ.2 Vision-audit 把关（简化版 ④.5）
- Φ.3 分析 layout pattern + 决策入库方式（关键 gate）
- Φ.4 命名 + 字母分配
- Φ.5 自动生成 USAGE header
- Φ.6 写入库 + 更新索引
- Φ.7 提醒用户后续补 CONSTRAINTS
- Φ 与 ⑦ 经验沉淀的区别

## 前置条件

- 用户提供已编译通过的 `.tex` 文件路径
- 文件能 xelatex 编译成功
- 渲染后视觉无明显 bug

## 流程

```
Φ.1 接收 + 编译验证
   - 读取用户提供的 .tex 文件
   - 跑 xelatex -interaction=nonstopmode + pdftoppm -r 150 渲染 PNG
   - 编译失败 → 报告错误，停止入库

Φ.2 Vision-audit 把关（简化版 ④.5）
   - Read 渲染出的 PNG
   - 走 Step 0（3 大法则）+ 18 项中的关键 6 项（S1 整图对齐 / S5 元素间距 /
     T1 文字渲染 / M3 信息流方向 / E5 箭头清晰 / V1 整体审美）
   - 任何 blocker → 报告给用户，要求修复后再入库

Φ.3 分析 layout pattern + 决策入库方式（**关键 gate**）
   - 扫描 .tex 提取结构指纹：zone 数量 / zone 坐标范围 / hero 子结构 /
     嵌入 viz 类型 / 配色（line/fill 色对集合）/ 箭头模式
   - **若 .tex 头部注释明示 "Adapted from Skeleton X"** → 直接判定为 X 变体，
     跳过结构相似度计算
   - 否则与现有 6 skeleton 比对相似度，按 zone 数 + 关键结构（hero 位置/
     side panel/底部图表对）匹配，**三档判定**：
     * **>90% 匹配（结构等同，仅内容/主题不同）** → 默认 skip 入库，
       提示用户"这就是 skeleton X 的 <主题> 应用，直接用 X 即可"。
       若用户坚持入库 → Φ.3 verdict = "变体入库"，记录 parent letter
     * **50-90% 匹配（明显借鉴 X 但有结构修改）** → 询问用户
       (a) 合并到 X 作内部变体注释  (b) 作 hybrid 新 skeleton 入库
       后者 → Φ.3 verdict = "结构创新"
     * **<50% 匹配（结构创新）** → Φ.3 verdict = "结构创新"
   - **输出**：verdict + parent letter（若变体）/ 主题 keyword

Φ.4 命名 + 字母分配（**按 Φ.3 verdict 分支**）
   - **若 verdict = "变体入库"**：
     - 文件名 = `example-skeleton-{parent}-variant-{domain}.tex`
       例：D 的 MoE 变体 → `example-skeleton-D-variant-moe.tex`
     - **不占用新字母槽**，留给真正的结构创新
   - **若 verdict = "结构创新"**：
     - `ls tikz-snippets/example-skeleton-*.tex` 取下一个可用字母
       （当前 B-G 已用，下一个 = H）
     - 询问用户 kebab-case 主题（如 "sankey-flow" / "matrix-grid" / "timeline"）
     - 文件名 = `example-skeleton-{letter}-{topic}.tex`

Φ.5 自动生成 USAGE header（**含具体生成算法**）
   - 顶部模板字段及生成方法：
     * **标题行**：
       - 创新：`Skeleton {letter}` 后跟一个 em-dash 分隔符，再跟 layout 的一句话描述
       - 变体：`Skeleton {parent}-variant` 后跟 em-dash，再跟 {domain}，
         末尾括号注明 ({parent}-layout domain variant)
       - 分隔符必须与库里现有 6 个 skeleton 的头部一致（见
         `tikz-snippets/example-skeleton-D-vertical-sidepanel.tex` 第 2 行），
         本文件受禁破折号的 lint 约束所以只能描述、不能写出字面量
     * **USAGE**：固定模板 "Sub-agent: copy ENTIRE file as figure.tex,
       change ONLY content (text/labels/numbers). DO NOT touch layout."
     * **LAYOUT MODEL** ASCII 生成步骤：
       a) 扫所有 `\fill[...] rectangle (x0,y0) (x1,y1)` 和 `\draw[...] rectangle`
          提 zone bounding box
       b) 按 y 范围归 row（top/mid/bottom），x 范围归 col（left/center/right）
       c) 画 ASCII box：每个 zone 一个 □，按相对位置布局
       d) **若是变体，直接继承 parent 的 LAYOUT MODEL，加注 "(same as Skeleton X)"**
     * **WHEN TO USE**：从用户提供主题 + 域关键词推断
       （如 "MoE" → "Mixture-of-Experts papers, sparse gating/routing"）
       若变体：加一行 "For non-{domain} structurally similar cases, prefer skeleton X directly"
     * **CONTAINS**：自动列清单
       a) 数 `\node[*_node]` count by color (e.g., "4 blue_node + 3 purple_node")
       b) 扫嵌入 viz：heatmap (`\fill` matrix) / bar (`\fill` rect series) /
          curve (`\draw ... smooth`) / radar (`\draw` polar) / formula box (`$...$` in node)
       c) 列 bullet
     * **CONSTRAINTS 段**（标题行是 CONSTRAINTS 接 em-dash 再接 DO NOT VIOLATE，
       与现有 skeleton 的字面格式一致）：留空 + TODO 注释
       - 若变体：加 "see example-skeleton-{parent}.tex CONSTRAINTS for inherited rules"
       - 加 4-5 个领域专属的 TODO 起跑提示

Φ.6 写入库 + 更新索引（**含明确路径与格式**）
   - 写文件：`tikz-snippets/example-skeleton-{X}.tex`（X = 完整文件名前缀）
   - 渲染：`xelatex -interaction=nonstopmode` + `pdftoppm -r 100 -png`
     **PNG 输出到 `tikz-snippets/previews/example-skeleton-{X}.png`**
     （注意是 `previews/` 子目录，不是 `tikz-snippets/` 根，与现有 6 个一致）
   - 更新 `tikz-snippets/README.md` inline gallery：
     a) 定位 gallery 表（anchor 行：含 `example-skeleton-B-horizontal.tex` 的 markdown 表格）
     b) 插入位置：
        - 创新：最后一行 example-skeleton-G 之后
        - 变体：parent skeleton 行下面，行最后加 "({parent} 领域变体)" 标注
     c) 行格式：
        ```
        | `example-skeleton-X.tex` | **X: <一句话布局描述>** | <主要应用场景> | ![example-X](previews/example-skeleton-X.png) |
        ```

Φ.7 提醒用户后续补 CONSTRAINTS（关键防回归提示）
   - "⚠️ 新 skeleton 已入库，但 CONSTRAINTS 段当前是 TODO 占位。
      如果你在画这张图时踩过坑（标签长度上限 / 锚点选择 / 路径形状 /
      box 宽度依赖等），请手动补充到这一段。
      这是防止未来 sub-agent 复用时重新引入 bug 的关键，参考
      D/E/F/G 的 CONSTRAINTS section 写法。"
```

## Φ 与 ⑦ 经验沉淀 的区别

- ⑦ 沉淀**抽象 lessons 与基线参数**（分别写入 `lessons.md` 与 `baselines.md`）
- Φ 沉淀**完整可复用的 figure 模板**（写入 `tikz-snippets/example-skeleton-X-*.tex`）
- 两者独立工作，可在同一会话各做各的

**Φ 的杠杆价值**：每入一个 skeleton，未来 N 个 user/session 都能复用。**库是 self-growing 的**，这是本 skill 长期复利的核心机制。
