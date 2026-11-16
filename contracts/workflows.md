# Workflow Definition Contract

Profile `2.0` applies to `workflows/<name>/workflow.yaml` under the
[common contract](components.md). A workflow is a declarative process definition.
YAML makes its structure inspectable; it does not provide an executor, installation,
automatic delegation, or tool permissions.

## Responsibility and representation

Use a workflow for a repeated process across capabilities when one Skill does not
already own the responsibility. Reference Skills and agents without copying their
internal instructions. Keep the entire process in one canonical YAML document;
an optional README may explain usage but must not duplicate its steps.

Use one YAML 1.2-compatible document with string mapping keys and no duplicate
keys, custom tags, anchors, aliases, merge keys, or executable expressions. Quote
version strings. Unknown fields require a contract review rather than silently
acquiring runtime meaning. Optional component resources stay inside the package.

## Document fields

The seven common metadata fields are required: `contract_version`, `kind`,
`name`, `description`, `version`, `status`, and `dependencies`.
Use `contract_version: "2.0"` and `kind: workflow`.

The following process fields are also required:

| Field | Shape and meaning |
| --- | --- |
| `when_to_use` | Nonempty list of selection conditions |
| `when_not_to_use` | Nonempty list of exclusions |
| `inputs` | Nonempty mapping of input names to `description`, `format`, and boolean `required` |
| `preconditions` | List of conditions checked before starting; may be empty |
| `outputs` | Nonempty mapping of output names to `description`, `format`, and `source` |
| `steps` | Nonempty list of steps under the contract below |
| `constraints` | Nonempty list of scope, effects and authority boundaries |
| `failure_behavior` | Nonempty description of missing inputs, blocked work and partial results |
| `quality_criteria` | Nonempty list of observable final criteria |
| `validation` | Nonempty list of checks; distinguish static checks from future host tests |

Names of inputs, outputs and steps use lowercase kebab-case. Formats are
descriptive strings, not executable schemas. A consumer must check semantic
compatibility; a matching label alone does not establish compatible contents.

## Step contract

| Field | Shape and rule |
| --- | --- |
| `id` | Unique kebab-case step name |
| `uses` | Required `skill/<name>` or `agent/<name>` reference |
| `needs` | List of unique predecessor step IDs; `[]` for a root step |
| `inputs` | Mapping of names supplied to the capability to source references |
| `outputs` | Nonempty mapping of result names to `description` and `format` |
| `instructions` | Nonempty scope and mode guidance, without copying the capability's procedure |
| `completion` | Nonempty observable condition required before dependents proceed |
| `on_failure` | Literal `block_dependents`; no implicit recovery or retry |

Input mappings are plain source references, never interpolation or code:

- `inputs.<name>` selects a declared workflow input.
- `steps.<step-id>.outputs.<name>` selects a declared predecessor output.
- Final output `source` must use the second form and refer to an existing step.

A consumed step output must come from a predecessor reachable through `needs`.
All predecessor IDs must exist, and the graph must be acyclic, with no self edges.
All `uses` references must resolve and appear in common `dependencies`; avoid
unused required dependencies. A mapping name identifies an input to the selected
capability, not a parameter in an implemented calling API.

Profile `2.0` models bounded component steps only. Existing Skills or agents may
use their own permitted tools. Direct tool steps, human approval steps, branching,
loops, retries, concurrency and expression syntax are deferred until a demonstrated
consumer needs a separately reviewed contract. List order is for readability;
`needs` defines required ordering and does not authorize parallel execution.

## Boundaries and results

Check required inputs, accessible context, component availability and authority
before starting. Missing optional input remains absent; do not invent a value or
an implicit default. Missing required input blocks affected work. An unavailable,
failed or blocked required predecessor blocks dependent steps. Unrelated steps
are not implicitly authorized to continue.

Preserve useful partial results and evidence. Report `completed`, `partial`,
`blocked`, or `failed`, actual validations and remaining issues. Completion
requires all final outputs and quality criteria. Neither a dependency reference
nor a workflow file grants installation, execution or additional privileges.

## Validation and future execution

Static review covers YAML parsing, fields, identities, required references, cycles,
source mappings and consistency with the authoring template. Semantic review checks
the input/output meanings, scope, authority and absence of copied procedures.

Keep reference workflows `draft` until representative host tests exercise success,
missing input, unavailable capabilities and failed or blocked predecessors. Record
actual evidence separately from proposed scenarios. A future executor must reject
unsupported versions or semantics and preserve permissions. This contract does
not implement persistence, cancellation, resumption or provider bindings.
