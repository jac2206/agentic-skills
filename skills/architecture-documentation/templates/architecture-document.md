# Architecture: <system name>

> **Status:** verified current state | proposed target state | mixed. State the evidence boundary and date.

## Product purpose and domain

Explain what the product enables, who uses it, and its core business capabilities in concrete domain terms. Base this summary on project context/specifications and corroborate it against implemented routes, screens, services, or domain code. Cite repository paths. If evidence is absent or conflicting, say so instead of inferring the product from its technology stack or the request wording.

## Scope and evidence

List the inspected repositories and sources. Classify important claims as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Explain limitations and resolve stale/generic README claims against stronger evidence.

## System context

Describe the system purpose, actors, external systems, scope, and top-level interaction. Mark unsupported purpose or behavior as unknown.

## Components and responsibilities

| Component | Responsibility | Evidence / status |
|---|---|---|
| <component> | <responsibility> | <source and status> |

## Component diagram

Link both `component-diagram.mmd` and the editable `component-diagram.drawio`. Keep the two diagrams semantically aligned. Embed Mermaid here when useful; keep Draw.io XML in its standalone `.drawio` file.

## Runtime and integration paths

Describe important synchronous requests, asynchronous events, protocols, entry points, branches, and outcomes. Only include paths supported by evidence.

## Data and persistence

Describe data ownership, stores, important relationships, and flow. Mark unspecified schemas, transactions, retention, or consistency as unknown.

## Cloud infrastructure and deployment

Name the selected target provider and explain whether the topology is configured, deployed, inferred, or proposed. Link `infrastructure.drawio`. If current providers differ from the target, link a separate `current-deployment.drawio` when current deployment is in scope. Include only evidenced or explicitly proposed network, runtime, ingress, and storage boundaries. Never describe a proposal as deployed.

## Security

Document evidenced identity, authorization, trust boundaries, secrets, encryption, audit, and network controls. Separate missing controls from implemented controls.

## Availability and operations

Document evidenced scaling, health checks, resilience, backup/recovery, observability, deployment, and operational ownership. Identify missing targets.

## Decisions and evidence gaps

List the decisions or missing sources needed to resolve material unknowns. Do not silently choose values that change architecture.

## Diagram index

- Component diagram: `component-diagram.mmd`
- Editable component diagram: `component-diagram.drawio`
- Cloud infrastructure: `infrastructure.drawio`
- Current deployment (only when separate): `current-deployment.drawio`
- Archify architecture: `<system-name>.archify.html` (include only if Archify is installed and its generation workflow produced the file; omit this entry when unavailable)
