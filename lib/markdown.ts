import fs from 'node:fs';
import path from 'node:path';

import matter from 'gray-matter';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeRaw from 'rehype-raw';
import rehypeSlug from 'rehype-slug';
import rehypeStringify from 'rehype-stringify';
import remarkGfm from 'remark-gfm';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import { createHighlighter, type Highlighter } from 'shiki';
import { unified } from 'unified';
import { visit } from 'unist-util-visit';
import type { Element, Root as HastRoot, Text as HastText } from 'hast';
import type { Root as MdRoot } from 'mdast';

export interface Heading {
  id: string;
  text: string;
  depth: number;
}

export interface RenderedPage {
  html: string;
  meta: { title?: string; description?: string };
  headings: Heading[];
}

// ── images ──────────────────────────────────────────────────────────────────
//
// Authors write `![alt](/assets/img/x.png)` and should carry on doing so. What
// leaves the pipeline is a <picture> over the AVIF/WebP variants that
// tools/optimize_images.py produced, with the intrinsic size and the 20px
// placeholder from its manifest.
//
// This is deliberately not `next/image`: on a static export its optimizer does
// not run, so it would hand back the original PNG — the 1.25 MB that made the
// old site slow on a phone in the first place.

interface ImageEntry {
  w: number;
  h: number;
  widths: number[];
  lqip?: string;
}

const MANIFEST: Record<string, ImageEntry> = JSON.parse(
  fs.readFileSync(
    path.join(process.cwd(), 'assets', 'img', 'opt', 'manifest.json'),
    'utf8',
  ),
);

/** The content column is 780px; below the breakpoint an image is the viewport. */
const SIZES_BODY = '(max-width: 820px) 100vw, 780px';

function pictureFor(src: string, alt: string, sizes = SIZES_BODY): Element | null {
  const name = src.split('/').pop() ?? '';
  const entry = MANIFEST[name];
  if (!entry) return null;
  const stem = name.replace(/\.png$/, '');
  const srcset = (ext: string) =>
    entry.widths.map((w) => `/assets/img/opt/${stem}-${w}.${ext} ${w}w`).join(', ');

  const img: Element = {
    type: 'element',
    tagName: 'img',
    properties: {
      src: `/assets/img/opt/${stem}-${Math.min(...entry.widths)}.webp`,
      alt,
      width: entry.w,
      height: entry.h,
      loading: 'lazy',
      decoding: 'async',
      // The placeholder paints in the first frame, so a lazy image is a blurred
      // version of itself while it loads rather than a hole in the page.
      ...(entry.lqip
        ? { style: `background-image:url(${entry.lqip});background-size:cover` }
        : {}),
    },
    children: [],
  };

  return {
    type: 'element',
    tagName: 'picture',
    properties: {},
    children: [
      { type: 'element', tagName: 'source', properties: { type: 'image/avif', srcSet: srcset('avif'), sizes }, children: [] },
      { type: 'element', tagName: 'source', properties: { type: 'image/webp', srcSet: srcset('webp'), sizes }, children: [] },
      img,
    ],
  };
}

function rehypeResponsiveImages() {
  return (tree: HastRoot) => {
    visit(tree, 'element', (node: Element, index, parent) => {
      if (node.tagName !== 'img' || !parent || typeof index !== 'number') return;
      const src = String(node.properties?.src ?? '');
      if (!src.startsWith('/assets/img/')) return;
      const replacement = pictureFor(src, String(node.properties?.alt ?? ''));
      if (replacement) parent.children[index] = replacement;
    });
  };
}

// ── admonitions ─────────────────────────────────────────────────────────────
//
// The content uses python-markdown's syntax, which nothing in the remark world
// speaks:
//
//     !!! note "An optional title"
//         The indented body.
//
// Rewriting 108 files to fit a plugin would be the wrong way round — the
// content is the asset here, the generator is replaceable. So the generator
// learns the syntax instead.

const ADMONITION = /^!!!\s+(\w+)(?:\s+"([^"]*)")?\s*$/;

function remarkAdmonitions() {
  return (tree: MdRoot) => {
    visit(tree, 'paragraph', (node, index, parent) => {
      if (!parent || typeof index !== 'number') return;
      const first = node.children[0];
      if (first?.type !== 'text') return;
      const [head, ...rest] = first.value.split('\n');
      const m = ADMONITION.exec(head ?? '');
      if (!m) return;

      const kind = m[1] ?? 'note';
      const title = m[2];
      // python-markdown takes the indented block that follows; after parsing,
      // that arrives as the remainder of this paragraph's text.
      const body = rest.map((l) => l.replace(/^ {4}/, '')).join('\n').trim();
      const children: MdRoot['children'] = [];
      if (title) {
        children.push({
          type: 'paragraph',
          data: { hName: 'p', hProperties: { className: ['admonition-title'] } },
          children: [{ type: 'text', value: title }],
        });
      }
      if (body) children.push({ type: 'paragraph', children: [{ type: 'text', value: body }] });
      // Anything else that was part of the same paragraph node.
      children.push(...(node.children.slice(1) as MdRoot['children']));

      parent.children[index] = {
        type: 'blockquote',
        data: { hName: 'div', hProperties: { className: ['admonition', kind] } },
        children,
      } as MdRoot['children'][number];
    });
  };
}

// ── code highlighting ───────────────────────────────────────────────────────
//
// Shiki, using the same grammars VS Code does, so a snippet looks the same in
// the docs as in the editor it was copied from. It runs at build time only —
// nothing about highlighting reaches the browser.

let highlighter: Highlighter | undefined;

const LANGS = [
  'bash', 'json', 'yaml', 'dart', 'java', 'kotlin', 'sql', 'xml', 'html',
  'css', 'javascript', 'typescript', 'python', 'ini', 'diff', 'nginx', 'dockerfile',
];

async function getHighlighter(): Promise<Highlighter> {
  highlighter ??= await createHighlighter({
    themes: ['github-light', 'github-dark'],
    langs: LANGS,
  });
  return highlighter;
}

function rehypeShiki(hl: Highlighter) {
  return (tree: HastRoot) => {
    visit(tree, 'element', (node: Element, index, parent) => {
      if (node.tagName !== 'pre' || !parent || typeof index !== 'number') return;
      const code = node.children[0];
      if (code?.type !== 'element' || code.tagName !== 'code') return;
      const className = (code.properties?.className ?? []) as string[];
      const lang = className
        .map((c) => c.replace(/^language-/, ''))
        .find((c) => LANGS.includes(c));
      const text = (code.children[0] as HastText | undefined)?.value ?? '';

      // Both themes are emitted; CSS variables pick one, so switching the site
      // theme does not need a second copy of every snippet.
      const html = hl.codeToHtml(text, {
        lang: lang ?? 'text',
        themes: { light: 'github-light', dark: 'github-dark' },
        defaultColor: false,
      });
      parent.children[index] = {
        type: 'raw',
        value: html,
      } as unknown as Element;
    });
  };
}

// ── headings, for the "on this page" rail ───────────────────────────────────

function collectHeadings(tree: HastRoot, into: Heading[]) {
  visit(tree, 'element', (node: Element) => {
    if (!/^h[23]$/.test(node.tagName)) return;
    const id = String(node.properties?.id ?? '');
    if (!id) return;
    let text = '';
    visit(node, 'text', (t: HastText) => {
      text += t.value;
    });
    into.push({ id, text: text.replace(/#$/, '').trim(), depth: Number(node.tagName.slice(1)) });
  });
}

export async function renderMarkdown(source: string, version: string): Promise<RenderedPage> {
  const { data, content } = matter(source);
  const headings: Heading[] = [];
  const hl = await getHighlighter();

  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkAdmonitions)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, { behavior: 'append', properties: { className: ['anchor'], ariaHidden: 'true', tabIndex: -1 }, content: { type: 'text', value: '#' } })
    .use(rehypeResponsiveImages)
    .use(() => (tree: HastRoot) => rehypeShiki(hl)(tree))
    .use(() => (tree: HastRoot) => collectHeadings(tree, headings))
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(content.replaceAll('{{version}}', version));

  return {
    html: String(file),
    meta: { title: data.title, description: data.description },
    headings,
  };
}
