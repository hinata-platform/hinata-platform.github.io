import Link from 'next/link';

import { Article } from '@/components/Article';
import { Toc } from '@/components/Toc';
import { CodeCopy } from '@/components/CodeCopy';
import { VersionSync } from '@/components/VersionSync';
import {
  LEGAL,
  SITE,
  UI,
  type Lang,
  groupLabel,
  neighbours,
  pageUrl,
  titleOf,
} from '@/lib/content';
import { Icon } from '@/lib/icons';
import { renderMarkdown } from '@/lib/markdown';
import { readSource } from '@/lib/source';
import { latestAppVersion } from '@/lib/version';

/** One documentation page: breadcrumb, article, prev/next, footer, TOC rail.
 *
 * Both routes under [lang] render through here — `/de/` is the page whose slug
 * is `index`, and nothing else about it differs — so the shell exists once.
 */
export async function DocPage({ lang, slug }: { lang: Lang; slug: string }) {
  const ui = UI[lang]!;
  const version = await latestAppVersion();
  const { html, headings } = await renderMarkdown(readSource(lang, slug), version);
  const { prev, next } = neighbours(slug);
  const editUrl = `${SITE.repo_org}/hinata-platform.github.io/edit/main/content/${lang}/${slug}.md`;

  return (
    <main className="content">
      <article className="prose">
        <div className="breadcrumb">
          <Link href={pageUrl(lang, 'index')}>{String(SITE.name)}</Link>
          <span>/</span>
          <span>{groupLabel(slug, lang)}</span>
        </div>
        <div className="page-actions">
          <a className="edit-link" href={editUrl} target="_blank" rel="noopener">
            {ui.edit_page}
          </a>
        </div>
        <Article html={html} />
        <nav className="page-nav" aria-label="Pagination">
          {prev ? (
            <Link className="page-nav-card prev" href={pageUrl(lang, prev.slug)}>
              <Icon name="arrow-left" />
              <span>
                <em>{ui.previous}</em>
                <strong>{titleOf(prev.slug, lang)}</strong>
              </span>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link className="page-nav-card next" href={pageUrl(lang, next.slug)}>
              <span>
                <em>{ui.next}</em>
                <strong>{titleOf(next.slug, lang)}</strong>
              </span>
              <Icon name="arrow-right" />
            </Link>
          ) : null}
        </nav>
        <footer className="page-footer">
          <span>© {new Date().getFullYear()} Hinata · GPL-3.0</span>
          {LEGAL.map((p) => (
            <Link key={p.slug} href={pageUrl(lang, p.slug)}>
              {p.title[lang]}
            </Link>
          ))}
          <a href={String(SITE.repo_org)} target="_blank" rel="noopener">
            GitHub
          </a>
        </footer>
      </article>
      <Toc headings={headings} title={ui.on_this_page!} />
      <CodeCopy deps={`${lang}/${slug}`} copy={ui.copy!} copied={ui.copied!} />
      <VersionSync built={version} />
    </main>
  );
}

/** Head tags for one page — shared by both routes for the same reason. */
export async function docMetadata(lang: Lang, slug: string) {
  const version = await latestAppVersion();
  const { meta } = await renderMarkdown(readSource(lang, slug), version);
  const title = meta.title ?? titleOf(slug, lang);
  const description =
    meta.description ?? (SITE.tagline as Record<string, string>)[lang]!;
  const url = pageUrl(lang, slug);
  const other = lang === 'en' ? 'de' : 'en';
  return {
    title: `${title} · ${String(SITE.name)} Docs`,
    description,
    alternates: {
      canonical: url,
      languages: { [other]: pageUrl(other as Lang, slug) },
    },
    openGraph: {
      type: 'article' as const,
      siteName: `${String(SITE.name)} Documentation`,
      title,
      description,
      url,
    },
    twitter: { card: 'summary_large_image' as const },
  };
}
