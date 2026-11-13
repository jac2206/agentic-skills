# Application Security Review Usage

**Idioma / Language:** [Español](#español) | [English](#english)

**Instrucciones / Instructions:** [SKILL.md](../SKILL.md).

## Español

### Descripción

Evalúa riesgos de seguridad en aplicaciones y su entrega mediante evidencia. Produce hallazgos accionables y ayuda a verificar correcciones autorizadas, sin certificar la ausencia de vulnerabilidades.

### Contexto

Abre la aplicación de destino y sustituye <authorization-path> por una ruta real
de implementación de autenticación o autorización. Este Review es pasivo y no
autoriza pruebas contra sistemas en funcionamiento.

### Prompt de ejemplo

```text
Usa la Skill application-security-review en modo Review.
Revisa <authorization-path> y los manejadores de solicitudes y pruebas pertinentes.
Traza cómo se comprueban las identidades y permisos antes de acceder a datos protegidos.
Devuelve hallazgos sustentados con ubicación, evidencia, justificación de severidad,
impacto, correcciones recomendadas y comprobaciones para verificar una solución.
Distingue hallazgos confirmados, riesgos potenciales y evidencia faltante.
No edites archivos, contactes sistemas en funcionamiento ni imprimas secretos.
```

### Resultado esperado

Una revisión acotada en la respuesta, con hallazgos accionables o una explicación
de la cobertura inspeccionada y sus límites. La ausencia de hallazgos no certifica
la seguridad de la aplicación.

### Criterios de revisión

- Cada hallazgo confirmado tiene una ruta sustentada a través de los controles.
- Se justifican la severidad y la incertidumbre y se consideran las mitigaciones.
- No se exponen secretos ni se realizan pruebas activas o correcciones no solicitadas.
- Las pruebas no ejecutadas se identifican como tales.

### Estado de ejecución

Escenario ilustrativo; no ejecutado como parte de este cambio de documentación.
Los [escenarios de validación](../references/validation-scenarios.md) contienen
casos adicionales.

## English

### About this Skill

Assesses application and software-delivery security risks from evidence. It produces actionable findings and helps verify authorized fixes without certifying the absence of vulnerabilities.

### Context

Open the target application and replace `<authorization-path>` with an actual
authentication or authorization implementation path. This is a passive Review;
it does not authorize testing a live system.

### Example prompt

```text
Use the application-security-review Skill in Review mode.
Review <authorization-path> and the directly relevant request handlers and tests.
Trace how identities and permissions are checked before accessing protected data.
Return supported findings with location, evidence, severity rationale, impact,
recommended fixes, and checks that would verify a correction.
Distinguish confirmed findings from potential risks and missing evidence.
Do not edit files, contact live systems, or print secret values.
```

### Expected result

A scoped review in the response, with actionable findings or an explanation of
the inspected coverage and its limits. An absence of findings is not certification.

### Review criteria

- Each confirmed finding has a supported path through the relevant controls.
- Severity and uncertainty are explained; existing mitigations are considered.
- No secret values, active testing, or unrequested remediation is introduced.
- Unexecuted tests remain identified as unexecuted.

### Execution status

Illustrative scenario; not executed as part of this documentation change. Additional
cases are in [validation scenarios](../references/validation-scenarios.md).
