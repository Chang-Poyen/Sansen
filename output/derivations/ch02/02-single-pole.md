# 单极点、GBW 与尺寸练习

对应：027–0210；027–028 共用同一电路。

## 输出电容主导：027–028

令 $R=r_o\parallel R_L$，只保留输出 $C_L$。由 KCL

$$
\left(\frac1R+sC_L\right)v_o=-g_mv_i
\quad\Rightarrow\quad
a_v(s)=\frac{-g_mR}{1+sRC_L}.
$$

因此

$$ A_0=g_mR,\quad \omega_p=\frac1{RC_L},\quad BW=\frac1{2\pi RC_L}. $$

幅度与相对低频的相位：

$$
|a_v(j\omega)|=\frac{A_0}{\sqrt{1+(\omega/\omega_p)^2}},
\qquad \Delta\phi=-\tan^{-1}(\omega/\omega_p).
$$

在 $\omega_p$ 幅度下降 $20\log_{10}(1/\sqrt2)=-3.0103$ dB，相对相位为 $-45^\circ$。高频幅度正比 $1/\omega$，所以每十倍频下降 20 dB。

由定义相乘可精确消去 $R$：

$$ GBW\equiv A_0BW=\frac{g_m}{2\pi C_L}. $$

但单位增益交越频率另由 $|a_v|=1$ 解得

$$ f_u=BW\sqrt{A_0^2-1}=GBW\sqrt{1-A_0^{-2}}\qquad(A_0>1). $$

所以图上把 $f_u$ 标成 GBW，还用了 $A_0\gg1$。图中的相位是**相对相位**；共源级的固定反相不可遗忘。

## 029：依教材定义逐步重算

规格 $GBW=100$ MHz、$C_L=3$ pF，故

$$
g_m=2\pi(100\times10^6)(3\times10^{-12})
=1.88496\ {\rm mS}.
$$

选择而非推导出 $V_{OV}=0.2$ V，则

$$
\frac{g_m}{I_D}=\frac2{V_{OV}}=10\ {\rm V}^{-1},\quad
I_D=\frac{g_mV_{OV}}2=188.50\ \mu{\rm A}.
$$

本书 $K'_n=50\ \mu{\rm A/V^2}$，没有额外 $1/2$：

$$
\frac WL=\frac{I_D}{K'_n V_{OV}^2}=94.248.
$$

再**选择** $L=4L_{\min}=2\ \mu$m，可得 $W=188.50\ \mu$m。
若按教材先把 $g_m$ 取整为 2 mS，就得到 $I_D=0.2$ mA、$W/L=100$、$W=200\ \mu$m。这些是取整差异，不是模型不一致。

$$
FOM=\frac{GBW\,C_L}{I_D}
=1591.55\ {\rm MHz\cdot pF/mA}
\simeq1500\quad\text{（采 0.2 mA 的取整电流）}.
$$

## 0210：只有输入电容

信号源经 $R_S$ 驱动栅极，$C_{GS}$ 接地，输出没有电容：

$$
\frac{v_g-v_i}{R_S}+sC_{GS}v_g=0,\qquad v_o=-g_mr_o v_g.
$$

$$
a_v=\frac{-g_mr_o}{1+sR_SC_{GS}},\quad
BW=\frac1{2\pi R_SC_{GS}},\quad
GBW=\frac{g_m}{2\pi C_{GS}}\frac{r_o}{R_S}.
$$

在此电容模型中定义 $f_T=g_m/(2\pi C_{GS})$，便是教材 $f_Tr_o/R_S$。
若再采 $C_{GS}\simeq\alpha C_{ox}WL$（长沟道常用 $\alpha\simeq2/3$），则

$$
GBW\simeq\frac{V_E}{\pi\alpha R_S C_{ox}W V_{OV}}.
$$

所以图上的 $1/(WC_{ox}V_{OV})$ 是省略固定系数的**比例关系**，不是量纲完整的等式。

## 必要近似与失效条件

| 步骤 | 原式 → 简式 | 必要条件 | 失效时 |
|---|---|---|---|
| 单极点 | 完整寄生网络 → 一个 $C_L$ 或 $C_{GS}$ | 其他极点高于关注频带 | 不能再从 $A_0BW$ 预测实际交越 |
| 交越 | $\sqrt{A_0^2-1}\to A_0$ | $A_0\gg1$ | $A_0$ 接近 1 时误差很大 |
| 电容尺度 | $C_{GS}\to\alpha C_{ox}WL$ | 忽略 交叠电容、边缘电容，强反转 | 短沟道、小尺寸 |
| 设计电压 | 指定 $V_{OV}=0.2$ V | 教材的设计选择，须另查工艺 | 不能把这个选择当规格唯一解 |

## 方法与验算

不用 SFG：两个互不反馈的一阶关系直接相乘最清楚。数值检查包括未取整及取整的 029 解，以及 GBW 与实际 $f_u$ 的差异。


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [027](../../extraction/index.html#SANSEN-027) | 53 | 54 | 53 |
| [028](../../extraction/index.html#SANSEN-028) | 53 | 54 | 53 |
| [029](../../extraction/index.html#SANSEN-029) | 54 | 55 | 54 |
| [0210](../../extraction/index.html#SANSEN-0210) | 54 | 55 | 54 |
