# 第二章公式推导

[打开第二章网页](index.html) · [完整 Markdown](full.md) · [教材差异表](discrepancies.html) · [全书抽取数据库](../../extraction/index.html)

## 本轮成果

- 对照 021–0272 共 72 张幻灯片原图及正文；66 张技术内容合并为 20 组推导，6 张章节脉络页另外注明。
- 每组包括连接与模型、KCL／微分／矩阵、完整式、必要近似、成立条件、失效范围及教材结论对照。
- 只在米勒、高频源极跟随器、增益增强三组使用 SFG。三组均为 Physical / Causal SFG，含 A–F 六部分、电压／电流节点和逐边约束编号。独立物理约束保存在 `physical_sfg/models.json`，经 DOT 自动排版为 SVG。
- 新推导与来源差异注记优先于第一步的 OCR 候选及早期代表案例摘录。后者保留为来源记录。
- 13 项教材符号、近似或模型差异集中于 `discrepancies.json`；0244 的部分 BJT 高频模型／符号仍待厘清，没有宣称所有教材原式都已证明。

## 验算与实际限制

[verification.json](verification.json) 记录 48 项符号一致性检查及 4 组模型各 30 次随机复数频率节点解；皆通过。数值节点解最大相对差异约 1.69×10⁻¹³。

符号验算确认明列等效电路内的代数一致性；这份 verification.json 本身不代表 PDK、SPICE 或实验验证。后续已完成独立的 [Spectre 仿真阶段](../../simulations/ch02/index.html)，请依该报告查看实际运行结果。图中数值为可重建的指定模型案例。共同假设如小信号、固定电容、忽略体效应等必须连同各组局部条件一起使用。

[physical_sfg_verification.json](physical_sfg_verification.json) 另记录三组物理图的约束、量纲及 120 次端口数值对照。图的构建不使用整体传递函数；原有理论推导折叠保留。

[render_verification.json](render_verification.json) 记录 Markdown／TeX 编译；[site_verification.json](site_verification.json) 记录覆盖、资源链接、内嵌数据与 JavaScript 语法检查。三张 SFG 和三张曲线已作图像核对。未运行浏览器交互或版面测试。

## 文档结构

| 文档 | 用途 |
|---|---|
| `index.html` | 20 组导览与逐张对照 |
| `00-conventions.html` | 全章符号、模型与 SFG 原则 |
| `01-*.html` 至 `20-*.html` | 排版公式与 Markdown 解释 |
| 同名 `.md` / `full.md` | 单组／全章可编辑文本 |
| `coverage.json` / `case_map.json` | 72 张幻灯片与推导位置的映射 |
| `modules.json` | 模块、来源页码与 SFG 选用 |
| `discrepancies.json` | 来源差异的类型、说明及处理状态 |
| `assets/*-sfg.dot` / `.svg` | SFG 文本源档与自动排版图 |
| `assets/*-comparison.svg` | 三组科学数值图 |

## 重建

以下指令皆从工作区根目录运行。生成网页是本地静态文件，无外部 CDN、API 或数据上传。修改推导请改 `derivations/ch02/*.md`，不要只改输出副本。

Python 验算使用 `sympy==1.14.0`，另需 numpy 与 matplotlib；抽取目录重建另需 Pillow。已使用的套件版本见 `scripts/ch02-python-versions.json`，JavaScript 锁定依赖见 `scripts/ch02-web-deps/package-lock.json`。

```sh
mkdir -p tmp/ch02/web-deps
cp scripts/ch02-web-deps/package*.json tmp/ch02/web-deps/
npm ci --prefix tmp/ch02/web-deps --ignore-scripts
python3 -m pip install --target tmp/ch02/python-deps sympy==1.14.0
python3 scripts/build_physical_sfg.py
node scripts/render_ch02_sfg.mjs
python3 scripts/verify_ch02.py
python3 scripts/prepare_ch02.py
node scripts/build_ch02.mjs
python3 scripts/build_catalog.py
python3 scripts/verify_ch02_site.py
python3 scripts/verify_extraction.py
```

若系统 Python 缺少 numpy、matplotlib 或 Pillow，先按记录版本装到所用环境。原始 PDF 与第一步抽取结果必须保留，来源图与教材正文的链接才可使用。
