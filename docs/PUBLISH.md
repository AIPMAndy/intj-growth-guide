# GitHub Pages 发布说明

仓库为 `AIPMAndy/intj-growth-guide`。项目是纯 HTML/CSS/JS 静态站点，无构建服务器要求，发布由 GitHub Actions 完成。

## 当前发布方式

`.github/workflows/deploy-pages.yml` 负责发布，流程是：

1. **validate**：执行 `python3 scripts/build.py --check`，确认 `index.html` 与 `data/catalog.json`、`site/` 一致；再跑全部测试。
2. **deploy**：校验通过后才上传仓库根目录并发布。

因此 Pages 的 Source 必须是 **GitHub Actions**，不是分支：

1. 打开 `Settings → Pages`。
2. 在 `Build and deployment` 将 Source 设为 `GitHub Actions`。
3. 不需要选分支和目录；推送 `main` 即自动发布，也可在 Actions 里手动 `Run workflow`。

站点地址：<https://aipmandy.github.io/intj-growth-guide/>，另需确认 `/article.html`、`/plan.html` 与一个不存在的地址（应显示自定义 404）。

## 日常改动流程

```bash
python3 scripts/build.py     # 改了 data/ 或 site/ 后重新生成 index.html
python3 scripts/check.py     # 本地跑一遍 CI 的全部检查
git add -A && git commit -m "feat: 新增条目"
git push
```

`article.html` 与 `plan.html` 是手工维护的独立页面，不参与构建，改动后直接提交。**不要手改 `index.html`**，它是生成产物。

## 发布失败排查

| 现象 | 优先检查 |
| --- | --- |
| Actions 中 validate 失败 | 本地跑 `python3 scripts/build.py --check`，多半是忘了提交重新生成的 `index.html` |
| deploy 报 `Pages site not found` | `Settings → Pages` 的 Source 是否已设为 GitHub Actions |
| 首页 404 | 仓库是否 Public；`index.html` 是否在根目录；部署记录是否成功 |
| 样式或图标缺失 | 是否提交了 `assets/` 下的 PNG；路径是否被误改为绝对路径 |
| 微信 / Twitter 分享无缩略图 | `og:image` 必须是 PNG 且为 1200×630，当前为 `assets/social-preview.png` |

## 回滚

Pages 部署对应具体 commit。回滚有两种方式：

1. 在本地 `git revert <bad-commit>` 后推送，走正常发布流程（推荐，保留历史）。
2. 在 Actions 中找到上一个成功的部署记录，确认其 commit，再对该 commit 执行 revert。

不要用 `git push --force` 覆盖 `main`：会跳过校验，也可能让线上版本与仓库历史脱节。

## 自定义域名（可选）

若要绑定自有域名：

1. 在仓库根目录添加 `CNAME`，内容为域名（如 `atlas.example.com`）。
2. 在域名服务商处添加 CNAME 记录指向 `aipmandy.github.io`。
3. 在 `Settings → Pages` 勾选 Enforce HTTPS。
4. 同步修改三处 `canonical`、`og:url`、`og:image` 与 `sitemap.xml`、`robots.txt` 中的域名，否则分享卡片和搜索引擎仍指向旧地址。

`sitemap.xml` 中的 `lastmod` 在内容有实质更新时手动更新。
