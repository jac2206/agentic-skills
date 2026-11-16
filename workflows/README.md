# Workflow Authoring

Workflows define coordination across reusable capabilities. This directory contains
one draft reference process; it contains no executor or host integration.

## Catalog

| Workflow | Purpose | Status |
| --- | --- | --- |
| [Architecture and security review](architecture-security-review/workflow.yaml) | Pass an architecture assessment to a scoped security review using two existing Skills | Draft reference; statically reviewed, not host-tested |

The reference demonstrates dependencies, ordering, input/output handoffs and
blocked-step behavior. It does not create a new agent or execute either Skill.

## Package convention

Use `workflows/<name>/workflow.yaml`. The stable kebab-case directory must match
top-level `name`. Profile `2.0` replaces the earlier reserved `WORKFLOW.md`
convention; existing agents and Skills retain their entry points and metadata.
Keep optional supporting resources inside the package. Add a README only if it
provides distinct usage guidance; YAML remains the single process definition.

## Adding a workflow

1. Confirm the repeated process benefits from coordination across capabilities
   rather than one existing Skill.
2. Read [common metadata and references](../contracts/components.md) and
   [the workflow contract](../contracts/workflows.md).
3. Copy [the YAML template](../templates/workflow-template.yaml), replace every
   placeholder and declare required dependencies by canonical component name.
4. Define required/optional inputs, final outputs and step mappings. Use `needs`
   for predecessor IDs and source references for data handoffs. Check both graphs
   for cycles and review data meanings, not only their format labels.
5. State scope, authority, completion and failure rules. Select capabilities and
   modes without copying their internal procedures.
6. Apply [the validation checklist](../validators/README.md), keep the definition
   `draft` until representative host evidence exists, and update the root catalog.

## Using a definition

A caller may explicitly ask a capable host to read a workflow and its referenced
Skills, verify inputs and permissions, and follow the declared process. This is
manual interpretation, not native YAML execution. Check that each Skill is
actually available; a declared reference does not install it.

Until a host pilot is authorized, inspect the reference without executing it.
A future adapter may consume the same graph, but must separately verify supported
semantics, tool permissions and failure reporting. No CLI, editor extension or
web application is required to author or review definitions.

The `Workflow` section in an existing `SKILL.md` remains that Skill's internal
procedure, not an automatically separate workflow component.
