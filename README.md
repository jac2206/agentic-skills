# AI Skills

A reusable library of Skills for AI agents.

This repository contains structured capabilities designed to help AI systems perform specialized tasks consistently, reliably and across different projects.

The goal is not to build a collection of prompts.

The goal is to build **reusable capabilities for AI systems**.

---

## Philosophy

AI capabilities can be organized into different levels of abstraction:

```text
Prompt
  ↓
Skill
  ↓
Workflow
  ↓
Agent
  ↓
Application
```

We use the simplest abstraction that solves the problem correctly.

A Skill should be created when a capability is:

- Reusable.
- Specialized.
- Structured.
- Valuable across multiple tasks.
- Better represented as a repeatable workflow than as a single prompt.

---

## Repository Structure

```text
ai-skills/
│
├── AGENTS.md
├── README.md
│
├── skills/
│   ├── presentations/
│   │   └── SKILL.md
│   │
│   ├── testing/
│   │   └── SKILL.md
│   │
│   ├── software-development/
│   │   └── SKILL.md
│   │
│   ├── education/
│   │   └── SKILL.md
│   │
│   ├── prompt-engineering/
│   │   └── SKILL.md
│   │
│   └── automation/
│       └── SKILL.md
│
└── tests/
```

Skills may start as a single `SKILL.md` file.

As complexity increases, a Skill may introduce:

```text
references/
templates/
examples/
scripts/
```

Only add these directories when they provide meaningful value.

---

# Skills

## Presentations

Creates presentation structures and presentation-ready content based on audience, objective, narrative, duration and visual requirements.

The Skill can be used for:

- Presentations.
- Talks.
- Keynotes.
- Masterclasses.
- Workshops.
- Technical presentations.
- Executive presentations.
- Educational presentations.
- Slide decks.
- Turning documents or scripts into presentations.

---

## Testing

Provides guidance for designing and implementing automated tests.

It can cover:

- Unit testing.
- Integration testing.
- API testing.
- End-to-end testing.
- Test doubles.
- Coverage.
- Mutation testing.

---

## Software Development

Provides reusable development practices for designing, implementing, reviewing and improving software.

Potential areas include:

- Architecture.
- Backend.
- Frontend.
- APIs.
- Databases.
- Testing.
- Security.
- CI/CD.
- Cloud.

---

## Education

Provides reusable patterns for designing educational content.

Examples include:

- Classes.
- Workshops.
- Exercises.
- Laboratories.
- Evaluations.
- Student guides.
- Progressive learning paths.

---

## Prompt Engineering

Provides structured approaches for designing:

- Prompts.
- System instructions.
- Guardrails.
- Knowledge bases.
- RAG workflows.
- AI assistants.
- AI workflows.

---

## Automation

Provides reusable patterns for designing and implementing automated processes.

Examples include:

- API integrations.
- ETL.
- File processing.
- Notifications.
- Scheduled processes.
- Data synchronization.
- AI-powered automation.

---

# Skill Design

Every Skill should define:

- Purpose.
- When to use.
- When not to use.
- Inputs.
- Outputs.
- Workflow.
- Rules.
- Constraints.
- Quality criteria.
- Validation.

Complex Skills may also include:

```text
references/
templates/
examples/
scripts/
```

---

# Composition

Skills should be composable.

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

The objective is to avoid large monolithic Skills that attempt to perform every responsibility.

---

# Contributing

When creating a new Skill:

1. Identify the specific capability.
2. Determine whether it really needs to be a Skill.
3. Define its responsibility.
4. Create the `SKILL.md`.
5. Define inputs and outputs.
6. Define the workflow.
7. Add quality criteria.
8. Add validation.
9. Add references or templates only when necessary.
10. Test the Skill with representative scenarios.

---

# License

This repository is intended to contain reusable AI Skills.

Individual Skills may define their own license in their frontmatter.