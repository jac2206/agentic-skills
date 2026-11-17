/* Trusted offline interface. Repository and reviewer data are inserted only as text. */
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('review-data').textContent);
  const es = document.documentElement.lang === 'es';
  const labels = { 'Not assessed': 'Sin evaluar', 'Not applicable': 'No aplica', 'Blocked': 'Bloqueada',
    'Changes requested': 'Cambios solicitados', 'Incomplete': 'Incompleta', 'Ready for human review': 'Lista para revisión humana',
    architecture: 'Arquitectura', quality: 'Calidad', security: 'Seguridad', testing: 'Pruebas', standards: 'Estándares', performance: 'Rendimiento',
    Critical: 'Crítica', High: 'Alta', Medium: 'Media', Low: 'Baja', Suggestion: 'Sugerencia',
    confirmed: 'Confirmado', potential: 'Potencial', optional: 'Opcional', high: 'alta', medium: 'media', low: 'baja',
    introduced: 'introducido', existing: 'existente', unknown: 'desconocido', passed: 'cumplida', failed: 'incumplida',
    unverified: 'sin verificar', 'not-applicable': 'no aplica', 'not run': 'no ejecutada', 'not applicable': 'no aplica',
    accepted: 'aceptada', rejected: 'rechazada', deferred: 'pospuesta', pending: 'pendiente', old: 'anterior', new: 'nueva',
    'Alignment with evaluated rules only; 100% does not guarantee absence of defects.': 'Alineación con las reglas evaluadas; el 100% no garantiza ausencia de defectos.',
    'Actual untracked contents; not part of git diff': 'Contenido real sin seguimiento; no forma parte de git diff',
    'Current source snapshot; not a change': 'Contenido actual del archivo; no representa un cambio',
    'Metadata-only or no textual changes': 'Solo metadatos o sin diferencias de texto', 'Binary diff omitted': 'Diferencias binarias omitidas',
    'Manual only. Inspect the entire index: pre-existing staged files remain included. Never paste into a different shell.': 'Solo manual. Revisa todo el índice: los archivos ya preparados siguen incluidos. No pegues comandos en otra terminal.',
    'Collection is not semantic review. Mark files reviewed only after evaluation. Line statistics are displayed evidence, by layer; omitted content is excluded.': 'Recopilar no equivale a revisar. Los archivos se marcan revisados tras evaluarlos. Las estadísticas corresponden a la evidencia visible por capa y excluyen el contenido omitido.' };
  const display = value => es && Object.hasOwn(labels, value) ? labels[value] : value;
  const byId = id => document.getElementById(id);
  const make = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  };
  const paragraph = (parent, text, className) => parent.append(make('p', text, className));
  const list = (parent, items) => {
    const ul = make('ul');
    items.forEach(item => ul.append(make('li', typeof item === 'string' ? item : JSON.stringify(item))));
    parent.append(ul);
  };
  const button = (text, action, className) => {
    const b = make('button', text, className); b.type = 'button'; b.addEventListener('click', action); return b;
  };
  const badge = (label, color = label.toLowerCase()) => make('span', display(label), `badge ${color}`);
  const notice = message => { byId('notice').textContent = message; };
  const files = data.snapshot.files;
  const decisions = new Map(data.initialDecisions.decisions.map(d => [d.findingId, { ...d }]));
  let selectedFile = files[0]?.id;
  const payload = () => ({ schemaVersion: '1.0', reviewId: data.snapshot.reviewId, snapshotId: data.snapshot.snapshotId,
    decisions: [...decisions.values()].map(d => {
      const item = { ...d };
      const finding = data.findings.find(f => f.id === d.findingId);
      if (d.status === 'accepted') {
        item.recommendation = finding.recommendation;
        if (finding.correction) item.proposedCorrection = finding.correction;
      }
      return item;
    }), affectedFiles: [...new Set([...decisions.values()].filter(d => d.status !== 'pending').map(d => d.file))] });
  function decisionText() {
    const invalid = [...decisions.values()].find(d => d.status === 'rejected' && !d.reason.trim());
    if (invalid) { notice(`Add a rejection reason for ${invalid.findingId} before exporting.`); return null; }
    return JSON.stringify(payload(), null, 2);
  }

  function copyFallback(text) {
    byId('transfer').hidden = false; byId('transfer-text').value = text;
    byId('transfer-text').focus(); byId('transfer-text').select();
    notice('Clipboard unavailable. Copy the selected text below.');
  }
  async function copy(text) {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Unavailable');
      await navigator.clipboard.writeText(text); notice('Copied. Paste into Codex when ready.');
    } catch { copyFallback(text); }
  }
  byId('copy-decisions').addEventListener('click', () => { const text = decisionText(); if (text) copy(text); });
  byId('download-decisions').addEventListener('click', () => {
    const text = decisionText(); if (!text) return;
    const url = URL.createObjectURL(new Blob([text], { type: 'application/json' }));
    const a = make('a'); a.href = url; a.download = `code-review-${data.snapshot.reviewId}-decisions.json`;
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 3000);
    notice('Export requested. If this preview blocks downloads, use Copy decisions for Codex.');
  });
  byId('theme').addEventListener('click', () => {
    const light = document.documentElement.dataset.theme !== 'light';
    document.documentElement.dataset.theme = light ? 'light' : 'dark';
    byId('theme').textContent = light ? 'Dark theme' : 'Light theme';
  });
  if (matchMedia('(max-width: 680px)').matches) byId('diff-mode').value = 'unified';
  byId('identity').textContent = `${data.snapshot.mode.toUpperCase()} · ${data.snapshot.branch} · ${data.snapshot.reviewId}`;
  byId('summary').textContent = data.summary;
  const addMetric = (value, label) => { const div = make('div', undefined, 'metric'); div.append(make('strong', value), make('span', label)); byId('metrics').append(div); };
  addMetric(display(data.score.label), 'Standards alignment'); addMetric(display(data.status.label), `${data.status.blockers.length} blocking findings`);
  addMetric(data.score.coverage === null ? display('Not assessed') : `${data.score.coverage}%`, 'Rule assessment coverage');
  addMetric(`${files.filter(f => f.reviewed).length} / ${data.snapshot.coverage.inventory}`, 'Files reviewed / inventoried');
  byId('score-note').textContent = `${display(data.score.meaning)} Minimum assessed coverage: ${data.score.minCoverage}% per applicable dimension. Decisions do not change this score.`;
  for (const [name, d] of Object.entries(data.score.dimensions)) {
    const block = make('div', undefined, 'dimension'); const row = make('div', undefined, 'row');
    row.append(make('strong', display(name)), make('span', display(d.label))); block.append(row);
    if (d.score !== null) { const meter = make('meter'); meter.min = 0; meter.max = 100; meter.value = d.score; meter.setAttribute('aria-label', es ? `Alineación: ${display(name)}` : `${name} alignment`); block.append(meter); }
    paragraph(block, `${d.weight}% weight · ${d.counts.passed} passed · ${d.counts.failed} failed · ${d.counts.unverified} unverified · ${d.counts['not-applicable']} N/A`);
    byId('dimensions').append(block);
  }
  const coverage = byId('coverage');
  paragraph(coverage, display(data.snapshot.coverage.note)); paragraph(coverage, `Root: ${data.snapshot.root}`);
  paragraph(coverage, `Head: ${data.snapshot.head ?? 'unborn'} · Base: ${data.snapshot.base ?? 'not applicable'} · Merge-base: ${data.snapshot.mergeBase ?? 'not applicable'}`);
  paragraph(coverage, `Snapshot: ${data.snapshot.snapshotId} · Local dirty state: ${data.snapshot.dirty ? (es ? 'sí' : 'yes') : 'no'}`);
  paragraph(coverage, `Selected modules: ${data.snapshot.coverage.modules.join(', ') || (es ? 'inventario completo' : 'whole inventory')}`);
  coverage.append(make('h3', 'Project standards')); list(coverage, data.context.standards);
  if (data.context.description) paragraph(coverage, data.context.description);
  coverage.append(make('h3', 'Git statistics by evidence layer'));
  list(coverage, Object.entries(data.snapshot.statistics).map(([layer, s]) => `${layer}: ${s.files} ${es ? 'archivos' : 'files'} · +${s.added} / −${s.deleted}`));
  coverage.append(make('h3', 'Commits')); list(coverage, data.snapshot.commits);
  coverage.append(make('h3', 'Excluded or unavailable evidence')); list(coverage, [...data.snapshot.omitted, ...data.snapshot.limits, ...data.limitations]);
  if (data.strengths.length) { byId('strengths').append(make('h3', 'What is aligned')); list(byId('strengths'), data.strengths); }

  function showFinding(finding) {
    ['severity', 'category', 'decision-filter', 'search'].forEach(id => { byId(id).value = ''; });
    renderFindings();
    const node = [...byId('findings').children].find(n => n.dataset.findingId === finding.id);
    if (node) { node.classList.add('highlight'); node.scrollIntoView({ block: 'center' }); node.focus({ preventScroll: true }); }
  }
  function lineComments(file, layer, rows, parent, columns) {
    const findings = data.findings.filter(f => f.file === file.path && f.location?.layer === layer && rows.some(row => {
      const line = row?.[f.location.side === 'old' ? 'oldLine' : 'newLine'];
      return line >= f.location.start && line <= (f.location.end ?? f.location.start);
    }));
    if (!findings.length) return;
    const tr = make('tr'), td = make('td', undefined, 'comment'); td.colSpan = columns;
    findings.forEach(f => td.append(button(`${f.id} · ${display(f.severity)} · ${f.title}`, () => showFinding(f))));
    tr.append(td); parent.append(tr);
  }
  function addDiff(file, diff) {
    const split = byId('diff-mode').value === 'split';
    const scroller = make('div', undefined, 'diff-scroll'), table = make('table', undefined, `diff-table ${split ? 'split' : 'unified'}`);
    const caption = make('caption', `${diff.layer} · ${display(diff.note) || 'Actual repository diff'}${split ? ' · old | new' : ' · old/new lines'}`); table.append(caption);
    const columns = make('colgroup');
    (split ? ['number', 'code', 'number', 'code'] : ['number', 'number', 'code']).forEach(role => columns.append(make('col', undefined, role)));
    table.append(columns);
    const body = make('tbody'); table.append(body);
    const row = (left, right) => {
      const tr = make('tr');
      if (split) {
        tr.append(make('td', left?.oldLine ?? '', 'number'), make('td', left ? `${left.kind === 'delete' ? '−' : ' '} ${left.text}` : '', left?.kind),
          make('td', right?.newLine ?? '', 'number'), make('td', right ? `${right.kind === 'add' ? '+' : ' '} ${right.text}` : '', right?.kind));
      } else {
        const item = left || right;
        tr.append(make('td', item.oldLine ?? '', 'number'), make('td', item.newLine ?? '', 'number'),
          make('td', `${item.kind === 'add' ? '+' : item.kind === 'delete' ? '−' : ' '} ${item.text}`, item.kind));
      }
      body.append(tr); lineComments(file, diff.layer, [left, right], body, split ? 4 : 3);
    };
    for (let i = 0; i < diff.rows.length;) {
      const current = diff.rows[i];
      if (current.kind === 'hunk' || current.kind === 'note') {
        const tr = make('tr'), td = make('td', current.text, current.kind); td.colSpan = split ? 4 : 3; tr.append(td); body.append(tr); i++;
      } else if (split && ['delete', 'add'].includes(current.kind)) {
        const deleted = [], added = [];
        while (i < diff.rows.length && ['delete', 'add'].includes(diff.rows[i].kind)) {
          const r = diff.rows[i++]; (r.kind === 'delete' ? deleted : added).push(r);
        }
        for (let j = 0; j < Math.max(deleted.length, added.length); j++) row(deleted[j], added[j]);
      } else { row(current.kind === 'add' ? null : current, current.kind === 'delete' ? null : current); i++; }
    }
    if (!diff.rows.length) { const tr = make('tr'), td = make('td', diff.note || 'No textual diff'); td.colSpan = split ? 4 : 3; tr.append(td); body.append(tr); }
    scroller.append(table); byId('diff').append(scroller);
  }
  function showFile(id, focus = false) {
    selectedFile = id; const file = files.find(f => f.id === id);
    byId('diff').replaceChildren();
    if (!file) { byId('file-title').textContent = 'No collected file evidence'; return; }
    byId('file-title').textContent = file.path;
    byId('file-state').textContent = `${file.previousPath ? `Renamed from ${file.previousPath} · ` : ''}${file.untracked ? 'Untracked' : `Staged: ${file.staged || '—'} · Unstaged: ${file.unstaged || '—'} · Status: ${file.status || 'local'}`} · ${file.reviewed ? 'Reviewed' : 'Not reviewed'}`;
    for (const node of byId('file-list').children) node.setAttribute('aria-current', String(node.dataset.fileId === id));
    file.diffs.forEach(diff => addDiff(file, diff));
    const fileComments = data.findings.filter(f => f.file === file.path && !f.location);
    fileComments.forEach(f => byId('diff').append(button(`File comment: ${f.id} · ${f.title}`, () => showFinding(f))));
    if (focus) byId('file-title').focus();
  }
  files.forEach(file => {
    const b = button(file.path, () => showFile(file.id, true), 'file-button'); b.dataset.fileId = file.id;
    b.append(make('small', `${file.untracked ? 'Untracked' : file.status || `${file.staged || ' '}${file.unstaged || ' '}`} · ${file.reviewed ? 'reviewed' : 'not reviewed'}`)); byId('file-list').append(b);
  });
  byId('diff-mode').addEventListener('change', () => showFile(selectedFile)); showFile(selectedFile);
  [...new Set(data.findings.map(f => f.severity))].forEach(s => { const option = make('option', display(s)); option.value = s; byId('severity').append(option); });
  [...new Set(data.findings.map(f => f.category))].sort().forEach(s => { const option = make('option', display(s)); option.value = s; byId('category').append(option); });
  function decisionSummary() {
    byId('decision-summary').textContent = ['accepted', 'rejected', 'deferred', 'pending'].map(s => `${[...decisions.values()].filter(d => d.status === s).length} ${display(s)}`).join(' · ');
    const allAccepted = decisions.size > 0 && [...decisions.values()].every(d => d.status === 'accepted');
    byId('commit-decision-state').textContent = allAccepted
      ? (es ? 'Todas las recomendaciones están aceptadas. El commit sigue siendo una propuesta: primero aplica y verifica las correcciones.' : 'All recommendations are accepted. The commit remains a proposal: first apply and verify the corrections.')
      : (es ? 'El mensaje es una propuesta basada en el alcance revisado. Atiende las decisiones y validaciones pendientes antes del commit.' : 'The message is a proposal based on the reviewed scope. Address pending decisions and checks before committing.');
  }
  function renderFindings() {
    const root = byId('findings'); root.replaceChildren();
    const filtered = data.findings.filter(f => (!byId('severity').value || f.severity === byId('severity').value) &&
      (!byId('category').value || f.category === byId('category').value) &&
      (!byId('decision-filter').value || decisions.get(f.id).status === byId('decision-filter').value) &&
      JSON.stringify(f).toLowerCase().includes(byId('search').value.toLowerCase()));
    byId('finding-count').textContent = `${filtered.length} of ${data.findings.length} findings`;
    if (!filtered.length) paragraph(root, 'No findings match these filters.', 'empty');
    for (const f of filtered) {
      const article = make('article', undefined, 'finding'); article.tabIndex = -1; article.dataset.findingId = f.id;
      const head = make('div', undefined, 'finding-head'); head.append(badge(f.severity), badge(f.verification), make('span', `${f.id} · ${display(f.category)}`)); article.append(head, make('h3', f.title));
      article.append(button(`${f.file}${f.location ? ` · ${display(f.location.side)} ${f.location.start}${f.location.end ? `–${f.location.end}` : ''} (${f.location.layer})` : (es ? ' · archivo completo' : ' · file-level')}`, () => {
        showFile(files.find(file => file.path === f.file).id, true); byId('workspace').scrollIntoView();
      }));
      paragraph(article, f.description);
      const dl = make('dl');
      for (const [key, value] of [['Rule', f.ruleId], ['Evidence', f.evidence.join('\n')], ['Impact', f.impact], ['Recommendation', f.recommendation],
        ['Verification', `${display(f.verification)} · ${display(f.confidence)} confidence · ${display(f.origin)}`], ['Severity basis', f.severityRationale], ...(f.blocking ? [['Blocking reason', f.blockingReason]] : [])])
        dl.append(make('dt', key), make('dd', value));
      article.append(dl);
      if (f.correction) {
        const example = make('details');
        example.append(make('summary', 'View correction example'), make('p', 'Proposed example · not applied', 'muted'), make('pre', f.correction));
        article.append(example);
      } else paragraph(article, 'No code example available for this finding.', 'muted');
      const reasonLabel = make('label', 'Decision reason (required to reject)');
      const reason = make('textarea'); reason.rows = 2; reason.value = decisions.get(f.id).reason; reasonLabel.append(reason);
      reason.addEventListener('input', () => { decisions.get(f.id).reason = reason.value; });
      const actions = make('div', undefined, 'actions');
      for (const [status, label] of [['accepted', 'Accept recommendation'], ['rejected', 'Reject with reason'], ['deferred', 'Defer']]) {
        const b = button(label, () => {
          if (status === 'rejected' && !reason.value.trim()) { reason.focus(); notice('Add a reason before rejecting this recommendation.'); return; }
          decisions.set(f.id, { findingId: f.id, status, reason: reason.value, file: f.file });
          renderFindings(); decisionSummary(); notice(`${f.id}: ${display(status)}. No code was changed.`);
        });
        b.setAttribute('aria-pressed', String(decisions.get(f.id).status === status)); actions.append(b);
      }
      article.append(reasonLabel, actions, make('p', `Decision: ${display(decisions.get(f.id).status)}`, 'muted')); root.append(article);
    }
    decisionSummary();
  }
  ['severity', 'category', 'decision-filter'].forEach(id => byId(id).addEventListener('change', renderFindings));
  byId('search').addEventListener('input', renderFindings); renderFindings();
  const rules = make('table', undefined, 'rules'), header = make('tr');
  ['Rule / dimension', 'State', 'Source / criterion', 'Evidence / reason'].forEach(t => { const th = make('th', t); th.scope = 'col'; header.append(th); });
  const thead = make('thead'); thead.append(header); rules.append(thead); const tbody = make('tbody');
  data.rules.forEach(r => { const tr = make('tr'); tr.append(make('td', `${r.id} · ${display(r.dimension)}\n${r.title}`), make('td', display(r.state), r.state),
    make('td', `${r.source}\n${r.criterion}`), make('td', r.evidence?.join('\n') || r.reason)); tbody.append(tr); }); rules.append(tbody); byId('rules').append(rules);
  if (!data.validations.length) paragraph(byId('validation-list'), 'No validations executed. This is an evidence review only.', 'muted');
  data.validations.forEach(v => { const div = make('div', undefined, 'validation'); div.append(badge(v.status), make('strong', ` ${v.name} · ${v.kind}`)); paragraph(div, v.evidence); byId('validation-list').append(div); });
  const commits = byId('commit-content'); list(commits, data.commitAdvisor.conventionEvidence);
  paragraph(commits, `Commitlint: ${display(data.commitAdvisor.commitlint?.status || 'not run')} · ${data.commitAdvisor.commitlint?.evidence || 'No executed validation evidence supplied'}`);
  if (!data.commitAdvisor.groups.length) paragraph(commits, 'No commit proposed for this scope. Ask Codex for a proposal if there are relevant changes.');
  data.commitAdvisor.groups.forEach((g, i) => {
    const div = make('div', undefined, 'commit-group'); div.append(make('h3', `Commit ${i + 1}${g.type ? ` · ${g.type}${g.scope ? `(${g.scope})` : ''}` : ''}`));
    paragraph(div, g.rationale); div.append(make('pre', g.message), button('Copy commit message', () => copy(g.message)));
    paragraph(div, 'Include'); list(div, g.include); paragraph(div, 'Exclude'); list(div, g.exclude);
    if (g.manual) { paragraph(div, `${g.manual.shell} · ${display(g.manual.warning)}`); div.append(make('pre', g.manual.commands.join('\n')),
      button('Copy manual commands', () => copy(g.manual.commands.join('\n')))); }
    commits.append(div);
  });
  list(byId('next-steps'), data.nextSteps);
})();
