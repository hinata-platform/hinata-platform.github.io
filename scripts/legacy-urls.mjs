// Post-export fix-ups that Next cannot express, run against out/.
//
// 1. `lang` on <html>. The root layout owns that attribute and knows nothing
//    about the route, so every page ships lang="en". The German tree is a
//    whole second site and has to say so — to screen readers, to hyphenation,
//    and to search engines. Rewriting it here is exact and needs no runtime.
//
// 2. The old .html URLs. The generator this replaces wrote /en/features.html,
//    and those URLs are in the store listings, in the apps, in other people's
//    links. Each one becomes a stub that redirects to the new directory URL —
//    canonical tag included, so the duplicate never competes in search.
import fs from 'node:fs';
import path from 'node:path';

const out = path.join(process.cwd(), 'out');
if (!fs.existsSync(out)) {
  console.error('out/ not found — run `next build` first');
  process.exit(1);
}

let relabelled = 0;
let stubs = 0;

function walk(dir, lang) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, lang ?? (['en', 'de'].includes(entry.name) ? entry.name : undefined));
      // /en/features/index.html also answers at /en/features.html
      if (lang && entry.name !== '_next') {
        const index = path.join(full, 'index.html');
        if (fs.existsSync(index)) {
          fs.writeFileSync(`${full}.html`, redirect(`/${lang}/${entry.name}/`));
          stubs++;
        }
      }
    } else if (lang && entry.name === 'index.html') {
      const html = fs.readFileSync(full, 'utf8');
      if (lang !== 'en') {
        fs.writeFileSync(full, html.replace(/<html lang="en"/, `<html lang="${lang}"`));
        relabelled++;
      }
    }
  }
}

function redirect(to) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Hinata Docs</title>
<link rel="canonical" href="${to}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=${to}">
<script>location.replace('${to}' + location.hash);</script>
</head><body><p><a href="${to}">${to}</a></p></body></html>
`;
}

for (const lang of ['en', 'de']) {
  const dir = path.join(out, lang);
  if (fs.existsSync(dir)) walk(dir, lang);
}

console.log(`legacy URLs: ${stubs} stub(s) · ${relabelled} page(s) relabelled de`);
