# Diagram Engineering Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Selecciona, crea, modifica y valida diagramas técnicos en Mermaid y Draw.io
editable. Se concentra en la representación y su calidad; las decisiones de
arquitectura y la documentación completa pertenecen a otras Skills.

### Contexto

Ejecuta el prompt en el proyecto que deseas diagramar. `diagram-engineering`
incluye sus scripts, referencias y ejemplos visuales; no necesita instalar
`architecture-documentation`. La comprobación Draw.io requiere Python 3.10+;
el control de intentos también usa Python, sin paquetes adicionales. El parser Mermaid y los renderizadores
dependen de las herramientas disponibles en el entorno. Para infraestructura,
indica AWS, Azure, Google Cloud o IBM Cloud y las fuentes del modelo.
Mermaid CLI, si se utiliza, requiere su propio Node.js instalado; los controles
y la exportación Draw.io funcionan sin Node.js.

Reemplaza `<source-path>` por la ruta a una especificación o modelo existente,
y `<output-directory>` por un directorio dentro del proyecto. No se necesitan
archivos de una aplicación real para leer esta guía. El prompt siguiente sí
presupone que el usuario proporciona el modelo al ejecutarlo.

### Prompt de ejemplo

```text
Usa diagram-engineering con el modelo de <source-path>.
Crea únicamente software-components y sequence, ambos en Mermaid y Draw.io
editable, en <output-directory>. Usa español en las etiquetas.
Conserva los componentes, relaciones y orden definidos en el modelo; señala
las incógnitas. Usa los recursos locales de la Skill para íconos, estilos,
colisiones y validación Draw.io. No elijas proveedor ni rediseñes el sistema.
Valida con las herramientas disponibles y entrega el inventario de íconos,
la correspondencia entre formatos y los resultados reales de cada comprobación.
No modifiques código ni configuración. No abras Draw.io Desktop para renderizar.
```

### Resultado esperado

Dos vistas seleccionadas, cada una con `.mmd` y `.drawio`, más un registro breve
de evidencia, íconos, validaciones y limitaciones. Cada pareja representa el
mismo modelo; las vistas de componentes y secuencia responden preguntas distintas.
Las comprobaciones de renderizado no disponibles se declaran sin afirmar éxito.
Si se autoriza una vista previa en otro encargo, cada archivo tiene un intento
por renderizador. Tras el primer fallo de Draw.io o Mermaid, no se vuelve a
intentar esa herramienta durante el encargo; continúan los controles estáticos.

### Criterios de revisión

- Se entregan solo las dos vistas y los dos formatos solicitados.
- Los íconos Draw.io son verificables o tienen un símbolo genérico justificado;
  nodos, etiquetas y conectores siguen siendo editables.
- Cada pareja mantiene componentes, relaciones y significado; la secuencia
  conserva participantes, mensajes, respuestas y orden suministrados.
- Las rutas y etiquetas evitan superposiciones; el texto es legible y las rutas
  automáticas o posiciones no verificadas se informan como limitaciones.
- Se distinguen sintaxis, estructura, semántica, recursos, equivalencia y revisión
  visual; no se presenta un control no ejecutado como aprobado.

### Selección guiada y uso desde agentes

Para recibir recomendaciones, usa: “Usa diagram-engineering para recomendar
diagramas a partir de <source-path>; presenta opciones por categoría y deja
que seleccione los tipos y Mermaid, Draw.io o ambos antes de generar”.

Un agente como `backend-engineer` o `frontend-engineer`, o un futuro
`software-architect`, puede cargar `skill/diagram-engineering` y entregar:

```text
objective: Explain the supplied model
source: <source-path>
diagram_types: [software-components, sequence]
formats: both
output_directory: <output-directory>
language: Spanish
status: supplied model; preserve its evidence labels
allowed_effects: write selected diagrams only; no application edits or Desktop launch
```

Este bloque es una descripción del encargo, no una API ni un comando ejecutable.
No vuelve a pedir selecciones ya definidas. El agente recibe rutas, cambios,
incógnitas, inventario y resultados; referenciar una Skill no instala ni registra
un agente, y no amplía sus permisos.

### Estado de ejecución

Escenarios ilustrativos; no se ejecutaron estos prompts ni se generaron diagramas
de una aplicación real durante la creación de la Skill. Las comprobaciones de
autoría y de reutilización se registran por separado en el repositorio.

## English

### About this Skill

Selects, creates, modifies and validates technical diagrams in Mermaid and editable
Draw.io. It owns representation and diagram quality; architecture decisions and
comprehensive documentation belong to other Skills.

### Context

Run the prompt in the project to diagram. `diagram-engineering` bundles its
scripts, references and visual examples; installing `architecture-documentation`
is unnecessary. Draw.io checking needs Python 3.10+; the attempt guard uses
Python's standard library. The Mermaid parser and renderers depend on the environment's
available tools. For infrastructure, specify AWS, Azure, Google Cloud or IBM Cloud
and the model's sources.
Mermaid CLI, if used, requires its own installed Node.js; checking and Draw.io
export work without Node.js.

Replace `<source-path>` with an existing specification/model path, and
`<output-directory>` with a directory inside the project. Reading this guide
does not require real application files. Executing the following prompt does
require a user-supplied model.

### Example prompt

```text
Use diagram-engineering with the model at <source-path>.
Create only software-components and sequence, each in Mermaid and editable
Draw.io, in <output-directory>. Use English labels.
Preserve the model's components, relationships and order; identify unknowns.
Use the Skill's local resources for icons, styles, collisions and Draw.io
validation. Do not select a provider or redesign the system.
Validate with available tools and deliver the icon inventory, correspondence
between formats and actual results of each check.
Do not modify code or configuration. Do not launch Draw.io Desktop for rendering.
```

### Expected result

Two selected views, each with `.mmd` and `.drawio`, plus a concise evidence, icon,
validation and limitation record. Each pair represents the same model; component
and sequence views answer different questions. Unavailable rendering checks are
disclosed without claiming success.
If a preview is authorized in another task, each file gets one attempt per
renderer. After the first Draw.io or Mermaid failure, that tool is not attempted
again during the task; static checks continue.

### Review criteria

- Only the two selected views and both requested formats are delivered.
- Draw.io icons are verifiable or use a justified generic symbol; nodes, labels
  and connectors remain editable.
- Each pair preserves components, relationships and meaning; sequence preserves
  supplied participants, messages, returns and order.
- Routes and labels avoid overlaps; text is legible and unverified automatic
  routes or label positions are disclosed as limitations.
- Syntax, structure, semantics, resources, equivalence and visual review are
  distinguished; an unexecuted check is never presented as passed.

### Guided selection and agent use

For recommendations, use: “Use diagram-engineering to recommend diagrams from
<source-path>; present options by category and let me select types and Mermaid,
Draw.io or both before generating”.

An agent such as `backend-engineer` or `frontend-engineer`, or a future
`software-architect`, can load `skill/diagram-engineering` and supply:

```text
objective: Explain the supplied model
source: <source-path>
diagram_types: [software-components, sequence]
formats: both
output_directory: <output-directory>
language: English
status: supplied model; preserve its evidence labels
allowed_effects: write selected diagrams only; no application edits or Desktop launch
```

This block describes a handoff, not an API or executable command. Defined
selections are not requested again. The agent receives paths, changes, unknowns,
inventory and results; a Skill reference does not install/register an agent or
expand its permissions.

### Execution status

Illustrative scenarios; these prompts were not executed and no real application
diagrams were generated during Skill creation. Authoring and resource-reuse
checks are recorded separately in the repository.
