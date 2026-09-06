'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useMemo, useRef, useState } from 'react';

import type { Lang } from '@/lib/content';
import { Icon } from '@/lib/icons';

interface Doc {
  lang: string;
  title: string;
  group: string;
  url: string;
  text: string;
  desc: string;
}

/** ⌘K search over the whole tree of the current language.
 *
 * The index is fetched the first time the palette opens, not on page load: it
 * is ~300 KB of prose and most readers never search. Scoring is the same as the
 * old site's — title hit, prefix, description, body — because it was tuned
 * against these 52 pages and had no complaints.
 */
export function SearchPalette({
  lang,
  open,
  onClose,
  ui,
}: {
  lang: Lang;
  open: boolean;
  onClose: () => void;
  ui: Record<string, string>;
}) {
  const router = useRouter();
  const [index, setIndex] = useState<Doc[] | null>(null);
  const [q, setQ] = useState('');
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    inputRef.current?.focus();
    inputRef.current?.select();
    if (index) return;
    let alive = true;
    fetch('/search-index.json')
      .then((r) => r.json())
      .then((all: Doc[]) => alive && setIndex(all.filter((d) => d.lang === lang)))
      .catch(() => alive && setIndex([]));
    return () => {
      alive = false;
    };
  }, [open, index, lang]);

  const results = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle || !index) return [];
    return index
      .map((d) => {
        const t = d.title.toLowerCase();
        let score = 0;
        if (t.includes(needle)) score += 10;
        if (t.startsWith(needle)) score += 8;
        if ((d.desc || '').toLowerCase().includes(needle)) score += 4;
        if (d.text.toLowerCase().includes(needle)) score += 2;
        return { d, score };
      })
      .filter((s) => s.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 12)
      .map((s) => s.d);
  }, [q, index]);

  useEffect(() => setActive(0), [q]);

  // Keep the highlighted row in view when the arrows walk past the fold.
  useEffect(() => {
    listRef.current
      ?.querySelectorAll('.search-result')
      [active]?.scrollIntoView({ block: 'nearest' });
  }, [active]);

  if (!open) return null;

  function go(d: Doc) {
    onClose();
    router.push(d.url);
  }

  return (
    <div className="search-modal open" aria-hidden="false">
      <div className="search-scrim" onClick={onClose} />
      <div
        className="search-box glass"
        role="dialog"
        aria-modal="true"
        aria-label={ui.search_placeholder}
      >
        <div className="search-field">
          <Icon name="search" />
          <input
            ref={inputRef}
            type="search"
            value={q}
            placeholder={ui.search_placeholder}
            autoComplete="off"
            spellCheck={false}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (results.length) setActive((i) => (i + 1) % results.length);
              } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (results.length)
                  setActive((i) => (i - 1 + results.length) % results.length);
              } else if (e.key === 'Enter' && results[active]) {
                go(results[active]!);
              }
            }}
          />
          <kbd>ESC</kbd>
        </div>
        <div className="search-results" ref={listRef}>
          {!q.trim() ? (
            <p className="search-empty">{ui.search_empty}</p>
          ) : results.length === 0 ? (
            <p className="search-empty">{ui.no_results}</p>
          ) : (
            results.map((d, i) => (
              <a
                key={d.url}
                className={`search-result${i === active ? ' active' : ''}`}
                href={d.url}
                onMouseMove={() => setActive(i)}
                onClick={(e) => {
                  e.preventDefault();
                  go(d);
                }}
              >
                <div className="sr-group">{d.group}</div>
                <div className="sr-title">{d.title}</div>
                <div className="sr-snippet">
                  <Snippet text={pickBody(d, q)} q={q.trim()} />
                </div>
              </a>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function pickBody(d: Doc, q: string): string {
  return (d.text || '').toLowerCase().includes(q.trim().toLowerCase())
    ? d.text
    : d.desc || d.text;
}

/** The matched phrase in context, with the hit marked.
 *
 * Built out of React nodes rather than an HTML string: the text is page prose
 * and the needle is whatever the reader typed, and neither should ever be
 * parsed as markup on its way to the screen.
 */
function Snippet({ text, q }: { text: string; q: string }) {
  const i = text.toLowerCase().indexOf(q.toLowerCase());
  if (i < 0) return <>{text.slice(0, 120)}</>;
  const start = Math.max(0, i - 40);
  return (
    <>
      {start > 0 ? '…' : ''}
      {text.slice(start, i)}
      <mark>{text.slice(i, i + q.length)}</mark>
      {text.slice(i + q.length, i + q.length + 80)}
    </>
  );
}
