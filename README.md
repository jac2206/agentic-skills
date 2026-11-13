# Agentic Skills — Reusable AI Components

A reusable library of focused, composable capabilities for AI systems.

This repository contains Skills that help AI systems perform specialized tasks consistently across projects. The goal is to build reusable capabilities, not a collection of one-off prompts.

The eleven original Skills retain their structure and behavior. Agent Factory
extends the library to twelve Skills and uses the existing contracts and templates
to author reusable agent definitions. The repository also defines authoring
standards for future workflows; it includes no agent definitions, executable
workflows, adapters, or repository-specific CLI.

Start with [the architecture and roadmap](docs/architecture.md)
and [validation evidence](docs/architecture-validation.md).

## Philosophy

Choose the simplest abstraction that solves the problem correctly:

```text
Prompt → Skill → Workflow → Agent → Application
```

A Skill is useful when a capability is reusable, specialized, structured, and valuable across multiple tasks. A one-time request may need only a prompt.

## Repository structure

```text
agentic-skills/
├── AGENTS.md
├── README.md
├── agents/                           # Future agent packaging and authoring guide
│   └── README.md
├── contracts/                        # Common, agent and workflow authoring contracts
├── docs/                             # Architecture and validation evidence
├── examples/                         # Concrete artifacts produced with Skills
│   ├── architecture/
│   ├── design/
│   ├── docs/
│   ├── presentations/
│   ├── projects/
│   └── requirements/
├── skills/
│   ├── agent-factory/
│   ├── agentic-project-setup/
│   ├── application-security-review/
│   ├── architecture-documentation/
│   ├── backend-documentation/
│   ├── presentations/                # Declared Skill name: html-presentations
│   ├── project-documentation-blueprint/
│   ├── requirements-engineering/
│   ├── software-architecture-design/
│   ├── spec-driven-development/
│   ├── skill-factory/
│   ├── ui-ux-design-system/
│   └── templates/                    # Existing Skill authoring template
├── templates/                        # Agent and workflow authoring templates
├── validators/                       # Review rules; shared automation deferred
└── workflows/
    └── README.md                     # Future workflow packaging and authoring guide
```

The repository contains twelve Skills. Every Skill must have a `SKILL.md` and a
bilingual `examples/usage.md`; add other references, templates, examples, or scripts
only when they provide real value. Keep Skill-specific resources inside that
Skill's directory. Shared Skill authoring templates live under `skills/templates/`.

Use the root `examples/` directory for representative artifacts generated with Skills. Keep instructional examples and reference fixtures that a Skill needs after installation inside that Skill's directory. A separate README inside each Skill is not required; `SKILL.md` is its operational entry point and this root README is the library catalog.

The current `.gitignore` excludes root example outputs and `.archify/` working
files. They may exist locally without being distributed by Git. This architecture
phase preserves that policy; explicitly review it before publishing a showcase.

The local `examples/projects/loyalty-rewards/` foundation, when present, demonstrates
an agent-ready project context for a loyalty system. It contains instructions and
documented decisions, not runnable application code or deployment configuration.

## Component authoring resources

| Resource | Purpose | Availability |
| --- | --- | --- |
| [Skills](#skills) | Reusable procedures and their supporting resources | Twelve Skills |
| [Agents](agents/README.md) | Bounded delegated judgment using referenced capabilities | Authoring guide; definitions deferred |
| [Workflows](workflows/README.md) | Process ordering, input/output mapping and failure rules | Authoring guide; definitions deferred |
| [Common contract](contracts/components.md) | Identity, metadata profiles, references and discovery boundaries | Written authoring contract |
| [Agent template](templates/agent-template.md) / [Workflow template](templates/workflow-template.md) | Starting structures for future components | Authoring templates only |
| [Validation](validators/README.md) | Cross-component review checks and future automation conventions | Manual checklist; no shared executable |

The existing [Skill template](skills/templates/skill-template.md) remains canonical
for Skill authoring. The [usage template](skills/templates/usage-template.md) supplies
the required English and Spanish guide structure. Root templates are for component
authors; templates used by a Skill to produce deliverables remain inside that Skill.

## Repository documentation

The documents under `docs/` are intended to be versioned with the repository:

- [Architecture and roadmap](docs/architecture.md): component responsibilities,
  organization, decisions, and future integration boundaries.
- [Architecture validation](docs/architecture-validation.md): the dated record of
  checks performed when preparing the repository architecture.
- [Agent Factory validation](docs/agent-factory-validation.md): the dated review of
  that Skill's initial authoring and integration, with execution limits.

Validation records describe their inspected snapshot, not a continuously updated
inventory or proof of later runtime behavior. Keep durable decisions and useful
evidence here; a separate report for every change or Skill is not required.
Skill-specific usage guides belong inside their packages and are linked below.
Do not ignore `docs/` as a whole. Exclude temporary outputs or private material
individually when needed; the current `.gitignore` keeps these documents versionable.
Contributing agents classify outputs by purpose and report what should be versioned
or excluded. Generating a file does not make it temporary, and preparing files for
Git does not itself authorize a commit or publication.

## Install a Skill

The repository is the canonical source. Install Skills into Codex, Claude Code, or another supported agent with the [`skills` CLI](https://github.com/vercel-labs/skills). The CLI places or links each Skill into the selected agent's expected directory; no per-agent copies need to be maintained in this repository.

Install one Skill for Codex and Claude Code in the current project:

```sh
npx skills add jac2206/agentic-skills --skill backend-documentation --agent codex --agent claude-code
```

Install that Skill globally so it is available across projects:

```sh
npx skills add jac2206/agentic-skills --skill backend-documentation --agent codex --agent claude-code --global
```

Install every Skill in the collection for both agents:

```sh
npx skills add jac2206/agentic-skills --skill "*" --agent codex --agent claude-code
```

Install every Skill globally:

```sh
npx skills add jac2206/agentic-skills --skill "*" --agent codex --agent claude-code --global
```

To install the version from your current checkout (including local changes), run this from the repository root:

```sh
npx skills add . --skill architecture-documentation --agent codex --global --copy
```

For example, install the UI/UX Skill globally from this checkout:

```sh
npx skills add . --skill ui-ux-design-system --agent codex --global --copy
```

Replace `architecture-documentation` with a Skill name such as `agent-factory`, `agentic-project-setup`, `application-security-review`, `architecture-documentation`, `backend-documentation`, `html-presentations`, `project-documentation-blueprint`, `requirements-engineering`, `spec-driven-development`, `software-architecture-design`, `ui-ux-design-system`, or `skill-factory`. The `presentations/` directory declares the Skill name `html-presentations` in its frontmatter.

### Update installed Skills

These commands work in terminals on Windows, macOS, and Linux with Node.js and
`npx` available.

#### Update from a recorded remote source

If the Skills were installed globally from GitHub and the changes have been
pushed to their recorded source and branch, update all globally installed
Skills with:

```sh
npx skills update --global
```

This checks all eligible global Skills, including those from other repositories.
To update one by name:

```sh
npx skills update backend-documentation --global
```

To update the six Skills listed below:

```sh
npx skills update skill-factory agentic-project-setup application-security-review architecture-documentation backend-documentation requirements-engineering --global
```

Run `npx skills list --global` to view globally installed Skills. For
project-installed Skills, use `npx skills update --project`. The CLI may skip
Skills installed from local paths or sources it cannot check automatically;
read its output to see what was updated or skipped.

#### Update from this local checkout

From the repository root, reinstall all Skills from the current checkout for
Codex globally, including local changes that have not been pushed:

```sh
npx skills add . --skill "*" --agent codex --global --copy
```

To update just one Skill, replace `"*"` with its name. Add
`--agent claude-code` to also install for Claude Code. To update only the six
Skills listed above from the checkout:

```sh
npx skills add . --skill skill-factory --skill agentic-project-setup --skill application-security-review --skill architecture-documentation --skill backend-documentation --skill requirements-engineering --agent codex --global --copy
```

`--copy` installs the Skill directory and its supporting resources as a copy.
Reinstalling replaces the selected installed copies, so preserve any edits you
made directly in those copies first. Restart the agent or open a new session if
it does not immediately discover the updated instructions.

To update the architecture design, specification, and UI/UX Skills together
from the current checkout:

```sh
npx skills add . --skill software-architecture-design --skill spec-driven-development --skill ui-ux-design-system --agent codex --global --copy
```

Reinstall a globally installed Skill from a specific branch of this repository:

```sh
npx skills remove --global architecture-documentation

npx skills add https://github.com/jac2206/agentic-skills/tree/master/skills/architecture-documentation --global --copy
```

Replace `master` with the branch containing your changes if they have not been merged there yet. The remove command deletes the global installation; the add command installs a copy from the selected branch.

For example, install the application security review Skill from this checkout:

```sh
npx skills add . --skill application-security-review --agent codex --global --copy
```

## Skills

The first column links to each canonical definition and shows the declared name
used by the installer. Each usage guide opens in Spanish and links to its English
section using ordinary Markdown navigation. Both sections include a brief Skill
description, representative prompt, required context, expected result, review
criteria, and execution status. They describe the same task and authority boundaries.

| Skill | Capability | Usage |
| --- | --- | --- |
| [agent-factory](skills/agent-factory/SKILL.md) | Designs, creates, improves and validates portable agent definitions; does not install or execute agents. | [Guide and prompt](skills/agent-factory/examples/usage.md) |
| [agentic-project-setup](skills/agentic-project-setup/SKILL.md) | Assesses and incrementally prepares repositories for AI collaboration. | [Guide and prompt](skills/agentic-project-setup/examples/usage.md) |
| [application-security-review](skills/application-security-review/SKILL.md) | Assesses application and delivery risks and validates authorized remediations. | [Guide and prompt](skills/application-security-review/examples/usage.md) |
| [architecture-documentation](skills/architecture-documentation/SKILL.md) | Creates evidence-based architecture documents, Mermaid/Draw.io views and optional native Archify output. | [Guide and prompt](skills/architecture-documentation/examples/usage.md) |
| [backend-documentation](skills/backend-documentation/SKILL.md) | Documents implemented backend behavior and use-case flows from source evidence. | [Guide and prompt](skills/backend-documentation/examples/usage.md) |
| [html-presentations](skills/presentations/SKILL.md) | Creates self-contained HTML slide decks with presentation controls and visual guidance. | [Guide and prompt](skills/presentations/examples/usage.md) |
| [project-documentation-blueprint](skills/project-documentation-blueprint/SKILL.md) | Turns project evidence into a visual, navigable HTML Blueprint. | [Guide and prompt](skills/project-documentation-blueprint/examples/usage.md) |
| [requirements-engineering](skills/requirements-engineering/SKILL.md) | Produces traceable backlogs with stories, acceptance criteria and explicit readiness. | [Guide and prompt](skills/requirements-engineering/examples/usage.md) |
| [skill-factory](skills/skill-factory/SKILL.md) | Designs, creates, reviews and improves focused reusable Skills. | [Guide and prompt](skills/skill-factory/examples/usage.md) |
| [software-architecture-design](skills/software-architecture-design/SKILL.md) | Designs and evaluates architectures against actual requirements and constraints. | [Guide and prompt](skills/software-architecture-design/examples/usage.md) |
| [spec-driven-development](skills/spec-driven-development/SKILL.md) | Manages proportionate change specifications, implementation, verification and closure. | [Guide and prompt](skills/spec-driven-development/examples/usage.md) |
| [ui-ux-design-system](skills/ui-ux-design-system/SKILL.md) | Designs and evolves interfaces and design systems, preserving identity and producing requested design deliverables. | [Guide and prompt](skills/ui-ux-design-system/examples/usage.md) |

### Using the guides

1. Open the project where the task should be performed. Ensure the selected Skill
   is installed or make its canonical entry point and supporting files accessible.
2. Read the Spanish section or select English at the top of the guide. Replace
   angle-bracket placeholders with real paths or scope. Output paths in prompts
   are relative to the target workspace.
3. Paste the prompt into the agent environment you use. The prompts are natural
   language requests, not custom CLI commands, and remain subject to that host's
   capabilities and permissions.
4. Review the actual result against the listed criteria and record any unavailable
   checks. The guides are illustrative scenarios, not a record of passed tests.

`SKILL.md` remains the operational source of truth. The guides are illustrative
documentation, not additional operational rules. Skill Factory and the authoring
templates require this bilingual guide for new Skills. Skill Factory is now version
1.2.0 because its authoring workflow gained new requirements; other Skill versions
are unchanged. Generated deliverables may use the language requested in the prompt.

## Skill design

Each Skill should define, in proportion to its complexity:

- Purpose and when to use it.
- When not to use it.
- Inputs and outputs.
- A clear workflow.
- Rules and constraints.
- Measurable quality criteria and validation.

Skills should have one clear responsibility, remain reusable across projects, and compose with other Skills without duplicating their work.

## Composition

Skills can be combined into a larger workflow while retaining separate responsibilities. For example:

```text
Research → Content Development → Presentation Design → Generation → QA
```

Future agents will select Skills by typed references such as
`skill/html-presentations`, load their canonical instructions, pass scoped inputs,
and check their results. Workflows will define ordering and handoffs across
capabilities. Tools perform concrete operations supplied by the consuming host.
Neither an agent nor a workflow should duplicate a Skill's instructions.

Canonical future packages are `agents/<name>/AGENT.md` and
`workflows/<name>/WORKFLOW.md`. These neutral formats do not imply native runtime
support. Codex, Strands Agents and other integrations require separate verified
bindings. The existing external Skill installer commands above remain separate
from any future repository CLI.

## Contributing

When adding or improving a Skill:

1. Identify the problem and confirm that a Skill is the right abstraction.
2. Define one clear responsibility, inputs, and outputs.
3. Write the workflow, rules, and constraints.
4. Add measurable quality criteria and validation.
5. Review related resources for consistency.
6. Keep the Skill focused, composable, and as simple as possible.

Follow the repository's `AGENTS.md` instructions. Operational definitions and
technical documentation are written in English. User-facing usage guides include
English and Spanish sections, maintained through Skill Factory and the usage
template; this is the explicit language exception. Generated artifacts should use
the language requested by the user or present in the input material.

For a future agent or workflow, follow its authoring guide and contracts, keep
resources local, declare required dependencies, and record actual validation
evidence. Do not create functional components merely to fill the directory tree.
All new operational content, identifiers and filenames must be English; user-facing
usage sections follow the bilingual exception above. Preserve inherited Skill
resources rather than renaming or translating them during unrelated changes.

## Licensing

This repository does not currently define a licensing policy for individual Skills. Do not add a `license` field to Skill frontmatter unless the repository adopts one.
