# 图审查通道（AUDIT 模式：审查用户已有的成品图）

本文件是 tikz-figures 的 AUDIT 模式完整流程，在用户选择 AUDIT 路径时加载。

**触发**：用户已有一张成品图，要的是"这张图能用吗 / 帮我审查"，不是让你新画一张。产出是一份审查报告（advisory），不是新 figure.tex。

**核心契约：graceful degradation（对齐本插件 inspection / attestation 纪律）**。本通道有两条路径，按用户是否给了图片分叉。铁律：能看见就 Read 图再判；看不见就显式标 "user must verify"，绝不凭文字描述猜视觉。这与 claim-verification 的"语义匹配是 advisory，soft-fail 交用户裁决"同源：AI 视觉对自己没看过的像素是盲的，伪造一个"font 12pt 合格"的判断比诚实说"我没看到图"更糟。

```
Ψ.1 判断是否有图（路径分叉点）
   - 用户给了图片路径（PNG/PDF/JPG），或图已在 .writing/figures/ → 有图路径（Ψ.2A）
   - 用户只描述了图、没给文件 → 无图路径（Ψ.2B）
   - 不确定时，先问用户"能给我图片文件吗"：有图的审查质量远高于无图

Ψ.2A 有图路径（vision 优先，在规则审查之前）
   - 先用 Read 工具读图片（vision），在跑任何规则之前。这是本路径的前提
   - 读完后，亲眼审下面四类 vision-only 信号（文字描述给不出，必须看图）：
     * font legibility（字号可读性）：最小标签在成图尺寸下能否读清；轴标题/刻度是否过小
     * palette（配色）：是否 colorblind-safe（Okabe-Ito 类）；是否冗余编码（形状加颜色，不只靠颜色）；灰度下是否仍可区分
     * raster-vs-vector tells（栅格/矢量判别）：放大有无锯齿/像素块/JPEG 振铃即栅格；论文图应是矢量（PDF/SVG/TikZ），栅格成图要提醒用户换矢量或提高 DPI
     * chartjunk：3D 效果 / 渐变 / 阴影 / 装饰网格 / jet 配色 / 截断 y 轴误导，逐个标出位置
   - 然后走规则审查（见 Ψ.3），每条 vision 检查写一句"我在图中看到…"的证据

Ψ.2B 无图路径（text-only，显式降级）
   - 没有图就不跑 vision 检查，也不猜。把三类 vision-only 检查显式标为 "user must verify"：
     * font size（字号）→ "user must verify：我没有图，无法判断最小字号在成图尺寸下是否 ≥ 8pt"
     * raster detection（栅格判别）→ "user must verify：无法判断是矢量还是栅格，请确认导出格式为 PDF/SVG"
     * colour palette（配色）→ "user must verify：无法判断配色是否 colorblind-safe / 灰度可读"
   - 仍可做的 text-only 检查：基于用户描述判断图的修辞角色（是不是三张叙事图之一 / Figure-1 范式选得对不对 / gains 边际却用了 teaser / 有没有 Entity1/X 占位）；这些不依赖看图
   - 报告顶部写明"本次为 text-only 审查，vision-only 项已标 user must verify"

Ψ.3 规则审查（复用既有的 18 项视觉审查清单）
   - 加载既有的 18 项视觉审查清单（visual review checklist），不另造清单
   - 有图路径：逐项回答 18 项 Y/N，每项一句证据（"我在图中看到…"）。vision 相关项（T1/T3/T4 文字、S1/S6 空间、A1/V1 美学）正常判
   - 无图路径：依赖看图的项（T1/T3/T4/S1/S6/S8/S9/A1/V1）一律标 "user must verify"，不强行 Y/N；不依赖看图的语义/修辞项照常评
   - 叠加 figure-rhetoric 的设计判断：30 秒理解测试（图传达的是不是它该支撑的 claim）、真实实体（无 Entity1/X）、Figure-1 范式适配

Ψ.4 输出审查报告（高/中/低 severity，defect-hunting 不是 confirmation）
   - 框架：默认"这张图有缺陷，去找"（不是"找理由说它过了"）
   - 每条 finding 标 severity：
     * high：误导读者或让图看起来坏掉，例如栅格化的论文图、截断 y 轴夸大增益、关键标签不可读/被截断、配色仅靠颜色（灰度全糊）、伪造/不诚实的数据呈现、范式选错（gains 边际用了 teaser）
     * medium：降低专业度/理解度，例如 chartjunk（3D/装饰网格）、字号偏小但勉强可读、Entity1/X 占位、配色非 colorblind-safe、图与 claim 弱相关
     * low：纯外观，例如轻微对齐 / 配色微调 / 可选的密度精简
   - 修 high 加能低成本修的 medium；low 列出但不强求
   - verdict 是 advisory：报告交用户，由用户决定改不改 / 是否重画。绝不自动改图、绝不替用户拍板"不能用"
   - 用户若要把成图重画成矢量 → 转 C 复刻（用成图作 ref.png，figure-diff.py 验还原度）

Ψ.5 NEVER-FABRICATE
   - 不编造"我看到字号 9pt"这类没看图就给的数字；没看到就标 user must verify
   - 不编造图里的数据/趋势是否真实：数据真实性是用户的责任，审查只看"呈现是否诚实"（如 y 轴有没有截断却不标注）
```

**Ψ 与 ④.5 的区别**：④.5 是画图过程中对自己刚生成的图的强制闭环（有 overlap.json、能重编译迭代）；Ψ 是对用户已有成图的一次性审查（可能只有一张 PNG、不能重编译、不一定有源码）。④.5 的 mode-C 多镜头 gate 是 defect-hunting 的最强形式；Ψ 对齐同一 framing（高/中/低 severity 加默认找茬），但因为没有源码和重编译循环，停在"报告加交用户"。
