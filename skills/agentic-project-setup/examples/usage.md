# Agentic Project Setup Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Analiza y prepara repositorios para colaborar con agentes de IA, conservando su estructura y convenciones. Identifica mejoras de contexto e instrucciones antes de aplicarlas.

### Contexto

Abre el repositorio de destino con su código e instrucciones existentes accesibles.
El modo Analyze es de solo lectura; este ejemplo no aplica la preparación propuesta.

### Prompt de ejemplo

```text
Usa la Skill agentic-project-setup en modo Analyze sobre el repositorio actual.
Inspecciona sus instrucciones, estructura, documentación, comprobaciones disponibles
y configuración de agentes existente. Evalúa la aplicabilidad de cada dimensión.
Identifica qué conservar o mejorar, con rutas de evidencia y hallazgos priorizados.
Devuelve el plan mínimo de preparación útil y señala la evidencia no disponible.
No edites archivos, instales dependencias ni crees agentes o configuración.
```

### Resultado esperado

Un perfil del repositorio, una evaluación de aplicabilidad, hallazgos sustentados
y un plan priorizado que preserve la estructura existente.

### Criterios de revisión

- Los hallazgos citan archivos reales sin asumir un framework o una estructura.
- Las dimensiones no aplicables se explican sin generar carpetas de relleno.
- Las propuestas y afirmaciones no verificadas se distinguen de los hechos observados.
- El repositorio de destino permanece sin cambios.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
El [ejemplo de diagnóstico](diagnosis-and-minimal-setup.md) muestra un seguimiento
acotado para aplicar la preparación.

## English

### About this Skill

Assesses and prepares repositories for AI-agent collaboration while preserving established structure and conventions. It identifies context and instruction improvements before applying them.

### Context

Open the target repository with its source and existing instructions accessible.
Analyze mode is read-only; this example does not apply the recommended setup.

### Example prompt

```text
Use the agentic-project-setup Skill in Analyze mode on the current repository.
Inspect its instructions, structure, documentation, available checks and existing
agent configuration. Assess each evaluation dimension for applicability.
Identify what to keep or improve, with evidence paths and prioritized findings.
Return the smallest useful preparation plan and disclose unavailable evidence.
Do not edit files, install dependencies, or create agents or configuration.
```

### Expected result

A repository profile, applicability assessment, evidence-based findings and a
prioritized improvement plan that preserves the established structure.

### Review criteria

- Findings cite actual files rather than assuming a framework or directory layout.
- Non-applicable dimensions are explained without generating placeholder folders.
- Proposed changes and unverified claims are distinguishable from observed facts.
- The target repository remains unchanged.

### Execution status

Illustrative scenario; not executed as part of this documentation change. See the
[diagnosis example](diagnosis-and-minimal-setup.md) for a bounded setup follow-up.
