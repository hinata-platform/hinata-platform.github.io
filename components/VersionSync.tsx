'use client';

import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

const CACHE_KEY = 'hinata-app-version';
const TTL = 6 * 60 * 60 * 1000;
const REPO = 'hinata-platform/hinata-app';

/** Keeps the version shown on the page level with the newest hinata-app tag.
 *
 * The build bakes in the version it saw — into the hero pill and into every
 * `{{version}}` the prose and the snippets contain — and that value goes stale
 * the moment the app ships a release, which is days before the docs deploy
 * again. So the page asks GitHub once per six hours and rewrites what it finds.
 *
 * Rewriting the text rather than only the marked-up pill is the point: the
 * places that matter most are inside highlighted code (`HINATA_APP_TAG=…`),
 * where there is nothing to hang an attribute on. Any failure — offline, rate
 * limit — simply leaves the built value standing.
 */
export function VersionSync({ built }: { built: string }) {
  const path = usePathname();

  useEffect(() => {
    let current = built;

    function apply(version: string) {
      if (!version || version === current) return;
      document.querySelectorAll<HTMLElement>('[data-app-version]').forEach((el) => {
        const prefix = el.textContent?.startsWith('v') ? 'v' : '';
        el.textContent = prefix + version;
      });
      replaceInText(current, version);
      current = version;
    }

    const hit = cached();
    if (hit) apply(hit.version);
    if (hit?.fresh) return;

    let alive = true;
    fetch(`https://api.github.com/repos/${REPO}/tags?per_page=100`, {
      headers: { Accept: 'application/vnd.github+json' },
    })
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((tags: Array<{ name?: string }>) => {
        const version = highest(tags ?? []);
        if (!version || !alive) return;
        store(version);
        apply(version);
      })
      .catch(() => {
        /* offline or rate-limited — the built value stands */
      });
    return () => {
      alive = false;
    };
  }, [built, path]);

  return null;
}

function parse(name: string | undefined): number[] | null {
  const m = /^v?(\d+)\.(\d+)\.(\d+)$/.exec(name ?? '');
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
}

function highest(tags: Array<{ name?: string }>): string | null {
  const versions = tags.map((t) => parse(t.name)).filter((v): v is number[] => !!v);
  if (!versions.length) return null;
  versions.sort((a, b) => b[0]! - a[0]! || b[1]! - a[1]! || b[2]! - a[2]!);
  return versions[0]!.join('.');
}

function cached(): { version: string; fresh: boolean } | null {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const entry = JSON.parse(raw) as { v?: string; t?: number };
    if (!entry.v || !parse(entry.v)) return null;
    return { version: entry.v, fresh: Date.now() - (entry.t ?? 0) < TTL };
  } catch {
    return null;
  }
}

function store(version: string) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ v: version, t: Date.now() }));
  } catch {
    /* private mode — just skip the cache */
  }
}

/** Every text node that spells out the old version, code blocks included. */
function replaceInText(from: string, to: string) {
  if (!from) return;
  const escaped = `\\b${from.replace(/\./g, '\\.')}\\b`;
  const pattern = new RegExp(escaped, 'g');
  // A separate, non-global copy: .test() on a /g regex is stateful.
  const probe = new RegExp(escaped);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const tag = node.parentNode?.nodeName;
      if (tag === 'SCRIPT' || tag === 'STYLE') return NodeFilter.FILTER_REJECT;
      return probe.test(node.nodeValue ?? '')
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_REJECT;
    },
  });
  const hits: Node[] = [];
  while (walker.nextNode()) hits.push(walker.currentNode);
  for (const n of hits) n.nodeValue = (n.nodeValue ?? '').replace(pattern, to);
}
