---
name: agentic-project-setup
description: >
  Analyzes, audits, and incrementally prepares any software repository for
  safe, effective AI-agent collaboration while preserving its proven structure
  and handing specialized work to the appropriate Skill.
metadata:
  version: "1.0.3"
---

# Agentic Project Setup

Prepare a software repository so AI agents can understand its context, follow
its conventions, find authoritative guidance, and make safe, verifiable
changes. This Skill is technology-agnostic: it starts from repository evidence
and adapts to the project's size, architecture, and actual needs.

## Purpose

Assess the agent-readiness of a project and, when authorized, make the
smallest incremental documentation and instruction changes that improve it.
This Skill owns discovery, readiness diagnosis, and collaboration context. It
does not own application implementation, architecture documentation, security
review, specification lifecycle management, or a multi-agent platform.

## When to use

Use this Skill when the user asks to:

- Prepare a new or existing software project for Codex or other AI agents.
- Inspect agent instructions, local Skills, AI configuration, or repository
  context and identify gaps.
- Establish or improve an `AGENTS.md` entry point and scoped agent guidance.
- Audit whether project context, quality checks, safety constraints, and
  navigation remain coherent for agents.
- Incrementally organize existing agent-related documentation without imposing
  a framework, stack, or directory tree.

## When not to use

Do not use this Skill to:

- Implement product features, refactor code, or install tools.
- Produce comprehensive architecture or backend documentation; hand off to
  `architecture-documentation` or `backend-documentation` when available.
- Perform a security assessment or threat model; hand off to
  `application-security-review` when available.
- Create, migrate, or manage specifications, ADR lifecycle, or OpenSpec; hand
  off to `spec-driven-development` when available.
- Create a reusable cross-project Skill; use `skill-factory` instead.
- Create specialized agents or subagents by default, or claim a target
  environment supports delegation without verification.

## Operating modes

Select one mode before acting. Default to **Analyze** when the user does not
specify one.

| Mode | Goal | File changes |
| --- | --- | --- |
| **Analyze** | Inspect the project, determine applicable dimensions, report evidence, gaps, and prioritized recommendations. | Never modify files. |
| **Setup** | Analyze first, agree on the targeted incremental plan when approval is required, then make and validate safe changes. | Only approved, non-destructive, evidence-based changes. |
| **Audit** | Reassess an existing agent setup for drift, contradictions, broken references, duplication, and instruction quality. | Never modify files. |

An explicit request to create or revise a particular low-risk instruction file
is authorization for that file only. In Setup mode, request approval before a
material policy decision, an ambiguous consolidation, moving or deleting files,
overwriting customized content, changing code or functional configuration,
installing dependencies, or handling secrets.

If the user first requests an analysis and later says to apply the
recommendations, update the setup, or improve it, continue in Setup mode using
the diagnosis as the scope. Apply clearly supported, low-risk documentation
changes without asking again for approval. If the request includes no clear
scope and a finding has materially different outcomes, ask only about that
decision. Reinspect each target before editing and pause for the protected
decisions listed above.

## Core principles

### Analyze before modifying

Do not impose a canonical repository layout. Inspect the project first, retain
working structures, and compare the actual state with the smallest useful
target state. A missing document is not automatically a deficiency.

### Evidence, status, and minimal change

Separate observed facts from reasonable inferences, user decisions, proposals,
and unknowns. Each proposed action must name its evidence, expected benefit,
priority, and affected files. Prefer updating authoritative material over
creating a parallel source of truth.

### Context is not capability

Instructions explain repository-specific work. Local Skills contain reusable
repository-specific procedures. Global Skills are installed reusable
capabilities. Do not copy a global Skill into a repository, create a local
Skill when instructions suffice, or assume documents under `.agents/` are
loaded without an explicit entry-point reference.

A portable agent definition, such as this library's `AGENT.md`, describes a
specialized responsibility; it is distinct from repository instructions such as
`AGENTS.md`. During project setup, inspect existing definitions and their
references when relevant, and ensure the intended host can access them. A
reference or filename alone does not install, activate, delegate to, or prove
host support for an agent. Follow the target host's actual discovery rules;
do not assume every host recognizes `AGENTS.md` or `AGENT.md` automatically.
Agent authoring remains with `agent-factory` when available.

### Safe, idempotent setup

Before changing a file, compare current and proposed content. Preserve useful
customizations and conventions. A repeated run must converge: it must not
duplicate instructions, documents, links, directories, or contradictory rules.

## Inputs

### Required

- A repository path or accessible project workspace.
- Requested mode, or permission to default to **Analyze**.

### Optional

- Intended agent platform, target scope, known pain points, desired output
  location, and approval boundaries.
- Existing project standards, architecture documentation, specifications,
  deployment details, CI configuration, design references, or security policy.
- Constraints such as supported tooling, monorepo ownership, regulated data,
  or preferred language for generated artifacts.

If information is absent, inspect what is accessible, label the limitation, and
continue with a bounded diagnosis. Do not infer technologies, commands,
ownership, policies, or decisions merely from common practice.

## Outputs

### Analyze and Audit

Return a diagnosis with:

- Project profile: purpose, scope, structure, detected technologies,
  conventions, and evidence limitations.
- Applicability assessment for every dimension with **Keep**, **Improve**,
  **Create**, **Consolidate**, or **Not applicable**.
- Findings: identifier, priority (`P0`–`P3`), finding, evidence, impact,
  proposed action, affected area, and confidence/status.
- A prioritized, non-destructive improvement plan; Audit also lists stale,
  duplicate, contradictory, or broken references.
- Open questions, assumptions, dependencies, and specialist-Skill handoffs.

### Setup

Produce the same pre-change diagnosis and an applied-change summary. Save only
approved, evidence-supported artifacts at established project locations. For a
Codex-compatible target, when there is no established equivalent, create a root
`AGENTS.md` entry point and
build a tailored `.agents/` knowledge structure when the project has confirmed
context or instructions that need a separate, discoverable home. Populate only
the documents agents need for the applicable dimensions, using repository
evidence and approved decisions. Create no placeholders or empty directories;
for a small project, one concise context document or root instructions alone
may be sufficient.

For other hosts, preserve an established entry point or use the host's verified
instruction convention. If its discovery behavior is unknown, state that
limitation and do not imply automatic loading or impose a host-specific filename.

The root `AGENTS.md` must be the navigable entry point for Codex-compatible
agents. It must state repository-wide rules and explicitly link or direct
agents to relevant scoped documents, commands, and local Skills. It must not
imply that `.agents/` files load automatically.

Repository-specific reusable procedures may be local Codex-compatible Skills
at `.agents/skills/<skill-name>/SKILL.md`. Record their triggering conditions
and limits from the entry point or applicable scoped instruction. Do not create
one merely to mirror an instruction document.

## Evaluation dimensions

Evaluate every dimension below for applicability. Inspection depth must be
proportionate to the evidence; **Not applicable** is a valid outcome.

| Dimension | Inspect for |
| --- | --- |
| Project context | Purpose, scope, languages, tools, modules, layout, key commands, conventions, constraints. |
| Architecture | Components, responsibilities, dependencies, patterns, flows, decisions, and useful diagrams. |
| Design | UI/UX, design system, visual components, tokens, responsive behavior, accessibility, navigation; only for projects with an interface. |
| Development | Code organization, naming, errors, validation, dependencies, environments, implementation rules. |
| Testing and quality | Unit, integration, E2E and contract tests; fixtures, mocks, coverage, mutation testing when relevant; linting, formatting, gates, and validation commands. |
| Security baseline | Secret handling, auth boundaries, input validation, dependency and configuration practices, sensitive data, agent safety rules. |
| Deployment and infrastructure | Environments, containers, cloud, IaC, releases, rollback, scaling, environment variables. |
| CI/CD | Pipelines, builds, automated checks, analysis, artifacts, publishing, deployments, releases, branch protections. |
| Data and databases | Schemas, migrations, ORMs, storage, pipelines, integrity, quality, backups, recovery. |
| APIs and integrations | Contracts, protocols, auth, webhooks, events, queues, external services, module interfaces. |
| Observability | Logs, metrics, traces, alerts, request correlation, error reporting. |
| Operations | Runbooks, troubleshooting, maintenance, incident response, health checks, backups, recovery. |
| Documentation | README, setup, technical, architecture, API, module, ADR, user, troubleshooting documentation. |
| Specifications and change management | Requirements, acceptance criteria, proposals, traceability, ADRs, OpenSpec, other SDD methods. |
| Agent collaboration | `AGENTS.md`, scoped instructions, AI configuration, local Skills, discoverability, approvals, real delegation capabilities. |

For every applicable dimension, classify the current state as **Keep**,
**Improve**, **Create**, or **Consolidate**. Use **Keep** for a sound,
discoverable arrangement; **Improve** for a bounded issue; **Create** only for
an evidenced gap; and **Consolidate** only after identifying the authoritative
source and obtaining approval when content must be moved or merged.

## Workflow

1. **Establish scope and mode.** Read repository instructions first. Confirm
   workspace, mode, user goal, and authority boundaries. In a monorepo,
   identify root and package/domain boundaries before treating root guidance as
   universal.
2. **Build an evidence inventory.** Inspect the tree and non-sensitive
   manifests, entry points, READMEs, documentation, instructions, AI
   configuration, local Skills, tests, quality tooling, infrastructure,
   delivery configuration, schemas, integrations, and operations evidence as
   relevant. Read existing guidance before proposing its replacement. Never
   read or expose secret values for this inventory.
3. **Profile the project.** Determine supported purpose, type, languages,
   frameworks, tooling, structure, architectural patterns, key commands, and
   constraints. Record evidence paths and label facts, inferences, unknowns,
   conflicts, and user-provided decisions distinctly.
4. **Assess dimensions.** Decide whether each dimension applies and assign its
   disposition. Look for strengths as well as gaps; do not recreate correct
   documentation or structures. Check that instructions point to authoritative
   sources, distinguish commands by evidence, and do not contradict each other.
   Where architecture rules or API specs are relevant, compare a representative
   sample of actual imports, route registrations and prefixes with the stated
   layer rules and current contracts. Record both paths and the observed
   difference; distinguish an intended exception, an older spec and an unknown
   authority. Search results alone do not establish full architectural compliance.
5. **Evaluate collaboration design.** Determine whether one agent can safely
   complete normal tasks. Consider specialized or parallel work only when
   independent domains, complexity, available tools, and conflict-free file
   ownership justify it. Verify actual delegation support. If justified,
   propose—not automatically create—a primary integrator and narrowly scoped
   specialists, including ownership, permitted tools, communication,
   consolidation, and validation. Otherwise state why a single agent or
   sequential workflow is preferable.
6. **Diagnose and prioritize.** Create evidence-based findings. Use `P0` for a
   critical safety, correctness, or blocking issue; `P1` for an important agent
   effectiveness risk; `P2` for a recommended improvement; and `P3` for an
   optional optimization. Separate facts, inferences, and questions.
7. **Plan changes.** In Analyze or Audit mode, stop after reporting the plan.
   In Setup mode, translate approved recommendations into a minimal change set,
   identify file-level effects and rollback approach, and request approval for
   protected decisions or destructive/ambiguous changes.
8. **Apply incrementally in Setup mode.** Reinspect targets immediately before
   editing. Preserve existing content and identifiers where possible; update
   links atomically within approved scope. Do not create empty directories,
   boilerplate dimensions, duplicate documents, or unrequested configurations.
9. **Validate and report.** Re-scan changed guidance and references; check
   paths, links, headings, scope boundaries, duplicate directives, and stated
   commands against evidence. Re-run safe existing checks only when relevant
   and authorized. Report changes, withheld recommendations, validation, and
   remaining questions.

## Rules

The Skill must:

- Remain independent of language, framework, cloud provider, architecture,
  agent platform, and repository size.
- Preserve working structures, local changes, ownership boundaries, and
  established conventions.
- Use actual evidence for every project claim; record source paths where useful.
- Keep root and scoped instructions concise, actionable, non-conflicting, and
  explicit about scope and precedence.
- Prefer root-only guidance for small projects; use scoped context in monorepos
  only where it resolves a real boundary or ownership difference.
- Treat security as baseline context and refer deeper review to a specialist
  Skill rather than asserting a security approval.
- Make document creation conditional on a concrete consumer, authoritative
  source, or repeated decision need.
- Validate actual ability to use agents or subagents separately from written
  definitions.

The Skill must not:

- Rebuild a functional repository into the reference layout or impose DDD,
  Clean Architecture, Hexagonal Architecture, MVC, a cloud provider, or any
  other pattern.
- Modify code, `.env` files, secrets, credentials, functional configuration,
  or dependencies without explicit authorization.
- Delete, move, rename, consolidate, or overwrite material automatically.
- Fabricate commands, tooling, policies, design systems, thresholds, owners,
  implementation details, or technical decisions.
- Duplicate documentation owned by `technical-documentation`,
  `backend-documentation`, `architecture-documentation`, or another dedicated
  Skill; provide a bounded handoff instead.
- Manage specification lifecycles, create OpenSpec, or migrate existing
  specifications automatically.
- Create all possible `.agents/` folders, platform configurations, local
  Skills, agents, or subagents by default.

## Constraints

- Do not modify files in Analyze or Audit mode.
- Do not read, print, commit, or relocate secret material. Treat the existence
  of secret-related files as sensitive metadata where appropriate.
- Do not run destructive commands, migrations, deployments, servers, or
  dependency installation merely to inspect readiness.
- Do not use a generic reference tree as a mandatory template. For example,
  `.agents/architecture/`, `design/`, `testing/`, `security/`, `deployment/`,
  `data/`, `integrations/`, `observability/`, and `operations/` are optional
  areas, not required directories.
- Treat existing uncommitted changes as user work. Avoid overlapping files
  without explicit authority and report the limitation.
- Use the repository's documentation language and conventions for generated
  artifacts unless the user requests otherwise.

## Tools

Use repository tree, search, file-reading, version-control status, and safe
validation tools as needed to establish evidence. Use build, test, lint, or
format commands only when they are already evidenced, relevant to the change,
and safe within the user's authorization. Do not require any particular tool,
runtime, or platform.

## Composition

This Skill prepares repository context for specialized capabilities; it does
not require them to be installed.

| Need discovered | Handoff when available |
| --- | --- |
| Reusable Skill design or local Skill scope | `skill-factory` |
| Reusable agent definition or agent authoring | `agent-factory` |
| Backlog and acceptance criteria | `requirements-engineering` |
| Specification lifecycle or SDD | `spec-driven-development` |
| Architecture evidence and diagrams | `architecture-documentation`, `system-design`, or `diagram-engineering` |
| Implemented backend behavior | `backend-documentation` |
| Security review | `application-security-review` |
| Tests, APIs, databases, deployment, review, technical docs | The relevant installed testing, API, database, DevOps, review, or documentation Skill |

Consume existing outputs as evidence when current and in scope. Never claim an
unavailable Skill ran, and do not make setup contingent on it.

## Quality criteria

The result is valid when:

- [ ] Mode, scope, authority boundary, and evidence limitations are clear.
- [ ] The project was inspected before recommendations or changes were made.
- [ ] Every dimension has an explicit applicability and disposition.
- [ ] Findings are evidence-based, prioritized, actionable, and distinguish
      facts from inferences, proposals, and open questions.
- [ ] Existing useful structure and documentation are preserved rather than
      recreated from a generic template.
- [ ] Agent instructions are discoverable, scoped, non-duplicative, and point
      to relevant authoritative material.
- [ ] Portable agent definitions and project instructions are distinguished;
      discovery and execution claims match evidence for the intended host.
- [ ] Local Skills, specialized agents, and subagents are proposed only where
      their value and real execution support are established.
- [ ] Setup changes are approved where required, incremental, safe, and
      idempotent; Analyze and Audit leave files unchanged.
- [ ] References and modified structures are valid, coherent, and free of new
      contradictory instructions.
- [ ] Responsibilities are handed to specialist Skills rather than duplicated.

## Validation

Before returning the result:

1. Confirm repository instructions and relevant agent guidance were read before
   diagnosis or setup planning.
2. Reconcile each finding with an inspected file, supplied evidence, or an
   explicitly labeled inference. Remove unsupported claims.
3. Verify each dimension has a justified disposition; verify non-applicable
   dimensions did not become boilerplate artifacts.
4. In Audit mode, check links, file references, document scope, precedence,
   duplicate guidance, stale references, and contradictions without editing.
5. In Setup mode, compare before/after content and structure, verify modified
   paths and references, check duplicate directives, and ensure no unapproved
   files or empty directories were created.
6. Verify that a created or changed root `AGENTS.md` is an explicit entry point
   and references relevant `.agents/` materials rather than relying on implicit
   loading.
7. Confirm no protected files, secrets, functional code, dependency,
   deployment, or destructive action changed without authority.
8. State checks actually performed, changes made, blocked checks, assumptions,
   pending decisions, and specialist handoffs.

## Examples and validation scenarios

Use these scenarios to check that the workflow adapts to different projects;
they describe expected decisions, not mandatory project layouts.

See [Diagnosis and minimal setup](examples/diagnosis-and-minimal-setup.md) for
an end-to-end example of reviewing existing agent guidance and applying a
selected recommendation in a follow-up request.

| Scenario | Expected behavior |
| --- | --- |
| New project with no agent configuration | Analyze evidence, identify only useful context and instruction gaps, propose a minimal entry point; do not invent commands or create files in Analyze mode. |
| Complete `.agents/` setup | Classify sound guidance as Keep and avoid reconstructing it. Report only evidence-backed improvements or drift. |
| Incomplete instructions | Identify missing scope, commands, ownership, or safety boundaries; propose the smallest evidence-backed completion. |
| Contradictory instructions | Identify precise conflicts, precedence, scope, and affected agents; propose an authoritative resolution but do not choose policy without authority. |
| Small project | Prefer a concise root instruction and avoid a directory taxonomy. |
| Multi-language monorepo | Identify package/domain boundaries and propose scoped guidance only where root instructions would be ambiguous. |
| OpenSpec | Preserve its approach, point agents to it, and hand lifecycle work to the appropriate SDD capability. |
| Custom specifications | Preserve the existing specification approach without automatically migrating it to OpenSpec or another methodology. |
| Layer rule conflicts with imports | Cite the written dependency rule and an actual cross-layer import; report the observed conflict and propose review without assuming the intended fix. |
| Old spec conflicts with an active route | Trace the full route including prefixes; cite both documents and code, and flag the spec's status as unknown until its authority is confirmed. |
| Local Skills | Validate discoverability, scope, and non-duplication with instructions; do not copy global Skills. |
| Portable agent definition | Identify the definition and project instructions separately; verify how the intended host accesses each and do not claim registration or delegation from a reference alone. |
| Documented CI/CD and infrastructure | Keep authoritative material, reference it as needed, and avoid duplicate deployment documentation. |
| Project with a design system | Assess design and accessibility only because an interface exists; preserve authoritative sources. |
| Project without an interface | Mark Design as Not applicable and create no UI guidance. |
| Justified specialist work | Propose non-overlapping roles with a single integrator only after verifying parallelism and environment support. |
| No justified delegation | Explain why one agent or sequential work is safer and more efficient; create no agent definitions. |

The key scenario is a well-configured project: a repeated Setup run must
preserve its structure and content, report Keep where appropriate, and make no
unnecessary reconstruction.
