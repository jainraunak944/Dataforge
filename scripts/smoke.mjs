/**
 * Browser smoke test for the built app (run `npm run build` first).
 *
 * Checks: page loads with zero console errors; the claim and all 7 steps
 * render; moving the ρ slider genuinely changes the displayed numbers to the
 * mathematically expected values (no painted outputs); ρ=1 shows the
 * ambiguity notice; keyboard focus works; reduced-motion is honored; mobile
 * viewport has no horizontal overflow; and control→render feedback is well
 * under one second. Saves desktop + mobile screenshots and a JSON log to
 * artifacts/.
 *
 * Uses the container's preinstalled Chromium unless CHROMIUM_PATH overrides.
 */
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const dist = path.join(root, 'dist');
const artifacts = path.join(root, 'artifacts');
const executablePath =
  process.env.CHROMIUM_PATH ??
  (existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);

const MIME = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.map': 'application/json',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.svg': 'image/svg+xml',
};

function serve(dir) {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      let p = path.join(dir, decodeURIComponent(url.pathname));
      if (url.pathname === '/' || !path.extname(p)) p = path.join(dir, 'index.html');
      const body = await readFile(p);
      res.writeHead(200, { 'content-type': MIME[path.extname(p)] ?? 'application/octet-stream' });
      res.end(body);
    } catch {
      res.writeHead(404);
      res.end('not found');
    }
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

const results = { startedAt: new Date().toISOString(), checks: [], consoleErrors: [] };
function check(name, ok, detail = '') {
  results.checks.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ` — ${detail}` : ''}`);
  if (!ok) process.exitCode = 1;
}

const server = await serve(dist);
const port = server.address().port;
const base = `http://127.0.0.1:${port}/`;
await mkdir(path.join(artifacts, 'screenshots'), { recursive: true });

const browser = await chromium.launch({ executablePath });

// ---------- desktop ----------
{
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on('console', (m) => {
    if (m.type() === 'error') results.consoleErrors.push(m.text());
  });
  page.on('pageerror', (e) => results.consoleErrors.push(String(e)));
  await page.goto(base, { waitUntil: 'networkidle' });

  check('title set', (await page.title()).includes('Memory Under Pressure'));
  check(
    'claim rendered',
    (await page.textContent('.claim')).includes('orthogonal unit keys'),
  );
  const stepHeads = await page.locator('main h2').allTextContents();
  check('all 7 steps + references render', stepHeads.length >= 8, stepHeads.join(' | '));

  // Keyboard: on the freshly loaded page, first Tab reaches the skip link.
  await page.keyboard.press('Tab');
  const focused = await page.evaluate(() => document.activeElement?.className ?? '');
  check('first Tab lands on skip link', focused.includes('skip-link'), focused);

  // No painted values: drive the guided ρ slider and verify the retrieved
  // vector equals the closed form [1, ρ] to displayed precision.
  const slider = page.locator('#step-2 ~ * input[type=range], .panel input[type=range]').first();
  const readRetrievedA = async () =>
    (await page
      .locator('.panel', { hasText: 'One slider' })
      .locator('.vec')
      .nth(1)
      .locator('.cell')
      .allTextContents()) // retrieved column for cue A
      .map(Number);

  await slider.fill('0');
  const at0 = await readRetrievedA();
  check('ρ=0 retrieved A is [1.000, 0.000]', at0[0] === 1 && at0[1] === 0, JSON.stringify(at0));

  const t0 = Date.now();
  await slider.fill('0.37');
  await page.waitForFunction(
    () => document.body.textContent.includes('0.370'),
    { timeout: 2000 },
  );
  const latencyMs = Date.now() - t0;
  const at37 = await readRetrievedA();
  check(
    'ρ=0.37 retrieved A is [1.000, 0.370] (live math, not painted)',
    at37[0] === 1 && Math.abs(at37[1] - 0.37) < 1e-9,
    JSON.stringify(at37),
  );
  check(
    `slider→render feedback under 1s (measured ${latencyMs}ms on this machine; not a device-independent guarantee)`,
    latencyMs < 1000,
  );

  await slider.fill('1');
  check(
    'ρ=1 ambiguity notice shown, reported as tie',
    (await page.locator('.note.warn', { hasText: 'full ambiguity' }).count()) === 1,
  );
  check(
    'ρ=1 outcome stated as a tie, not a winner',
    (await page.locator('.note.warn', { hasText: 'full ambiguity' }).textContent()).includes(
      'reports a tie',
    ),
  );

  // L2 error text present beside desired value; scores labeled as scores.
  check('L2 error shown', (await page.locator('.error-chip').count()) > 0);
  const bodyText = await page.textContent('body');
  check('scores never labeled probabilities', !/probabilit/i.test(bodyText));
  check('honest-label badges present', (await page.locator('.badge').count()) >= 4);
  check(
    'toy-not-BDH disclaimer present',
    bodyText.includes('not an official BDH model'),
  );

  // Quiz determinism: clicking the correct prediction yields "Correct."
  await slider.fill('0.6');
  const quizPanel = page.locator('.panel', { hasText: 'Predict, then see' });
  await quizPanel.locator('button.quiz-option', { hasText: '[1.00, 0.80]' }).click();
  check(
    'quiz reveals computed answer and grades deterministically',
    (await quizPanel.locator('.quiz-feedback.correct').count()) === 1 &&
      (await quizPanel.textContent()).includes('computed now'),
  );

  // Presets reset reproducibly.
  const sandbox = page.locator('.panel', { hasText: 'Sandbox' });
  await sandbox.locator('button', { hasText: 'Identical cues' }).click();
  check(
    'identical-cues preset triggers tie reporting in sandbox',
    (await sandbox.locator('.note.warn', { hasText: 'tie' }).count()) >= 1,
  );
  await sandbox.locator('button', { hasText: 'Orthogonal cues' }).click();
  check(
    'orthogonal preset returns L2 error 0.000',
    (await sandbox.locator('.error-chip.zeroish').count()) === 2,
  );

  // URL hash sharing.
  await slider.fill('0.42');
  await page.waitForFunction(() => location.hash.includes('rho=0.42'));
  check('settings mirrored to URL hash', true);
  const page2 = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page2.goto(`${base}#rho=0.25&lambda=1&repeats=1`, { waitUntil: 'networkidle' });
  check(
    'URL-shared ρ restores state',
    (await page2.textContent('body')).includes('0.250'),
  );
  await page2.close();

  await page.screenshot({
    path: path.join(artifacts, 'screenshots', 'desktop-full.png'),
    fullPage: true,
  });
  await slider.fill('0.6');
  await page.locator('.panel', { hasText: 'One slider' }).screenshot({
    path: path.join(artifacts, 'screenshots', 'desktop-collide.png'),
  });
  await page.close();
}

// ---------- invalid shared-hash regression ----------
// A mistyped or edited share link must render with normalized values, not a
// blank page (regression: "#lambda=2" used to throw RangeError in the first
// render). Every value below derives from the stated public bounds:
// ρ, λ ∈ [0, 1]; repeats capped so retained pairs stay ≤ 64, i.e. 64/2 each.
{
  const MAX_REPEATS = 64 / 2;
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const pageErrors = [];
  page.on('pageerror', (e) => {
    pageErrors.push(String(e));
    results.consoleErrors.push(String(e));
  });
  page.on('console', (m) => {
    if (m.type() === 'error') results.consoleErrors.push(m.text());
  });
  await page.goto(`${base}#rho=7&lambda=2&repeats=500`, { waitUntil: 'networkidle' });

  const stepHeads = await page.locator('main h2').allTextContents();
  check('invalid hash: page renders all lesson content, not a blank page', stepHeads.length >= 8);
  check(
    'invalid hash: no uncaught page errors',
    pageErrors.length === 0,
    pageErrors.slice(0, 2).join(' | '),
  );

  check(
    'invalid hash: guided ρ display normalized to 1.00',
    (await page.getByTestId('guided-rho-value').textContent()).trim() === '1.00',
  );
  check(
    'invalid hash: guided ρ slider holds the normalized value',
    (await page.getByTestId('guided-rho').inputValue()) === '1',
  );
  check(
    'invalid hash: sandbox ρ display normalized to 1.00',
    (await page.getByTestId('sandbox-rho-value').textContent()).trim() === '1.00',
  );
  check(
    'invalid hash: sandbox λ display normalized to 1.00',
    (await page.getByTestId('sandbox-lambda-value').textContent()).trim() === '1.00',
  );
  check(
    'invalid hash: sandbox λ slider holds the normalized value',
    (await page.getByTestId('sandbox-lambda').inputValue()) === '1',
  );
  check(
    `invalid hash: repeats display normalized to ${MAX_REPEATS}×`,
    (await page.getByTestId('sandbox-repeats-value').textContent()).trim() === `${MAX_REPEATS}×`,
  );
  check(
    'invalid hash: repeats slider holds the cap',
    (await page.getByTestId('sandbox-repeats').inputValue()) === String(MAX_REPEATS),
  );

  // Display agrees with computation: 2·MAX_REPEATS writes actually ran, and at
  // ρ = 1, λ = 1 each read returns MAX_REPEATS·[1, 1] (all writes superimpose).
  const sandbox = page.locator('.panel', { hasText: 'Sandbox' });
  check(
    `invalid hash: matrix caption counts ${2 * MAX_REPEATS} computed writes`,
    (await sandbox.locator('.matrix-label', { hasText: `M after ${2 * MAX_REPEATS} writes` }).count()) === 1,
  );
  const retrievedA = (
    await page.getByTestId('sandbox-retrieved-A').locator('.cell').allTextContents()
  ).map(Number);
  check(
    `invalid hash: displayed retrieved A equals computed [${MAX_REPEATS}, ${MAX_REPEATS}]`,
    retrievedA.length === 2 && retrievedA[0] === MAX_REPEATS && retrievedA[1] === MAX_REPEATS,
    JSON.stringify(retrievedA),
  );
  await page.close();
}

// ---------- reduced motion ----------
{
  const page = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    reducedMotion: 'reduce',
  });
  await page.goto(base, { waitUntil: 'networkidle' });
  check(
    'reduced-motion: Play control announces instant mode',
    (await page.textContent('body')).includes('reduced motion'),
  );
  await page.close();
}

// ---------- mobile ----------
{
  const page = await browser.newPage({ viewport: { width: 375, height: 720 } });
  page.on('console', (m) => {
    if (m.type() === 'error') results.consoleErrors.push(m.text());
  });
  await page.goto(base, { waitUntil: 'networkidle' });
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  check('mobile: no horizontal page overflow', overflow <= 1, `overflow ${overflow}px`);
  await page.screenshot({
    path: path.join(artifacts, 'screenshots', 'mobile-top.png'),
  });
  await page.screenshot({
    path: path.join(artifacts, 'screenshots', 'mobile-full.png'),
    fullPage: true,
  });
  await page.close();
}

check('zero console errors across all pages', results.consoleErrors.length === 0,
  results.consoleErrors.slice(0, 3).join(' | '));

await browser.close();
server.close();
results.finishedAt = new Date().toISOString();
await writeFile(path.join(artifacts, 'smoke-results.json'), JSON.stringify(results, null, 2));
console.log(`\n${results.checks.filter((c) => c.ok).length}/${results.checks.length} checks passed; log → artifacts/smoke-results.json`);
