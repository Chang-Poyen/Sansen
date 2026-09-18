# 共栅级的跨阻、输入阻抗与有限偏置电阻

对应：0249–0252、0269、0271。

## 电流方向与连接

栅极接 AC 地；漏极接 $R_L$，源极接注入信号电流 $i_{\rm in}$ 及偏置源输出电阻 $R_B$。本节 $i_{\rm in}$ 定义为**注入源极节点**，因此与 0271 的向下电流箭头相反；比较有号结果时须反号。

令 $v_x$ 是源极电压，$G_L=1/R_L,\ G_B=1/R_B$，不含体效应：

$$
(G_B+g_m+g_o)v_x-g_ov_o=i_{\rm in},
$$

$$
-(g_m+g_o)v_x+(G_L+g_o)v_o=0.
$$

## 直接解 KCL

令 $Q=1+g_mr_o$，乘开导纳分母后：

$$
A_R=\frac{v_o}{i_{\rm in}}
=\frac{Q R_BR_L}{R_L+r_o+Q R_B},
$$

$$
R_{\rm in}=\frac{v_x}{i_{\rm in}}
=\frac{R_B(R_L+r_o)}{R_L+r_o+Q R_B}.
$$

流入负载的电流比为

$$ \frac{i_L}{i_{\rm in}}=\frac{A_R}{R_L}
=\frac{Q R_B}{R_L+r_o+Q R_B}. $$

受控源电流的大小比为 $g_mR_{\rm in}$。它可能大于 1，但真正输送到负载的电流比仍由上一式决定；不可混淆受控源内部循环电流与外部负载电流。

## 渐近区域与教材 $R_{Lc}$

实际分母的转折尺度为

$$ R_{\rm crit}=r_o+Q R_B. $$

若 $g_mr_o\gg1,\ g_mR_B\gg1$，则

$$ R_{\rm crit}\simeq R_{Lc}=g_mr_oR_B. $$

| 区域 | $A_R$ | $R_{\rm in}$ | 条件 |
|---|---|---|---|
| 小负载 | $\simeq R_L$ | $\simeq1/g_m$ | $R_L\ll r_o$ 且 $Q R_B\gg r_o$ |
| 中间 | $\simeq R_L$ | $\simeq R_L/(g_mr_o)$ | $r_o\ll R_L\ll Q R_B$ |
| 大负载 | $\to Q R_B$ | $\to R_B$ | $R_L\gg r_o+Q R_B$ |

大负载时，$i_L/i_{\rm in}\to0$，而内部受控源电流比趋近 $g_mR_B$，解释 0251 图的两条不同曲线。

## 0271：理想输出电流源负载

取 $R_L\to\infty$：

$$ v_x=R_Bi_{\rm in},\quad
v_o=(1+g_mr_o)v_x,\quad
A_R=(1+g_mr_o)R_B\simeq g_mr_oR_B.
$$

若采原图向下的 $i_{\rm in}$，两个电压与 $A_R$ 都反号。教材的正值 $A_R$ 是大小。

## 输出阻抗必须说明是否包含负载

将输入信号电流源开路、注入漏极测试电流，放大器本体阻抗为

$$ R_{\rm out,amp}=r_o+(1+g_mr_o)R_B. $$

若测量端包含外置 $R_L$，则 $R_{\rm out,loaded}=R_{\rm out,amp}\parallel R_L$。0269 表中含 $R_L$ 却列很大的 $R_{\rm out}$，是**排除外置负载的放大器本体值**；必须先讲清楚端口定义。

$R_B\to\infty$ 而 $R_L$ 有限时：$A_R=R_L$，$R_{\rm in}=(R_L+r_o)/(1+g_mr_o)$。若 $R_B,R_L$ 都理想无限，注入非零 DC 小信号电流没有有限的静态解；不能把表格的「—」当成 0。

不用 SFG：二节点矩阵与三个极限已完整解释图形。符号程序验证两个阻抗、跨阻及端点极限。


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [0249](../../extraction/index.html#SANSEN-0249) | 74 | 75 | 74 |
| [0250](../../extraction/index.html#SANSEN-0250) | 75 | 76 | 75 |
| [0251](../../extraction/index.html#SANSEN-0251) | 75 | 76 | 75, 76 |
| [0252](../../extraction/index.html#SANSEN-0252) | 76 | 77 | 76 |
| [0269](../../extraction/index.html#SANSEN-0269) | 85 | 86 | 85 |
| [0271](../../extraction/index.html#SANSEN-0271) | 86 | 87 | 86 |
