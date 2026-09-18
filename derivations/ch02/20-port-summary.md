# 全章端口参数总表：端接、有限 β 与适用极限

对应：0266–0270；0269 的完整 MOS 共栅推导见 12 组。表中的 $R_{\rm out,amp}$ 排除外加负载；含负载时还要并联该负载。

## 0266–0267：MOS 四种基本用法

在低频、衬底跟源极相连、忽略栅极漏电下：

| 配置 | 完整模型或前节引用 | 教材极限 |
|---|---|---|
| 共源，源极接地 | $G_m=g_m,\ R_{\rm in}=\infty,\ R_{\rm out}=r_o$ | 同左 |
| 共源，源极接 $R_B$ | $G_m=g_m/[1+(g_m+g_o)R_B]$ | $1/R_B$，须 $g_mR_B\gg1,g_o\ll g_m$ |
| 同上输出阻抗 | $r_o+(1+g_mr_o)R_B$ | $g_mr_oR_B$，须可省两个独立阻抗项 |
| 源极跟随器，理想偏置源 | $a_v=g_m/(g_m+g_o)$ | $1$，须 $g_mr_o\gg1$ |
| follower，源极负载 $R_B$ | $a_v=g_m/(g_m+g_o+1/R_B)$ | $1$，另须 $g_mR_B\gg1$ |
| follower 输出阻抗 | $1/(g_m+g_o)$，有偏置电阻则再并联 | $1/g_m$ |

电压 follower 的 $\infty$ 输入电阻只限 DC／低频栅极无电流模型；高频已有 09 组的电容电流。

## 0268：BJT 增加基极电阻与输入电流

定义 intrinsic $r_\pi=\beta/g_m$、基极 spreading $r_b$。

若忽略 $r_o$，发射极负载为 $R_E$：

$$
R_{\rm in}=r_b+r_\pi+(\beta+1)R_E,
$$

$$
G_{m,\rm ext}=
\frac{\beta}{r_b+r_\pi+(\beta+1)R_E}.
$$

$R_E=0$ 且 $r_b\ll r_\pi$ 时 $G_{m,\rm ext}\simeq g_m$。
深度负反馈时 $G_{m,\rm ext}\simeq1/R_E$ 还要求 $\beta\gg1$。

对输入置零的输出阻抗，令基极到外部 AC 地的电阻为 $R_b$（可含信号源电阻及 $r_b$），且

$$
R_* = R_E\parallel(r_\pi+R_b),\qquad
g_* = g_m\frac{r_\pi}{r_\pi+R_b}.
$$

由发射极 KCL $v_e=i_tR_*$ 和集电极电流式可得

$$ R_{\rm out,amp}=r_o+(1+g_*r_o)R_*. $$

所以教材 $g_mr_oR_E$ 还隐含 $R_E\ll r_\pi+R_b$、$R_b\ll r_\pi$。如果发射极偏置源理想，$R_E\to\infty$，输出阻抗饱和至约 $\beta r_o$，不会像 MOS 那样无界增加。

Follower 的精确低频输出阻抗（忽略 $r_o$）为

$$
R_{\rm out}=\frac{R_S+r_b+r_\pi}{\beta+1},
$$

可按 08 组再化成 $1/g_m+(R_S+r_b)/\beta$。
看入基极的负载应包含发射极的 $r_o$ 或偏置源阻抗，再乘 $\beta+1$；这解释 0268 表中的 $\beta r_o$ 项。

## 0270：BJT 共基级

基极接 AC 地，先取 $r_b=0$。源极名称改为发射极。其节点方程：

$$
(G_B+g_\pi+g_m+g_o)v_e-g_ov_o=i_{\rm in},
$$

$$
-(g_m+g_o)v_e+(G_L+g_o)v_o=0.
$$

因此 12 组的 MOS 式可用

$$ R_B^*=R_B\parallel r_\pi $$

取代 $R_B$，得到

$$
A_R=\frac{(1+g_mr_o)R_B^*R_L}
{R_L+r_o+(1+g_mr_o)R_B^*},
$$

$$
R_{\rm in}=\frac{R_B^*(R_L+r_o)}
{R_L+r_o+(1+g_mr_o)R_B^*}.
$$

有限 $r_b$ 时则用 $R_B^*=R_B\parallel(r_\pi+r_b)$，并把 $g_m$ 换成
$g_mr_\pi/(r_\pi+r_b)$。这是由基极支路分压取得，不是直接把 $\beta$ 塞进公式。

### 三个重要极限

1. $R_L$ 小、$R_B^*$ 足够大：$R_{\rm in}\simeq1/g_m$，$A_R\simeq R_L$，误差包含 $1/\beta$。
2. $R_L\to\infty$、有限 $R_B$：$R_{\rm in}\to R_B^*$，$A_R\to(1+g_mr_o)R_B^*$。
3. $R_B,R_L\to\infty$，但有限电流增益 β：$R_{\rm in}\to r_\pi$，$A_R\to(1+g_mr_o)r_\pi\simeq\beta r_o$。与 MOS 的无有限静态解不同，BJT 有基极电流路径。原表「—」不可解读成跨阻为 0。

## 方法与核对

不用 SFG：这是前面模型的端接极限总结。每次求 $R_{\rm out}$ 都先把独立电压输入短路、独立电流输入开路，并保留其内阻。用这套定义才能一致阅读 0267–0270 的表格。
