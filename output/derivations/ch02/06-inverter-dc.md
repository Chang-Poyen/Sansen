# CMOS 反相器的工作点与大信号电流

对应：0223–0227、0234。

## 连接与 KCL

NMOS 源极接地，PMOS 源极接 $V_{DD}$；两栅极接 $V_I$，两漏极接 $V_O$。正值 $I_n,I_p$ 分别代表吸入地与从电源供出的电流：

$$
V_{GSn}=V_I,\quad V_{DSn}=V_O,\quad
V_{SGp}=V_{DD}-V_I,\quad V_{SDp}=V_{DD}-V_O.
$$

$$ C_L\frac{dV_O}{dt}=I_p-I_n. $$

DC 时 $I_n=I_p$；瞬态中差值就是电容充放电电流。

## 由电流相等解切换中心

令 $k_n=K'_n(W/L)_n,\ k_p=K'_p(W/L)_p$。两管饱和且忽略沟道长度调制：

$$
I_n=k_n(V_I-V_{Tn})^2,\quad
I_p=k_p(V_{DD}-V_I-|V_{Tp}|)^2.
$$

取正平方根并解出：

$$
V_M=\frac{\sqrt{k_p}(V_{DD}-|V_{Tp}|)+\sqrt{k_n}V_{Tn}}
{\sqrt{k_n}+\sqrt{k_p}}.
$$

若 $V_{Tn}=|V_{Tp}|=V_T$ 且要求 $V_M=V_{DD}/2$，得到 $k_n=k_p$：

$$
K'_n\frac{W_n}{L_n}=K'_p\frac{W_p}{L_p},\qquad
I_{DQ}=k_n(V_{DD}/2-V_T)^2.
$$

但忽略 $g_o$ 的平方律在双饱和区**不能唯一决定 $V_O$**。输出满足

$$ V_I-V_{Tn}\le V_O\le V_I+|V_{Tp}| $$

即可维持两管饱和。要真正解出 $V_O=V_{DD}/2$，须保留有限输出导纳、对称性或偏置反馈；不能只靠 $k_n=k_p$ 宣称该输出唯一。

## 0225–0226 的完整曲线如何求

对每个输入，按 cutoff、线性区、saturation 选电流式，再解 $I_n(V_I,V_O)=I_p(V_I,V_O)$：

- 低输入：NMOS 截止，输出接近 $V_{DD}$。
- 高输入：PMOS 截止，输出接近 0。
- 中间：两管导通，局部斜率由下一组的小信号式求出。

理想模型的两端 DC 电流为零；真实漏电不在此模型中。教材把完整 DC 曲线交由 SPICE 处理；本轮没有宣称平方律能还原实际工艺所有细节。

## 0223、0234：Class A 与 Class AB

PMOS 栅极固定且理想电流源近似成立时，供出电流约为偏置值。两栅极同驱动时，两管分别增加／减少供出与吸入电流：

$$
\frac{dV_O}{dt}=\frac{I_p-I_n}{C_L}.
$$

若其中一管电流远大于另一管，充电斜率才可近似 $I_p/C_L$，放电斜率大小才近似 $I_n/C_L$。不能将线性 $v_o=a_vv_i$ 外推至整个 rail-to-rail 范围。

## 条件与设计选择

| 步骤 | 条件 | 失效情况 |
|---|---|---|
| $V_M=V_{DD}/2$ | 相同阈值、匹配 $k$；对称设计选择 | mismatch |
| $W_p/L_p\simeq2W_n/L_n$ | 采本书 $K'_n/K'_p\simeq2$ | 不是跨工艺常数 |
| PMOS 电流固定 | 高输出阻抗且在饱和区 | 接近 rail |
| $i_L$ 近似单管电流 | 另一管可忽略 | 交越区 |

不用 SFG：DC 与大信号分区不适合强行使用线性信号流图。


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [0223](../../extraction/index.html#SANSEN-0223) | 61 | 62 | 61 |
| [0224](../../extraction/index.html#SANSEN-0224) | 61 | 62 | 61 |
| [0225](../../extraction/index.html#SANSEN-0225) | 62 | 63 | 61, 62 |
| [0226](../../extraction/index.html#SANSEN-0226) | 62 | 63 | 62 |
| [0227](../../extraction/index.html#SANSEN-0227) | 63 | 64 | 63 |
| [0234](../../extraction/index.html#SANSEN-0234) | 66 | 67 | 66 |
