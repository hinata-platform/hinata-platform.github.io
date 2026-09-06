# Hinata Documentation

The official documentation & self-hosting guide for **[Hinata](https://github.com/hinata-platform)** —
an open-source, self-hosted project & issue tracker with one published client app for self-hosted server instances.

📖 **Live site: https://hinata.ahmadre.com**

The docs are bilingual (English 🇬🇧 / Deutsch 🇩🇪) and cover every feature plus a
complete guide to running your own server and shipping your own branded client.

- **App:** https://github.com/hinata-platform/hinata-app
- **Server:** https://github.com/hinata-platform/hinata-server

---

## How it's built

A **Next.js** app (App Router, Turbopack, React 19) that pre-renders every page
to static HTML — `output: 'export'`, so what GitHub Pages serves is 116 files
and no server. Markdown from `content/<lang>/*.md` goes through remark/rehype
with build-time Shiki highlighting; the Liquid-Glass theme is one stylesheet.

```
content/
  nav.json          # navigation & site structure (single source of truth)
  en/*.md           # English pages
  de/*.md           # German pages
app/                # routes: /, /[lang], /[lang]/[slug], sitemap, search index
components/         # the chrome — top bar, sidebar, ⌘K palette, TOC rail
lib/                # markdown pipeline, nav model, version lookup
assets/             # favicon and the screenshots (masters + optimized variants)
scripts/            # asset mirror and the legacy-URL stubs, run around the build
```

Screenshots are not served as authored: `tools/optimize_images.py` writes AVIF
and WebP at four widths plus a 48px placeholder, and the markdown pipeline emits
a `<picture>` over them. Its output is committed — the encode is slow enough
that doing it in CI would add minutes to every deploy.

### Build locally

```bash
npm install
npm run dev                 # http://localhost:3000
npm run build && npm run preview
```

`npm run images` re-runs the screenshot optimizer (needs Python + Pillow).

### URLs

Pages live at `/<lang>/<slug>/`. The generator this replaced wrote
`/<lang>/<slug>.html`, and those addresses are in the store listings, in the
apps and in other people's links, so every one of them is still answered by a
stub that redirects — `scripts/legacy-urls.mjs` writes them after the export.

### Deploy

Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the
site and publishes it to GitHub Pages. No manual step required.

## Contributing to the docs

1. Edit or add a Markdown file under `content/en/` **and** `content/de/`
   (both languages are required).
2. If you add a page, register its slug + titles in `content/nav.json`.
3. Follow the conventions in [`tools/AUTHORING_BRIEF.md`](tools/AUTHORING_BRIEF.md).
4. Open a pull request.

## License

Documentation © the Hinata authors, released under **GPL-3.0** (matching the
platform). Made with 🍯.
