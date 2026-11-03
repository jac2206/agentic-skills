---
name: architecture-documentation
description: >
  Creates evidence-based application architecture documentation with a domain-
  grounded document, a logical component diagram in Mermaid, a distinct cloud
  deployment diagram in editable Draw.io XML, and an Archify architecture
  diagram generated through the installed Archify Skill when available.
metadata:
  version: "1.5.0"
---

# Architecture Documentation

Create a traceable architecture package from the application's repositories and user-supplied requirements. Explain the product and its business capabilities from project evidence, then produce distinct logical and deployment views: Mermaid and editable Draw.io component diagrams, plus a provider-specific Draw.io infrastructure diagram. At generation time, check whether the Archify Skill is installed: if installed, hand off Archify generation to that Skill and use its native authoring, CLI finalization, and HTML delivery workflow; if absent, create no Archify artifacts.

## Purpose

Explain an application's components, relationships, deployment topology, data and integration paths, security boundaries, and operational concerns without presenting unknown or proposed facts as implemented behavior. Every complete architecture package includes a provider-specific infrastructure Draw.io diagram. Use AWS as a proposed target when the user does not name a target cloud, regardless of whether they explicitly asked for a cloud diagram. If Archify is installed, its architecture HTML is also a required deliverable.

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

- Target cloud provider (`AWS`, `Google Cloud`, `Azure`, or another provider), audience, deployment environment, architecture style, and output directory. Honor a named target; if none is supplied, default to AWS and mark the infrastructure diagram as a proposed AWS target. Generate only the selected/default provider view unless the user explicitly asks for multi-cloud alternatives. This default applies to every complete architecture package and does not depend on an explicit request for a cloud diagram.
- Existing diagrams, ADRs, API specifications, infrastructure-as-code, deployment manifests, and architecture documents.
- Backend documentation created by `backend-documentation`.

If no application implementation or specification is available, document only what the supplied material establishes. Identify evidence gaps and label any target-state design as proposed. A host named as part of the current stack (for example, Vercel, Railway, or Supabase) is evidence about that deployment, not an implicit selection of AWS, Google Cloud, or Azure as the target cloud. Keep those views distinct when the requested/default target differs from current hosts.

## Outputs

Create the requested artifacts together under the project's established documentation location. If none exists, use `docs/architecture/`:

For every complete architecture package, generate all of these distinct deliverables. Do not infer that a diagram is optional because the user did not repeat the artifact list in the latest prompt. Do not count either component format as a substitute for the infrastructure view.

These deliverables are cumulative, not alternatives: retain or create `architecture.md`, the Mermaid component diagram, and the editable component Draw.io, then add the separate cloud infrastructure Draw.io. When Archify is installed, add its HTML and source JSON as well. Never repurpose the component Draw.io as the infrastructure diagram or replace the base artifacts with Archify output.

Always include the separate infrastructure Draw.io. Honor a target provider named by the user; when none is named, use AWS and label the diagram as a proposed target, even if the request never explicitly says “cloud” or “AWS”.

- `component-diagram.drawio` — editable Draw.io version of the logical component view in `component-diagram.mmd`.
- `component-diagram.mmd` — Mermaid version of the same logical component view.
- Provider-specific infrastructure Draw.io — required and separate from component diagrams: `aws-infrastructure.drawio`, `google-cloud-infrastructure.drawio`, or `azure-infrastructure.drawio` for the selected provider. When no provider is named, create only `aws-infrastructure.drawio`. Do not emit all provider diagrams unless the user requests multi-cloud alternatives.
- `current-deployment.drawio` — optional, only when the current hosting topology is in scope and differs from the selected/default target-cloud proposal.
- `architecture.md` — scope, system context, components, interactions, data and events, cloud topology, security, availability/operations, evidence status, decisions, and gaps. Omit sections that do not apply.
- Archify's native architecture candidate JSON and finalized standalone HTML in the output location prescribed by Archify — required when Archify is installed. Create and deliver these by invoking the installed Archify Skill and its documented CLI `finalize architecture` workflow; use the candidate schema, examples, repository-evidence guidance, and validation gates specified by that Skill. Preserve its candidate, HTML, and receipt outputs, and link the actual paths from `architecture.md`. Do not hand-author HTML, imitate Archify's appearance, or use a generic/custom renderer as a substitute. If Archify is absent, omit all Archify artifacts and directories. If its native workflow cannot run, report the blocker; do not fabricate or substitute an output.

Adapt filenames and location to existing project conventions. Do not place generated artifacts in the repository root.

## Workflow

### Product and view separation gates

Before following the numbered workflow:

- For a system spanning repositories, inspect each repository the user identifies. Read applicable agent instructions, product context/specs, README, and architecture notes, then corroborate domain claims against routes, screens, service calls, domain logic, or deployment configuration. A generic or stale README must not define the architecture by itself.
- The architecture document must open with the actual product purpose, actors, and core business capabilities when evidence exists. A technology inventory or paraphrase of the user's prompt does not satisfy the product overview.
- Keep the Mermaid component view logical: software responsibilities, domain capabilities, and their calls/data relationships. Keep cloud services, VPCs, subnets, load balancers, and placement in the Draw.io deployment view.
- The separate infrastructure Draw.io must show where workloads and data are deployed, using the selected cloud's current native service icons and readable provider service names. For AWS, prefer the latest AWS architecture icon set available in diagrams.net; follow the visual style of a user-provided reference when supplied. The `aws4` library includes both direct stencils (such as `mxgraph.aws4.endpoint` and `mxgraph.aws4.lambda_function`) and `mxgraph.aws4.resourceIcon` with service-specific `resIcon` values. Verify each icon against the target service and avoid legacy libraries, gradients, or oversized icon tiles when the reference uses the current flat icon style. Do not render the cloud view with generic boxes when the native icon library is available, and do not copy the component-box layout into this file.
- For Google Cloud or Azure, prefer current official provider SVG product icons embedded in the `.drawio` file when built-in stencils are stale; do not use AWS icons or generic service boxes. For Google Cloud, prefer its 2025 product/category icon set over legacy console icons; for Azure, use the current Architecture Center package. Keep icon assets proportional and intact, make labels and connections editable, and label a category icon as a category when no product-specific icon is available. Select provider services from evidence and explicit design assumptions; examples are proposed illustrations, not one-to-one service mappings. Create only the requested/selected provider's infrastructure file unless multi-cloud output is explicitly requested.
- Save XML only in `.drawio` files. Markdown documents link to artifacts; never append raw or escaped XML to a README or link list.

1. **Establish scope.** Read applicable `AGENTS.md` files, product context/specs, READMEs, existing architecture documentation, source/configuration/deployment evidence, and user-provided diagrams. For multi-repository systems, inspect each repository named by the user. Determine product purpose, actors, business capabilities, which repository owns each component, and whether each view is current-state, proposed target-state, reported, or mixed. Corroborate README claims with implementation or specs; record generic/stale/conflicting README content instead of copying it as product truth.
2. **Build an evidence map.** Trace components and relationships through imports, calls, API routes, infrastructure definitions, configurations, schemas, and supplied diagrams. Classify each material claim as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Keep repository-relative evidence paths for product purpose and key capabilities as well as technical components. A resource name, README claim, dependency, or icon alone does not prove active deployment or runtime behavior.
3. **Select one cloud target.** Honor an explicit target-cloud choice. If the user did not specify a target provider, default to AWS and create the required `aws-infrastructure.drawio` as a proposed AWS design. This applies even when the prompt only says “architecture documentation” or does not explicitly mention a cloud diagram. If Google Cloud or Azure is specified, use only its provider-named infrastructure file and icon library; do not also emit AWS by default. Generate multiple target-cloud diagrams only when the user explicitly requests alternatives/multi-cloud. A current host such as Vercel, Railway, or Supabase describes the reported/current deployment; it does not silently replace or satisfy the target-cloud diagram. When current deployment is in scope and differs from the selected/default target, document the current hosting facts in `architecture.md` and create a separate `current-deployment.drawio` when useful; never use it in place of the required target infrastructure diagram. Mark unverified user-reported placement as reported, not deployed/configured.
4. **Write the architecture document.** Use the bundled template as a starting structure when the project has no local template. Begin with the product purpose and actual domain capabilities, then explain components, request/data/event paths, persistence, deployment, security, availability, and operations only as supported. Cite evidence in the document and distinguish facts from user-reported details and proposals. Do not overwrite the general project README. If `docs/architecture/README.md` is the established architecture document, update it in place with evidence-based content and valid links. Record unresolved decisions and evidence gaps.
5. **Create the component diagram.** Create both `component-diagram.mmd` and editable `component-diagram.drawio` from the same logical model. Use domain-meaningful names, group software components by real system boundary, label important calls/actions and async paths, and preserve evidence-backed relationships. Do not draw network/cloud placement as part of this logical view. Cross-check the two formats for the same components and relationships.
6. **Create the cloud infrastructure diagram.** Always write one required editable Draw.io deployment view as a separate file: `aws-infrastructure.drawio` for selected/default AWS, `google-cloud-infrastructure.drawio` for selected Google Cloud, or `azure-infrastructure.drawio` for selected Azure. This is additional to `component-diagram.drawio`; it must show cloud placement and must not repeat the logical component diagram. Use the selected provider's native service icon library and editable full service names. Before delivery, confirm the XML contains provider-specific icon styles and is a cloud deployment view; a generic-shape component map fails. Show clients, provider services, runtime/compute, data services, ingress, and only evidenced or explicitly proposed network/security boundaries. Keep application modules inside actual compute boundaries unless separate deployments are evidenced. Label the view CURRENT, REPORTED, or PROPOSED; keep inferred services visibly proposed. Keep node IDs unique and all edge references valid. Consult `references/drawio-xml.md`.
7. **Detect and invoke the installed Archify Skill.** Before writing an Archify candidate or output, inspect the active Skill catalog and installed Skill locations available to the agent for `archify/SKILL.md`. Treat Archify as installed when it appears in the active catalog or its Skill file is available in an installed location. If found, read and invoke that Skill as the downstream authoring and delivery capability; do not merely imitate its output or independently write HTML. For this repository-backed architecture, follow its `architecture` native-diagram route, repository-authoring guidance, matching showcase example, schema, and authoring defaults. Create the native candidate JSON and run the installed CLI's complete `finalize architecture` workflow with the repository root, matching quality profile, and JSON receipt as prescribed by the Archify Skill. Let Archify own its candidate/output/receipt paths and link the actual delivered HTML from `architecture.md`. Candidate creation and HTML delivery are mandatory; do not skip them for convenience or omit their status from the final report. If Archify is absent from both the catalog and available installed locations, do not create Archify JSON, HTML, or Archify-specific directories; continue with the other artifacts and state that Archify was unavailable. If its native workflow fails, retry/fix the failure where possible, then report the failing step and retain/link only artifacts actually produced. Never substitute handwritten HTML or another renderer. If HTML was delivered but a later browser gate fails, retain it and the candidate, report the failed gate, and do not claim full validation or visual review.
8. **Cross-check the diagrams.** Compare Mermaid, Draw.io, Archify (when generated), and prose against the same evidence map. Their supported components and relationships must agree; any difference must be an explicitly different abstraction or a documented scope limitation.
9. **Validate and report.** Parse both component and infrastructure `.drawio` files as XML; check unique cell IDs and valid source/target references. Check Mermaid structure and compare the Mermaid/Draw.io component nodes and relationships. Run Archify's documented validation/delivery workflow when installed. Verify every required deliverable exists and is linked in the architecture document: component Mermaid, component Draw.io, provider-specific infrastructure Draw.io and, when installed, Archify HTML plus its candidate JSON. If a required artifact is missing, create or repair it before completion, or state the concrete blocker and status in the final report. Include a concise checklist naming the chosen/default provider, whether the infrastructure view is proposed/current, Archify detection status, and Archify output status.

## Rules

The Skill must:

- Keep implemented/current-state facts separate from inferred or proposed target-state design.
- Trace every component and relationship to source evidence or explicitly label it as proposed/unknown.
- Preserve the user's requested scope, cloud provider, language, and diagram formats.
- Represent trust, network, runtime, and data-ownership boundaries only when evidence supports them; label proposal boundaries as proposed.
- Keep Mermaid, Draw.io, the output from Archify's installed Skill, and written descriptions synchronized. When Archify is installed, invoke its native authoring and complete CLI delivery workflow as a required output step; handwritten imitation is not an acceptable substitute.
- Use service names appropriate to the chosen provider and keep product/API names in their original form.
- Derive the product/domain summary from repository context and corroborate it with implementation or specifications; do not produce a technology-only summary when product evidence exists.
- For a multi-repository solution, identify which repository supports each product, client, backend, and deployment claim.
- Make the component and deployment diagrams answer different questions; use provider-specific service icons in Draw.io when available.
- Provide the component view in both Mermaid and editable Draw.io when creating a complete architecture package.
- Treat outputs as additive: preserve/create the architecture Markdown and both component-diagram formats, then add the separate cloud infrastructure Draw.io and, when installed, Archify HTML and source JSON. No output substitutes for another.
- Always provide a separate cloud infrastructure Draw.io for a complete package, named for its provider (`aws-infrastructure.drawio` for selected/default AWS). Default to proposed AWS when no target provider is named, even when the user did not explicitly request a cloud diagram. The infrastructure view must use native provider service icons and cannot be satisfied by the component Draw.io or the Archify HTML.
- When the user specifies Google Cloud or Azure, use that provider's named file and icon library instead of AWS. Generate only that selected target unless multi-cloud alternatives are requested. Do not infer one-to-one service equivalence from the AWS example; explain any proposed service substitutions and unresolved choices.
- Keep `.drawio` XML in its own `.drawio` file. Never paste raw or escaped XML into Markdown, a README, or a link list.
- Reuse established project documentation location, naming, and style when available.

The Skill must not:

- Invent services, routes, protocols, regions, networking, data stores, security controls, availability, compliance, or production status.
- Treat a diagram icon, README claim, directory name, dependency, or infrastructure template as proof that a component is deployed or active.
- Do not create Archify artifacts when the Archify Skill is absent. Do not silently skip its generation workflow when installed, hand-author a substitute HTML, or claim a native Archify artifact without a successful Archify CLI delivery receipt. Report execution failures accurately.
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
- `archify` owns the candidate authoring, native HTML rendering, validation, and delivery whenever its Skill is installed. This Skill must invoke that capability and link its actual output; it must not implement an alternate Archify renderer. When Archify is absent, omit Archify artifacts. Archify does not replace evidence collection or the written architecture and Draw.io outputs.

## Quality criteria

- The document opening identifies the real product purpose and core capabilities from repository context/specs and implementation evidence; a stack-only summary or prompt paraphrase fails.
- The document states scope, evidence status, and whether the architecture is current or proposed.
- Every material component and relationship has evidence or an explicit proposal/unknown label.
- Mermaid is a logical software-component view; Draw.io is a provider-specific deployment view with runtime placement, cloud services, and applicable boundaries. The views are visibly distinct and consistent with the document.
- The Mermaid component diagram and Draw.io component diagram describe the same logical topology; the separately named infrastructure Draw.io is a distinct deployment topology.
- The infrastructure Draw.io uses current native AWS icons for AWS services when AWS is selected/default, with readable provider service names and the user's visual reference when supplied. Use verified service-specific stencils and avoid legacy icon sets. A generic box-only component map fails as an infrastructure view.
- Google Cloud/Azure targets use current official product SVGs embedded in their provider-named Draw.io file when older built-in libraries would look stale; otherwise use verified native stencils. Category icons are identified as such. The selected provider alone is generated unless alternatives were requested; service mappings are justified and labeled proposed.
- Current/provider-reported deployment and target-cloud proposal are clearly distinguished; proposals are never represented as deployed.
- Markdown links to standalone artifacts and contains no inline XML dump.
- The Draw.io XML is parseable; cell IDs are unique; every edge endpoint resolves to a cell.
- Cloud provider and service choices follow user input or documented evidence; assumptions are visible.
- Security, persistence, availability, and operations claims are calibrated to the evidence.
- Archify installation is checked. When installed, the installed Archify Skill authors the native candidate and its CLI finalizes and delivers the HTML; verify the delivery receipt and report its actual validation gates. Handwritten or imitation HTML does not satisfy this criterion. When Archify is absent, no Archify files or directories are created.
- The final report explicitly accounts for component Mermaid, component Draw.io, infrastructure Draw.io and, if Archify is installed, Archify HTML and candidate JSON. Required artifacts are not silently omitted; any blocker is stated.
- Files follow project conventions and links resolve.

## Validation

1. Reconcile the architecture document and each diagram with the evidence map.
2. Parse both Draw.io XML files and check IDs, vertex/edge references, and labels.
3. Confirm Mermaid is a logical view and Draw.io is a deployment view; reject Draw.io that only repeats generic application-component boxes.
4. Confirm product purpose/capabilities against repository context/specs and code, and ensure the opening describes this application rather than echoing the prompt.
5. Confirm Mermaid components and relationships agree with the documented logical architecture and that the cloud view agrees with deployment evidence/proposal labels.
6. Check the active Skill catalog and installed locations for Archify. When installed, invoke its native architecture authoring and complete CLI `finalize` workflow; confirm the receipt is successful and distinguish structural checks, browser checks, and visual inspection. Confirm the HTML was produced by that workflow, not hand-authored. When absent, verify there are no Archify artifacts or directories.
7. Confirm that the architecture document links the component Mermaid, component Draw.io, and separate provider-named infrastructure Draw.io. If no provider was named, confirm `aws-infrastructure.drawio` uses AWS4 resource-icon stencils and is labeled proposed. Reject any output where a component diagram or Archify HTML is presented in place of this file. When Archify is installed, confirm its HTML and candidate JSON exist and are linked; report a concrete blocker if either could not be generated.
8. Verify links, output locations, generated file inventory, and that XML exists only in `.drawio` files.
9. Report unresolved evidence gaps or validation failures, with an explicit generated/missing status for every required deliverable and the Archify detection result.

## References

- [Architecture document template](templates/architecture-document.md) — use when the project has no established architecture-document template.
- [Draw.io XML authoring and validation](references/drawio-xml.md) — consult when creating or repairing `.drawio` files.
- `backend-documentation` — optional upstream documentation for implemented backend flows; do not duplicate its use-case analysis.
- `archify` — downstream architecture authoring/rendering Skill. Invoke its installed `SKILL.md` and native CLI workflow to create the candidate and HTML; do not reproduce its renderer. Required when installed, omitted when absent.

## Examples

- [Reference application architecture package](examples/reference-application/architecture.md) demonstrates how to mark a diagram-derived design as proposed, document evidence gaps, keep logical and deployment diagrams separate, and provide component, infrastructure, and Archify artifacts when available.
- [Google Cloud infrastructure example](examples/reference-application/google-cloud-infrastructure.drawio) and [Azure infrastructure example](examples/reference-application/azure-infrastructure.drawio) demonstrate provider-specific proposed variants. They are instructional alternatives and do not mean all providers should be generated for a single target request.
