# INTJ 升职加薪书影音实战指南

> 48 部精挑电影、电视剧和书籍，六条职场路线。每部都有 **为什么看 / 学到什么 / 看完做什么 / 什么不能照搬**，附 7 天、30 天实践方案和谈薪模板。

**作者：AI 酋长 Andy**｜[交互网站](https://aipmandy.github.io/intj-growth-guide/career/)｜[原有 41 部成长图鉴](../)｜[职业咨询与陪跑](https://metaver.vip/services)

![分享封面](assets/social-preview.svg)

## 一分钟用起来

1. 打开 [交互网站](https://aipmandy.github.io/intj-growth-guide/career/)，选自己遇到的真实卡点。
2. 根据「电影 / 电视剧 / 书籍」筛选，选择最有用的一部。
3. 点开卡片，先看 **行动建议**，确定自己愿意做。
4. 阅读 / 观看后完成小实验，标记为已实践。
5. 把成果写进 [晋升成果包](templates/promotion-case.md)，按 [30 天路线](guides/30-day.md) 迭代。

| 路线 | 真实问题 | 作品数 | 代表作品 |
| --- | --- | ---: | --- |
| 市场定位 | 我的经验为什么没有议价权 | 8 | 点球成金、硅谷、优秀到不能被忽视 |
| 业绩证明 | 做了很多却写不出成果 | 8 | 隐藏人物、熊家餐馆、这就是OKR |
| 沟通影响 | 方案正确却推不动别人 | 8 | 十二怒汉、继承之战、关键对话 |
| 晋升带队 | 想从骨干走向管理岗位 | 8 | 阿波罗13号、办公室、领导梯队 |
| 组织博弈 | 看不懂组织的决策和激励 | 8 | 商海通牒、新闻编辑室、系统之美 |
| 谈薪跳槽 | 如何申请合理薪酬与新机会 | 8 | 在云端、金装律师、谈判力 |

**48 部 = 18 部电影 + 12 部电视剧 + 18 本书**。完整机器可读目录在 [data/catalog.json](data/catalog.json)；作品解读均为项目原创编辑性内容。

## 交互网站有什么

- 48 部作品详情、6 种问题路线、3 种媒介筛选与即时搜索
- 个人收藏、实践标记、完成进度与随机推荐
- 每部作品有可以带去工作的行动建议和风险提醒
- 四周 30 天行动清单，记录在浏览器 localStorage
- 一键复制行动清单或导出 Markdown，便于 Obsidian / Notion / 飞书使用
- 手机与桌面响应式，无帐号、无后端、无第三方追踪脚本
- 作者链接、公开仓库、贡献指南与版权边界

> 浏览器本地状态可能因清理缓存或更换设备丢失；请定期导出 Markdown。本站不会把收藏与任务进度上传到服务器。

## 保姆级路线 / 工具

- [7 天快速起步](guides/7-day.md)
- [30 天升职证据实战](guides/30-day.md)
- [晋升答辩成果包模板](templates/promotion-case.md)
- [谈薪和 Offer 谈判模板](templates/salary-negotiation.md)
- [每周职业复盘模板](templates/weekly-review.md)
- [事实来源、局限与版权](docs/SOURCES.md)
- [参与共建](CONTRIBUTING.md)

## 目录

```text
career/
├── index.html                 # 专题网站
├── style.css                  # 响应式样式，无外部依赖
├── app.js                     # 搜索/过滤/收藏/进度/导出
├── data/catalog.json         # 48 条书影音数据
├── assets/social-preview.svg # 原创分享卡片
├── guides/                   # 7 / 30 天行动路线
├── templates/                # 晋升/谈薪/复盘可填模板
├── docs/SOURCES.md           # 内容原则、证据与限制
└── CONTRIBUTING.md           # 共建指引
```

## 本地预览

从仓库根目录运行：

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000/career/
python3 -m unittest discover -s tests -v
```

网站通过仓库现有 GitHub Actions 工作流发布到 GitHub Pages。新内容推送至 `main` 后会触发自动部署。发布状态见 [Actions](https://github.com/AIPMAndy/intj-growth-guide/actions/workflows/deploy-pages.yml)。

## 很重要的边界

人格类型只是题材标签，不能预测能力、职位或薪酬。作品中的虚构角色不能直接判定为 INTJ；影视剧情不可当真实职业证据。方法建议取决于你的职级、公司、行业、城市、个人约束等情况，**不存在 30 天保证晋升或涨薪**。

禁止在 Issue、PR 或公开提交中上传含有身份证号、未公开客户信息、员工档案、内部绩效与保密薪酬的数据。本项目不提供影视、电子书盗版资源。

项目中自行创作的代码、文本及 SVG 分享图沿用根目录 [MIT License](../LICENSE)。影视作品名、书名及其权利仍归原权利人所有。
