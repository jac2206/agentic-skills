---
name: requirements-engineering
description: >
  Turn business needs and source requirements into a validated, traceable backlog
  of epics, features, and professional user stories with acceptance criteria,
  Gherkin scenarios, business rules, and functional and non-functional requirements.
metadata:
  version: "1.0.0"
---

# Requirements Engineering

Convert supplied business context into clear, verifiable, and traceable backlog
artifacts while exposing ambiguity and preserving decisions for the stakeholders
who own them.

## Purpose

Help product and delivery teams analyze business requirements and create a
structured Markdown backlog containing epics, features, and user stories.

## When to use

Use this Skill when the user asks to:

- Elicit, analyze, validate, or refine business or product requirements.
- Break requirements down into epics, features, and user stories.
- Write or improve acceptance criteria and testable Gherkin scenarios.
- Identify functional requirements, non-functional requirements, business rules,
  gaps, conflicts, assumptions, or dependencies.
- Save a traceable backlog as Markdown files.

## When not to use

Do not use this Skill to:

- Design or implement software, APIs, architecture, or test automation.
- Decide unresolved business policy on behalf of a stakeholder.
- Create a backlog from absent or insufficient source material by inventing
  product behavior.
- Replace a project-specific requirements standard when one is supplied.

## Inputs

### Required

- Business need, source requirements, or discovery notes sufficient to identify
  the intended outcome. Accept prose, documents, existing backlog items, or
  stakeholder-provided notes.

### Optional

- Product context, user roles, workflows, constraints, policies, terminology,
  existing identifiers, priorities, dependencies, and domain glossary.
- Required language, Markdown conventions, or an existing backlog location.

If context is incomplete, continue with the supported parts, record open
questions and assumptions, and do not present assumptions as confirmed policy.
Ask only when a missing decision prevents a useful and safe result.

## Outputs

Create Markdown files under `backlog/` in the project workspace, unless the user
specifies another location:

```text
backlog/
└── <epic-id>-<epic-name>/
    ├── epic.md
    └── features/
        └── <feature-id>-<feature-name>/
            ├── feature.md
            └── user-stories/
                └── <story-id>-<story-name>.md
```

- Nest each feature under its parent epic and each story under its parent
  feature. Create only levels supported by the source; do not create empty
  directories or placeholder parent items.
- Use stable supplied identifiers when available. Otherwise assign concise,
  unique identifiers and state that they are provisional.
- Write generated backlog content in the language requested by the user or used
  by the source material. Keep Skill instructions and templates in English.
- Each user-story file must include a story description, acceptance criteria in
  Given/When/Then form, and relevant business rules. Include functional and
  non-functional requirements when they are evidenced or explicitly requested.
- Include a validation summary of unresolved questions, inconsistencies,
  assumptions, dependencies, and traceability to source requirements. Do not
  silently omit unresolved items.

Use the linked templates in `templates/` as starting structures. Adapt or omit
sections that do not apply; never fill a section with invented content.

## Workflow

1. **Inspect sources.** Read the provided requirements and relevant project
   context. Identify goals, actors, workflows, constraints, terminology, and
   source references. Do not infer unstated behavior as fact.
2. **Analyze and validate.** Extract functional requirements, quality
   constraints, and business rules. Check for ambiguity, contradiction,
   duplication, missing actors or outcomes, unverifiable wording, dependencies,
   and scope boundaries. Record each issue with its source and the decision or
   clarification needed.
3. **Decompose and trace.** Group related outcomes into epics and features, then
   create independently deliverable user stories where the source supports
   them. Nest each child in its parent's directory and record the parent ID and
   source requirement in the child document where possible.
4. **Write story descriptions.** Use `As a <role>, I want <capability>, so that
   <benefit>` (or the natural equivalent in the output language). Make the role,
   capability, and user or business value specific. Keep implementation design
   out unless it is a stated constraint.
5. **Define acceptance criteria.** Write observable, testable Given/When/Then
   scenarios covering the normal outcome and relevant alternate, boundary, and
   failure cases. Use Gherkin keywords in the output language or project
   convention. Keep each scenario focused on one behavior.
6. **Produce Markdown files.** Create the supported epic, feature, and story
   files in the nested backlog structure. Include functional and
   non-functional requirements at the level where they are meaningful; refer
   to shared rules and constraints rather than duplicating them inconsistently.
7. **Validate the backlog.** Check completeness, hierarchy, traceability,
   terminology consistency, unique IDs, measurable acceptance criteria, and
   alignment with the source. Mark unresolved decisions visibly and summarize
   the files created and open items.

## Rules

The Skill must:

- Preserve the user's intent and distinguish source facts, assumptions,
  recommendations, and open questions.
- Make every story clear, specific, valuable, estimable, small enough for
  incremental delivery, and verifiable. If a story cannot yet meet these
  qualities, flag why and suggest the needed split or clarification.
- Ensure acceptance criteria describe outcomes and can be checked without
  guessing. Use concrete values and boundaries only when supported by evidence.
- Keep business rules explicit and traceable; do not bury policy in scenarios.
- Express functional requirements as system behaviors and non-functional
  requirements as measurable quality constraints whenever the source permits.
- Identify inconsistencies and gaps, explain their impact, and state the
  stakeholder question needed to resolve each material issue.
- Keep traceability from backlog items to supplied source references where
  available.
- Use the Markdown templates as adaptable structures, not mandatory content.

The Skill must not:

- Invent roles, benefits, permissions, thresholds, error handling, data rules,
  service levels, or business policies.
- Treat implementation tasks as user stories unless the user explicitly asks
  for technical tasks.
- Write vague criteria such as “works correctly” or “is user-friendly” without
  a defined observable outcome.
- Hide uncertainty by converting assumptions into acceptance criteria.
- Add unnecessary hierarchy or split one coherent outcome into artificial
  stories merely to fill backlog folders.

## Constraints

- Use plain Markdown; do not require a particular backlog product or runtime.
- The output language may differ from the language of this Skill.
- Do not overwrite existing backlog files with conflicting content. Inspect
  existing files first, preserve their identifiers and conventions, and update
  only when the user requests changes or the task clearly requires generation
  in that location.
- If requirements conflict, preserve both source statements and flag the
  conflict instead of choosing a winner without authority.

## Quality criteria

The backlog is ready for stakeholder review when:

- [ ] Every generated item is supported by input or clearly marked as a proposal.
- [ ] Each feature is stored under its epic and each story under its feature;
  parent IDs and relative links are consistent.
- [ ] Each story identifies a specific role, capability, and value.
- [ ] Stories are independent, negotiable, valuable, estimable, small, and
  testable, or explicitly flagged where they are not.
- [ ] Acceptance criteria use observable Given/When/Then scenarios and cover
  relevant alternate and failure paths.
- [ ] Relevant rules, functional requirements, and quality constraints are
  explicit and traceable.
- [ ] Ambiguities, contradictions, assumptions, and missing information are
  visible with actionable questions.
- [ ] Files are valid Markdown, have unique identifiers, and are saved in the
  requested backlog structure.

## Validation

Before returning the result:

1. Compare every story and criterion against its source; remove unsupported
   behavior or label it as an assumption or question.
2. Check that each criterion states a trigger and observable outcome and does not
   depend on unstated interpretation.
3. Check story quality (independent, negotiable, valuable, estimable, small,
   testable) and flag items that need stakeholder refinement.
4. Check that functional and non-functional requirements and business rules are
   categorized correctly and are not contradictory.
5. Check IDs, nested locations, parent references, relative links, source
   traceability, filenames, Markdown structure, and the output directory tree.
6. Report files created or updated, key unresolved questions, and any validation
   limitation. Do not claim checks that were not performed.

## References

- See [Epic template](templates/epic.md), [Feature template](templates/feature.md),
  and [User story template](templates/user-story.md) when creating backlog
  files.

## Examples

### Example: identify an unresolved rule

**Input:** “Customers can cancel an order before it ships. A cancellation fee
may apply.”

**Expected behavior:** Record the cancellation outcome as a supported need, but
flag fee applicability, amount, and calculation as unresolved. Do not invent a
fee policy or encode one in acceptance criteria.
