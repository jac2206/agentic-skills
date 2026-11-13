# Skill Factory Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Diseña, crea, revisa y mejora Skills reutilizables. Ayuda a elegir la abstracción más sencilla y mantiene claras sus responsabilidades, recursos, guías de uso y criterios de calidad.

### Contexto

Sustituye <skill-directory> por un paquete real con SKILL.md y sus recursos.
Este ejemplo solicita únicamente evaluación.

### Prompt de ejemplo

```text
Usa la Skill skill-factory para evaluar <skill-directory> sin modificar archivos.
Revisa responsabilidad reutilizable, condiciones de selección, entradas y salidas,
reglas coherentes, límites de composición y criterios de calidad medibles.
Inspecciona las plantillas, ejemplos y scripts referenciados cuando corresponda.
Devuelve hallazgos priorizados con rutas de evidencia, impacto y correcciones concretas.
Distingue calidad de las instrucciones y evidencia de ejecución observada; declara
la validación de comportamiento faltante. No asignes una nota numérica ni ejecutes la capacidad.
```

### Resultado esperado

Una evaluación sustentada con recomendaciones accionables y una explicación clara
de recursos inspeccionados, comportamiento no verificado y abstracción elegida.

### Criterios de revisión

- Los hallazgos citan la definición o sus recursos, no preferencias genéricas.
- Las recomendaciones preservan la responsabilidad y comportamiento válidos.
- Los escenarios documentados no se presentan como pruebas funcionales aprobadas.
- La evaluación no cambia archivos, versiones ni copias instaladas.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Esta guía no es un informe de evaluación de una Skill concreta.

## English

### About this Skill

Designs, creates, reviews and improves reusable Skills. It helps choose the smallest sufficient abstraction and keeps responsibilities, resources, usage guides and quality criteria clear.

### Context

Replace `<skill-directory>` with a real package containing `SKILL.md` and its
supporting resources. This example requests evaluation only.

### Example prompt

```text
Use the skill-factory Skill to evaluate <skill-directory> without changing files.
Check whether it has one reusable responsibility, clear selection conditions,
inputs and outputs, coherent rules, composition boundaries and measurable quality.
Inspect its referenced templates, examples and scripts where relevant.
Return prioritized findings with evidence paths, impact and concrete corrections.
Distinguish instruction quality from observed execution evidence, disclose missing
behavioral validation, and do not assign a numeric score or run the capability.
```

### Expected result

An evidence-based evaluation with actionable recommendations and a clear account
of inspected resources, unverified behavior and the chosen abstraction.

### Review criteria

- Findings cite the actual definition or resources rather than generic preferences.
- Recommendations preserve the Skill's valid responsibility and behavior.
- Documented scenarios are not presented as passed functional tests.
- No files, versions or installed copies are changed by this evaluation.

### Execution status

Illustrative scenario; not executed as part of this documentation change. This
guide is not an evaluation report for a particular Skill.
