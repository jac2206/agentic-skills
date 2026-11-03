---
name: architecture-documentation
description: >
  Creates evidence-based application architecture documentation with a Mermaid
  and editable Draw.io component view, a separate provider-specific Draw.io
  infrastructure view, and a native Archify architecture diagram when the
  Archify Skill is installed.
metadata:
  version: "1.7.0"
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

The component diagrams and cloud infrastructure diagram are cumulative deliverables. Never use one as a substitute for another. If no target provider is named, use AWS and label the infrastructure diagram as a proposed AWS target. Generate only the selected/default provider unless the user requests multi-cloud alternatives.

## Workflow

1. **Establish scope.** Read applicable `AGENTS.md` instructions, product context, specifications, READMEs, existing architecture documentation, source/configuration/deployment evidence, and supplied diagrams in the active workspace. Record the product purpose, actors, business capabilities, system boundaries, and whether each view is current, reported, proposed, or mixed. Do not let a generic README substitute for product evidence.
2. **Build an evidence map.** Trace components and relationships through source, imports, API routes, calls, schemas, deployment configuration, and supplied material. Mark material claims as verified, configured, documented, user-reported, inferred, proposed, unknown, or conflicting. Keep evidence paths for product claims as well as technical claims. A dependency, resource name, README statement, or icon alone does not prove active behavior or deployment.
3. **Select the views.** Honor a named target cloud. Otherwise use proposed AWS, even when the user did not explicitly ask for a cloud diagram. Keep a reported/current host topology distinct from the target-cloud proposal. Use a logical component diagram for software responsibilities and relationships; use the infrastructure diagram for runtime placement, provider services, and evidence-backed or explicitly proposed boundaries.
4. **Write the document.** Use `templates/architecture-document.md` if the project has no suitable template. Open with the application's actual purpose and capabilities when evidence exists. Describe only supported behavior, cite evidence, distinguish reported facts from proposals, and record unresolved questions. Do not overwrite the general project README.
5. **Create the diagrams.** Keep Mermaid and component Draw.io consistent and cloud-agnostic. Create a separate editable infrastructure Draw.io using current native provider icons and readable service names. For AWS, prefer the current diagrams.net AWS4 service stencils and the user's visual reference, if supplied. For Google Cloud and Azure, prefer current official provider SVGs when built-in stencils are stale. Do not use generic component boxes as a cloud diagram or imply that proposed services are deployed.
6. **Invoke Archify when available.** Check the active Skill catalog and installed Skill locations for `archify/SKILL.md`. If found, read and invoke it for native architecture authoring. Prefer its candidate schema, repository guidance, matching example, CLI `finalize architecture` workflow, validation, and delivery paths; preserve and link the actual candidate, HTML, and receipt. If a tool process cannot start, first follow any shell-unavailable fallback explicitly documented by that Archify version for native diagrams. Use its own template and authoring constraints; label the result as a fallback and do not claim CLI finalization, receipts, or validations that did not occur. Do not invent an alternate renderer. If Archify is absent, create no Archify artifacts. If both the native workflow and its documented fallback fail, report the blocker and link only outputs actually produced.
7. **Cross-check and report.** Compare the document and all diagrams against the evidence map. Validate XML, cell IDs, edge references, Mermaid structure, links, and required output inventory. Report the selected provider, current/proposed status, Archify detection and output status, evidence gaps, and any blocked checks.

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
- The infrastructure diagram uses current provider icons, readable service names, and clear current/reported/proposed status.
- XML is parseable, cell IDs are unique, edge endpoints resolve, and artifact links work.
- When Archify is installed, the native workflow produces a linked candidate, finalized HTML, and receipt; if its documented shell-unavailable fallback is needed, the HTML is labeled as a fallback and no missing receipt or validation is claimed. When absent, no Archify files are created.

## Validation

1. Reconcile the document and diagrams against the evidence map; check that reported and proposed claims are labeled.
2. Parse component and infrastructure Draw.io XML; check unique IDs and valid edge endpoints.
3. Check Mermaid syntax and compare its components and relationships with the component Draw.io and document.
4. Confirm the infrastructure diagram is a provider-specific deployment view, not a repeated component map; confirm AWS is used and marked proposed when no provider was named.
5. Check artifact links and locations. For a complete package, confirm the document, both component diagrams, and separate infrastructure diagram exist.
6. Check Archify in the active catalog and installed locations. If available, use its native workflow and verify the receipt and actual outputs. If a tool process cannot start, check the installed Archify Skill's documented shell-unavailable fallback; if used, report it as a fallback without claiming finalize receipts or gates. Distinguish structural validation, browser checks, and visual review. If Archify is absent, confirm no Archify artifacts were created.
7. Report generated/missing status for each required artifact, the Archify result, and any evidence or tool blocker. Do not claim blocked checks passed.

## Composition

- `backend-documentation` may provide verified backend behavior and structure; this Skill owns the system-wide architecture package and diagrams.
- `archify` owns native candidate authoring, HTML rendering, validation, and delivery when installed, including any fallback it documents for shell-unavailable native diagrams. It does not replace evidence collection, the architecture document, or Draw.io deliverables.

## References

- [Architecture document template](templates/architecture-document.md) — use when the project has no suitable template.
- [Draw.io XML authoring and validation](references/drawio-xml.md) — consult when creating or repairing Draw.io files.
- `backend-documentation` — optional source of verified backend details; do not duplicate its use-case analysis.
- `archify` — invoke its installed Skill for native architecture output; omit Archify artifacts when absent.

## Examples

- [Reference application architecture package](examples/reference-application/architecture.md) demonstrates a diagram-derived proposal with evidence gaps and distinct component, infrastructure, and Archify artifacts.
- [Google Cloud infrastructure example](examples/reference-application/google-cloud-infrastructure.drawio) and [Azure infrastructure example](examples/reference-application/azure-infrastructure.drawio) demonstrate provider-specific alternatives. They do not mean all provider diagrams should be generated for one request.
