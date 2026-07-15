# Hinata Documentation

The official documentation & self-hosting guide for **[Hinata](https://github.com/hinata-platform)** —
an open-source, self-hosted project & issue tracker with one published client app for self-hosted server instances.

📖 **Live site: https://hinata-platform.github.io**

The docs are bilingual (English 🇬🇧 / Deutsch 🇩🇪) and cover every feature plus a
complete guide to running your own server and shipping your own branded client.

- **App:** https://github.com/hinata-platform/hinata-app
- **Server:** https://github.com/hinata-platform/hinata-server

---

## How it's built

A tiny, dependency-light static-site generator (`build.py`) renders Markdown from
`content/<lang>/*.md` into a Liquid-Glass themed static site. No JS framework —
the output is plain HTML + one CSS + one JS file, with client-side ⌘K search.

```
content/
  nav.py            # navigation & site structure (single source of truth)
  en/*.md           # English pages
  de/*.md           # German pages
assets/             # styles.css, app.js, landing.js, favicon.svg
build.py            # Markdown -> static HTML generator
landing.py          # the root landing page
```

### Build locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py
python -m http.server -d site 8080   # http://localhost:8080
```

### Deploy

Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the
site and publishes it to GitHub Pages. No manual step required.

## Contributing to the docs

1. Edit or add a Markdown file under `content/en/` **and** `content/de/`
   (both languages are required).
2. If you add a page, register its slug + titles in `content/nav.py`.
3. Follow the conventions in [`tools/AUTHORING_BRIEF.md`](tools/AUTHORING_BRIEF.md).
4. Open a pull request.

## License

Documentation © the Hinata authors, released under **GPL-3.0** (matching the
platform). Made with 🍯.
