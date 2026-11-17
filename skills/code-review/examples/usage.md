# Code Review Usage

**Idioma / Language:** [Español](#español) | [English](#english)

Operational instructions: [Code Review](../SKILL.md).

## Español

### Descripción

Revisa cambios locales, ramas o módulos contra las reglas reales del proyecto.
Entrega evidencia, puntuación justificable y un HTML temporal para decidir qué
recomendaciones atender. No modifica código ni ejecuta escrituras Git.

### Contexto

Abre el proyecto objetivo en Codex y proporciona esta Skill con todos sus recursos.
Para los módulos incluidos necesitas Node.js 20+ y Git; no hay dependencias nuevas.
Reemplaza `<backend-path>`, `<base-branch>` y `<module-path>` por valores reales.
El HTML se crea en el temporal del sistema, fuera del backend. Si no has elegido
idioma, la Skill te preguntará: español, inglés u otro que puedas escribir. Para
otro idioma, el contenido se redacta en ese idioma y la interfaz usa inglés; la
Skill informará de esta limitación. Los mensajes de commit siempre van en inglés.

### Prompt de ejemplo

```text
Usa $code-review en <backend-path> en modo Quick Review. Inspecciona AGENTS.md,
especificaciones y convenciones del proyecto. Incluye staged, unstaged y untracked
relevantes, con hallazgos verificables y Quality Score. Genera el HTML temporal
    offline en español con Commit Advisor y exportación de decisiones. No modifiques el proyecto
ni ejecutes operaciones Git de escritura. Informa ruta, cobertura y checks reales.
```

Variantes equivalentes:

```text
Usa $code-review en <backend-path> en modo Pull Request Review con base
<base-branch>. Compara desde merge-base, separa el estado local y genera el HTML
temporal. No modifiques código ni ejecutes escrituras Git.
```

```text
Usa $code-review en <backend-path> en modo Full Code Audit, limitado inicialmente
a <module-path>. Declara módulos y archivos cubiertos, deuda existente y evidencia
no verificada. Genera el HTML temporal sin modificar el proyecto ni escribir Git.
```

### Resultado esperado

Ruta exacta a un HTML independiente con dashboard, cobertura, reglas, hallazgos,
diffs reales, validaciones y propuesta de commits. `Accept recommendation`,
`Reject with reason` y `Defer` guardan decisiones en la sesión del HTML; usa
`Copy decisions for Codex` o exporta JSON y pégalo/entrégalo a Codex antes de cerrar.
Aceptar no aplica correcciones. Confirma explícitamente el fin de la revisión
antes de pedir su limpieza. Markdown/JSON de resultados son opcionales y temporales.

### Criterios de revisión

- Estados staged/unstaged/untracked, ramas y merge-base correctos.
- Hallazgos con evidencia real y lados/líneas correctos; sin secretos completos.
- Puntuación calculada, cobertura visible y `Not assessed` cuando falta evidencia.
- Filtros, navegación y decisiones funcionan; exportación identifica revisión y snapshot.
- Commit Advisor refleja las convenciones; Commitlint solo aparece validado si se ejecutó.
- Proyecto intacto y reporte conservado hasta confirmación explícita de cierre.

### Estado de ejecución

Prompts ilustrativos; todavía no se han ejecutado sobre un backend real. Las pruebas
automatizadas usan fixtures sintéticos; consulta el [registro](../references/validation.md)
para resultados reales y límites. Piloto propuesto: un backend real con un cambio
de endpoint, su prueba y un archivo nuevo no relacionado; ejecutar primero Quick
Review, decidir/exportar, después PR contra su base real y finalmente auditar un
módulo. Comparar reglas, cobertura y estado Git antes/después sin aplicar fixes.

## English

### About this Skill

Review local changes, branches or modules against actual project rules. Produce
evidence, justified alignment scores and temporary HTML for recommendation
decisions. It never changes code or executes Git writes.

### Context

Open the target project in Codex and make this Skill and its bundled resources
available. Included modules need Node.js 20+ and Git; no new dependencies are needed.
Replace `<backend-path>`, `<base-branch>` and `<module-path>` with actual values.
HTML goes to system temporary storage outside the backend. If no language has been
selected, the Skill will ask: Spanish, English or another language you can enter.
For another language, the assessment uses that language and the interface falls
back to English; the Skill will disclose this limitation. Proposed commit messages
are always written in English.

### Example prompt

```text
Use $code-review on <backend-path> in Quick Review mode. Inspect AGENTS.md,
specifications and project conventions. Include relevant staged, unstaged and
untracked changes, verifiable findings and a Quality Score. Generate temporary
offline HTML in Spanish with Commit Advisor and decision export. Do not modify the project
or execute Git writes. Report the exact path, coverage and actual checks.
```

Equivalent variants:

```text
Use $code-review on <backend-path> in Pull Request Review mode with base
<base-branch>. Compare from merge-base, separate local dirty state and generate
temporary HTML. Do not modify code or execute Git writes.
```

```text
Use $code-review on <backend-path> in Full Code Audit mode, initially limited to
<module-path>. Declare covered modules/files, existing debt and unverified
evidence. Generate temporary HTML without modifying the project or writing Git.
```

### Expected result

An exact path to self-contained HTML with dashboard, coverage, rules, findings,
actual diffs, validations and commit proposals. `Accept recommendation`,
`Reject with reason` and `Defer` retain decisions in the HTML session; use
`Copy decisions for Codex` or export JSON and paste/provide it to Codex before
closing. Acceptance applies no corrections. Explicitly confirm review completion
before requesting cleanup. Markdown/JSON result exports are optional and temporary.

### Review criteria

- Correct staged/unstaged/untracked states, branches and merge-base.
- Findings have actual evidence and correct sides/lines; no complete secrets.
- Computed score, visible coverage and `Not assessed` for insufficient evidence.
- Working filters/navigation/decisions; export identifies the review and snapshot.
- Commit Advisor reflects conventions; Commitlint is validated only if actually run.
- Target stays intact and the report remains until explicit completion confirmation.

### Execution status

Illustrative prompts; not yet executed on a real backend. Automated tests use
synthetic fixtures; see the [record](../references/validation.md) for actual results
and limits. Proposed pilot: a real backend with an endpoint change, its test and
an unrelated new file; first run Quick Review and export decisions, then PR against
the actual base, then audit one module. Compare rules, coverage and Git state
before/after without applying fixes.
