# Workflow Authoring

This directory establishes how future reusable workflows are packaged. It
contains no workflow definitions or executable processes yet.

## Package convention

Use `workflows/<name>/WORKFLOW.md`, with YAML frontmatter for discovery and a
declarative Markdown process body. The stable kebab-case directory must match
frontmatter `name`. Keep optional supporting resources inside the package.

## Adding a workflow in a later phase

1. Identify a repeated process across capabilities. Confirm one existing Skill
   cannot already own it without unnecessary orchestration.
2. Read [common metadata and references](../contracts/components.md) and
   [the workflow contract](../contracts/workflows.md).
3. Start from [the authoring template](../templates/workflow-template.md).
   Declare required dependencies using canonical component names.
4. Define inputs and final outputs, then map step inputs, outputs, predecessor
   IDs, completion checks and failure handling. Reference procedures at their
   source rather than reproducing them.
5. Describe any tool operation and human decision explicitly. Keep provider
   configuration and executable commands outside the portable process definition.
6. Apply [the validation checklist](../validators/README.md). Before declaring
   `ready`, exercise the process in a selected host, including a blocked or failed
   dependency, and record the actual evidence.
7. Update the root catalog when a real workflow is added. Propose an executable
   representation only if a later consumer requires it.

The `Workflow` section inside an existing `SKILL.md` remains that Skill's internal
procedure. It is not automatically a separate workflow component.
