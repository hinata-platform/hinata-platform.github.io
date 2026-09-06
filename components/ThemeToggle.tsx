'use client';

import { Icon } from '@/lib/icons';

/** Flips light/dark and remembers the choice.
 *
 * There is no React state behind it on purpose: the attribute on <html> is the
 * source of truth, it is set by the blocking script in the head before the
 * first paint, and holding a copy in state would only give the two a chance to
 * disagree across a hydration.
 */
export function ThemeToggle({ label }: { label: string }) {
  return (
    <button
      className="icon-btn theme-toggle"
      aria-label={label}
      onClick={() => {
        const root = document.documentElement;
        const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try {
          localStorage.setItem('hinata-theme', next);
        } catch {
          /* private mode — the choice just doesn't outlive the tab */
        }
      }}
    >
      <Icon name="sun" className="icon-sun" />
      <Icon name="moon" className="icon-moon" />
    </button>
  );
}
