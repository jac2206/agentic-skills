# Reference Application Architecture

> **Status: proposed reference architecture.** This document was reconstructed from `C:\Users\arang\Downloads\Diagramas ejemplo.drawio`, supplied as a visual reference. The active repository contains no source code, deployment manifests, infrastructure as code, API specification, or operational configuration for the depicted application. The components and relationships therefore describe the reference design; they do not represent a verified or deployed system.

## 1. Scope and evidence

The supplied diagram shows web and mobile clients, an AWS API entry point, authentication and authorization capabilities, a serverless path, a Kubernetes path, domain services, persistence, and asynchronous messaging. This document organizes that topology into a component view and an infrastructure view.

Evidence status:

- **Visible in the diagram:** web and mobile clients; HTTPS/REST; API Gateway; Cognito; Lambda; Application Load Balancer; EKS; user, transaction, partner, and notification backends; Aurora; DocumentDB; EventBridge; rules; and SQS queues.
- **Proposed interpretation:** API Gateway serves both the Lambda path and the ALB/EKS path; EKS runs the four backends; each service is associated with the data store connected to it in the drawing; EventBridge routes events to SQS queues.
- **Not defined:** application name and purpose, API contracts, exact AWS account/Region/VPC, network exposure, event contracts, queue consumers, Lambda purpose, availability targets, scaling, backup and recovery, observability, CI/CD, and security policies.

AWS is used because the reference diagram already contains AWS services. There is no evidence for a Google Cloud or Azure deployment design.

## 2. System context

The system has two client types: a web frontend and a mobile application. Both send HTTPS/REST requests to API Gateway. Cognito appears in the authentication and authorization area. The diagram shows two compute paths: a Lambda function and an ALB that forwards traffic to an EKS cluster. The cluster groups separate backends for users, transactions, partners, and notifications.

The diagram also shows a shared event path through EventBridge, rules, and SQS queues. The visible persistence associations are users with Aurora, transactions with DocumentDB, partners with Aurora, and notifications with Aurora. The diagram does not specify which events each service publishes, who consumes the queues, or whether databases are isolated by service. The one-to-one service-to-store associations are retained as proposals based on the drawn connections.

## 3. Component responsibilities

| Component | Responsibility in this reference | Evidence / status |
| --- | --- | --- |
| Web frontend | Client that calls the API over HTTPS | Visible in the diagram; behavior unknown |
| Mobile application | Mobile client that calls the API over HTTPS | Visible; behavior unknown |
| Amazon API Gateway | API entry point and request routing | Visible; routes and policies unspecified |
| Amazon Cognito | Authentication and authorization capability | Visible; identity flow and enforcement point unspecified |
| AWS Lambda | Serverless compute path from API Gateway | Visible; function and triggers unknown |
| Application Load Balancer | Routes API traffic to the Kubernetes service tier | Visible; listeners, target groups, and network unknown |
| Amazon EKS | Runs backend workloads | Visible; topology and configuration unknown |
| User backend | User-domain service/API | Visible; implementation and contract unknown |
| Transaction backend | Transaction-domain service/API | Visible; implementation and contract unknown |
| Partner backend | Partner-domain service/API | Visible; implementation and contract unknown |
| Notification backend | Notification-domain service | Visible; providers and consumers unknown |
| Amazon Aurora | Relational persistence associated with multiple services | Visible; engine, schema, and ownership need confirmation |
| Amazon DocumentDB | Document persistence associated with transactions | Visible; schema and ownership need confirmation |
| Amazon EventBridge | Event bus and routing | Visible; contracts and rules unknown |
| EventBridge rules | Filter and route events to queues | Visible; conditions unspecified |
| Amazon SQS | Asynchronous messaging destinations | Visible; consumers, retries, DLQ, and ordering unspecified |

## 4. Component diagram

The logical component view is available in two editable, equivalent formats: [Mermaid](component-diagram.mmd) and [Draw.io](component-diagram.drawio). Both describe roles and relationships inferred from the reference diagram; neither establishes a verified deployment.

## 5. Infrastructure and deployment view

The editable AWS diagram is [aws-infrastructure.drawio](aws-infrastructure.drawio). It is a proposed provider mapping of the shared illustrative topology, not a faithful reproduction of every AWS service in the supplied source. It uses API Gateway, Lambda, VPC Link, a Network Load Balancer, EKS, RDS for PostgreSQL, DynamoDB, EventBridge, and SQS. These choices differ from the source drawing's Cognito, Application Load Balancer, Aurora, and DocumentDB; the identity provider, load-balancing pattern, and data-store substitutions need review. The diagram uses AWS4 service icons with separate editable labels. VPC Link is shown as an editable labeled card; its icon has not been verified in this environment. The diagram does not establish that any AWS resource is deployed. The outer cloud, account, Region, and VPC scopes are explicitly marked proposed, with unknown placement shown as TBD; web/mobile clients remain in an external zone. DynamoDB and messaging services are outside the VPC boundary, while RDS and EKS are inside it.

The Skill also includes [a proposed Google Cloud variant](google-cloud-infrastructure.drawio) and [a proposed Azure variant](azure-infrastructure.drawio). Google Cloud uses official product/category SVGs; category marks are labeled for Cloud Load Balancing, Firestore, and Pub/Sub. Azure uses embedded SVGs from Microsoft's Architecture Center icon package. Text, connections, and boundaries remain editable. Each view separates external clients, provider/project/subscription, Region, and proposed private network scopes; managed services that do not require VNet/VPC attachment remain outside those network frames. Google Cloud Load Balancing and Pub/Sub are shown at global/project scope, Cloud Run remains outside the VPC, and GKE/Cloud SQL use a proposed private-network path. Azure AKS workloads are inside the proposed VNet; PostgreSQL remains outside the VNet boundary with private access proposed, and Cosmos DB, Event Grid, and Service Bus remain outside it. The exact Region, account/project/subscription, subnet, and availability-zone placement is TBD. All three cloud files are alternatives for requests naming a provider. They are not current deployment claims or automatic service-by-service equivalents. A normal generation produces only the selected cloud; AWS is the default when no provider is specified.

### Provider icon inventory

| Diagram | Provider service icons | Client pictograms / fallback |
| --- | --- | --- |
| AWS | AWS4 stencils: API Gateway, Lambda, Network Load Balancer, EKS, RDS, DynamoDB, EventBridge, and SQS. VPC Link is a labeled card because its icon was not verified. | UML actor plus embedded neutral laptop and phone SVGs; no cloud icon is used for clients. |
| Azure | Embedded Azure Architecture Center SVGs: API Management, Functions, AKS, Database for PostgreSQL, Cosmos DB, Event Grid, and Service Bus. | UML actor plus embedded neutral laptop and phone SVGs; no cloud icon is used for clients. |
| Google Cloud | Embedded Google Cloud product/category SVGs: Load Balancing, Cloud Run, GKE, Cloud SQL, Firestore, Pub/Sub, and subscriptions. Category marks retain explicit service labels. | UML actor plus embedded neutral laptop and phone SVGs; no cloud icon is used for clients. |

The embedded SVGs and AWS4 stencil identifiers are structurally present; the static checker cannot prove that each glyph matches its label or how Draw.io renders it. No Draw.io Desktop preview was run, so visual rendering and icon-to-service mapping remain unverified.

The request, data, and event paths below describe the supplied source drawing. The provider-specific diagrams are illustrative deployment proposals and may use different services or routing patterns.

### Request path

1. A web or mobile client calls the API over HTTPS in the supplied source design.
2. API Gateway is the represented API entry point.
3. Cognito is the represented identity capability; the OAuth/OIDC flow and policy enforcement point are undefined.
4. API Gateway routes requests to Lambda or to ALB/EKS. The diagram does not say which APIs use each path.
5. The ALB forwards requests to backend workloads in EKS.

### Data path

The drawing associates backends with Aurora and DocumentDB. It does not define schemas, cross-service transactions, backups, encryption, or recovery objectives. Treat the connections as proposed ownership until the data design is confirmed.

### Event path

The source shows an event bus, rules, and SQS queues, but does not identify consumers or message lifecycle behavior. Before production, define schemas, delivery guarantees, retries, dead-letter queues (DLQs), idempotency, retention, and ownership.

## 6. Security boundaries and controls

The drawing shows Cognito and an API entry point, but does not prove that any control is implemented. Confirm and document the following before deployment:

- TLS termination and encryption in transit at every hop.
- Cognito user/identity pools, token validation, scopes, roles, and service identity.
- Authorization, throttling, request validation, and abuse protection in API Gateway.
- VPC, subnets, security groups, private endpoints, and network egress for EKS, databases, and queues.
- At-rest encryption and key ownership for data stores, logs, and queues.
- Secret management and rotation, least-privilege IAM roles, auditing, and sensitive-data handling.

## 7. Availability and operations

The source contains no deployment configuration or service objectives. Multi-AZ deployment, autoscaling, health checks, database failover, backups, disaster recovery, monitoring, alerting, logs, traces, release strategy, and cost controls remain undefined. The presence of managed-service icons does not demonstrate production readiness.

## 8. Decisions required before implementation

1. Define the application's purpose, actors, API domains, and endpoint ownership.
2. Choose the target API path and compute split; the source shows Lambda and ALB/EKS, while the AWS proposal shows Lambda and VPC Link/NLB/EKS.
3. Confirm the identity provider and where authorization is enforced; Cognito appears in the source drawing, while the AWS proposal leaves identity unspecified.
4. Confirm database ownership and whether to retain the source's Aurora/DocumentDB choices or use the proposed RDS for PostgreSQL/DynamoDB mapping.
5. Define event producers, schemas and versions, rules, SQS consumers, retries, DLQs, and idempotency.
6. Specify the AWS account and Region, VPC, subnets, ingress/egress, private connectivity, and environments.
7. Establish availability, latency, RPO/RTO, backup, scaling, and deployment objectives.
8. Choose observability, auditing, secrets, encryption, and CI/CD controls.

## 9. Artifacts

- [Mermaid component diagram](component-diagram.mmd)
- [Editable component diagram (Draw.io)](component-diagram.drawio)
- [AWS infrastructure proposal (Draw.io)](aws-infrastructure.drawio)
- [Google Cloud infrastructure proposal](google-cloud-infrastructure.drawio)
- [Azure infrastructure proposal](azure-infrastructure.drawio)
- [Archify architecture diagram](reference-application.archify.html)
- [Archify source candidate](reference-application.archify.json)
- [Archify finalization summary](reference-application.archify.finalize-summary.json)

Archify produced the HTML through its native `finalize architecture` workflow. Structural validation, delivery, and the strict check passed. The Chrome check was blocked because this environment could not verify the identity of its temporary directory (`C:\Users\arang\AppData\Local\Temp`); browser validation and full visual review are not claimed.

## 10. Sources

- User-supplied reference: `C:\Users\arang\Downloads\Diagramas ejemplo.drawio` (read-only input; not copied into the repository).
- Inspected repository sources: `AGENTS.md`, `README.md`, and available Skills. No implementation of the depicted application was found.
