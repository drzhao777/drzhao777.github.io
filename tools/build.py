"""Build the eight static pages from the author's Markdown and TOML. Python 3.11+."""
import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, quote

try:
    import tomllib
except ModuleNotFoundError:
    raise SystemExit("本地生成网页需要 Python 3.11 或更高版本；也可以使用 GitHub 自动生成。")

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "tools/vendor"))
import markdown2
from sections import render_section

NAMES = ["About", "Publications", "Research", "Teaching", "CV", "Services", "People", "Openings"]
ICONS = {"linkedin":"LinkedIn", "scholar":"Google Scholar", "zhihu":"Zhihu", "researchgate":"ResearchGate", "orcid":"ORCID", "github":"GitHub"}
def md(s):
    return str(markdown2.markdown(s.strip(), extras=["tables","strike"]))
def inline(s):
    return md(s).strip().removeprefix("<p>").removesuffix("</p>")
def source(page):
    return (BASE / f"content/{page}.md").read_text(encoding="utf-8")
def local_asset(value, prefix):
    value = value.strip()
    if not value:
        return ""
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] not in ("assets","files") or not (BASE/path).is_file():
        raise ValueError(f"profile.toml：找不到本地附件 {value}；请将文件放到 files/ 并填写完整相对路径。")
    return escape(prefix + quote(path.as_posix()), quote=True)
def news():
    rows = []
    for line in re.sub(r"<!--.*?-->", "", source("News"), flags=re.S).splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith("## "):
            rows.append(f"<h3>{inline(line[3:])}</h3>")
        elif line.startswith("- ") and "|" in line:
            day, info = line[2:].split("|", 1)
            rows.append(f'<div class="news-row"><span class="date">{escape(day.strip())}</span><div>{inline(info.strip())}</div></div>')
        else: raise ValueError(f"content/News.md：请使用「## 年份」或「- 日期 | 正文」：{line}")
    return '<section class="news"><h2>🔥 News</h2>'+"".join(rows)+'</section>' if rows else ''
def home(cfg, name):
    img = local_asset(cfg["portrait"],"") or "assets/portrait.svg"
    links = []
    for key, label in ICONS.items():
        icon = f'<img src="assets/social/{key}.svg" width="29" height="29" alt="">'
        url = cfg["social"].get(key,"").strip()
        if url:
            if urlsplit(url).scheme not in ("http","https") or not urlsplit(url).netloc:
                raise ValueError(f"profile.toml：{key} 需要完整 https:// 网址。")
            links.append(f'<a href="{escape(url,quote=True)}" aria-label="{label}" title="{label}" rel="me">{icon}</a>')
        else:
            links.append(f'<span aria-hidden="true">{icon}</span>')
    email = cfg.get("email","").strip()
    contact = f'<a href="mailto:{escape(quote(email,safe="@+."))}">{escape(email)}</a>' if email else '[Your email]'
    body = md(source('About')).replace('<strong>Openings</strong>','<strong class="urgent">Openings</strong>')
    return f'''<header><h1>{name}</h1><p class="job">{escape(cfg["position"].strip() or "[Your position]@[Your institution]")}</p></header>
    <article><aside class="profile"><img class="portrait" src="{img}" alt="{'Portrait' if cfg['portrait'] else 'Portrait placeholder'}"><div class="socials">{"".join(links)}</div><p class="email">Email: {contact}</p></aside>
    <div class="bio">{body}</div>{news()}</article>'''
def page_html(page, cfg):
    is_home = page=="About"
    prefix = "" if is_home else "../"
    first,last = [cfg.get(i,"").strip() for i in ("first_name","last_name")]
    if not first and not last: first,last = "[Your", "Name]"
    full = escape(" ".join(x for x in [first,last] if x))
    name = (f"<strong>{escape(first)}</strong> {escape(last)}").strip()
    nav = []
    for item in cfg["pages"]:
        url = ("./" if is_home else "../") if item=="About" else prefix+item+"/"
        current = ' aria-current="page"' if item==page else ''
        nav.append(f'<a href="{url}"{current}>{item}</a>')
    brand = '' if is_home else f'<a class="brand" href="../">{name}</a>'
    if is_home:
        content = home(cfg, name)
    else:
        content = f'<h1 class="page-title">{page}</h1>' + render_section(page,source(page),md)
        if page == "CV" and cfg.get("cv_pdf"):
            content += f'<p><a href="{local_asset(cfg["cv_pdf"],prefix)}">Download CV (PDF)</a></p>'
    title = full if is_home else f'{page} | {full}'
    return f'''<!doctype html>
<html lang="{escape(cfg["language"],quote=True)}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E⚛️%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/sections.css"><script src="{prefix}assets/site.js"></script>
<noscript><style>@media(max-width:740px){{.nav-inner{{display:block}}.nav-links{{display:flex;flex-direction:row;flex-wrap:wrap}}.site-bar{{position:static}}body,body.about{{padding-top:0}}.menu,.theme{{display:none}}}}</style></noscript>
</head><body class="{'about' if is_home else 'subpage'}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-bar"><nav class="wrap nav-inner" aria-label="Main navigation">{brand}<button class="menu" aria-label="Toggle navigation" aria-controls="nav-links" aria-expanded="false"><i></i><i></i><i></i></button>
<div class="nav-links" id="nav-links">{"".join(nav)}
<button class="theme" aria-label="Change theme" title="Change theme"><svg viewBox="0 0 24 24" aria-hidden="true"><defs><g id="sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></g></defs><use href="#sun"/><path class="sun" d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5 M16 12a4 4 0 1 1-8 0 4 4 0 1 1 8 0Z"/><path class="moon" d="M20 15.5A8.5 8.5 0 0 1 8.5 4 8.5 8.5 0 1 0 20 15.5Z" fill="currentColor"/></svg></button>
</div></nav><div class="read-progress" aria-hidden="true"></div></header>
<main class="wrap" id="main">{content}</main>
<button class="to-top" hidden aria-label="Back to top" title="Back to top">↑</button>
<footer class="site-footer">© Copyright {date.today().year} {full}.</footer></body></html>'''
def build():
    cfg = tomllib.loads((BASE/'profile.toml').read_text(encoding='utf-8'))
    pages = cfg.get("pages", [])
    if "About" not in pages or len(set(pages))!=len(pages) or any(x not in NAMES for x in pages):
        raise ValueError("profile.toml：pages 需包含 About；请使用八个栏目原名，不要重复。")
    rendered = {page:page_html(page,cfg) for page in pages}
    out = BASE/"dist"
    if out.exists(): shutil.rmtree(out)
    out.mkdir()
    shutil.copytree(BASE/'assets',out/'assets')
    shutil.copytree(BASE/'files',out/'files',ignore=shutil.ignore_patterns(".gitkeep","README.md",".DS_Store"))
    for page,html in rendered.items():
        dest = out if page=="About" else out/page
        dest.mkdir(exist_ok=True)
        (dest/"index.html").write_text(html,encoding="utf-8")
    (out/".nojekyll").touch()
    print(f"已生成 {len(pages)} 个页面：{out / 'index.html'}")
if __name__=="__main__":
    build()
