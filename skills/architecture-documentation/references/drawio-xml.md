# Draw.io XML authoring and validation

Use `.drawio` as an editable diagrams.net document. The file is XML with an `mxfile` root, a `diagram` element, an `mxGraphModel`, and a `root` containing cells.

## Cell structure

- Include base cells `id="0"` and `id="1"` with `id="1"` parented to `0`.
- Give each vertex and edge a unique, stable `id`.
- Vertices use `vertex="1"`, `parent="1"`, a Draw.io `style`, a human-readable `value`, and an `mxGeometry` child with `x`, `y`, `width`, `height`, and `as="geometry"`.
- Edges use `edge="1"`, `parent="1"`, valid `source` and `target` cell IDs, a style with an arrowhead, a readable `value` label when the relationship is not self-evident, and relative geometry.
- Escape XML special characters in `value` text. Use `&#xa;` for line breaks.
- Use native editable shapes and text. Do not embed a rendered screenshot as the diagram.

## Architecture layout

Place clients to the left, ingress and identity next, compute in the center, and data/messaging or external dependencies to the right or below. Use containers only for real or clearly marked proposed boundaries. Label protocols, asynchronous paths, ownership, and unconfirmed mappings. Avoid making the visual imply a deployment fact that the evidence does not support.

## Cloud deployment view

This file answers where the application runs. It is not a second component diagram.

- Use the selected provider's native diagrams.net shape library for AWS, Google Cloud, or Azure services. Prefer vendor service icons over generic database/cloud shapes and keep the full service name as editable text. If the user requested branded provider icons, do not silently fall back to generic shapes: resolve the native stencil identifiers or report that the icon requirement is blocked. A provider-colored fallback is permitted only when the request does not require branded icons and the fallback is disclosed.
- AWS diagrams.net libraries include multiple generations of AWS shapes. Prefer the current AWS architecture icon set and follow an attached user reference's library and visual treatment when provided. AWS icons may use direct service stencils (for example, `shape=mxgraph.aws4.endpoint` or `shape=mxgraph.aws4.lambda_function`) or `shape=mxgraph.aws4.resourceIcon` plus a service-specific `resIcon`. Verify each stencil against the diagrams.net AWS library or authoritative catalog; do not guess or replace a requested icon with a generic box. Avoid old library generations and dated gradients when the user supplies a newer flat service-icon treatment. AWS notes that icon libraries can contain legacy sets and are updated periodically: [AWS architecture icons](https://aws.amazon.com/architecture/icons/). See also the [diagrams.net shape style reference](https://github.com/jgraph/drawio/wiki/Styles).
- For Google Cloud, prefer the current official product and category SVG pack over legacy console icons or older `mxgraph.gcp2.*` stencils. Google updated its product iconography in 2025. Use a product icon when available; use a clearly labelled category icon only when the official pack has no service-specific icon. Keep the service name explicit so a category mark is not mistaken for the product logo. Embed only the SVGs used as `data:image/svg+xml` in Draw.io `image` cells so the file is portable.
- For Azure, prefer the current official Azure Architecture Center SVG package over older `mxgraph.azure.*` stencils when its icon set is newer. Embed only the used SVGs as portable Draw.io `image` cells. Preserve each vendor icon's proportions and colors; Microsoft says not to crop, flip, rotate, or distort its icons. Keep labels, relationships, and boundaries as editable Draw.io objects. Embedded SVG icons remain movable/scalable image objects, not individually path-editable stencils. See [Google Cloud product icons](https://cloud.google.com/icons) and [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).
- Show each application runtime within its deployment boundary (for example, one API runtime containing the backend modules). Draw modules as separate cloud workloads only when they have independent deployment/runtime evidence.
- Draw only meaningful deployment infrastructure: client/device, hosting/compute, ingress, database/object storage, queues if used, and network/security boundaries if evidenced or clearly marked as proposed. Do not add fashionable services just to fill the topology.
- Label the view `CURRENT`, `REPORTED`, or `PROPOSED`. When actual hosting (such as Vercel/Railway/Supabase) differs from a requested/default AWS target, separate the current topology and the AWS proposal into separately named Draw.io files when both views are in scope.
- A cloud-service icon is visual notation, not evidence that a service exists. A proposed AWS topology must visibly say so in its title or legend.
- Keep application component names and business responsibilities in the Mermaid view. In Draw.io, labels should explain the deployed workload and provider service, not repeat the whole logical module tree.

Recommended visual order is clients -> edge/ingress -> compute -> persistence or messaging, grouped by provider/network boundary. Keep user devices and mobile-store distribution outside a server VPC unless their placement is actually part of it.

## Component view

When a complete architecture package requests a Draw.io component diagram, create `component-diagram.drawio` alongside `component-diagram.mmd`. Both show the same logical components and relationships; use editable native shapes and group components by software boundary (client, API, domain modules, persistence, or integrations). Do not add cloud regions, subnets, availability zones, CDN/load-balancer placement, or service-icon containers to this view. Those belong in the separately named provider infrastructure diagram: `aws-infrastructure.drawio` by default, `google-cloud-infrastructure.drawio` for Google Cloud, or `azure-infrastructure.drawio` for Azure. Generate only the selected provider unless the user requests multi-cloud alternatives.

Before delivery, compare nodes and edges in the two component formats. Differences in layout and notation are expected; differences in architecture are not. Compare the infrastructure diagram separately against the documented runtime/deployment model rather than requiring one-to-one node parity with the logical component view.

## Validation

Parse the document with a standard XML parser. Then check:

1. The root and required Draw.io structure exist.
2. Cell IDs are unique.
3. Every edge's `source` and `target` resolve to existing cell IDs.
4. Every component in scope is present and relationships agree with the evidence map.
5. The `.drawio` opens in diagrams.net as an editable diagram when that application is available.

A successful XML parse verifies syntax and references, not that diagrams.net rendered the diagram correctly. Report the actual level of validation.
