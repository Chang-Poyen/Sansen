# 第二章：教材公式差异与待厘清项目

这份表区分模型、符号与近似的限制，并非将所有差异都判成教材错误。对应推导保留完整方程；待厘清式不算已证明。

## D01 · 0216 · 线性区 M2 的 Cgs2

**拓扑条件** · PDF 57／书本 58

原图 M2 源极接地时 Cgs2 直接接输入与地，不能套用 M1 源极的自举因子；M2 栅极扰动也须包含其 gm2。

[查看完整推导](04-degeneration.html) · [Markdown](04-degeneration.md)

## D02 · 0221 · 输入输出 DC 相等与尺寸比

**DC 一致性** · PDF 60／书本 61

同 Vt、同 Vov 且相等电流时，平方律要求相等尺寸比；不能同时独立指定任意尺寸增益比。

[查看完整推导](05-diode-loads.html) · [Markdown](05-diode-loads.md)

## D03 · 0229 · 并联输出电阻

**代数系数** · PDF 64／书本 65

若 go 指单管导纳，ro/2=1/(2go)；正文所写 2/go 不相等。

[查看完整推导](07-inverter-ac.html) · [Markdown](07-inverter-ac.md)

## D04 · 0231 · 反相器的输入主导 GBW

**符号系数** · PDF 65／书本 66

若 gm、ro、fT 均使用单管定义，匹配反相器的输入主导 GBW 为 fT ro/(2Rs)；原式的二倍差异需区分单管与总量。

[查看完整推导](07-inverter-ac.html) · [Markdown](07-inverter-ac.md)

## D05 · 0232 · 反相器前馈零点

**符号系数** · PDF 65／书本 66

跨接总电容对应的零点为 Gm/CF；Gm 是 NMOS 与 PMOS 跨导之和。

[查看完整推导](07-inverter-ac.html) · [Markdown](07-inverter-ac.md)

## D06 · 0242 · 复极点区间与相消

**近似范围** · PDF 71／书本 72

精确区间须解判别式；图中的宽度量不能直接当精确上下界比。1/Rs 相消近似还需 Cgd 远小于 Cgs。

[查看完整推导](09-followers-hf.html) · [Markdown](09-followers-hf.md)

## D07 · 0243 · 输出阻抗的 gmu

**渐近式差异** · PDF 71／书本 72

完整分母代入零点得到 gm=Cgs/[Rs(Cgs+Cgd)]；教材带 Cds 的估式不等于一般精确相消条件。

[查看完整推导](09-followers-hf.html) · [Markdown](09-followers-hf.md)

## D08 · 0244 · BJT 的 gmr 与 gmu

**待厘清** · PDF 72／书本 73

保留有限 β 和 Cpi=CjE+gm tauF 后须重解判别式；教材 gmr 不能由本组冻结电容模型重现，尚需原模型或符号说明。gmu 也只在列出的额外条件下接近相消解。

[查看完整推导](10-emitter-hf.html) · [Markdown](10-emitter-hf.md)

## D09 · 0245 · 有源电感的串联电阻

**频带条件** · PDF 72／书本 73

Rs 是简化模型的高频阻抗极限；低频 Taylor 等效的串联电阻是 1/gm，L=(Rs−1/gm)/omegaT。

[查看完整推导](11-active-inductors.html) · [Markdown](11-active-inductors.md)

## D10 · 0247 · 差分电感与半电路

**端口定义** · PDF 73／书本 74

跨两输出端的差分电感为每半边等效电感的两倍；调谐电容也须依同一端口定义换算。

[查看完整推导](11-active-inductors.html) · [Markdown](11-active-inductors.md)

## D11 · 0256 · No 米勒 effect 的语义

**近似范围** · PDF 78／书本 79

跨接电容与 RHP 零点仍在完整模型中；此叙述仅指某参数区域的主极点不受米勒放大项主导。

[查看完整推导](14-cascode-miller.html) · [Markdown](14-cascode-miller.md)

## D12 · 0264 · 辅助 GBW 与原共源共栅级 BW 对齐

**模型限制** · PDF 82／书本 83

在明列的 B(s) 单极点模型中，精确相消条件指向 go2/CL，并非原共源共栅级主极点；不能当成普遍设计等式。

[查看完整推导](18-gain-boosting.html) · [Markdown](18-gain-boosting.md)

## D13 · 0265 · Step response 的快慢留数

**时间近似** · PDF 83／书本 84

精确快慢系数之和等于 1；将快系数直接写成 1 会牺牲 t=0 的一致性，只能视为小留数或晚时间近似。

[查看完整推导](19-doublet-settling.html) · [Markdown](19-doublet-settling.md)

