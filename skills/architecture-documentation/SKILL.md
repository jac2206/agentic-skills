---
name: architecture-documentation
description: >
  Creates evidence-based application architecture documentation with a domain-
  grounded document, a logical component diagram in Mermaid, a distinct cloud
  deployment diagram in editable Draw.io XML, and an Archify diagram when
  Archify is installed.
metadata:
  version: "1.1.0"
---

# Architecture Documentation

Create a traceable architecture package from the application's repositories and user-supplied requirements. Explain the product and its business capabilities from project evidence, then produce distinct logical and deployment views: Mermaid and editable Draw.io component diagrams, plus a provider-specific Draw.io infrastructure diagram. At generation time, check whether the Archify Skill is installed: if installed, its documented workflow and HTML delivery are required; if absent, create no Archify artifacts.

## Purpose

Explain an application's components, relationships, deployment topology, data and integration paths, security boundaries, and operational concerns without presenting unknown or proposed facts as implemented behavior.

## When to use

Use this Skill when the user asks to create or update comprehensive application architecture documentation, especially with component, cloud infrastructure, Mermaid, Draw.io, or Archify diagrams.

## When not to use

Do not use this Skill for:

- A single implementation use-case flow or backend behavior document; use `backend-documentation` when that Skill is available.
- A future architecture proposal without a project or requirements source, unless the user asks for a proposal. Label all such content as proposed.
- A diagram-only request that does not need an architecture document; use the smallest requested deliverable.

## Inputs

### Required

- One or more project repositories/source trees, an architecture specification, or a user-supplied diagram that provides evidence for the requested system. For multi-repository systems, use each repository identified or linked by the user.
- The requested scope and output language, inferred from the user's request or source material.

### Optional

- Target cloud provider (`AWS`, `Google Cloud`, `Azure`, or another provider), audience, deployment environment, architecture style, and output directory. If a provider-specific cloud design is requested without a target selection, default to AWS and mark it as proposed.
- Existing diagrams, ADRs, API specifications, infrastructure-as-code, deployment manifests, and architecture documents.
- Backend documentation created by `backend-documentation`.

If no application implementation or specification is available, document only what the supplied material establishes. Identify evidence gaps and label any target-state design as proposed. A host named as part of the current stack (for example, Vercel, Railway, or Supabase) is evidence about that deployment, not an implicit selection of AWS, Google Cloud, or Azure as the target cloud. Keep those views distinct when the requested/default target differs from current hosts.

## Outputs

Create the requested artifacts together under the project's established documentation location. If none exists, use `docs/architecture/`:

For a complete architecture package, provide the component diagram in both editable Draw.io and Mermaid formats, plus a separate Draw.io cloud deployment diagram. Do not count either component format as a substitute for the infrastructure view.

- `component-diagram.drawio` — editable Draw.io version of the logical component view in `component-diagram.mmd`.
- `component-diagram.mmd` — Mermaid version of the same logical component view.
- `infrastructure.drawio` — provider-specific cloud deployment view, separate from the component diagrams.
- `current-deployment.drawio` — optional, only when the current hosting topology is in scope and differs from the selected/default target-cloud proposal.
- `architecture.md` — scope, system context, components, interactions, data and events, cloud topology, security, availability/operations, evidence status, decisions, and gaps. Omit sections that do not apply.
- `<system-name>.archify.json` and `<system-name>.archify.html` — required when Archify is installed. Generate and deliver them by following the installed Archify Skill's authoring, validation, and finalization workflow; keep the candidate JSON for reproducibility. If Archify is absent, omit both files and any Archify-specific directory. If the installed workflow fails, report the failed step and do not claim or link an artifact that was not produced.

Adapt filenames and location to existing project conventions. Do not place generated artifacts in the repository root.

## Workflow

### Product and view separation gates

Before following the numbered workflow:

- For a system spanning repositories, inspect each repository the user identifies. Read applicable agent instructions, product context/specs, README, and architecture notes, then corroborate domain claims against routes, screens, service calls, domain logic, or deployment configuration. A generic or stale README must not define the architecture by itself.
- The architecture document must open with the actual product purpose, actors, and core business capabilities when evidence exists. A technology inventory or paraphrase of the user's prompt does not satisfy the product overview.
- Keep the Mermaid component view logical: software responsibilities, domain capabilities, and their calls/data relationships. Keep cloud services, VPCs, subnets, load balancers, and placement in the Draw.io deployment view.
- The Draw.io must show provider services and where runtimes/data are deployed, using available native AWS/GCP/Azure icon shapes with readable labels. Do not use a generic copy of the component boxes as the infrastructure diagram.
- Save XML only in `.drawio` files. Markdown documents link to artifacts; never append raw or escaped XML to a README or link list.

1. **Establish scope.** Read applicable `AGENTS.md` files, product context/specs, READMEs, existing architecture documentation, source/configuration/deployment evidence, and user-provided diagrams. For multi-repository systems, inspect each repository named by the user. Determine product purpose, actors, business capabilities, which repository owns each component, and whether each view is current-state, proposed target-state, reported, or mixed. Corroborate README claims with implementation or specs; record generic/stale/conflicting README content instead of copying it as product truth.
2. **Build an evidence map.** Trace components and relationships through imports, calls, API routes, infrastructure definitions, configurations, schemas, and supplied diagrams. Classify each material claim as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Keep repository-relative evidence paths for product purpose and key capabilities as well as technical components. A resource name, README claim, dependency, or icon alone does not prove active deployment or runtime behavior.
3. **Select a cloud target.** Honor an explicit target-cloud choice. If the user requests a provider-specific cloud design but does not select AWS, Google Cloud, or Azure, default to AWS and label it proposed. A current host such as Vercel, Railway, or Supabase describes the reported/current deployment; it does not silently replace the target-cloud choice. When current deployment is in scope and differs from the selected/default target, show it in a separate, clearly labeled current-deployment diagram. Mark unverified user-reported placement as reported, not deployed/configured.
4. **Write the architecture document.** Use the bundled template as a starting structure when the project has no local template. Begin with the product purpose and actual domain capabilities, then explain components, request/data/event paths, persistence, deployment, security, availability, and operations only as supported. Cite evidence in the document and distinguish facts from user-reported details and proposals. Do not overwrite the general project README. If `docs/architecture/README.md` is the established architecture document, update it in place with evidence-based content and valid links. Record unresolved decisions and evidence gaps.
5. **Create the component diagram.** Create both `component-diagram.mmd` and editable `component-diagram.drawio` from the same logical model. Use domain-meaningful names, group software components by real system boundary, label important calls/actions and async paths, and preserve evidence-backed relationships. Do not draw network/cloud placement as part of this logical view. Cross-check the two formats for the same components and relationships.
6. **Create the cloud infrastructure diagram.** Write an editable Draw.io `.drawio` XML deployment view, distinct from Mermaid. Show clients, selected-provider services, runtime/compute, data services, ingress, and only evidenced or explicitly proposed network/security boundaries. Use native provider icon shapes where available and readable service labels. Keep application modules inside the actual compute boundary unless separate deployments are evidenced. Label the view CURRENT, REPORTED, or PROPOSED; keep inferred services visibly proposed. Keep node IDs unique and all edge references valid. Consult `references/drawio-xml.md`.
7. **Detect and use Archify.** Before writing an Archify candidate or output, inspect the active Skill catalog and installed Skill locations available to the agent for `archify/SKILL.md`. Treat Archify as installed when it appears in the active catalog or its Skill file is available in an installed location. If found, read the Skill and follow its repository-evidence guidance, authoring, validation, and finalization workflow. Generating and delivering the candidate JSON and standalone HTML is mandatory; do not skip it for convenience. If Archify is absent from both the catalog and available installed locations, do not create Archify JSON, HTML, or Archify-specific directories; continue with the other artifacts and state that Archify was unavailable. If the installed workflow fails, report the failing step and retain/link only artifacts that were actually produced. If HTML was delivered but a later browser gate fails, retain it and the candidate, report the failed gate, and do not claim full validation or visual review.
8. **Cross-check the diagrams.** Compare Mermaid, Draw.io, Archify (when generated), and prose against the same evidence map. Their supported components and relationships must agree; any difference must be an explicitly different abstraction or a documented scope limitation.
9. **Validate and report.** Parse both component and infrastructure `.drawio` files as XML; check unique cell IDs and valid source/target references. Check Mermaid structure and compare the Mermaid/Draw.io component nodes and relationships. Run Archify's documented validation/delivery workflow when applicable. Verify local links, output locations, and that the final status matches the evidence. Report what was generated, checks performed, assumptions, and remaining gaps.

## Rules

The Skill must:

- Keep implemented/current-state facts separate from inferred or proposed target-state design.
- Trace every component and relationship to source evidence or explicitly label it as proposed/unknown.
- Preserve the user's requested scope, cloud provider, language, and diagram formats.
- Represent trust, network, runtime, and data-ownership boundaries only when evidence supports them; label proposal boundaries as proposed.
- Keep Mermaid, Draw.io, Archify, and written descriptions synchronized. When Archify is installed, execute its complete generation and delivery workflow as a required output step.
- Use service names appropriate to the chosen provider and keep product/API names in their original form.
- Derive the product/domain summary from repository context and corroborate it with implementation or specifications; do not produce a technology-only summary when product evidence exists.
- For a multi-repository solution, identify which repository supports each product, client, backend, and deployment claim.
- Make the component and deployment diagrams answer different questions; use provider-specific service icons in Draw.io when available.
- Provide the component view in both Mermaid and editable Draw.io when creating a complete architecture package.
- Keep `.drawio` XML in its own `.drawio` file. Never paste raw or escaped XML into Markdown, a README, or a link list.
- Reuse established project documentation location, naming, and style when available.

The Skill must not:

- Invent services, routes, protocols, regions, networking, data stores, security controls, availability, compliance, or production status.
- Treat a diagram icon, README claim, directory name, dependency, or infrastructure template as proof that a component is deployed or active.
- Do not create Archify artifacts when the Archify Skill is absent, and do not silently skip its generation workflow when installed. Report execution failures accurately.
- Present an illustrative cloud topology as a verified deployment.
- Replace detailed backend use-case tracing owned by `backend-documentation`.
- Add empty directories, diagrams without a reader question, or unrelated design recommendations.

## Constraints

- Repository instructions, this Skill, its template, and references are written in English; generated architecture artifacts follow the user's requested language or source language.
- Draw.io output must be `.drawio` XML that imports as an editable diagram, not a screenshot or flattened image.
- If evidence is sparse, reduce the claimed scope and make gaps explicit rather than filling them with common patterns.
- Do not modify application source code or deployment configuration as part of documentation generation.
- An Archify browser or delivery failure is a validation limitation, not permission to claim success or fabricate an Archify output.

## Composition

- `backend-documentation` may provide verified backend structure, integrations, and use-case flows as evidence; this Skill owns the overall architecture package and its component/deployment diagrams.
- `archify` adds a required HTML architecture artifact whenever its Skill is installed. When absent, this Skill omits Archify artifacts. Archify does not replace evidence collection or the written architecture and Draw.io outputs.

## Quality criteria

- The document opening identifies the real product purpose and core capabilities from repository context/specs and implementation evidence; a stack-only summary or prompt paraphrase fails.
- The document states scope, evidence status, and whether the architecture is current or proposed.
- Every material component and relationship has evidence or an explicit proposal/unknown label.
- Mermaid is a logical software-component view; Draw.io is a provider-specific deployment view with runtime placement, cloud services, and applicable boundaries. The views are visibly distinct and consistent with the document.
- The Mermaid component diagram and Draw.io component diagram describe the same logical topology; the infrastructure Draw.io is a separate deployment topology.
- Draw.io uses readable provider-specific service icons where available and does not invent services to make the diagram look complete.
- Current/provider-reported deployment and target-cloud proposal are clearly distinguished; proposals are never represented as deployed.
- Markdown links to standalone artifacts and contains no inline XML dump.
- The Draw.io XML is parseable; cell IDs are unique; every edge endpoint resolves to a cell.
- Cloud provider and service choices follow user input or documented evidence; assumptions are visible.
- Security, persistence, availability, and operations claims are calibrated to the evidence.
- Archify installation is checked. When installed, the Skill's generation and HTML delivery workflow is run, and its candidate, output, and validation gates are reported accurately; when absent, no Archify files or directories are created.
- Files follow project conventions and links resolve.

## Validation

1. Reconcile the architecture document and each diagram with the evidence map.
2. Parse both Draw.io XML files and check IDs, vertex/edge references, and labels.
3. Confirm Mermaid is a logical view and Draw.io is a deployment view; reject Draw.io that only repeats generic application-component boxes.
4. Confirm product purpose/capabilities against repository context/specs and code, and ensure the opening describes this application rather than echoing the prompt.
5. Confirm Mermaid components and relationships agree with the documented logical architecture and that the cloud view agrees with deployment evidence/proposal labels.
6. Check the active Skill catalog and installed locations for Archify. When installed, run its complete authoring, validation, and HTML delivery workflow; distinguish structural checks, browser checks, and visual inspection. When absent, verify there are no Archify artifacts or directories.
7. Verify links, output locations, generated file inventory, and that XML exists only in `.drawio` files.
8. Report any unresolved evidence gaps or validation failures.

## References

- [Architecture document template](templates/architecture-document.md) — use when the project has no established architecture-document template.
- [Draw.io XML authoring and validation](references/drawio-xml.md) — consult when creating or repairing `.drawio` files.
- `backend-documentation` — optional upstream documentation for implemented backend flows; do not duplicate its use-case analysis.
- `archify` — architecture HTML renderer; inspect its installed `SKILL.md` at generation time. Its generation and delivery workflow is required when installed and omitted when absent.

## Examples

- [Reference application architecture package](examples/reference-application/architecture.md) demonstrates how to mark a diagram-derived design as proposed, document evidence gaps, keep logical and deployment diagrams separate, and provide component, infrastructure, and Archify artifacts when available.
