---
name: architecture-documentation
description: >
  Creates evidence-based application architecture documentation with a Mermaid
  and editable Draw.io component view, a separate provider-specific Draw.io
  infrastructure view, and a native Archify architecture diagram when the
  Archify Skill is installed.
metadata:
  version: "1.8.10"
---

# Architecture Documentation

Create a traceable architecture package that explains an application's product context, software components, integrations, data paths, and deployment without presenting unknown or proposed details as verified facts.

## Purpose

Produce complementary architecture documentation and diagrams from project evidence and user-supplied requirements. Keep the logical software view separate from deployment topology.

## When to use

Use this Skill to create or update comprehensive application architecture documentation, including component, cloud infrastructure, Mermaid, Draw.io, or Archify diagrams.

## When not to use

- For a single backend use case or implementation flow, use `backend-documentation` when available.
- For a diagram-only request, create only the requested diagram.
- For a target architecture without implementation evidence, proceed only when the user requests a proposal and label it proposed.

## Inputs

### Required

- The active project workspace, an architecture specification, or user-supplied diagrams.
- Requested scope and output language, inferred from the request and project documentation.

### Optional

- Target cloud provider, audience, deployment environment, architecture style, output directory, API specifications, infrastructure as code, deployment manifests, ADRs, or backend documentation.

Use the active workspace as the only repository by default. Inspect another repository only when the user explicitly supplies its local path or link and asks to include it. Do not search for sibling repositories, clone or fetch repositories, or contact remote repository services. For components without supplied source, use the user's description and label claims user-reported or unknown. Missing external evidence is not a reason to stop.

If implementation or a specification is unavailable, document only what the supplied material establishes. A named host such as Vercel, Railway, or Supabase is evidence about the reported/current deployment, not a target-cloud choice.

## Outputs

Save artifacts under the project's established documentation location; use `docs/architecture/` when none exists. For a complete package, produce:

- `architecture.md`: product context, scope, components, interactions, data/events, deployment, evidence status, security and operations where supported, decisions, and gaps.
- `component-diagram.mmd` and `component-diagram.drawio`: equivalent logical component views.
- One separate infrastructure file for the selected provider: `aws-infrastructure.drawio`, `google-cloud-infrastructure.drawio`, or `azure-infrastructure.drawio`.
- `current-deployment.drawio` only when a separate current-hosting view is useful and differs from the selected target design.
- If Archify is installed, its native candidate JSON, standalone HTML, and workflow receipt/summary when produced. Prefer the finalized HTML. If its CLI cannot run, use only a shell-unavailable fallback explicitly documented by the installed Archify Skill and label the result as a fallback, not finalized.

Treat requests for complete, comprehensive, or system-wide architecture documentation as a request for this complete package by default. Do not require the user to enumerate the standard artifacts. A diagram-only request remains limited to the diagram explicitly requested. When the user names multiple cloud providers, create one separate infrastructure Draw.io per provider; retain one cloud-agnostic component view.

The component diagrams and cloud infrastructure diagram are cumulative deliverables. Never use one as a substitute for another. If no target provider is named, use AWS and label the infrastructure diagram as a proposed AWS target. Generate only the selected/default provider unless the user requests multi-cloud alternatives.

## Workflow

1. **Establish scope.** Read applicable `AGENTS.md` instructions, product context, specifications, READMEs, existing architecture documentation, source/configuration/deployment evidence, and supplied diagrams in the active workspace. Record the product purpose, actors, business capabilities, system boundaries, and whether each view is current, reported, proposed, or mixed. Do not let a generic README substitute for product evidence.
2. **Build an evidence map.** Trace components and relationships through source, imports, API routes, calls, schemas, deployment configuration, and supplied material. Mark material claims as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Keep evidence paths for product claims as well as technical claims. A dependency, resource name, README statement, or icon alone does not prove active behavior or deployment.
3. **Select the views.** Honor a named target cloud. Otherwise use proposed AWS, even when the user did not explicitly ask for a cloud diagram. Keep a reported/current host topology distinct from the target-cloud proposal. Use a logical component diagram for software responsibilities and relationships; use the infrastructure diagram for runtime placement, provider services, and evidence-backed or explicitly proposed boundaries.
4. **Write the document.** Use `templates/architecture-document.md` if the project has no suitable template. Open with the application's actual purpose and capabilities when evidence exists. Describe only supported behavior, cite evidence, distinguish reported facts from proposals, and record unresolved questions. Do not overwrite the general project README.
5. **Find, embed, validate icons, and show deployment boundaries.** Keep Mermaid and component Draw.io consistent and cloud-agnostic. Create a separate editable infrastructure Draw.io for every requested provider, using a recognizable provider icon for every service that has a verifiable icon. For each service, search in this order: (a) the current built-in Draw.io provider library; (b) the Draw.io extra-icon catalog when available; (c) the provider's current official icon catalog. Follow [Draw.io XML guidance](references/drawio-xml.md) and the provider reference. Prefer an exact service icon. When only a truthful category icon exists, use it and retain the exact service name as a separate editable label. Prefer official SVGs embedded as data URIs when the native stencil cannot be verified or might be missing in the recipient's Draw.io installation. Never guess a stencil name, use a different provider's icon, link to a remote image, or choose a generic rectangle before completing this search. If no suitable icon can be verified, use the documented labeled service-card fallback and record the service, sources checked, and reason in the architecture document. Before finalizing, produce a compact icon inventory for each provider diagram (service label, icon/stencil or SVG source, and fallback reason if any).

   In every provider infrastructure view, draw a labeled outer provider boundary and place users, client devices, and external systems outside it unless they are themselves hosted in that provider. Add nested boundaries for accounts/projects/subscriptions, regions, and network scopes (AWS VPC, Azure VNet, or Google VPC network) when they are evidenced or part of the proposed target. For a proposal whose exact region, account, subnet, or availability-zone placement is unknown, label that boundary or placement `TBD` instead of inventing a value. Keep workloads and managed services inside/outside the network boundary according to the provider's documented topology; do not put every cloud service inside a VPC/VNet. Show external integrations in a visually distinct `External systems` zone and route connectors across the relevant boundary. Label network paths when needed to distinguish public ingress, private connectivity, and external calls. Mark proposed boundaries `PROPOSED`; never let a container imply an existing deployment fact.

   For people and client devices in either diagram, search the general Draw.io libraries and supplied visual references for recognizable user/person, browser/laptop, phone/tablet, kiosk, or other device pictograms. Keep their labels separate and use a generic box only after searching; disclose that fallback. Software responsibilities may use standard component shapes. Route connectors with clear right-angle paths, minimize crossings, and never let lines cover labels or unrelated icons. Inspect a supplied visual reference and the closest existing Draw.io example before authoring. Match its visual language without copying unsupported architecture details. Run `scripts/check_drawio.py` on every Draw.io file created or modified, using `--require-provider-icons <provider>` on every infrastructure diagram. Inspect all warnings and the icon inventory. Do not launch Draw.io Desktop or its exporter automatically. Use `scripts/render_drawio.py preview` only when the user requests visual export/review or confirms the installed renderer is working. If export fails or times out, stop without retrying; deliver the editable XML, report that rendered review was unavailable, and do not describe it as visually verified.
6. **Invoke Archify when available.** Check the active Skill catalog and installed Skill locations for `archify/SKILL.md`. If found, read and invoke it for native architecture authoring. Prefer its candidate schema, repository guidance, matching example, CLI `finalize architecture` workflow, validation, and delivery paths; preserve and link the actual candidate, HTML, and receipt. If a tool process cannot start, first follow any shell-unavailable fallback explicitly documented by that Archify version for native diagrams. Use its own template and authoring constraints; label the result as a fallback and do not claim CLI finalization, receipts, or validations that did not occur. Do not invent an alternate renderer. If Archify is absent, create no Archify artifacts. If both the native workflow and its documented fallback fail, report the blocker and link only outputs actually produced.
7. **Cross-check and report.** Compare the document and all diagrams against the evidence map. Validate XML, cell IDs, edge references, Mermaid structure, links, and required output inventory. Confirm that every requested provider has its own infrastructure file and icon inventory. List service-card fallbacks and sources checked. Report the provider(s), current/proposed status, Archify detection and output status, evidence gaps, and any blocked checks. If an infrastructure diagram is missing or contains no recognized provider icons, report the package as incomplete; never imply the component view fulfilled the infrastructure requirement.

### Tool and environment failures

- Report the exact operation and error when a tool process cannot start. A startup failure does not prove that a repository is missing, inaccessible, or was contacted, nor that this Skill could not be read.
- Do not repeatedly retry startup failures or search unrelated repositories. Use another available workspace-reading mechanism if provided; otherwise continue from supplied evidence and mark source claims unverified.
- Never claim source inspection, validation, or artifact generation completed unless it did.

## Rules

- Never invent services, routes, protocols, regions, network boundaries, security controls, availability, compliance, or production status.
- Label uncertain, user-reported, inferred, conflicting, and proposed claims accurately.
- Keep `.drawio` XML in its own file; never paste raw or escaped XML into Markdown.
- Keep current deployment and target-cloud proposal distinct. Do not treat illustrative services as verified deployment.
- Do not create Archify files when the Skill is absent. When installed, use its native workflow or its documented shell-unavailable fallback; never invent an alternate renderer or claim that a fallback was CLI-finalized.
- Do not modify application source code or deployment configuration as part of documentation generation.
- Preserve project conventions and link artifacts from the architecture document.

## Constraints

- Write repository instructions, this Skill, references, templates, examples, and technical documentation in English. Write generated artifacts in the requested language or the language of project documentation.
- Draw.io deliverables must be editable `.drawio` XML, not screenshots or flattened images.
- When evidence is sparse, narrow the claims and state gaps instead of filling them with common patterns.
- An Archify browser or delivery failure limits validation; it does not justify claiming success or fabricating an output.

## Quality criteria

- The document describes the actual product and capabilities when evidence exists and states scope and evidence status.
- Every material component and relationship has evidence or an explicit status label.
- Mermaid and component Draw.io describe the same logical topology; the provider-specific infrastructure diagram is a distinct deployment view.
- People and client devices are visually distinguishable through recognizable pictograms, with readable labels kept separate.
- Lines follow clear routes without obscuring labels or crossing unrelated icons; text remains readable at normal zoom.
- Cloud services use verified icons from the selected provider when available. Any service-card fallback is clearly labeled and reported with the sources checked and why no icon was used.
- The infrastructure diagram uses current provider icons, readable service names, and clear current/reported/proposed status. Structural checks pass, layout warnings are resolved or explained, and supplied visual references are compared with a rendered output when a renderer is available.
- Each requested provider has a separate infrastructure diagram and icon inventory; the checker recognizes provider-icon markup and validates embedded SVG syntax. Stencils and SVGs still need visual inspection to prove their appearance; run a preview only when requested or when the renderer is known to work.
- Infrastructure diagrams distinguish the provider boundary, relevant account/project, region and network scopes from client devices and external systems. Unknown placement is labeled `TBD`, and proposed boundaries are visibly marked.
- XML is parseable, cell IDs are unique, edge endpoints resolve, and artifact links work.
- When Archify is installed, the native workflow produces a linked candidate, finalized HTML, and receipt; if its documented shell-unavailable fallback is needed, the HTML is labeled as a fallback and no missing receipt or validation is claimed. When absent, no Archify files are created.

## Validation

1. Reconcile the document and diagrams against the evidence map; check that reported and proposed claims are labeled.
2. Run `scripts/check_drawio.py` with every generated or modified `.drawio` path. For each infrastructure diagram, also pass `--require-provider-icons aws`, `--require-provider-icons azure`, or `--require-provider-icons google`. Resolve XML, duplicate-ID, dangling-edge, icon-overlap, and label-overlap errors. Review warnings for icon/label collisions, connector/label intersections, inline labels, AWS4 icon size/stroke, labeled or non-orthogonal edges, and routes crossing icons. The provider-icon option checks markup presence; embedded SVGs are parsed for XML validity. Neither check can verify the service-to-glyph mapping or visual appearance. Confirm source and mapping in the icon inventory. Confirm people and device endpoints use recognizable pictograms. Fix real issues and explain intentional warnings. The script is bundled inside this Skill directory, requires Python 3.10+, and uses only the standard library. Use `python3` on macOS/Linux or `py -3` on Windows. If Python is unavailable, report that check as blocked and continue with manual structural validation.
3. Check Mermaid syntax and compare its components and relationships with the component Draw.io and document.
4. Confirm the infrastructure diagram is a provider-specific deployment view, not a repeated component map; confirm AWS is used and marked proposed when no provider was named.
5. Check artifact links and locations. For a complete package, confirm the document, both component diagrams, and separate infrastructure diagram exist.
6. Do not launch Draw.io Desktop just to validate a generated diagram. If the user asks for a rendered preview, or confirms the exporter is stable, export diagrams sequentially with `scripts/render_drawio.py preview <file.drawio> <preview.png>` and inspect the PNG. Stop after the first exporter failure or timeout; do not retry automatically. Report rendered review as unavailable and do not claim visual verification. Structural validation and icon inventory remain required either way.
7. Check Archify in the active catalog and installed locations. If available, use its native workflow and verify the receipt and actual outputs. If a tool process cannot start, check the installed Archify Skill's documented shell-unavailable fallback; if used, report it as a fallback without claiming finalize receipts or gates. Distinguish structural validation, browser checks, and visual review. If Archify is absent, confirm no Archify artifacts were created.
8. Report generated/missing status for each required artifact, the Archify result, and any evidence or tool blocker. Do not claim blocked checks passed.

## Composition

- `backend-documentation` may provide verified backend behavior and structure; this Skill owns the system-wide architecture package and diagrams.
- `archify` owns native candidate authoring, HTML rendering, validation, and delivery when installed, including any fallback it documents for shell-unavailable native diagrams. It does not replace evidence collection, the architecture document, or Draw.io deliverables.

## References

- [Architecture document template](templates/architecture-document.md) — use when the project has no suitable template.
- [Draw.io XML authoring and validation](references/drawio-xml.md) — consult when creating or repairing Draw.io files; it defines icon discovery, portable embedding, and visual verification.
- [AWS4 icon guidance](references/aws4-icons.md) — consult when searching and verifying current AWS4 stencils and official AWS SVGs.
- [Azure icon guidance](references/azure-icons.md) — consult when selecting and embedding official Azure SVG icons.
- [Google Cloud icon guidance](references/google-cloud-icons.md) — consult when selecting and embedding current Google Cloud product/category SVG icons.
- [Draw.io checker](scripts/check_drawio.py) — run on each generated or modified Draw.io file; requires Python 3.10+ and no third-party packages.
- [Draw.io exporter](scripts/render_drawio.py) — use for preview/rendered visual review when diagrams.net Desktop is installed.
- `backend-documentation` — optional source of verified backend details; do not duplicate its use-case analysis.
- `archify` — invoke its installed Skill for native architecture output; omit Archify artifacts when absent.

## Examples

- [Reference application architecture package](examples/reference-application/architecture.md) demonstrates a diagram-derived proposal with evidence gaps and distinct component, infrastructure, and Archify artifacts.
- [AWS infrastructure proposal](examples/reference-application/aws-infrastructure.drawio), [Google Cloud infrastructure proposal](examples/reference-application/google-cloud-infrastructure.drawio), and [Azure infrastructure proposal](examples/reference-application/azure-infrastructure.drawio) show the same illustrative backend topology expressed with provider-specific services. They are alternatives, not evidence of deployment or a requirement to generate all three for one request.
- [Serverless GenAI Agent reference](examples/reference-application/serverless-genai-agent.drawio) demonstrates a more detailed AWS GenAI/RAG architecture. Treat its region, compute choices, integrations, and controls as illustrative unless separately verified.
