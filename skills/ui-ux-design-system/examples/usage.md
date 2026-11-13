# UI/UX Design System Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Diseña, implementa, audita y evoluciona interfaces y sistemas de diseño. Respeta la identidad existente o solicitada y utiliza JAC cuando no hay otra establecida; los diseños de interfaz incluyen un prototipo HTML por defecto.

### Contexto

Abre el proyecto de interfaz con sus recursos de marca y sistema de diseño cuando
existan. El escenario suministra tres estados y pide un prototipo, no una función
de producción ni un archivo editable de Figma.

### Prompt de ejemplo

```text
Usa la Skill ui-ux-design-system en modo Design Interface.
Diseña una pantalla adaptable de estado de pedido con referencia, estado actual
y línea de tiempo. Los estados suministrados son pending, shipped y delivered.
Conserva la identidad explícita o existente del proyecto; aplica el valor
predeterminado de la Skill solo si no existe identidad. Marca pedidos e interacciones de ejemplo como simulados.
Crea un prototipo HTML revisable en examples/design/order-status.html sin cambiar
código ni inventar funciones de pago, cancelación o seguimiento.
Comprueba diseño, acceso por teclado y contraste cuando sea posible e informa los límites.
```

### Resultado esperado

Un prototipo HTML coherente que cubre los estados suministrados y diseños adaptables,
con decisiones de identidad y comportamiento simulado explícitos.

### Criterios de revisión

- Las restricciones de marca existentes prevalecen sobre la identidad predeterminada.
- El significado del estado y la línea de tiempo se conserva entre tamaños de pantalla.
- Foco, etiquetas, contraste y desbordamiento se revisan con evidencia cuando es posible.
- El prototipo no se presenta como implementación de producción ni archivo de Figma.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Al escribir esta guía no se generó un prototipo ni se estableció conformidad de accesibilidad.

## English

### About this Skill

Designs, implements, audits and evolves interfaces and design systems. It respects explicit or existing identity and uses JAC when none is established; interface designs default to a reviewable HTML prototype.

### Context

Open the target UI project with its brand assets and design system when present.
This scenario supplies three display states and requests a prototype, not a
production feature or editable Figma file.

### Example prompt

```text
Use the ui-ux-design-system Skill in Design Interface mode.
Design a responsive order-status screen showing an order reference, current status
and timeline. Supplied statuses are pending, shipped and delivered.
Preserve the project's explicit or existing identity; apply the Skill's default
only when no identity is established. Mark sample orders and interactions simulated.
Create a reviewable HTML prototype at examples/design/order-status.html without
changing application code or inventing payment, cancellation or tracking features.
Check layout, keyboard access and contrast when possible, and report validation limits.
```

### Expected result

A coherent HTML prototype covering the supplied states and responsive layouts,
with identity decisions and simulated behavior made clear.

### Review criteria

- Existing brand constraints take precedence over the default design identity.
- Status and timeline meaning remain consistent across screen sizes.
- Focus, labels, contrast and overflow are reviewed with actual evidence when possible.
- The prototype is not represented as a production implementation or Figma file.

### Execution status

Illustrative scenario; not executed as part of this documentation change. No
prototype was generated or accessibility conformance established while writing this guide.
