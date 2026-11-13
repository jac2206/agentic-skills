# Common Component Contract

Contract version: `1.0`. This is a normative authoring contract, not an executable
schema, runtime protocol, or implemented discovery API.

## Profiles and entry points

| Kind | Canonical entry point | Identity | Version source |
| --- | --- | --- | --- |
| `skill` | `skills/<directory>/SKILL.md` | Existing frontmatter `name` | Existing `metadata.version`, when present |
| `agent` | `agents/<name>/AGENT.md` | Frontmatter `name` | Frontmatter `version` |
| `workflow` | `workflows/<name>/WORKFLOW.md` | Frontmatter `name` | Frontmatter `version` |

The agent entry point is a repository-defined portable format, not a Codex
`AGENTS.md` instruction file or a host-native agent registration. Renaming
it does not install or activate it. See the agent contract for this boundary.

Skills retain their existing profile. Do not add `kind`, `contract_version`,
`status`, `dependencies`, or a top-level `version` to existing Skills to make
them conform to the new agent/workflow profile. Existing prose composition links
are not automatically required install dependencies.

Discovery is limited to these canonical locations and entry points. Exclude
authoring templates, READMEs, contracts, documentation, examples, and hidden or
generated directories. `skills/skill-factory/templates/` is authoring material,
not a separate Skill. A future discovery
implementation must preserve these exclusions rather than scan every Markdown
file for metadata.

## Agent and workflow metadata

Future definitions require these YAML frontmatter fields:

| Field | Type and rule |
| --- | --- |
| `contract_version` | String `"1.0"`; selects this authoring contract |
| `kind` | String `agent` or `workflow`, matching its directory and entry point |
| `name` | Nonempty stable kebab-case string matching its package directory |
| `description` | Nonempty English summary of purpose and selection conditions |
| `version` | String of three nonnegative integers, `MAJOR.MINOR.PATCH` |
| `status` | String `draft`, `ready`, or `deprecated` |
| `dependencies` | List of unique required component references; use `[]` when none |

Names match `^[a-z0-9]+(?:-[a-z0-9]+)*$` and are unique within a kind. Do not
require a second `id` duplicating `name`. Versions start at `0.1.0` for a draft;
breaking input, output, identity, or authority changes increment the major version,
compatible capability additions increment minor, and corrections increment patch.
The contract version is independent of each component's content version.

`draft` means incomplete or awaiting validation. `ready` requires the declared
quality checks and representative host execution evidence; a well-formatted file
alone is insufficient. `deprecated` requires a reason and migration guidance in
the body. These statuses are not retroactively inferred for Skills.

Do not add provider, model, credentials, SDK, or editor settings to portable
metadata. Evolve the written contract before adding shared metadata fields;
component-specific explanation belongs in the body.

## References and dependency resolution

A reference is `<kind>/<name>`, using `skill`, `agent`, or `workflow`. Resolve the
name from frontmatter, not a guessed directory name. For example,
`skill/html-presentations` resolves to `skills/presentations/SKILL.md` in this
checkout. This example illustrates identity only; it introduces no dependency.

`dependencies` lists every component required for the definition to fulfill its
declared behavior. Optional suggestions belong in the body, explicitly marked
optional, and cannot be assumed available. A direct required reference in an agent
capability table or workflow step must appear in `dependencies`; transitive
dependencies remain owned by the referenced component.

For this phase the resolution scope is one repository revision. Require exactly
one matching definition per reference. Missing, ambiguous, wrong-kind, self, or
cyclic required references are errors. Do not invent external search, aliases,
download behavior, version ranges, or fallback components. A future installer must
resolve and record versions before using more than one source revision.

Links to authoring documentation are not runtime dependencies. A component may use
the host's ordinary tools directly; tools are declared by capability in the body,
not resolved as library components through `dependencies`.

## Shared content requirements

Every future agent/workflow definition must state its purpose, when to use and
avoid it, inputs and preconditions, outputs, constraints, quality criteria, and
validation method. It must distinguish required inputs from optional context and
explain missing-input behavior. The type-specific contracts define the remaining
requirements: [agents](agents.md) and [workflows](workflows.md).

Keep operational instructions at the owning entry point. Link detailed resources
and explain when to read them. Package-local resource links must resolve inside
the component directory; do not assume sibling resources are installed together.
Declare reuse of another component by reference instead of copying its procedure.

Root contracts/templates are authoring aids. Installed definitions must carry
their own component-specific boundaries and refer to declared capabilities; they
must not require a checkout-relative link to root authoring documents to run.

## Evolution and compatibility

Changing an existing Skill is separate from adding an agent/workflow consumer.
Do not normalize Skill names, filenames, resources, or metadata during discovery.
Reject an unsupported contract version explicitly. Treat new shared required
fields or incompatible semantics as a contract revision, with migration guidance
and consumer checks before adoption.

Source definitions remain authoritative. A future generated catalog may expose
kind, name, description, version, status when declared, entry-point path, and
required references. Do not maintain another authoritative manifest in parallel.
