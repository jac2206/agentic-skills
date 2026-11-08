# Security Review Playbook

Use this reference selectively after establishing the system scope. It is a
coverage aid, not a mandatory checklist and not a substitute for project
requirements or a standard's complete verification guidance.

## Review dimensions

Select dimensions based on the actual assets, actors, architecture, change, and
exposure. Record areas not assessed when relevant; do not imply exhaustive
coverage from a checklist.

| Dimension | Questions to guide evidence collection |
| --- | --- |
| Identity and sessions | How are identities established, sessions created, renewed, expired, revoked, recovered, and protected against guessing or replay? |
| Authorization | Are permissions checked on every relevant object, property, operation, tenant, and administrative action? Can a caller alter identifiers or fields to cross a boundary? |
| Input and output | Are inputs constrained at trust boundaries? Are database, shell, template, browser, file, URL-fetch, and serialization contexts handled safely? |
| API and abuse controls | Are authentication, resource authorization, schema validation, quotas, rate limits, inventory, errors, webhooks, and sensitive workflows appropriate to the threat? |
| Data protection and privacy | What sensitive data is collected, moved, stored, logged, retained, backed up, deleted, and exposed? Are encryption and key-management controls appropriate? |
| Secrets and configuration | Are credentials stored and scoped safely? Are debug, CORS, transport, headers, error, network, and environment settings appropriate? Do logs or artifacts expose values? |
| Dependencies and supply chain | Are components identified, pinned or constrained appropriately, maintained, sourced, and checked against advisories? Are build inputs and artifacts protected? |
| Infrastructure and cloud | Are identities, networks, storage, workloads, containers, clusters, and management interfaces exposed and privileged only as required? |
| Web, desktop, and mobile clients | Are browser boundaries, CSRF/XSS, content policies, local storage, deep links, inter-app communication, local files, and platform-provided secure storage handled appropriately? |
| Logging, errors, and resilience | Are security events observable without leaking sensitive data? Are errors safe? Can failures, retries, concurrency, or resource exhaustion bypass controls? |
| AI and LLM systems | Can untrusted content influence instructions or tools? Are retrieval, tenant isolation, tool permissions, output handling, data egress, and agent autonomy bounded? |
| CI/CD and operations | Are pipeline identities, branch controls, secrets, approvals, artifact integrity, environment separation, and deployment permissions limited and auditable? |
| Distributed systems and integrations | Are service identities, message trust, replay/idempotency, schema evolution, retries, callbacks, and third-party data trust addressed? |

For each applicable dimension, identify the relevant control, evidence source,
assessment state (`Passed`, `Finding`, `Not Assessed`, `Not Applicable`), and
reason. `Passed` requires positive evidence of the control's behavior, not just
the presence of documentation or a clean tool result.

## Threat modeling

Threat model when design complexity, sensitive assets, trust boundaries,
external exposure, or impact justifies the effort. Keep the model proportional
to the change. Document:

1. Scope, assumptions, and explicit exclusions.
2. Assets and security-relevant data flows.
3. Actors, entry points, components, and trust boundaries.
4. Existing controls and threats relevant to the flows.
5. Mitigations, residual risks, owners, and evidence gaps.

Use STRIDE as a prompt when it fits (spoofing, tampering, repudiation,
information disclosure, denial of service, elevation of privilege). Do not
force categories that add no insight. A data-flow sketch or concise table may
be sufficient; do not invent architecture to complete a diagram.

## Risk classification

Use a supplied organizational rubric when available. Otherwise classify the
review's severity using impact, likelihood, exposure, required access and user
interaction, exploit complexity, affected data and population, blast radius,
and existing mitigations. Explain the factors that drive the result.

CVSS is a separate vulnerability scoring system. Use it only when the issue is
appropriate for CVSS, evidence supports the required metrics, and a score is
useful. Name the version and provide the vector alongside a score. Do not
derive a numeric score from the review severity alone. CVSS base, threat, and
environmental context are different views; do not present a base score as a
complete local risk assessment.

## Standards selection

Choose a small set of references that answers the review question. Verify the
edition from the official source when current version matters, and capture the
version/date used in the report. Standards organize review coverage; they do
not establish that every item applies or that a product is certified.

| Reference | Best fit | Official source |
| --- | --- | --- |
| OWASP Top 10 | Awareness categories for web application risks; not a verification checklist. | [OWASP Top 10](https://owasp.org/www-project-top-ten/) |
| OWASP ASVS | Testable security requirements for web applications and services. Cite version-qualified requirement identifiers. | [OWASP ASVS](https://asvs.owasp.org/) |
| OWASP API Security Top 10 | Awareness categories for API-specific risks. Verify the current edition. | [OWASP API Security Project](https://owasp.org/www-project-api-security/) |
| OWASP MASVS and MASTG | Mobile application controls and platform-specific verification guidance. Use together as applicable and verify current releases. | [MASVS](https://mas.owasp.org/MASVS/) · [MASTG](https://mas.owasp.org/MASTG/) |
| CWE | Classify a demonstrated weakness using a precise, maintained entry. CWE is a weakness taxonomy, not a severity score. | [CWE](https://cwe.mitre.org/) |
| CVE | Identify a publicly cataloged vulnerability when the affected component/version match. A CVE alone does not prove reachability or local impact. | [CVE Program](https://www.cve.org/) |
| CVSS | Communicate vulnerability characteristics and severity using a named version and vector. | [FIRST CVSS](https://www.first.org/cvss/) |
| NIST CSF | Organize cybersecurity risk outcomes and governance for organizational context; it is not an application test checklist. | [NIST CSF](https://www.nist.gov/cyberframework) |
| Secure SDLC guidance | Integrate security activities across requirements, design, implementation, verification, release, and maintenance. Select an applicable authoritative framework rather than assuming one prescribed lifecycle. | [NIST SSDF](https://csrc.nist.gov/Projects/ssdf) |

OWASP awareness lists, ASVS control requirements, CWE weakness identifiers,
CVE records, CVSS scores, and organizational risk severity are distinct
artifacts. Do not conflate them. A referenced standard release may change;
record the actual release used instead of treating this reference as a
permanent version assertion.

## Security requirements handoff

When a story or specification lacks a relevant security outcome, provide a
compact proposal with:

- Source story/specification ID and risk rationale.
- Proposed requirement phrased as observable system behavior.
- One or more verifiable acceptance criteria covering success and a meaningful
  denial or failure case.
- Any policy decision still needed from the product or security owner.
- Related review finding IDs, if known.

Examples of topics include authentication, resource-level authorization,
sensitive data handling, input constraints, audit events, rate limits, session
management, and tenant separation. Include only controls justified by the
specific flow. Send the proposal to `requirements-engineering`; do not silently
rewrite backlog items.

## Specification traceability

Use the existing specification format and lifecycle. Add or suggest a concise
`Security Review` section only where it is accepted by that format. Include a
review ID/date, assessed controls and their real state, linked findings,
pending actions, evidence paths, and applicable limitations. A security scan
alone cannot set a specification to `Passed`. For OpenSpec, use its existing
change artifacts and conventions; do not invent directories, modify its
structure, or bypass its lifecycle.

