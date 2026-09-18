# 高频源极跟随器：二阶模型、峰化与真正的极零相消

对应：0241–0243。


[独立 Physical / Causal SFG Markdown](physical_sfg/follower.md)


## A. 选取的 SFG 节点及选择理由

漏极接交流地，衬底接源极；输入串联 Rs；保留 Cg = CGS、Cd = CGD、CL、CDS、有限 ro 和偏置支路输出电导 GB。iG 从栅极流向源极；im 注入源极；iB、iL、iDS、io 从源极流向地；测试电流 it 从外部注入输出，电压激励分析时令 it = 0。CL 与 CDS、go 与 GB 分开建模，不在边系数中预先合并。

所有量为工作点附近的小信号，电容采用零初始条件的拉普拉斯关系。按局部器件关系选择因果方向，不预先求整体传递函数，也不消元为最少节点图。

| 节点 | 类型 | 选择理由 |
|---|---|---|
| $v_i$（`vi`） | 电压 / V | 独立输入电压。 |
| $i_t$（`it`） | 电流 / A | 独立输出测试电流；可设为零，保留电流输入端口。 |
| $v_g$（`vg`） | 电压 / V | 实际栅极电压。 |
| $v_{gs}$（`vgs`） | 电压 / V | 跨导源与 Cg 共用的端电压。 |
| $i_m$（`im`） | 电流 / A | MOS 跨导源注入输出的电流。 |
| $i_G$（`iG`） | 电流 / A | Cg 从栅极到源极的电流。 |
| $i_D$（`iD`） | 电流 / A | Cd 从栅极到交流地的电流。 |
| $i_R$（`iR`） | 电流 / A | 输入电阻电流。 |
| $v_R$（`vR`） | 电压 / V | 输入电阻压降。 |
| $i_B$（`iB`） | 电流 / A | 偏置支路有限电导引起的输出电流。 |
| $i_L$（`iL`） | 电流 / A | 负载电容 CL 电流。 |
| $i_{DS}$（`iDS`） | 电流 / A | 器件 CDS 电流。 |
| $i_o$（`io`） | 电流 / A | 输出电阻 ro 电流。 |
| $v_o$（`vo`） | 电压 / V | 源极输出电压。 |

## B. 独立约束

每行是一个独立局部约束，整理为 $y=\sum_k a_kx_k$。右侧的每一项生成一条边；一行分成多条边不等于重复使用约束。

| 约束 | 物理来源 | 定向方程 |
|---|---|---|
| F1 | 栅源端电压定义（KVL） | $v_{gs} = v_g - v_o$ |
| F2 | MOS 跨导源的本构关系 | $i_m = g_m v_{gs}$ |
| F3 | Cg 的本构关系 | $i_G = s C_{GS} v_{gs}$ |
| F4 | Cd 的本构关系 | $i_D = s C_{GD} v_g$ |
| F5 | 栅极 KCL | $i_R = i_G + i_D$ |
| F6 | Rs 的本构关系 | $v_R = R_S i_R$ |
| F7 | 输入串联支路 KVL | $v_g = v_i - v_R$ |
| F8 | 偏置支路 GB 的本构关系 | $i_B = G_B v_o$ |
| F9 | CL 的本构关系 | $i_L = s C_L v_o$ |
| F10 | CDS 的本构关系 | $i_{DS} = s C_{DS} v_o$ |
| F11 | 源极输出节点 KCL | $i_o = i_m + i_G + i_t - i_B - i_L - i_{DS}$ |
| F12 | ro 的本构关系 | $v_o = r_o i_o$ |

电阻只使用 $v=Ri$ 这一方向，不再同时添加 $i=v/R$；同一电容的支路电流可以出现在两端节点的 KCL 中，但其本构关系只建一次。
本图保留有限输出电阻以采用“电流 → 电压”的电阻方向。若另取输出电导严格为零的理想模型，应重新分配约束方向，不能直接在图上使用无穷大的电阻。

## C. SFG edge list

```text
E01: vg --(1)--> vgs    [F1]
E02: vo --(-1)--> vgs    [F1]
E03: vgs --(gm)--> im    [F2]
E04: vgs --(s*Cg)--> iG    [F3]
E05: vg --(s*Cd)--> iD    [F4]
E06: iG --(1)--> iR    [F5]
E07: iD --(1)--> iR    [F5]
E08: iR --(Rs)--> vR    [F6]
E09: vi --(1)--> vg    [F7]
E10: vR --(-1)--> vg    [F7]
E11: vo --(GB)--> iB    [F8]
E12: vo --(s*CL)--> iL    [F9]
E13: vo --(s*CDS)--> iDS    [F10]
E14: im --(1)--> io    [F11]
E15: iG --(1)--> io    [F11]
E16: it --(1)--> io    [F11]
E17: iB --(-1)--> io    [F11]
E18: iL --(-1)--> io    [F11]
E19: iDS --(-1)--> io    [F11]
E20: io --(ro)--> vo    [F12]
```

## D. ASCII SFG

以下按目标节点分组绘制，重复出现的变量名指同一个节点；所有连接均列出。V 为电压节点，A 为电流节点。

```text
vg --(1)---+
           |
vo --(-1)--+--> vgs [V]  (F1)

vgs --(gm)--> im [A]  (F2)

vgs --(s*Cg)--> iG [A]  (F3)

vg --(s*Cd)--> iD [A]  (F4)

iG --(1)--+
          |
iD --(1)--+--> iR [A]  (F5)

iR --(Rs)--> vR [V]  (F6)

vi --(1)---+
           |
vR --(-1)--+--> vg [V]  (F7)

vo --(GB)--> iB [A]  (F8)

vo --(s*CL)--> iL [A]  (F9)

vo --(s*CDS)--> iDS [A]  (F10)

im --(1)----+
            |
iG --(1)----+
            |
it --(1)----+
            |
iB --(-1)---+
            |
iL --(-1)---+
            |
iDS --(-1)--+--> io [A]  (F11)

io --(ro)--> vo [V]  (F12)

```

![高频源极跟随器的 Physical / Causal SFG](assets/follower-sfg.svg)

图中椭圆为电压节点，圆角矩形为电流节点，双边框为独立输入。每条边显示系数和约束编号；按图中箭头读取方向。

[打开 SVG 矢量图](assets/follower-sfg.svg) · [DOT 连接文本](assets/follower-sfg.dot) · [机器可读边表](physical_sfg/follower-edges.json)

## E. 主要正向通路与反馈环路

- 跨导正向通路：vi → vg → vgs → im → io → vo；并行的 Cg 前馈通路为 vgs → iG → io → vo。
- 主要局部负反馈：vo → vgs → im → io → vo，输出在 vgs 的端电压定义中取负号。
- 栅极电流反馈：vg → vgs → iG → iR → vR → vg；Cd 也通过 iD → iR 影响输入压降。输出的 GB、CL、CDS 各自形成 vo → 支路电流 → io → vo 的负号返回路径。
- it → io → vo 明确保留输出测试电流的物理端口，测试时将 vi 设为零即可；无需先求整体传递函数或另造反向器件约束。

## F. 逐边对应独立约束检查

| 边 | 起点 → 终点 | 系数 | 唯一来源约束 |
|---|---|---|---|
| E01 | $v_g\to v_{gs}$ | $1$ | F1：栅源端电压定义（KVL） |
| E02 | $v_o\to v_{gs}$ | $-1$ | F1：栅源端电压定义（KVL） |
| E03 | $v_{gs}\to i_m$ | $g_m$ | F2：MOS 跨导源的本构关系 |
| E04 | $v_{gs}\to i_G$ | $s C_{GS}$ | F3：Cg 的本构关系 |
| E05 | $v_g\to i_D$ | $s C_{GD}$ | F4：Cd 的本构关系 |
| E06 | $i_G\to i_R$ | $1$ | F5：栅极 KCL |
| E07 | $i_D\to i_R$ | $1$ | F5：栅极 KCL |
| E08 | $i_R\to v_R$ | $R_S$ | F6：Rs 的本构关系 |
| E09 | $v_i\to v_g$ | $1$ | F7：输入串联支路 KVL |
| E10 | $v_R\to v_g$ | $-1$ | F7：输入串联支路 KVL |
| E11 | $v_o\to i_B$ | $G_B$ | F8：偏置支路 GB 的本构关系 |
| E12 | $v_o\to i_L$ | $s C_L$ | F9：CL 的本构关系 |
| E13 | $v_o\to i_{DS}$ | $s C_{DS}$ | F10：CDS 的本构关系 |
| E14 | $i_m\to i_o$ | $1$ | F11：源极输出节点 KCL |
| E15 | $i_G\to i_o$ | $1$ | F11：源极输出节点 KCL |
| E16 | $i_t\to i_o$ | $1$ | F11：源极输出节点 KCL |
| E17 | $i_B\to i_o$ | $-1$ | F11：源极输出节点 KCL |
| E18 | $i_L\to i_o$ | $-1$ | F11：源极输出节点 KCL |
| E19 | $i_{DS}\to i_o$ | $-1$ | F11：源极输出节点 KCL |
| E20 | $i_o\to v_o$ | $r_o$ | F12：ro 的本构关系 |

共 14 个节点、12 个独立约束、20 条边。每个非输入节点只有一个定义方程；每条边属于唯一约束。边系数仅含单个器件的本构参数（包括理想受控源的常数增益）、电容导纳或带符号的 1。

本节输出止于 Physical / Causal SFG，不进一步化为 algebraic SFG。


<details>
<summary>原有公式推导与必要近似（展开查看）</summary>

## 电路与符号

漏极为 AC 地，衬底跟源极相连；$R_S$ 串在信号源和栅极间。定义

$$
C_g=C_{GS},\quad C_d=C_{GD},\quad C_0=C_L+C_{DS},\quad
g=g_o+G_B,\quad G_S=1/R_S.
$$

$C_g$ 跨栅极–源极；$C_d$ 因漏极接地，成为栅极对地电容。输出是源极，不能套用共源级米勒增益。

## 完整二节点方程

$$
[G_S+s(C_d+C_g)]v_g-sC_gv_o=G_Sv_i,
$$

$$
-(g_m+sC_g)v_g+[g_m+g+s(C_g+C_0)]v_o=0.
$$

令

$$
C_2=C_0C_d+C_0C_g+C_dC_g,
$$

$$
D(s)=g_m+g+s[C_g+C_0+R_Sg_mC_d+R_Sg(C_d+C_g)]
+s^2R_SC_2.
$$

则

$$
H(s)=\frac{v_o}{v_i}=\frac{g_m+sC_g}{D(s)},\qquad
Z_o(s)=\left.\frac{v_o}{i_{\rm test}}\right|_{v_i=0}
=\frac{1+sR_S(C_d+C_g)}{D(s)}.
$$

这两个传输共用同一分母，但分子不同，所以零点不同。

## 0241：化成教材形式

令 $g=0$，除以 $g_m$：

$$
H=\frac{1+sC_g/g_m}{1+sB+s^2R_SC_2/g_m},\quad
B=R_SC_d+\frac{C_g+C_0}{g_m}.
$$

教材另外保留 $R_SC_g/(g_mr_o)$，却省去常数 $1/(g_mr_o)$ 与
$R_SC_d/(g_mr_o)$。这是选择性的一阶修正；若需要有限 $r_o$ 的一致模型，应使用上面的完整 $D(s)$。

电压零点为 $s_{zv}=-g_m/C_g$（左半平面）。若令分母 $a_0+a_1s+a_2s^2$，则

$$
s_{p1,p2}=\frac{-a_1\pm\sqrt{a_1^2-4a_0a_2}}{2a_2}.
$$

复极点条件是 $a_1^2<4a_0a_2$。**复极点不必然造成可见的增益峰值**：零点及阻尼还会影响幅度，需要实际计算 $|H(j\omega)|$。

## 0242：复极点区域的精确边界

以下令 $g=0$，并在扫描 $g_m$ 时先把电容视为固定。设

$$
B_c=C_g+C_0,\quad
r=\frac{C_0C_g}{C_d(C_0+C_g)},\quad k=1+r,\quad
g_{mr}=\frac{B_c}{R_SC_d},\quad x=\frac{g_m}{g_{mr}}.
$$

将判别式除以 $B_c^2$：

$$
(x+1)^2-4kx<0.
$$

因此真正的边界为

$$
x_\pm=(\sqrt{k}\pm\sqrt{k-1})^2,\qquad
g_{m,\pm}=g_{mr}x_\pm,\qquad x_+x_-=1.
$$

教材的 $g_{mr}$ 正是两个边界的几何中心。但若把「宽度」定义成上下界比，

$$
W_g=\frac{g_{m,+}}{g_{m,-}}
=(\sqrt{k}+\sqrt{k-1})^4,
$$

就不是幻灯片列的 $\Delta g_{mr}=C_{DGt}/C_{DG}=r$。
原图的 $C_{DGt}=C_0C_g/(C_0+C_g)$ 可视为一个电容比参数，但不能不加定义地当作精确区域宽度，再套 $g_{mr}/\sqrt{\Delta g_{mr}}$ 求下界。

## 将零点代入分母：不能只看渐近线交叉

电压零点 $s=-g_m/C_g$ 代入：

$$
D(-g_m/C_g)=
\frac{C_0g_m}{C_g^2}
[R_Sg_m(C_d+C_g)-C_g].
$$

除去退化情况，精确相消条件是

$$
g_{m,\rm cancel}=\frac{C_g}{R_S(C_d+C_g)}
\simeq\frac1{R_S}\quad(C_d\ll C_g).
$$

这说明 0242 的 $1/R_S$ 是近似而非一般精确相消点。

输出阻抗零点是

$$
s_{zo}=-\frac1{R_S(C_d+C_g)}
\simeq-\frac1{R_SC_g}.
$$

把它代入同一分母得到**相同的精确相消条件**。在该点：

$$
Z_o(s)=\frac1{g_m+s[C_0+C_gC_d/(C_g+C_d)]},
$$

$$
H(s)=\frac{g_m}{g_m+s[C_0+C_gC_d/(C_g+C_d)]}.
$$

0243 的
$g_{mu}\simeq(C_g+C_{DS})/[R_S(C_g+C_d)]$
是把近似极点与零点位置对齐的估计；它只有在 $C_{DS}\ll C_g$ 等条件下接近上面的精确相消值。保留任意 $C_{DS}$ 时，代入完整分母不会得到零。

高 $g_m$ 时，一个极点趋向 $-1/(R_SC_d)$，因此可得到图中的
$f_{d,\rm high\,gm}\simeq1/(2\pi R_SC_d)$。输出阻抗先升后降的区段可呈感性。


## 近似与验算

| 原式 → 简式 | 条件 | 失效情况 |
|---|---|---|
| $g\to0$ | 不只 $g\ll g_m$，还须 $R_Sg(C_d+C_g)$ 对 $a_1$ 足够小 | 大 $R_S$ |
| $C_d+C_g\to C_g$ | $C_d\ll C_g$ | 补偿电容加大后 |
| $g_{m,\rm cancel}\to1/R_S$ | 同上 | 0242 的补偿恰好会改变此比值 |
| 极点渐近交点 → 精确相消 | 必须另外验 $D(s_z)=0$ | 复极点或电容比不小 |
| 固定电容扫 $g_m$ | 局部模型比较 | 真实偏置变动也改变电容 |

![峰化与精确相消比较](assets/follower-comparison.svg)

图中标出完整模型相消值与教材估计值。符号程序验证两个零点代入结果及相消后的一阶式。

例图固定 $R_S=10$ kΩ、$C_g=1$ pF、$C_d=0.2$ pF、$C_{DS}=3$ pF、$C_L=0$、$g=0$。完整相消值为 $83.33$ µS，0243 估式为 $333.33$ µS，复极点区域的几何中心为 $2$ mS。这是固定电容的模型比较，不是扫描真实器件偏置。

</details>


## 来源对照

| 幻灯片 | PDF 页 | 书本页 | 讲解所在 PDF 页 |
|---|---:|---:|---|
| [0241](../../extraction/index.html#SANSEN-0241) | 70 | 71 | 70 |
| [0242](../../extraction/index.html#SANSEN-0242) | 71 | 72 | 70, 71 |
| [0243](../../extraction/index.html#SANSEN-0243) | 71 | 72 | 71 |
