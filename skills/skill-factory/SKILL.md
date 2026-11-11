---
name: skill-factory
description: >
  Designs, creates, reviews, and improves reusable AI Skills. Use when a user
  wants to create or revise a Skill, assess its quality, compose Skill
  responsibilities, or choose between a prompt, Skill, workflow, agent, or
  application.
metadata:
  version: "1.1.2"
---

# Skill Factory

Help users turn a repeatable capability into a focused, reusable, maintainable
Skill, or assess and improve Skills they already have. Preserve the Skill's
valid purpose and behavior when revising it.

## Purpose

Choose the simplest abstraction that reliably solves the user's problem:

**Prompt → Skill → Workflow → Agent → Application**

Design Skills that are clear, composable, and testable. Do not create a Skill
just because the user used the word “Skill”; determine whether a reusable
capability is actually useful.

## When to use

Use this Skill when the user asks to:

- Create or design a Skill or `SKILL.md`.
- Turn a repeatable process into a reusable capability.
- Review, evaluate, refactor, or improve an existing Skill.
- Decide how multiple Skills should be divided or composed.
- Decide whether a problem calls for a prompt, Skill, workflow, agent, or application.
- Check a Skill against repository conventions.

## When not to use

Do not use this Skill for a one-time prompt or answer, ordinary content or code
work, or implementing a capability whose Skill design is already settled.
Use the smallest abstraction that fits the task.

## Inputs

Use the information available in the request and repository. Relevant inputs
may include:

- The problem, intended users, and expected outcome.
- Existing `SKILL.md` files and their supporting resources.
- Constraints, tools, target platforms, and repository conventions.
- Existing Skills that may overlap or provide inputs.

Ask a concise question only when a missing decision materially affects the
design and cannot be reasonably inferred. Otherwise, state a reasonable
assumption and proceed.

## Outputs

Match the deliverable to the request:

- **New Skill:** a complete `SKILL.md` and only the supporting resources that
  have a clear purpose.
- **Improved Skill:** an updated Skill that preserves its core responsibility
  and valid behavior, with relevant supporting resources kept consistent.
- **Evaluation:** findings, severity or impact, and actionable recommendations.
  Do not rewrite files unless the user asked for changes.
- **Composition design:** responsibility boundaries, dependencies, and the
  proposed flow of inputs and outputs. Implement only when requested.
- **Abstraction recommendation:** a reasoned choice among prompt, Skill,
  workflow, agent, and application.

## Core principles

### One primary responsibility

Describe the Skill's job in one sentence. Split independent capabilities when
combining them would make the Skill harder to discover, use, or maintain.

### Reuse and composition

Make the capability useful across projects where practical. Identify upstream
inputs and downstream consumers only when that relationship is real. Do not
duplicate another Skill's responsibility; define a handoff when composition
works better.

### Clear, operational instructions

Define when to use and avoid the Skill, its inputs and outputs, its workflow,
important rules and constraints, and how to judge the result. Make decisions
explicit where ambiguity would change the outcome. Leave routine judgment to
the agent when rigid rules add no value.

### Smallest sufficient design

Include only instructions and resources that improve decisions, consistency,
or reliability. Prefer deterministic procedures for repeatable operations and
use judgment for contextual work.

## Workflow

### 1. Select the requested mode

Identify whether the user wants creation, revision, evaluation, composition,
or an abstraction recommendation. Follow only the applicable path below.

### 2. Understand the capability and inspect evidence

Identify the user's goal, intended user, expected result, constraints, and
available inputs. For repository work, inspect the relevant Skill, its
references, templates, examples, scripts, and existing conventions before
proposing changes. Do not infer behavior that the source material does not
support.

### 3. Choose the simplest abstraction

Use a prompt for a one-off instruction; a Skill for a reusable capability
with stable guidance; a workflow for a coordinated sequence; an agent when
independent delegated work is needed; and an application when a persistent
user-facing product is required. These are decision aids, not mandatory
architecture layers.

If a Skill is appropriate, define its one-sentence responsibility and check
for overlap with existing Skills.

### 4. Define the contract

Specify only relevant items:

- Required and optional inputs, including useful defaults.
- Expected outputs and their format.
- The minimum workflow and meaningful decision points.
- Rules, constraints, tools, and composition relationships that affect results.
- Observable quality criteria and proportionate validation.

### 5. Decide which supporting resources add value

Start with `SKILL.md`. Add a resource only when it solves a concrete need that
would otherwise cause repeated work, excessive context, ambiguity, or errors.
Keep all Skill-specific resources inside that Skill's directory.

| Resource | Add it when | Do not add it when |
| --- | --- | --- |
| `references/` | Detailed domain guidance, policies, schemas, or mode-specific procedures are needed only for some tasks. Link each reference and say when to read it. | The material is short, generic, already available from an authoritative source, or repeats the main instructions. |
| `templates/` | The Skill repeatedly produces a structured artifact and a reusable starting format improves consistency. Explain when and how to fill it. | A few instructions in `SKILL.md` are enough, or the template would be used once. |
| `examples/` | A concrete example resolves ambiguity or teaches a non-obvious behavior. Keep examples illustrative, not hidden rules. | Examples merely restate instructions or exist to populate a directory. |
| `scripts/` | Repeated deterministic work can be automated and automation materially improves correctness, speed, or repeatability. Document invocation, inputs, outputs, dependencies, and failure behavior. | The task depends on contextual judgment, is infrequent, or a script would add more maintenance than value. |

For scripts, prefer the existing project runtime and dependencies when they
fit. Otherwise, choose based on the target environment: Python is a practical
portable choice for file, data, and validation utilities; Node.js fits
JavaScript/TypeScript projects and their tooling; PowerShell fits Windows
administration; and POSIX shell fits simple Unix command pipelines. These are
defaults, not requirements. Avoid adding dependencies without a clear benefit.
Make script behavior deterministic where possible and validate new or changed
scripts when they are part of the requested work.

Distinguish instructional examples inside a Skill from concrete artifacts
generated by using it. Follow repository conventions for their locations;
here, Skill examples belong in `skills/<skill-name>/examples/`, while generated
demonstration artifacts belong in the appropriate `examples/<category>/`.

### 6. Create, revise, or report

- **Create:** use `skills/templates/skill-template.md` as the repository
  starting point. Preserve its frontmatter fields and include only sections
  relevant to the capability. In this repository, use separate `Quality criteria`
  and `Validation` sections: express applicable outcomes as a checklist and
  explain how to check them. Keep checks proportional to the Skill's scope.
- **Revise:** preserve the name, primary responsibility, and valid behavior
  unless the user requests a scope change. Resolve contradictions, remove
  duplication, improve clarity, and update any affected supporting resources.
  Check the repository's separate quality checklist and validation sections.
- **Evaluate:** report evidence-based findings and practical fixes. Do not
  silently change the Skill. Use the evaluation rubric below when a quality
  assessment is requested; give a numeric score only when the user asks for it.
- **Compose:** recommend boundaries and handoffs; consolidate only when that
  produces a more focused, reusable capability.
- **Recommend an abstraction:** explain the choice briefly and provide the
  requested prompt or design only if asked.

Do not implement the capability described by a new Skill unless the user also
requests its implementation.

### Evaluation rubric

Assess (1) responsibility and activation, (2) inputs, outputs and workflow,
(3) constraints and composition, (4) observable validation and supporting
resources, and (5) observed behavior on representative tasks. Cite concrete
paths or results for material findings. Separate instructions inspected,
outputs observed, checks executed, and unavailable evidence; generated outputs
alone do not establish which Skill or version produced them. State confidence
and limitations, prioritize actionable improvements, and do not assume missing
runtime evidence is a failure of the instructions.

If the user asks for a 1–5 rating, explain it as a judgment, not a computed
measurement: 1 = unusable or contradictory; 2 = major gaps; 3 = usable with
important gaps; 4 = strong with specific improvements; 5 = strong and supported
by representative execution evidence. Use intermediate scores when helpful.
Do not award 5 from instruction inspection alone. Keep per-dimension observations
visible when they differ substantially; never invent executed tests.

### 7. Validate and present

Validate against the relevant criteria below. Report what changed or what you
found, any important limitation, and checks performed. Do not claim a script,
Skill, or workflow was tested unless it was actually exercised.

## Rules

The Skill Factory must:

- Preserve user intent and the established scope.
- Prefer the smallest reliable abstraction and resource set.
- Keep instructions in `SKILL.md` and supporting detail in a linked resource
  only when progressive disclosure helps.
- Preserve valid behavior during revisions and check related resources for
  consistency.
- Distinguish requirements from recommendations and repository conventions.
- Make recommendations specific and actionable.

## Constraints

The Skill Factory must not:

- Generate or rewrite files for an evaluation-only request.
- Create resources or sections merely to fill a template.
- Add tools, dependencies, scripts, or rigid steps without a concrete benefit.
- Hide mandatory behavior in examples or duplicate guidance across files.
- Expand a Skill into unrelated responsibilities.

## Tools

No specific tool is required. Use repository and file tools when inspecting
existing Skills, templates, supporting resources, or conventions will improve
accuracy. Use external tools only when the requested design depends on
information unavailable in the provided context or repository.

## Composition

The Skill Factory may use existing Skills, templates, workflows, or domain
documentation as inputs. Its outputs may feed implementation, documentation,
validation, or human review workflows. Name specific upstream or downstream
Skills only when the repository contains a meaningful relationship.

## Quality criteria

A created or revised Skill is ready when:

- [ ] Its purpose and primary responsibility are clear and focused.
- [ ] Its abstraction fits a repeatable user need.
- [ ] Use cases, inputs, outputs, and workflow are understandable.
- [ ] Rules and constraints affect the result and do not conflict.
- [ ] Tools, composition, and supporting resources are justified or omitted.
- [ ] Any references are linked and read conditionally where appropriate.
- [ ] Any scripts document how to run them and have meaningful validation.
- [ ] Examples clarify behavior without acting as hidden instructions.
- [ ] Quality criteria and validation match the capability's complexity.
- [ ] Repository Skills have separate quality and validation sections; quality
      criteria are a checklist and validation explains proportionate checks.
- [ ] The official repository template and naming conventions are followed.
- [ ] Existing behavior and related resources remain consistent after revision.

An evaluation is complete when each finding is supported by the Skill or its
resources and recommendations are prioritized by practical impact. A
composition design is complete when responsibilities and handoffs are clear.

## Examples

### One-off request

**Input:** “Give me a prompt to summarize one meeting.”

**Expected behavior:** Recommend a prompt; do not create a Skill unless the
user's broader need shows a repeatable capability.

### Repeated deterministic work

**Input:** “Create a Skill that validates the same structured files every day.”

**Expected behavior:** Define the Skill's decision rules and outputs, then
consider a small script if deterministic checks will reduce repeated effort
or errors. Pick a language that fits the target runtime, document how to run
it, and validate its behavior. Do not add a script if the checks are simple
enough to state and perform reliably without one.

### Evaluation request

**Input:** “Review this Skill and tell me what should improve.”

**Expected behavior:** Inspect its instructions and relevant resources, report
evidence-based findings and recommendations, and leave files unchanged unless
the user asks for edits.

### Evaluation with limited runtime evidence

**Input:** Clear instructions and an example exist, but the execution history
and Skill version are unknown.

**Expected behavior:** Assess the instructions and observed artifact separately,
label attribution and runtime reliability unknown, state lower confidence, and
recommend a representative execution before a top score.

### Evaluation with an observed contradiction

**Input:** A documented output conflicts with a current workflow rule, while
the current generator already contains a guard.

**Expected behavior:** Cite both artifacts and propose a regression scenario;
do not attribute the old result to the current generator without evidence.

## Validation

For each task, apply only the relevant checks:

1. Confirm the deliverable matches the requested mode; do not turn a review
   into an unrequested rewrite.
2. For creation or revision, confirm the Skill has a focused responsibility,
   explicit contract, coherent workflow, and no conflicting instructions.
3. Confirm the abstraction and each optional resource are justified by the
   user's need; check resource paths and links.
4. Confirm scripts have documented usage and were exercised when their
   behavior is part of the requested deliverable.
5. Confirm examples teach rather than silently impose behavior.
6. Confirm the repository template, naming, and location conventions are
   followed.
7. Confirm revisions preserve intended behavior and keep related resources
   consistent.
8. State which checks were performed and distinguish inspection from execution.

---

Use only the sections and resources that serve the Skill's actual purpose.
