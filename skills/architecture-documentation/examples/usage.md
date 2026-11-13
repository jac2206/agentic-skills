# Architecture Documentation Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Crea documentación de arquitectura sustentada en evidencia, con vistas complementarias de componentes e infraestructura. Genera Mermaid, Draw.io editable y salida nativa de Archify cuando su Skill está disponible.

### Contexto

Abre un repositorio de aplicación con código accesible o proporciona una
especificación de arquitectura. Una solicitud de un solo diagrama puede ser menor
que este ejemplo de paquete completo. Archify es opcional y requiere que su Skill
esté instalada y pueda utilizarse.

### Prompt de ejemplo

```text
Usa la Skill architecture-documentation para documentar esta aplicación en español.
Inspecciona solo el espacio de trabajo actual y guarda el resultado en docs/architecture/.
Crea el paquete completo: architecture.md, vistas de componentes equivalentes en
Mermaid y Draw.io editable, y una vista separada de infraestructura AWS en Draw.io.
Marca el destino AWS como propuesto salvo que exista evidencia de despliegue.
Incluye salida nativa de Archify cuando su Skill instalada esté disponible.
Registra evidencia, incógnitas y comprobaciones realmente realizadas. No cambies
código ni configuración de despliegue y no abras Draw.io Desktop para renderizar.
```

### Resultado esperado

Un documento enlazado con diagramas complementarios de componentes e infraestructura,
separando los hechos actuales de las propuestas. Se informa explícitamente el estado
de Archify y las comprobaciones no disponibles.

### Criterios de revisión

- Las vistas de componentes coinciden; la infraestructura describe el despliegue.
- Las relaciones relevantes tienen evidencia o una etiqueta de propuesta/incógnita.
- Los iconos del proveedor y las comprobaciones estructurales siguen la Skill.
- Los artefactos faltantes o controles bloqueados se declaran sin afirmar finalización.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
El [paquete de referencia](reference-application/architecture.md) es otro ejemplo;
no demuestra que este prompt se haya ejecutado.

## English

### About this Skill

Creates evidence-based architecture documentation with complementary component and infrastructure views. It produces Mermaid, editable Draw.io and native Archify output when that Skill is available.

### Context

Open an application repository with inspectable source or supply an architecture
specification. Diagram-only requests can be smaller than this full-package example.
Optional Archify output depends on that Skill being installed and usable.

### Example prompt

```text
Use the architecture-documentation Skill to document this application in English.
Inspect only the current workspace and use docs/architecture/ for the output.
Create the complete package: architecture.md, equivalent Mermaid and editable
Draw.io component views, and a separate AWS infrastructure Draw.io view.
Label the AWS target as proposed unless deployment evidence establishes it.
Include native Archify output when its installed Skill is available.
Record evidence, unknowns and checks actually performed. Do not change application
code or deployment configuration, and do not launch Draw.io Desktop for rendering.
```

### Expected result

A linked architecture document and complementary component/infrastructure diagrams,
with current and proposed facts separated. Archify status and unavailable checks
are reported explicitly.

### Review criteria

- Component views agree; the infrastructure view describes deployment separately.
- Material relationships have evidence or an explicit proposed/unknown status.
- Provider icons and applicable structural checks follow the Skill's guidance.
- Missing artifacts or blocked checks are disclosed without claiming completion.

### Execution status

Illustrative scenario; not executed as part of this documentation change. The
[reference package](reference-application/architecture.md) is a separate example,
not evidence that this prompt has been executed.
