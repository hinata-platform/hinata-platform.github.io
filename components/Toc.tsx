'use client';

import { useEffect, useState } from 'react';

import type { Heading } from '@/lib/markdown';

/** The "on this page" rail, with the current section marked as you scroll. */
export function Toc({ headings, title }: { headings: Heading[]; title: string }) {
  const [active, setActive] = useState<string>('');

  useEffect(() => {
    if (!headings.length) return;
    const spy = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      // The band is a sliver just under the top bar: a heading counts as "the
      // one you are reading" the moment it reaches it, and stops counting well
      // before it leaves the screen, so the rail never lags a section behind.
      { rootMargin: '-80px 0px -70% 0px', threshold: 0 },
    );
    for (const h of headings) {
      const el = document.getElementById(h.id);
      if (el) spy.observe(el);
    }
    return () => spy.disconnect();
  }, [headings]);

  if (!headings.length) return <aside className="toc-rail" />;

  return (
    <aside className="toc-rail">
      <div className="toc-inner">
        <p className="toc-title">{title}</p>
        <ul className="toc-list">
          {headings.map((h) => (
            <li key={h.id} className={`toc-l${h.depth}`}>
              <a
                href={`#${h.id}`}
                className={active === h.id ? 'active' : undefined}
              >
                {h.text}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
