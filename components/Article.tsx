'use client';

import { useRouter } from 'next/navigation';

/** The rendered page body, with its internal links routed client-side.
 *
 * The body is HTML from the markdown pipeline, so its links are plain anchors
 * and every one of them would be a full document load — the docs' own
 * cross-references are the most-followed links on the site. One delegated
 * click handler turns them into the same client transition the sidebar makes,
 * while leaving modified clicks, new tabs and external links to the browser.
 */
export function Article({ html }: { html: string }) {
  const router = useRouter();

  return (
    <div
      onClick={(e) => {
        if (e.defaultPrevented || e.button !== 0) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        const a = (e.target as HTMLElement).closest('a');
        if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
        const href = a.getAttribute('href');
        // Same-document anchors keep the browser's own scroll and history.
        if (!href?.startsWith('/') ) return;
        e.preventDefault();
        router.push(href);
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
