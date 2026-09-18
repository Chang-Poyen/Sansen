# BJT 高频输出阻抗：有限 β 与扩散电容

对应：0244。

## 先指定足够完整的模型

集电极接 AC 地；基极经 $R_S$ 接地（测量输出阻抗时输入置零），忽略基区扩展电阻时：

$$
g_\pi=1/r_\pi=g_m/\beta,\quad
Y_\pi=g_\pi+sC_\pi,\quad
C_\pi=C_{jE}+g_m\tau_F.
$$

$C_\mu$ 是基极–集电极电容，$C_{CE}$ 是发射极对 AC 地电容。若要保留 $r_b$，将外部 $R_S$ 换成 $R_S+r_b$。

由基极与发射极 KCL：

$$
\begin{bmatrix}
G_S+Y_\pi+sC_\mu&-Y_\pi\\
-(g_m+Y_\pi)&g_m+Y_\pi+g_o+sC_{CE}
\end{bmatrix}
\begin{bmatrix}v_b\\v_e\end{bmatrix}
=\begin{bmatrix}0\\i_t\end{bmatrix}.
$$

因此

$$
Z_e(s)=\frac{N(s)}{D(s)},\quad
N=G_S+Y_\pi+sC_\mu,
$$

$$
D=N(g_m+Y_\pi+g_o+sC_{CE})-Y_\pi(g_m+Y_\pi).
$$

这是本模型内完整式；用其二次多项式的判别式求复极点，用 $D(s_z)$ 检查相消。

## 零点与教材对照

$$
s_z=-\frac{G_S+g_\pi}{C_\pi+C_\mu},\qquad
f_z=\frac1{2\pi(R_S\parallel r_\pi)(C_\pi+C_\mu)}.
$$

这一式直接重现 0244 的零点。$\beta\to\infty$ 才能把 $R_S\parallel r_\pi$ 改成 $R_S$。

在 $g_o=0$ 下，常见的非退化相消条件来自
$g_m+Y_\pi(s_z)=0$：

$$
g_m(C_\pi+C_\mu)+g_\pi C_\mu-G_SC_\pi=0.
$$

代入 $C_\pi=C_{jE}+g_m\tau_F$、$g_\pi=g_m/\beta$：

$$
\tau_Fg_m^2+
g_m(C_{jE}+C_\mu+C_\mu/\beta-G_S\tau_F)
-G_SC_{jE}=0.
$$

令括号系数为 $b$，可用正根

$$
g_{m,\rm cancel}=\frac{-b+\sqrt{b^2+4\tau_FG_SC_{jE}}}{2\tau_F}.
$$

若扩散电容可忽略、$\beta\gg1$，才化为

$$ g_{m,\rm cancel}\simeq\frac{C_{jE}}{R_S(C_{jE}+C_\mu)}. $$

## 哪些原图公式不能直接当精确值

0244 的 $g_{mu}\simeq(C_{jE}+C_{CE})/[R_S(C_{jE}+C_\mu)]$ 在
$C_{CE}\ll C_{jE}$、$g_m\tau_F\ll C_{jE}$、$\beta\gg1$ 时接近上式；任意保留 $C_{CE}$ 时并非完整模型的相消解。

原图的 $g_{mr}=(C_\pi+C_{CE})/[R_S(C_\pi+C_\mu)]$ 也不能直接视为精确复极点区域中心。若冻结所有电容且取 $\beta\to\infty,g_o=0$，上一组推导的中心应为

$$ g_{mr,\rm frozen}=\frac{C_\pi+C_{CE}}{R_SC_\mu}. $$

这与原式分母不同。若让 $C_\pi$ 随 $g_m$ 变动，则需指定 $\tau_F,C_{jE},\beta$ 再解判别式，不能只替换字母。**此原图中心式列为模型／符号待厘清，未标成已证明。**

## 感性阻抗

再忽略 $g_\pi,g_o,C_\mu,C_{CE}$，可得

$$ Z_e=\frac{1+sR_SC_\pi}{g_m+sC_\pi}. $$

在 $\omega\ll\omega_T=g_m/C_\pi$ 展开：

$$
Z_e\simeq\frac1{g_m}
+s\frac{C_\pi}{g_m}\left(R_S-\frac1{g_m}\right).
$$

若 $g_mR_S\gg1$，等效电感 $L\simeq R_S/\omega_T$，重现原图。

## 方法与限制

不另画 SFG：它是上一组模型增加 $g_\pi$ 的版本，矩阵最容易核对。不能用「BJT 类似 MOS」而省掉有限电流增益 β、扩散电容及原图未交代的跨导扫描条件。符号检查涵盖矩阵、零点与相消条件，未确认的 $g_{mr}$ 式明列于差异表。
