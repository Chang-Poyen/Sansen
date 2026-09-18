# 团队协作与环境配置

## 克隆后从哪里开始

每位成员在自己的电脑上克隆仓库，在该目录启动 Codex。先读取 `AGENTS.md`、`SFG_REQUIREMENTS.md` 和本文档；项目文件包含共同约定，对话历史不会随 Git 自动同步。

- 直接浏览：打开 `output/extraction/index.html`，无需运行 Spectre。
- Prompt 规范：`SFG_REQUIREMENTS.md`。
- 物理模型：`derivations/ch02/physical_sfg/models.json`。
- 推导源稿：`derivations/ch02/*.md`。其中 physical-sfg 标记由构建脚本展开。
- 原始仿真证据：`output/simulations/ch02/runs/`。

仓库包含教材、提取资料与离线结果，供本项目私有协作使用。不要将这个资料仓库改成公开仓库。机器依赖、SSH 配置、凭证和构建临时目录不提交。

## Python 与 JavaScript 依赖

建议使用 Python 3.12 和 Node.js 22 或更新的兼容版本。在项目根目录创建环境：

```sh
python3 -m venv .venv
```

macOS / Linux 激活方式：`source .venv/bin/activate`；Windows PowerShell：`.venv\Scripts\Activate.ps1`。

```sh
python -m pip install -r requirements-dev.txt
python -c "from pathlib import Path; import shutil; p=Path('tmp/ch02/web-deps'); p.mkdir(parents=True, exist_ok=True); [shutil.copy2(f,p/f.name) for f in Path('scripts/ch02-web-deps').glob('package*.json')]"
npm ci --prefix tmp/ch02/web-deps --ignore-scripts
```

SFG 的约束检查和绘制可离线完成。科学曲线需要中文字体：脚本自动检测 Noto Sans CJK、思源黑体、微软雅黑或 macOS 中文字体，也可用环境变量 `SANSEN_CJK_FONT` 指定字体文件。不要将某位成员的绝对字体路径写入脚本。

## 迭代 Prompt 与重新验证

只修改 Prompt 文件不会自动改变现有 SFG。请明确让 Agent 按新 Prompt 重新分析给定电路、修订物理约束模型，并解释变化；随后执行：

```sh
python scripts/build_physical_sfg.py
node scripts/render_ch02_sfg.mjs
python scripts/verify_ch02.py
python scripts/prepare_ch02.py
node scripts/build_ch02.mjs
python scripts/build_catalog.py
python scripts/verify_ch02_site.py
```

这组命令不连接 Spectre。检查内容包括独立约束、量纲、与独立节点方程的数值对照及网页链接。生成文件可随对应源文件一起提交，便于另一位成员直接查看。

若改了根目录的推导源稿，仿真报告中的源稿摘要会失效。只有核对新模型仍与已保存的网表对应后，才运行 `python scripts/report_ch02_sim.py` 更新来源记录，再重建仿真页面；模型本身变了则先重新仿真。不能仅为了让检查通过而刷新来源摘要。

## 连接共用 Spectre 服务器

在已激活的环境中安装固定版本的 runner：

```sh
python -m pip install -r requirements-spectre.txt
python -c "from pathlib import Path; import shutil; p=Path('simulations/ch02/bridge.env'); assert not p.exists(), 'bridge.env already exists'; shutil.copy2('simulations/ch02/bridge.env.example',p)"
```

在 `bridge.env` 中填写自己的 SSH 主机、用户名、服务器上的 Spectre 路径和唯一的 VB_CLIENT_ID，沿用各自的 SSH 密钥／配置。可用 `--env-file` 指定其他本地配置文件。该配置被 Git 忽略，不要提交。

```sh
python scripts/run_ch02_spectre.py --help
python scripts/run_ch02_spectre.py smoke
```

先用 `smoke` 检查连接、许可证和受控源方向，再按 `output/simulations/ch02/README.md` 执行完整流程。此处使用 Spectre runner，不需要打开 Virtuoso GUI。

runner 将远程任务放入带随机任务标识的独立目录。每位成员使用自己的本地克隆；不要同时让两个 Agent 写同一份本地输出目录。运行同名网表会更新该克隆的对应结果，应通过分支或另存结果保留前后对照。并发仿真仍受服务器许可证和计算资源限制。

历史 `result.json` 保留原始运行路径作为证据；解析脚本优先寻找该记录旁的 `.raw` 目录，因此克隆到不同路径后仍可读取已保存结果。若本机需要额外 bridge 兼容工具，可用 `SANSEN_BRIDGE_BIN` 指定工具目录，不再写死作者电脑路径。

## Git 协作约定

1. 各自创建分支，修改 Prompt 时说明动机和适用范围。
2. 用固定三组案例对比修改前后图；新模型应有对应的局部物理约束依据。
3. 提交 Prompt、模型／源稿、生成结果和验证记录，发起 Pull Request。
4. 另一位成员复核约束独立性、因果方向及必要近似后合并。

数值一致不能单独证明物理解释合理。Prompt 更改也不应悄悄修改验证标准来掩盖失败。

## 发布边界

本次授权将项目推送到 GitHub **私有仓库**，用于成员协作。它不包含发布或更新 Cloudflare Pages 网站的授权；网站继续仅在本地修订。
