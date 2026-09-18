# Source／射极跟随器的 DC、增益与阻抗

对应：0236–0240；亦供 0266–0268 的总表引用。

## MOS：固定电流如何产生跟随

漏极接 AC 地，输出在源极。若衬底跟源极相连、理想偏置电流固定且忽略 $r_o$：

$$
I_B=K'(W/L)(V_{GS}-V_{T0})^2
\Rightarrow V_{GS}=V_{T0}+\sqrt{I_B/[K'(W/L)]}.
$$

$V_{GS}$ 在这个模型中固定，所以 $V_O=V_I-V_{GS}$，微分后 $a_v=1$。

若保留 $g_o$、固定衬底的 $g_{mb}$、负载／偏置导纳 $G_B$，源极 KCL 是

$$
[g_m+g_{mb}+g_o+G_B+sC_L]v_o=g_mv_i.
$$

因此

$$
a_v(s)=\frac{g_m}{g_m+g_{mb}+g_o+G_B+sC_L},\qquad
R_{\rm out,amp}=\frac1{g_m+g_{mb}+g_o}.
$$

若把偏置支路也包含在测量内，$R_{\rm out}$ 还要与 $1/G_B$ 并联。

## 0238–0239：衬底固定的微分

固定 $K'$、固定电流时

$$
V_I=V_O+V_{T0}+\gamma[\sqrt{\Phi+V_O}-\sqrt{\Phi}]+V_{OV},
\quad \Phi=|2\phi_F|.
$$

对 $V_O$ 微分：

$$
\frac{dV_I}{dV_O}=1+\frac{\gamma}{2\sqrt{\Phi+V_O}}
=1+\frac{g_{mb}}{g_m}\equiv n.
$$

所以

$$ a_v=\frac1n,\quad R_{\rm out}\simeq\frac1{ng_m}<\frac1{g_m}. $$

$n$ 是**工作点局部值**，不能当固定全域斜率。再微分可得此固定电流模型的曲率：

$$
\frac{d^2V_O}{dV_I^2}
=\frac{\gamma}{4(\Phi+V_O)^{3/2}n^3}.
$$

0239 的曲线可说明「体效应使增益小于 1 且非线性」，不应将示意曲线的具体曲率当成此简化模型的数值结果。负载电流或 $K'$ 随偏置改变时，上面的固定电流曲率也会改变。

## 0240：BJT 的有限基极电流

先忽略 $r_o$，令 $r_\pi=\beta/g_m$，外部基极电阻为 $r_b$。由
$i_e=(\beta+1)i_b,\ v_{be}=r_\pi i_b$：

若发射极负载为 $R_E$，

$$
R_{\rm in,base}=r_b+r_\pi+(\beta+1)R_E,
$$

$$
\frac{v_o}{v_i}
=\frac{(\beta+1)R_E}
{R_S+r_b+r_\pi+(\beta+1)R_E}.
$$

输入置零、向发射极注入测试电流：

$$
R_{\rm out}=\frac{R_S+r_b+r_\pi}{\beta+1}
=\frac{\beta}{\beta+1}\frac1{g_m}
+\frac{R_S+r_b}{\beta+1}.
$$

用 $\beta\gg1$ 才得到教材
$R_{\rm out}\simeq1/g_m+(R_S+r_b)/(\beta+1)$，进一步可把 $\beta+1$ 换成 $\beta$。

## 近似记录

| 原式 → 简式 | 必要条件 | 失效情况 |
|---|---|---|
| MOS $a_v\to1$ | $g_{mb}+g_o+G_B\ll g_m$ | 体效应、重负载 |
| $R_{\rm out}\to1/g_m$ | 同上但需区分是否包含外置负载 | 理想电流源不代表器件 $r_o=\infty$ |
| 体效应 $a_v=1/n$ | 固定电流、固定 $K'$；忽略 $g_o,G_B$ | 有限偏置阻抗 |
| BJT $a_v\to1$ | $(\beta+1)R_E\gg R_S+r_b+r_\pi$ | 小发射极负载 |
| $\beta/(\beta+1)\to1$ | $\beta\gg1$ | 低电流或高频 $\beta$ 下降 |

不用 SFG：此处 DC 微分与单节点 KCL 已足够。高频跨接电容留到下一组才使用 SFG。
