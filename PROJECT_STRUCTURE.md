# 项目结构说明 (Project Structure)

本文件详细说明了本博客项目的目录结构、各核心文件的功能以及自动化工作流的运行机制。

## 1. 核心目录结构

```text
E:\personal_web\siiverash.github.io
├── _config.yml             # Jekyll 全局配置文件（包含站点标题、描述、插件等）
├── index.md                # 博客首页，包含分类导航与 AI 动态展示区域
├── about.md                # 关于页面
├── search.json             # 全站搜索索引数据
├── Gemfile                 # Ruby 依赖管理文件
├── requirements.txt        # Python 脚本依赖文件（OpenAI, PyYAML, Requests 等）
│
├── _data/                  # 数据文件目录，用于存储静态或自动更新的数据
│   ├── me.yml              # 个人信息、硬件配置、摄影装备（Snap）等数据
│   └── recommendations.yml # 存储每日 AI 推荐的结构化数据
│
├── _includes/              # Jekyll 页面组件（HTML 片段）
│   ├── sidebar.html        # 主侧边栏
│   ├── extra-sidebar.html  # 文章详情页的扩展侧边栏（动态显示声优、装备等）
│   ├── head.html           # 页面头部引用（CSS、Meta 标签）
│   ├── scripts.html        # 全局 JS 逻辑（包含时钟、邮件提示等）
│   └── footer.html         # 页面底部
│
├── _layouts/               # 页面模板布局
│   ├── default.html        # 基础布局
│   ├── post.html           # 文章详情页布局
│   └── category.html       # 分类列表页布局
│
├── _posts/                 # 所有的博客文章 (Markdown 格式)
│   ├── 2026-02-18-Dongman.md
│   └── ...
│
├── assets/                 # 静态资源目录
│   ├── css/                # 样式表（main.css, responsive.css）
│   ├── js/                 # 脚本文件
│   └── images/             # 图片、图标资源
│
├── categories/             # 分类聚合页
│   ├── anime.md            # 动漫分类入口
│   ├── study.md            # 学习分类入口
│   └── ...
│
├── .github/workflows/      # GitHub Actions 自动化工作流
│   ├── deploy.yml          # 自动构建并部署到 GitHub Pages
│   ├── daily_update.yml    # 每日定时运行 update_daily.py 生成推荐
│   └── auto_tag_posts.yml  # 当有新文章提交时，自动打标签并提取作品名
│
└── scripts/                # Python 自动化脚本
    ├── update_daily.py     # 核心脚本：结合 DeepSeek AI 爬取信息并生成每日推荐
    ├── auto_tagger.py      # 自动根据文章内容生成 3-5 个精准标签
    └── extract_subject.py  # 专门针对动漫文章，精准提取“作品原名”用于 Bangumi 跳转
```

## 2. 核心功能说明

### 2.1 自动化工作流 (CI/CD)
*   **AI 自动打标签与作品提取**：当你上传新的 `.md` 文章到 `_posts` 目录时，系统会自动运行 `auto_tagger.py` 和 `extract_subject.py`。它们会使用 DeepSeek AI 分析你的内容，并在文章顶部自动添加 `tags`（标签）和 `subject`（作品名）。
*   **每日 AI 推荐**：通过 `daily_update.yml` 定时任务，DeepSeek 会结合实时热点（GitHub、新闻等）为你生成一份涵盖 Study、Anime、Game 等领域的推荐，并更新到首页。

### 2.2 前端交互特色
*   **动态扩展侧边栏**：在文章页中，如果是动漫文章，侧边栏会自动显示声优介绍；如果是摄影文章（snap），则会自动从 `_data/me.yml` 读取并展示你的 Z8 等拍摄装备。
*   **移动端适配**：侧边栏在手机端点击左上角“三杠”弹出，且针对分类列表过长的情况添加了**半透明细长滚动条**，确保护理体验。
*   **Bangumi 联动**：在动漫文章中，系统会根据 AI 提取的 `subject` 字段，自动生成跳转到 Bangumi 评分页面的链接。

## 3. 开发者手册
*   **本地运行脚本**：确保已设置 `DEEPSEEK_API_KEY` 环境变量。
*   **修改 UI**：移动端适配主要在 `assets/css/responsive.css` 中修改；全局 JS 逻辑在 `_includes/scripts.html` 中。
