/** Captures the blog's screenshots from the built app (npm run build first). */
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const dist = path.join(root, 'dist');
const out = path.join(root, 'submission', 'src', 'img');
await mkdir(out, { recursive: true });

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const server = createServer(async (req, res) => {
  try {
    let p = path.join(dist, req.url === '/' ? 'index.html' : decodeURIComponent(req.url.split('?')[0].split('#')[0]));
    if (!path.extname(p)) p = path.join(dist, 'index.html');
    const b = await readFile(p);
    res.writeHead(200, { 'content-type': MIME[path.extname(p)] ?? 'application/octet-stream' });
    res.end(b);
  } catch {
    res.writeHead(404);
    res.end();
  }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await chromium.launch({
  executablePath:
    process.env.CHROMIUM_PATH ?? (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined),
});
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await page.goto(base, { waitUntil: 'networkidle' });

const shots = [
  ['store', 'Two writes into one 2×2 matrix'],
  ['collide', 'One slider'],
  ['crossterm', 'Point at the interference'],
  ['bdh', 'The same write and read inside BDH-GPU'],
  ['sandbox', 'Sandbox'],
];
for (const [name, text] of shots) {
  const panel = page.locator('.panel', { hasText: text }).first();
  await panel.scrollIntoViewIfNeeded();
  await panel.screenshot({ path: path.join(out, `${name}.png`) });
  console.log('captured', name);
}
await browser.close();
server.close();
