# Documentación de arquitectura — aplicación de referencia

> **Estado: arquitectura de referencia propuesta.** Este documento se reconstruyó a partir de `C:\Users\arang\Downloads\Diagramas ejemplo.drawio`, entregado como referencia visual. El repositorio actual no contiene código fuente, manifiestos de despliegue, infraestructura como código, especificación de API ni configuración operativa de la aplicación dibujada. Por ello, los componentes y relaciones describen el diseño de referencia; no representan un sistema verificado o desplegado.

## 1. Alcance y evidencia

El diagrama suministrado muestra una aplicación web y móvil, una entrada de API en AWS, capacidades de autenticación/autorización, una ruta serverless, otra ruta Kubernetes, servicios de dominio, persistencia y mensajería asíncrona. Esta documentación organiza esa topología en una vista de componentes y otra de infraestructura.

Estado de evidencia:

- **Visible en el diagrama:** clientes web y móvil; HTTPS/REST; API Gateway; Cognito; Lambda; Application Load Balancer; EKS; backends de usuarios, transacciones, partners y notificaciones; Aurora; DocumentDB; EventBridge; reglas y colas SQS.
- **Interpretación propuesta:** API Gateway atiende tanto la ruta Lambda como la ruta ALB/EKS; EKS ejecuta los cuatro backends; cada servicio se asocia al almacén conectado en el dibujo; EventBridge dirige eventos a colas SQS.
- **No definido:** nombre y propósito de la aplicación, contratos de API, cuenta/región/VPC exactos, exposición de red, contratos de eventos, consumidores de colas, función de Lambda, objetivos de disponibilidad, escalamiento, copias/recuperación, observabilidad, CI/CD y políticas de seguridad.

Se usa AWS porque el diagrama de referencia ya contiene servicios de AWS. No hay evidencia para diseñar despliegues en Google Cloud o Azure.

## 2. Contexto del sistema

El sistema tiene dos tipos de clientes: frontend web y aplicación móvil. Ambos envían solicitudes HTTPS/REST a API Gateway. Cognito aparece en el área de autenticación/autorización. El tráfico tiene dos rutas de cómputo dibujadas: una función Lambda y un ALB que lleva a un clúster EKS. El clúster agrupa backends separados para usuarios, transacciones, partners y notificaciones.

El diagrama también muestra una ruta compartida de eventos mediante EventBridge, reglas y colas SQS. Las asociaciones visibles de persistencia son usuarios con Aurora, transacciones con DocumentDB, partners con Aurora y notificaciones con Aurora. No se especifican los eventos que emite cada servicio, los consumidores de las colas ni si las bases están aisladas por servicio. La asociación uno a uno entre servicio y almacén se conserva como propuesta basada en las conexiones visuales.

## 3. Responsabilidades de componentes

| Componente | Responsabilidad en esta referencia | Evidencia / estado |
|---|---|---|
| Frontend web | Cliente para usuarios que llama a la API HTTPS | Visible en el diagrama; comportamiento desconocido |
| Aplicación móvil | Cliente móvil que llama a la API HTTPS | Visible; comportamiento desconocido |
| Amazon API Gateway | Entrada de API y enrutamiento de solicitudes | Visible; rutas y políticas no especificadas |
| Amazon Cognito | Capacidad de autenticación/autorización | Visible; flujo de identidad y punto de validación no especificados |
| AWS Lambda | Ruta de cómputo serverless desde API Gateway | Visible; función y disparadores desconocidos |
| Application Load Balancer | Enruta tráfico API al nivel de servicios Kubernetes | Visible; listeners, target groups y red desconocidos |
| Amazon EKS | Ejecuta los workloads backend | Visible; topología y configuración desconocidas |
| Backend de usuarios | Servicio/API del dominio de usuarios | Visible; implementación y contrato desconocidos |
| Backend de transacciones | Servicio/API del dominio de transacciones | Visible; implementación y contrato desconocidos |
| Backend de partners | Servicio/API del dominio de partners | Visible; implementación y contrato desconocidos |
| Backend de notificaciones | Servicio del dominio de notificaciones | Visible; proveedores y consumidores desconocidos |
| Amazon Aurora | Persistencia relacional asociada a varios servicios | Visible; motor, esquema y propiedad por confirmar |
| Amazon DocumentDB | Persistencia documental asociada a transacciones | Visible; esquema y propiedad por confirmar |
| Amazon EventBridge | Bus y enrutamiento de eventos | Visible; contratos y reglas desconocidos |
| Reglas de EventBridge | Filtrado y direccionamiento hacia colas | Visible; condiciones no especificadas |
| Amazon SQS | Destinos de mensajería asíncrona | Visible; consumidores, reintentos, DLQ y orden no especificados |

## 4. Diagrama de componentes

La vista logica de componentes se entrega en dos formatos editables y equivalentes: [Mermaid](component-diagram.mmd) y [Draw.io](component-diagram.drawio). Ambos describen los roles y relaciones inferidos del diagrama de referencia; no establecen despliegues verificados.
## 5. Vista de infraestructura y despliegue

El diagrama editable de AWS está en [aws-infrastructure.drawio](aws-infrastructure.drawio). Usa stencils nativos AWS4, incluidas variantes de servicio como `endpoint` y `lambda_function`, y el tratamiento plano de color del XML de referencia compartido. Conserva los nombres completos de los servicios como etiquetas editables. La vista está marcada como propuesta porque no hay configuración de despliegue. Los módulos de aplicación están dentro de los límites de cómputo propuestos; este diagrama no sustituye a la vista lógica de componentes.

La skill también incluye [una variante propuesta para Google Cloud](google-cloud-infrastructure.drawio) y [otra para Azure](azure-infrastructure.drawio). Google Cloud usa SVG oficiales de producto/categoría actualizados en 2025; las marcas de networking, bases de datos e integración son iconos de categoría para Cloud Load Balancing, Firestore y Pub/Sub. Azure usa SVG oficiales del paquete de arquitectura de Microsoft. Los SVG están incrustados para que cada `.drawio` sea portable; el texto, las conexiones y los límites siguen editables. Son ejemplos alternativos para una solicitud que nombre uno de esos proveedores; no forman parte de este paquete AWS, no son despliegues actuales ni equivalencias automáticas servicio por servicio. En una generación normal se entrega solo la nube seleccionada; si no se especifica, se usa AWS.

### Ruta de solicitudes

1. Un cliente web o móvil llama al endpoint HTTPS de la API.
2. API Gateway es la entrada de API representada.
3. Cognito es la capacidad de identidad representada; el flujo OAuth/OIDC y el punto de aplicación de políticas no están definidos.
4. API Gateway dirige solicitudes a Lambda o a ALB/EKS. El diagrama no indica qué APIs usan cada ruta.
5. El ALB reenvía solicitudes a workloads backend en EKS.

### Ruta de datos

El dibujo asocia backends con Aurora y DocumentDB. No define esquemas, transacciones entre servicios, respaldos, cifrado ni objetivos de recuperación. Las conexiones deben tratarse como una propuesta de propiedad hasta confirmar el diseño de datos.

### Ruta de eventos

La fuente muestra un bus, reglas y colas SQS, pero no identifica consumidores ni el ciclo de vida de los mensajes. Antes de producción hay que definir esquemas, garantías de entrega, reintentos, colas de mensajes fallidos (DLQ), idempotencia, retención y responsables.

## 6. Límites y controles de seguridad

El dibujo muestra Cognito y una entrada API, pero no demuestra que algún control esté implementado. Antes del despliegue, confirmar y documentar:

- Terminación TLS y cifrado en tránsito en cada salto.
- User pools/identity pools, validación de tokens, scopes, roles e identidad entre servicios en Cognito.
- Autorización, throttling, validación de solicitudes y protección contra abuso en API Gateway.
- VPC, subredes, security groups, endpoints privados y salida de red para EKS, bases y colas.
- Cifrado en reposo y propiedad de claves para almacenes, logs y colas.
- Gestión y rotación de secretos, roles IAM de mínimo privilegio, auditoría y tratamiento de datos sensibles.

## 7. Disponibilidad y operación

La fuente no incluye configuración de despliegue ni objetivos de servicio. Multi-AZ, escalamiento automático, health checks, failover de bases, respaldos, recuperación ante desastres, monitoreo, alertas, logs, trazas, estrategia de releases y control de costos quedan por definir. La presencia de iconos de servicios administrados no demuestra preparación para producción.

## 8. Decisiones necesarias para implementar esta arquitectura

1. Definir propósito de la aplicación, actores, dominios de API y propiedad de endpoints.
2. Asignar cada ruta API a Lambda o a un backend EKS; aclarar por qué se requieren ambas rutas de cómputo.
3. Confirmar integración de Cognito y dónde se aplica autorización: API Gateway, servicios o ambos.
4. Confirmar propietario de cada base, motor de Aurora, uso de DocumentDB, esquemas y aislamiento de datos.
5. Definir productores, esquemas/versionado de eventos, reglas, consumidores SQS, reintentos, DLQ e idempotencia.
6. Especificar cuenta/región AWS, VPC, subredes, ingreso/egreso, conectividad privada y entornos.
7. Establecer disponibilidad, latencia, RPO/RTO, respaldos, escalamiento y objetivos de despliegue.
8. Elegir observabilidad, auditoría, secretos, cifrado y controles CI/CD.

## 9. Artefactos

- [Diagrama de componentes Mermaid](component-diagram.mmd)
- [Diagrama de componentes editable (Draw.io)](component-diagram.drawio)
- [Diagrama de infraestructura AWS para Draw.io](aws-infrastructure.drawio)
- [Ejemplo alternativo de infraestructura Google Cloud](google-cloud-infrastructure.drawio)
- [Ejemplo alternativo de infraestructura Azure](azure-infrastructure.drawio)
- [Diagrama de arquitectura Archify](reference-application.archify.html)
- [Candidato fuente de Archify](reference-application.archify.json)
- [Resumen de finalización de Archify](reference-application.archify.finalize-summary.json)

Archify produjo el HTML mediante su flujo nativo `finalize architecture`. La validación estructural, la entrega y la comprobación estricta pasaron. El chequeo de Chrome quedó bloqueado porque este entorno no pudo verificar la identidad de su directorio temporal (`C:\Users\arang\AppData\Local\Temp`); no se declara validación de navegador ni revisión visual completa.

## 10. Fuente

- Referencia entregada por el usuario: `C:\Users\arang\Downloads\Diagramas ejemplo.drawio` (entrada de solo lectura; no se copió al repositorio).
- Repositorio inspeccionado: `AGENTS.md`, `README.md` y Skills disponibles. No se encontró implementación de la aplicación representada.
