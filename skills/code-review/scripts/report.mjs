// Owner-local offline report rendering and contained, explicit temporary lifecycle.
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync, lstatSync, realpathSync, readdirSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, basename, relative, isAbsolute, sep, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { validateReview, calculateScore, reviewStatus, exportDecisions } from './model.mjs';
import { redact } from './collect.mjs';
import { localizeHtmlTemplate, localizeUiScript } from './localization.mjs';

const OWNER = 'agentic-code-review-v1';
const ALLOWED = new Set(['owner.json', 'report.html', 'review.json', 'review.md', 'desktop.png', 'workspace.png', 'mobile.png', 'mobile-workspace.png']);
const escaped = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
const hash = text => createHash('sha256').update(text).digest('base64');
const childOf = (parent, child) => { const r = relative(parent, child); return !!r && r !== '..' && !r.startsWith(`..${sep}`) && !isAbsolute(r); };

function scrub(value) {
  if (typeof value === 'string') return redact(value);
  if (Array.isArray(value)) return value.map(scrub);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, scrub(v)]));
  return value;
}
export function prepareReport(input) {
  validateReview(input);
  const data = scrub(input);
  validateReview(data);
  // The public snapshot identity also binds redacted assessment input to avoid foreign decisions.
  data.score = calculateScore(data.rules, data.scorePolicy);
  data.status = reviewStatus(data, data.score);
  data.snapshot.coverage.reviewed = data.snapshot.files.filter(f => f.reviewed).length;
  data.initialDecisions = exportDecisions(data);
  return data;
}

export function renderHtml(input, { locale = 'en' } = {}) {
  if (!['en', 'es'].includes(locale)) throw new Error('Report locale must be en or es');
  const data = prepareReport(input);
  // HTML parsing normalizes CRLF; hash the same normalized text on every checkout.
  const css = readFileSync(new URL('./report.css', import.meta.url), 'utf8').replace(/\r\n?/g, '\n');
  const script = localizeUiScript(readFileSync(new URL('./report-ui.js', import.meta.url), 'utf8').replace(/\r\n?/g, '\n'), locale);
  const json = JSON.stringify(data).replaceAll('<', '\\u003c').replaceAll('>', '\\u003e').replaceAll('&', '\\u0026').replaceAll('\u2028', '\\u2028').replaceAll('\u2029', '\\u2029');
  const csp = `default-src 'none'; script-src 'sha256-${hash(script)}'; style-src 'sha256-${hash(css)}'; img-src data:; connect-src 'none'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'`;
  const template = `<!doctype html>
<html lang="${locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="${csp}"><meta name="color-scheme" content="dark light">
<title>Code Review · ${escaped(data.snapshot.reviewId)}</title><style>${css}</style></head>
<body><a class="skip" href="#main">Skip to review</a>
<header><div><span class="brand">JAC / CODE REVIEW</span><h1>Review workspace</h1><p id="identity"></p></div>
<div class="actions"><button id="theme" type="button">Light theme</button><button id="copy-decisions" type="button">Copy decisions for an AI agent</button><button id="download-decisions" type="button">Export decisions JSON</button></div></header>
<nav class="sections" aria-label="Report sections"><a href="#overview">Overview</a><a href="#workspace">Files & diff</a><a href="#findings-section">Findings</a><a href="#rules-section">Standards</a><a href="#validations">Validations</a><a href="#commits">Commit Advisor</a><a href="#closing">Next steps</a></nav>
<main id="main"><section id="overview" aria-labelledby="overview-title"><p class="eyebrow">Executive dashboard</p><h2 id="overview-title">Evidence before approval</h2><p id="summary"></p><div id="metrics" class="metrics"></div><p id="score-note" class="muted"></p><div id="dimensions" class="dimensions"></div><details><summary>Assessment coverage, context and limitations</summary><div id="coverage"></div></details><div id="strengths"></div></section>
<section id="workspace" aria-labelledby="workspace-title"><div class="section-head"><div><p class="eyebrow">Changes & evidence</p><h2 id="workspace-title">File workspace</h2></div><label>Diff view <select id="diff-mode"><option value="split">Side by side</option><option value="unified">Unified</option></select></label></div>
<div class="workspace"><aside><h3>Files reviewed</h3><div id="file-list" aria-label="File navigation"></div></aside><div class="diff-workspace"><h3 id="file-title" tabindex="-1"></h3><p id="file-state" class="muted"></p><div id="diff"></div></div></div></section>
<section id="findings-section" aria-labelledby="findings-title"><p class="eyebrow">Review conversation</p><h2 id="findings-title">Findings & recommendations</h2><div class="filters"><label>Search <input id="search" type="search" placeholder="Title, file, evidence…"></label><label>Severity <select id="severity"><option value="">All severities</option></select></label><label>Category <select id="category"><option value="">All categories</option></select></label><label>Decision <select id="decision-filter"><option value="">All decisions</option><option>pending</option><option>accepted</option><option>rejected</option><option>deferred</option></select></label></div>
<p id="finding-count" role="status" aria-live="polite"></p><div id="findings"></div><h3>Your decisions</h3><p id="decision-summary"></p><p class="muted">Accept means intent to address. Reject retains the finding with your reason. Defer keeps it pending. Decisions never modify code or the score. Keep this tab open until you copy or export; refreshing clears this session.</p><fieldset id="implementation-request" class="implementation-request" hidden><legend>Would you like the AI agent to correct the accepted recommendations?</legend><label><input type="radio" name="implementation" value="yes"> Yes, request corrections</label><label><input type="radio" name="implementation" value="no"> No, keep the code unchanged</label><p class="muted">Copy and paste your decisions to the AI agent. This report cannot send messages or change files by itself.</p></fieldset></section>
<section id="rules-section"><p class="eyebrow">Traceable criteria</p><h2>Standards alignment</h2><div id="rules" class="table-scroll"></div></section>
<section id="validations"><p class="eyebrow">Executed checks</p><h2>Validation results</h2><div id="validation-list"></div></section>
<section id="commits"><p class="eyebrow">Manual preparation</p><h2>Commit Advisor</h2><p>No command runs from this report. Check all existing staged work before committing.</p><p id="commit-decision-state" role="status"></p><div id="commit-content"></div></section>
<section id="closing"><p class="eyebrow">Handoff & lifecycle</p><h2>Conclusions & next steps</h2><div id="next-steps"></div><p>Keep the temporary report while work is pending. Ask your AI agent to remove this specific review only after confirming you are finished. Closing VS Code does not clean it up.</p></section>
<section id="transfer" hidden><h2>Copy fallback</h2><p>Select and copy the text below. A preview may restrict clipboard or downloads.</p><textarea id="transfer-text" readonly rows="12" aria-label="Structured text to copy"></textarea></section>
</main><p id="notice" role="status" aria-live="polite"></p><noscript>This report needs local JavaScript for navigation and decisions. Open in a trusted local browser if preview scripts are blocked.</noscript>
<script id="review-data" type="application/json">__REVIEW_DATA__</script><script>__REVIEW_SCRIPT__</script></body></html>`;
  return localizeHtmlTemplate(template, locale).replace('__REVIEW_DATA__', () => json).replace('__REVIEW_SCRIPT__', () => script);
}

export function renderMarkdown(input) {
  const data = prepareReport(input);
  const safe = s => String(s).replace(/[<>]/g, c => c === '<' ? '&lt;' : '&gt;');
  const lines = ['# Code Review', '', `Review: ${data.snapshot.reviewId}`, `Snapshot: ${data.snapshot.snapshotId}`, '',
    `Status: ${data.status.label}`, `Alignment: ${data.score.label}`, `Assessment coverage: ${data.score.coverage ?? 'Not assessed'}%`, '', safe(data.summary), '',
    '## Scope and limitations', '', safe(JSON.stringify(data.snapshot.coverage)), ...data.limitations.map(safe), '', '## Findings', ''];
  for (const f of data.findings) lines.push(`### ${safe(f.id)} · ${f.severity} · ${safe(f.title)}`, '',
    `${safe(f.file)} (${f.verification}, ${f.confidence} confidence, ${f.origin})`,
    `Rule: ${safe(f.ruleId)}`, f.location ? `Location: ${safe(JSON.stringify(f.location))}` : 'Location: file-level',
    safe(f.description), `Evidence: ${f.evidence.map(safe).join('; ')}`, `Impact: ${safe(f.impact)}`,
    `Recommendation: ${safe(f.recommendation)}`, '');
  lines.push('## Rules', '', ...data.rules.map(r => `${safe(r.id)}: ${r.state} — ${safe((r.evidence || [r.reason]).join('; '))}`), '',
    '## Validations', '', ...data.validations.map(v => `${safe(v.name)}: ${v.status} — ${safe(v.evidence)}`), '',
    '## Commit Advisor', '', ...data.commitAdvisor.groups.map(g => safe(JSON.stringify(g, null, 2))), '',
    '## Next steps', '', ...data.nextSteps.map(safe), '', data.score.meaning);
  return lines.join('\n');
}

function ownedRoot() {
  const temp = realpathSync(tmpdir()), root = join(temp, 'agentic-code-review');
  if (!existsSync(root)) mkdirSync(root, { mode: 0o700 });
  if (!lstatSync(root).isDirectory() || lstatSync(root).isSymbolicLink() || realpathSync(root) !== root)
    throw new Error('Temporary root must be a real owned directory, not a link');
  return root;
}
export function writeReport(input, { json = false, markdown = false, locale = 'en' } = {}) {
  const data = prepareReport(input);
  const html = renderHtml(data, { locale });
  const root = ownedRoot(), target = realpathSync(data.snapshot.root);
  if (root === target || childOf(target, root)) throw new Error('Report must be outside analyzed repository');
  const directory = mkdtempSync(join(root, `${data.snapshot.reviewId}-`));
  const marker = { owner: OWNER, reviewId: data.snapshot.reviewId, directory };
  writeFileSync(join(directory, 'owner.json'), JSON.stringify(marker), { flag: 'wx', mode: 0o600 });
  const report = join(directory, 'report.html');
  writeFileSync(report, html, { flag: 'wx', mode: 0o600 });
  if (json) writeFileSync(join(directory, 'review.json'), JSON.stringify(data, null, 2), { flag: 'wx', mode: 0o600 });
  if (markdown) writeFileSync(join(directory, 'review.md'), renderMarkdown(data), { flag: 'wx', mode: 0o600 });
  return { directory, report, reviewId: data.snapshot.reviewId };
}

export function cleanupReview({ directory, reviewId, confirmed = false }) {
  if (confirmed !== true) throw new Error('Explicit user completion confirmation required');
  const root = ownedRoot(), location = resolve(directory);
  if (!/^[a-f0-9-]{36}$/i.test(reviewId) || dirname(location) !== root || !basename(location).startsWith(`${reviewId}-`) ||
    lstatSync(location).isSymbolicLink() || !lstatSync(location).isDirectory() || realpathSync(location) !== location)
    throw new Error('Cleanup target is not an exact contained review directory');
  const markerPath = join(location, 'owner.json');
  if (lstatSync(markerPath).isSymbolicLink()) throw new Error('Linked ownership marker');
  const marker = JSON.parse(readFileSync(markerPath, 'utf8'));
  if (marker.owner !== OWNER || marker.reviewId !== reviewId || marker.directory !== location) throw new Error('Ownership mismatch');
  for (const name of readdirSync(location)) {
    const stat = lstatSync(join(location, name));
    if (!ALLOWED.has(name) || !stat.isFile() || stat.isSymbolicLink()) throw new Error('Unexpected file or link; cleanup refused');
  }
  // All absolute targets and direct children were checked before recursive removal.
  rmSync(location, { recursive: true, force: false });
  if (existsSync(location)) throw new Error('Cleanup did not complete');
  return { deleted: location, verified: true };
}
