/** The version number shown in the chrome and substituted for `{{version}}`.
 *
 * Nothing in this repository writes it down: it is the highest vX.Y.Z tag on
 * hinata-app, resolved from the GitHub API while the site builds — the same
 * rule the previous generator used, kept because it cannot go stale.
 * The tags endpoint is not ordered by semver, so this pages through and takes
 * the maximum instead of trusting the first entry, and a failure aborts the
 * build rather than inventing a number.
 */
const REPO = 'hinata-platform/hinata-app';

async function tagPage(page: number): Promise<Array<{ name?: string }>> {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/tags?per_page=100&page=${page}`,
    {
      headers: {
        Accept: 'application/vnd.github+json',
        ...(process.env.GITHUB_TOKEN
          ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` }
          : {}),
      },
      // Build-time only, but Next caches fetches across the export; one call is
      // enough for 216 pages.
      cache: 'force-cache',
    },
  );
  if (!res.ok) throw new Error(`GitHub tags: ${res.status} ${res.statusText}`);
  return res.json();
}

let cached: string | undefined;

export async function latestAppVersion(): Promise<string> {
  if (cached) return cached;
  const versions: number[][] = [];
  for (let page = 1; page <= 3; page++) {
    const tags = await tagPage(page);
    for (const t of tags) {
      const m = /^v(\d+)\.(\d+)\.(\d+)$/.exec(t.name ?? '');
      if (m) versions.push([Number(m[1]), Number(m[2]), Number(m[3])]);
    }
    if (tags.length < 100) break;
  }
  if (!versions.length) throw new Error(`no vX.Y.Z tags found on ${REPO}`);
  versions.sort((a, b) => b[0]! - a[0]! || b[1]! - a[1]! || b[2]! - a[2]!);
  cached = versions[0]!.join('.');
  return cached;
}
