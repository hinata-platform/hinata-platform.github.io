import navData from '@/content/nav.json';

export type Lang = 'en' | 'de';
export const LANGS: Lang[] = ['en', 'de'];

type Localised = Record<Lang, string>;

export interface NavPage {
  slug: string;
  title: Localised;
}

export interface NavGroup {
  id: string;
  label: Localised;
  icon?: string;
  pages: NavPage[];
}

/** nav.json is the site's structure, exported once from the Python generator
 * this replaced and now edited directly; these types narrow it. */
const raw = navData as unknown as {
  site: Record<string, unknown>;
  ui: Record<string, Record<string, string>>;
  nav: Array<{
    id: string;
    label: Localised;
    icon?: string;
    pages: Array<[string, Localised]>;
  }>;
  legal: Array<[string, Localised]>;
  appRepo: string;
};

export const SITE = raw.site;
export const UI = raw.ui;
export const APP_REPO = raw.appRepo;

export const NAV: NavGroup[] = raw.nav.map((g) => ({
  id: g.id,
  label: g.label,
  icon: g.icon,
  pages: g.pages.map(([slug, title]) => ({ slug, title })),
}));

export const LEGAL: NavPage[] = raw.legal.map(([slug, title]) => ({ slug, title }));

/** Every documentation page, in sidebar order — which is also prev/next order. */
export const PAGES: NavPage[] = NAV.flatMap((g) => g.pages);

export const ALL_SLUGS = [...PAGES, ...LEGAL].map((p) => p.slug);

/** The group a page belongs to, for the breadcrumb and the sidebar's open state. */
export function groupOf(slug: string): NavGroup | undefined {
  return NAV.find((g) => g.pages.some((p) => p.slug === slug));
}

/** The pages either side of this one, for the footer's prev/next pair. */
export function neighbours(slug: string): { prev?: NavPage; next?: NavPage } {
  const i = PAGES.findIndex((p) => p.slug === slug);
  if (i < 0) return {};
  return { prev: PAGES[i - 1], next: PAGES[i + 1] };
}

export function titleOf(slug: string, lang: Lang): string {
  return [...PAGES, ...LEGAL].find((p) => p.slug === slug)?.title[lang] ?? slug;
}

/** Canonical URL of a page.
 *
 * `trailingSlash: true`, so every route is a directory with an index.html —
 * which is the only shape GitHub Pages serves without a rewrite layer. The old
 * generator wrote `/en/features.html`; those URLs are kept alive by the stubs
 * scripts/legacy-urls.mjs writes after the export, because they are in the
 * store listings, in the apps and in other people's bookmarks.
 */
export function pageUrl(lang: Lang, slug: string): string {
  return slug === 'index' ? `/${lang}/` : `/${lang}/${slug}/`;
}

export function otherLang(lang: Lang): Lang {
  return lang === 'en' ? 'de' : 'en';
}

/** The label above a page in the breadcrumb — its nav group, or "Legal". */
export function groupLabel(slug: string, lang: Lang): string {
  const g = groupOf(slug);
  if (g) return g.label[lang];
  if (LEGAL.some((p) => p.slug === slug)) return lang === 'de' ? 'Rechtliches' : 'Legal';
  return '';
}
