# 箭头与连线 canonical pattern

步骤③ 写任何连线之前读本文。`tikz-global-rules.md` 管的是布局层面的走线（方向感、扇出、绕框、弯折质量），本文管的是 style 层面的语法铁律。两者互补，都要遵守。

本文件内的相对路径都从 `references/` 算起（本文件所在目录）。

## Contents

- 六个 canonical style 及选用铁律
- 禁止手写 Stealth scale
- 短箭头铁律（< 1.5cm）
- fan-out 树状分叉的 stub
- `rounded corners` 使用规则
- `|-` / `-|` L-bend 穿框安全条款
- 编译前的两个 checker

## 六个 canonical style

`tikz-template.tex` 中 6 个预定义 styles 是经过 PGF 官方文档 + PlotNeuralNet 业界实践 + arrows.meta + bending library 综合调研的最佳实践（深度调研 2026-05-18，5 batches 教训）：

| style | 用途 | 何时用（铁律） | 关键差异 |
|---|---|---|---|
| `arrow` / `arrow thick` / `arrow thin` | 长连线 | **⚠️ 仅 ≥ 1.5cm，短于此必须改用 `arrow short`** | tip 6.5pt, `shorten >=2pt, shorten <=1pt` |
| **`arrow short`** | 短箭头（相邻 box 间） | **⚠️ < 1.5cm 必用此 style** | tip 3pt, `shorten >=1pt, shorten <=0pt`，防止 tip 吃光 stem |
| `residual` | dashed skip / 反馈 | residual / feedback | 紫色虚线 + rounded corners |
| `leader` | annotation 引线 | 引线 / 标注 leader | 灰色 dotted |
| **`fan_stub`** / `fan_stub thin` / `fan_stub thick` | fan-out 树状分叉的 stub（spine → target） | **fan-out / fan-in 的 stub 段必用此** | **`shorten <=0pt`**，起点紧贴 spine 无 gap |

**禁止**自己手写 `-{Stealth[scale=X]}`，4 轮 Batch 教训证明手调 scale 治标不治本。只调 `line width`（0.6/1.0/1.6pt 三档），tip 通过 `length=⟨dim⟩ ⟨line_width_factor⟩` 语法自动跟随。`\usetikzlibrary{bending}` **必加载**，否则弯折路径上 tip 必然 mis-align。

## 短箭头铁律

Batch 10 用户反馈：fig91-95 大量"只有头的箭头"。**任何 < 1.5cm 的连接箭头必须用 `arrow short`**，不要默认 `arrow` 或 `arrow thick`。

原因：默认 `arrow` 的 tip = 5pt + 1.5×line_width = 6.5pt，加上 `shorten` 3pt，一条 15pt（0.5cm）的短箭头剩下 stem 只 5.5pt，视觉上"只剩个头"。`arrow short` 用 3pt tip + 1pt shorten，stem 保留充足。

## fan-out 树状分叉

1 source → N targets：spine 用普通 `\draw[line width=1.0pt]`（无 shorten），**stub 用 `fan_stub` 不用 `arrow`**，后者的 `shorten <=1pt` 会在 stub 起点和 spine 间留 1pt 视觉 gap（fig86 Batch 9 教训：MPD/MSD spine 全断裂）。

## `rounded corners` 使用规则

Batch 10 用户反馈：fig92 出现"莫名其妙曲线"。[PGF 官方手册原话](https://tikz.dev/tikz-paths)："very short line segments → rounding causes inadvertent effects"。

```
✅ 只在显式 ≥2 段折线用 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (corner) -- (B);
   \draw[arrow, rounded corners=5pt] (A) |- (B);             % | 和 - 是隐式 corner

❌ 直线禁加 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (B);   ❌ TikZ 在端点附近产生鬼影弧
```

## `|-` / `-|` L-bend 安全条款

Batch 10 用户反馈：fig97 Pedersen Commitment hero 出现"箭头穿过框体"，`(msg.south) |- (ped_hero.west)` 中 msg.x 落在 hero 的 x 范围内，TikZ 把横线**画在 hero 内部**。

```
✅ (A.south) |- (B.west) 仅当 A 不在 B 的水平投影内（A.x < B.x0 OR A.x > B.x1）：
   A
   |
   +----→ B          ← A 在 B 左上方，横线在 B 外部 OK

❌ (A.south) |- (B.west) 当 A.x ∈ [B.x0, B.x1]：
   A
   |
   |  ↓
   +→ B         ← 横线穿过 B 的内部 = pierce bug

✅ 修复 1：用 named coordinate 显式 waypoint 绕开 B：
   \coordinate (wp) at (B.x0 - 0.5cm, B.center.y);
   \draw[arrow] (A.south) |- (wp) -- (B.west);

✅ 修复 2：换 anchor 让箭头从 B 的上方接入：
   \draw[arrow] (A.south) -- (B.north);   % 直线，A 在 B 上方
```

PGF 不做 obstacle-aware routing（[官方手册确认](https://tikz.dev/base-nodes)），所以必须自己保证 `|-` / `-|` 的中段不撞 obstacle。`pdf-overlap-checker.py --json` 的 line-through-node 检测会抓到这种 bug。

## 编译前两个 checker（pre-flight，所有路径通用）

- `python3 tikz-validator.py <file.tex>`，几何/语法 gate：微斜线 / 溢出 / 碰撞 / 方向反转。**ERROR 必修**
- `python3 tikz-design-linter.py <file.tex> [--type rich|sequence|simple]`，**advisory** 设计指标。**默认 WARN 不阻挡**，简单论文图可以简单，linter 只汇报指标供 Claude+用户判断是否匹配论文复杂度。仅当 ≥8 节点且尺寸比 < 1.5（严重视觉层次缺失）才 ERROR。
