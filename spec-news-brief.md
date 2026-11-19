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

观点来源（Economist 与 FT 为必查两家：窗口内全部相关栏目、专题与作者页先建完整候选清单再逐篇核对，合格文章全部纳入观点）：
- The Economist：官方 RSS `https://www.economist.com/latest/rss.xml`（300 条，只有标题与链接、无摘要）建候选清单；原站正文付费墙，tavily_extract 只到首段，写摘要标注「仅读到首段」。中文导读走 `https://news.sisuer.cn/tag/economist/` 取最新一期，URL 加 `.md` 取该期综述与中英目录，标「第三方导读，非原文」。
- FT：`https://www.ft.com/rss/` 下 world、markets、opinion、companies、economy、technology、global-economy、financials、climate-capital、lex、us、energy、trade 等栏目 feed，各 25 条，按 pubDate 筛窗口、按标题去重。原站正文 403 且付费墙，tavily_extract 也取不到；用 RSS 的 description 与页面 og:description（`/root/web-agent/run_page.sh` 拿到标题与导语），摘要只写导语支持的内容并标「仅读到导语」。FT 中文网首页可开但正文跳登录，不当作正文来源。
- 全文口径：Economist 与 FT 只用 RSS／导语或首段，摘要标注「仅读到导语/首段」，中文细节用 sisuer 综述补；用户已定先不接全文，不再为此重查。
- Foreign Affairs：`https://www.foreignaffairs.com/rss.xml`，curl 直连抓正文，失败时检索转载。
- Project Syndicate：`https://www.project-syndicate.org/rss`；带免费账号 Cookie 仍只能读到导言，标注「仅读到导言」。
- Foreign Policy：`https://foreignpolicy.com/feed/`（feed 带 content:encoded）；原页对自动化检测返回技术故障页，正文用 tavily_extract 取全文。
- Lawfare：`https://www.lawfaremedia.org/feeds/articles`（可能 403，失败转检索 lawfaremedia.org）；War on the Rocks：`https://warontherocks.com/feed/`。
- VoxEU：cepr.org 整站 Cloudflare 403，`rss.xml` 是空 channel，browser 停在「Just a moment」。用 tavily_search（site:cepr.org）发现专栏，再 tavily_extract 取全文，这条路线实测可拿到完整正文。
- Bruegel：`https://www.bruegel.org/rss.xml`（10 条，带摘要）；PIIE 无公开 RSS，`https://www.piie.com/research/publications` 直连 200，旧 /publications 已 403 重定向。
- Noema：`https://www.noemamag.com/feed/`。

新闻来源：
- WSJ：镜像 `https://nav.daven.us/wsj/` 只列标题与 wsj.com 原站链接（`?url=` 参数同样只回列表），不能取正文。原站 curl 401、browser 停在「Please enable JS and disable any ad blocker」。正文用 tavily_extract（实测首两段）或 tavily_search 片段，标注「仅读到导语」；时间核对用 Google News RSS `site:wsj.com when:1d`。`feeds.a.dj.com` 的 RSS 已停更，不用。
- Bloomberg：`https://feeds.bloomberg.com/markets/news.rss`、`https://feeds.bloomberg.com/politics/news.rss`（markets 偶发超时，重试一次）；原站 curl 403，正文用 browser（`/root/web-agent/run_page.sh`）读付费墙前几段，tavily_extract 对原站失败。
- Reuters：原站、RSS 均 401，tavily_extract 也取不到；用 tavily_search（topic=news、time_range=day、include_domains=reuters.com）拿标题与首段，或 Google News RSS 发现，正文从可直连转载（Japan Times、BNN Bloomberg、swissinfo、CNA）取；标注「路透稿件，转载」，全无可读转载时写明。
- NYT World：`https://rss.nytimes.com/services/xml/rss/nyt/World.xml`（59 条）；curl 403、browser 被同一广告拦截提示挡住，正文用 tavily_extract 取全文。
- Politico：美国版用 `https://rss.politico.com/politics-news.xml`（200，约 20 条，带 content:encoded）；Politico Europe 的 feed 403 Cloudflare，用 browser 打开站点取正文。
- Nikkei Asia：`https://asia.nikkei.com/rss/feed/nar`（51 条，无摘要）；curl 超时，browser 可开但付费墙只放前 3 段，摘要标注「仅读到开头」。
- Al Jazeera：`https://www.aljazeera.com/xml/rss/all.xml`；France 24：`https://www.france24.com/en/rss`。
- Rest of World：`https://restofworld.org/feed/` 对本机 IP 回 429，改用 browser 打开站点与文章；MIT Technology Review：`https://www.technologyreview.com/feed/`，正文直连可读（产品评测与纯消费科技不收）。
- AP：原站 feed 403 Cloudflare，browser 可正常打开站点与文章；也可用 Google News RSS 发现标题，转载时标注「美联稿件，转载」。
- BBC World：`https://feeds.bbci.co.uk/news/world/rss.xml`；Guardian World：`https://www.theguardian.com/world/rss`（补位与交叉核对）。

## 数量与编排
- 「一、观点」置于要闻之前：Economist 与 FT 的合格文章全部纳入，数量不设上限，不为压到十篇以内删减；其余来源择优补充，单一来源原则上最多 2 条。
- 全量纳入不等于不筛：只排除纯体育、娱乐、文化消费、生活方式、活动预告、讣告、纯产品评测、无实质短讯与经济社会政策无关的内容；深度报道与分析型新闻属于观点，摘要中区分事实报道与评论判断。
- 观点每篇 2–3 句，点明核心论点、关键依据或作用机制与作者/机构，优先呈现文章本身的增量判断，不复述新闻报道里的同一组事实。
- 「二、要闻」5–10 条，每条不超过两句，写清事件事实、关键数字与主要影响；不足 5 条按实际数量刊发，不凑数。
- 「今日主线」一句话串起当天最重要的 2–3 个点，放在标题之后、观点之前，浅色块突出。
- 编排前先按底层事件建主题簇，不按单篇：同一事件、同一轮融资／IPO、同一项公司决策、同一政策进展或同一争议的多篇报道合并为一条，标题角度不同也合并；不拆成融资安排、竞争影响、政府反应、市场反应等多条。
- 合并不等于混并：同一主体在窗口内彼此独立、时间与因果清楚分开且各有独立信息价值的事件可分别刊发，判断依据是底层事件是否相同，不是主体名称是否相同。
- 合并条目用一个准确的中文标题、一段统一摘要，来源栏并列全部原始链接并逐一标明机构与日期；摘要综合共同事实，保留各来源有实质差异的角度，不逐家重复转述。
- 同一事件跨观点与要闻出现时只留一处：观点留评论的机制或政策判断，要闻留事件事实；给不出不同增量就不重复呈现。
- 观点与要闻之间不复述同一组事实：观点只写评论本身的新论点。
- 按重要性排序，不按来源顺序机械排列。
- 只有 RSS 摘要可读时只写摘要能支持的事实，不补正文细节。

## 排除
- 活动预告、纯产品发布与评测、人物讣告、无实质内容的短讯、纯体育与娱乐文化消费类内容。
- 窗口外的旧文、已在上一期收录的同一事实；同一事件有新的实质进展时只写新增部分。

## 每条条目
- 标题：准确凝练的中文标题，不保留英文原题。
- 来源：中文资料名、发布机构、日期与可点击链接；转载与导读按上面的标注规则注明。
- 文字：正式、凝练，不写免责套话，不用“本文/该文”指称发布形式。

## 兜底与出页

- 出页前先查 `origin/main` 是否已有当天 `news-brief-YYYYMMDD.html`（本地根目录已有或 Pages 直链已 200 也算）：已存在就不生成、不覆盖，只回一行「今日已有出页，未重复生成」加该直链。
- 文件名、主色、模板、目录注入、首页重建、推送与交付按 `AGENTS.md` 的「栏目与产物」「页面生产」「发布」「交付」。
- 抓不到或整类渠道失效时按来源节标注，不编造、不用旧文凑数。
