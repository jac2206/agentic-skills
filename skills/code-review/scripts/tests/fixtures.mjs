// Isolated synthetic Git fixtures. Objects, refs and index are authored directly;
// no Git write command or application code is executed by these tests.
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, lstatSync, rmSync, realpathSync } from 'node:fs';
import { join, dirname, relative, isAbsolute, sep } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { deflateSync } from 'node:zlib';
import { collectReview } from '../collect.mjs';
import { DIMENSIONS, commitCommands } from '../model.mjs';

const digest = data => createHash('sha1').update(data).digest();
export function gitFixture({ head = { 'app.js': 'export const value = 1;\n' }, index = head, worktree = index,
  base = head, baseExtra = null, config = '', conflicts = {} } = {}) {
  const root = mkdtempSync(join(realpathSync(tmpdir()), 'code-review-fixture-'));
  const put = (path, data) => { mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, data); };
  mkdirSync(join(root, '.git', 'objects'), { recursive: true });
  const object = (kind, body) => {
    const raw = Buffer.concat([Buffer.from(`${kind} ${body.length}\0`), Buffer.from(body)]), id = digest(raw).toString('hex');
    put(join(root, '.git', 'objects', id.slice(0, 2), id.slice(2)), deflateSync(raw)); return id;
  };
  const tree = files => {
    const entries = {};
    for (const [path, content] of Object.entries(files)) {
      const [name, ...parts] = path.split('/');
      if (parts.length) { entries[name] ||= {}; entries[name][parts.join('/')] = content; }
      else entries[name] = content;
    }
    const records = Object.keys(entries).sort((a, b) => Buffer.compare(Buffer.from(a + (typeof entries[a] === 'object' ? '/' : '')), Buffer.from(b + (typeof entries[b] === 'object' ? '/' : ''))))
      .map(name => {
        const folder = typeof entries[name] === 'object';
        const sha = folder ? tree(entries[name]) : object('blob', Buffer.from(entries[name]));
        return Buffer.concat([Buffer.from(`${folder ? '40000' : '100644'} ${name}\0`), Buffer.from(sha, 'hex')]);
      });
    return object('tree', Buffer.concat(records));
  };
  const commit = (files, parent, message) => object('commit', Buffer.from(`tree ${tree(files)}\n${parent ? `parent ${parent}\n` : ''}author Fixture <fixture@example.invalid> 1700000000 +0000\ncommitter Fixture <fixture@example.invalid> 1700000000 +0000\n\n${message}\n`));
  const ancestor = commit(base, null, 'chore: create fixture baseline');
  const tip = commit(head, ancestor, 'fix(auth): check caller permission');
  const baseTip = baseExtra ? commit(baseExtra, ancestor, 'docs: independent base change') : ancestor;
  put(join(root, '.git', 'HEAD'), 'ref: refs/heads/feature/review\n');
  put(join(root, '.git', 'refs', 'heads', 'feature', 'review'), tip + '\n');
  put(join(root, '.git', 'refs', 'heads', 'release'), baseTip + '\n');
  put(join(root, '.git', 'config'), `[core]\n repositoryformatversion = 0\n bare = false\n filemode = false\n logallrefupdates = false\n${config}`);
  for (const [path, content] of Object.entries(worktree)) put(join(root, path), content);
  const stagedEntries = Object.entries(index).filter(([path]) => !conflicts[path]).map(([path, content]) => ({ path, content, stage: 0 }));
  for (const [path, versions] of Object.entries(conflicts)) versions.forEach((content, i) => stagedEntries.push({ path, content, stage: i + 1 }));
  const header = Buffer.alloc(12); header.write('DIRC'); header.writeUInt32BE(2, 4); header.writeUInt32BE(stagedEntries.length, 8);
  const entries = stagedEntries.sort((a, b) => Buffer.compare(Buffer.from(a.path), Buffer.from(b.path)) || a.stage - b.stage).map(({ path, content, stage }) => {
    const name = Buffer.from(path), entry = Buffer.alloc(Math.ceil((62 + name.length + 1) / 8) * 8);
    entry.writeUInt32BE(0o100644, 24); Buffer.from(object('blob', Buffer.from(content)), 'hex').copy(entry, 40);
    entry.writeUInt16BE((stage << 12) | Math.min(name.length, 0xFFF), 60); name.copy(entry, 62); return entry;
  });
  const contents = Buffer.concat([header, ...entries]); put(join(root, '.git', 'index'), Buffer.concat([contents, digest(contents)]));
  return { root, ancestor, tip, baseTip, put: (path, data) => put(join(root, path), data), close: () => disposeFixture(root) };
}

export function fingerprint(root) {
  const entries = [];
  function walk(folder) {
    for (const name of readdirSync(folder).sort()) {
      const path = join(folder, name), stat = lstatSync(path);
      if (stat.isDirectory()) walk(path);
      else entries.push([relative(root, path), createHash('sha256').update(readFileSync(path)).digest('hex')]);
    }
  }
  walk(root); return JSON.stringify(entries);
}
export function disposeFixture(path) {
  const temp = realpathSync(tmpdir()), rel = relative(temp, path);
  if (!rel.startsWith('code-review-fixture-') || rel.includes(sep) || isAbsolute(rel)) throw new Error('Unsafe fixture disposal');
  rmSync(path, { recursive: true, force: false });
}

export function sampleReview() {
  const fixture = gitFixture({
    head: { 'auth.js': 'export function allowed(user) {\n  return !!user;\n}\n', 'notes.md': '# Review fixture\n' },
    index: { 'auth.js': 'export function allowed(user) {\n  return true;\n}\n', 'notes.md': '# Review fixture\n' },
    worktree: { 'auth.js': 'export function allowed(user) {\n  return true;\n}\n', 'notes.md': '# Review fixture\n', 'new.js': 'export const added = 1;\n' }
  });
  const snapshot = collectReview({ root: fixture.root }); snapshot.files.forEach(f => { f.reviewed = true; });
  const rules = DIMENSIONS.map((dimension, i) => ({ id: `R${i + 1}`, dimension, title: `${dimension} fixture criterion`,
    source: 'Synthetic fixture review policy (test only)', criterion: `Inspect ${dimension} behavior in the fixture scope`,
    state: dimension === 'security' ? 'failed' : 'passed', evidence: ['auth.js staged diff and new.js actual contents inspected in this synthetic scenario'] }));
  const finding = (id, severity, category, ruleId, title, verification = 'confirmed') => ({ id, severity, category, ruleId, title, file: 'auth.js',
    location: { layer: 'staged', side: 'new', start: 2 }, verification, confidence: 'high', origin: 'introduced',
    description: 'The changed permission function returns true for every caller.', evidence: ['auth.js staged new line 2: return true;'],
    impact: 'Unauthenticated callers pass this permission predicate in this synthetic fixture.', recommendation: 'Restore the caller check and cover an absent caller.',
    severityRationale: 'The observed predicate controls access in the isolated fixture scenario.', correction: 'return !!user; // Proposed only; not applied' });
  const data = { schemaVersion: '1.0', snapshot, context: { standards: ['Synthetic fixture policy; not a real backend assessment'], description: 'Illustrative offline report used by deterministic tests.' },
    summary: 'Synthetic fixture: the staged permission check needs correction. No real project has been reviewed.', rules,
    findings: [finding('F1', 'High', 'security', 'R3', 'Permission predicate accepts an absent caller'),
      { ...finding('F2', 'Suggestion', 'testing', 'R4', 'Consider an explicit absent-caller test', 'optional'), location: null }],
    validations: [{ name: 'Fixture source inspection', status: 'passed', kind: 'structural', evidence: 'Synthetic source diff collected; application tests were not run.' }],
    strengths: ['Actual file states and evidence layers are distinguished.'], limitations: ['Synthetic scenario only; backend pilot pending.'], nextSteps: ['Export decisions to Codex.', 'Run a new review after separately authorized corrections.'],
    commitAdvisor: { conventionEvidence: ['Fixture branch commit subjects use Conventional Commits. This does not prove a project policy.'],
      commitlint: { status: 'not run', evidence: 'No Commitlint installation in fixture.' }, groups: [{ type: 'fix', scope: 'auth', description: 'restore caller permission check',
        message: 'fix(auth): restore caller permission check', include: ['auth.js'], exclude: ['new.js — independent change'],
        rationale: 'Separate the permission change from the new module; suggestion requires correction first.',
        manual: commitCommands({ paths: ['auth.js'], message: 'fix(auth): restore caller permission check' }) }] } };
  return { fixture, data };
}
