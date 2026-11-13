---
name: <skill-name>
description: >
  <Short description of what the Skill does and when it should be used.>
metadata:
  version: "1.0.0"
---

# <Skill Name>

<Short explanation of the capability provided by the Skill.>

## Purpose

<What problem this Skill solves and what capability it provides.>

## When to use

Use this Skill when the user asks to:

- ...
- ...
- ...

## When not to use

Do not use this Skill when:

- ...
- ...
- ...

## Core Principles

### 1. <Principle>

<Rule or design principle.>

### 2. <Principle>

<Rule or design principle.>

## Inputs

### Required

- `<input>`
  - Description:
  - Constraints:

### Optional

- `<input>`
  - Description:
  - Default:

## Outputs

The Skill should produce:

- `<output>`
  - Format:
  - Requirements:

## Workflow

Execute the following process:

1. <Step>
2. <Step>
3. <Step>
4. Validate the result.
5. Return the final output.

## Rules

The Skill must:

- ...
- ...
- ...

The Skill must not:

- ...
- ...
- ...

## Constraints

- ...
- ...
- ...

## Tools

### Required

Use the following tools when necessary:

- `<tool>`
  - Purpose:
  - When to use:

### Optional

The following tools may be used when they provide value:

- `<tool>`
  - Purpose:
  - When to use:

Do not use tools when they are unnecessary.

## Composition

### Upstream Skills

Optional Skills that may provide inputs:

- ...

### Downstream Skills

Optional Skills that may consume outputs:

- ...

## Quality Criteria

The result is valid when:

- [ ] The Skill has one clear primary responsibility.
- [ ] Required inputs are clearly defined.
- [ ] Expected outputs are clearly defined.
- [ ] The workflow is deterministic where possible.
- [ ] The result satisfies the defined rules and constraints.
- [ ] The Skill can be reused in different contexts.
- [ ] The Skill does not duplicate responsibilities unnecessarily.
- [ ] The bilingual usage guide opens in Spanish with language links and provides
      equivalent descriptions, context, prompts, expected results, review criteria
      and execution status in both languages.

## Examples

See the bilingual usage guide at `examples/usage.md` for context, a copyable prompt,
expected results, review criteria, and execution status in English and Spanish.

<Authoring note: create examples/usage.md using skills/templates/usage-template.md
in this repository and turn the path above into a relative Markdown link to it.
Remove this note from the finished Skill. Add other examples
only when they teach a distinct case; keep operational instructions here in English.>

## Validation

Before returning the result:

1. Verify that the Skill fulfills its stated purpose.
2. Verify that all required inputs are processed.
3. Verify that the output follows the expected structure.
4. Verify that all rules and constraints are satisfied.
5. Verify that the quality criteria are satisfied.
6. Verify that the Skill maintains a clear and focused responsibility.
7. Verify that examples/usage.md contains equivalent English and Spanish sections,
   clear placeholders, valid links, and an accurate execution status. A documented
   prompt is not evidence that it was executed.

---

> Use only the sections that are relevant to the Skill.
> Do not add sections merely to satisfy the template.
> Keep the Skill focused, reusable, composable, and maintainable.
> Include the required bilingual usage guide; all other resources remain conditional.
