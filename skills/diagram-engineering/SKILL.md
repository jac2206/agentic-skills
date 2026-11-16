---
name: diagram-engineering
description: >
  Selects, creates, modifies, improves and validates professional technical
  diagrams in Mermaid and editable Draw.io. Supports C4 context, containers and
  components, software components, layers, cloud infrastructure, deployment,
  integration, messaging, sequence, process, entity-relationship and data flow.
metadata:
  version: "2.3.0"
---

# Diagram Engineering

## Purpose

Turn evidence or a supplied conceptual model into clear, editable technical
diagrams, and improve existing diagrams without silently changing their meaning.
Own diagram selection, notation, layout, generation and validation only.

## When to use

- Create one or more of the thirteen supported diagram types.
- Repair syntax, update relationships, improve layout or iconography, or convert
  an existing diagram between Mermaid and native Draw.io.
- Recommend a small set of views for a question and let the requester select.
- Execute a bounded diagram handoff from an agent or workflow.

## When not to use

- Architecture decisions, technology selection or architectural evaluation:
  use `software-architecture-design` when available.
- A comprehensive architecture document: use `architecture-documentation`.
- General illustrations, UI mockups, dashboards, slide decks, or an HTML diagram
  application. This Skill produces Mermaid and Draw.io sources only.
- Implementing application code, infrastructure or a diagramming runtime.

## Inputs

Required: the objective and scoped source material: accessible project evidence,
a specification, an explicit model, or existing diagrams plus the requested change.

Optional: selected type IDs from the [catalog](references/diagram-catalog.md),
formats (`mermaid`, `drawio`, `both`), audience, language, output directory,
current/reported/proposed status, provider, visual reference, existing IDs,
renderer/editor version and capabilities, and allowed effects.

Read only the active workspace and explicitly supplied sources. For a material
gap, preserve an unknown or ask a focused question; do not invent technology,
cardinality, protocols, deployment placement or behavior. Explicit proposals are
valid inputs, but must remain visibly proposed. An icon is never deployment evidence.

## Outputs

- Only selected views and formats: `<view>.mmd` and/or `<view>.drawio`.
  Use established project locations, otherwise `docs/diagrams/`. Keep existing
  filenames during edits unless a rename is requested.
- A concise delivery record, in the response or an existing documentation file:
  selection, scope and status, source evidence and unknowns, icon inventory,
  checks with actual results and limitations, and artifact links. Do not create
  a full architecture document just to hold this record.
- When both formats are selected, equivalent representations of one model for
  each view; different selected views may have different abstraction levels.

The working model may be a small table in context; a separate model file is not
mandatory. Previews, when produced, supplement the editable sources.

## Workflow

Follow **Context → Analysis → Recommendation → Selection → Modeling → Generation
→ Validation → Delivery**. Skip recommendation and selection when supplied.

1. **Context.** Read applicable project instructions and supplied diagrams and
   visual references. Establish create, modify, improve, convert or validate mode,
   authorized effects, scope, audience and evidence status. In validate mode,
   report findings without rewriting files unless repairs are authorized.
2. **Analysis.** Identify the question each view must answer and the source of
   each material node, relationship and boundary. Inspect relevant code, schemas,
   API contracts or manifests only as needed. Inspect the closest bundled
   reference diagram and relevant provider reference for style and icon treatment.
3. **Recommendation.** If types are unspecified, recommend the smallest useful
   set with one reason per view. Present the categorized menu below, marking
   recommendations. Do not interpret a recommendation as the user's selection.
4. **Selection.** Let the requester select one or more types and `mermaid`,
   `drawio` or `both`, using available interactive controls or a textual reply.
   Wait for selection before generation. Ask only for fields still missing. If
   an existing file is being improved, infer its type and format from that file;
   do not ask again. An agent/workflow's explicit selection is sufficient.
5. **Modeling.** Read only the selected catalog entries. Build the common model
   described in [authoring and validation](references/authoring-and-validation.md).
   Agree on scope and abstraction, IDs, nodes, relationships, containment and
   view-specific semantics before formatting. Preserve existing IDs and meaning
   during edits; explain additions, removals and any unsupported conversion.
6. **Generation.** Generate each chosen format from that model, never by guessing
   semantics from another format's coordinates. Apply the icon policy below and
   the selected notation. Use the reused Draw.io resources for XML, provider
   icons and layout; apply this Skill's documented notation adaptations.
7. **Validation.** Apply the separate syntax, structure, semantics, icon/resource,
   equivalence and visual checks below. Resolve errors and inspect every warning.
   When a check is unavailable, record its limitation and perform remaining checks.
8. **Delivery.** Link the requested sources and report evidence, icon fallbacks,
   actual checks, unavailable checks and material changes. Identify missing
   requested files or failed mandatory checks as incomplete. No visual pass may
   be inferred from XML parsing or successful export.

### Selection menu

| Category | Selectable IDs |
| --- | --- |
| Architecture | 1 `c4-context`; 2 `c4-container`; 3 `c4-component`; 4 `software-components`; 5 `layers-dependencies` |
| Infrastructure and integrations | 6 `cloud-infrastructure`; 7 `deployment`; 8 `system-integration`; 9 `events-messaging` |
| Behavior and processes | 10 `sequence`; 11 `process-flow` |
| Data | 12 `entity-relationship`; 13 `data-flow` |

Text fallback: “Recommended: <IDs and reasons>. Select diagram IDs and formats:
Mermaid, Draw.io, or both.” Keep any already selected fields. Never generate all
thirteen by default. If only a format is missing, ask for that format alone.

## Rules

### Icons and visual language

- Every component needs an identifiable visual representation. In Draw.io, use
  a verified compatible icon whenever available. Use a truthful generic native
  symbol when no specific icon exists: actor, component, database cylinder,
  server, device, queue or entity/table notation as appropriate. Search the
  actual library before choosing a stencil; never guess a shape identifier.
- Follow the bundled references' discovery order for cloud services: installed provider
  library, extra-icon catalog when available, then the provider's official pack.
  Use an exact icon, then a truthful category icon, then a disclosed labeled
  generic symbol/service card when sources or resources cannot be verified.
  Distinguish “unavailable” from “not verified because access was blocked.”
- Keep vendor colors and proportions. Never invent an official logo or borrow a
  different technology's mark. Reuse verified generic pictograms or embedded
  assets from bundled reference diagrams when they fit; do not copy their topology.
- Use native editable Draw.io nodes, text, containers and connectors. Embed
  required SVGs as data URIs, with separate editable labels. An SVG is movable
  and scalable but its paths are not native editable diagram shapes. Do not
  flatten a view, insert a screenshot, or embed Mermaid as the Draw.io deliverable.
- In Mermaid, use icons only after verifying the target renderer, version and
  available icon pack/font with an actual render. Otherwise use typed labels,
  compatible shapes, grouping and styles. Do not require external CSS or adopt
  experimental syntax to force an icon. Semantic symbols in ER/sequence views
  take precedence over decorative pictograms.
- Use the bundled references' restrained palette, separate labels, tiered layout,
  whitespace and clear boundaries as the visual baseline. Match a supplied
  visual reference where compatible with the selected notation. Preserve
  architecture semantics even when formats need different visual devices.

### Semantic and editing rules

- Never invent components, services, relations, schemas, network boundaries or
  guarantees. Cite evidence or label supplied, inferred, proposed and unknown
  facts. Diagram repair does not authorize architecture redesign.
- Keep logical, runtime, deployment, behavior and data abstractions distinct.
  Use only boundaries appropriate to the selected view.
- If both formats are selected, reconcile the identity and meaning of every
  node, relationship, boundary and view-specific property against one model.
  Equal counts alone do not prove equivalence.
- Inspect every page when editing a multi-page Draw.io. Preserve unrelated pages,
  labels, metadata and user work. Do not discard unsupported constructs silently;
  narrow the conversion or report what cannot be represented.
- Retain readable labels, uniform spacing, hierarchy, alignment and directed
  relationships. Avoid crossings, text over connectors and decorative clutter.
  Plan connector routes and their labels together: use explicit ports, waypoints
  and label offsets or separate editable annotations where needed. Avoid placing
  captions over components, boundary titles or other captions; minimize shared
  connector segments and ambiguous crossings. Rerun checks after moving nodes.
  Wrap long Mermaid labels and choose a suitable direction to avoid an
  excessively wide view; assess readability at normal and fit-to-page scales.
  Split an overcrowded selected view into linked pages only when needed and
  preserve coverage; do not add unselected diagram types.
- For layout repair, preserve the existing diagram until a candidate has been
  checked. Compare the baseline and candidate by finding and location, not just
  warning counts or an optimization score. Reject new interior crossings,
  obscured labels, excessive bends or semantic changes even if a count falls.
  If rendered comparison is unavailable, do not claim visual improvement;
  report unresolved findings and retain the baseline for review.

## Constraints

- No application or deployment edits, publication, installation, new agents,
  executable workflows, repository CLI or automatic dependency downloads.
- Do not inherit `architecture-documentation`'s full-package generation, default
  proposed AWS target, document template or Archify invocation. They belong to
  its documentation responsibility. An unspecified provider remains unspecified.
- Keep this package's scripts, references and examples consistent. Their source
  and deliberate adaptations are recorded in `references/reuse-provenance.md`;
  changes here do not modify Architecture Documentation.
- Write artifacts in the requested language, otherwise the source language;
  instructions and technical filenames remain English.
- A missing parser/editor limits validation; it does not authorize claiming
  compatibility or replacing an editable deliverable with an image.

## Tools and bundled resources

This package is self-contained: installing `architecture-documentation` is not
required. Its proven diagram resources were incorporated from version `1.8.13`
and adapted here with the user's authorization. All paths below resolve relative
to this `SKILL.md`; no sibling installation or repository root is needed.

| Package-local resource | Use |
| --- | --- |
| `references/drawio-xml.md` | XML, layout, native objects, portable icons and boundaries for every Draw.io operation |
| `references/aws4-icons.md`, `references/azure-icons.md`, `references/google-cloud-icons.md`, `references/ibm-cloud-icons.md` | Read only for the matching provider: AWS, Azure, Google Cloud or IBM Cloud |
| `examples/reference-diagrams/component-diagram.mmd` and `component-diagram.drawio` | Logical notation and style reference |
| `examples/reference-diagrams/<provider>-infrastructure.drawio` | Bundled AWS, Azure and Google Cloud style/icon examples; Google uses `google-cloud-infrastructure.drawio`. No IBM example is claimed. |
| `scripts/check_drawio.py` | Local structural, component/icon/text collision and SVG checks; Python 3.10+, standard library only |
| `scripts/render_diagram.py` | Single-attempt render guard for Draw.io and Mermaid; Python 3.10+, standard library only |
| `scripts/render_drawio.py` | Reused Desktop export backend; invoke through the render guard only |

The Python scripts adapt the established mechanisms instead of replacing their
XML parser with a new dependency. All bundled utilities and tests use Python.
Neither
checker nor exporter designs architecture or generates a topology. Author XML
from the common model, run the checker, repair static collisions and recheck.
Use an already available Mermaid parser/CLI; do not install tools automatically.
The external Mermaid CLI requires its own installed Node.js runtime; Python
does not replace Mermaid's parser/renderer. Draw.io checking/export and the
attempt guard do not require Node.js.

### One attempt per renderer

Keep one render-attempt record for the entire task and pass it to every call to
`render_diagram.py`. Each file gets at most one attempt in each applicable
renderer. After a renderer fails, times out, cannot start or is interrupted,
stop using that renderer for the rest of the task, including other files.
Do not delete/change the record, switch executables or use the backend directly
to retry. Reuse a known failure from the current task without another launch.
The other renderer may have its own single attempt. Static checks and manual
source review can continue, but cannot establish a visual pass. A fresh attempt
after failure requires an explicit new user request.

## Composition

- `skill/software-architecture-design` may supply approved decisions and models;
  this Skill visualizes them and returns diagram findings, not architecture choices.
- `skill/architecture-documentation` owns its document and broader package; it may
  receive selected diagrams. It is an optional collaborator, not an installation
  dependency. This package owns its incorporated diagram resources independently.
- `backend-engineer`, `frontend-engineer`, and a future or external
  `software-architect` can supply objective, evidence/model, types, formats,
  destination, status and permissions; receive artifact paths, changes, unknowns,
  icon inventory and validation results. This does not create or register agents.
- A calling agent/workflow owns task ordering and acceptance. It should load
  `skill/diagram-engineering` and pass selections rather than copy this procedure.
  This task changes no existing agent definition or host integration.

## Quality criteria

- [ ] Only selected types and formats are delivered, in editable sources.
- [ ] Every material element traces to evidence or an explicit evidence status.
- [ ] Selected catalog conventions and abstraction boundaries are satisfied.
- [ ] Draw.io uses verified compatible icons or disclosed truthful fallbacks;
  the inventory identifies each symbol's source and verification status.
- [ ] Native grouping, readable labels and spacing make roles distinguishable;
  visual verification is reported only when a rendered view was inspected.
- [ ] Syntax, structure, semantics, resources, equivalence and visual results are
  reported separately, with failures and unavailable checks visible.
- [ ] Both selected formats preserve topology and type-specific semantics.
- [ ] Edits preserve unrelated content and identify meaningful semantic changes.

## Validation

1. Reconcile selection, output inventory, evidence and selected catalog rules.
2. Validate Mermaid with the actual target parser when available; otherwise
   perform a manual review and report syntax validation as not run. A textual
   checklist or regular expression is not a Mermaid parser.
3. Run the bundled `check_drawio.py` on every output. It preflights structure,
   parent references and geometry, then checks collisions and resources. Use
   provider-icon enforcement and SVG inventory for AWS, Azure, Google or IBM
   where applicable. Apply documented notation exceptions,
   never suppress errors or describe warnings as renderer verification.
4. Check icon provenance, embedded/existing resources and label mappings;
   provider markup alone cannot establish any of these.
5. Compare each selected view in both formats against the common model, including
   sequence order, ER cardinalities or data-flow labels where applicable.
6. When a safe renderer is available, render and inspect the view through
   `render_diagram.py`, using one task-wide attempt record. Use Draw.io Desktop
   only for requested visual review or when the exporter is confirmed working.
   Apply the one-attempt rule to both Draw.io and Mermaid; no retry after failure.
7. Report each check as `passed`, `failed`, `not run` or `not applicable`, with
   method and limitations. Follow the detailed gates in the authoring reference.

## References

- [Diagram catalog](references/diagram-catalog.md): selection, required inputs,
  notation and semantic rules for all thirteen supported types.
- [Authoring and validation](references/authoring-and-validation.md): common
  model, format compatibility, visual adaptations, commands and validation gates.
- [Draw.io XML](references/drawio-xml.md) and provider guidance:
  [AWS](references/aws4-icons.md), [Azure](references/azure-icons.md),
  [Google Cloud](references/google-cloud-icons.md), [IBM Cloud](references/ibm-cloud-icons.md).
- [Reuse provenance](references/reuse-provenance.md): incorporated resources,
  ownership, adaptations and maintenance boundaries.

## Examples

See the bilingual [usage guide](examples/usage.md) for direct and caller-supplied
invocations, guided selection and review criteria. These are instructional
scenarios, not proof of executed application diagrams.
