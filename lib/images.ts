import fs from 'node:fs';
import path from 'node:path';

export interface ImageEntry {
  w: number;
  h: number;
  widths: number[];
  lqip?: string;
  alpha?: boolean;
}

/** What tools/optimize_images.py wrote, keyed by the master's filename.
 *
 * Server-only, like lib/source.ts: it reads from disk, so a client component
 * must be handed the entry it needs rather than import this.
 */
export const IMAGE_MANIFEST: Record<string, ImageEntry> = JSON.parse(
  fs.readFileSync(
    path.join(process.cwd(), 'assets', 'img', 'opt', 'manifest.json'),
    'utf8',
  ),
);

export function imageEntry(name: string): ImageEntry | undefined {
  return IMAGE_MANIFEST[name];
}
