import fs from 'node:fs';
import path from 'node:path';

import type { Lang } from './content';

/** Reads a page's Markdown.
 *
 * It sits apart from lib/content.ts because that module is imported by the
 * sidebar and the landing page, which are client components: a single
 * `node:fs` import anywhere in their graph fails the build outright. Everything
 * derived from nav.json is shared; touching the filesystem is not.
 */
export function readSource(lang: Lang, slug: string): string {
  return fs.readFileSync(
    path.join(process.cwd(), 'content', lang, `${slug}.md`),
    'utf8',
  );
}
