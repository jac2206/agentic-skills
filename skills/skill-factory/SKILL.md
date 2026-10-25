---
name: skill-factory
description: >
  Designs, creates, reviews, and improves reusable AI Skills following the
  repository's official Skill template and design principles. Use when the user
  asks to create a new Skill, improve an existing Skill, evaluate a Skill,
  combine Skills, or determine whether a problem should be solved with a Prompt,
  Skill, Workflow, Agent, or Application.
metadata:
  version: "1.0.0"
---

# Skill Factory

Design, create, evaluate, and improve reusable Skills for AI agents and systems.

This Skill is responsible for turning a concrete capability or problem into a
well-defined, reusable, maintainable, and composable Skill.

It must not simply generate prompts or fill templates mechanically.

## Purpose

Provide a structured process for designing high-quality AI Skills.

The Skill must:

- Understand the problem the user wants to solve.
- Determine whether a Skill is actually the appropriate solution.
- Define a clear and focused responsibility.
- Design the Skill according to the repository's official template.
- Make the Skill reusable across different contexts.
- Define inputs, outputs, workflow, rules, constraints, tools, and validation.
- Identify opportunities for composition with other Skills.
- Detect unnecessary complexity or duplicated responsibilities.
- Produce a complete `SKILL.md` ready to implement.

## When to use

Use this Skill when the user asks to:

- Create a new Skill.
- Design a Skill.
- Build a reusable AI capability.
- Turn a process into a Skill.
- Create a `SKILL.md`.
- Improve an existing Skill.
- Refactor a Skill.
- Evaluate a Skill.
- Review a Skill.
- Combine multiple Skills.
- Determine whether something should be a Prompt, Skill, Workflow, Agent, or Application.
- Define the architecture of a Skill.
- Validate whether a Skill follows the repository standard.

## When not to use

Do not use this Skill when the user only wants:

- A normal prompt.
- A one-time answer.
- A simple piece of text.
- A code implementation unrelated to Skill design.
- A presentation, document, application, or workflow itself.
- A modification to an existing Skill that does not require architectural or structural reasoning.

Do not create a Skill when a simpler solution is sufficient.

Prefer the simplest appropriate abstraction:

Prompt → Skill → Workflow → Agent → Application

## Core Principles

### 1. One clear responsibility

Every Skill must solve one clearly defined problem.

Do not create Skills that attempt to solve unrelated problems.

If the requested capability contains multiple independent responsibilities,
consider separating them into multiple Skills.

### 2. Reusability

A Skill should be useful across multiple projects, users, or contexts.

Avoid instructions that depend unnecessarily on:

- A specific project.
- A specific user.
- A single execution.
- Temporary context.
- Hardcoded implementation details.

Project-specific information should only be included when it is an intentional
constraint of the Skill.

### 3. Composability

Skills should be designed so they can work independently or as part of a
larger workflow.

Identify:

- Upstream Skills that may provide inputs.
- Downstream Skills that may consume outputs.

Avoid duplicating responsibilities that belong to other Skills.

### 4. Determinism

Instructions should reduce ambiguity whenever possible.

Prefer:

- Explicit inputs.
- Explicit outputs.
- Ordered workflows.
- Clear decision rules.
- Defined constraints.
- Verifiable quality criteria.

Avoid vague instructions such as:

- "Make it good."
- "Use your best judgment."
- "Be creative."

When judgment is necessary, define the criteria that should guide it.

### 5. Minimal sufficient complexity

Do not make a Skill more complex than necessary.

Only include:

- Rules that materially affect the result.
- Tools that provide real value.
- Inputs that are actually required.
- Validation that can meaningfully verify quality.

The goal is not to maximize the number of instructions.

The goal is to create the smallest reliable capability that solves the problem.

### 6. Quality must be verifiable

Every important Skill must define how its result can be evaluated.

Quality criteria should be observable and testable whenever possible.

## Inputs

The Skill Factory accepts the following types of input.

### Required

A description of the capability or problem the user wants to solve.

This may be provided as:

- A natural-language request.
- A rough idea.
- Existing instructions.
- An existing Skill.
- A process.
- Multiple Skills that need to be combined.

### Optional

The user may also provide:

- Existing `SKILL.md`.
- Templates.
- Examples.
- Technical constraints.
- Required tools.
- Expected output format.
- Existing Skills that should be reused.
- Domain-specific requirements.

## Outputs

Depending on the user's request, produce one of the following.

### New Skill

A complete `SKILL.md` following the repository's official template.

### Improved Skill

A revised complete `SKILL.md` preserving valid existing behavior while
improving clarity, structure, reuse, composition, and validation.

### Skill Evaluation

A structured analysis identifying:

- Problems.
- Ambiguities.
- Redundancies.
- Missing requirements.
- Contradictions.
- Risks.
- Opportunities for simplification.
- Opportunities for composition.

### Skill Composition

A proposed architecture showing:

- Shared responsibilities.
- Independent responsibilities.
- Dependencies.
- Inputs and outputs.
- Recommended Skill boundaries.

### Abstraction Recommendation

When appropriate, explicitly recommend one of:

- Prompt
- Skill
- Workflow
- Agent
- Application

instead of creating a Skill unnecessarily.

## Workflow

Execute the following process.

### Step 1 — Understand the problem

Identify:

- What the user wants to accomplish.
- Who or what will use the capability.
- What should be automated or standardized.
- What the expected result is.
- What constraints exist.

Do not start writing the Skill before understanding the capability.

### Step 2 — Determine the appropriate abstraction

Evaluate whether the problem requires:

Prompt → Skill → Workflow → Agent → Application

Use the simplest abstraction that solves the problem correctly.

A Skill should be created only when the capability is:

- Reusable.
- Structured.
- Meaningfully more complex than a simple prompt.
- Valuable as an independent capability.

### Step 3 — Define the responsibility

Write a single sentence describing what the Skill does.

Use the following test:

"This Skill is responsible for..."

If the sentence contains multiple unrelated responsibilities, reconsider the
Skill boundary.

### Step 4 — Define inputs and outputs

Identify:

- Required inputs.
- Optional inputs.
- Expected outputs.
- Output format.
- Important constraints.

Inputs and outputs should be explicit enough for another Skill or workflow to
consume them.

### Step 5 — Design the workflow

Define the minimum sequence of steps required to execute the capability.

Prefer a simple flow such as:

Input → Analyze → Transform → Validate → Output

Add decision points only when they are necessary.

### Step 6 — Define rules and constraints

Identify:

- Mandatory behavior.
- Forbidden behavior.
- Domain-specific rules.
- Technical limitations.
- Safety or quality requirements.

Do not add rules that do not materially affect the result.

### Step 7 — Identify tools

Determine whether external tools are required.

For each tool, define:

- Purpose.
- When it should be used.
- When it should not be used.

Do not introduce tools merely because they are available.

### Step 8 — Design composition

Determine whether the Skill should interact with other Skills.

Define:

### Upstream Skills

Skills that may provide inputs.

### Downstream Skills

Skills that may consume outputs.

If no meaningful composition exists, keep the section minimal.

### Step 9 — Define quality criteria

Create objective criteria for determining whether the Skill produced a valid
result.

Whenever possible, criteria should be testable.

### Step 10 — Create examples

Add examples that demonstrate the intended behavior.

Examples must clarify the Skill without becoming hidden instructions.

Keep instructions in the main Skill sections rather than inside examples.

### Step 11 — Generate the Skill

Create the complete `SKILL.md` using the repository's official template:

`skills/_templates/skill-template.md`

The generated Skill must preserve the template's frontmatter structure.

Use only the sections that are relevant to the Skill.

Do not add sections merely to satisfy the template.

### Step 12 — Validate the Skill

Before returning the result, verify:

- The Skill has one clear primary responsibility.
- The abstraction level is appropriate.
- Inputs are clearly defined.
- Outputs are clearly defined.
- Workflow is understandable.
- Rules are explicit.
- Constraints are meaningful.
- Tools are justified.
- Composition is clear.
- Quality criteria are verifiable.
- Examples represent the intended behavior.
- No unnecessary complexity was introduced.
- No responsibilities were duplicated unnecessarily.

## Rules

The Skill Factory must:

- Follow the repository's official Skill template.
- Prefer reusable capabilities over one-off instructions.
- Prefer simple abstractions over unnecessary architecture.
- Preserve valid behavior when improving an existing Skill.
- Separate instructions from examples.
- Keep Skills focused.
- Make important behavior explicit.
- Include validation for meaningful Skills.
- Identify composition opportunities when they provide value.

The Skill Factory must not:

- Create a Skill merely because the user asks for "a Skill" if a simpler abstraction is clearly sufficient.
- Create overly broad Skills.
- Duplicate existing Skill responsibilities unnecessarily.
- Add tools without a clear purpose.
- Add sections without a reason.
- Hide important instructions inside examples.
- Replace a reusable capability with project-specific instructions without justification.
- Optimize for Skill length instead of capability quality.

## Constraints

### Template constraint

All generated Skills must follow:

`skills/_templates/skill-template.md`

unless the user explicitly requests a different structure.

### Responsibility constraint

A Skill must have one clear primary responsibility.

### Reuse constraint

The design should not depend unnecessarily on a single project or execution.

### Validation constraint

A Skill should define how its output can be checked whenever meaningful
validation is possible.

### Maintenance constraint

Avoid unnecessary complexity that increases future maintenance.

## Tools

### Required

No specific external tool is required.

The Skill Factory can design Skills using the information provided by the user
and the repository conventions.

### Optional

Repository or file tools may be used when available to:

- Inspect existing Skills.
- Read the official template.
- Compare existing Skills.
- Detect duplicated responsibilities.
- Validate repository structure.

Use tools only when they provide useful information.

## Composition

### Upstream Skills

The Skill Factory may consume:

- Existing Skills.
- Skill templates.
- Domain-specific research Skills.
- Existing workflows.
- Existing documentation.

### Downstream Skills

The output of the Skill Factory may be consumed by:

- Repository implementation workflows.
- Code generation workflows.
- Documentation workflows.
- Testing and validation workflows.
- Human review processes.

The Skill Factory should not implement the generated Skill unless explicitly
requested.

## Quality Criteria

The result is valid when:

- [ ] The requested capability is clearly understood.
- [ ] The correct abstraction has been selected.
- [ ] The Skill has one clear primary responsibility.
- [ ] Required inputs are clearly defined.
- [ ] Expected outputs are clearly defined.
- [ ] The workflow is deterministic where possible.
- [ ] Rules and constraints are explicit.
- [ ] Tools are justified.
- [ ] Composition opportunities are identified when relevant.
- [ ] Quality criteria are verifiable.
- [ ] Examples demonstrate intended behavior.
- [ ] The official Skill template is followed.
- [ ] No unnecessary complexity was introduced.
- [ ] Responsibilities are not unnecessarily duplicated.

## Examples

### Example 1 — Creating a Skill

**Input**

Create a Skill that converts technical documentation into educational
workshops.

**Expected behavior**

The Skill Factory should:

1. Determine that the capability is reusable.
2. Define the Skill's responsibility.
3. Define inputs such as documentation, audience, and learning objectives.
4. Define outputs such as workshop structure and exercises.
5. Define the workflow.
6. Define quality criteria.
7. Generate a complete `SKILL.md`.

**Output**

A complete Skill following the official repository template.

### Example 2 — Not creating a Skill

**Input**

Give me a prompt to summarize a meeting.

**Expected behavior**

The Skill Factory should recognize that a reusable Skill may not be necessary.

**Output**

Recommend a Prompt instead of creating a Skill.

### Example 3 — Improving an existing Skill

**Input**

Improve this Skill. It has too many responsibilities and duplicates another
Skill.

**Expected behavior**

The Skill Factory should:

1. Identify duplicated responsibilities.
2. Separate unrelated responsibilities.
3. Recommend appropriate Skill boundaries.
4. Preserve useful existing behavior.
5. Produce the improved Skill or composition architecture.

### Example 4 — Combining Skills

**Input**

Combine these two Skills because both generate presentation content.

**Expected behavior**

The Skill Factory should determine:

- What responsibilities overlap.
- What responsibilities should remain independent.
- Whether one Skill should consume the output of the other.
- Whether combining them improves reuse or creates an overly broad Skill.

**Output**

A recommended composition or a consolidated Skill when appropriate.

## Validation

Before returning the result:

1. Verify that the requested problem is understood.
2. Verify that the correct abstraction was selected.
3. Verify that the Skill has one clear primary responsibility.
4. Verify that the Skill follows the official template.
5. Verify that inputs and outputs are explicit.
6. Verify that the workflow is coherent.
7. Verify that rules and constraints are necessary.
8. Verify that tools are justified.
9. Verify that composition is appropriate.
10. Verify that quality criteria are testable.
11. Verify that examples do not contain hidden instructions.
12. Verify that no unnecessary complexity or duplication was introduced.

---

> Use only the sections that are relevant to the Skill.
> Do not add sections merely to satisfy the template.
> Keep the Skill focused, reusable, composable, and maintainable.