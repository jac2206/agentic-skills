# Workflow Definition Contract

Applies to future `workflows/<name>/WORKFLOW.md` definitions using
[common contract 1.0](components.md). The definition is a declarative process for
review and guidance, not an executable workflow or engine-specific DSL.

## Responsibility and body

A workflow owns a bounded process across Skills, tools, agents, or human decisions.
State its purpose, use and exclusion conditions, required/optional inputs,
preconditions, final outputs, steps, failure behavior, quality criteria and
validation. Use a workflow only when coordination adds value beyond one Skill's
internal procedure. Do not extract or rewrite existing Skill workflows just to
populate this component type.

## Step contract

Describe steps in a Markdown table or equivalent explicit prose:

| Element | Rule |
| --- | --- |
| Step ID | Unique kebab-case name within the workflow |
| Uses | A typed Skill/agent reference, a named tool capability, or a human decision |
| Needs | Explicit predecessor IDs; state `none` for an initial step |
| Inputs | Named workflow inputs or named outputs from predecessor steps |
| Outputs | Named result and its format/evidence |
| Completion | Observable condition required before dependent steps proceed |
| On failure | Stop or mark dependent work blocked; identify any explicitly permitted recovery |

All required component references must appear in frontmatter `dependencies`.
Tool and human steps must identify their required capability or decision without
inventing a registered component. Input/output names must be declared and have
compatible meaning and format. Every consumed upstream output must come from a
predecessor reachable through `Needs`.

The step graph must be acyclic and all predecessor IDs must exist. Listing steps
does not imply parallel execution. Contract 1.0 uses a bounded dependency graph;
runtime branching, loops, scheduling and retry syntax are deferred until a tested
consumer needs them. Use separate explicitly scoped definitions rather than
inventing an execution language in a component body.

## Boundaries and results

The process selects a capability and checks its result. Internal Skill procedures
remain in `SKILL.md`; agent judgment remains in `AGENT.md`. A tool step describes
an operation, effects, permission boundary and expected result rather than a shell
command, SDK call or provider-specific configuration.

A failed or blocked required step prevents its dependent steps from being reported
complete. Preserve useful partial outputs and their evidence. No automatic retry
is assumed, especially for operations with side effects. Recovery must state its
preconditions and authority and must avoid duplicate effects.

Final output identifies completed, failed and blocked work, actual validations,
artifact locations and remaining issues. Use the result states `completed`,
`partial`, `blocked`, or `failed`; completion requires all declared final criteria.
These terms describe reports, not an implemented state machine.

## Future execution

Machine schemas, executable representations, state persistence, cancellation,
resumption and host bindings require a separate design and authorization. A future
executor must preserve ordering, contracts and permissions, and report unsupported
semantics explicitly. `WORKFLOW.md` alone does not promise automatic execution.
