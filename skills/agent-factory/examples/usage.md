# Agent Factory Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Diseña, crea, mejora y valida definiciones reutilizables de agentes. Ayuda a decidir si un agente está justificado y cómo reutilizar Skills; no instala ni ejecuta agentes.

### Contexto

Abre un espacio de trabajo con sus contratos de autoría, plantilla de agente y
Skills existentes, o proporciona sus equivalentes autorizados. Este ejemplo usa
el modo Recommend y devuelve una respuesta sin crear un agente.

### Prompt de ejemplo

```text
Usa la Skill agent-factory en modo Recommend para este espacio de trabajo.
Revisamos propuestas de arquitectura de forma recurrente. Cada revisión necesita
contexto independiente para seleccionar capacidades de arquitectura y seguridad
pertinentes y consolidar los hallazgos.
Evalúa si esta responsabilidad requiere un agente o una abstracción más sencilla.
Inspecciona las Skills disponibles y explica la responsabilidad, las oportunidades
de reutilización, las entradas, las acciones permitidas y las capacidades faltantes.
No crees archivos, ejecutes otro agente ni implementes una integración.
```

### Resultado esperado

Una recomendación justificada sobre la abstracción, con referencias a capacidades,
límites de autoridad y requisitos pendientes. Recomendar una opción más sencilla
también es válido.

### Criterios de revisión

- La recomendación identifica necesidades reales de juicio o aislamiento.
- Las Skills se resuelven por su nombre declarado y no se copian sus procedimientos.
- La evidencia faltante es explícita; no se afirma ejecución ni compatibilidad.
- Este escenario Recommend no modifica archivos del espacio de trabajo.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Consulta los [escenarios de validación](../references/validation-scenarios.md)
para otros casos de revisión.

## English

### About this Skill

Designs, creates, improves and validates reusable agent definitions. It checks whether an agent is justified and how to reuse Skills; it does not install or execute agents.

### Context

Open a workspace containing its authoring contracts, agent template and existing
Skills, or provide their authoritative equivalents. This example uses Recommend
mode and returns a response without creating an agent.

### Example prompt

```text
Use the agent-factory Skill in Recommend mode for this workspace.
We repeatedly review architecture proposals. Each review needs independent context
to select relevant architecture and security capabilities and consolidate findings.
Assess whether this responsibility needs an agent or a simpler abstraction.
Inspect the available Skills and explain the responsibility, reuse opportunities,
required inputs, permitted actions, and missing host capabilities.
Do not create files, execute another agent, or implement an integration.
```

### Expected result

A justified abstraction recommendation, relevant capability references, authority
boundaries and unresolved prerequisites. Recommending a simpler option is valid.

### Review criteria

- The recommendation identifies actual judgment or isolation needs.
- Referenced Skills resolve by declared name and their procedures are not copied.
- Missing evidence is explicit; no agent execution or compatibility is claimed.
- No workspace files are changed by this Recommend scenario.

### Execution status

Illustrative scenario; not executed as part of this documentation change. For
additional review cases, see [validation scenarios](../references/validation-scenarios.md).
