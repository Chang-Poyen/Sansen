# Sansen 教材抽取结果

## 开始浏览

- [离线浏览页](index.html)：用浏览器打开，可搜索幻灯片编号、英文主题与正文，并依章节、图形、反馈与核对状态筛选。
- [CSV 索引](catalog.csv)：适合用试算表快速筛选。
- [完整 JSON](catalog.json)／[逐笔 JSONL](cases.jsonl)：供后续程序处理。
- [统计](statistics.json)／[完整性检查](verification.json)。

## 本次完成的范围

已对用户提供的 `Analog Design Essentials (Willy Sansen).pdf` 全部 **759 个 PDF 页面、24 章、1,468 张幻灯片**完成初步抽取。

| 层级 | 完成内容 | 核对程度 |
|---|---|---|
| 原始数据 | 1,468 张原生幻灯片图片，没有重新压缩；759 页正文文本 | 图片数量、编号连续性、页码及引用完整性已检查 |
| 讲解配对 | 每张幻灯片与对应正文合并；274 笔讲解跨页 | 依编号字体、位置及顺序配对；代表跨页案例已检查 |
| 图中文本 | 1,468 张图片均有本地 Vision OCR 结果、行座标与信心值 | 未将信心值视为数学正确性 |
| 公式 | 3,464 个含等号／关系符号的 OCR 候选及周边裁切 | 不是 3,464 个已确认完整公式；可能有重复、误收与漏收 |
| 结论与条件 | 分别截取正文中的性能结论、图形说明、连接叙述、条件与近似句子 | 规则产生的原文摘录；未逐张完成语义核对 |
| 代表案例 | 12 笔加入中文解读、部分公式 LaTeX、曲线结论、连接关系与近似注记 | 只核对各笔明列的内容，不代表同页所有细节皆已核对 |
| 独立图区 | 13 个代表案例中的电路、波特图或方块图裁切区 | 人工定位；全书其他图仍完整保留在幻灯片原图内 |
| 后续候选 | 366 笔含电路及反馈关键词的 SFG 待评估记录 | 只是筛选入口，不是适合 SFG 的最终判定 |

**全书初步抽取已完成；全书逐公式语义校正、逐器件连接还原尚未完成。** 本次没有进行新公式推导、SFG 建模、晶体管尺寸设计或 SPICE 仿真。

## 原始 PDF 的版面特性

这个文件已把幻灯片与教材讲解排在一起，因此以幻灯片编号作为主键，不把一个 PDF 页面当作一个案例。有些编号在前页底部，图片在次页顶部；同一段讲解也可能跨页。

其中 7 张参考文献幻灯片（1170、1171、1249、1250、1251、2253、2254）原页没有另附正文讲解；已视觉核对并标为 `absent_in_source_verified_reference_slide`，不是抽取漏失。

数据同时保留：

- `slide_id`：原幻灯片编号，如 `027` 表示第 2 章第 7 张，`0210` 表示第 2 章第 10 张。必须当作字符串。
- `source.pdf_page`：幻灯片编号出现的 PDF 页。
- `slide_images[].pdf_page`：图片实际出现的 PDF 页。
- `printed_page`：印在书上的页码；章节首页从页脚读取，其余页面从页眉读取。
- `commentary_segments[]`：逐段讲解的 PDF 页、书本页、截取范围与原始文本。

供应的 PDF 页码连续为 1–759，印刷页码则到 771，中间跳过 **50、88、116、148、210、238、262、388、456、484、566、710**。这是来源档本身的页码串行，未据此推断缺少正文，也没有补造页面。

## 已核对的案例

- [025：单管增益的尺寸与偏置取舍](cases/SANSEN-025.md)
- [027：负载电容、增益与带宽](cases/SANSEN-027.md)／[028：对应波特图](cases/SANSEN-028.md)
- [0210：输入电容限制带宽](cases/SANSEN-0210.md)
- [0211：反馈电容限制带宽](cases/SANSEN-0211.md)／[0212：米勒等效](cases/SANSEN-0212.md)
- [0242：源极跟随器峰化](cases/SANSEN-0242.md)／[0243：输出阻抗](cases/SANSEN-0243.md)
- [0244：射极跟随器输出阻抗](cases/SANSEN-0244.md)
- [0512：有限衰减的低通](cases/SANSEN-0512.md)
- [0513：增益与带宽的交换](cases/SANSEN-0513.md)
- [0514：开环／闭环与近似条件](cases/SANSEN-0514.md)

例：0212 列出 `C_FM=(1+A_v0)C_F`，0211 的带宽式却使用 `A_v0 C_F`。数据已把省略 1 所需的大增益近似记为跨页核对注记。027 与 028 也注明，幻灯片使用的是正值增益大小与相对相位，不能直接当作包含共源反相的有号增益。

## 如何使用机器数据

每笔完整记录在 `cases/SANSEN-<slide_id>.json`，阅读版在同名 `.md`。

| 字段 | 用途 |
|---|---|
| `slide_images` | 原生图片、尺寸与 PDF 座标 |
| `commentary_segments` / `commentary_text` | 对应讲解；前者保留逐段来源 |
| `ocr.lines` | 未校正的图中文本、信心值与框线 |
| `formula_candidates` | 公式候选、周边裁切与来源；未核对的 `latex` 固定为 null |
| `circuit.connection_description_excerpts` | 正文中的器件与连接关系叙述；不是网表 |
| `analysis_objective_excerpts` | 分析目标的原文候选 |
| `source_conclusions` / `graph_conclusion_excerpts` | 公式／性能／曲线结论的原文候选 |
| `explicit_assumption_excerpts` | 原文明示条件与近似的候选句子 |
| `reviewed_extraction` | 12 个案例的已核对内容，含 `review_scope` 限定范围 |
| `verified_visual_regions` | 人工定位的独立图区；不代表已核对网表 |
| `sfg_triage` | 关键词初筛结果 |

PDF 座标以左上为原点，单位为 point。OCR 及代表图区座标为左上原点的 0–1 范式 `[x0,y0,x1,y1]`。所有页码从 1 起算。

`*_excerpts` 是直接摘录，不是模型推导；正文文本层本身会把 Ω、μ、上下标与特殊字符提取错误。不要只凭文本层把 `50 V` 或 `1 MV` 当成已核对单位。电路、公式及图形的原始幻灯片始终是核对依据。

没有找到公式或图形候选，不表示页面没有公式或图形。`unreviewed`、`not_netlist_verified`、`latex: null` 都是刻意保留的状态，避免后续程序误用。

## 重跑

脚本在工作区 `scripts/`：

1. `extract_book.py`：抽取原图、页面文本、编号及跨页讲解。
2. `ocr_slides.swift`：使用 macOS Vision 在本地运行 OCR；已有输出时可续跑。
3. `build_catalog.py`：产生 JSON、JSONL、CSV、Markdown、候选裁切与离线浏览页。
4. `reviewed_cases.json`：可持续扩充的核对数据，不会被抽取覆盖。
5. `verify_extraction.py`：验证覆盖率、编号、来源哈希、资源引用及跨页回归案例。

在工作区根目录，以具备 `pdfplumber`、`pypdf`、`Pillow` 的 Python 运行：

```sh
python3 scripts/extract_book.py 'Analog Design Essentials (Willy Sansen).pdf'
swiftc -O scripts/ocr_slides.swift -o tmp/pdfs/ocr_slides
tmp/pdfs/ocr_slides output/extraction
python3 scripts/build_catalog.py
python3 scripts/verify_extraction.py
```

本次使用 Codex bundled Python 与系统 macOS Vision，没有把书或幻灯片上传到外部 OCR 服务。来源 PDF 未修改，SHA-256 保存在 `manifest.json`。

## 检查与限制

已检查全数编号、原图、OCR 记录、来源页码及文件引用，并视觉检查代表幻灯片、公式和独立裁切。浏览器安全政策阻止本地 `file://` 页面的自动预览；没有绕过限制，因此离线接口的交互及浏览器版面尚未完成自动验证。可以自行用浏览器打开 `index.html`，或直接阅读 Markdown / JSON。

要达成全书可直接进入自动推导的数据品质，后续还需要逐张核对公式、补齐具体器件节点、交叉引用前页模型，以及确认曲线结论的适用条件。本输出保留了完成这些核对所需的原图与来源。
