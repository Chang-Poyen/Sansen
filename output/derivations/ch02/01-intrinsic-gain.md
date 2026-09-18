# 单管增益与 MOS／BJT 比较

对应：024、025、026。

## 电路与完整方程

NMOS 源极接地，栅极由理想小信号源驱动，漏极接理想偏置电流源。先保留有限负载 $R_L$；其导纳 $G_L=1/R_L$。

漏极 KCL：

$$
(g_o+G_L)v_o+g_m v_i=0.
$$

因此有号增益及增益大小为

$$
a_v=-\frac{g_m}{g_o+G_L}=-g_m(r_o\parallel R_L),\qquad
A_0=g_m(r_o\parallel R_L).
$$

理想电流源负载 $G_L=0$ 时，模型内精确得到 $A_0=g_mr_o$。

## 从器件电流重新得到教材式

本书平方律与厄利电压模型：

$$
I_D=K'\frac WL V_{OV}^{2},\quad
g_m=\left.\frac{\partial I_D}{\partial V_{GS}}\right|_Q
=2K'\frac WL V_{OV}=\frac{2I_D}{V_{OV}},
\quad r_o\simeq\frac{V_A}{I_D}.
$$

代入而不是直接引用结论：

$$
A_0\simeq
\underbrace{\frac{2I_D}{V_{OV}}}_{g_m}
\;\underbrace{\frac{V_A}{I_D}}_{r_o}
=\frac{2V_A}{V_{OV}}=\frac{2V_E L}{V_{OV}}.
$$

等价的乘法式为

$$ A_0\simeq (2I_D/V_{OV})(V_A/I_D). $$

电流消掉不表示任何改变电流的操作都不影响增益：固定 $W/L$ 时，改变 $I_D$ 也会改变 $V_{OV}$。只有在比较时固定 $V_{OV}$、以尺寸调整电流，才有此形式的电流独立性。

BJT 由 $I_C=I_S e^{V_{BE}/U_T}$ 得

$$
g_m=I_C/U_T,\qquad r_o\simeq V_A/I_C,\qquad
A_0\simeq V_A/U_T,\quad U_T=kT/q.
$$

教材数值：MOS $V_A=10$ V、$V_{OV}=0.2$ V 得 100；BJT $V_A=26$ V、$U_T=26$ mV 得 1000。忽略级间负载时，$100^3=1000^2=10^6$，解释 026 的三级与两级比较。

## 必要近似

| 步骤 | 原式 → 简式 | 条件／理由 | 何时失效 |
|---|---|---|---|
| 负载忽略 | $r_o\parallel R_L\to r_o$ | $R_L\gg r_o$；相对于简式的差异为 $r_o/(R_L+r_o)$ | 电阻负载或有限电流源阻抗 |
| 输出电阻 | $g_o=\partial I_D/\partial V_{DS}\to I_D/V_A$ | 线性的沟道长度调制近似 | $V_A$ 随偏置显著改变 |
| 尺寸结论 | $2V_A/V_{OV}\to2V_E L/V_{OV}$ | $V_A\propto L$，且 $V_E$ 在比较范围近似固定 | 短沟道效应 |
| 级联乘积 | $a_1a_2\cdots$ | 后级不负载前级、各级线性 | 有限输入阻抗、寄生电容 |

025 的「小 $V_{OV}$、大 $L$」是上述模型的方向性结论，不能延伸成无限制降低 $V_{OV}$；A2 会先失效，且带宽、面积与噪声限制尚未加入。

## 方法与验算

不用 SFG：一条 KCL 已直接显示跨导与输出电阻的乘积。符号检查验证 KCL 解与含 $R_L$ 的增益式相同。


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [024](../../extraction/index.html#SANSEN-024) | 51 | 52 | 51 |
| [025](../../extraction/index.html#SANSEN-025) | 52 | 53 | 51, 52 |
| [026](../../extraction/index.html#SANSEN-026) | 52 | 53 | 52 |
