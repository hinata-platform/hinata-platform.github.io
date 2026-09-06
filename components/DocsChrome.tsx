'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useCallback, useEffect, useState } from 'react';

import {
  NAV,
  SITE,
  UI,
  type Lang,
  otherLang,
  pageUrl,
} from '@/lib/content';
import { Icon } from '@/lib/icons';

import { SearchPalette } from './SearchPalette';
import { ThemeToggle } from './ThemeToggle';

/** The whole frame around a documentation page: top bar, sidebar, search.
 *
 * These three are one component because they share one piece of state each way
 * — the burger opens the sidebar, ⌘K and the search field open the palette,
 * following a link closes both — and splitting them would mean lifting that
 * state into a context for no gain. The page body itself stays server-rendered
 * and arrives as `children`.
 */
export function DocsChrome({
  lang,
  children,
}: {
  lang: Lang;
  children: React.ReactNode;
}) {
  const ui = UI[lang]!;
  const other = otherLang(lang);
  const path = usePathname();
  const [navOpen, setNavOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  // A link inside the drawer navigates *and* has to shut it; on desktop the
  // drawer is not a drawer, so closing is a no-op there.
  useEffect(() => setNavOpen(false), [path]);

  const openSearch = useCallback(() => setSearchOpen(true), []);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const typing =
        document.activeElement instanceof HTMLElement &&
        ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName);
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen((v) => !v);
      } else if (e.key === 'Escape') {
        setSearchOpen(false);
        setNavOpen(false);
      } else if (e.key === '/' && !typing) {
        e.preventDefault();
        setSearchOpen(true);
      }
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  // The language switch is a navigation between two URL trees, not a class on
  // <html>. `?lang=` tells the destination that this was a deliberate choice —
  // LangGate stores it and wipes the query — so the preference follows the
  // reader to every other page.
  const otherHref = `${swapLang(path, lang, other)}?lang=${other}`;

  return (
    <>
      <header className="topbar">
        <div className="topbar-inner glass">
          <button
            className="icon-btn menu-toggle"
            onClick={() => setNavOpen((v) => !v)}
            aria-label={ui.menu}
            aria-expanded={navOpen}
          >
            <Icon name="menu" />
          </button>
          <Link className="brand" href="/">
            <span className="brand-mark">
              <Icon name="hexagon" className="brand-hex" />
            </span>
            <span className="brand-name">
              {String(SITE.name)}
              <em>docs</em>
            </span>
          </Link>
          <button
            className="search-trigger"
            onClick={openSearch}
            aria-label={ui.search_placeholder}
          >
            <Icon name="search" />
            <span>{ui.search_hint}</span>
            <kbd>⌘K</kbd>
          </button>
          <div className="topbar-actions">
            <a
              className="lang-switch"
              href={otherHref}
              title={other.toUpperCase()}
              aria-label={ui.language}
            >
              <Icon name="languages" />
              <span>{lang.toUpperCase()}</span>
            </a>
            <ThemeToggle label={ui.theme} />
            <a
              className="icon-btn"
              href={String(SITE.repo_org)}
              target="_blank"
              rel="noopener"
              aria-label="GitHub"
            >
              <Icon name="github" />
            </a>
          </div>
        </div>
      </header>

      <div className="layout">
        <aside className={`sidebar${navOpen ? ' open' : ''}`}>
          <div className="sidebar-inner glass">
            <SidebarTree lang={lang} />
          </div>
        </aside>
        <div
          className={`sidebar-scrim${navOpen ? ' open' : ''}`}
          onClick={() => setNavOpen(false)}
        />
        {children}
      </div>

      <SearchPalette
        lang={lang}
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        ui={ui}
      />
    </>
  );
}

function SidebarTree({ lang }: { lang: Lang }) {
  const path = usePathname();
  return (
    <nav className="nav-tree" aria-label="Docs">
      {NAV.map((group) => (
        <div className="nav-group" key={group.id}>
          <div className="nav-group-label">
            {group.icon ? <Icon name={group.icon} className="nav-group-icon" /> : null}
            <span>{group.label[lang]}</span>
          </div>
          <ul className="nav-links">
            {group.pages.map((p) => {
              const href = pageUrl(lang, p.slug);
              const active = path === href || `${path}/` === href;
              return (
                <li key={p.slug}>
                  <Link
                    className={`nav-link${active ? ' active' : ''}`}
                    aria-current={active ? 'page' : undefined}
                    href={href}
                  >
                    {p.title[lang]}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}

/** The same page in the other language: only the language segment changes. */
function swapLang(path: string, from: Lang, to: Lang): string {
  if (path.startsWith(`/${from}/`) || path === `/${from}`) {
    return `/${to}${path.slice(from.length + 1)}` || `/${to}/`;
  }
  return `/${to}/`;
}
