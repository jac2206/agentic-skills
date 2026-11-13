# Workflow Authoring Template

Use only for an authorized future workflow. Read the
[workflow contract](../contracts/workflows.md) and
[common contract](../contracts/components.md). Copy the fenced metadata as
frontmatter and the sections below to `workflows/<name>/WORKFLOW.md`; remove this
preface and replace all placeholders. This is not an executable workflow.

```yaml
---
contract_version: "1.0"
kind: workflow
name: <workflow-name>
description: <Process purpose and selection conditions.>
version: "0.1.0"
status: draft
dependencies: []
---
```

# <Workflow Title>

## Purpose

<One repeated process and why coordination across capabilities is useful.>

## When to use

<Selection conditions.>

## When not to use

<Exclusions and cases already covered by one Skill.>

## Inputs

<Named required/optional inputs, formats, preconditions and missing-input behavior.>

## Outputs

<Named final deliverables, formats, source step outputs and completion criteria.>

## Steps

| ID | Uses | Needs | Inputs | Outputs | Completion | On failure |
| --- | --- | --- | --- | --- | --- | --- |
| <step-id> | <kind/name, tool capability, or human decision> | <predecessor IDs or none> | <workflow inputs or predecessor outputs> | <named output and format> | <observable condition> | <stop or block; permitted recovery> |

## Constraints

<Scope, authority and permitted effects. Required component references belong in
dependencies. Tool steps describe effects and permissions without executable commands.>

## Failure behavior

<Blocked dependents, partial-output preservation, final reporting and recovery
conditions; no implicit retries.>

## Quality criteria

- [ ] <Observable final process criterion.>

## Validation

<How to check dependencies, graph, input/output mappings and final criteria.
Record actual host execution separately from planned scenarios.>
