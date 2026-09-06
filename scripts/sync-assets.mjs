// Mirrors assets/ into public/ so the export ships it, minus the masters.
//
// The source PNGs are 71 MB and nothing points at one any more: every
// screenshot is served from assets/img/opt as AVIF or WebP. Only the ones the
// optimizer knows about are skipped, so a screenshot added without re-running
// tools/optimize_images.py still reaches the site rather than 404ing.
//
// It is a mirror and not a copy: a file deleted from assets/ is deleted from
// public/ too. Without that, a renamed or removed asset stays in the export
// forever, because nothing else ever looks at that directory. public/ is
// generated and git-ignored — this script owns every byte in it.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const manifestPath = path.join(root, 'assets', 'img', 'opt', 'manifest.json');
const manifest = fs.existsSync(manifestPath)
  ? JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
  : {};

const src = path.join(root, 'assets');
const dest = path.join(root, 'public', 'assets');

let copied = 0;
let removed = 0;

function mirror(from, to, inImgDir) {
  fs.mkdirSync(to, { recursive: true });
  const want = new Set();

  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      want.add(entry.name);
      mirror(path.join(from, entry.name), path.join(to, entry.name), entry.name === 'img');
      continue;
    }
    if (inImgDir && manifest[entry.name]) continue; // a master, superseded
    want.add(entry.name);
    const source = path.join(from, entry.name);
    const target = path.join(to, entry.name);
    const s = fs.statSync(source);
    // Skip what is already there unchanged; the image tree is ~750 files and
    // this runs on every dev start.
    if (fs.existsSync(target)) {
      const d = fs.statSync(target);
      if (d.size === s.size && d.mtimeMs >= s.mtimeMs) continue;
    }
    fs.copyFileSync(source, target);
    copied++;
  }

  for (const stale of fs.readdirSync(to)) {
    if (want.has(stale)) continue;
    fs.rmSync(path.join(to, stale), { recursive: true, force: true });
    removed++;
  }
}

mirror(src, dest, false);

// GitHub Pages needs both of these at the root of what is published.
fs.copyFileSync(path.join(root, 'CNAME'), path.join(root, 'public', 'CNAME'));
fs.writeFileSync(path.join(root, 'public', '.nojekyll'), '');

console.log(`assets → public: ${copied} copied, ${removed} removed`);
