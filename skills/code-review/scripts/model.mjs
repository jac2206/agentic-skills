// Validated review model, deterministic scoring, manual commit text and decision handoff.
export const DIMENSIONS = ['architecture', 'quality', 'security', 'testing', 'standards', 'performance'];
export const DEFAULT_WEIGHTS = { architecture: 20, quality: 20, security: 20, testing: 20, standards: 15, performance: 5 };
export const SEVERITIES = ['Critical', 'High', 'Medium', 'Low', 'Suggestion'];
const STATES = ['passed', 'failed', 'unverified', 'not-applicable'];
const requireValue = (condition, message) => { if (!condition) throw new Error(message); };
const text = value => typeof value === 'string' && !!value.trim();
const evidence = value => Array.isArray(value) && value.length > 0 && value.every(text);
const percent = value => Math.round(value * 10000) / 100;
const unique = list => new Set(list).size === list.length;
export function calculateScore(rules, { weights = DEFAULT_WEIGHTS, minCoverage = 0.8 } = {}) {
  requireValue(Array.isArray(rules) && rules.length > 0, 'Rules are required');
  requireValue(unique(rules.map(r => r.id)), 'Duplicate rule ID');
  requireValue(minCoverage > 0 && minCoverage <= 1, 'Coverage threshold must be in (0, 1]');
  requireValue(DIMENSIONS.every(d => Number.isFinite(weights[d]) && weights[d] > 0) &&
    Math.abs(Object.values(weights).reduce((a, b) => a + b, 0) - 100) < 0.000001 && Object.keys(weights).length === 6,
  'Six positive dimension weights must sum to 100');
  for (const r of rules) {
    requireValue(text(r.id) && text(r.title) && text(r.source) && text(r.criterion) && DIMENSIONS.includes(r.dimension), 'Rule identity, source, criterion and dimension required');
    requireValue(STATES.includes(r.state), 'Invalid rule state');
    requireValue(r.weight === undefined || (Number.isFinite(r.weight) && r.weight > 0), 'Invalid rule weight');
    requireValue(['passed', 'failed'].includes(r.state) ? evidence(r.evidence) : text(r.reason), 'Rule evidence or reason required');
  }
  const dimensions = {};
  for (const d of DIMENSIONS) {
    const selected = rules.filter(r => r.dimension === d);
    requireValue(selected.length > 0, `Declare applicable or justified N/A rules for ${d}`);
    const counts = Object.fromEntries(STATES.map(s => [s, selected.filter(r => r.state === s).length]));
    const sum = state => selected.filter(r => r.state === state).reduce((n, r) => n + (r.weight ?? 1), 0);
    const passed = sum('passed'), failed = sum('failed'), unverified = sum('unverified');
    const applicableWeight = passed + failed + unverified, assessedWeight = passed + failed;
    const coverage = applicableWeight ? assessedWeight / applicableWeight : null;
    const score = assessedWeight && coverage >= minCoverage ? percent(passed / assessedWeight) : null;
    dimensions[d] = { weight: weights[d], counts, applicableWeight, assessedWeight, passedWeight: passed,
      coverage: coverage === null ? null : percent(coverage), score,
      label: !applicableWeight ? 'Not applicable' : score === null ? 'Not assessed' : `${score}%` };
  }
  const applicable = Object.values(dimensions).filter(d => d.applicableWeight > 0);
  const weight = applicable.reduce((n, d) => n + d.weight, 0);
  const coverage = weight ? applicable.reduce((n, d) => n + d.weight * d.assessedWeight / d.applicableWeight, 0) / weight : null;
  const sufficient = applicable.length > 0 && applicable.every(d => d.score !== null) && coverage >= minCoverage;
  const score = sufficient ? percent(applicable.reduce((n, d) => n + d.weight * d.passedWeight / d.assessedWeight, 0) / weight) : null;
  return { score, label: score === null ? 'Not assessed' : `${score}%`, coverage: coverage === null ? null : percent(coverage),
    minCoverage: minCoverage * 100, dimensions,
    meaning: 'Alignment with evaluated rules only; 100% does not guarantee absence of defects.' };
}

export function validateReview(data) {
  requireValue(data.schemaVersion === '1.0', 'Unsupported review schema');
  const s = data.snapshot;
  requireValue(s && /^[a-f0-9-]{36}$/i.test(s.reviewId) && /^[a-f0-9]{64}$/.test(s.snapshotId), 'Review and snapshot identity required');
  requireValue(['quick', 'pr', 'full'].includes(s.mode) && Array.isArray(s.files) && unique(s.files.map(f => f.id)) && unique(s.files.map(f => f.path)), 'Invalid snapshot files');
  requireValue(text(s.root) && text(s.branch) && Array.isArray(s.omitted) && Array.isArray(s.limits) && Array.isArray(s.commits) &&
    s.statistics && s.coverage && Array.isArray(s.coverage.modules) && Number.isInteger(s.coverage.inventory) && s.coverage.inventory >= s.files.length &&
    typeof s.dirty === 'boolean', 'Snapshot context and coverage required');
  requireValue(data.context && evidence(data.context.standards) && text(data.summary), 'Context standards and summary required');
  for (const key of ['findings', 'rules', 'validations', 'strengths', 'limitations', 'nextSteps']) requireValue(Array.isArray(data[key]), `Missing ${key} list`);
  requireValue(unique(data.findings.map(f => f.id)), 'Duplicate finding ID');
  const ruleIds = new Set(data.rules.map(r => r.id));
  for (const file of s.files) {
    requireValue(text(file.id) && text(file.path) && typeof file.reviewed === 'boolean' && Array.isArray(file.diffs), 'Invalid file');
    for (const diff of file.diffs) requireValue(text(diff.layer) && Array.isArray(diff.rows) && diff.rows.every(r =>
      ['hunk', 'add', 'delete', 'context', 'note'].includes(r.kind) && typeof r.text === 'string' &&
      [r.oldLine, r.newLine].every(n => n === null || Number.isInteger(n) && n > 0)), 'Invalid diff rows');
  }
  for (const f of data.findings) {
    const file = s.files.find(x => x.path === f.file);
    requireValue(text(f.id) && file && ruleIds.has(f.ruleId) && DIMENSIONS.includes(f.category) && SEVERITIES.includes(f.severity), 'Finding identity, file, rule or severity invalid');
    const rule = data.rules.find(r => r.id === f.ruleId);
    requireValue(rule.dimension === f.category, 'Finding category must match its rule');
    requireValue(['confirmed', 'potential', 'optional'].includes(f.verification) && ['high', 'medium', 'low'].includes(f.confidence) &&
      ['introduced', 'existing', 'unknown'].includes(f.origin), 'Finding verification/confidence/origin required');
    for (const k of ['title', 'description', 'impact', 'recommendation', 'severityRationale']) requireValue(text(f[k]), `Finding ${k} required`);
    requireValue(evidence(f.evidence), 'Finding evidence required');
    if (f.correction !== undefined) requireValue(text(f.correction), 'Correction example must be nonempty text');
    if (f.verification === 'confirmed') requireValue(rule.state === 'failed', 'Confirmed finding requires a failed rule');
    if (f.blocking) requireValue(f.verification === 'confirmed' && text(f.blockingReason), 'Blocker requires confirmation and policy/impact reason');
    if (f.location != null) {
      const { layer, side, start, end = start } = f.location;
      requireValue(['old', 'new'].includes(side) && Number.isInteger(start) && Number.isInteger(end) && start > 0 && end >= start, 'Invalid line range');
      const diff = file.diffs.find(d => d.layer === layer);
      const key = side === 'old' ? 'oldLine' : 'newLine';
      const available = new Set(diff?.rows.map(r => r[key]).filter(n => n !== null));
      requireValue(end - start < available.size && Array.from({ length: end - start + 1 }, (_, i) => start + i).every(n => available.has(n)), 'Finding line not present in evidence; add verified context or omit location');
    }
  }
  for (const r of data.rules.filter(r => r.state === 'failed'))
    requireValue(data.findings.some(f => f.ruleId === r.id && f.verification === 'confirmed'), 'Failed rule requires a confirmed finding');
  for (const v of data.validations) requireValue(text(v.name) && ['passed', 'failed', 'not run', 'not applicable'].includes(v.status) &&
    ['structural', 'functional', 'visual'].includes(v.kind) && text(v.evidence), 'Invalid validation result');
  requireValue(data.commitAdvisor && Array.isArray(data.commitAdvisor.groups) && evidence(data.commitAdvisor.conventionEvidence), 'Commit advisor evidence/groups required');
  requireValue(data.commitAdvisor.commitlint && ['passed', 'failed', 'not run', 'not applicable'].includes(data.commitAdvisor.commitlint.status) &&
    text(data.commitAdvisor.commitlint.evidence), 'Commitlint validation status/evidence required');
  for (const g of data.commitAdvisor.groups) {
    requireValue(text(g.type) && (g.scope == null || text(g.scope)) && text(g.description) && text(g.message) && text(g.rationale) && Array.isArray(g.include) &&
      g.include.every(p => s.files.some(f => f.path === p || f.previousPath === p)) && Array.isArray(g.exclude), 'Invalid commit group');
    if (g.manual) requireValue(JSON.stringify(g.manual) === JSON.stringify(commitCommands({ paths: g.include, message: g.message, shell: g.manual.shell })), 'Manual commands must be generated from verified paths and message');
  }
  calculateScore(data.rules, data.scorePolicy);
  return data;
}

export function reviewStatus(data, score = calculateScore(data.rules, data.scorePolicy)) {
  const blockers = data.findings.filter(f => f.verification === 'confirmed' && (f.severity === 'Critical' || f.blocking));
  return { label: blockers.length ? 'Blocked' : data.findings.some(f => f.verification === 'confirmed') ? 'Changes requested' :
    score.score === null || data.snapshot.files.some(f => !f.reviewed) || data.snapshot.omitted?.length || data.snapshot.limits?.length ? 'Incomplete' : 'Ready for human review',
  blockers: blockers.map(f => f.id) };
}

export function exportDecisions(data, decisions = {}, implementationDecision = 'not_decided') {
  const items = data.findings.map(f => {
    const d = decisions[f.id] || { status: 'pending', reason: '' };
    requireValue(['accepted', 'rejected', 'deferred', 'pending'].includes(d.status) && typeof d.reason === 'string', 'Invalid decision');
    requireValue(d.status !== 'rejected' || !!d.reason.trim(), 'Reject with reason');
    const item = { findingId: f.id, status: d.status, reason: d.reason, file: f.file };
    if (d.status === 'accepted') {
      item.recommendation = f.recommendation;
      if (f.correction) item.proposedCorrection = f.correction;
    }
    return item;
  });
  requireValue(['yes', 'no', 'not_decided'].includes(implementationDecision), 'Invalid implementation request');
  const acceptedIds = items.filter(d => d.status === 'accepted').map(d => d.findingId);
  requireValue(implementationDecision !== 'yes' || acceptedIds.length > 0, 'Implementation request requires accepted findings');
  return { schemaVersion: '1.0', reviewId: data.snapshot.reviewId, snapshotId: data.snapshot.snapshotId,
    targetRoot: data.snapshot.root, decisions: items,
    implementationRequest: { decision: implementationDecision, findingIds: implementationDecision === 'yes' ? acceptedIds : [] },
    affectedFiles: [...new Set(items.filter(d => d.status !== 'pending').map(d => d.file))] };
}
export function importDecisions(data, payload) {
  requireValue(payload.schemaVersion === '1.0' && payload.reviewId === data.snapshot.reviewId &&
    payload.snapshotId === data.snapshot.snapshotId, 'Stale or foreign decision payload');
  if (payload.targetRoot !== undefined) requireValue(payload.targetRoot === data.snapshot.root, 'Foreign target');
  requireValue(Array.isArray(payload.decisions) && payload.decisions.length === data.findings.length && unique(payload.decisions.map(d => d.findingId)), 'Decision set mismatch');
  const decisions = Object.create(null);
  for (const d of payload.decisions) {
    const finding = data.findings.find(f => f.id === d.findingId && f.file === d.file);
    requireValue(finding, 'Unknown finding/file');
    if (d.recommendation !== undefined) requireValue(d.status === 'accepted' && d.recommendation === finding.recommendation, 'Modified recommendation');
    if (d.proposedCorrection !== undefined) requireValue(d.status === 'accepted' && d.proposedCorrection === finding.correction, 'Modified correction example');
    decisions[d.findingId] = { status: d.status, reason: d.reason };
  }
  const request = payload.implementationRequest;
  if (request !== undefined) requireValue(request && Array.isArray(request.findingIds) &&
    ['yes', 'no', 'not_decided'].includes(request.decision), 'Invalid implementation request');
  const result = exportDecisions(data, decisions, request?.decision ?? 'not_decided');
  if (request) requireValue(JSON.stringify(request.findingIds) === JSON.stringify(result.implementationRequest.findingIds), 'Implementation scope mismatch');
  return result;
}

export function checkConventionalMessage(message) {
  if (typeof message !== 'string') return { valid: false, kind: 'syntax only; not Commitlint' };
  const [header, ...rest] = message.split(/\r?\n/);
  return { valid: /^[A-Za-z][A-Za-z0-9-]*(?:\([^()\r\n]+\))?!?: \S[^\r\n]*$/.test(header) && (!rest.length || rest[0] === ''),
    kind: 'syntax only; not Commitlint' };
}

// The caller supplies an already inspected installed API and resolved configuration.
// This function does not search, import configs, install, spawn or invoke hooks.
export async function checkCommitlint({ message, lint, config, toolEvidence, configEvidence } = {}) {
  if (!lint || !config) return { status: 'not run', evidence: 'Inspected installed Commitlint API/configuration unavailable' };
  requireValue(typeof lint === 'function' && text(message) && config.rules && text(toolEvidence) && text(configEvidence), 'Inspected Commitlint API, config and provenance required');
  try {
    const result = await lint(message, config.rules, { parserOpts: config.parserPreset?.parserOpts,
      plugins: config.plugins, ignores: config.ignores, defaultIgnores: config.defaultIgnores });
    requireValue(typeof result.valid === 'boolean' && Array.isArray(result.errors) && Array.isArray(result.warnings), 'Invalid Commitlint result');
    return { status: result.valid ? 'passed' : 'failed', evidence: `${toolEvidence}; ${configEvidence}`, errors: result.errors, warnings: result.warnings };
  } catch (error) { return { status: 'not run', evidence: `${toolEvidence}; ${configEvidence}; validation error: ${error.message}` }; }
}

export function commitCommands({ paths, message, shell = 'powershell' }) {
  requireValue(['powershell', 'posix'].includes(shell), 'Declare powershell or posix shell');
  requireValue(Array.isArray(paths) && paths.length > 0 && paths.every(p => text(p) && !/^[\\/]|^[A-Za-z]:|[\x00-\x1f\x7f]/.test(p) && !p.split(/[\\/]/).includes('..')), 'Unsafe manual command path');
  requireValue(text(message) && !/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(message), 'Unsafe message');
  const quote = value => "'" + value.replaceAll("'", shell === 'posix' ? "'\"'\"'" : "''") + "'";
  const paragraphs = message.split(/\r?\n\r?\n/).map(p => `-m ${quote(p)}`).join(' ');
  return { shell, warning: 'Manual only. Inspect the entire index: pre-existing staged files remain included. Never paste into a different shell.',
    commands: [`git --literal-pathspecs add -- ${paths.map(quote).join(' ')}`, 'git diff --cached --check', 'git diff --cached --stat', `git commit ${paragraphs}`] };
}
