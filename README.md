# Sansen 教材工作区

团队成员请先阅读 [协作与环境配置](TEAM_SETUP.md)。仓库用于私有协作；可直接打开已生成网页，也可配置依赖后重新建图和验证。

## 本地浏览

[打开本地案例页](output/extraction/index.html)。默认展示米勒反馈、源极跟随器高频分析、增益增强三组 SFG 案例（9 张相关幻灯片），其他 1,459 张幻灯片默认折叠。搜索仍覆盖全部内容，展开“其他幻灯片”后可浏览匹配结果。

[第二章总览](output/derivations/ch02/index.html) 同样优先展示这三组，其余 17 组推导可展开查看。原始材料、Markdown、公式与仿真数据完整保留。

当前修订仅保存在本地，按用户要求暂不发布。

## 在线网站

- [Cloudflare Pages 网站](https://sansen-study.pages.dev)
- [部署与更新说明](DEPLOYMENT.md)：`sh scripts/deploy_pages.sh`，采纯静态免费托管。

第一步的全书初步抽取已产生：

- [抽取范围、格式与限制](output/extraction/README.md)
- [离线浏览页](output/extraction/index.html)
- [完整索引 CSV](output/extraction/catalog.csv)
- [完整数据 JSONL](output/extraction/cases.jsonl)
- [完整性检查](output/extraction/verification.json)

覆盖 759 个 PDF 页、24 章、1,468 张幻灯片及对应讲解。公式 OCR 候选与已核对内容分开保存；详细数量与核对程度请看抽取说明。

## SFG 建模要求

后续 SFG 工作遵守 [Physical / Causal SFG 要求](SFG_REQUIREMENTS.md)。现有三组均按 A–F 格式记录电压／电流节点、独立物理约束及逐边来源，不再采用消元后的最少电压节点图。

## 第二章公式推导

- [网页：20 组公式推导、近似条件与来源对照](output/derivations/ch02/index.html)
- [完整 Markdown](output/derivations/ch02/full.md)
- [教材差异与待厘清](output/derivations/ch02/discrepancies.md)
- [验算范围与重建方式](output/derivations/ch02/README.md)

覆盖第二章 72 张幻灯片；只有 3 组采用 SFG。结果已同步到原抽取网页。理论数值验算针对指定小信号模型；后续的实际 Spectre 仿真见下节。

## 第二章 Spectre 仿真

- [实际仿真报告与波形](output/simulations/ch02/index.html)
- [Markdown 解释](output/simulations/ch02/report.md)
- [运行证据、容许误差与验证统计](output/simulations/ch02/verification.json)
- [gm/Id 法确定尺寸与工作点](output/simulations/ch02/gmid_selection.json)

20 组推导的代表模型完成 32 组线性 AC、7 个 MOS1 电路 AC、5 组 PZ 及 3 组瞬态检查。原始 PSF 与网表已保存；尚未使用晶圆厂 PDK。
