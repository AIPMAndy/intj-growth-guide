# INTJ 书影音开源指南｜升职加薪专题 + 完整成长图鉴

> **新增：INTJ 升职加薪的电影、电视剧、书籍推荐**。48 部作品、6 条真实职场路线、30 天实践计划、谈薪与晋升模板。免费开源，可贡献、可复用。

## 🚀 从「升职加薪专题」开始

**[🌐 打开 INTJ 升职加薪交互网站](https://aipmandy.github.io/intj-growth-guide/career/)**

**[📖 查看 48 部作品与全部源代码](career/README.md)** · [48 条结构化数据](career/data/catalog.json) · [30 天实战计划](career/guides/30-day.md) · [晋升成果包](career/templates/promotion-case.md) · [谈薪模板](career/templates/salary-negotiation.md)

| 专题方向 | 电影 | 电视剧 | 书籍 | 合计 |
| --- | ---: | ---: | ---: | ---: |
| INTJ 升职加薪 | 18 | 12 | 18 | **48** |

六条路线：市场定位、业绩证明、沟通影响、晋升带队、组织博弈、谈薪跳槽。

这里的作品解读都给出明确行动建议和“不该照搬”的提醒；没有“看完保升职”的虚假承诺。INTJ 只作为检索主题标签，不能预测能力和薪酬。

![INTJ 升职加薪分享封面](career/assets/social-preview.svg)

---

## 📚 原有项目：INTJ 成长必看 41 部书影音图鉴

如果你想研究更多系统思维、决策判断、情绪管理与个人成长主题，**原版内容完全保留**：

**[原版互动首页](https://aipmandy.github.io/intj-growth-guide/)** · [41 部完整解读](article.html) · [原版 7 / 30 天计划](plan.html) · [原版结构化目录](data/catalog.json)

原版包括：10 部电视剧、12 部电影、15 本书、4 部纪录片；六条路线覆盖决策判断、系统思维、职业与商业、沟通与关系、情绪与自洽、执行与成长。

## 🛠 开发、运行与贡献

本项目是静态 HTML / CSS / JavaScript，无后端。两套内容均可本地运行：

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000
```

打开 `http://localhost:8000/` 为原版，`http://localhost:8000/career/` 为升职加薪专题。

发布流程：[GitHub Pages 自动部署](.github/workflows/deploy-pages.yml) · [部署状态](https://github.com/AIPMAndy/intj-growth-guide/actions/workflows/deploy-pages.yml) · [共建指南](career/CONTRIBUTING.md)

## 作者与咨询

**AI 酋长 Andy**：前腾讯、百度 AI 产品从业者，曾任 AI 创业公司 VP，长期做职业发展和 AI 陪跑。

[个人网站](https://metaver.vip/) · [职业咨询与陪跑](https://metaver.vip/services) · 微信 `AIPMAndy`

内容免费公开，欢迎 Star、Fork、Issue 与 PR。仓库自身原创代码与文案使用 [MIT License](LICENSE)。书影音作品版权属于相应权利人；不提供盗版内容。
