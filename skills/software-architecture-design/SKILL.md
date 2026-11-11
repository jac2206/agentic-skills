---
name: software-architecture-design
description: >
  Analyze, design, evolve, compare, review, and validate software architectures
  against real requirements and constraints without prescribing a stack or pattern.
metadata:
  version: "1.0.1"
---

# Software Architecture Design

Design and evaluate technical solutions proportionate to actual needs, constraints
and evidence. Applies to new and existing backend, frontend, mobile, full-stack,
cloud, data, AI, integration and distributed systems.

## Purpose

Turn system needs and constraints into justified architectural choices, or assess
existing and proposed choices, without imposing unnecessary complexity.

## When to use

Use for an architectural diagnosis, target design, evolution, comparison, design
review or requirements-based validation, from a small change to a whole system.

## When not to use

Do not substitute for requirements engineering, implementation, security audit,
specification lifecycle management, visual UI/UX design, or comprehensive
evidence-based documentation of implemented systems. Compose with specialists
when those deliverables are requested.

## Inputs

Required: the goal or problem and scope, or enough accessible project context to
establish them. If a critical missing decision prevents a defensible recommendation,
ask a focused question; otherwise proceed with explicit assumptions and conditions.

Optional: requirements and acceptance criteria; quality targets; existing code,
configuration, diagrams, decisions and documentation; budget, team skills,
expected workload, operations and deployment practices; alternatives, mode and
output location. Distinguish user-reported context from independently observed
facts. Never invent workloads, targets, budgets, requirements, components or
existing behavior. Identify unknowns, conflicts, impact and evidence needed to
resolve material gaps.

## Outputs

Provide only what serves the requested scope: a diagnosis, proposal, comparison,
review, validation matrix, component boundaries and contracts, decisions,
diagrams, risks, evolution plan or validation criteria. A concise decision may
suffice. Label current, reported, inferred and proposed elements; cite relevant
project evidence and identify assumptions, open decisions, limitations and next
checks. Relate significant choices to requirements, quality and constraints.

## Modes

Choose the requested mode; if ambiguous infer it from the goal and state the
choice. Modes may be combined when requested; their restrictions still apply.

| Mode | Result and boundary |
| --- | --- |
| Analyze | Evidence-based diagnosis of existing components, responsibilities, dependencies, integrations, constraints, quality attributes, risks and debt. Never modify files. |
| Design | Propose a new system or feature, with relevant boundaries, choices and validation. |
| Evolve | Propose changes against the evidenced current state, including compatibility, transition and rollback when relevant. |
| Compare | Compare plausible alternatives against context-specific criteria and recommend conditionally; explain uncertainty. |
| Review | Assess a supplied design against requirements and constraints; prioritize supported issues, impacts and remedies, including strengths. |
| Validate | Trace requirements and constraints to decisions and evidence; identify satisfied, violated, unverified and unknown items. Report actual checks separately from proposed tests. |

Outside Analyze, write requested artifacts only within the user's authorized scope
and existing project conventions. Do not modify application code without explicit
authorization. A design request alone does not authorize implementation.

## Workflow

Apply only necessary steps, at a depth proportional to the decision:

1. **Scope and evidence.** Establish mode, goal, boundaries, authorization and
   audience. Inspect applicable instructions, conventions, architecture and
   decisions, relevant code, configuration and tests when accessible. Preserve
   existing work. Separate observed facts, reported facts, inferences, proposed
   elements and unknowns, with sources.
2. **Needs and constraints.** Identify relevant business objective, users,
   functional needs, quality attributes, workload, stack, team, cost, deployment,
   operations and organizational limits. Record measurable targets only when
   supplied or verified; flag missing targets and their decision impact.
3. **Alternatives.** For consequential choices compare plausible options,
   including retaining the current or a simpler design when viable. Select
   relevant criteria: complexity, cost, performance, scalability, security,
   operations, maintainability, team experience and migration risk. State evidence
   and uncertainty; do not invent numeric scores. Explain the recommendation,
   trade-offs, conditions and reasons to revisit it. For small changes a brief
   rationale is sufficient.
4. **Design or assess.** Define applicable context, responsibilities, boundaries,
   dependencies, communication and contracts, persistence, events, integrations,
   security, observability, deployment, scalability, resilience and evolution.
   Trace important decisions to needs and quality attributes. Consider relevant
   integration concerns such as compatibility, authentication, authorization,
   errors, timeouts, retry safety, idempotency, consistency, versioning and circuit
   breakers without prescribing them universally. Consult [design considerations](references/design-considerations.md)
   when a domain or migration needs deeper prompts.
5. **Communicate decisions.** Use a diagram only when it clarifies the solution
   or is requested. Select an appropriate context, container, component, sequence,
   deployment, data or event view; prefer editable Mermaid or Draw.io when
   available. Mark proposed nodes and relationships and include existing ones only
   when supported. Match diagram and narrative. Delegate specialized diagram
   generation to `diagram-engineering` if available and applicable. Record material
   decisions as ADRs when useful, using existing project conventions and location;
   include context, problem, alternatives, decision, rationale, consequences and
   risks. Do not create ADRs for trivial choices.
6. **Validate and report.** Map material requirements and constraints to decisions
   and evidence or explicit gaps. Check boundaries, flows, contracts, dependencies,
   security, operability, cost and migration risks as applicable. Distinguish
   reasoning from executed tests, results and limits. Provide next checks, open
   questions and handoffs. Respect existing locations; do not impose directories,
   HTML or slides.

## Rules

- Select patterns and technologies for demonstrated needs and trade-offs, never
  by default. Monoliths, modular monoliths, microservices, layered, Clean,
  hexagonal, DDD, event-driven, CQRS, event sourcing, serverless, microfrontends,
  BFF, MVC/MVVM, data and agent architectures are options, not requirements.
- Separate responsibilities and reduce coupling where beneficial; do not add
  abstractions, components, services or diagrams without a reason.
- Never claim a future design is implemented or theoretical validation is a
  passed test. Label assumptions about proposed elements and relationships.
- Consider cost and operations alongside quality, security, reliability and
  delivery constraints. Avoid generic recommendations or universal winners.

## Constraints

- Respect existing conventions and authoritative documents; avoid duplication and
  overwriting user work. Do not modify user stories without authorization.
- Security design is not a security audit, and architecture review is not a
  certification. Never claim guarantees unsupported by evidence.

## Composition

Optional handoffs, only when applicable and available:

- `agentic-project-setup`: consume context and conventions; do not rebuild `.agents/`.
- `requirements-engineering`: consume requirements and quality needs; do not own backlog management.
- `spec-driven-development`: provide technical analysis and decisions; do not manage proposals, tasks or archival.
- `application-security-review`: supply trust boundaries for specialist assessment; incorporate findings without substituting for it.
- `architecture-documentation`: hand off labeled design and evidence; it owns its documentation package and labels proposals as such.
- `backend-documentation`: consume verified implemented behavior; do not replace its implementation tracing.
- `ui-ux-design-system`, API and data specialists: respect their contracts and design decisions; do not duplicate specialist responsibilities.
- `diagram-engineering`: delegate specialized diagram work when available.

## Quality criteria

The result is ready when applicable criteria are supported by evidence:

- [ ] Important decisions trace to needs and constraints and are proportionate.
- [ ] Boundaries and modularity are justified, internally consistent, maintainable and operable.
- [ ] Security and relevant quality attributes are addressed within scope.
- [ ] Material trade-offs, uncertainty and risks are visible.
- [ ] Proposed elements are distinguished from implemented behavior.
- [ ] Verifiable designs specify checks for material claims and their limits.

## Validation

1. Check the mode, authorization, evidence and status labels.
2. Trace relevant requirements and constraints to decisions and identify gaps.
3. Review quality attributes, alternatives and trade-offs for consequential decisions.
4. Check consistency of prose, contracts and diagrams, and migration and operations when relevant.
5. Identify unknowns and unverified items; distinguish checks actually run from planned validation.

Consult [examples](examples/design-scenarios.md)
for illustrative new design, evolution and comparison; they are not mandatory patterns.
See [scenario walkthroughs](examples/scenario-walkthroughs.md) for bounded review cases.
