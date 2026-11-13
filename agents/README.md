# Agent Authoring

This directory establishes how reusable agents are packaged. The
[backend-engineer](backend-engineer/AGENT.md) is the first definition. Repository-wide `AGENTS.md` contains contributor
instructions; it is not a reusable agent definition.

## Package convention

Use `agents/<name>/AGENT.md` with a stable kebab-case directory matching frontmatter
`name`. Add local references or templates only when the agent needs them. Do not
use provider-native filenames as the canonical portable entry point.

## Adding an agent

1. Identify the delegated responsibility and justify it against the abstraction
   ladder in [the architecture](../docs/architecture.md).
2. Inspect existing Skills for reusable procedures and select the smallest set.
3. Read [common metadata and references](../contracts/components.md) and
   [the agent contract](../contracts/agents.md).
4. Start from [the authoring template](../templates/agent-template.md), replace
   placeholders, and declare only actual required dependencies.
5. Define selection, inputs, outputs, tool capabilities, authority, failure
   behavior and evidence. Reference Skill names without copying instructions.
6. Review using [the validation checklist](../validators/README.md). Before
   declaring `ready`, exercise representative tasks in a selected host and record
   the actual results and limits.
7. Update the root catalog when a real component is added. Add provider bindings
   only as separately scoped, tested integration work.

An authoring template or dependency reference does not install or activate an
agent. Never infer host execution support from the presence of this directory.
