# 第二章 Spectre 仿真

[仿真网页](index.html) · [Markdown 报告](report.md) · [运行与验证索引](verification.json)

## 已运行的范围

20 组推导的代表模型：32 组显式小信号组件 AC、7 个 MOS1 电路 AC、5 组独立 PZ、3 个瞬态情境，共 47 项检查。每组的实际案例见 [module_summary.json](module_summary.json)。这不等同于逐张搭建第二章全部电路。

使用已安装的 virtuoso-bridge-lite 0.8.0，原代码 commit `74649fbc28af14f1a6853ae8586b43cdba3747a1`；通过独立 Spectre runner 运行，没有启动或修改 Virtuoso GUI 的设计。实际 Spectre 版本为 18.1.0.077。

## 教学模型的定义

本轮没有指定 PDK，使用可追溯的 MOS1：

- NMOS、PMOS 的 |VTO|=0.45 V，KP=100 µA/V²，lambda=0.1 V⁻¹。
- gamma=0、tox=10 nm；显式 交叠电容／junction 电容设零，MOS1 的本征 Cgs 仍保留。
- L=2 µm，查表 W=20 µm；VOV 扫描 0.05–0.60 V、步长 5 mV。
- 先取仿真的 gm/Id=10 V⁻¹，再由 Id/W 选 W=171.360 µm，使 VDS=1 V 时 gm=1.88496 mS、Id=188.496 µA。
- PMOS 的 gm/Id 采 gm/|Id|；饱和条件采 |Vds|>|Vdsat|。

模型档包含在各完整网表中。BJT 目前是显式 混合 π 型 等效电路，没有使用 foundry BJT 模型。原仓库提供 Spectre／网表 skill，本次在其 runner 上实现测量 gm/Id 的查表流程。

## 三种误差分开记录

1. **完整模型 vs Spectre**：AC 复数传输、相位与符号一起比较，逐点相对误差上限 2e-5。
2. **教材近似 vs Spectre**：另外报告偏差，不把近似失效算成完整模型验证失败。
3. **瞬态 vs 完整理论**：积分输入的 1 ns 上升沿后比较，归一化输出最大绝对误差上限 2e-5。

PZ 原始输出单位为 Hz；代数 s 平面根除以 2π 后比较，容许相对误差 2e-5。使用 `docancel=no` 保留重合的 pole／zero。PZ 的 `dcGain` 字段未用来决定传输正负号；正负号由 AC 复数波形核对。

MOS 的 AC 参考使用实际 DC 工作点 gm、gds、Cgs。七个电路共十颗 MOS 都通过 `region=2` 及正的饱和裕量检查。这证明所列 MOS1 模型内的小信号一致性，没有验证真实工艺、大信号失真、PVT 或版图。

## 原始数据

- `netlists/`：实际运行的 `.scs` 副本，带清楚节点与引脚顺序。
- `runs/<deck>/result.json`：命令、exit code、原始网表 SHA-256、下载路径及运行时间。
- `runs/<deck>/spectre.out`：原始 Spectre 日志。
- `runs/<deck>/*.raw/`：未修改的 PSF ASCII。
- `csv/`：逐点仿真、理论与误差，或 gm/Id 查表。
- `assets/`：可缩放的 SVG 科学图。
- `*_results.json`：每个案例的条件、误差与结果。

初始 `smoke` 是连接与受控源方向探针，其输出为 +100；正式线性套件已按此测试确认 VCCS 端子方向，CS 输出为 −100。`smoke` 没有计入 47 项验证。

所有正式数据已下载到本地持久工作区。远程 `/tmp` 仅运行暂存，日后消失不影响现有网表与波形。

## 重建流程

从 Sansen 工作区根目录运行。先按根目录 TEAM_SETUP.md 创建并激活项目虚拟环境，安装 requirements-spectre.txt：

```sh
python3 scripts/generate_ch02_sims.py
python scripts/run_ch02_spectre.py linear_suite gmid_characterization doublet_transient
python scripts/analyze_ch02_linear.py
python scripts/design_ch02_mos.py
python scripts/run_ch02_spectre.py mos_validation pz_miller pz_follower_cancel pz_follower_center pz_two_stage pz_gainboost_slow
python scripts/analyze_ch02_mos.py
python scripts/analyze_ch02_pz.py
python scripts/report_ch02_sim.py
node scripts/build_ch02_sim.mjs
python3 scripts/prepare_ch02.py
node scripts/build_ch02.mjs
python3 scripts/build_catalog.py
python3 scripts/verify_ch02_sim_artifacts.py
python3 scripts/verify_ch02_site.py
python3 scripts/verify_extraction.py
```

连接设置为工作区内的 `simulations/ch02/bridge.env`，沿用既有 SSH 认证；各成员分别填写配置，不共享登录凭证。SSH 网络权限及 Spectre license 必须可用。重新运行同名 deck 会更新本地该 run 目录，若需保留多次完整实验，先拷贝或版本化 `output/simulations/ch02/runs`。

网页为本地静态文档，含 Markdown 解释与排版公式。图像与资源完成静态检查，没有运行浏览器交互测试。
