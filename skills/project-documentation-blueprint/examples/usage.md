# Project Documentation Blueprint Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Convierte la evidencia de un proyecto en un Project Blueprint visual y navegable en HTML. Explica problema, solución, arquitectura, capacidades y límites de evidencia para distintos públicos.

### Contexto

Abre la aplicación de destino con la documentación y código disponibles. Las capturas,
evidencia de despliegue y análisis anteriores son opcionales; no se asume que existan.

### Prompt de ejemplo

```text
Usa la Skill project-documentation-blueprint sobre la aplicación actual.
Crea un Project Blueprint en español para líderes técnicos e interesados del proyecto.
Explica el problema, solución, alcance, flujo principal, arquitectura, tecnología y
capacidades sustentados. Distingue evidencia documentada, verificada, inferida y faltante.
Guarda solo examples/docs/project-blueprint.html usando el estilo visual predeterminado,
navegación por secciones y estilos de impresión. No crees diapositivas ni PDF,
cambies código o inventes capturas, estado de despliegue o métricas.
```

### Resultado esperado

Un HTML navegable cuya portada identifica el proyecto real y cuya narrativa visual
explica tanto las capacidades sustentadas como las lagunas de evidencia.

### Criterios de revisión

- Las afirmaciones relevantes y relaciones de diagramas remiten a evidencia.
- La portada destaca PROJECT BLUEPRINT y la identidad real del proyecto.
- Las secciones construyen una narrativa concisa en lugar de un inventario de archivos.
- Se comprueban navegación, adaptación e impresión cuando hay herramientas;
  las revisiones visuales no disponibles se informan.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Al escribir esta guía no se generó ni se inspeccionó visualmente un Blueprint.

## English

### About this Skill

Turns project evidence into a visual, navigable HTML Project Blueprint. It explains the problem, solution, architecture, capabilities and evidence limits for different audiences.

### Context

Open the target application with available documentation and source. Screenshots,
deployment evidence and prior analyses are optional, not assumed present.

### Example prompt

```text
Use the project-documentation-blueprint Skill on the current application.
Create an English Project Blueprint for technical leads and project stakeholders.
Explain the evidenced problem, solution, scope, main flow, architecture, technology
and capabilities. Label documented, verified, inferred and missing evidence.
Save only examples/docs/project-blueprint.html with the Skill's default visual
language, section navigation and print styles. Do not create a slide deck or PDF,
change application code, or invent screenshots, deployment status or metrics.
```

### Expected result

One navigable HTML Blueprint whose cover identifies the actual project and whose
visual narrative makes both supported capabilities and evidence gaps clear.

### Review criteria

- Material claims and diagram relationships trace to project evidence.
- The cover leads with PROJECT BLUEPRINT and the actual project identity.
- Sections form a concise narrative instead of an exhaustive file inventory.
- Navigation, responsive layout and print behavior are checked when tools allow;
  unavailable visual checks are explicitly reported.

### Execution status

Illustrative scenario; not executed as part of this documentation change. No
Blueprint was generated or visually inspected while writing this guide.
