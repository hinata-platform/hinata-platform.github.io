/** @type {import('next').NextConfig} */
const nextConfig = {
  // GitHub Pages serves files, not a Node server, so the whole site is
  // pre-rendered to `out/`. Everything below follows from that.
  output: 'export',

  // `next/image`'s optimizer needs that server. With `output: export` it cannot
  // run, so images would be served exactly as authored — which is the bug this
  // rebuild started with. The markdown pipeline emits its own <picture> over
  // the AVIF/WebP variants tools/optimize_images.py wrote, with the 48px
  // placeholder from its manifest.
  images: { unoptimized: true },

  // Pages has no rewrite layer, so every route is a directory with an
  // index.html. Without this, /de/features would 404 unless the visitor typed
  // the .html themselves.
  trailingSlash: true,

  // `next dev` otherwise writes AGENTS.md and CLAUDE.md into the repository
  // root on every start. This is a public docs repo; agent instructions for
  // whoever is working on it do not belong in what it publishes.
  agentRules: false,
};

export default nextConfig;
