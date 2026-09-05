/**
 * Renders the submission PDFs from their editable HTML sources.
 *   submission/src/concept-summary.html → submission/concept-summary.pdf (must be exactly 1 page)
 *   submission/src/blog.html            → submission/blog.pdf
 * Reproduce with: npm run pdfs
 */
import path from 'node:path';
import { existsSync } from 'node:fs';
import { chromium } from 'playwright-core';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const src = (f) => `file://${path.join(root, 'submission', 'src', f)}`;
const out = (f) => path.join(root, 'submission', f);

const browser = await chromium.launch({
  executablePath:
    process.env.CHROMIUM_PATH ?? (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined),
});
const page = await browser.newPage();

for (const [html, pdf] of [
  ['concept-summary.html', 'concept-summary.pdf'],
  ['blog.html', 'blog.pdf'],
]) {
  await page.goto(src(html), { waitUntil: 'networkidle' });
  await page.pdf({ path: out(pdf), format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('rendered', pdf);
}
await browser.close();
