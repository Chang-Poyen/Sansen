# Cloudflare Pages 部署

正式网站：https://sansen-study.pages.dev

## 免费方案

网页、原始幻灯片图片、公式裁切、KaTeX 字体与仿真波形都作为 Pages 静态文件托管。
没有 Pages Functions、Workers 运算、R2、Cloudflare Images 或其他付费绑定；使用免费的 `pages.dev` 网址。

- [Pages 静态资源请求免费且不限次数](https://developers.cloudflare.com/pages/functions/pricing/)
- [免费限制：20,000 个文件，单档最多 25 MiB](https://developers.cloudflare.com/pages/platform/limits/)

打包脚本会检查文件数量与大小，超出限制即停止，不会自动升级方案。
当前版本共 10,445 个文件、约 176 MiB；最新数字以 `dist/pages-verification.json` 为准。

## 更新网站

在工作区完成原有内容的重建后运行：

```sh
sh scripts/deploy_pages.sh
```

首次在另一台电脑运行时需 Node.js、npm、Python 3.9+，并先使用 Wrangler 登录 Cloudflare：

```sh
npm ci --prefix scripts/pages-deps
scripts/pages-deps/node_modules/.bin/wrangler login
sh scripts/deploy_pages.sh
```

此项目采 Wrangler Direct Upload；目前无需 GitHub。日后可将选定的原代码存入 GitHub，通过 CI 调用相同部署命令。
不要将 `simulations/ch02/bridge.env`、登录凭证或本地依赖提交到 GitHub。

## 部署范围

`scripts/build_pages.py` 将 `output/extraction`、`output/derivations`、`output/simulations` 拷贝到 `dist/pages`，保留相对路径。
根网址转到 `/extraction/`；另提供 404 页和基本回应标头。

原始 PDF 约 49 MiB，超过 Pages 单档限制，保留在本地；上线版移除其本地链接，改显示来源页码提示。
所有幻灯片原图均有上线。原有离线 HTML 不变，仍可连回本地 PDF。

打包会检查静态 HTML/CSS 链接、字体、1,468 张幻灯片、公式裁切、案例下载与推导链接。
建置中介档、SSH 设置、原始 PDF 与 node_modules 不会随此部署上传。

## 部署记录

2026-09-15 首次部署完成：[此版本](https://a445010b.sansen-study.pages.dev)。
`deployment-verification.json` 保存本次打包、HTTP 与浏览器检查结果。
正式首页、推导页、仿真页、图片、字体与 CSV 回传 200；不存在的路径回传 404。
已实际测试幻灯片搜索、原图切换、推导链接及仿真波形显示。

```sh
scripts/pages-deps/node_modules/.bin/wrangler pages deployment list --project-name sansen-study
```

Wrangler 认证保存在用户的 Cloudflare 登录设置中；项目不保存 API token。

## 2026-09-16 简体中文修订

界面、Markdown 解释、章节名称和图表说明已统一为简体中文，术语采用中国大陆模拟集成电路领域常用表达。公式、教材原始材料和已执行网表保持不变。

本地构建与验证通过，结果见 `localization-verification.json`。发布被自动审批拒绝：需用户明确授权将含仿真报告、网表和原始数据的现有静态目录上传到 `sansen-study` Cloudflare Pages 站点。因此本次修订尚未上线。

### 2026-09-16 暂缓发布记录

用户随后明确要求暂不发布，继续本地修订。前台已改为优先展示三组 SFG 案例，其他幻灯片和推导默认折叠。`output/` 与 `dist/pages/` 均为本地更新产物，本次未执行上传。

## 2026-09-18 当前发布状态

用户明确要求部署修改后的网页，本次更新已发布到原有正式站点。

- 正式网址：https://sansen-study.pages.dev
- 本次版本：https://b7d8e08f.sansen-study.pages.dev
- 内容：简体中文界面、三组 Physical / Causal SFG 的 A–F 内容；其余幻灯片和推导默认折叠保留。
- 上传 3,088 个变更文件，复用 7,355 个已有文件；继续使用纯静态 Pages，无新增付费服务。
- 网页链接、三组物理 SFG 及 47 项仿真验证通过；10 个线上关键文件的 SHA-256 与部署包一致。
- 浏览器已确认三组默认案例、原图和 SFG 加载，以及其他幻灯片展开／折叠操作。

本次明确发布指示仅用于此次更新；后续修订仍按项目约定，取得新的明确发布指示后再上线。
