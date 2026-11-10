# Architecture: <system name>

> **Status:** verified current state | proposed target state | mixed. State the evidence boundary and date.

## Product purpose and domain

Explain what the product enables, who uses it, and its core business capabilities in concrete domain terms. Base this summary on project context/specifications and corroborate it against implemented routes, screens, services, or domain code. Cite repository paths. If evidence is absent or conflicting, say so instead of inferring the product from its technology stack or the request wording.

## Scope and evidence

List the inspected repositories and sources, and the inspected revision when available. Check that reused paths and revision references actually match the current workspace; identify historical, unavailable, or conflicting references without inventing a revision. Classify important claims as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Explain limitations and resolve stale/generic README claims against stronger evidence.

## System context

Describe the system purpose, actors, external systems, scope, and top-level interaction. Mark unsupported purpose or behavior as unknown.

## Components and responsibilities

| Component | Responsibility | Evidence / status |
|---|---|---|
| <component> | <responsibility> | <source and status> |

## Component diagram

Link both `component-diagram.mmd` and the editable `component-diagram.drawio`. Keep the two diagrams semantically aligned. These are the logical component views; retain them alongside the additional cloud infrastructure Draw.io. Embed Mermaid here when useful; keep Draw.io XML in its standalone `.drawio` file.

## Runtime and integration paths

Describe important synchronous requests, asynchronous events, protocols, entry points, branches, and outcomes. Only include paths supported by evidence.

## Data and persistence

Describe data ownership, stores, important relationships, and flow. Mark unspecified schemas, transactions, retention, or consistency as unknown.

## Cloud infrastructure and deployment

Name the selected target provider and explain whether the topology is configured, deployed, inferred, or proposed. Always link the additional, separate provider-named infrastructure Draw.io (`aws-infrastructure.drawio` by default, `google-cloud-infrastructure.drawio` for Google Cloud, or `azure-infrastructure.drawio` for Azure); it supplements and does not replace the component diagrams. Generate only the selected provider unless the user explicitly requests multi-cloud alternatives. If the user did not name a target provider, this is a proposed AWS design and must use native AWS service icons. A current stack hosted on other providers does not replace this target diagram. If current providers differ from the target, describe them as current or user-reported and link a separate `current-deployment.drawio` when useful. Include only evidenced or explicitly proposed network, runtime, ingress, and storage boundaries. Never describe a proposal as deployed.

In the deployment diagram, distinguish the provider scope, any known or proposed account/project/subscription and region, network boundaries such as VPC/VNet, and external clients or systems. Put external clients and integrations outside the provider boundary unless they are hosted there. Mark unknown placement `TBD`; do not invent a region, subnet, or availability zone. Mark proposed boundaries visibly.

## Security

Document evidenced identity, authorization, trust boundaries, secrets, encryption, audit, and network controls. Separate missing controls from implemented controls.

## Availability and operations

Document evidenced scaling, health checks, resilience, backup/recovery, observability, deployment, and operational ownership. Identify missing targets.

## Decisions and evidence gaps

List the decisions or missing sources needed to resolve material unknowns. Do not silently choose values that change architecture.

## Diagram index

- Component diagram: `component-diagram.mmd`
- Editable component diagram: `component-diagram.drawio`
- Cloud infrastructure: `<provider>-infrastructure.drawio` (for example, `aws-infrastructure.drawio`)
- Current deployment (only when separate): `current-deployment.drawio`
- Archify architecture: link the HTML and candidate JSON at the actual paths produced by the installed Archify Skill (required when installed; omit when unavailable)

Record static diagram checks and visual inspection separately, including the
tool and result or why visual inspection was not performed. Follow the Skill's
renderer safety limits; a static pass does not establish visual correctness.
