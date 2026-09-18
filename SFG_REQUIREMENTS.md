# Physical / Causal SFG 工作要求

用户于 2026-09-16 明确指定。本要求替代之前将 SFG 化成最少电压节点的做法。

1. 从给定小信号电路的局部物理约束出发，不先求整体传递函数，不默认所有节点都是电压。
2. 先列 MOS、电容、电阻／阻抗、电导及 KCL／KVL 等独立约束。同一独立约束只使用一次，不得将一个方程及其反解同时当作两条独立反馈关系。
3. 自动选择自然的电压、电流中间变量。优先保持边系数为单个器件的本构参数，例如 gm、go、R、Z、sC，避免过早使用 gm/(go+sC)、sRC/(1+sRC) 等多器件组合系数。
4. 优先采用器件天然方向：跨导 v → i；电容 Δv → i；电阻／阻抗 i → v；电导 v → i。给定电路中的理想受控源按其本构关系定向，并注明其常数参数与适用范围。
5. 每个约束写成 y = Σ ak*xk，逐项生成 xk --ak--> y，每条边保留来源约束编号。
6. 只输出 Physical / Causal SFG，不进一步压缩为最少节点的 algebraic SFG。原有整体公式推导若保留，作为独立折叠资料，不用于倒推图。

## 固定输出格式

- A. 选取的 SFG 节点及选择理由
- B. 独立约束
- C. SFG edge list
- D. ASCII SFG
- E. 简要解释主要 forward path 和 feedback loop
- F. 检查每条边对应哪个独立约束

## 本项目实现

物理约束源文件为 `derivations/ch02/physical_sfg/models.json`。`scripts/build_physical_sfg.py` 从同一份约束生成 A–F Markdown、边表和 DOT；`scripts/render_ch02_sfg.mjs` 仅负责 Graphviz 排版。

`scripts/verify_physical_sfg.py` 核对节点定义、边的单位、约束映射以及与独立节点方程的一致性。验证用的消元不生成或展示另一张 algebraic SFG。

缺失器件内部信息时，明确给定等效模型的边界，不把猜测的内部电路当作原电路。按 TEAM_SETUP.md 进行私有仓库协作；网站发布仍需用户新的明确指示。
