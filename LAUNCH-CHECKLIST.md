# 主站② 上线清单（gamecodetoday.com，域名注册后按序）
1. YG：Dynadot 注册 gamecodetoday.com（~$10/年）→ CF 加 zone + orange-cloud A @ → GH Pages repo（percallio/gamecodetoday.com，PAT 同主站①）
2. 我：把本 staging 推到 repo（替换 sitemap/llms/canonical 的域名占位=已是 gamecodetoday.com）
3. 我：批次 19 页（site2-batch1-words.md 的 top 19 词，每页=码表+双源核验+expired 区；弱模型抽取官方源码表+judge 双源验证，F12 纪律）
4. 我：gen_og（游戏版 stat 行=N working codes + last checked）+ qa_gate.py 9/9 全绿
5. 我：GSC 加站+提交 sitemap；GA4/GTM 换 property（站群隔离纪律）
6. 我：codes_fetcher.py 日更管线（每游戏源 URL 配置化→弱模型抽码→双源对账→页面刷新→push）+ daemon 实例 2
7. YG：Reddit r/RobloxGames 或游戏官方 Discord 发码表帖（评论包打法 F13）
8. 判读：14 天 GSC 展现>0 + 首条 Reddit 帖互动 → 批次 #2（229 词池继续排产）
