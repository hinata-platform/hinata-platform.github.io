import type { Metadata, Viewport } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';

import { SITE } from '@/lib/content';

import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const mono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE.base_url as string),
  icons: { icon: [{ url: '/assets/favicon.svg', type: 'image/svg+xml' }] },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: '#151327',
};

/** Paints the stored theme onto <html> before the first frame.
 *
 * It has to be an inline, blocking script and it cannot be a React effect: by
 * the time React hydrates, a light page has already been shown to a reader who
 * chose dark. `data-theme` starts empty in the markup and is filled here.
 */
const THEME_SCRIPT = `(function(){try{var t=localStorage.getItem('hinata-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.setAttribute('data-theme',t);}
catch(e){document.documentElement.setAttribute('data-theme','light');}})();`;

/** Sends a reader to the tree in their language, before anything paints.
 *
 * The docs are two URL trees, so "switch language" is a navigation. Three
 * inputs, in order: `?lang=` (what the switch appends — an explicit choice, so
 * it is stored and then wiped from the address bar), the stored choice, and
 * finally the browser's own language. Reading the choice off the URL rather
 * than from a click handler is what makes it race-free: the destination page
 * decides, so a click that lands before any deferred script ran still counts.
 *
 * It derives the page's language from the path instead of being told, which is
 * why it can live in the root head and cover every route: outside /en/ and
 * /de/ — the landing page — it does nothing at all. A redirect can neither loop
 * nor 404, because both trees are built from the same set of pages.
 */
const LANG_SCRIPT = `(function(){try{
var m=/^\\/(en|de)(\\/|$)/.exec(location.pathname); if(!m)return;
var PAGE=m[1], OTHER=PAGE==='en'?'de':'en';
var pref=null, q=new URLSearchParams(location.search).get('lang');
if(q==='en'||q==='de'){pref=q;try{localStorage.setItem('hinata-lang',q);}catch(e){}
 if(history.replaceState)history.replaceState(null,'',location.pathname+location.hash);}
if(!pref){try{pref=localStorage.getItem('hinata-lang');}catch(e){}}
if(!pref)pref=(navigator.language||'en').toLowerCase().indexOf('de')===0?'de':'en';
if(pref!==PAGE&&pref===OTHER)location.replace('/'+OTHER+location.pathname.slice(3)+location.hash);
}catch(e){}})();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" data-theme="" className={`${inter.variable} ${mono.variable}`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_SCRIPT }} />
        <script dangerouslySetInnerHTML={{ __html: LANG_SCRIPT }} />
      </head>
      <body>
        <div className="aurora" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        {children}
      </body>
    </html>
  );
}
