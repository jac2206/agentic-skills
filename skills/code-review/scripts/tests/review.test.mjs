import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync, symlinkSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import { collectReview, parseStatus, parseDiff, redact } from '../collect.mjs';
import { calculateScore, validateReview, reviewStatus, exportDecisions, importDecisions, commitCommands, checkConventionalMessage, checkCommitlint, DIMENSIONS } from '../model.mjs';
import { renderHtml, writeReport, cleanupReview, prepareReport } from '../report.mjs';
import { gitFixture, fingerprint, sampleReview } from './fixtures.mjs';

test('Quick detects staged, unstaged, both layers, untracked, rename and delete without target writes', () => {
  const head = { 'both.js': 'const n = 1;\n', 'gone.js': 'removed\n', 'old.js': 'unchanged rename content\n', 'work.js': 'old\n' };
  const index = { 'both.js': 'const n = 2;\n', 'renamed.js': head['old.js'], 'work.js': 'old\n' };
  const f = gitFixture({ head, index, worktree: { ...index, 'both.js': 'const n = 3;\n', 'work.js': 'new\n', 'new.js': 'new module\n', '.env': 'SECRET=hidden\n', 'file with spaces.js': 'space\n' } });
  try {
    const before = fingerprint(f.root), s = collectReview({ root: f.root });
    assert.equal(fingerprint(f.root), before);
    assert.deepEqual(s.files.find(x => x.path === 'both.js').diffs.map(d => d.layer), ['staged', 'unstaged']);
    assert.equal(s.files.find(x => x.path === 'gone.js').staged, 'D');
    assert.equal(s.files.find(x => x.path === 'renamed.js').previousPath, 'old.js');
    assert.equal(s.files.find(x => x.path === 'work.js').unstaged, 'M');
    assert.equal(s.files.find(x => x.path === 'new.js').untracked, true);
    assert(s.files.some(x => x.path === 'file with spaces.js'));
    assert(s.omitted.some(x => x.path === '.env'));
    assert(s.files.find(x => x.path === 'gone.js').diffs[0].rows.some(r => r.kind === 'delete' && r.oldLine === 1 && r.newLine === null));
    assert.equal(s.coverage.reviewed, 0);
  } finally { f.close(); }
});

test('PR compares merge-base to head and excludes independent base and dirty changes', () => {
  const f = gitFixture({ base: { 'app.js': 'baseline\n' }, baseExtra: { 'app.js': 'baseline\n', 'base-only.md': 'independent\n' },
    head: { 'app.js': 'feature\n' }, worktree: { 'app.js': 'dirty\n', 'local.js': 'local\n' } });
  try {
    const before = fingerprint(f.root), s = collectReview({ root: f.root, mode: 'pr', base: 'release' });
    assert.equal(fingerprint(f.root), before); assert.equal(s.mergeBase, f.ancestor); assert.notEqual(s.mergeBase, f.baseTip);
    assert.equal(s.base, 'release'); assert.equal(s.branch, 'feature/review'); assert.equal(s.commits.length, 1);
    assert.deepEqual(s.files.map(x => x.path), ['app.js']); assert.equal(s.dirty, true);
    assert(s.files[0].diffs[0].rows.some(r => r.text === 'feature')); assert(!JSON.stringify(s.files).includes('dirty'));
    assert.throws(() => collectReview({ root: f.root, mode: 'pr' }), /base/);
    assert.throws(() => collectReview({ root: f.root, mode: 'pr', base: '--help' }), /Invalid ref/);
    assert.throws(() => collectReview({ root: f.root, mode: 'pr', base: 'missing' }));
  } finally { f.close(); }
});

test('Full audit declares modules, snapshots, byte and count exclusions', () => {
  const f = gitFixture({ head: { 'api/a.js': 'a\n', 'api/b.js': 'b\n', 'web/c.js': 'c\n' } });
  try {
    const s = collectReview({ root: f.root, mode: 'full', modules: ['api'], maxFiles: 1 });
    assert.equal(s.coverage.inventory, 3); assert.equal(s.files.length, 1); assert.equal(s.omitted.length, 2);
    assert.equal(s.files[0].diffs[0].kind, 'snapshot'); assert.equal(s.statistics.snapshot.added, 0);
    assert.equal(collectReview({ root: f.root, mode: 'full', maxBytes: 1 }).files.length, 0);
    assert.throws(() => collectReview({ root: f.root, modules: ['../outside'] }));
  } finally { f.close(); }
});

test('Collector neutralizes fsmonitor and clean/process filter commands', () => {
  const f = gitFixture({ config: '[core]\n fsmonitor = definitely-no-such-command\n[filter "hostile"]\n clean = definitely-no-such-command\n process = definitely-no-such-command\n required = true\n',
    worktree: { 'app.js': 'changed\n', '.gitattributes': '*.js filter=hostile\n' } });
  try { const before = fingerprint(f.root); assert(collectReview({ root: f.root }).files.some(f => f.path === 'app.js')); assert.equal(fingerprint(f.root), before); }
  finally { f.close(); }
});

test('Partial/promisor clones are refused before object access can trigger a lazy fetch', () => {
  const f = gitFixture({ config: '[remote "origin"]\n promisor = true\n url = https://invalid.example/never-contact\n' });
  try {
    const before = fingerprint(f.root); assert.throws(() => collectReview({ root: f.root }), /prevent lazy network access/);
    assert.equal(fingerprint(f.root), before);
  } finally { f.close(); }
});

test('NUL paths, rename records, conflicts and hunk line mapping remain explicit', () => {
  assert.deepEqual(parseStatus('R  new\nname.js\0old name.js\0?? untracked.js\0UU conflict.js\0').map(f => [f.path, f.previousPath, f.conflict]),
    [['new\nname.js', 'old name.js', false], ['untracked.js', null, false], ['conflict.js', null, true]]);
  const rows = parseDiff('@@ -4,2 +5,2 @@\n-old\n+new\n context\n\\ No newline at end of file\n');
  assert.deepEqual(rows.slice(1, 4).map(r => [r.kind, r.oldLine, r.newLine]), [['delete', 4, null], ['add', null, 5], ['context', 5, 6]]);
});

test('Unborn HEAD, unstaged deletion, empty files, binary exclusion and private-key snapshots', () => {
  const f = gitFixture({ head: { 'staged.js': 'new\n', 'deleted.js': 'old\n' }, worktree: {
    'staged.js': 'new\n', 'empty.js': '', 'bytes.bin': 'binary\0data',
    'key-data.txt': '-----BEGIN PRIVATE KEY-----\nconfidential-key-bytes\n-----END PRIVATE KEY-----\n' } });
  try {
    const s = collectReview({ root: f.root });
    assert.equal(s.files.find(f => f.path === 'deleted.js').unstaged, 'D');
    assert.equal(s.files.find(f => f.path === 'empty.js').diffs[0].rows.length, 0);
    assert(s.omitted.some(f => f.path === 'bytes.bin'));
    assert(!JSON.stringify(s).includes('confidential-key-bytes'));
    assert.equal(s.files.find(f => f.path === 'key-data.txt').diffs[0].rows.length, 3);
    unlinkSync(join(f.root, '.git', 'refs', 'heads', 'feature', 'review'));
    const unborn = collectReview({ root: f.root }); assert.equal(unborn.head, null);
    assert.equal(unborn.files.find(f => f.path === 'staged.js').staged, 'A');
  } finally { f.close(); }
});

test('Unmerged index entries are disclosed and excluded from ordinary review diffs', () => {
  const f = gitFixture({ head: { 'app.js': 'base\n' }, worktree: { 'app.js': '<<<<<<< ours\nours\n=======\ntheirs\n>>>>>>> theirs\n' },
    conflicts: { 'app.js': ['base\n', 'ours\n', 'theirs\n'] } });
  try {
    const before = fingerprint(f.root), s = collectReview({ root: f.root });
    assert.equal(s.files.length, 0); assert.match(s.omitted[0].reason, /Unresolved conflict/); assert.equal(fingerprint(f.root), before);
  } finally { f.close(); }
});

test('Redaction covers assignments, service tokens, credentials and multiline private keys preserving lines', () => {
  const source = '+-----BEGIN PRIVATE KEY-----\n+secretbytes\n+-----END PRIVATE KEY-----\n+password = "sensitive"\n+https://person:credential@host.invalid\n+ghp_abcdefghijklmnopqrstuvwxyz';
  const result = redact(source); assert.equal(result.split('\n').length, source.split('\n').length);
  for (const word of ['secretbytes', 'sensitive', 'credential', 'abcdefghijklmnopqrstuvwxyz']) assert(!result.includes(word));
  assert(result.split('\n').every(l => l.startsWith('+')));
});

const rules = () => DIMENSIONS.map((dimension, i) => ({ id: `r${i}`, dimension, title: dimension, source: 'Fixture policy',
  criterion: 'Verify with fixture evidence', state: 'passed', evidence: ['fixture.js:1 observed criterion'] }));

test('Score uses explicit weighted rules and dimensions, excluding N/A and exposing counts', () => {
  const r = rules(); r[2].state = 'failed';
  const s = calculateScore(r); assert.equal(s.score, 80); assert.equal(s.coverage, 100);
  r[5] = { ...r[5], state: 'not-applicable', reason: 'No relevant performance path in scope' };
  assert.equal(calculateScore(r).score, 78.95);
  r.push({ ...r[0], id: 'arch2', state: 'failed', weight: 3 });
  assert.equal(calculateScore(r).dimensions.architecture.score, 25);
  assert.equal(calculateScore(r).dimensions.performance.label, 'Not applicable');
});

test('Unverified rules count against coverage; insufficient/all N/A reviews are Not assessed', () => {
  const r = rules(); r[0] = { ...r[0], state: 'unverified', reason: 'Required evidence unavailable' };
  assert.equal(calculateScore(r).score, null); assert.equal(calculateScore(r).coverage, 80);
  assert.equal(calculateScore(r).dimensions.architecture.counts.unverified, 1);
  assert.equal(calculateScore(r.map(x => ({ ...x, state: 'not-applicable', reason: 'Out of fixture scope' }))).score, null);
  const partial = rules(); partial.push({ ...partial[0], id: 'arch2', state: 'unverified', reason: 'No evidence' });
  assert.equal(calculateScore(partial).score, null);
  assert.equal(calculateScore(partial, { minCoverage: 0.5 }).score, 100);
  assert.throws(() => calculateScore(r, { minCoverage: 0 }), /threshold/);
  assert.throws(() => calculateScore(r, { weights: { ...Object.fromEntries(DIMENSIONS.map(d => [d, 1])) } }), /weights/);
  assert.throws(() => calculateScore([...rules(), rules()[0]]), /Duplicate/);
  assert.throws(() => calculateScore(rules().map(r => ({ ...r, evidence: [] }))), /evidence/);
});

test('Findings require actual collected file/side/lines and complete evidence; Critical blocks independently', () => {
  const { fixture, data } = sampleReview();
  try {
    assert.equal(validateReview(data), data);
    data.findings[0].location.start = 999; assert.throws(() => validateReview(data), /line not present/);
    data.findings[0].location = { layer: 'staged', side: 'old', start: 2 }; assert.equal(validateReview(data), data);
    data.findings[0].severity = 'Critical'; assert.equal(reviewStatus(data).label, 'Blocked');
    data.rules.forEach(r => { r.state = 'passed'; });
    assert.equal(calculateScore(data.rules).score, 100); assert.equal(reviewStatus(data).label, 'Blocked');
    data.findings[0].verification = 'potential'; assert.notEqual(reviewStatus(data).label, 'Blocked');
    data.findings[0].file = 'invented.js'; assert.throws(() => validateReview(data), /file/);
  } finally { fixture.close(); }
});

test('Decisions include identities, all statuses, reasons and paths; reject stale/foreign sets', () => {
  const { fixture, data } = sampleReview();
  try {
    const p = exportDecisions(data, { F1: { status: 'accepted', reason: '' }, F2: { status: 'rejected', reason: 'Already covered by fixture integration case' } });
    assert.deepEqual(importDecisions(data, p), p); assert.deepEqual(p.affectedFiles, ['auth.js']);
    assert.throws(() => exportDecisions(data, { F1: { status: 'rejected', reason: '' } }), /reason/);
    assert.throws(() => importDecisions(data, { ...p, snapshotId: 'stale' }), /foreign/);
    assert.throws(() => importDecisions(data, { ...p, decisions: [p.decisions[0], p.decisions[0]] }), /mismatch/);
    assert.equal(exportDecisions(data, { F1: { status: 'deferred', reason: 'Later' } }).decisions[1].status, 'pending');
  } finally { fixture.close(); }
});

test('Conventional message helper is syntax-only; manual commands use explicit literal paths and shell quoting', () => {
  for (const msg of ['feat(auth): add caller policy', 'fix: check duplicates', 'refactor(db)!: change contract\n\nBREAKING CHANGE: response shape changes']) assert(checkConventionalMessage(msg).valid);
  for (const msg of ['message without type', 'fix(no close: error', 'feat: ', 'fix: title\nbody without blank line']) assert(!checkConventionalMessage(msg).valid);
  assert.match(checkConventionalMessage('fix: a').kind, /not Commitlint/);
  const paths = ["a'b.js", '$(touch bad).js', ':(glob)*.js'];
  assert(commitCommands({ paths, message: "fix: don't execute $(bad)" }).commands[0].includes("'a''b.js'"));
  assert(commitCommands({ paths, message: 'fix: safe', shell: 'posix' }).commands[0].includes("'a'\"'\"'b.js'"));
  assert.throws(() => commitCommands({ paths: ['../outside'], message: 'fix: a' }));
  assert.throws(() => commitCommands({ paths: ['line\nbreak'], message: 'fix: a' }));
});

test('Commitlint adapter forwards resolved rules/parser/plugins/ignores and fails closed on unavailable tools', async () => {
  assert.equal((await checkCommitlint({ message: 'fix: test' })).status, 'not run');
  const config = { rules: { 'type-enum': [2, 'always', ['fix']] }, parserPreset: { parserOpts: { headerPattern: /^(.*)$/ } },
    plugins: { fixture: { rules: {} } }, ignores: [message => message === 'ignored'], defaultIgnores: false };
  let observed;
  // API-contract spy only: it does not establish real Commitlint compatibility.
  const lint = async (...args) => { observed = args; return { valid: false, errors: [{ name: 'type-enum', message: 'Fixture rejection' }], warnings: [] }; };
  const result = await checkCommitlint({ message: 'feat: unsupported type', lint, config, toolEvidence: 'API-contract spy; not installed Commitlint', configEvidence: 'Synthetic resolved configuration' });
  assert.equal(result.status, 'failed'); assert.equal(observed[1], config.rules); assert.equal(observed[2].plugins, config.plugins);
  assert.equal(observed[2].parserOpts, config.parserPreset.parserOpts); assert.equal(observed[2].ignores, config.ignores); assert.equal(observed[2].defaultIgnores, false);
  assert.equal((await checkCommitlint({ message: 'fix: a', lint: async () => { throw new Error('Unavailable parser'); }, config,
    toolEvidence: 'Spy', configEvidence: 'Fixture' })).status, 'not run');
});

test('HTML embeds escaped JSON, hash CSP, inline assets and no source HTML execution', () => {
  const { fixture, data } = sampleReview();
  try {
    const attack = '</script><img src=x onerror="globalThis.pwned=1"> & ${danger}';
    data.findings[0].title = attack; data.findings[0].evidence.push('password = "do-not-leak"');
    const before = fingerprint(fixture.root), html = renderHtml(data);
    assert.equal(fingerprint(fixture.root), before);
    assert(!html.includes(attack)); assert(!html.includes('do-not-leak'));
    assert.match(html, /script-src 'sha256-/); assert.match(html, /connect-src 'none'/);
    assert(!/<(?:link|iframe)\b|<script[^>]+src=|@import|url\(https?:/i.test(html));
    assert(!readFileSync(new URL('../report-ui.js', import.meta.url), 'utf8').includes('innerHTML'));
    const embedded = JSON.parse(html.match(/<script id="review-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
    assert.equal(embedded.findings[0].title, attack); assert.equal(embedded.score.score, 80);
    assert.equal(prepareReport(data).snapshot.coverage.reviewed, 2);
  } finally { fixture.close(); }
});

test('Temporary outputs do not touch target; explicit cleanup verifies ownership, containment and contents', () => {
  const { fixture, data } = sampleReview(); let out, other;
  try {
    const before = fingerprint(fixture.root); out = writeReport(data, { json: true, markdown: true }); other = writeReport(data);
    assert.notEqual(out.directory, other.directory); assert(!out.directory.startsWith(fixture.root));
    assert.equal(fingerprint(fixture.root), before); assert(existsSync(join(out.directory, 'review.json'))); assert(existsSync(join(out.directory, 'review.md')));
    assert.throws(() => cleanupReview(out), /confirmation/);
    assert.throws(() => cleanupReview({ ...out, directory: fixture.root, confirmed: true }), /contained/);
    writeFileSync(join(out.directory, 'foreign.txt'), 'Do not remove');
    assert.throws(() => cleanupReview({ ...out, confirmed: true }), /Unexpected/);
    unlinkSync(join(out.directory, 'foreign.txt'));
    assert.equal(cleanupReview({ ...out, confirmed: true }).verified, true); assert(!existsSync(out.directory)); out = null;
    assert(existsSync(other.report)); assert.equal(fingerprint(fixture.root), before);
  } finally {
    if (out && existsSync(out.directory)) cleanupReview({ ...out, confirmed: true });
    if (other) cleanupReview({ ...other, confirmed: true }); fixture.close();
  }
});

test('Cleanup refuses symlink children when the host permits creating them', t => {
  const { fixture, data } = sampleReview(); const out = writeReport(data); const link = join(out.directory, 'desktop.png');
  try {
    try { symlinkSync(join(fixture.root, 'auth.js'), link); } catch (error) { if (['EPERM', 'EACCES'].includes(error.code)) { t.skip('Host does not permit symlink creation'); return; } throw error; }
    assert.throws(() => cleanupReview({ ...out, confirmed: true }), /Unexpected/); assert(existsSync(join(fixture.root, 'auth.js')));
  } finally { if (existsSync(link)) unlinkSync(link); cleanupReview({ ...out, confirmed: true }); fixture.close(); }
});
