# 排版尺寸闸门与 1:1 预览

> **何时加载**：步骤④，把图集成进论文时必读。独立出图（不进 LaTeX 正文）可跳过。
> **配套脚本**：`references/preview-loop.py`

## 目录

- [为什么需要这道闸门](#为什么需要这道闸门)
- [用法](#用法)
- [图源写法](#图源写法论文集成推荐)
- [宽度超标时先查左边](#宽度超标时先查左边)
- [高分辨率分块复检](#高分辨率分块复检)

---

## 为什么需要这道闸门

图在自己的画布上好看，不等于在论文里能用。两个失败模式编译**不报错**：

- **图比栏宽宽**。用 `\includegraphics[width=\columnwidth]` 时 LaTeX 静默缩放，字跟着一起变小；用 `\input` 时直接溢出到 gutter。
- **成品尺寸下字太小**。一张 400pt 宽的画布塞进 240pt 的单栏，缩放 0.59，图内 7pt 的标签落到 4pt，审稿人读不清。这是最常见也最致命的一类，因为开发时看的放大图上完全看不出来。

## 用法

```bash
python3 references/preview-loop.py --venue usenix --style mystyle fig1_pipeline fig2_depgraph
python3 references/preview-loop.py --venue ieee --wide fig1_overview   # 跨栏图
python3 references/preview-loop.py --col-pt 240.1 --text-pt 504 fig3   # 手填几何
```

对每张图报告**实际排版宽度**与栏宽预算的差，超了标 `WIDE`；同时产出两个 PNG：`_screen.png` 是 150 dpi 的 1:1 渲染，等于图被阅读时的真实大小；`_print.png` 是 300 dpi，用来查细节。

**判可读性只看 `_screen.png`。** 放大图会骗人：4pt 的标签在 300 dpi 渲染里清清楚楚，在纸上和屏幕上都读不出来。

预设几何覆盖 `usenix` / `acm` / `ieee` / `neurips`，用前对照该会议当年的 style 文件核一遍，模板会改。

## 图源写法（论文集成推荐）

`figure.tex` 只含裸 `tikzpicture`，不带 preamble；共用的配色和节点样式抽到一个 `style.tex`；主文档在 preamble `\input` 样式，正文用 `\input{figures/figX}` 而不是 `\includegraphics`。

这样图继承正文字体、零缩放、文字在 PDF 里可选可搜。`preview-loop.py` 的 wrapper 复刻同一套 preamble，所以预览和成品逐像素一致。

**给每张图设尺寸预算再动手**。单栏图高度超过 250pt 就该问是不是同时在讲两件事（见 `figure-rhetoric.md` 的 "One figure, one job"）；跨栏图和单栏图的面积往往差不多，跨栏换来的是形状不是空间，代价是必须浮到页顶。

## 宽度超标时先查左边

`anchor=east` 的标签、旋转节点、`amplitude` 较大的 brace 都会把画布边界推向负数，报告的宽度包含这部分。查宽度只盯右边会找不到源头。习惯做法是让最左元素的左边缘落在 x=0。

预览用 standalone 的 `border=Npt` 会给页面尺寸多算 2N，脚本已在报告前减掉；自己写 wrapper 时别忘了这一步，否则每张图都虚报 4pt。

## 高分辨率分块复检

复杂图（≥4 个分区，或含表格/矩阵）在 `④.5` 的视觉闭环里**加一轮分块复检**：渲到 900 dpi 后切 4~6 块逐块 Read。

```bash
pdftoppm -r 900 -png -singlefile fig.pdf hi
python3 -c "from PIL import Image; im=Image.open('hi.png'); W,H=im.size; \
  im.crop((0,0,W//2,H//2)).save('q1.png')"
```

`pdf-overlap-checker.py` 是几何检测，**贴边、压框线、文字骑在边框上这类"没有真重叠但视觉上糊"的问题它不报**，整图缩略图也看不出来。

实测一张六格图切六块，查出五处 checker 未报的问题：编号圆圈压表格上边框、表头压表格上边线、版本格竖排互叠、标签超出框被切、出框箭头从节点腰上穿过。
