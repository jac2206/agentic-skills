# Agent Authoring Template

Use only for an authorized future agent. Read the [agent contract](../contracts/agents.md)
and [common contract](../contracts/components.md). Copy the fenced metadata as
frontmatter and the sections below to `agents/<name>/AGENT.md`; remove this preface,
replace all placeholders, and retain no links to root authoring resources in the
installed definition. This file is not an agent or runtime configuration.

```yaml
---
contract_version: "1.0"
kind: agent
name: <agent-name>
description: <Purpose and observable selection conditions.>
version: "0.1.0"
status: draft
dependencies: []
---
```

# <Agent Title>

## Purpose

<One delegated responsibility; why an existing Skill or workflow is insufficient.>

## When to use

<Selection signals.>

## When not to use

<Exclusions and overlapping capability boundaries.>

## Inputs

<Required and optional context, scope, preconditions and missing-input behavior.>

## Outputs

<Deliverable format, evidence and completion criteria.>

## Capabilities

<Required kind/name references, selection conditions and expected results.
Add all required references to dependencies; label optional suggestions separately.>

## Tools and authority

<Required/optional capabilities, effects, permissions, prohibitions and missing-tool behavior.>

## Coordination

<Scoped input preparation, capability selection and result checks; reference
Skill procedures without copying them.>

## Handoffs

<State whether delegation is needed. If used, define task ownership and transfer
of scope, inputs, constraints, expected results and evidence.>

## Failure behavior

<Blocked, failed and partial-result handling; explicitly permitted recovery.>

## Quality criteria

- [ ] <Observable criterion for the delegated responsibility.>

## Validation

<How to check criteria, including representative host tasks; distinguish planned
scenarios from executed checks and record limits.>
