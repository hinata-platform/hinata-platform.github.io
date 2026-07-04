#!/usr/bin/env python3
"""Static-site generator for the Hinata documentation.

Renders bilingual (en/de) Markdown from content/<lang>/<slug>.md into a
Liquid-Glass themed static site under site/. Zero runtime JS framework — the
output is plain HTML + one CSS + one JS file, deployable on GitHub Pages as-is.

Usage:  python build.py            # build into ./site
Deps:   markdown, pygments  (see requirements.txt)
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

sys.path.insert(0, str(Path(__file__).parent / "content"))
from nav import SITE, UI, NAV  # noqa: E402

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "site"

# ---------------------------------------------------------------------------
# Lucide-style inline icons (the app uses Lucide, so we match it).
# ---------------------------------------------------------------------------
ICONS = {
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "server": '<rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>',
    "sparkles": '<path d="M9.94 14.34A6.53 6.53 0 0 0 4 20.5M12 3v4M12 3 9.5 5.5M12 3l2.5 2.5"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4M12.94 8.34 15 3l2.06 5.34L22 10.4l-4.94 2.06L15 17.8l-2.06-5.34L8 10.4z"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "plug": '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "devices": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "menu": '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "languages": '<path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>',
    "hexagon": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>',
}


def icon(name: str, cls: str = "") -> str:
    body = ICONS.get(name, "")
    c = f' class="{cls}"' if cls else ""
    return (
        f'<svg{c} xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


# ---------------------------------------------------------------------------
# Markdown pipeline
# ---------------------------------------------------------------------------
def make_md() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "attr_list",
            "def_list",
            "sane_lists",
            "md_in_html",
            "admonition",
            "codehilite",
            TocExtension(permalink="#", baselevel=2, toc_depth="2-3"),
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        },
    )


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text: str):
    meta = {}
    m = FM_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------
def flat_pages():
    """Return ordered list of (slug, titles-dict, group) across the whole nav."""
    out = []
    for group in NAV:
        for slug, titles in group["pages"]:
            out.append((slug, titles, group))
    return out


def page_url(lang: str, slug: str) -> str:
    if slug == "index":
        return f"/{lang}/"
    return f"/{lang}/{slug}.html"


def title_for(slug: str, lang: str) -> str:
    for s, titles, _ in flat_pages():
        if s == slug:
            return titles[lang]
    return slug


def render_sidebar(lang: str, active_slug: str) -> str:
    parts = ['<nav class="nav-tree" aria-label="Docs">']
    for group in NAV:
        parts.append('<div class="nav-group">')
        parts.append(
            f'<div class="nav-group-label">{icon(group["icon"], "nav-group-icon")}'
            f'<span>{escape(group["label"][lang])}</span></div>'
        )
        parts.append('<ul class="nav-links">')
        for slug, titles in group["pages"]:
            active = " active" if slug == active_slug else ""
            aria = ' aria-current="page"' if slug == active_slug else ""
            parts.append(
                f'<li><a class="nav-link{active}"{aria} href="{page_url(lang, slug)}">'
                f'{escape(titles[lang])}</a></li>'
            )
        parts.append("</ul></div>")
    parts.append("</nav>")
    return "".join(parts)


def render_toc(toc_tokens) -> str:
    if not toc_tokens:
        return ""
    items = []

    def walk(tokens):
        for t in tokens:
            items.append(
                f'<li class="toc-l{t["level"]}"><a href="#{t["id"]}">{escape(t["name"])}</a></li>'
            )
            if t.get("children"):
                walk(t["children"])

    walk(toc_tokens)
    return "<ul class='toc-list'>" + "".join(items) + "</ul>"


def prev_next(slug: str):
    seq = [s for s, _, _ in flat_pages()]
    i = seq.index(slug)
    prev = seq[i - 1] if i > 0 else None
    nxt = seq[i + 1] if i < len(seq) - 1 else None
    return prev, nxt


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def render_page(lang, slug, meta, body_html, toc_tokens, build_time):
    ui = UI[lang]
    other = "de" if lang == "en" else "en"
    title = meta.get("title", title_for(slug, lang))
    desc = meta.get("description", SITE["tagline"][lang])
    group_label = ""
    for g in NAV:
        if slug in [p[0] for p in g["pages"]]:
            group_label = g["label"][lang]
            break

    sidebar = render_sidebar(lang, slug)
    toc = render_toc(toc_tokens)
    prev, nxt = prev_next(slug)

    # prev/next cards
    nav_cards = ['<nav class="page-nav" aria-label="Pagination">']
    if prev:
        nav_cards.append(
            f'<a class="page-nav-card prev" href="{page_url(lang, prev)}">'
            f'{icon("arrow-left")}<span><em>{escape(ui["previous"])}</em>'
            f'<strong>{escape(title_for(prev, lang))}</strong></span></a>'
        )
    else:
        nav_cards.append("<span></span>")
    if nxt:
        nav_cards.append(
            f'<a class="page-nav-card next" href="{page_url(lang, nxt)}">'
            f'<span><em>{escape(ui["next"])}</em>'
            f'<strong>{escape(title_for(nxt, lang))}</strong></span>{icon("arrow-right")}</a>'
        )
    nav_cards.append("</nav>")

    # language switch target (same slug, other lang)
    other_url = page_url(other, slug)
    edit_url = f"{SITE['repo_org']}/hinata-platform.github.io/edit/main/content/{lang}/{slug}.md"
    canonical = f"{SITE['base_url']}{page_url(lang, slug)}"

    toc_block = (
        f'<aside class="toc-rail"><div class="toc-inner"><p class="toc-title">'
        f'{escape(ui["on_this_page"])}</p>{toc}</div></aside>'
        if toc
        else '<aside class="toc-rail"></aside>'
    )

    return TEMPLATE.format(
        lang=lang,
        title=escape(title),
        desc=escape(desc),
        canonical=canonical,
        og_url=canonical,
        site_name=SITE["name"],
        version=SITE["version"],
        sidebar=sidebar,
        body=body_html,
        toc=toc_block,
        nav_cards="".join(nav_cards),
        group_label=escape(group_label),
        page_title=escape(title),
        other_lang=other,
        other_lang_label=other.upper(),
        other_url=other_url,
        this_lang_label=lang.upper(),
        edit_url=edit_url,
        edit_label=escape(ui["edit_page"]),
        search_placeholder=escape(ui["search_placeholder"]),
        search_hint=escape(ui["search_hint"]),
        on_this_page=escape(ui["on_this_page"]),
        no_results=escape(ui["no_results"]),
        search_empty=escape(ui["search_empty"]),
        home_url=f"/{lang}/",
        repo_org=SITE["repo_org"],
        build_time=build_time,
        icon_menu=icon("menu"),
        icon_search=icon("search"),
        icon_languages=icon("languages"),
        icon_sun=icon("sun", "icon-sun"),
        icon_moon=icon("moon", "icon-moon"),
        icon_github=icon("github"),
        icon_hex=icon("hexagon", "brand-hex"),
        icon_copy=icon("copy"),
        copy_label=escape(ui["copy"]),
        copied_label=escape(ui["copied"]),
    )


# The page shell. {body} is trusted rendered markdown; everything else escaped.
TEMPLATE = """<!doctype html>
<html lang="{lang}" data-theme="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · {site_name} Docs</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{site_name} Documentation">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{og_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#151327">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" hreflang="{other_lang}" href="{other_url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/highlight.css">
<link rel="stylesheet" href="/assets/styles.css">
<script>
  (function() {{
    try {{
      var t = localStorage.getItem('hinata-theme');
      if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', t);
    }} catch (e) {{ document.documentElement.setAttribute('data-theme', 'light'); }}
  }})();
</script>
</head>
<body>
<div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

<header class="topbar">
  <div class="topbar-inner glass">
    <button class="icon-btn menu-toggle" id="menuToggle" aria-label="Menu">{icon_menu}</button>
    <a class="brand" href="{home_url}">
      <span class="brand-mark">{icon_hex}</span>
      <span class="brand-name">{site_name}<em>docs</em></span>
    </a>
    <button class="search-trigger" id="searchTrigger" aria-label="{search_placeholder}">
      {icon_search}<span>{search_hint}</span><kbd>⌘K</kbd>
    </button>
    <div class="topbar-actions">
      <a class="lang-switch" href="{other_url}" title="{other_lang_label}" aria-label="Language">
        {icon_languages}<span>{this_lang_label}</span>
      </a>
      <button class="icon-btn theme-toggle" id="themeToggle" aria-label="Toggle theme">
        {icon_sun}{icon_moon}
      </button>
      <a class="icon-btn" href="{repo_org}" target="_blank" rel="noopener" aria-label="GitHub">{icon_github}</a>
    </div>
  </div>
</header>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-inner glass">{sidebar}</div>
  </aside>
  <div class="sidebar-scrim" id="scrim"></div>

  <main class="content">
    <article class="prose">
      <div class="breadcrumb"><a href="{home_url}">{site_name}</a><span>/</span><span>{group_label}</span></div>
      <div class="page-actions">
        <a class="edit-link" href="{edit_url}" target="_blank" rel="noopener">{edit_label}</a>
      </div>
      {body}
      {nav_cards}
      <footer class="page-footer">
        <span>© <span id="year">2026</span> Hinata · GPL-3.0</span>
        <a href="{repo_org}" target="_blank" rel="noopener">GitHub</a>
      </footer>
    </article>
    {toc}
  </main>
</div>

<div class="search-modal" id="searchModal" aria-hidden="true">
  <div class="search-scrim" id="searchScrim"></div>
  <div class="search-box glass" role="dialog" aria-modal="true" aria-label="{search_placeholder}">
    <div class="search-field">{icon_search}
      <input type="search" id="searchInput" placeholder="{search_placeholder}" autocomplete="off" spellcheck="false">
      <kbd>ESC</kbd>
    </div>
    <div class="search-results" id="searchResults">
      <p class="search-empty">{search_empty}</p>
    </div>
  </div>
</div>

<script>
  window.HINATA = {{ lang: "{lang}", noResults: "{no_results}", copy: "{copy_label}", copied: "{copied_label}" }};
</script>
<script src="/assets/app.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # pygments highlight css
    from pygments.formatters import HtmlFormatter

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    # We ship our own token colours (see styles.css handles container); still emit
    # base structural css from pygments for correctness.
    hl = HtmlFormatter(style="default").get_style_defs(".codehilite")
    (OUT / "assets" / "highlight.css").write_text(PYGMENTS_CSS, encoding="utf-8")

    # copy static assets
    for f in (ROOT / "assets").glob("*"):
        if f.is_file():
            shutil.copy(f, OUT / "assets" / f.name)

    build_time = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    search_index = []
    built = 0

    for lang in SITE["languages"]:
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        for slug, titles, group in flat_pages():
            src = CONTENT / lang / f"{slug}.md"
            if not src.exists():
                print(f"  ! missing {lang}/{slug}.md — writing placeholder")
                raw = f"---\ntitle: {titles[lang]}\n---\n\n# {titles[lang]}\n\n_Coming soon._\n"
            else:
                raw = src.read_text(encoding="utf-8")
            meta, text = parse_front_matter(raw)
            meta.setdefault("title", titles[lang])
            md = make_md()
            body_html = md.convert(text)
            toc_tokens = getattr(md, "toc_tokens", [])

            html = render_page(lang, slug, meta, body_html, toc_tokens, build_time)
            dest = OUT / lang / ("index.html" if slug == "index" else f"{slug}.html")
            dest.write_text(html, encoding="utf-8")
            built += 1

            # search index entry (strip tags for plain text)
            plain = re.sub(r"<[^>]+>", " ", body_html)
            plain = re.sub(r"\s+", " ", plain).strip()
            search_index.append({
                "lang": lang,
                "title": meta["title"],
                "group": group["label"][lang],
                "url": page_url(lang, slug),
                "text": plain[:1400],
                "desc": meta.get("description", "")[:200],
            })

    (OUT / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )

    # root landing + language redirect helper
    (OUT / "index.html").write_text(render_landing(build_time), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n", encoding="utf-8"
    )
    (OUT / "sitemap.xml").write_text(render_sitemap(build_time), encoding="utf-8")
    (OUT / "404.html").write_text(render_404(), encoding="utf-8")

    print(f"✓ built {built} pages · {len(search_index)} indexed → {OUT}")


def render_sitemap(build_time):
    urls = []
    for lang in SITE["languages"]:
        for slug, _, _ in flat_pages():
            urls.append(
                f"<url><loc>{SITE['base_url']}{page_url(lang, slug)}</loc>"
                f"<lastmod>{build_time}</lastmod></url>"
            )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def render_404():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Not found · Hinata Docs</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>body{font-family:system-ui,sans-serif;background:#151327;color:#fff;display:grid;place-items:center;height:100vh;margin:0;text-align:center}a{color:#D9A032}</style>
</head><body><div><h1>404</h1><p>This page drifted off the board.</p>
<p><a href="/en/">← Documentation (EN)</a> · <a href="/de/">Dokumentation (DE) →</a></p></div></body></html>"""


# Landing page is rendered separately in build_landing.py content, imported here.
from landing import render_landing  # noqa: E402


# Minimal, readable Pygments token palette tuned for the glass code blocks.
PYGMENTS_CSS = """
.codehilite pre, .codehilite { background: transparent; }
.codehilite .hll { background-color: rgba(217,160,50,.15) }
.codehilite .c, .codehilite .ch, .codehilite .cm, .codehilite .c1, .codehilite .cs { color: #7f8aa6; font-style: italic }
.codehilite .cp { color: #b48ead }
.codehilite .k, .codehilite .kn, .codehilite .kd, .codehilite .kr, .codehilite .kt { color: #c792ea }
.codehilite .kc { color: #f78c6c }
.codehilite .o, .codehilite .ow { color: #89ddff }
.codehilite .p { color: #b6c2e2 }
.codehilite .s, .codehilite .s1, .codehilite .s2, .codehilite .sb, .codehilite .sc, .codehilite .sd, .codehilite .se, .codehilite .sh, .codehilite .si, .codehilite .sx, .codehilite .sr, .codehilite .ss, .codehilite .dl { color: #c3e88d }
.codehilite .m, .codehilite .mf, .codehilite .mh, .codehilite .mi, .codehilite .mo, .codehilite .il { color: #f78c6c }
.codehilite .na { color: #ffcb6b }
.codehilite .nb, .codehilite .bp { color: #82aaff }
.codehilite .nc, .codehilite .nn { color: #ffcb6b }
.codehilite .nf, .codehilite .fm { color: #82aaff }
.codehilite .nt { color: #f07178 }
.codehilite .nv, .codehilite .vc, .codehilite .vg, .codehilite .vi { color: #eeffff }
.codehilite .gd { color: #f07178 }
.codehilite .gi { color: #c3e88d }
.codehilite .gh { color: #82aaff; font-weight: 600 }
.codehilite .err { color: #ff5370 }
"""


if __name__ == "__main__":
    build()
