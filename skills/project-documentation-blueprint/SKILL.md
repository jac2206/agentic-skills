---
name: project-documentation-blueprint
description: >
  Analyzes a software project and transforms verified evidence into an executive,
  visual, and navigable Project Blueprint in HTML. Use when technical, managerial,
  or academic audiences need to understand a project's problem, solution,
  architecture, capabilities, user experience, technology, and evidence status.
metadata:
  version: "1.2.0"
---

# Project Documentation Blueprint

Transform an inspectable software project into a visual Project Blueprint: a
concise web narrative that explains what the project is, why it exists, how it
works, how it is built, and how much of it is supported by evidence.

The primary artifact is `project-blueprint.html`. It is a Blueprint web document,
not a README with decorative styling, a traditional technical report, or a slide
deck. The Skill also defines
the structured narrative, visual blocks, diagrams, and evidence labels that a
Presentation Skill may consume later.

## Purpose

This Skill owns the discovery, analysis, evidence validation, synthesis, visual
narrative, conceptual diagrams, Blueprint structure, and HTML generation for a
software project.

It must make a project understandable at three levels:

- **Executive** — purpose, value, scope, status, and important risks.
- **Technical** — behavior, architecture, stack, data, integrations, and decisions.
- **Academic or evaluative** — evidence, limitations, traceability, and explicit
  separation between observation and interpretation.

It does not own slide design, presentation layouts, presentation storytelling,
or PDF generation.

## When to use

Use this Skill when the user asks to:

- Create a visual Project Blueprint or Executive Technical Blueprint.
- Explain a software project to technical, managerial, or academic audiences.
- Turn a repository and its supporting evidence into a navigable HTML artifact.
- Create a visual overview of a project's problem, solution, architecture, stack,
  capabilities, UX, decisions, and current state.
- Prepare verified project content for later conversion into a presentation.

## When not to use

Do not use this Skill when:

- The requested output is only a README, API reference, or exhaustive code inventory.
- The user wants slides, a keynote, or a presentation as the primary artifact.
- The user wants a PDF or slide deck generated directly.
- The task defines a future architecture without an existing project to inspect.
- The task is implementation, testing, product strategy, or visual design unrelated
  to documenting an existing project.

## Core Principles

### 1. Evidence before interpretation

Inspect the project before writing the narrative. Use source code, configuration,
tests, assets, runtime observations, deployment definitions, and existing
documentation as evidence. A claim must be traceable to a source or labeled as
an interpretation, gap, or proposal.

### 2. Visual narrative over technical inventory

Organize the artifact around a sequence of questions:

1. What is this project?
2. What problem does it address?
3. What solution does it provide?
4. How does it work?
5. How is it built?
6. What can users do?
7. What is verified, incomplete, or still uncertain?

Use one main message per section and one main idea per visual block. Prefer
cards, diagrams, flows, short comparisons, indicators, screenshots, and concise
callouts over long paragraphs or exhaustive tables.

### 3. Explicit evidence status

Classify material as:

- **Documented** — stated in project documentation but not independently verified.
- **Verified** — confirmed by implementation, tests, or safe runtime observation.
- **Configured** — present in configuration or infrastructure but not proven active.
- **Inferred** — a clearly labeled interpretation supported by multiple observations.
- **Evidence missing** — relevant information could not be established.
- **Pending** — explicitly incomplete or awaiting implementation.
- **Proposed** — a recommendation or future possibility, never current behavior.

If the only source is Markdown, say so. Do not represent documentation claims as
runtime evidence.

### 4. Diagrams answer questions

Create a diagram only when it answers a concrete question and its nodes and
relationships are supported. A visually empty or unsupported diagram is worse
than an explicit evidence-gap block.

### 5. Composition without duplication

Produce content and a web Blueprint here. Let the Presentation Skill decide how
that content becomes slides, including slide layouts, density, transitions, and
PDF output.

### 6. Presentation-family visual language

The Blueprint must belong to the same visual family as the repository's dark
presentation examples. Use a dark navy or near-black foundation, electric blue
and cyan accents, restrained gradients, white primary text, muted gray secondary
text, semantic status colors, large type, dark cards, subtle borders, and glow
only where it improves hierarchy. Visual style supports the narrative; it must
not replace evidence.

## Inputs

### Required

- **Inspectable project**
  - Repository, project directory, or equivalent source package.
  - Must provide enough evidence to identify a purpose, behavior, or technical
    structure; otherwise report the evidence limitation.
- **Blueprint brief**
  - Audience, scope, language, and requested output location when provided.

### Optional

- README files, requirements, ADRs, changelogs, issues, API specifications, or
  existing technical documents.
  - Treat them as evidence with an appropriate status, not automatically as truth.
- Screenshots, recordings, design exports, or a safe running environment.
  - Use only when provenance and relation to the project are clear.
- Analysis produced by backend, frontend, UX, or repository-documentation Skills.
  - Reconcile important claims against current project evidence.
- Visual references such as `Expense_Tracker_Blueprint.pdf`.
  - Use only to understand communication level and narrative rhythm. Never copy
    its content, facts, or project-specific design.
- Repository presentation examples such as `presentation.html`,
  `clean-architecture.html`, `loyalty-react-native-executive.html`, and an
  existing Blueprint example when available.
  - Inspect them for reusable visual patterns such as dark themes, accent colors,
    large headlines, navigation, cards, flows, and diagram composition. Do not
    copy their content or turn this Skill into a slide-generation workflow.

## Outputs

The Skill should produce:

- **`project-blueprint.html`**
  - A modern, responsive, navigable, professional Blueprint web document.
  - Uses a dark presentation-family visual system: navy/near-black surfaces,
    electric blue and cyan accents, subtle gradients, high-contrast white text,
    muted secondary text, semantic status colors, dark cards, restrained borders,
    and generous spacing.
  - Uses a clear visual hierarchy, short content blocks, diagrams, flows,
    architecture, stack, capabilities, UX evidence, and status labels when supported.
  - Includes print-friendly CSS so it can be printed by a user, but does not export
    a PDF.
- **Structured Blueprint content inside the artifact**
  - Reusable section titles, key messages, visual-block descriptions, diagram
    definitions, source/status labels, and evidence gaps.
  - Must be understandable to a downstream Presentation Skill without reanalyzing
    the project.

Do not create a PDF, slide deck, presentation controls, or additional files as a
default result. Omit narrative sections that lack evidence or audience value.

The cover must primarily show, in this order:

1. `PROJECT BLUEPRINT` as the document identity.
2. The actual project name.
3. A concise project description.

Source information is secondary metadata. Never use a source label such as
`Blueprint ejecutivo técnico · fuente: Markdown proporcionado` as the main title,
eyebrow, or dominant cover message.

## Narrative Model

Select only the sections that contribute to the project's story. Use this model
as a flexible sequence, not a mandatory checklist:

1. **Cover** — project identity, short descriptor, audience, and evidence date.
2. **Executive summary** — what it is, why it matters, and current status.
3. **Problem to solution** — verified problem, affected users, and solution.
4. **Scope and users** — confirmed actors, boundaries, and exclusions.
5. **How it works** — the shortest important functional journey.
6. **Architecture** — components, boundaries, and verified relationships.
7. **Data and integrations** — data model, persistence, and external systems when evidenced.
8. **Technology stack** — technologies mapped to observed roles, not a dependency dump.
9. **Capabilities** — feature cards or a capability map with evidence status.
10. **User experience** — screens, states, actions, and screenshots when verified.
11. **Operation and delivery** — only confirmed runtime, deployment, or release facts.
12. **Decisions and challenges** — supported constraints, trade-offs, and technical risks.
13. **Evidence gaps and pending work** — limitations, unresolved claims, and explicit pending items.
14. **Conclusion** — concise restatement of value, maturity, and next evidence needed.

Prefer a strong short narrative over a complete but repetitive report. Combine or
remove sections when the project is small or the evidence does not support them.

## Workflow

Execute the following process:

### 1. Discover

- Read applicable repository instructions and establish the project boundary.
- Inspect the tree, entry points, package/build metadata, configuration, tests,
  assets, documentation, deployment files, and available UX evidence.
- Identify audience, language, scope, output location, and constraints.
- Create a source list before forming conclusions.

### 2. Analyze

Build an evidence inventory for applicable areas:

- purpose, domain, users, and terminology;
- entry points, user journeys, APIs, jobs, events, and runtime flows;
- frontend screens, routes, states, and user actions;
- modules, services, components, dependencies, and boundaries;
- persistence, entities, schemas, authentication, authorization, and integrations;
- technologies, versions, build/deployment configuration, and infrastructure;
- tests, screenshots, existing claims, limitations, and known changes.

Trace relationships through imports, calls, registrations, schemas, tests,
configuration, and execution paths. Do not infer architecture from filenames or
directory names alone.

### 3. Validate Evidence

Reconcile every candidate claim with its source. Mark it documented, verified,
configured, inferred, evidence missing, pending, or proposed. Detect conflicts
between code and documentation. Keep an evidence map for every architecture,
feature, flow, technology, metric, decision, and status claim used later.

### 4. Synthesize

Create a compact project model containing:

- problem, users, solution, and value;
- scope and key capabilities;
- most important functional and technical flows;
- architecture, data, integrations, and stack;
- UX evidence;
- decisions, constraints, challenges, risks, status, and evidence gaps.

Separate observed facts from interpretations. Remove details that do not help the
target audience understand the project.

### 5. Define Narrative

Choose the smallest complete sequence from the Narrative Model. For each section,
define:

- one audience question;
- one main message;
- up to a few supporting facts;
- one visual treatment;
- evidence/status labels and source references where needed.

Do not let a section become a technical report. If a detail cannot support the
main message, move it to evidence notes or omit it.

### 6. Define Visuals

Choose visuals according to the question they answer:

- **Architecture diagram** — what components exist and how verified boundaries connect.
- **Functional flow** — what happens from an entry point to a confirmed outcome.
- **User flow** — what a verified user does across screens or states.
- **Data model** — what confirmed entities or data stores relate to each other.
- **Integration map** — which confirmed external systems exchange what direction of data.
- **Stack map** — which technologies serve which observed responsibilities.
- **Capability cards** — what the project does and its evidence status.
- **Evidence panel** — what is documented, missing, pending, or proposed.

Use screenshots, icons, indicators, comparisons, and tables only when they make
the relationship clearer than short prose. Do not generate a diagram for styling.

### 7. Build Blueprint

Assemble the narrative as a web-document structure before writing detailed prose.
Give each section a stable anchor, a clear title, a short lead, and a consistent
visual block. Keep text scannable and preserve source/status information without
overloading the main story.

Use the default visual rhythm `Cover → Problem → Solution → Flow → Architecture
→ Data → Stack → Capabilities → Operation → Risks → Conclusion`, adapting or
omitting sections when evidence or audience value is absent. The result should
feel like a scrollable executive artifact with presentation-level composition,
not a collection of documentation chapters.

### 8. Generate HTML

Generate only `project-blueprint.html` unless the user explicitly changes the
output scope. The HTML should:

- provide visible section navigation and active section cues;
- use semantic headings and accessible landmarks;
- be responsive without losing the narrative hierarchy;
- use a dark visual system consistent with the presentation examples: near-black
  or navy background, electric blue/cyan accents, subtle radial or linear
  gradients, white headlines, muted gray support text, semantic status colors,
  dark cards, fine borders, and restrained glow;
- use large headlines, strong section numbering, generous whitespace, cards,
  badges, callouts, diagrams, captions, screenshots, and evidence labels;
- make architecture and important flows visual protagonists rather than prose
  summaries;
- use sticky or clearly persistent section navigation without implementing
  slide-only controls or one-slide-at-a-time behavior;
- prefer inline SVG or deterministic diagram markup when practical;
- keep assets self-contained when possible and disclose external dependencies;
- include print styles, sensible page breaks, readable contrast, and no clipped
  content, while remaining a scrollable web Blueprint rather than a slide deck;
- make key facts understandable without hover-only or interaction-only content.

Avoid white-paper defaults: do not make light paper backgrounds, dense tables,
long report paragraphs, or source metadata the dominant visual language. Use a
table only when it is clearer than cards, a flow, or another visual block.

### 9. Validate

Validate both the content and the artifact:

- compare every important claim and diagram relationship with the evidence map;
- check that the story answers what, why, how, with what, and how mature;
- inspect navigation, anchors, HTML structure, responsiveness, contrast, assets,
  overflow, diagram rendering, and print behavior when tools are available;
- verify that a downstream Presentation Skill can consume the sections, messages,
  visuals, and evidence labels without repeating project analysis.

## Rules

The Skill must:

- Inspect first and use the project as the primary factual authority.
- Make the narrative visual, concise, hierarchical, and audience-aware.
- Use the dark presentation-family language as the default HTML visual system.
- Make the cover immediately recognizable as `PROJECT BLUEPRINT`, followed by the
  actual project name and a short description.
- Make architecture, functional flows, and problem-to-solution relationships
  visually prominent whenever evidence supports them.
- Distinguish documented, verified, configured, inferred, missing, pending, and
  proposed information in both content and visual labels.
- Use actual component and technology names when they improve traceability.
- Create diagrams only from verified nodes, relationships, and flows.
- Include source or evidence references for claims that could be misunderstood.
- Omit empty or low-value sections instead of filling a template mechanically.
- Produce content that is directly reusable by the Presentation Skill.
- Validate factual correctness, narrative clarity, visual quality, and HTML behavior.

The Skill must not:

- Invent functionality, technologies, architecture, flows, decisions, metrics,
  integrations, users, screenshots, or production status.
- Treat a README, comment, filename, dependency, or configuration entry as proof
  of active behavior without corroboration.
- Turn every discovered file into a documentation section.
- Create a long technical report disguised as a Blueprint.
- Make `Markdown proporcionado`, source filenames, or evidence metadata the
  dominant title or cover message.
- Use a light README-like layout as the default when the dark visual system is
  available and appropriate.
- Generate slides, presentation controls, or PDF files.
- Copy content from `Expense_Tracker_Blueprint.pdf` or another visual reference.
- Modify application code, run destructive operations, or create auxiliary files.
- Present an inference or proposal as an implemented fact.

## Constraints

- The Skill is portable across project sizes, languages, frameworks, architectures,
  deployment models, and documentation conventions.
- Repository instructions and generated Skill documentation remain in English;
  the Blueprint language follows the user's request.
- The output is limited to `project-blueprint.html` unless explicitly requested otherwise.
- No fixed repository structure, framework, diagram syntax, or runtime environment
  may be assumed.
- If evidence is sparse, reduce scope and expose the limitation rather than guessing.
- The default visual theme is dark navy/near-black with blue/cyan accents; adapt
  only when accessibility, branding, or an explicit user constraint requires it.
- The Blueprint may include print CSS but must not perform PDF export.
- A presentation is a downstream transformation, not an automatic side effect.

## Tools

### Required

Use repository search and reading tools to inspect:

- implementation and entry points;
- package, build, and configuration files;
- tests, schemas, and deployment definitions;
- existing documentation;
- project screenshots and assets when available.

### Optional

- Browser or HTML renderer for responsive and visual inspection.
- SVG, Mermaid, or other deterministic diagram renderer for diagram validation.
- Static analysis, test inspection, or safe runtime observation to corroborate claims.
- Version-control diff tools to identify relevant project changes.

Do not run builds, migrations, servers, external services, or destructive commands
when they are not needed for evidence or output validation.

## Composition

### Upstream Skills

Optional upstream Skills may provide repository inventories, backend or frontend
documentation, UX evidence, or asset analysis. This Skill must reconcile important
claims with the current project before using them.

### Downstream Skills

- `html-presentations` / Presentation Skill consumes the verified Blueprint
  narrative, content blocks, diagrams, and evidence labels to create slides when
  explicitly requested.
- Documentation or HTML QA Skills may validate clarity, links, accessibility,
  rendering, and print behavior.

The boundaries are strict:

| Responsibility | This Skill | Presentation Skill |
| --- | --- | --- |
| Project discovery and evidence | Owns | Consumes result |
| Narrative and content model | Owns | Adapts for slides |
| Conceptual project diagrams | Owns | Recomposes as needed |
| Blueprint HTML | Owns | Does not replace |
| Slide layouts, density, transitions | Does not own | Owns |
| Presentation and PDF output | Does not own | Owns |

## Quality Criteria

The result is valid when:

- [ ] The Skill has one responsibility: evidence-based visual Blueprint generation.
- [ ] A reader can quickly identify the project, problem, solution, scope, and maturity.
- [ ] The narrative is visual and concise rather than a technical file inventory.
- [ ] The HTML uses the presentation-family dark theme with navy/near-black
      surfaces, blue/cyan accents, high-contrast type, subtle gradients, and dark cards.
- [ ] The cover leads with `PROJECT BLUEPRINT`, the actual project name, and a
      concise description; source metadata remains secondary.
- [ ] Problem and solution are explicitly distinguished.
- [ ] Architecture and important flows are represented visually and given visual
      prominence when evidence supports them.
- [ ] Technologies are mapped to observed responsibilities rather than listed without context.
- [ ] Capabilities and UX claims have evidence status and provenance.
- [ ] Evidence gaps, pending work, and proposals are visible and not conflated with facts.
- [ ] No diagram contains unsupported components or relationships.
- [ ] `project-blueprint.html` is navigable, responsive, accessible, and visually coherent.
- [ ] The HTML has usable print styles but does not generate a PDF or slide deck.
- [ ] The Blueprint content can be consumed by the Presentation Skill without reanalysis.
- [ ] The Skill remains reusable and does not depend on one project or reference document.

## Examples

### Example 1 — Evidence-rich application

**Input**

A repository contains a web client, API, database schema, tests, deployment
configuration, and verified screenshots.

**Expected behavior**

Create a short visual narrative from problem to solution, show the verified user
journey and architecture, map the stack to responsibilities, present capabilities
as status-labeled cards, and include screenshots with provenance. Generate only
`project-blueprint.html`.

### Example 2 — Documentation-only evidence

**Input**

A repository contains a README and partial source code, but no runtime evidence,
screenshots, or confirmed deployment.

**Expected behavior**

Use the README as documented evidence, verify what the source supports, label
unverified claims, omit unsupported diagrams, and include a visible evidence-gap
section. Do not imply that the system was executed or deployed.

### Example 3 — Presentation composition

**Input**

The user requests an executive presentation after the Blueprint is created.

**Expected behavior**

Pass the verified narrative, content blocks, diagrams, and evidence labels to the
Presentation Skill. Do not create slides or PDF output in this Skill.

## Validation

Before returning the result:

1. Verify that repository instructions, project scope, and available sources were inspected.
2. Verify that the evidence map supports every material problem, solution,
   capability, technology, architecture element, flow, integration, UX claim,
   decision, metric, and status label.
3. Verify that documented, verified, configured, inferred, missing, pending, and
   proposed material is visibly distinguished.
4. Verify that the selected sections form a coherent executive narrative and that
   no empty or repetitive sections remain.
5. Verify that every diagram answers a question and matches the evidence map.
6. Verify that the Blueprint looks and reads like a visual web artifact rather
   than a README or exhaustive technical report.
7. Verify the cover hierarchy: `PROJECT BLUEPRINT`, actual project name, and
   concise description; confirm that source metadata is secondary.
8. Verify the dark presentation-family visual language: dark background, blue/cyan
   accents, readable white text, muted secondary text, semantic statuses, cards,
   subtle borders, restrained gradients/glow, and sufficient whitespace.
9. Verify that architecture, flows, and problem-to-solution content are visual
   when evidence supports them and that text density remains low.
10. Verify `project-blueprint.html` navigation, anchors, semantic structure,
   responsive behavior, contrast, assets, overflow, and print behavior when tools
   are available.
11. Verify that the output contains no slides, presentation controls, PDF, invented
   content, copied reference content, or auxiliary files.
12. Verify that a Presentation Skill can consume the Blueprint content without
   repeating project discovery and evidence validation.

---

> Keep the Project Blueprint visual, evidence-based, concise, navigable, and
> composable. The Presentation Skill owns slides and PDF; this Skill owns the
> project story and its HTML Blueprint.
