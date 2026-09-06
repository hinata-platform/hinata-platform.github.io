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

import { IMAGE_MANIFEST } from './images';

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

/** The content column is 780px; below the breakpoint an image is the viewport. */
const SIZES_BODY = '(max-width: 820px) 100vw, 780px';

function pictureFor(
  src: string,
  alt: string,
  eager: boolean,
  sizes = SIZES_BODY,
): Element | null {
  const name = src.split('/').pop() ?? '';
  const entry = IMAGE_MANIFEST[name];
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
      // The width/height pair reserves the box so nothing below the image
      // moves when it lands. It only works together with `height: auto` in the
      // stylesheet — without that, the height attribute *is* the used height
      // and a 2880x1800 screenshot renders 1800px tall in a 390px column.
      decoding: 'async',
      // The first image on a page is at or just below the fold, so lazy-loading
      // it means the reader looks at the placeholder for as long as the request
      // takes. Everything further down stays lazy, which is where lazy pays.
      ...(eager ? { fetchPriority: 'high' } : { loading: 'lazy' }),
      // The placeholder paints in the first frame, so a lazy image is a blurred
      // version of itself while it loads rather than a hole in the page.
      //
      // Never behind a cut-out, though: it is a *background*, and under an
      // image with alpha it never goes away — it stays as a blurred copy of the
      // silhouette leaking around every edge. Opaque screenshots cover it
      // completely, which is the whole trick.
      ...(entry.lqip && !entry.alpha
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
    let seen = 0;
    visit(tree, 'element', (node: Element, index, parent) => {
      if (node.tagName !== 'img' || !parent || typeof index !== 'number') return;
      const src = String(node.properties?.src ?? '');
      if (!src.startsWith('/assets/img/')) return;
      const replacement = pictureFor(
        src,
        String(node.properties?.alt ?? ''),
        seen++ === 0,
      );
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

const ADMONITION = /^!!!\s+(\w+)(?:\s+"([^"]*)")?[ \t]*(?:\n|$)/;

function remarkAdmonitions() {
  return (tree: MdRoot) => {
    visit(tree, 'paragraph', (node, index, parent) => {
      if (!parent || typeof index !== 'number') return;
      const first = node.children[0];
      if (first?.type !== 'text') return;
      const m = ADMONITION.exec(first.value);
      if (!m) return;

      const kind = m[1] ?? 'note';
      const title = m[2];

      // The body is the rest of *this* paragraph — the marker line comes off
      // the front of the first text node and every child after it stays where
      // it is. Rebuilding the paragraph from the text alone is what used to
      // strand the links: "Jump straight to the" ended up in one paragraph and
      // the link it was pointing at in the next.
      first.value = first.value.slice(m[0].length);
      visit(node, 'text', (t2) => {
        t2.value = t2.value.replace(/\n {4}/g, '\n');
      });

      const children: MdRoot['children'] = [];
      if (title) {
        children.push({
          type: 'paragraph',
          data: { hName: 'p', hProperties: { className: ['admonition-title'] } },
          children: [{ type: 'text', value: title }],
        });
      }
      children.push(node);

      // A second body paragraph reaches remark as an indented code block: a
      // blank line plus four spaces means "code" everywhere except inside a
      // python-markdown admonition, which is where 22 of these live. Only the
      // blocks directly after the marker are folded back in, so an actual
      // indented snippet elsewhere on the page is untouched.
      let after = index + 1;
      while (
        parent.children[after]?.type === 'code' &&
        !(parent.children[after] as { lang?: string | null }).lang
      ) {
        const block = parent.children[after] as { value: string };
        children.push(...(parseFragment(block.value) as MdRoot['children']));
        after++;
      }
      const absorbed = after - index - 1;

      parent.children.splice(index, 1 + absorbed, {
        type: 'blockquote',
        data: { hName: 'div', hProperties: { className: ['admonition', kind] } },
        children,
      } as MdRoot['children'][number]);
    });
  };
}

/** Re-parses a folded-back admonition paragraph, so its links stay links. */
function parseFragment(md: string): MdRoot['children'] {
  return (unified().use(remarkParse).use(remarkGfm).parse(md) as MdRoot).children;
}

// ── internal links ──────────────────────────────────────────────────────────
//
// The pages were written against the old generator's URLs (/en/quick-start.html)
// and there are hundreds of them. Those addresses still answer — the export
// leaves a stub at each one — but a link that resolves through a redirect is a
// second round-trip on every click, which is precisely what this rebuild is
// about. So they are rewritten to the canonical directory URL as they are
// rendered, and the content keeps saying what it always said.

const INTERNAL = /^\/(en|de)\/([\w-]+)\.html(#.*)?$/;

function rehypeInternalLinks() {
  return (tree: HastRoot) => {
    visit(tree, 'element', (node: Element) => {
      if (node.tagName !== 'a') return;
      const href = String(node.properties?.href ?? '');
      const m = INTERNAL.exec(href);
      if (m) node.properties!.href = `/${m[1]}/${m[2]}/${m[3] ?? ''}`;
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

/** Splits the `---` block off the top of a page.
 *
 * Deliberately not a YAML parser. These files were written against one that
 * split each line on its first colon, so a description reading "Discuss work
 * where it lives: rich comments…" is perfectly ordinary here and is a syntax
 * error to real YAML. There are 108 of them, they hold exactly two keys, and
 * the content is the asset — the generator is what gets replaced.
 */
function frontMatter(source: string): {
  data: { title?: string; description?: string };
  content: string;
} {
  const m = /^---\s*\n([\s\S]*?)\n---\s*\n/.exec(source);
  if (!m) return { data: {}, content: source };
  const data: Record<string, string> = {};
  for (const line of m[1]!.split('\n')) {
    const i = line.indexOf(':');
    if (i < 0) continue;
    data[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { data, content: source.slice(m[0].length) };
}

export async function renderMarkdown(source: string, version: string): Promise<RenderedPage> {
  const { data, content } = frontMatter(source);
  const headings: Heading[] = [];
  const hl = await getHighlighter();

  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkAdmonitions)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
        // `headerlink` is the class the stylesheet hides until the heading is
    // hovered; anything else leaves a permanent # beside every title.
    .use(rehypeAutolinkHeadings, {
      behavior: 'append',
      properties: { className: ['headerlink'], ariaHidden: 'true', tabIndex: -1 },
      content: { type: 'text', value: '#' },
    })
    .use(rehypeInternalLinks)
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
