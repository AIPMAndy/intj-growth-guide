# GitHub Pages 发布说明

仓库为 `AIPMAndy/intj-growth-guide`。本项目以 HTML/CSS/JS 静态页面运行，无构建服务器要求。

1. 在 GitHub 打开 `Settings → Pages`。
2. 在 `Build and deployment` 将 Source 设置为 `Deploy from a branch`。
3. Branch 选择 `main`，Folder 选择 `/(root)`，点击 Save。
4. 等待 GitHub Pages 构建并显示发布成功。
5. 网站应为 https://aipmandy.github.io/intj-growth-guide/ ，并分别检查 `/article.html` 和 `/plan.html`。

如果看见 404：确认仓库 Public、Pages 的 main/root 配置已保存、首页 `index.html` 在仓库根目录，以及 Actions 中是否显示部署成功。

每次修改结构化数据后在本地运行 `python3 scripts/build.py` 重新生成独立首页，提交 `data/catalog.json` 和 `index.html`。GitHub Action 会检查文件一致性。
