# 有源电感、频率范围与差分两倍因子

对应：0245–0247。

## 0245：从输出测试电流解阻抗

测量源极输出阻抗时，栅极经 $R_S$ 接 AC 地。只保留 $C_{GS}=C$、$g_m$，暂时移除外置 $C_L$：

$$
(G_S+sC)v_g-sCv_o=0,\qquad
i_t=(g_m+sC)(v_o-v_g).
$$

先解 $v_g=sR_SCv_o/(1+sR_SC)$，代入：

$$
Z_o=\frac{1+sR_SC}{g_m+sC}.
$$

低频与高频极限为

$$ Z_o(0)=1/g_m,\qquad Z_o(\infty)=R_S. $$

以 $\omega_T=g_m/C$，精确重写：

$$
Z_o=\frac1{g_m}+
\frac{sL_{\rm eff}}{1+s/\omega_T},\qquad
L_{\rm eff}=\frac{R_S-1/g_m}{\omega_T}.
$$

在 $\omega\ll\omega_T$ 且 $g_mR_S\gg1$ 时，

$$ Z_o\simeq\frac1{g_m}+sL,\qquad L\simeq R_S/\omega_T=R_S/(2\pi f_T). $$

感性项显著的频带约为

$$ \frac{\omega_T}{g_mR_S}\ll\omega\ll\omega_T. $$

因此教材「up to $f_T$」应理解为尺度上限，并非在 $f_T$ 处仍能无误差使用纯电感近似。$R_S$ 是高频平台，不是低频串联电阻；低频串联电阻是 $1/g_m$。

若原图保留外置 $C_L$，总阻抗还要取

$$ Z_{\rm loaded}=[Z_o^{-1}+sC_L]^{-1}. $$

不能一面保留 $C_L$，一面宣称上面的无负载 $Z_o$ 是总阻抗。

## 0246：用 MOS 电阻代替 $R_S$

二极管连接 PMOS 若为 AC 地参考且 $g_{mp}\gg g_{op}$，其电阻约为 $1/g_{mp}$：

$$ L\simeq\frac1{g_{mp}\omega_{Tn}}. $$

采右侧低压配置时，源极跟随器的近单位跟随使 PMOS 的栅极/漏极小信号近似短接，才可沿用相同电阻。这要求中间跟随增益接近 1、内部极点高于使用频带；不能在任意频率把复合反馈支路当成理想电阻。

依图上的 DC 节点电压：

- 电阻反馈的基本配置：$V_{DSn}=V_{GSn}$。
- 中间 PMOS 二极管配置：$V_{DSn}=V_{GSn}+V_{SGp}$。
- 右侧低压配置：$V_{DSn}=V_{SGp}$。

以上 PMOS 电压使用正值 $V_{SGp}$，避免原图 $V_{GSp}$ 的符号混用。

## 0247：差分半电路

左右匹配，tail 电流源对差模形成虚地；每边的上管阻抗近似

$$ Z_h\simeq r_h+sL_h,\quad r_h=1/g_{m2},\quad L_h=R_{\rm tune}/\omega_{T2}. $$

两个 output 之间量到的阻抗是 **$2Z_h$**。所以若图右画的是跨两端的实体等效电感，其值为

$$ L_{\rm diff}=2L_h=\frac{2R_{\rm tune}}{\omega_{T2}}. $$

教材标 $L=R_{\rm tune}/\omega_{T2}$ 可当半电路电感，但不能同时把它当完整两端差分电感，否则差一倍。

跨输出的电容 $C$ 在半电路等效为 $2C$，因而

$$
a_{vd}(s)\simeq\frac{g_{m1}(r_h+sL_h)}
{1+2sCr_h+2s^2CL_h}.
$$

低频 $|a_{vd}(0)|=g_{m1}/g_{m2}$，重现教材；无阻尼共振尺度则为
$\omega_0=1/\sqrt{2L_hC}$。峰化由二阶分母及一个零点共同决定。

## 近似与验算

| 近似 | 条件 | 失效情况 |
|---|---|---|
| $Z_o$ 忽略其他寄生 | $g_o,C_{GD},C_{DS}$、负载效应小 | 真实高频 |
| $L_{\rm eff}\to R_S/\omega_T$ | $g_mR_S\gg1$ | $g_mR_S\le1$ 不呈此感性 |
| $1/(1+s/\omega_T)\to1$ | $\omega\ll\omega_T$ | 接近截止 |
| PMOS $\to1/g_{mp}$ | $g_{mp}r_{op}\gg1$，频率远低于其极点 | 电阻也变成频率函数 |
| 差分半电路 | 左右匹配、纯差模 | 共模、mismatch |

不用额外 SFG：从上一组二节点模型直接取极限即可。$L$ 的系数及差分阻抗因子在符号与数值检查中分开验证。
