# AI Skills

A reusable library of focused, composable capabilities for AI agents.

This repository contains Skills that help AI systems perform specialized tasks consistently across projects. The goal is to build reusable capabilities, not a collection of one-off prompts.

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
├── examples/                         # Concrete artifacts produced with Skills
│   ├── architecture/
│   ├── docs/
│   ├── presentations/
│   ├── projects/
│   └── requirements/
└── skills/
    ├── agentic-project-setup/         # SKILL.md and an end-to-end setup example
    ├── application-security-review/   # Evidence-based application security assessment and remediation validation
    ├── architecture-documentation/   # SKILL.md, references, templates, examples, scripts
    ├── backend-documentation/        # SKILL.md and optional templates
    ├── presentations/                # Skill name: html-presentations
    ├── project-documentation-blueprint/
    ├── requirements-engineering/     # SKILL.md and backlog templates
    ├── software-architecture-design/ # Proportionate architecture design and evaluation
    ├── spec-driven-development/ # Adaptive, traceable software change lifecycle
    ├── skill-factory/
    ├── ui-ux-design-system/         # Adaptive interface and design-system design
    └── templates/                    # Shared Skill authoring template
```

The repository contains eleven Skills. Every Skill must have a `SKILL.md`; add references, templates, examples, or scripts only when they provide real value. Keep Skill-specific resources inside that Skill's directory. The shared Skill authoring template lives under `skills/templates/`.

Use the root `examples/` directory for representative artifacts generated with Skills. Keep instructional examples and reference fixtures that a Skill needs after installation inside that Skill's directory. A separate README inside each Skill is not required; `SKILL.md` is its operational entry point and this root README is the library catalog.

The [`projects/loyalty-rewards` foundation](examples/projects/loyalty-rewards/README.md) demonstrates an agent-ready project context for a loyalty system. It contains instructions and documented decisions, not runnable application code or deployment configuration.

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

Replace `architecture-documentation` with a Skill name such as `agentic-project-setup`, `application-security-review`, `architecture-documentation`, `backend-documentation`, `html-presentations`, `project-documentation-blueprint`, `requirements-engineering`, `spec-driven-development`, `software-architecture-design`, `ui-ux-design-system`, or `skill-factory`. The `presentations/` directory declares the Skill name `html-presentations` in its frontmatter.

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

### Agentic Project Setup

Analyzes, audits, and incrementally prepares any software repository for safe, effective AI-agent collaboration while preserving its established structure and handing specialized work to the appropriate Skill.

### Application Security Review

Assesses application and software-delivery security risks, reviews changes, documents evidence-based findings, and helps validate authorized remediations across technology stacks.

### Backend Documentation

Documents an existing backend from implementation evidence. It traces implemented use cases and maintains an evidence-based system overview and use-case documentation.

### Architecture Documentation

Creates evidence-based application architecture documentation with Mermaid and editable Draw.io component diagrams, a separate provider-specific Draw.io infrastructure diagram, and native Archify output when that Skill is installed.

### HTML Presentations

Creates presentation-grade HTML slide decks, with guidance for narrative, visual composition, diagrams, layout, and runtime validation.

### Project Documentation Blueprint

Analyzes project evidence and produces a structured visual blueprint for project documentation, including narrative and diagram guidance.

### Software Architecture Design

Analyzes, designs, evolves, compares, reviews, and validates software architectures against actual needs and constraints without prescribing patterns or technologies.

### Spec-Driven Development

Manages software changes through proportionate specifications, implementation, verification, and closure, preserving existing conventions and optionally integrating with OpenSpec.

### Skill Factory

Designs, creates, reviews, and improves reusable Skills, and helps choose whether a problem needs a prompt, Skill, workflow, agent, or application.

### Requirements Engineering

Turns business needs and source requirements into a traceable backlog of epics, features, and user stories with testable acceptance criteria, business rules, and readiness statuses.

### UI/UX Design System

Designs, implements, audits, and evolves accessible user interfaces and design systems across web and mobile. It preserves explicit or existing identities and uses the bundled JAC Design System when no identity is established. Interface design requests default to a reviewable HTML prototype; an explicitly requested editable Figma design is also produced when suitable tools and access are available.

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

## Contributing

When adding or improving a Skill:

1. Identify the problem and confirm that a Skill is the right abstraction.
2. Define one clear responsibility, inputs, and outputs.
3. Write the workflow, rules, and constraints.
4. Add measurable quality criteria and validation.
5. Review related resources for consistency.
6. Keep the Skill focused, composable, and as simple as possible.

Follow the repository's `AGENTS.md` instructions. Repository documentation and Skill definitions are written in English; generated artifacts should use the language requested by the user or present in the input material.

## Licensing

This repository does not currently define a licensing policy for individual Skills. Do not add a `license` field to Skill frontmatter unless the repository adopts one.
