# Backend Documentation Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Documenta el comportamiento implementado de un backend a partir de su código. Reconstruye casos de uso, flujos, integraciones y efectos, respetando las convenciones documentales del proyecto.

### Contexto

Abre un backend existente y sustituye <implemented-use-case> por un caso de uso
o endpoint real. Deja accesibles su documentación y plantillas locales.

### Prompt de ejemplo

```text
Usa la Skill backend-documentation para <implemented-use-case> en este espacio de trabajo.
Traza su entrada real, validación, autorización, lógica de aplicación y dominio,
persistencia, integraciones, efectos secundarios y respuesta donde estén implementados.
Crea o actualiza docs/main.md y el documento del caso de uso dentro de la ubicación
de documentación existente, siguiendo la plantilla y las reglas de diagramas locales.
Limita los cambios a la documentación pertinente. Registra rutas de evidencia,
conflictos e incógnitas; no inventes comportamiento ni cambies código de la aplicación.
```

### Resultado esperado

Una visión general y un documento de caso de uso sustentados y enlazados de forma
consistente. Se incluye o actualiza el diagrama cuando la Skill y las convenciones
del proyecto lo requieren.

### Criterios de revisión

- Rutas, campos, errores y efectos coinciden con la evidencia de implementación.
- Se respetan la estructura documental y las plantillas locales.
- Los diagramas coinciden con el flujo descrito y no contienen pasos inventados.
- Los conflictos de especificación se señalan sin cambiar su intención silenciosamente.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Los [ejemplos de uso](../references/usage-examples.md) cubren otros casos de evidencia.

## English

### About this Skill

Documents implemented backend behavior from source evidence. It reconstructs use cases, flows, integrations and effects while respecting the project's documentation conventions.

### Context

Open an existing backend and replace `<implemented-use-case>` with an actual
use case or endpoint. Make its existing documentation and local templates available.

### Example prompt

```text
Use the backend-documentation Skill for <implemented-use-case> in this workspace.
Trace its real entry point, validation, authorization, application/domain logic,
persistence, integrations, side effects and response where implemented.
Create or update docs/main.md and the scoped use-case document in the project's
existing documentation location, following its local template and diagram rules.
Keep changes limited to relevant documentation. Record evidence paths, conflicts
and unknowns; do not invent behavior or change application code.
```

### Expected result

An evidence-based overview and use-case document, linked consistently. Include or
update the flow diagram when the Skill and project conventions call for one.

### Review criteria

- Routes, fields, errors and side effects match implementation evidence.
- Existing documentation structure and local templates are respected.
- Diagrams agree with the described execution path and contain no invented steps.
- Conflicting specifications are identified without silently changing their intent.

### Execution status

Illustrative scenario; not executed as part of this documentation change. See
[usage examples](../references/usage-examples.md) for additional evidence cases.
