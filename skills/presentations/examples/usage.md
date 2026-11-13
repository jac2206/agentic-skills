# HTML Presentations Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Transforma un tema o material suministrado en una presentación HTML autocontenida, con narrativa, diseño visual y controles de navegación. Su nombre declarado es html-presentations y su carpeta es presentations.

### Contexto

El esquema del prompt es el material suministrado para una presentación educativa
breve. La ruta de salida es relativa al espacio de trabajo de destino, no a la Skill
instalada. El nombre declarado es html-presentations; la carpeta es presentations.

### Prompt de ejemplo

```text
Usa la Skill html-presentations para crear cinco diapositivas en español para desarrolladores.
Tema: revisar una propuesta de arquitectura de software antes de implementarla.
Usa este esquema: propósito y restricciones; evidencia y supuestos; límites de
componentes; decisiones y alternativas; lista de revisión y próximas decisiones.
Usa el tema predeterminado de la Skill y una idea clara por diapositiva. Incluye un
diagrama de proceso sencillo cuando aporte valor, sin inventar métricas ni productos.
Guarda un HTML autocontenido en examples/presentations/architecture-review.html.
Comprueba los límites y la navegación; informa qué revisiones de navegador no realizaste.
```

### Resultado esperado

Una presentación HTML autocontenida con escenario 16:9, una diapositiva visible
a la vez, navegación, escalado adaptable y manejo de movimiento reducido.

### Criterios de revisión

- Las cinco diapositivas siguen el esquema sin afirmaciones factuales no sustentadas.
- Textos, diagramas y controles caben en el escenario y son legibles.
- Anterior/siguiente, teclado e indicador de progreso funcionan cuando se comprueban.
- La inspección del código se distingue de la revisión visual y funcional.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Al escribir esta guía no se generó una presentación ni se probó su comportamiento.

## English

### About this Skill

Turns a topic or supplied material into a self-contained HTML slide deck with narrative, visual design and presentation controls. Its declared name is html-presentations; its package directory is presentations.

### Context

The outline below is supplied source material for a short educational deck.
The output path is relative to the target workspace, not the installed Skill.

### Example prompt

```text
Use the html-presentations Skill to create a five-slide English deck for developers.
Topic: reviewing a software architecture proposal before implementation.
Use this outline: purpose and constraints; evidence and assumptions; component
boundaries; trade-offs; review checklist and next decisions.
Use the Skill's default theme and one clear idea per slide. Include a simple
process diagram where useful, without inventing metrics or product examples.
Save a self-contained deck at examples/presentations/architecture-review.html.
Check slide bounds and navigation; disclose any browser checks not performed.
```

### Expected result

One self-contained HTML deck with a 16:9 stage, one visible slide at a time,
navigation, responsive scaling and reduced-motion handling.

### Review criteria

- The five slides follow the supplied outline without unsupported factual claims.
- Text, diagrams and controls fit the stage and remain legible.
- Previous/next, keyboard navigation and progress work when actually checked.
- Source inspection and rendered/runtime checks are reported separately.

### Execution status

Illustrative scenario; not executed as part of this documentation change. No deck
was generated or browser behavior tested while writing this guide.
