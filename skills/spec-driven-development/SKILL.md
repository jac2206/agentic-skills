---
name: spec-driven-development
description: >
  Manage software changes through proportionate specifications, planning,
  implementation, verification, and closure while preserving existing project
  conventions and optionally integrating with OpenSpec.
metadata:
  version: "1.0.1"
---

# Spec-Driven Development

Manage a software change from its source through verifiable results, using the
smallest useful workflow and the project's authoritative change system.

## Purpose

Coordinate the lifecycle and traceability of a change. Adapt documentation and
checks to its complexity and risk; working software and evidence matter more
than ceremonies. This Skill works independently of technology or architecture.

## When to use

Use for a feature, user story, bug, refactoring, architectural or infrastructure
change, migration, integration, security improvement, or technical change
without a story, when the user wants the change managed or carried out with
appropriate specification and verification. Support backend, frontend, mobile,
APIs, monorepos, services, and other software systems.

## When not to use

Do not use for backlog engineering alone, project setup alone, a standalone
security audit, or documentation alone: use the relevant specialist when
available. Do not impose a specification lifecycle on an ordinary task whose
user did not request or need it.

## Inputs

Required: a change request or existing change, and accessible project context.
Optional: requested mode, scope, source requirements, acceptance criteria,
existing change artifacts, constraints, risks, and authorization boundaries.
Inspect available evidence; ask only when an unresolved business decision or
material ambiguity prevents safe progress. Label confirmed requirements,
assumptions, open questions, and pending decisions separately.

## Outputs

Produce only the artifacts needed by the selected mode in the existing system:
Analyze: diagnosis and recommended stages; Propose: proposal; Specify:
verifiable specification; Design: proportionate technical design; Plan:
ordered tasks; Implement: implementation and related tests; Verify: actual
results and evidence; Close / Archive: closure and history; Full Workflow:
the necessary combination. A concise response or plan may suffice. No HTML
report by default; visual reporting is optional on request.

## Workflow

1. **Discover.** Read applicable project instructions, scoped context,
   architecture, testing, security, infrastructure, and local Skills as
   relevant. Inspect version-control status and preserve local edits. Find
   requirements, active changes and their state, and specification systems,
   including `specs/`, `.agents/specs/`, `docs/specifications/`, custom and
   third-party systems. Search relevant project guidance as well as paths.
   Establish the authoritative source and reuse an equivalent active change;
   do not create another. If authority is unclear, report the conflict and
   avoid divergent changes until resolved. Record evidence and unknowns.
2. **Choose the minimum flow.** Select the requested mode; for a general change
   request use Full Workflow within the authorized scope. Explain the stages
   chosen or omitted based on impact, uncertainty, complexity, and risk.
   Small fixes may need analyze, implement, validate; a feature may benefit
   from specification and tasks; complex changes may need proposal and design;
   refactoring needs behavioral regression checks; security changes need risk
   and control verification. These are examples, not mandatory sequences.
   Analyze is strictly read-only. A single mode does not authorize later modes.
3. **Preserve the system.** Follow existing templates, state transitions,
   ownership, validation and history. Avoid duplicate sources and unrequested
   migrations. If no system exists, do not install tools or create directories
   by default. Use a brief plan or single document where sufficient; only if a
   durable system is needed consider a project-appropriate `specs/` with active
   and archive areas and only the files needed. The chosen system is the source
   of truth. Use [the lightweight template](templates/change.md) only when it
   helps and no existing template takes precedence.
4. **Execute the selected stages.** Use the mode contract below. Link artifacts
   and decisions rather than copying them. Continue independently on safe,
   in-scope work when another part is blocked. Update progress in the existing
   system and preserve history on repeat runs.
5. **Verify and report.** Apply the checks and closure rules below. Report what
   changed, evidence and actual commands/results, outstanding risks and
   decisions, and what was not run. Do not call a partial result complete.

## Modes

- **Analyze:** inspect without modifying files; identify conventions, system,
  equivalent active changes, scope, complexity, risks and evidence gaps;
  recommend stages and justify them.
- **Propose:** when warranted, define problem, motivation, goal, scope,
  exclusions, impact, dependencies, risks and measurable success criteria.
- **Specify:** describe expected behavior, not just files. As applicable capture
  identifier, name, goal, status, source, business rules, scenarios, acceptance
  criteria, contracts, expected errors, constraints, nonfunctional needs,
  dependencies and edge cases. Criteria must be observable and testable; use
  Gherkin only when it clarifies. Never invent business decisions.
- **Design:** where warranted, capture components, architecture, interfaces,
  data, flows, integrations, decisions, alternatives, risks and test strategy
  at the necessary level. A trivial change needs no extensive design.
- **Plan:** create small, ordered, verifiable tasks with goals, dependencies,
  completion criteria and progress. Use native states when present; otherwise
  Pending, In Progress, Blocked, Completed and Verified are suggestions.
  Verified requires evidence.
- **Implement:** execute authorized tasks within scope and architecture; add or
  update appropriate tests, record consequential decisions, and update progress.
  Identify deviations, contract and compatibility effects. For new requirements
  update the relevant authoritative artifacts before expanding scope; obtain
  approval for material scope or business decisions. Resolve routine choices
  safely using existing conventions.
- **Verify:** check applicable acceptance criteria, behavior, tests, security,
  contracts, quality, compatibility and documentation. Trace evidence to the
  requirement or task and distinguish actual execution from inspection.
- **Close / Archive:** verify the change and required gates, update current
  specifications and decisions in their authoritative location, record results
  and preserve history using native lifecycle rules. Never label incomplete
  work complete or automatically archive a change with failed mandatory checks.
- **Full Workflow:** combine only applicable stages above; selection does not
  override authorization boundaries or require every artifact.

## OpenSpec and existing systems

When OpenSpec is present, identify installation, version, configuration, active
changes and project conventions from actual evidence. Consult documentation for
that installed version, including official guidance when available, and
inspect the tool's own help before using commands. Follow its actual artifacts,
state transitions and validation; reuse existing changes and do not invent
commands or structure, change configuration needlessly, or create a parallel
system. If version, commands or guidance cannot be established, report the
limitation and avoid guessing; continue safe work using evidenced conventions.
When absent, assess whether it adds value but do not install it or create an
`openspec/` directory by default. Ask authorization before installation or
migration. Existing Markdown and other systems remain valid and are never
migrated automatically.

## Rules

Connect applicable source request or story → specification → tasks →
implementation → tests, and link proposals, design, security review, findings,
and final result when present. References suffice; do not duplicate a backlog,
security report, or full artifact, and never invent external identifiers.
Technical changes need no story. Do not modify stories without authorization.
Resolve contradictory or ambiguous requirements before dependent implementation;
record blocked decisions and proceed on independent work.

Before implementation, assess whether authentication, authorization, sensitive
data, validation, integrations, dependencies, infrastructure, AI/agents, or
attack surfaces are affected. Define proportionate controls and use or request
`application-security-review` where appropriate and available. During work
check those controls; during verification link applicable findings, mitigations,
tests and evidence. If specialist review is unavailable, record pending controls
or bounded checks without presenting them as an audit. Functional tests alone
cannot establish security. Do not alter the specialist's findings or reports
without authorization.

## Constraints

Request approval for consequential business decisions, material scope changes,
destructive operations, significant risks, installation or tool migration;
respect existing authorization and project instructions. Do not halt for
trivial decisions. Do not modify global instructions without authorization,
rebuild `.agents/`, overwrite local work, or change code outside scope.

## Verification and closure

For each applicable acceptance criterion and required gate, record evidence,
including actual commands and results when executed. Use native statuses or:
Passed, Failed, Partial, Blocked, Not Run, Not Applicable; explain applicability
and limitations. Check completed tasks, tests, contracts, security, documents,
remaining risks and material decisions. Never claim a test passed without
running it or mark a task Verified without evidence. A required Failed, Partial,
Blocked or Not Run gate, incomplete task, or unresolved required decision
prevents completion; preserve the active state and report the blocker. Record
accepted residual risks only when authorized. A validated change may be closed
and archived according to the existing system and authorized scope.

## Composition

- `agentic-project-setup` supplies context and conventions; recommend it when
  relevant context is missing, without requiring it or rebuilding its output.
- `requirements-engineering` owns backlog and business requirements; reuse its
  stories, rules, acceptance criteria and nonfunctional needs by reference.
- `application-security-review` owns specialist assessment and finding
  lifecycle; exchange references and evidence without duplicating reports.
- Use system design, testing (including `unit-testing-vitest` when relevant),
  code review, API testing, diagramming, database design, deployment and
  technical documentation Skills when available and appropriate. They are
  optional and own their specialized work.

## Quality criteria

- [ ] Scope, authority, existing active change and source of truth are clear.
- [ ] Selected stages and artifacts are justified by risk and complexity.
- [ ] Expected behavior and applicable acceptance criteria are verifiable.
- [ ] References connect requirements, work, tests and applicable security.
- [ ] Existing conventions, local changes and history are preserved.
- [ ] Results distinguish executed checks, failures, limitations and unknowns.
- [ ] Closure only occurs after all applicable mandatory gates pass.

## Validation

Before reporting, check these criteria against actual evidence, inspect changed
artifacts and links, and report missing or blocked evidence. See the illustrative
[small and complex examples](examples/change-scenarios.md); they are not rules.
