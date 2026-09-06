import {
  LANGS,
  NAV,
  pageUrl,
  titleOf,
  type Lang,
} from '@/lib/content';
import { renderMarkdown } from '@/lib/markdown';
import { readSource } from '@/lib/source';
import { latestAppVersion } from '@/lib/version';

/** The ⌘K index: one entry per page per language, built with the pages.
 *
 * It is a route rather than a script so it goes through the same markdown
 * pipeline the pages do — an index built by a second, simpler parser is an
 * index that slowly stops matching what readers can actually see. `force-static`
 * makes the export write it to out/search-index.json.
 */
export const dynamic = 'force-static';

export async function GET() {
  const version = await latestAppVersion();
  const index: Array<Record<string, string>> = [];

  for (const lang of LANGS) {
    for (const group of NAV) {
      for (const page of group.pages) {
        const { html, meta } = await renderMarkdown(
          readSource(lang as Lang, page.slug),
          version,
        );
        const text = plainText(html);
        index.push({
          lang,
          title: meta.title ?? titleOf(page.slug, lang as Lang),
          group: group.label[lang as Lang],
          url: pageUrl(lang as Lang, page.slug),
          text: text.slice(0, 1400),
          desc: (meta.description ?? '').slice(0, 200),
        });
      }
    }
  }

  return Response.json(index);
}

/** Page prose, as a reader would read it aloud.
 *
 * Three things have to come off, and the old generator did none of them: the
 * `#` a heading's permalink leaves behind, the tags, and the entities the
 * serializer wrote — a snippet that says "Boards &#x26; sprints #" is the index
 * showing its working.
 */
const ENTITIES: Record<string, string> = {
  amp: '&',
  lt: '<',
  gt: '>',
  quot: '"',
  apos: "'",
  nbsp: ' ',
};

function plainText(html: string): string {
  return html
    .replace(/<a[^>]*class="[^"]*headerlink[^"]*"[^>]*>.*?<\/a>/g, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&(?:#(\d+)|#[xX]([0-9a-fA-F]+)|([a-zA-Z]+));/g, (m, dec, hex, name) => {
      if (dec) return String.fromCodePoint(Number(dec));
      if (hex) return String.fromCodePoint(parseInt(hex, 16));
      return ENTITIES[name!] ?? m;
    })
    .replace(/\s+/g, ' ')
    .trim();
}
