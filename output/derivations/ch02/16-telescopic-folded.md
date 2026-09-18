# 套筒式与折叠式共源共栅级

对应：0258–0259。

## 0258：上下两个共源共栅级阻抗并联

下方 NMOS 堆栈的阻抗

$$ R_N=r_{o1}+r_{o2}+(g_{m2}+g_{mb2})r_{o1}r_{o2}. $$

上方 PMOS 堆栈同理为 $R_P$（使用相应器件参数及正值跨导）。输出看到

$$ R_{\rm out}=R_N\parallel R_P. $$

只有 $R_N=R_P$ 才有 $R_{\rm out}=R_N/2$；再忽略体效应与独立 $r_o$ 项，才到教材

$$ R_{\rm out}\simeq\tfrac12g_{m2}r_{o1}r_{o2}. $$

输入电流传递跨导 $G_{\rm eff}$ 由 13 组求出，通常近似 $g_{m1}$：

$$
a_v\simeq-\frac{g_{m1}R_{\rm out}}{1+sR_{\rm out}C_L},\quad
BW=\frac1{2\pi R_{\rm out}C_L},\quad
GBW\simeq\frac{g_{m1}}{2\pi C_L}.
$$

理想 long-channel 饱和要求的输出范围：

$$
V_{OV1}+V_{OV2}\lesssim V_O
\lesssim V_{DD}-V_{OV3}-V_{OV4}.
$$

每管 $V_{OV}\simeq0.2$ V 时，可用范围约 $V_{DD}-0.8$ V。这是给定偏置的电压裕量估计，不是跨工艺常数。

## 0259：折叠电流路径

M1 漏极接节点 $x$；上方电流源提供 $I_{B1}$；PMOS M2 从 $x$ 把电流送往输出，输出另由 $I_{B2}$ 吸走偏置。

$$ I_{D1}+I_{D2}=I_{B1},\quad I_{D2}=I_{B2}
\Rightarrow I_{D1}=I_{B1}-I_{B2}. $$

若选 $I_{B1}=2I_{B2}$，两管电流相同；$I_{B1}/2$ 是设计选择，不是拓扑必然。

有限偏置源下，$x$ 点原始阻抗

$$ R_x=r_{o1}\parallel r_{B1}. $$

从 M2 漏极看入的共源共栅级支路

$$ R_{\rm branch}=r_{o2}+[1+(g_{m2}+g_{mb2})r_{o2}]R_x. $$

输出还要与下方电流源阻抗并联：

$$ R_{\rm out}=R_{\rm branch}\parallel r_{B2}. $$

理想 $r_{B1},r_{B2}\to\infty$、$g_{mb2}=0$、高本征增益时，才得到原图
$R_{\rm out}\simeq g_{m2}r_{o1}r_{o2}$。

输入变大会让 M1 多吸电流，使供到输出的 PMOS 电流变少，故本图电压增益仍反相。把输入电流有效传递率近似为 1 后：

$$
a_v\simeq-\frac{g_{m1}R_{\rm out}}{1+sR_{\rm out}C_L},\qquad
GBW\simeq\frac{g_{m1}}{2\pi C_L}.
$$

## 比较条件

- 同输入管电流时，等电流分配的折叠式支路要求供电电流约两倍；不是任意 sizing 下都精确两倍。
- 原书说折叠式与套筒式摆幅相近，还依赖偏置源用几颗管实现，不能由两个理想电流源图唯一决定。
- 忽略体效应、有限偏置源阻抗、内部电容，均需分别验证。
- 不用 SFG：逐支路计阻抗及电流守恒已清楚呈现折叠的意义。


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [0258](../../extraction/index.html#SANSEN-0258) | 79 | 80 | 79 |
| [0259](../../extraction/index.html#SANSEN-0259) | 80 | 81 | 79, 80 |
