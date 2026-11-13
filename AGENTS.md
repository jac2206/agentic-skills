# Reusable AI Components Repository — Agent Instructions

## Purpose

This repository preserves its reusable Skill library and establishes an architecture for reusable agents and workflows. It owns component definitions and authoring standards, not an application runtime.

The goal is not to collect prompts, but to build reusable capabilities that can be applied consistently across different projects, domains, and agents.

## Architecture and current phase

Read [the architecture](docs/architecture.md) before changing repository structure.
Use [the common contract](contracts/components.md), [agent contract](contracts/agents.md),
and [workflow contract](contracts/workflows.md) when authoring those component types.
Use [the validation checklist](validators/README.md) for cross-component review.

The current phase establishes documentation, contracts and authoring templates only.
It does not implement agents, executable workflows, a CLI, adapters or new dependencies.
Implement these only in a later explicitly authorized task; do not treat the
documented roadmap as permission to implement it.

## Core Principle

Always choose the simplest abstraction that correctly solves the problem:

**Prompt → Skill → Workflow → Agent → Application**

Do not create or use an Agent when a Skill or workflow is sufficient.

---

# Skill Design Principles

Every Skill should:

1. Have one clear responsibility.
2. Define when it should be used.
3. Define when it should not be used.
4. Clearly define its inputs.
5. Clearly define its outputs.
6. Define an explicit workflow.
7. Define rules and constraints.
8. Define measurable quality criteria.
9. Define how the result should be validated.
10. Avoid unnecessary instructions and duplication.
11. Be reusable across projects.
12. Be composable with other Skills.

Skills should be deterministic whenever possible.

---

# Skill Selection

Before executing a task:

1. Understand the user's actual objective.
2. Identify whether an existing Skill applies.
3. Select the smallest Skill that can solve the problem.
4. Load additional references only when required.
5. Execute the Skill workflow.
6. Validate the result against the Skill's quality criteria.

Do not use a Skill simply because it is available.

---

# Skill Composition

Skills should be designed so they can be combined without duplicating responsibilities.

For example:

```text
Research
    ↓
Content Development
    ↓
Presentation Design
    ↓
Presentation Generation
    ↓
Presentation QA
```

Each Skill should own only its part of the workflow.

Avoid creating large Skills that unnecessarily combine research, generation, validation, and publishing when those responsibilities can be separated.

---

# Repository Language

Repository instructions, component definitions, references, examples, templates, scripts, code, comments, filenames, directory names and technical documentation must be written in English. Preserve inherited filenames and existing Skill behavior unless a migration is explicitly authorized.

User-facing `skills/<directory>/examples/usage.md` guides are an explicit exception:
each must contain equivalent `## Español` and `## English` sections, with Spanish
first, brief descriptions and Markdown links for language navigation. Operational
Skill instructions and filenames remain in English.

Generated artifacts should normally use the language requested by the user or the language used in the input material.

Technical names, APIs, programming identifiers, and product names should remain in their original form.

---

# Repository Structure

The repository separates reusable component definitions, shared authoring resources,
architecture documentation and concrete generated artifacts.

```text
agentic-skills/
├── AGENTS.md
├── README.md
├── agents/          # Authoring guide; future <name>/AGENT.md packages
├── contracts/       # Shared authoring contracts
├── docs/            # Architecture, evidence and decisions
├── examples/
├── skills/          # Existing library and Skill authoring template
├── templates/       # Agent and workflow authoring templates
├── validators/      # Cross-component checks; manual in the current phase
└── workflows/       # Authoring guide; future <name>/WORKFLOW.md packages
```

## Skills

All reusable Skills must live under `skills/`. Preserve existing Skill packages
and keep supporting resources inside their owner. Skill Factory owns the canonical
Skill and usage authoring templates under `skills/skill-factory/templates/`.
Do not migrate or normalize them when adding another component type.

Each Skill is self-contained:

```text
skills/
└── skill-name/
    ├── SKILL.md
    ├── references/
    ├── templates/
    ├── examples/
    └── scripts/
```

`SKILL.md` and a bilingual `examples/usage.md` guide are required for each Skill.

Other supporting resources are optional and should only be created when they provide real value.

- `references/` — supporting knowledge and detailed guidance.
- `templates/` — reusable templates and starting points.
- `examples/` — examples that document or demonstrate how the Skill itself should be used.
- `scripts/` — executable utilities required by the Skill.

Skill-specific resources must remain inside the corresponding Skill directory.

Do not create root `references/`, `scripts/`, or component-specific deliverable-template
directories. Root `templates/` is reserved for shared agent/workflow authoring;
Skill authoring templates are bundled under `skills/skill-factory/templates/`.
Templates used to produce a
component's deliverables remain inside that component.

Do not create empty directories simply to follow the structure. Add a directory only when it provides real value.

## Agents and workflows

Follow [agent authoring](agents/README.md) or [workflow authoring](workflows/README.md)
when a later task explicitly requests a new component. Future canonical entry points
are `agents/<name>/AGENT.md` and `workflows/<name>/WORKFLOW.md`.

Reference reusable components by kind and declared name under the common contract.
An agent selects Skills and checks results; a workflow owns ordering and handoffs.
Neither copies the internal procedures of its referenced Skills. Required references
must resolve, and required dependency graphs must be acyclic.

Describe tools by capabilities, effects and permission boundaries. Concrete tool
bindings, model selection, credentials and framework configuration belong to a
future host integration, not portable definitions. Never assume installation,
execution, delegation support or permissions from a reference alone.

Shared authoring contracts are not new runtime dependencies for existing Skills.
Keep component-local resources packaged with their owner. Do not create registries,
groups, adapters, lockfiles or runtime folders without a demonstrated consumer.

---

# Repository Examples

The root-level `examples/` directory contains concrete artifacts generated using the Skills. Store complete or representative generated outputs there, organized by category.

For example:

```text
examples/
└── presentations/
    └── presentation.html
```

These files demonstrate the output produced by a Skill and are not part of the Skill definition itself. They may be linked from a Skill as reference outputs, but should not be stored under that Skill's directory.

Generated artifacts should not be placed in the repository root.

Use:

```text
skills/<skill-name>/examples/
```

for instructional examples or reference fixtures that the Skill links to and needs in order to teach or perform its workflow. Keep them clearly identified as examples, not rules. A complete output package intended as a repository showcase belongs under root `examples/`; bundle it with the Skill only when the Skill itself needs that reference package after installation.

Use:

```text
examples/<category>/
```

for concrete artifacts generated by using a Skill.

Do not confuse these two purposes.

---

# README Files

The repository-level `README.md` is the library catalog and contains shared installation and contribution guidance. `SKILL.md` is the canonical instruction file for each Skill; future agents and workflows use their own canonical entry points under the common contract.

When adding, renaming, or removing a Skill, review the repository README and update its catalog, structure, and installation examples where affected. Discover Skills from their `SKILL.md` frontmatter rather than assuming that a directory name is the installable Skill name. Keep this file focused on repository-wide instructions instead of duplicating the catalog.

Apply the same catalog review when adding, renaming or removing an agent/workflow.
Do not advertise templates or authoring guides as installed or executable components.

Do not add a separate `README.md` inside every Skill by default. Add one only when that Skill has a distinct human-facing packaging, setup, or contribution guide that cannot be covered clearly in its `SKILL.md` or the repository README. Avoid duplicating Skill instructions across README files.

---

# SKILL.md Structure

Every Skill should follow this general structure:

```text
---
name:
description:
metadata:
---

# Skill Name

## Purpose

## When to use

## When not to use

## Inputs

## Outputs

## Workflow

## Rules

## Constraints

## Quality criteria

## Validation

## References

## Examples
```

`SKILL.md` must not include a `license` field unless the repository explicitly adopts a licensing strategy for Skills.

Not every section must contain extensive content. Keep the Skill proportional to its complexity.

---

# References

References contain detailed domain knowledge that should not unnecessarily increase the size of the main Skill instructions.

Use references for:

- Detailed technical guidance.
- Patterns.
- Standards.
- Domain-specific rules.
- Large examples.
- Advanced cases.

The main `SKILL.md` should contain the operational rules required to execute the Skill.

References should support the Skill rather than duplicate its instructions.

---

# Templates

Templates contain reusable structures for generating outputs.

Examples:

- Presentation templates.
- Document structures.
- Code skeletons.
- Configuration templates.
- Report formats.

Templates must not replace the Skill instructions.

The Skill explains when and how to use the template.

---

# Examples

Examples demonstrate how a Skill should be applied.

Examples should be clearly separated from operational instructions.

Do not treat examples as mandatory rules unless explicitly stated in the Skill.

Examples inside a Skill should remain focused on teaching or demonstrating the Skill.

The required bilingual usage guide contains a representative prompt and review
criteria, not a second copy of the operational instructions. Use
`skills/skill-factory/templates/usage-template.md` as its authoring scaffold. Keep the root
README's catalog linked to the canonical definition and guide.

Concrete generated artifacts intended to demonstrate actual Skill output should be stored under the repository-level `examples/` directory.

---

# Scripts

Scripts may be included when deterministic automation or validation provides meaningful value.

Examples:

- Static validation.
- Rendering.
- File generation.
- Formatting.
- QA.
- Data transformation.

Prefer deterministic scripts over asking the agent to perform repetitive manual operations.

Scripts should remain inside the Skill that owns them unless they are genuinely shared infrastructure. Future cross-component static validators belong in `validators/`; keep existing Skill artifact validators in their packages. Do not implement shared automation during the architecture-only phase.

---

# Quality

A Skill is not complete merely because it produces an output.

Quality must be evaluated through explicit criteria.

Whenever possible, validation should verify:

- Correctness.
- Completeness.
- Consistency.
- Maintainability.
- Reusability.
- Compliance with the Skill rules.
- Absence of avoidable errors.

Validation should be proportional to the complexity and risk of the Skill.

Report checks actually performed separately from documented scenarios or planned tests. Do not treat the presence of instructions or examples as evidence that a Skill was executed successfully.

---

# Changes to Existing Skills

When improving a Skill:

1. Preserve its original responsibility.
2. Remove ambiguity.
3. Remove redundant instructions.
4. Resolve conflicting rules.
5. Improve determinism.
6. Improve validation.
7. Avoid unnecessary complexity.
8. Keep backward compatibility when practical.

Do not expand a Skill into unrelated responsibilities.

When operational instructions or required outputs change, review and update the
Skill's `metadata.version`: compatible capability additions use a minor increment,
corrections a patch, and incompatible behavior changes a major increment. Translation
or presentation-only usage changes do not automatically require a version increment.

When modifying a Skill, also review its references, templates, examples, and scripts to ensure they remain consistent with the updated Skill definition.

---

# Naming

Use lowercase kebab-case for Skill directories.

Examples:

```text
presentation-design
software-development
testing
prompt-engineering
data-analysis
video-generation
```

Skill names should describe the capability rather than a specific implementation.

Prefer:

```text
presentation-design
```

over:

```text
ppts-slides-santi
```

unless the Skill intentionally represents a specific branded implementation.

---

# Generated Artifacts

When a Skill generates an artifact during development, testing, or demonstration:

1. Do not place the artifact in the repository root.
2. Store concrete demonstration artifacts under the appropriate repository-level `examples/` category.
3. Keep Skill-specific instructional examples inside the Skill's `examples/` directory.
4. Use clear, descriptive filenames.
5. Do not add generated artifacts to the repository unless they provide meaningful demonstration or testing value.

For example:

```text
skills/
└── presentations/
    └── examples/
        └── presentation-structure.md
```

is a Skill example, while:

```text
examples/
└── presentations/
    └── ai-systems-talk.html
```

is a generated presentation artifact.

---

# Version Control and Generated Material

Classify new files by purpose, not by whether an agent generated them. Keep reusable
components, usage guides, contracts, templates, architecture and useful validation
records versionable. Exclude disposable outputs, caches and scratch files with
narrow `.gitignore` rules only when such files are actually produced.

Inspect current ignore rules before changing them. Do not blanket-ignore `docs/`,
`skills/` or all generated files, hide meaningful deliverables, or untrack existing
files merely to make an ignore rule apply. Preserve existing output policies unless
the task authorizes changing them. Report intended versioned files and exclusions;
stage, commit or push only when covered by the user's authorization.

---

# Final Principle

The objective of this repository is to build a professional library of reusable AI capabilities.

A good Skill should be:

**Clear → Focused → Reusable → Composable → Testable → Maintainable**
