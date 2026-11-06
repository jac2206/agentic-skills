# Draw.io XML authoring and validation

Use `.drawio` as an editable diagrams.net document. The file is XML with an `mxfile` root, a `diagram` element, an `mxGraphModel`, and a `root` containing cells.

## Cell structure

- Include base cells `id="0"` and `id="1"` with `id="1"` parented to `0`.
- Give each vertex and edge a unique, stable `id`.
- Vertices use `vertex="1"`, `parent="1"`, a Draw.io `style`, a human-readable `value`, and an `mxGeometry` child with `x`, `y`, `width`, `height`, and `as="geometry"`.
- Edges use `edge="1"`, `parent="1"`, valid `source` and `target` cell IDs, a style with an arrowhead, and relative geometry. Keep edge `value` empty in the reference house style; put a short editable text annotation next to the connector when its meaning is not self-evident.
- Escape XML special characters in `value` text. Use `&#xa;` for line breaks.
- Use native editable shapes and text. Do not embed a rendered screenshot as the diagram.

## Architecture layout

Place clients to the left, ingress and identity next, compute in the center, and data/messaging to the right or below. Use distinct tiers and whitespace; do not compress all nodes into one horizontal line. In infrastructure views, include an outer boundary labeled with the target provider and a visually distinct external zone for clients and third-party systems. Use nested containers for account/project/subscription, region, and network scopes (VPC, VNet, or VPC network) when they are evidenced or explicitly proposed. Label unknown location or scope `TBD`; do not invent a region, subnet, or availability zone. Keep each service inside or outside the VPC/VNet according to its actual provider topology. Draw boundary-crossing connectors clearly and label public, private, and external paths when needed. Mark proposed boundaries as proposed. These deployment boundaries do not belong in the cloud-agnostic component diagram.

### People and device pictograms

- Search the general Draw.io libraries and any supplied visual references for recognizable person/user, browser/laptop, phone/tablet, kiosk, or device pictograms before using boxes. Apply this in both the component and infrastructure views wherever people or client devices appear.
- Prefer native Draw.io vector shapes or embedded SVG image cells that remain movable. Check that the selected shape/library exists in the target Draw.io environment; if an SVG is embedded, keep its label as a separate editable text cell.
- Keep actor/device pictograms visually distinct from cloud-provider service icons. A user, browser, or phone is not an AWS/Azure/Google Cloud service.
- Use standard boxes or UML/component symbols for application modules when pictograms would imply an inaccurate product or make the view harder to read. The goal is semantic visual cues, not an icon on every node.
- Use a generic box for a person/device only when no suitable pictogram can be found. Mark this as a visual fallback and keep it visually distinct from service or software-component boxes. Do not turn application modules into pictograms when that would misrepresent their role. The linter can detect common actor/device shape names for collision checks, but cannot decide whether a pictogram semantically matches its label. If a rendered preview is requested and available, confirm this visually there.

## Matching a visual reference

When the user supplies an image or points to an existing diagram as a style reference, inspect it before drawing and compare these dimensions:

- Canvas background, grid, contrast, and overall aspect ratio.
- Reading direction, tier order, grouping, and boundary treatment.
- Provider icon generation, icon size, and use of editable service labels.
- Color palette, typography hierarchy, label length, and whitespace.
- Connector color, line weight, routing, arrowheads, and placement of explanatory notes.

Carry over the visual language, not unverified nodes or relationships. Keep labels concise; put long explanations in a note or legend away from connectors. If the user requests visual comparison and the renderer is stable, render the diagram and compare it with the reference. Fix visible differences that are not required by the architecture. `scripts/check_drawio.py` checks XML structure and limited geometry heuristics; it does not compare styles, detect stale or blank provider glyphs, assess all dynamic connector-label collisions, or decide whether two diagrams look alike. If no render was requested or rendering is unavailable, do not claim visual matching was verified.

For the supplied house-style linter, use sharp orthogonal connectors (`edgeStyle=orthogonalEdgeStyle;rounded=0`), leave edge labels empty, and place any explanatory caption in a separate text cell away from connector routes. Route edges around labels and unrelated icons; avoid crossings where a small reroute can remove them. Keep service names in separate editable text cells rather than embedding them in provider icon/image cells. AWS4 resource icons use 78×78 px primary icons or 46×46 px secondary icons with a white stroke; do not apply those fixed dimensions or stroke rules to official Google Cloud or Azure SVGs.

## Cloud deployment view

This file answers where the application runs. It is not a second component diagram.

### Provider, region, network, and external boundaries

- Draw one outer provider scope (`AWS Cloud`, `Azure`, or `Google Cloud`) for the proposed or current deployment. Do not use that frame to imply a specific account or tenant unless the account/tenant is identified or explicitly proposed.
- Nest an account/project/subscription and region boundary only when they are known or useful to explain the target. For proposals, use a neutral placeholder such as `Region TBD` or `Account / project TBD` where the placement matters; never invent a region name.
- Draw the network boundary (`VPC`, `VNet`, or Google Cloud `VPC network`) around only the resources that belong to that network. A provider-managed service may be in the provider/region boundary but outside the customer VPC/VNet. Follow that provider's topology instead of nesting every icon in one network box.
- Put browsers, mobile devices, users, and systems hosted outside the target provider in a separate `External` zone. Keep them outside the provider frame. If a client is hosted by the provider, show that hosting placement explicitly.
- Place Kubernetes cluster/workloads inside the appropriate network scope when the proposed design requires it. Show public and private subnets/AZs only when evidence or a clearly labeled proposal supports them; otherwise note `subnets/AZs TBD` without drawing fabricated detail.
- Route connectors across boundary edges cleanly. A line crossing a boundary should make the ingress/egress relationship readable; label it `HTTPS/API`, `private link`, or another protocol/path only when supported or clearly proposed.
- Use a dashed/soft boundary or a `PROPOSED` header for hypothetical scopes. The frame represents an architecture boundary, not a provider service icon.

### Provider icon discovery and fallback

Use this resolution order for every cloud service in the selected provider's infrastructure diagram:

1. Search the installed diagrams.net provider library and verify the exact service name/stencil identifier.
2. Search the diagrams.net extra-icon catalog when available. Do not leave the delivered diagram dependent on a remote custom-library URL.
3. Check the selected provider's current official icon catalog and the corresponding provider reference in this Skill. Prefer an exact service icon; use its official SVG if the Draw.io stencil is missing or stale.
4. If the current official catalog has no suitable service icon, use an official category icon only when it accurately represents the service category, and keep the exact service name in a separate editable label.
5. If neither an exact nor a truthful category icon can be verified, use a simple editable service card instead of an invented logo. Give it a restrained accent from the selected provider/category, show the exact provider and service name, and mark the icon as unavailable/unverified in the card or a nearby legend. Report the fallback in the architecture document.

Do not stop at AWS4: perform this search for AWS, Azure, or Google Cloud according to the selected target. Do not substitute another cloud's logo, guess a stencil name, or say an icon does not exist if the catalog/library could not be inspected. If access to the sources is blocked, call the icon unverified and use the service-card fallback with that limitation recorded. A service-card fallback is a deliberate notation for a cloud resource, not a claim that the card is an official provider icon.

For portable output, prefer a native stencil or embed the selected official SVG in the `.drawio` as a data URI. Do not reference an icon by local path or remote URL: those can disappear when the file is opened on another machine or offline. Record the source/stencil for each cloud service in the architecture document's icon inventory.

- Use the selected provider's verified current service icons where available, and keep the full service name as editable text. Apply the fallback order above when none can be verified. Use human/device pictograms for user and client endpoints, separate from provider boundaries and cloud service icons. For AWS4 identifiers, consult [AWS4 icon guidance](aws4-icons.md); for official Azure SVGs, consult [Azure icon guidance](azure-icons.md).
- AWS diagrams.net libraries include multiple generations of AWS shapes. Prefer the current AWS4 service icon set and follow an attached user reference's library and visual treatment when provided. AWS icons may use direct service stencils or `shape=mxgraph.aws4.resourceIcon` plus a service-specific `resIcon`. Verify each stencil against the installed diagrams.net AWS library or official catalog; do not guess a stencil name. If the exact icon is not available, continue through the category-icon and service-card fallback order. Avoid old library generations and dated gradients when the user supplies a newer flat service-icon treatment. AWS notes that third-party libraries can contain legacy icon sets and the official icon package is updated periodically: [AWS architecture icons](https://aws.amazon.com/architecture/icons/). See the [diagrams.net style reference](https://www.drawio.com/docs/reference/diagram-generation/style-reference/) and [AWS4 icon guidance](aws4-icons.md).
- For Google Cloud, prefer the current official product and category SVG pack over legacy console icons or older `mxgraph.gcp2.*` stencils. Google updated its product iconography in 2025. Use a product icon when available; use a clearly labelled category icon only when the official pack has no service-specific icon. Keep the service name explicit so a category mark is not mistaken for the product logo. Embed only the SVGs used as `data:image/svg+xml` in Draw.io `image` cells so the file is portable. Consult [Google Cloud icon guidance](google-cloud-icons.md) for selection and verification.
- For Azure, prefer the current official Azure Architecture Center SVG package over older `mxgraph.azure.*` stencils when its icon set is newer. Embed only the used SVGs as portable Draw.io `image` cells. Preserve each vendor icon's proportions and colors; Microsoft says not to crop, flip, rotate, or distort its icons. Keep labels, relationships, and boundaries as editable Draw.io objects. Embedded SVG icons remain movable/scalable image objects, not individually path-editable stencils. See [Google Cloud product icons](https://cloud.google.com/icons), [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/), and [Azure icon guidance](azure-icons.md).
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
3. Every edge has both a `source` and a `target`, and both resolve to existing cell IDs. Report intentionally free-ended connectors separately; do not count them as validated relationships.
4. Every component in scope is present and relationships agree with the evidence map.
5. Open the `.drawio` in diagrams.net when available. Confirm provider icons and person/device pictograms render, text remains readable at normal zoom, connector routes avoid labels and unrelated icons, and spacing remains clear.

A successful XML parse verifies syntax and references, not that diagrams.net rendered the diagram correctly. Run [`scripts/check_drawio.py`](../scripts/check_drawio.py) for structure, label/icon overlap, explicit connector/label intersections, inline-label, connector-style, route-crossing, and embedded SVG syntax checks. Add `--require-provider-icons aws|azure|google` for infrastructure diagrams; it fails if no recognized provider stencil is present, or if no embedded SVG markup is present for Azure/Google diagrams. The checker recognizes `mxgraph.gcp`, `mxgraph.gcp2`, and `mxgraph.gcp3` families and parses percent-encoded or base64 SVG data URIs even when the Draw.io style contains the `;base64` metadata separator. Embedded SVG markup is provider-neutral to the checker: it cannot prove the SVG source belongs to the claimed provider or represents the labeled service. Verify those facts in the icon inventory. Do not launch the Draw.io exporter by default. Use [`scripts/render_drawio.py`](../scripts/render_drawio.py) for a preview only when the user requests rendered review or confirms the installed Desktop exporter works; inspect the preview for blank/stale icons, label fit, connector routing, and readability. The scripts need Python 3.10+ and no third-party packages:

```powershell
py -3 <skill-directory>/scripts/check_drawio.py docs/architecture/component-diagram.drawio
py -3 <skill-directory>/scripts/check_drawio.py --require-provider-icons aws docs/architecture/aws-infrastructure.drawio
py -3 <skill-directory>/scripts/check_drawio.py --require-provider-icons azure docs/architecture/azure-infrastructure.drawio
py -3 <skill-directory>/scripts/check_drawio.py --require-provider-icons google docs/architecture/google-cloud-infrastructure.drawio
py -3 <skill-directory>/scripts/render_drawio.py preview docs/architecture/aws-infrastructure.drawio %TEMP%\aws-infrastructure-preview.png
```

```sh
python3 <skill-directory>/scripts/check_drawio.py docs/architecture/component-diagram.drawio
python3 <skill-directory>/scripts/check_drawio.py --require-provider-icons aws docs/architecture/aws-infrastructure.drawio
python3 <skill-directory>/scripts/check_drawio.py --require-provider-icons azure docs/architecture/azure-infrastructure.drawio
python3 <skill-directory>/scripts/check_drawio.py --require-provider-icons google docs/architecture/google-cloud-infrastructure.drawio
python3 <skill-directory>/scripts/render_drawio.py preview docs/architecture/aws-infrastructure.drawio /tmp/aws-infrastructure-preview.png
```

Report which levels of validation actually ran.
