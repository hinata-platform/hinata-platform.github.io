import type { MetadataRoute } from 'next';

import { ALL_SLUGS, LANGS, SITE, pageUrl, type Lang } from '@/lib/content';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = String(SITE.base_url);
  const now = new Date();
  return [
    { url: `${base}/`, lastModified: now },
    ...LANGS.flatMap((lang: Lang) =>
      ALL_SLUGS.map((slug) => ({
        url: `${base}${pageUrl(lang, slug)}`,
        lastModified: now,
      })),
    ),
  ];
}
