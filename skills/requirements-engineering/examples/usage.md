# Requirements Engineering Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Convierte necesidades y requisitos suministrados en un backlog trazable con historias, criterios de aceptación, reglas y estados de preparación. Hace visibles las decisiones de negocio pendientes.

### Contexto

El prompt proporciona un requisito pequeño sobre devoluciones en una biblioteca.
El contexto de producto y los identificadores existentes pueden suministrarse
por separado; no se asume que existan.

### Prompt de ejemplo

```text
Usa la Skill requirements-engineering en modo Draft para este requisito:
Un bibliotecario puede registrar la devolución de un libro con su identificador de
inventario. Se rechaza un identificador desconocido. Una devolución ya registrada
no debe registrarse por segunda vez.
Crea un backlog Markdown en español en backlog/ con solo la jerarquía sustentada.
Incluye historias enfocadas, criterios Given/When/Then, reglas explícitas,
trazabilidad al requisito y estado de preparación. Marca los IDs nuevos como provisionales.
Lista preguntas pendientes sobre roles, respuestas y políticas de circulación;
no inventes cargos, permisos o reglas de préstamo ni implementes software.
```

### Resultado esperado

Un backlog pequeño en borrador basado en las reglas suministradas, con criterios
verificables, incertidumbres visibles y niveles de épica/funcionalidad solo si se justifican.

### Criterios de revisión

- Se cubren devolución normal, identificador desconocido y devolución ya registrada.
- Las políticas no sustentadas quedan como preguntas, no como requisitos aprobados.
- IDs, relaciones padre e identificadores de fuente son consistentes donde aplican.
- La preparación refleja las decisiones pendientes, no solo el formato del documento.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Al escribir esta guía no se creó un backlog ni una implementación.

## English

### About this Skill

Turns supplied needs and requirements into a traceable backlog with stories, acceptance criteria, rules and readiness states. It makes unresolved business decisions visible.

### Context

The prompt supplies a small library-return requirement. Existing product context
or IDs may be supplied separately; do not assume that they exist.

### Example prompt

```text
Use the requirements-engineering Skill in Draft mode for this supplied requirement:
A librarian can record a returned book using its inventory ID. An unknown ID is
rejected. A return already recorded must not be recorded a second time.
Create an English Markdown backlog under backlog/ using only supported hierarchy.
Include focused user stories, Given/When/Then criteria, explicit business rules,
source traceability and readiness status. Mark any assigned IDs as provisional.
List unresolved questions about roles, responses and related circulation policy;
do not invent fees, permissions or borrowing rules, and do not implement software.
```

### Expected result

A small draft backlog grounded in the supplied rules, with testable acceptance
criteria, visible uncertainties and only justified epic/feature levels.

### Review criteria

- Normal return, unknown ID and already-recorded return are covered.
- Unsupported policies remain questions rather than approved requirements.
- IDs, parent relationships and source references are consistent where applicable.
- Readiness reflects unresolved decisions rather than document formatting alone.

### Execution status

Illustrative scenario; not executed as part of this documentation change. No
backlog files or implementation were produced while writing this guide.
