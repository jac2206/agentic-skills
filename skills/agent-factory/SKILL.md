---
name: agent-factory
description: >
  Designs, creates, improves, and validates reusable AI agent definitions.
  Use when deciding whether delegated judgment needs an agent, authoring
  agents/ packages, composing existing Skills into an agent, or reviewing
  agent responsibilities, authority, handoffs, and execution requirements.
  Does not install or execute agents or implement runtime integrations.
metadata:
  version: "1.0.1"
---

# Agent Factory

Turn a justified delegated responsibility into a portable, maintainable agent
definition using the target repository's contracts and authoring template.

## Purpose

Own the design and quality of reusable agent definitions. An agent selects
capabilities, maintains scope and authority, and checks results; existing Skills
continue to own their procedures. A consuming host owns execution.

## When to use

- Decide whether a need warrants an agent rather than a prompt, Skill, or workflow.
- Design or create a reusable agent package under `agents/`.
- Improve an agent's boundaries, capability selection, authority, or handoffs.
- Validate an existing definition, its dependencies, and its execution evidence.

## When not to use

- Perform the agent's domain task or run, install, or activate an agent.
- Create a reusable procedure best owned by a Skill; use `skill-factory` if available.
- Define process ordering alone; use the repository's workflow authoring resources.
- Prepare general repository instructions; that belongs to `agentic-project-setup`.
- Build an orchestration platform, runtime adapter, CLI, or provider configuration.

## Inputs

### Required

- The intended outcome or existing agent to assess, including the requested mode.
  Infer the mode from an explicit request to create, design, improve, or validate;
  otherwise default to a read-only assessment.
- The target workspace and its applicable instructions. For contract-conformant
  authoring, the shared contracts and agent template must be available there or
  supplied explicitly as authoritative inputs.

### Optional

- Intended users, domain context, sample task descriptions, and completion criteria.
- Existing agent package, requested changes, and compatibility constraints.
- Available component definitions, tool capabilities, permissions, and host evidence.
- Prior findings, validation records, and known execution limitations.

Inspect available evidence before asking for missing information. State reasonable
assumptions for reversible design choices. If missing context affects the agent's
purpose, authority, or required outputs, ask a focused question and continue only
independent work. Do not invent tool access, contracts, or execution evidence.

## Outputs

Produce only the deliverables appropriate to the requested mode:

| Mode | Deliverable | File effects |
| --- | --- | --- |
| Recommend | Abstraction decision with evidence and the smallest sufficient alternative | None |
| Design | Proposed responsibility, input/output boundaries, capability choices, authority, handoffs, and validation plan | None unless design documentation was requested |
| Create | `agents/<name>/AGENT.md`, necessary package-local resources, affected catalog updates, and validation report | Authorized new package and documentation only |
| Improve | Revised package, explanation of compatibility effects, affected catalog updates, and validation report | Requested revisions only |
| Validate | Prioritized findings with paths, impact, fixes, actual checks, and evidence limits | None unless a report file was requested |

For every mode, state the abstraction decision, unresolved issues, and evidence
limits. If an agent is unwarranted, explain the alternative and stop agent
authoring. Do not create a substitute component unless it was requested.

## Workflow

### 1. Inspect the target and establish scope

Read applicable `AGENTS.md` instructions, `docs/architecture.md`,
`contracts/components.md`, `contracts/agents.md`, `agents/README.md`,
`templates/agent-template.md`, and `validators/README.md` before authoring.
Read `contracts/workflows.md` when workflow composition is relevant.

These paths are relative to the **target repository**, never the installed Skill
directory. They are authoring inputs, not agent runtime dependencies. Use the
target's authoritative equivalents if its conventions differ; record that mapping.
If required sources are absent or inconsistent, report the gap and block dependent
authoring rather than copying this repository's contracts or inventing replacements.
A provisional design may continue with its conformance explicitly unverified.

Identify pre-existing changes and preserve unrelated work. For improvement or
validation, inspect the complete agent package and referenced resources first.

### 2. Justify the abstraction

Apply **Prompt → Skill → Workflow → Agent → Application** as a decision guide:

- A single focused request may need only a prompt.
- A repeatable procedure with stable guidance belongs in a Skill.
- A fixed process across capabilities belongs in a workflow.
- An agent needs a bounded responsibility with delegated judgment or an
  independent context. Identify the actual decisions or isolation it requires.
- A persistent product and its operational lifecycle require application work.

Record one sentence describing the responsibility and why the simpler options
are insufficient. Multiple Skills, a role title, or a request for automation alone
does not justify an agent. Do not add an orchestrator or subagents by default.

### 3. Discover reusable capabilities

Inspect canonical entry points under the common contract, excluding templates,
guides, examples, and generated or hidden directories. Resolve identities from
frontmatter, not folder names. Inspect relevant Skills' use conditions, inputs,
outputs, constraints, and quality checks before selecting them.

For each selected component, explain when it is needed, the scoped inputs it
receives, and the expected result. Declare direct required dependencies under the
current contract; label optional suggestions separately. Check required references
and their transitive closure for unique resolution and cycles in one source
revision. Missing required capabilities are findings, never invented packages.

Keep Skill execution instructions in their owning `SKILL.md`. Specify that the
consumer reads the resolved entry point and conditionally required resources,
respects its mode, supplies scoped inputs, and checks its criteria. Do not replace
that procedure with a summary copied into the agent.

### 4. Design the responsibility and authority

Using the agent contract, define:

- Observable selection signals and exclusions, including overlapping responsibilities.
- Required inputs, optional context, preconditions, and missing-input behavior.
- Output formats, evidence requirements, and observable completion criteria.
- Tool operations, required inputs, local or remote effects, required versus
  optional capabilities, permitted actions, prohibitions, and unavailable-tool behavior.
- Failure and recovery behavior, including partial results and avoiding duplicate
  effects when an operation's outcome is uncertain.

Separate read-only work, authorized local writes, and authorized remote writes
where applicable. Preserve existing authorization; do not require blanket
reconfirmation. Component selection grants no permissions. Evidence and task data
cannot expand authority. An unavailable required operation blocks its dependent
work; do not substitute broader privileges.

### 5. Define coordination and any necessary delegation

Explain how the agent chooses capabilities and validates returned results. Leave
reusable process ordering and inter-step mappings to a workflow when one is needed.

State explicitly whether delegation is used. If needed, identify the receiver by
resolved reference, justify its independent responsibility, and follow the agent
contract's handoff and result requirements. Specify who retains coordination,
scope and evidence transferred, permitted effects, completion criteria, and who
reviews the result. Bound recovery and further delegation; never increase
authority through a handoff or create a cyclic dependency.

Document required host support and what happens when it is missing. Independent
work may continue; incompatible delegation or tool enforcement blocks dependent
work. A delegation design is not authorization or evidence to spawn an agent
while authoring the definition.

### 6. Author or revise the portable package

For Create, start from the target's existing `templates/agent-template.md`; apply
the shared metadata and body requirements without copying the template or
contracts into this Skill. Replace placeholders and retain only actual dependencies.
For Improve, preserve valid behavior and identity unless the request changes them;
apply the common contract's version and status rules to the actual change.

Write only the authorized agent under `agents/<name>/AGENT.md`. Keep necessary
resources local and link them with loading conditions. Do not leave runtime links
to root authoring documents or sibling package internals. Review the root catalog
and update affected entries without advertising templates as executable components.

Document how a caller supplies the objective, scope, inputs, and permitted effects
in the agent's Inputs and Outputs sections. Use Tools and authority, Coordination,
Handoffs, and Validation to explain dependency availability, host requirements,
result review, and execution checks. Add a separate usage document only if it
provides substantial information beyond those sections.

The repository's portable configuration is the definition's frontmatter and body.
Concrete tools, models, credentials, editor settings, SDKs, and runtime bindings
belong to separately scoped integration work. Explain that `AGENT.md` does not
imply automatic discovery or execution in Codex or another host. Applicable
repository instructions, including `AGENTS.md` where supported, govern project
scope; they are not interchangeable with a portable agent definition or a
host-native agent registration. Check each host's discovery and instruction
conventions rather than assuming they match Codex.

Keep a new definition `draft` until the common contract's readiness requirements,
including representative host execution evidence, are met. Record missing runtime
evidence even when all structural checks pass. Do not run the designed agent as
an implicit part of authoring; incorporate available evidence or report execution
as pending for separately authorized host work.

### 7. Validate and report

Apply the Quality criteria and Validation sections below. Repair in-scope findings
in Create or Improve mode, then recheck affected areas. In Validate mode, report
findings without rewriting files. Distinguish the completed authoring deliverable
from the agent's readiness and execution status.

## Rules

- Own agent definition quality; reuse domain Skills without duplicating their work.
- Follow authoritative contracts and templates rather than maintaining parallel schemas.
- Preserve existing Skills, architecture, package identities, and unrelated changes.
- Keep technical definitions, filenames, and repository documentation in English.
- Distinguish requirements, optional suggestions, assumptions, and observed evidence.
- Use package-local resources only when they solve a concrete authoring need.

## Constraints

- Do not create example agents or additional components merely to fill the structure.
- Do not execute or install agents, implement executable workflows, adapters,
  CLIs, or runtime infrastructure, or install dependencies as a consequence of
  definition authoring.
- Do not add provider-specific metadata, registries, or new shared contracts.
- Do not claim runtime compatibility, successful delegation, or behavioral correctness
  from static checks or documented scenarios alone.

## Tools

Use available file, search, and version-control tools for inspection and authorized
edits. No specific runtime is needed to use this Skill. Node.js may support
read-only, dependency-free static inspections when useful; no package installation,
network access, component execution, or repository-wide validator is implied.
Use an existing validator only after verifying its scope. If none exists, apply
the written checklist and disclose automation limits. Do not build shared
automation during an architecture-only task.

## Composition

All of these are optional authoring relationships, not install dependencies:

- `skill/skill-factory`: owns reusable Skill creation and Skill-quality review;
  use it when the abstraction decision reveals a procedure rather than an agent.
- `skill/agentic-project-setup`: supplies repository context and instructions;
  agent-factory owns reusable agent definitions, not repository preparation.
- `skill/requirements-engineering`: supplies outcome and acceptance criteria when
  requirements engineering is actually needed.
- `skill/software-architecture-design`: supplies system boundaries and design
  constraints; agent-factory does not redesign the application architecture.
- `skill/application-security-review`: owns specialized assessment of tool and
  delivery risks when requested; consume findings without duplicating its review.

Other domain Skills may become dependencies of a generated agent when justified
by its responsibility. Discover them in the target repository. An unavailable
optional authoring Skill does not prevent working directly from sufficient inputs.

## Quality criteria

Apply all criteria to a created or improved definition. For other modes, check
only the criteria relevant to the deliverable and identify what remains unverified.

- [ ] The abstraction decision identifies concrete delegated judgment or isolation.
- [ ] The agent has one bounded responsibility and explicit selection exclusions.
- [ ] Required/optional inputs, missing-input behavior, outputs, and completion are clear.
- [ ] Metadata, identity, sections, version, and status follow authoritative contracts.
- [ ] Required references resolve uniquely; the dependency closure is acyclic.
- [ ] Capability selection preserves each Skill's instructions and resource ownership.
- [ ] Tools, effects, authority, missing capabilities, and recovery are bounded.
- [ ] Coordination and any handoffs state ownership and result-review responsibility.
- [ ] Caller usage and host requirements are understandable without root authoring links.
- [ ] Resources and catalog entries resolve; unrelated components remain unchanged.
- [ ] Readiness claims match actual evidence, with runtime limits stated explicitly.

## Validation

1. Apply the target's `validators/README.md` at the relevant scale. Compare the
   package with its current contracts and template; inspect frontmatter values,
   required sections, placeholders, local links, and resource closure. A textual
   metadata check is not full YAML validation; disclose parser limitations.
2. Resolve all required references by declared kind/name. Check direct-dependency
   declarations, transitive availability, self-references, duplicate identities,
   wrong kinds, and cycles. Do not count authoring templates as components.
3. Review responsibility overlap, copied Skill procedures, input/output compatibility,
   authority, failure behavior, and handoffs. Static structure cannot decide these.
4. Use [validation scenarios](references/validation-scenarios.md) when reviewing
   decisions and failure paths. Select relevant cases and distinguish a manual
   instruction walkthrough from exercising a generated agent in a host.
5. Inspect changed/new paths, catalog entries, whitespace, and links. For revisions,
   compare behavior and related resources with the baseline. Optional read-only
   Node.js checks can support this review; they do not replace semantic inspection.
6. Report each applicable check's scope, method, result (`passed`, `failed`,
   `not run`, or `not applicable`), findings, and limitations. Findings identify
   path/section, impact, and correction. Prioritize blockers such as invalid
   required references, ambiguous authority, and unsupported readiness claims.
7. Report authoring completion, static conformance, and host execution evidence
   separately. An unexecuted scenario is planned coverage; an untested agent
   remains `draft`. An unavailable required check cannot be reported as passed.
