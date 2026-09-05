/**
 * Regenerates submission/manifest.json: deliverable paths, SHA-256 checksums,
 * completion status, and the source commit at generation time (the manifest
 * therefore describes the tree as of that commit; committing the manifest
 * creates the next commit — recorded in the field's note).
 */
import { createHash } from 'node:crypto';
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

const deliverables = [
  ['app', 'index.html'],
  ['app', 'src/App.tsx'],
  ['app', 'src/memory/additiveMemory.ts'],
  ['app', 'src/memory/reference.ts'],
  ['app', 'src/memory/session.ts'],
  ['tests', 'tests/memory.test.ts'],
  ['tests', 'tests/session.test.ts'],
  ['tests', 'artifacts/smoke-results.json'],
  ['docs', 'README.md'],
  ['docs', 'docs/CLAIM.md'],
  ['docs', 'docs/REQUIREMENTS.md'],
  ['docs', 'docs/RESEARCH.md'],
  ['docs', 'docs/ARCHITECTURE.md'],
  ['docs', 'docs/LEARNER_TEST.md'],
  ['docs', 'docs/PROVENANCE.md'],
  ['docs', 'docs/AI_DISCLOSURE.md'],
  ['docs', 'docs/DEFENSE_GUIDE.md'],
  ['docs', 'docs/DEMO_SCRIPT.md'],
  ['submission', 'submission/concept-summary.pdf'],
  ['submission', 'submission/src/concept-summary.html'],
  ['submission', 'submission/blog.pdf'],
  ['submission', 'submission/src/blog.html'],
  ['submission', 'submission/SUBMISSION_CHECKLIST.md'],
  ['meta', 'LICENSE'],
  ['meta', 'package-lock.json'],
];

const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const git = (cmd) => execSync(`git ${cmd}`, { cwd: root }).toString().trim();

const files = deliverables.map(([category, rel]) => {
  const abs = path.join(root, rel);
  return existsSync(abs)
    ? { category, path: rel, sha256: sha256(abs), status: 'present' }
    : { category, path: rel, status: 'MISSING' };
});

const manifest = {
  project: 'Memory Under Pressure — DataForge 2026 Pathway track',
  generatedAt: new Date().toISOString(),
  sourceCommit: git('rev-parse HEAD'),
  sourceCommitNote:
    'Commit at manifest generation; the commit that adds/updates this manifest is its child.',
  branch: git('rev-parse --abbrev-ref HEAD'),
  completion: {
    built: true,
    verifiedLocally: 'see submission/SUBMISSION_CHECKLIST.md for the per-check record',
    publicUrls: 'see SUBMISSION_CHECKLIST.md — external gates listed there; none claimed here',
  },
  files,
};

writeFileSync(path.join(root, 'submission', 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
const missing = files.filter((f) => f.status === 'MISSING');
console.log(`manifest.json written; ${files.length - missing.length}/${files.length} present`);
if (missing.length) {
  console.log('MISSING:', missing.map((m) => m.path).join(', '));
  process.exitCode = 1;
}
