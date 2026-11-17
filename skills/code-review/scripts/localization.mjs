// Translate only trusted interface templates, never repository or reviewer data.
const html = [
  ['Skip to review', 'Ir a la revisión'], ['Review workspace', 'Espacio de revisión'],
  ['Light theme', 'Tema claro'], ['Copy decisions for an AI agent', 'Copiar decisiones para un agente de IA'],
  ['Export decisions JSON', 'Exportar decisiones en JSON'], ['Report sections', 'Secciones del informe'],
  ['>Overview<', '>Resumen<'], ['>Files & diff<', '>Archivos y diferencias<'], ['>Findings<', '>Hallazgos<'],
  ['>Standards<', '>Estándares<'], ['>Validations<', '>Validaciones<'], ['>Next steps<', '>Próximos pasos<'],
  ['Executive dashboard', 'Panel ejecutivo'], ['Evidence before approval', 'Evidencia para la revisión'],
  ['Assessment coverage, context and limitations', 'Cobertura, contexto y limitaciones'],
  ['Changes & evidence', 'Cambios y evidencia'], ['File workspace', 'Archivos y diferencias'],
  ['Diff view', 'Vista de diferencias'], ['Side by side', 'Lado a lado'], ['>Unified<', '>Unificada<'],
  ['Files reviewed', 'Archivos revisados'], ['File navigation', 'Navegación de archivos'],
  ['Review conversation', 'Conversación de revisión'], ['Findings & recommendations', 'Hallazgos y recomendaciones'],
  ['>Search ', '>Buscar '], ['Title, file, evidence…', 'Título, archivo, evidencia…'],
  ['>Severity ', '>Severidad '], ['All severities', 'Todas las severidades'],
  ['>Category ', '>Categoría '], ['All categories', 'Todas las categorías'], ['>Decision ', '>Decisión '], ['All decisions', 'Todas las decisiones'],
  ['<option>pending</option>', '<option value="pending">pendiente</option>'],
  ['<option>accepted</option>', '<option value="accepted">aceptada</option>'],
  ['<option>rejected</option>', '<option value="rejected">rechazada</option>'],
  ['<option>deferred</option>', '<option value="deferred">pospuesta</option>'],
  ['Your decisions', 'Tus decisiones'],
  ['Accept means intent to address. Reject retains the finding with your reason. Defer keeps it pending. Decisions never modify code or the score. Keep this tab open until you copy or export; refreshing clears this session.', 'Aceptar indica la intención de atender el hallazgo. Rechazar lo conserva con tu motivo. Posponer lo deja pendiente. Las decisiones no modifican el código ni la puntuación. Copia o exporta antes de cerrar o actualizar esta pestaña.'],
  ['Would you like the AI agent to correct the accepted recommendations?', '¿Quieres que el agente de IA corrija las recomendaciones aceptadas?'],
  ['Yes, request corrections', 'Sí, solicitar correcciones'], ['No, keep the code unchanged', 'No, dejar el código sin cambios'],
  ['Copy and paste your decisions to the AI agent. This report cannot send messages or change files by itself.', 'Copia y pega tus decisiones al agente de IA. Este informe no puede enviar mensajes ni cambiar archivos por sí mismo.'],
  ['Traceable criteria', 'Criterios trazables'], ['Standards alignment', 'Alineación con estándares'],
  ['Executed checks', 'Comprobaciones ejecutadas'], ['Validation results', 'Resultados de validación'],
  ['Manual preparation', 'Preparación manual'],
  ['No command runs from this report. Check all existing staged work before committing.', 'Este informe no ejecuta comandos. Revisa todos los cambios preparados antes de crear un commit.'],
  ['Handoff & lifecycle', 'Entrega y ciclo de vida'], ['Conclusions & next steps', 'Conclusiones y próximos pasos'],
  ['Keep the temporary report while work is pending. Ask your AI agent to remove this specific review only after confirming you are finished. Closing VS Code does not clean it up.', 'Conserva el informe temporal mientras haya trabajo pendiente. Pide a tu agente de IA que elimine esta revisión específica solo después de confirmar que terminaste. Cerrar VS Code no elimina el informe.'],
  ['Copy fallback', 'Copia manual'], ['Select and copy the text below. A preview may restrict clipboard or downloads.', 'Selecciona y copia el texto siguiente. La vista previa puede restringir el portapapeles o las descargas.'],
  ['Structured text to copy', 'Texto estructurado para copiar'],
  ['This report needs local JavaScript for navigation and decisions. Open in a trusted local browser if preview scripts are blocked.', 'Este informe necesita JavaScript local para la navegación y las decisiones. Ábrelo en un navegador local de confianza si la vista previa bloquea los scripts.']
];

// Exact JavaScript string fragments from our own interface source; no user data.
const script = [
  ["'Dark theme'", "'Tema oscuro'"], ["'Light theme'", "'Tema claro'"],
  ["'Clipboard unavailable. Copy the selected text below.'", "'Portapapeles no disponible. Copia el texto seleccionado abajo.'"],
  ["'Copied. Paste into your AI agent when ready.'", "'Copiado. Pega las decisiones al agente de IA cuando quieras.'"],
  ["'Export requested. If this preview blocks downloads, copy decisions for your AI agent.'", "'Exportación solicitada. Si la vista previa bloquea descargas, copia las decisiones para tu agente de IA.'"],
  ["'Standards alignment'", "'Alineación con estándares'"], ["'Rule assessment coverage'", "'Cobertura de reglas evaluadas'"],
  ["'Files reviewed / inventoried'", "'Archivos revisados / identificados'"],
  ["'Project standards'", "'Estándares del proyecto'"], ["'Git statistics by evidence layer'", "'Estadísticas Git por capa'"],
  ["'Excluded or unavailable evidence'", "'Evidencia excluida o no disponible'"], ["'What is aligned'", "'Aspectos que cumplen'"],
  ["'Actual repository diff'", "'Diferencias reales del repositorio'"], ["' · old | new'", "' · anterior | nuevo'"], ["' · old/new lines'", "' · líneas anteriores/nuevas'"],
  ["'No textual diff'", "'Sin diferencias de texto'"], ["'No collected file evidence'", "'No hay evidencia de archivos recopilada'"],
  ["'Untracked'", "'Sin seguimiento'"], ["'Reviewed'", "'Revisado'"], ["'Not reviewed'", "'Sin revisar'"],
  ["'reviewed'", "'revisado'"], ["'not reviewed'", "'sin revisar'"],
  ["'No findings match these filters.'", "'Ningún hallazgo coincide con los filtros.'"],
  ["'Rule'", "'Regla'"], ["'Evidence'", "'Evidencia'"], ["'Impact'", "'Impacto'"], ["'Recommendation'", "'Recomendación'"], ["'Verification'", "'Verificación'"],
  ["'Severity basis'", "'Motivo de severidad'"], ["'Blocking reason'", "'Motivo de bloqueo'"],
  ["'View correction example'", "'Ver ejemplo de corrección'"],
  ["'Proposed example · not applied'", "'Ejemplo propuesto · no aplicado'"],
  ["'No code example available for this finding.'", "'No hay un ejemplo de código disponible para este hallazgo.'"],
  ["'Decision reason (required to reject)'", "'Motivo de la decisión (obligatorio al rechazar)'"],
  ["'Accept recommendation'", "'Aceptar recomendación'"], ["'Reject with reason'", "'Rechazar con motivo'"], ["'Defer'", "'Posponer'"],
  ["'Add a reason before rejecting this recommendation.'", "'Escribe un motivo antes de rechazar esta recomendación.'"],
  ["'Rule / dimension'", "'Regla / dimensión'"], ["'State'", "'Estado'"], ["'Source / criterion'", "'Fuente / criterio'"], ["'Evidence / reason'", "'Evidencia / motivo'"],
  ["'No validations executed. This is an evidence review only.'", "'No se ejecutaron validaciones. Esta revisión se basa en la evidencia disponible.'"],
  ["'No executed validation evidence supplied'", "'No se proporcionó evidencia de validación ejecutada'"],
  ["'No commit proposed for this scope. Ask your AI agent for a proposal if there are relevant changes.'", "'No se propuso un commit para este alcance. Si hay cambios relevantes, pide una propuesta a tu agente de IA.'"],
  ["'Copy commit message'", "'Copiar mensaje de commit'"], ["'View manual commands'", "'Ver comandos manuales'"], ["'Copy manual commands'", "'Copiar comandos manuales'"],
  ['Add a rejection reason for ${invalid.findingId} before exporting.', 'Añade un motivo de rechazo para ${invalid.findingId} antes de exportar.'],
  ['${data.status.blockers.length} blocking findings', '${data.status.blockers.length} hallazgos bloqueantes'],
  [' Minimum assessed coverage: ${data.score.minCoverage}% per applicable dimension. Decisions do not change this score.', ' Cobertura mínima evaluada: ${data.score.minCoverage}% por dimensión aplicable. Las decisiones no cambian esta puntuación.'],
  ['% weight · ${d.counts.passed} passed · ${d.counts.failed} failed · ${d.counts.unverified} unverified', '% de peso · ${d.counts.passed} cumplidas · ${d.counts.failed} incumplidas · ${d.counts.unverified} sin verificar'],
  ['Root: ${data.snapshot.root}', 'Raíz: ${data.snapshot.root}'],
  ['Local dirty state: ${data.snapshot.dirty ?', 'Cambios locales pendientes: ${data.snapshot.dirty ?'],
  ['Selected modules: ${data.snapshot.coverage.modules.join', 'Módulos seleccionados: ${data.snapshot.coverage.modules.join'],
  ['Renamed from ${file.previousPath}', 'Renombrado desde ${file.previousPath}'],
  ['Staged: ${file.staged', 'Preparado: ${file.staged'], ['Unstaged: ${file.unstaged', 'Sin preparar: ${file.unstaged'],
  ['Status: ${file.status', 'Estado: ${file.status'], ['File comment: ${f.id}', 'Comentario del archivo: ${f.id}'],
  ['${filtered.length} of ${data.findings.length} findings', '${filtered.length} de ${data.findings.length} hallazgos'],
  ['${f.id}: ${display(status)}. No code was changed.', '${f.id}: ${display(status)}. No se modificó el código.'],
  ['Decision: ${display(decisions.get(f.id).status)}', 'Decisión: ${display(decisions.get(f.id).status)}'],
  ['${display(f.confidence)} confidence', 'confianza ${display(f.confidence)}'],
];

function replace(source, pairs) {
  for (const [from, to] of pairs) {
    if (!source.includes(from)) throw new Error(`Missing localization template: ${from}`);
    source = source.replaceAll(from, to);
  }
  return source;
}

export function localizeHtmlTemplate(source, locale) {
  return locale === 'es' ? replace(source, html) : source;
}
export function localizeUiScript(source, locale) {
  return locale === 'es' ? replace(source, script) : source;
}
