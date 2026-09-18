# CMOS 反相器的增益、两极点与米勒限制

对应：0228–0233。

## 用总跨导避免倍数混淆

$$ G_m=g_{mn}+g_{mp},\quad G_o=g_{on}+g_{op},\quad R_o=1/G_o. $$

输入上升，NMOS 吸入增大、PMOS 供出减小，两项都使输出下降：

$$
(G_o+sC_L)v_o=-G_mv_i,\quad
a_v=-\frac{G_mR_o}{1+sR_oC_L}.
$$

$$
A_0=G_mR_o,\quad BW=\frac1{2\pi R_oC_L},\quad GBW=\frac{G_m}{2\pi C_L}.
$$

匹配且两管同 $I_D,V_{OV},V_A$：

$$
G_m=2g_m,\quad G_o=2g_o,\quad R_o=r_o/2,\quad
a_v(0)=-g_mr_o\simeq-\frac{2V_A}{V_{DD}/2-V_T}.
$$

这解释 current reuse：同一 DC 电流产生两个 AC 跨导。0229 正文将 $r_o/2$ 说成 $2/g_o$ 是倒数错误；应为 $1/(2g_o)$。

## 0231：只有输入、输出对地电容

令 $C_i=C_{GSn}+C_{GSp}$，栅极前有 $R_S$：

$$ a_v=\frac{-G_mR_o}{(1+sR_SC_i)(1+sR_oC_L)}. $$

两极点为 $1/(R_SC_i)$、$1/(R_oC_L)$。若 $R_SC_i\gg R_oC_L$，输入极点主导。若还要把主极点 GBW 当交越频率，另一极点须高于交越，光是高于主极点仍不足。

$$ GBW_i\simeq\frac{G_mR_o}{2\pi R_SC_i}. $$

匹配时 $C_i=2C_{GS}$，单管 $f_T=g_m/(2\pi C_{GS})$：

$$ GBW_i=\frac{f_Tr_o}{2R_S}. $$

**教材差异：** 0231 写 $f_Tr_{DS}/R_S$，主导条件写 $R_SC_{GSt}>r_{DS}C_L$。按同章 $r_{DS}$ 是单管阻抗的定义，这两处都少了系数 $1/2$。若改定义成总 $R_o$，必须明示。

## 0232–0233：加入 $C_F=C_{GDn}+C_{GDp}$

完整矩阵：

$$
\begin{bmatrix}
G_S+s(C_i+C_F)&-sC_F\\
G_m-sC_F&G_o+s(C_L+C_F)
\end{bmatrix}
\begin{bmatrix}v_g\\v_o\end{bmatrix}
=\begin{bmatrix}G_Sv_i\\0\end{bmatrix}.
$$

展开：

$$ a_v(s)=\frac{-A_0(1-sC_F/G_m)}{1+a_1s+a_2s^2}, $$

$$ a_1=R_o(C_L+C_F)+R_S(C_i+C_F)+A_0R_SC_F, $$

$$ a_2=R_SR_o(C_iC_L+C_iC_F+C_FC_L). $$

$$
s_{p1,p2}=\frac{-a_1\pm\sqrt{a_1^2-4a_2}}{2a_2},\qquad
s_z=\frac{G_m}{C_F}.
$$

匹配时零点为 $2g_m/C_F$。0232 若写 $1-sC_F/g_m$，其中 $g_m$ 必须是总跨导，否则零点差一倍。

## 逐步化成教材分母

先令 $C_i=0$，再忽略 $C_F(R_o+R_S)$：

$$
a_v\simeq\frac{-A_0(1-sC_F/G_m)}
{1+s(R_oC_L+A_0R_SC_F)+s^2R_SR_oC_FC_L}.
$$

| 近似 | 必要条件 | 失效时 |
|---|---|---|
| 忽略 $C_i$ | 对 $a_1,a_2$ 贡献均远小于保留项 | 用完整矩阵 |
| 省 $C_F(R_o+R_S)$ | $C_F(R_o+R_S)\ll R_oC_L+A_0R_SC_F$ | 大 $A_0$ 本身不保证可省 |
| 根分离 | $a_1^2\gg4a_2$ | 用完整二次方程 |
| 米勒主导 | $G_mR_SC_F\gg C_L$ | 交界处保留两个时间常数 |
| GBW 近似交越 | 大 $A_0$、交越远离零点和次极点 | 不可只乘低频增益与 BW |

根分离时 $\omega_d\simeq1/a_1,\ \omega_{nd}\simeq a_1/a_2$。0233 的条件因此为

$$
R_SC_F\gg\frac{C_L}{G_m}=\frac1{2\pi GBW_{\rm load}},
\qquad GBW_{\rm Miller}\simeq\frac1{2\pi R_SC_F}.
$$

SFG 机制与 03 组相同，只需换成总 $G_m$ 并加入对地电容，不再画重复图。矩阵行列式、零点及匹配因子均由符号程序检查。
