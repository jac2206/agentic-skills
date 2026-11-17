// Read-only evidence collector. No command-line interface or repository code execution.
import { execFileSync } from 'node:child_process';
import { lstatSync, readFileSync, realpathSync } from 'node:fs';
import { resolve, relative, isAbsolute, sep } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';

const MAX_BYTES = 200_000;
const OMIT = /(^|\/)(?:\.git|node_modules|vendor|dist|build|coverage)(\/|$)|(^|\/)(?:\.env(?:\..*)?|id_rsa|id_ed25519|credentials(?:\..*)?|[^/]+\.(?:pem|key|p12|pfx))$/i;
export function redact(value) {
  let privateKey = false;
  return String(value).split('\n').map(line => {
    if (/-----BEGIN [^-]*PRIVATE KEY-----/.test(line)) privateKey = true;
    if (!privateKey) return line;
    if (/-----END [^-]*PRIVATE KEY-----/.test(line)) privateKey = false;
    return (/^[+ -]/.test(line) ? line[0] : '') + '[REDACTED PRIVATE KEY]';
  }).join('\n')
    .replace(/((?:password|passwd|secret|token|api[_-]?key|authorization)\s*["']?\s*[:=]\s*)([^\r\n]+)/gi, '$1[REDACTED]')
    .replace(/\b(?:gh[pousr]_[A-Za-z0-9_]{15,}|github_pat_[A-Za-z0-9_]{15,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b/g, '[REDACTED TOKEN]')
    .replace(/(https?:\/\/)[^\s/@:]+:[^\s/@]+@/gi, '$1[REDACTED]@');
}

function inside(root, path) {
  const rel = relative(root, path);
  return rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel);
}

export function parseStatus(raw) {
  const records = raw.split('\0');
  const files = [];
  for (let i = 0; i < records.length; i++) {
    if (!records[i]) continue;
    const x = records[i][0], y = records[i][1], path = records[i].slice(3);
    const previousPath = /[RC]/.test(x + y) ? records[++i] : null;
    files.push({ path, previousPath, staged: x === '?' || x === ' ' ? null : x,
      unstaged: y === '?' || y === ' ' ? null : y, untracked: x === '?',
      conflict: /U/.test(x + y) || ['AA', 'DD'].includes(x + y) });
  }
  return files;
}

export function parseNames(raw) {
  const parts = raw.split('\0'), files = [];
  for (let i = 0; i < parts.length && parts[i];) {
    const status = parts[i++];
    const previousPath = /^[RC]/.test(status) ? parts[i++] : null;
    files.push({ path: parts[i++], previousPath, status: status[0] });
  }
  return files;
}

export function parseDiff(patch) {
  const rows = [];
  let oldLine = 0, newLine = 0, active = false;
  for (const text of patch.split('\n')) {
    const header = /^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/.exec(text);
    if (header) {
      oldLine = Number(header[1]); newLine = Number(header[2]); active = true;
      rows.push({ kind: 'hunk', text, oldLine: null, newLine: null });
    } else if (active && text[0] === '+') {
      rows.push({ kind: 'add', text: text.slice(1), oldLine: null, newLine: newLine++ });
    } else if (active && text[0] === '-') {
      rows.push({ kind: 'delete', text: text.slice(1), oldLine: oldLine++, newLine: null });
    } else if (active && text[0] === ' ') {
      rows.push({ kind: 'context', text: text.slice(1), oldLine: oldLine++, newLine: newLine++ });
    } else if (active && text.startsWith('\\ No newline')) {
      rows.push({ kind: 'note', text, oldLine: null, newLine: null });
    } else if (text.startsWith('diff --git ')) active = false;
  }
  return rows;
}

export function collectReview({ root, mode = 'quick', base, head = 'HEAD', modules = [],
  exclude = [], maxFiles = 500, maxBytes = MAX_BYTES } = {}) {
  if (!['quick', 'pr', 'full'].includes(mode)) throw new Error('Unknown review mode');
  if (!Number.isInteger(maxFiles) || maxFiles < 1 || !Number.isInteger(maxBytes) || maxBytes < 1)
    throw new Error('Positive collection bounds required');
  const target = realpathSync(root);
  const gitEnvironment = { ...process.env, GIT_OPTIONAL_LOCKS: '0', GIT_NO_LAZY_FETCH: '1', GIT_PAGER: 'cat', GIT_TERMINAL_PROMPT: '0' };
  const disabledFilters = [];
  const git = (...args) => execFileSync('git', ['--no-pager', '--literal-pathspecs', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false', ...disabledFilters, '-C', target, ...args], {
    encoding: 'utf8', maxBuffer: 8_000_000, timeout: 30_000,
    env: gitEnvironment,
    windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  const optional = (...args) => { try { return git(...args).trim(); } catch { return null; } };
  // Older Git versions ignore GIT_NO_LAZY_FETCH. Reject promisor/partial clones
  // before resolving objects so a read cannot silently contact a remote service.
  if (optional('config', '--get-regexp', '^(extensions\\.partialclone|remote\\..*\\.promisor)$'))
    throw new Error('Partial/promisor clone requires complete local evidence; automatic collection refused to prevent lazy network access');
  // Status may invoke clean/process filters when hashing files; disable configured
  // filters before any index/worktree inspection. Config enumeration executes none.
  const filterKeys = optional('config', '--name-only', '--get-regexp', '^filter\\..*\\.(clean|process|required)$');
  for (const key of filterKeys?.split(/\r?\n/) || []) disabledFilters.push('-c', `${key}=${key.endsWith('.required') ? 'false' : ''}`);
  const actualRoot = realpathSync(git('rev-parse', '--show-toplevel').trim());
  if (actualRoot !== target) throw new Error('Use the repository root, not a nested working directory');
  const resolveCommit = ref => {
    if (typeof ref !== 'string' || !ref || ref.startsWith('-')) throw new Error('Invalid ref');
    return git('rev-parse', '--verify', '--end-of-options', `${ref}^{commit}`).trim();
  };
  const headSha = optional('rev-parse', '--verify', 'HEAD');
  const branch = optional('symbolic-ref', '--short', 'HEAD') || '(detached HEAD)';
  const statusRaw = git('status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=all');
  const limits = [], omitted = [];
  const underModule = path => !modules.length || modules.some(m => path === m || path.startsWith(`${m.replace(/\/$/, '')}/`));
  for (const m of [...modules, ...exclude]) {
    if (typeof m !== 'string' || !m || isAbsolute(m) || m.split(/[\\/]/).includes('..'))
      throw new Error('Module/exclusion paths must be repository-relative');
  }
  const reasonFor = path => {
    if (!underModule(path)) return 'Outside selected modules';
    if (OMIT.test(path) || exclude.some(e => path === e || path.startsWith(`${e.replace(/\/$/, '')}/`)))
      return 'Sensitive, generated, vendor or explicitly excluded path';
    const location = resolve(target, path);
    if (!inside(target, location)) return 'Path outside target';
    // Check each existing ancestor; never follow symlinks/junctions, even on a deleted leaf.
    let cursor = target;
    for (const part of relative(target, location).split(sep)) {
      cursor = resolve(cursor, part);
      try {
        const stat = lstatSync(cursor);
        if (stat.isSymbolicLink()) return 'Symlink or junction';
        if (cursor === location && !stat.isFile()) return 'Non-file or submodule';
        if (cursor === location && stat.size > maxBytes) return 'File exceeds byte limit';
      } catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
    return null;
  };
  let candidates, mergeBase = null, resolvedHead = headSha, commits = [];
  if (mode === 'pr') {
    if (!base) throw new Error('PR review requires a resolved base ref');
    const baseSha = resolveCommit(base); resolvedHead = resolveCommit(head);
    const bases = git('merge-base', '--all', baseSha, resolvedHead).trim().split(/\r?\n/);
    if (bases.length !== 1 || !bases[0]) throw new Error('No unique merge-base');
    mergeBase = bases[0];
    candidates = parseNames(git('diff', '--no-ext-diff', '--no-textconv', '--find-renames', '--name-status', '-z', mergeBase, resolvedHead));
    const logs = git('log', '--format=%H%x00%s%x00', `${mergeBase}..${resolvedHead}`).split('\0');
    for (let i = 0; i + 1 < logs.length; i += 2)
      if (logs[i].trim()) commits.push({ sha: logs[i].trim(), subject: redact(logs[i + 1]) });
  } else if (mode === 'quick') candidates = parseStatus(statusRaw);
  else candidates = [...new Set(git('ls-files', '-z', '--cached', '--others', '--exclude-standard').split('\0').filter(Boolean))]
    .map(path => ({ path, status: 'snapshot' }));

  const files = [];
  for (const candidate of candidates) {
    const file = { ...candidate, id: `f-${createHash('sha256').update(candidate.path).digest('hex').slice(0, 16)}`, diffs: [], reviewed: false };
    const reason = reasonFor(file.path) || (file.previousPath && reasonFor(file.previousPath)) ||
      (file.conflict ? 'Unresolved conflict; inspect manually without combining diff' : null);
    if (reason || files.length >= maxFiles) {
      omitted.push({ path: file.path, reason: reason || 'File count limit' }); continue;
    }
    try {
      const paths = file.previousPath ? [file.previousPath, file.path] : [file.path];
      const diff = (layer, refs = [], cached = false) => {
        const patch = git('diff', '--no-ext-diff', '--no-textconv', '--no-color', '--ignore-submodules=all', '--find-renames', '--unified=3',
          ...(cached ? ['--cached'] : []), ...refs, '--', ...paths);
        if (Buffer.byteLength(patch) > maxBytes) { limits.push(`${file.path} ${layer}: diff exceeds byte limit`); return; }
        const rows = parseDiff(redact(patch));
        file.diffs.push({ layer, kind: 'diff', rows,
          note: /Binary files|GIT binary patch/.test(patch) ? 'Binary diff omitted' : rows.length ? '' : 'Metadata-only or no textual changes' });
      };
      if (mode === 'pr') diff('pr', [mergeBase, resolvedHead]);
      else if (mode === 'quick' && !file.untracked) {
        if (file.staged) diff('staged', [], true);
        if (file.unstaged) diff('unstaged');
      } else {
        const content = readFileSync(resolve(target, file.path));
        if (content.includes(0)) { omitted.push({ path: file.path, reason: 'Binary content' }); continue; }
        const lines = redact(content.toString('utf8')).split('\n');
        if (lines.at(-1) === '') lines.pop();
        file.diffs.push({ layer: file.untracked ? 'untracked' : 'snapshot', kind: file.untracked ? 'untracked' : 'snapshot',
          note: file.untracked ? 'Actual untracked contents; not part of git diff' : 'Current source snapshot; not a change',
          rows: lines.map((text, i) => ({ kind: file.untracked ? 'add' : 'context', text, oldLine: null, newLine: i + 1 })) });
      }
      files.push(file);
    } catch (error) { omitted.push({ path: file.path, reason: `Collection failed (${error.code || 'unavailable'}); evidence not assessed` }); }
  }
  const statistics = {};
  for (const file of files) for (const diff of file.diffs) {
    const stat = statistics[diff.layer] ||= { files: 0, added: 0, deleted: 0 };
    stat.files++;
    if (diff.kind !== 'snapshot') for (const row of diff.rows) {
      if (row.kind === 'add') stat.added++;
      if (row.kind === 'delete') stat.deleted++;
    }
  }
  const finalStatus = git('status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=all');
  const finalHead = optional('rev-parse', '--verify', 'HEAD');
  if (finalStatus !== statusRaw || finalHead !== headSha) throw new Error('Target changed during collection; retry');
  const snapshotId = createHash('sha256').update(JSON.stringify({ headSha, resolvedHead, mergeBase, statusRaw, files, omitted })).digest('hex');
  return { reviewId: randomUUID(), snapshotId, root: target, mode, branch, base: base || null, head: resolvedHead,
    mergeBase, commits, dirty: !!statusRaw, statistics, files, omitted, limits,
    coverage: { inventory: candidates.length, collected: files.length, reviewed: 0, modules,
      note: 'Collection is not semantic review. Mark files reviewed only after evaluation. Line statistics are displayed evidence, by layer; omitted content is excluded.' } };
}
