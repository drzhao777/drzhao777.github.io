# 个人学术主页

这是可独立维护的 GitHub Pages 学术主页。版式参考 [tbendong.github.io](https://tbendong.github.io/)：八个栏目、右侧照片、按年分组的动态，以及独立的研究、论文和成员页面。姓名、经历、论文、照片和联系方式都留给你填写。无需注册第三方服务。

## 从哪里开始

**第一步只改 [profile.toml](profile.toml)**：把姓名、职位、单位和邮箱填在英文双引号内。比如中文姓名可以完整填在 `first_name`，`last_name` 留空。没有照片、个人链接或简历 PDF 时，相关字段可以继续留空。空的社交图标不是链接。请勿填入不希望公开的资料。

**第二步写 [个人简介](content/About.md)**：把英文方括号和里面的提示一起替换成你的文字。可写中文或英文。可以先写一段，再逐步增加研究方向、论文与动态。暂不展示的整个栏目可从 `profile.toml` 的 `pages` 列表移除；重新加回即可恢复原内容。想隐藏首页 News，可清空 [News.md](content/News.md)。

| 我想修改 | 修改位置 | 写法 |
| --- | --- | --- |
| 姓名、职位、邮箱和社交链接 | [profile.toml](profile.toml) | 修改引号中的值 |
| 头像、简历 PDF | [files/](files/) + [profile.toml](profile.toml) | 上传文件，例如在 `portrait` 填 `"files/photo.jpg"`、在 `cv_pdf` 填 `"files/cv.pdf"` |
| 个人介绍、研究兴趣、首页招生提示 | [About.md](content/About.md) | 空一行分段，用 `- ` 列要点 |
| 首页动态 | [News.md](content/News.md) | 年份前加 `## `；每条写作 `- 日期 \| 正文`，最新放在最前 |
| 期刊论文、会议论文 | [Publications.md](content/Publications.md) | 在相应分类中每篇加一行 `- 作者，题名，期刊，年份。`，编号自动生成 |
| 研究课题、配图、代表作 | [Research.md](content/Research.md) | 复制一个课题小节；图片路径如 `../files/research.png`，下一段斜体为图注 |
| 课程 | [Teaching.md](content/Teaching.md) | 修改研究生或本科课程列表 |
| 教育、工作经历、奖项 | [CV.md](content/CV.md) | 修改相应小节 |
| 学术服务 | [Services.md](content/Services.md) | 编辑任职、会员或审稿列表 |
| 团队成员 | [People.md](content/People.md) | 在对应分组中复制从 `### 姓名` 开始的一段；可替换或删掉照片行 |
| 招生说明 | [Openings.md](content/Openings.md) | 填写研究方向、申请条件和流程 |

Markdown 中 `**文字**` 表示加粗，`[显示文字](https://...)` 表示链接。不需要的占位条目或段落可以直接删除。正文里以 `<!--` 和 `-->` 包住的中文提示不会出现在浏览器里。

## 本地预览

在这台 Mac 上，双击 [预览主页.command](预览主页.command)，会生成并打开网页。每次编辑后再双击一次，或在终端从项目文件夹运行 `python3 tools/build.py`。已生成的 [dist/index.html](dist/index.html) 可直接在本机浏览器打开；导航、主题、图片和字体均可离线使用。网页由源码生成，请直接修改上表中的文件。

新克隆的仓库不会包含 `dist/`；本地生成需要 Python 3.11 或以上版本，没有额外的软件包。只在 GitHub 网页上维护时，电脑不需要安装 Python。

## 第一次发布到自己的 GitHub Pages

1. 登录 GitHub Desktop，点 **File → Add Local Repository… → Choose…**，选包含 `profile.toml` 的 `academic-homepage` 文件夹，然后点 **Add Repository**。
2. 点 **Publish repository**。把 **Name** 改成「小写的 GitHub 用户名」加上 `.github.io`。例如用户名为 `linchen`，仓库名就填 `linchen.github.io`。选个人账号，免费账号取消勾选 **Keep this code private**，再点 **Publish Repository**。如果你已经用同名仓库运行另一个主页，可以先取新仓库名 `academic-homepage`；它会拥有独立的项目网址。参见[从 Desktop 发布已有项目](https://docs.github.com/zh/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop)和[个人 Pages 仓库命名规则](https://docs.github.com/zh/pages/getting-started-with-github-pages/creating-a-github-pages-site)。
3. 在 Desktop 点 **Repository → View on GitHub**，在网页中进入 **Settings → Pages → Build and deployment**。把 **Source** 设为 **GitHub Actions**。模板已经带有发布工作流。参见[配置 Pages 发布来源](https://docs.github.com/zh/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。
4. 在仓库网页打开 **Actions**，左栏选 **Deploy academic homepage**，点 **Run workflow**，选择 `main`，再点绿色的 **Run workflow**。首次上传可能会在完成第 3 步前触发一次发布；设置好 Pages 后手动运行一次即可。参见[手动运行工作流](https://docs.github.com/zh/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)。
5. 等本次运行出现绿色对勾，回到 **Settings → Pages** 点 **Visit site**。上例的个人主页网址是 `https://linchen.github.io/`，项目仓库的网址则是 `https://linchen.github.io/academic-homepage/`。后续每次把更改提交到 `main`，工作流都会重新生成并发布网页。

## 以后怎么更新

**用 GitHub 网页版改文字。** 进入仓库的 **Code** 页，打开 `profile.toml` 或 `content/` 中对应栏目的 `.md` 文件，点右上角的铅笔图标。写完点 **Commit changes**，填一句说明（例如“更新个人简介”），提交到 `main`。要上传照片或 PDF，先进入放置该资源的文件夹，点 **Add file → Upload files** 上传，再在对应内容中填写文件路径。链接中的文件名要与上传的文件完全一致，包括大小写。参见[网页上传文件](https://docs.github.com/zh/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)。

**用 GitHub Desktop 一次改多处。** 编辑前在客户端点 **Fetch origin**，若出现 **Pull origin**，点击同步到本机。用文本编辑器修改本地仓库中的文件并保存。在 Mac 上双击 `预览主页.command` 检查效果。打开 Desktop，在 **Changes** 查看修改，**Summary** 填本次改了什么，点 **Commit to main**，再点 **Push origin** 发布。参见[提交与推送修改](https://docs.github.com/zh/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop)。

**网址显示 404，或仍是旧内容。** 先看 **Actions → Deploy academic homepage** 最近一次运行有没有绿色对勾。若为红色，点击展开失败的步骤，按日志中指出的文件或设置修正后重新提交。若没有这项工作流，查看仓库首页能否直接看到 `.github/workflows/` 和 `profile.toml`。成功后以 **Settings → Pages → Visit site** 打开的地址为准，在浏览器强制刷新一次（Mac 按 `⌘⇧R`，Windows 按 `Ctrl+F5`）。

## 项目组成

`content/` 与 `profile.toml` 是内容来源；`assets/` 管版式和图标；`tools/` 将内容转换成八个独立的 HTML 页面；`.github/workflows/pages.yml` 发布生成的 `dist/`。字体、图标和 Markdown 转换器的许可随相应文件收录在 `assets/fonts/`、`assets/social/` 和 `tools/vendor/` 中。
