# Software Architecture Design Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Analiza, diseña, evoluciona y compara arquitecturas según requisitos, restricciones y evidencia reales. Justifica decisiones y alternativas sin imponer un stack o patrón.

### Contexto

Abre el código de la aplicación y los requisitos de arquitectura disponibles.
La generación de reportes en segundo plano es una propuesta, no una función observada.

### Prompt de ejemplo

```text
Usa la Skill software-architecture-design en modos Evolve y Compare.
Evalúa agregar generación de reportes en segundo plano a la aplicación actual.
Inspecciona la estructura existente y compara las opciones viables más sencillas,
incluyendo conservar procesamiento síncrono si la evidencia lo justifica.
Explica límites, flujo de datos, fallos, compatibilidad y decisiones entre alternativas.
Identifica requisitos de carga y operación faltantes en vez de inventarlos.
Devuelve el diseño y próximas comprobaciones solo en la respuesta; no implementes
código, crees diagramas como archivos separados ni agregues infraestructura o dependencias.
```

### Resultado esperado

Una recomendación condicional basada en el sistema existente, con alternativas,
consecuencias, incertidumbres y evidencia necesaria antes de implementar.

### Criterios de revisión

- Se distingue el comportamiento actual de los componentes propuestos.
- Se evalúan alternativas sencillas antes de introducir colas o servicios.
- No se inventan cargas, niveles de servicio, proveedor cloud ni hechos de despliegue.
- Se incluyen criterios concretos de validación y riesgos de compatibilidad.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Los [recorridos de escenarios](scenario-walkthroughs.md) cubren otros casos de diseño.

## English

### About this Skill

Analyzes, designs, evolves and compares architectures against actual requirements, constraints and evidence. It explains decisions and alternatives without imposing a stack or pattern.

### Context

Open the target application's source and available architecture requirements. The
requested background-report capability is a proposal, not an observed feature.

### Example prompt

```text
Use the software-architecture-design Skill in Evolve and Compare modes.
Assess adding background report generation to the current application.
Inspect the existing structure and compare the smallest viable approaches,
including retaining synchronous processing if the evidence supports it.
Explain boundaries, data flow, failure handling, compatibility and trade-offs.
Identify missing workload and operational requirements instead of inventing them.
Return the design and next validation checks in the response only; do not implement
code, create diagrams as separate files, or add infrastructure or dependencies.
```

### Expected result

A conditional recommendation grounded in the existing system, with alternatives,
consequences, uncertainty and the evidence needed before implementation.

### Review criteria

- Current behavior and proposed components are clearly distinguished.
- Simpler alternatives are assessed before introducing queues or new services.
- No workload, service level, cloud choice or deployment fact is invented.
- The recommendation includes concrete validation criteria and compatibility risks.

### Execution status

Illustrative scenario; not executed as part of this documentation change. See
[scenario walkthroughs](scenario-walkthroughs.md) for other design review cases.
