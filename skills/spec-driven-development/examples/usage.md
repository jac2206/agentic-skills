# Spec-Driven Development Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Gestiona cambios de software mediante especificaciones, planificación, implementación, verificación y cierre proporcionales. Conserva la fuente de verdad y las convenciones del proyecto.

### Contexto

Abre una aplicación con listado de tickets existente y los registros de cambios
activos disponibles. Si falta esa funcionalidad, el análisis debe señalarlo.

### Prompt de ejemplo

```text
Usa la Skill spec-driven-development en modo Analyze para este cambio propuesto:
agregar un filtro opcional de estado al listado de tickets existente, preservando
el comportamiento actual cuando no se proporciona filtro.
Inspecciona implementación, instrucciones, especificaciones y cambios activos.
Identifica comportamiento esperado, áreas afectadas, decisiones pendientes,
seguridad pertinente y las etapas mínimas de especificación, implementación y
verificación. Devuelve hallazgos y plan recomendado con rutas de evidencia.
No edites archivos, implementes el filtro, instales OpenSpec ni crees otro cambio.
```

### Resultado esperado

Un diagnóstico de cambio de solo lectura y una selección justificada de etapas
usando la fuente de verdad existente, con requisitos y comprobaciones pendientes explícitos.

### Criterios de revisión

- Se descubren los cambios activos antes de proponer uno nuevo.
- Se identifica comportamiento con y sin filtro sin inventar valores de estado.
- La verificación propuesta se relaciona con la solicitud y las rutas afectadas reales.
- Analyze no modifica archivos ni el estado del ciclo de especificación.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Los [escenarios de cambio](change-scenarios.md) describen otros procesos proporcionales.

## English

### About this Skill

Manages software changes through proportionate specifications, planning, implementation, verification and closure. It preserves the project's source of truth and conventions.

### Context

Open an application with an existing ticket-list feature and any active change
records. If that feature is absent, the analysis should report the missing context.

### Example prompt

```text
Use the spec-driven-development Skill in Analyze mode for this proposed change:
add an optional status filter to the existing ticket list while preserving the
current behavior when no filter is supplied.
Inspect the implementation, project instructions, specifications and active changes.
Identify expected behavior, affected areas, open decisions, relevant security
concerns, and the smallest useful specification, implementation and verification
stages. Return findings and a recommended plan with evidence paths.
Do not edit files, implement the filter, install OpenSpec, or create another change.
```

### Expected result

A read-only change diagnosis and justified stage selection using the project's
existing source of truth, with unresolved requirements and checks made explicit.

### Review criteria

- Existing change records are discovered before proposing a new change.
- Filtered and unfiltered behavior are identified without inventing status values.
- Proposed verification traces to the requested behavior and actual affected paths.
- Analyze mode leaves files and specification lifecycle state unchanged.

### Execution status

Illustrative scenario; not executed as part of this documentation change. The
[change scenarios](change-scenarios.md) describe other proportional workflows.
