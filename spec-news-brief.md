# 要闻观点摘编 · 任务规范（固定不变）

## 截止与窗口
- 每日北京时间 08:35 为截止点，覆盖前一日 08:35 至当日 08:35，共 24 小时。
- 截止之后发布的内容归下一期；窗口内无符合内容就不收，不拿旧文凑数，不要求每个来源每期都出现。

## 检索顺序
- 单一来源先用专用渠道（镜像、RSS、转载页、站点搜索接口），能直达就不绕道搜索引擎。
- 需要检索、核对或专用渠道失效时：codex_search → tavily（必要时 tavily_extract）→ web_search 兜底；某个工具不可用就跳下一个，不反复重试。
- codex 对 reuters.com 检索为空，不能当兜底。
- 每条必须有可点击链接；Google News 跳转页不能作为引用链接。

## 来源与入口

观点来源：
- The Economist：官方 RSS `https://www.economist.com/latest/rss.xml` 核对标题与链接；周刊页被 Cloudflare 拦截，不再试原页。正文导读走 `https://news.sisuer.cn/tag/economist/` 取最新一期，URL 加 `.md` 取正文。条目标注「第三方导读，非原文」。
- Foreign Affairs：`https://www.foreignaffairs.com/rss.xml`，curl 直连抓正文，失败时检索转载。
- Project Syndicate：`https://www.project-syndicate.org/rss`；带免费账号 Cookie 仍只能读到导言，标注「仅读到导言」。
- Foreign Policy：`https://foreignpolicy.com/feed/`。
- Lawfare：`https://www.lawfaremedia.org/feeds/articles`（可能 403，失败转检索 lawfaremedia.org）；War on the Rocks：`https://warontherocks.com/feed/`。
- VoxEU：`https://cepr.org/voxeu` 与 feed 可能 403，用检索并打开原页核对。
- Bruegel：`https://www.bruegel.org/rss.xml`；PIIE 无公开 RSS，查官网 What's New 与 commentary 栏目。
- Noema：`https://www.noemamag.com/feed/`。

新闻来源：
- WSJ：镜像 `https://nav.daven.us/wsj/`（同标题去重）；时间核对用 Google News RSS `site:wsj.com when:1d`；引用镜像给出的 wsj.com 原站地址。头版 PDF 按美东日期判断，403 直接跳过。`feeds.a.dj.com` 的 RSS 已停更，不用。
- Bloomberg：`https://feeds.bloomberg.com/markets/news.rss`、`https://feeds.bloomberg.com/politics/news.rss`；原站 403，不直连。
- Reuters：原站、RSS 均 401；用 tavily_search（topic=news、time_range=day、include_domains=reuters.com）或 Google News RSS 发现标题，正文从可直连转载（Japan Times、BNN Bloomberg、swissinfo、CNA）取；标注「路透稿件，转载」，全无可读转载时写明。
- NYT World：`https://rss.nytimes.com/services/xml/rss/nyt/World.xml`。
- Politico：美国版 RSS 403，用 Google News RSS 发现再做检索核对；Politico Europe：`https://www.politico.eu/feed/`。
- Nikkei Asia：`https://asia.nikkei.com/rss/feed/nar`。
- Al Jazeera：`https://www.aljazeera.com/xml/rss/all.xml`；France 24：`https://www.france24.com/en/rss`。
- Rest of World：`https://restofworld.org/feed/`；MIT Technology Review：`https://www.technologyreview.com/feed/`（产品评测与纯消费科技不收）。
- AP：原站不稳定，用 Google News RSS 发现标题后找可读转载，标注「美联稿件，转载」。
- BBC World：`https://feeds.bbci.co.uk/news/world/rss.xml`；Guardian World：`https://www.theguardian.com/world/rss`（补位与交叉核对）。
- FT 已排除，不要加回。

## 数量与编排
- 「一、观点」5–10 篇，置于要闻之前；每篇 2–3 句，点明核心论点、关键依据、作者或机构，优先有机制、数据和具体政策主张的文章。
- 「二、要闻」5–10 条，每条不超过两句，写清事实、关键数字与影响。
- 「今日主线」一句话串起当天最重要的 2–3 个点，放在标题之后、观点之前，浅色块突出。
- 同一事件被多家报道只出一条：各来源链接并列该条之后，摘要综合各方事实与数字，不拆成「公司动作／国会反应／外交影响」多条。
- 观点与要闻之间不复述同一组事实：观点只写评论本身的新论点。
- 按重要性排序；单一来源原则上最多 2 条。
- 只有 RSS 摘要可读时只写摘要能支持的事实，不补正文细节。

## 排除
- 活动预告、纯产品发布与评测、人物讣告、无实质内容的短讯。
- 窗口外的旧文、已在上一期收录的同一事实。

## 每条条目
- 标题：准确凝练的中文标题，不保留英文原题。
- 来源：中文资料名、发布机构、日期与可点击链接；转载与导读按上面的标注规则注明。
- 文字：正式、凝练，不写免责套话，不用“本文/该文”指称发布形式。

## 交付物
- 单文件手机端 HTML：`news-brief-YYYYMMDD.html`，存放于 `/root/workspace/日报`；标题《要闻观点摘编（YYYY年MM月DD日）》。
- 版式原样复制 `style-template.html` 的 style 块与页面骨架，只换文字；本栏目主色 `#1f4e79`（把 `:root` 的 `--accent` 换成本色）。
- 出页后运行 `python3 build_index.py`，重建 `index.html`、四个 `archive-*.html`、`site.css`、`manifest.json`。
- 提交当期 HTML 与 `index.html`、`archive-academic.html`、`archive-research.html`、`archive-policy.html`、`archive-brief.html` 到 `FLIER001/research-dynamics` 的 main 分支。
- 交付只回 Pages 直链，附一行「本期 X 篇观点 · Y 条要闻」，不附其他链接，不调用 present。
