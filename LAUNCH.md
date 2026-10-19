# 上线检查表

## 内容与页面

- [x] 41 条结构化书影音信息（10 剧 / 12 电影 / 15 书 / 4 纪录片）
- [x] 独立 HTML 首页与完整攻略页
- [x] 7/30 天可交互成长计划
- [x] 可搜索、筛选、收藏、完成标记与微信复制
- [x] 作品风险提醒与反方审查
- [x] 作者网站及咨询服务入口

## 发布与工程

- [x] GitHub Pages 通过 Actions 发布成功（[部署记录](https://github.com/AIPMAndy/intj-growth-guide/actions/runs/39141847219)）
- [x] 部署前强制校验：`build.py --check` + 全部测试通过才发布
- [x] 推送与 PR 均触发校验工作流
- [x] 构建产物可复现（`index.html` 与 `site/`、`data/` 一致）
- [x] 自定义 404 页
- [x] `sitemap.xml`、`robots.txt`
- [x] 站点图标：SVG favicon、32px PNG、180px Apple Touch Icon

## 分享与检索

- [x] Open Graph / Twitter Card 元信息（三个页面各自独立）
- [x] 社交预览图为 1200×630 PNG（SVG 不被微信、Twitter 等平台支持）
- [x] JSON-LD 结构化数据：`CollectionPage` + 41 项 `ItemList`
- [x] 每页独立 `canonical`
- [ ] 用微信、X、LinkedIn 各试分享一次，确认卡片标题与缩略图正确

## 仓库门面

- [x] README 含部署与校验徽章、目录、配套资源表
- [x] Issue 表单：作品推荐、内容纠错
- [x] PR 模板与提交前自检清单
- [x] 仓库 About 描述、主页链接与 Topics
- [ ] GitHub 仓库社交预览图（需在 `Settings → General → Social preview` 手动上传 `assets/social-preview.png`）

## 待验证

- [ ] 外部浏览器分别确认首页、完整攻略与互动计划正常显示
- [ ] 真实用户试读反馈与内容纠错
- [ ] 移动端 4G 首屏加载时间实测

上线时不要将 GitHub 已提交和 Pages 已发布混为一谈。
