'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import { Icon } from '@/lib/icons';
import {
  FEATURES,
  LANGUAGES,
  LANGUAGE_ANCHOR,
  LINKS,
  MCP_CONNECT,
  QUICKSTART,
  T,
  type Lang,
} from '@/lib/landing';

import { ThemeToggle } from './ThemeToggle';
import { VersionSync } from './VersionSync';

/** The root page. One URL, both languages.
 *
 * It renders English on the server — that is what a crawler and a cold share
 * preview get — and swaps to the reader's language once the browser can say
 * what that is. Doing it the other way round, with a redirect, would make the
 * one link the stores and READMEs point at unshareable.
 */
export function Landing({ version }: { version: string }) {
  const [lang, setLang] = useState<Lang>('en');

  useEffect(() => {
    let pref: string | null = null;
    try {
      pref = localStorage.getItem('hinata-lang');
    } catch {
      /* private mode */
    }
    if (pref !== 'en' && pref !== 'de') {
      pref = navigator.language?.toLowerCase().startsWith('de') ? 'de' : 'en';
    }
    setLang(pref as Lang);
  }, []);

  function choose(next: Lang) {
    setLang(next);
    try {
      localStorage.setItem('hinata-lang', next);
    } catch {
      /* private mode */
    }
  }

  const t = (key: string) => T[key]![lang];
  const docs = (slug: string) => (slug ? `/${lang}/${slug}/` : `/${lang}/`);

  return (
    <>
      <VersionSync built={version} />
      <header className="topbar">
        <div className="topbar-inner glass">
          <Link className="brand" href="/">
            <span className="brand-mark">
              <Icon name="hexagon" />
            </span>
            <span className="brand-name">
              Hinata<em>docs</em>
            </span>
          </Link>
          <nav className="landing-nav">
            <Link href={docs('')}>{t('docs')}</Link>
            <Link href={docs('self-hosting')}>{t('self_host')}</Link>
            <a href={LINKS.org} target="_blank" rel="noopener">
              GitHub
            </a>
          </nav>
          <div className="topbar-actions">
            <button
              className="lang-switch"
              onClick={() => choose(lang === 'en' ? 'de' : 'en')}
              aria-label="Language"
            >
              <span>{lang.toUpperCase()}</span>
            </button>
            <ThemeToggle label="Theme" />
          </div>
        </div>
      </header>

      <main className="landing-main">
        <section className="hero">
          <span className="hero-eyebrow glass">{t('eyebrow')}</span>
          <h1 className="hero-title">
            <span>{t('headline_1')}</span>
            <span className="hero-accent">{t('headline_2')}</span>
          </h1>
          <p className="hero-sub">{t('sub')}</p>
          <div className="hero-cta">
            <Link className="btn btn-primary" href={docs('quick-start')}>
              {t('cta_start')}
            </Link>
            <Link className="btn btn-ghost glass" href={docs('self-hosting')}>
              {t('cta_host')}
            </Link>
          </div>
          <div className="hero-platforms">
            <span>Android</span>
            <i>·</i>
            <span>iOS</span>
            <i>·</i>
            <span>Web</span>
            <i>·</i>
            <span>macOS</span>
            <i>·</i>
            <span>Windows</span>
            <i>·</i>
            <span>Linux</span>
            <span className="ver-pill" data-app-version>
              v{version}
            </span>
          </div>
        </section>

        <div className="hero-shot-wrap">
          <DeviceShot
            className="device device-mac"
            stem="frame-macbook"
            alt="Hinata on desktop — the dashboard shown in a MacBook"
          />
          <DeviceShot
            className="device device-phone"
            stem="frame-iphone"
            alt="Hinata on mobile — the dashboard shown on an iPhone"
          />
        </div>

        <section className="section">
          <div className="section-head">
            <h2>{t('features_title')}</h2>
            <p>{t('features_sub')}</p>
          </div>
          <div className="feat-grid">
            {FEATURES.map((f) => (
              <article className="feat-card glass" key={f.title.en}>
                <div className="feat-emoji">{f.emoji}</div>
                <h3>{f.title[lang]}</h3>
                <p>{f.desc[lang]}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section lang-band">
          <div className="section-head">
            <h2>{t('langs_title')}</h2>
            <p>{t('langs_sub')}</p>
          </div>
          <div className="lang-flags">
            {LANGUAGES.map(([flag, name, code]) => (
              <span className="lang-chip" key={code}>
                <span>{flag}</span>
                <strong>{name}</strong>
                <em>{code}</em>
              </span>
            ))}
          </div>
          <p className="lang-note">{t('langs_note')}</p>
          <p className="lang-note">
            <Link href={docs(LANGUAGE_ANCHOR[lang])}>{t('langs_cta')}</Link>
          </p>
        </section>

        <section className="section">
          <div className="host-split glass">
            <div className="host-copy">
              <h2>{t('host_title')}</h2>
              <p>{t('host_sub')}</p>
              <Link className="btn btn-primary" href={docs('deployment')}>
                {t('host_cta')}
              </Link>
            </div>
            <div className="host-code">
              <CodeWindow code={QUICKSTART} />
            </div>
          </div>
        </section>

        <section className="section">
          <div className="host-split mcp-split glass">
            <div className="host-code">
              <CodeWindow code={MCP_CONNECT} />
            </div>
            <div className="host-copy">
              <span className="mcp-badge">{t('mcp_badge')}</span>
              <h2 className="mcp-title">
                <span>{t('mcp_title_1')}</span>
                <span>{t('mcp_title_2')}</span>
              </h2>
              <p>{t('mcp_sub')}</p>
              <Link className="btn btn-primary" href={docs('mcp')}>
                {t('mcp_cta')}
              </Link>
              <p className="mcp-clients">{t('mcp_clients')}</p>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-head">
            <h2>{t('repos_title')}</h2>
          </div>
          <div className="repo-grid">
            <a className="repo-card glass" href={LINKS.app} target="_blank" rel="noopener">
              <div className="repo-badge">Flutter · Dart</div>
              <h3>hinata-app</h3>
              <p>{t('app_desc')}</p>
              <span className="repo-link">github.com/hinata-platform/hinata-app →</span>
            </a>
            <a className="repo-card glass" href={LINKS.server} target="_blank" rel="noopener">
              <div className="repo-badge">Spring Boot 4 · Java 21</div>
              <h3>hinata-server</h3>
              <p>{t('server_desc')}</p>
              <span className="repo-link">github.com/hinata-platform/hinata-server →</span>
            </a>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <p>© {new Date().getFullYear()} Hinata · Made with 🍯 · GPL-3.0</p>
        <div>
          <Link href={docs('')}>{t('docs')}</Link>
          <a href={LINKS.app} target="_blank" rel="noopener">
            App
          </a>
          <a href={LINKS.server} target="_blank" rel="noopener">
            Server
          </a>
          <Link href={`/${lang}/privacy-policy/`}>{t('privacy')}</Link>
          <Link href={`/${lang}/terms-of-service/`}>{t('terms')}</Link>
        </div>
      </footer>
    </>
  );
}

function CodeWindow({ code }: { code: string }) {
  return (
    <div className="code-window">
      <div className="code-dots">
        <i />
        <i />
        <i />
      </div>
      <pre>
        <code>{code}</code>
      </pre>
    </div>
  );
}

/** A device frame, served from the same AVIF/WebP set the docs images use.
 *
 * These two are the largest files on the site and they sit above the fold, so
 * they are eager, full-viewport-sized and never lazy. The manifest's widths are
 * read at build time by the page that renders this. */
function DeviceShot({
  className,
  stem,
  alt,
}: {
  className: string;
  stem: string;
  alt: string;
}) {
  const srcset = (ext: string) =>
    [480, 960, 1440, 1920]
      .map((w) => `/assets/img/opt/${stem}-${w}.${ext} ${w}w`)
      .join(', ');
  return (
    <picture>
      <source type="image/avif" srcSet={srcset('avif')} sizes="100vw" />
      <source type="image/webp" srcSet={srcset('webp')} sizes="100vw" />
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        className={className}
        src={`/assets/img/opt/${stem}-960.webp`}
        alt={alt}
        fetchPriority="high"
        decoding="async"
      />
    </picture>
  );
}
