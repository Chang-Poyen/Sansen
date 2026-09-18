# 电阻、电感与 MOS 源极负反馈

对应：0214–0216。这里 $R_S$ 或 $L_S$ 位于源极与地之间，不是栅极前的信号源电阻。

## 0214：先保留 $r_o$ 的低频模型

设源极电压 $v_x$、负反馈阻抗 $Z_S$，且衬底跟源极相连：

$$
i_d=g_m(v_i-v_x)+g_o(v_o-v_x),\qquad v_x=Z_Si_d.
$$

代回并收集：

$$
i_d[1+(g_m+g_o)Z_S]=g_mv_i+g_ov_o.
$$

因此短路输出跨导与输出电阻为

$$
G_{mS}=\left.\frac{i_d}{v_i}\right|_{v_o=0}
=\frac{g_m}{1+(g_m+g_o)Z_S},\qquad
Z_{\rm out}=\left.\frac{v_o}{i_d}\right|_{v_i=0}
=r_o+(1+g_mr_o)Z_S.
$$

取 $Z_S=R_S$ 并依序近似：

$$
G_{mR}\simeq\frac{g_m}{1+g_mR_S}\simeq\frac1{R_S},
\qquad R_{\rm out}\simeq r_o(1+g_mR_S)\simeq g_mr_oR_S.
$$

低频、输出短路时 $v_x/v_i=g_mR_S/[1+(g_m+g_o)R_S]$。由 $i_g=sC_{GS}(v_i-v_x)$，得到一阶输入电容系数

$$
C_{\rm in}=C_{GS}\frac{1+g_oR_S}{1+(g_m+g_o)R_S}
\simeq\frac{C_{GS}}{1+g_mR_S}.
$$

这不是任意输出负载下通用的输入电容。$v_x/v_i$ 会随漏极终端改变。

## 0215：源极电感负反馈

忽略 $r_o$、$C_{GD}$，但保留 $C_{GS}$。令 $v_{gs}=v_i-v_x$：

$$
i_g=sC_{GS}v_{gs},\quad
i_s=(g_m+sC_{GS})v_{gs},\quad v_x=sL_Si_s.
$$

所以

$$
Z_{\rm in}=\frac{v_{gs}+sL_S(g_m+sC_{GS})v_{gs}}{sC_{GS}v_{gs}}
=\frac1{sC_{GS}}+sL_S+\frac{g_mL_S}{C_{GS}}.
$$

定义 $\omega_T=g_m/C_{GS}$，电阻项为 $L_S\omega_T$。只有在
$\omega_0=1/\sqrt{L_SC_{GS}}$ 附近，容性与感性虚部相消，输入才近似纯电阻。

若在求跨导时省略 $C_{GS}$，上一节给

$$
G_{mL}\simeq\frac{g_m}{1+sg_mL_S},\qquad
Z_{\rm out}\simeq r_o(1+sg_mL_S).
$$

若保留 $C_{GS}$，短路跨导则是

$$ G_{mL}=\frac{g_m}{1+sg_mL_S+s^2L_SC_{GS}}. $$

因此教材的 $G_{mL}$ 与 $Z_{\rm in}$ 使用不同层级的电容保留方式，必须分清。

## 0216：用 线性区 MOS 当负反馈电阻

两只 NMOS 的栅极同接 $v_i$；M1 源极接 M2 漏极（节点 $x$），M2 源极接地。DC 几何关系：

$$ V_{DS2}=V_{GS2}-V_{GS1}. $$

M2 的 线性区 近似：

$$
I_2=KP\frac{W_2}{L_2}
\left[(V_{GS2}-V_T)V_{DS2}-\frac{V_{DS2}^2}{2}\right].
$$

分别微分：

$$
g_{o2}=KP\frac{W_2}{L_2}(V_{GS2}-V_T-V_{DS2}),\quad
g_{m2}=KP\frac{W_2}{L_2}V_{DS2}.
$$

只有 $V_{DS2}\ll V_{GS2}-V_T$ 才有

$$
r_{o2}\simeq[KP(W_2/L_2)(V_{GS2}-V_T)]^{-1},\qquad g_{m2}\ll g_{o2}.
$$

两管电流相等给出

$$
(g_{m1}+g_{o1}+g_{o2})v_x
=(g_{m1}-g_{m2})v_i+g_{o1}v_o.
$$

因此

$$
R_{\rm out}=r_{o1}+r_{o2}+g_{m1}r_{o1}r_{o2},
$$

$$
G_{m,\rm eff}
=\frac{g_{m1}g_{o2}+g_{m2}(g_{m1}+g_{o1})}
{g_{m1}+g_{o1}+g_{o2}}.
$$

**教材差异：输入电容。** M2 源极接地，其 $C_{GS2}$ 没有被源极跟随所自举。只计两个 $C_{GS}$ 时，

$$
C_{\rm in}=C_{GS1}(1-H_x)+C_{GS2},\qquad
H_x=\left.\frac{v_x}{v_i}\right|_{v_o=0}.
$$

不能从此连接得到幻灯片的 $(C_{GS1}+C_{GS2})/(1+g_{m1}r_{o2})$。若另计 M2 的 $C_{GD2}$，它应与 $C_{GS1}$ 一样乘 $1-H_x$。

## 必要近似

| 原式 → 简式 | 条件 | 失效情况 |
|---|---|---|
| $g_m+g_o\to g_m$ | $g_mr_o\gg1$ | 低本征增益 |
| $r_o+(1+g_mr_o)R_S\to r_o(1+g_mR_S)$ | 被省的 $R_S\ll r_o(1+g_mR_S)$ | 串联项显著 |
| $g_m/(1+g_mR_S)\to1/R_S$ | $g_mR_S\gg1$ | 反馈深度不足 |
| $C_{\rm in}$ 分子 $1+g_oR_S\to1$ | $R_S\ll r_o$ | 只用 $g_mr_o\gg1$ 不够 |
| 忽略 $s^2L_SC_{GS}$ | $\omega^2L_SC_{GS}\ll|1+j\omega g_mL_S|$ | 共振附近 |
| 理想电感无额外热噪声 | 损耗电阻为零 | 真实 ESR／基板损耗 |
| M2 视为固定电阻 | $g_{m2}$ 项相对保留项足够小 | 「0.2 V 很小」不是充分条件 |

不用 SFG：一个源极电压的消元已明确显示负反馈作用。
