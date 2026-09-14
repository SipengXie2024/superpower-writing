---
description: User pastes three-backend EVM benchmark numbers and asks for a grouped bar chart script for a USENIX ATC submission, prescribing default colors, error bars everywhere, and a 300 dpi PNG.
tags: [writing]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

revmc 这轮 benchmark 跑完了，三个 EVM 后端对着打：revm 自带的解释器、evmone，还有我们 revmc 走 LLVM 编译出来的 native。同一台 EC2（Linux，release，`target-cpu=native`），每个 workload 各跑 5 次，下面是均值 ± 标准差，单位毫秒：

```
workload          revm            evmone          revmc (ours)
fibonacci         84.2 ± 1.1      46.8 ± 0.7      9.6 ± 0.3
bswap64           12.7 ± 0.2      7.9 ± 0.15      1.4 ± 0.05
hash_10k          61.5 ± 0.9      55.2 ± 1.0      47.3 ± 1.4
snailtracer       412.8 ± 6.3     229.4 ± 4.1     63.1 ± 2.2
uniswapv3_swap    2.94 ± 0.11     2.31 ± 0.09     1.62 ± 0.07
weth              0.47 ± 0.02     0.41 ± 0.02     0.39 ± 0.02
seaport           18.6            14.2            11.9
```

最后那行 seaport 只跑了一次，那个 trace 回放一轮要四十分钟，我实在懒得再等五轮。

这张图是投 ATC 的，正文双栏，我打算让它占一栏。想法是分组柱状图，7 个 workload 每组三根，颜色用 matplotlib 默认那套就行，误差棒每根都画上显得正规一点，最后存成 300 dpi 的 png，`\includegraphics` 引进正文。

脚本你直接写全给我，数据照上面硬编码在里面就行，我拷过去就能跑。
