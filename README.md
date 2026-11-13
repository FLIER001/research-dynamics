# 日报项目目录说明

本目录是四个栏目日常产出的工作目录：要闻观点摘编、智库与国际组织研究动态、国内外政策动态、学术研究前沿。

## 常驻文件（不要移动）
- `AGENTS.md`：目录与操作约定，任务开始时会读。
- `spec-daily-research.md`：智库与国际组织研究动态规范（08:50，工作日）。
- `spec-news-brief.md`：要闻观点摘编规范（08:35，每日）。
- `spec-academic-frontier.md`：学术研究前沿规范（09:20，每周一）。
- `spec-policy-watch.md`：国内外政策动态规范（09:05，工作日）。
- `style-template.html`：四个栏目共用的版式模板，出页时原样复制其 style 块与骨架，只把 `--accent` 换成本栏目主色。
- `index.html`：首页的本地副本，发布时同步到仓库。
- `package.json` / `package-lock.json` / `node_modules/`：PDF 解析工具（pdf-parse），抓年报、报告 PDF 时用；不要删。

## 首页与归档（自动生成）
- `build_index.py` 扫描本目录的成品页，生成 `index.html`（四栏，每栏月份按钮 + 同页日历）、`archive-academic.html`、`archive-research.html`、`archive-policy.html`、`archive-brief.html`（按年、月分组）、`site.css` 与 `manifest.json`（全部期数的清单）。
- 不要手工编辑这几个文件；改版或新增期数后重跑脚本即可。
- 单页超过约 200 行时按年拆页（如 `archive-research-2026.html`）；期数过三百后再考虑加客户端搜索。

## 成品
发布的页面都直接落在本目录根下，文件名固定：
- `academic-frontier-YYYYMMDD.html`
- `research-dynamics-YYYYMMDD.html`
- `news-brief-YYYYMMDD.html`
- `policy-watch-YYYYMMDD.html`

产物发布到 `FLIER001/research-dynamics` 的 main 分支，通过 `https://flier001.github.io/research-dynamics/<文件名>` 访问。

## 归档
- `归档/脚本/`：几个有代表性的生成脚本（build1113.py 日报、build1113brief.py 简报、restyle1112.py 重排版式），供以后复刻结构时参考。
- 成品页面不移动：首页与归档由 `build_index.py` 扫描根目录生成，移走会从归档中消失；期数过多时由脚本按年拆页。

## 清理原则
- 抓取过程文件（`d111x/`、`b111x/`、`p111x/` 这类目录，以及临时 XML/JSON/HTML/PDF/txt）用完即删，不长期保存；内容已在成品页面里，来源可重新抓取。
- 一次性的 build、merge、索引备份脚本不留在根目录；需要复用的放 `归档/脚本/`。
- 首页只保留当前使用的 `index.html`，历史版本不留在根目录。
