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

Place clients to the left, ingress and identity next, compute in the center, and data/messaging or external dependencies to the right or below. Use containers only for real or clearly marked proposed boundaries. Label protocols, asynchronous paths, ownership, and unconfirmed mappings. Avoid making the visual imply a deployment fact that the evidence does not support.

### People and device pictograms

- Search the general Draw.io libraries and any supplied visual references for recognizable person/user, browser/laptop, phone/tablet, kiosk, or device pictograms before using boxes. Apply this in both the component and infrastructure views wherever people or client devices appear.
- Prefer native Draw.io vector shapes or embedded SVG image cells that remain movable. Check that the selected shape/library exists in the target Draw.io environment; if an SVG is embedded, keep its label as a separate editable text cell.
- Keep actor/device pictograms visually distinct from cloud-provider service icons. A user, browser, or phone is not an AWS/Azure/Google Cloud service.
- Use standard boxes or UML/component symbols for application modules when pictograms would imply an inaccurate product or make the view harder to read. The goal is semantic visual cues, not an icon on every node.
- Use a generic box for a person/device only when no suitable pictogram can be found or rendered. Mark this as a visual fallback and keep it visually distinct from service or software-component boxes. Do not turn application modules into pictograms when that would misrepresent their role. The linter can detect common actor/device shape names for collision checks, but cannot decide whether a pictogram semantically matches its label. Confirm this during rendered visual review.

## Matching a visual reference

When the user supplies an image or points to an existing diagram as a style reference, inspect it before drawing and compare these dimensions:

- Canvas background, grid, contrast, and overall aspect ratio.
- Reading direction, tier order, grouping, and boundary treatment.
- Provider icon generation, icon size, and use of editable service labels.
- Color palette, typography hierarchy, label length, and whitespace.
- Connector color, line weight, routing, arrowheads, and placement of explanatory notes.

Carry over the visual language, not unverified nodes or relationships. Keep labels concise; put long explanations in a note or legend away from connectors. After authoring, render the diagram and compare it with the reference. Fix visible differences that are not required by the architecture. `scripts/check_drawio.py` checks XML structure and limited geometry heuristics; it does not compare styles, detect stale or blank provider glyphs, assess all dynamic connector-label collisions, or decide whether two diagrams look alike. If rendering is unavailable, report that visual matching could not be verified.

For the supplied house-style linter, use sharp orthogonal connectors (`edgeStyle=orthogonalEdgeStyle;rounded=0`), leave edge labels empty, and place any explanatory caption in a separate text cell away from connector routes. Route edges around labels and unrelated icons; avoid crossings where a small reroute can remove them. Keep service names in separate editable text cells rather than embedding them in provider icon/image cells. AWS4 resource icons use 78×78 px primary icons or 46×46 px secondary icons with a white stroke; do not apply those fixed dimensions or stroke rules to official Google Cloud or Azure SVGs.

## Cloud deployment view

This file answers where the application runs. It is not a second component diagram.

### Provider icon discovery and fallback

Use this resolution order for every cloud service in the selected provider's infrastructure diagram:

1. Search the installed diagrams.net provider library and its service names/stencil identifiers.
2. Check the selected provider's current official icon catalog and the corresponding provider reference in this Skill. Prefer an exact service icon; use its official SVG if the Draw.io stencil is missing or stale.
3. If the current official catalog has no suitable service icon, use an official category icon only when it accurately represents the service category, and keep the exact service name in a separate editable label.
4. If neither an exact nor a truthful category icon can be verified, use a simple editable service card instead of an invented logo. Give it a restrained accent from the selected provider/category, show the exact provider and service name, and mark the icon as unavailable/unverified in the card or a nearby legend. Report the fallback in the architecture document.

Do not stop at AWS4: perform this search for AWS, Azure, or Google Cloud according to the selected target. Do not substitute another cloud's logo, guess a stencil name, or say an icon does not exist if the catalog/library could not be inspected. If access to the sources is blocked, call the icon unverified and use the service-card fallback with that limitation recorded. A service-card fallback is a deliberate notation for a cloud resource, not a claim that the card is an official provider icon.

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

A successful XML parse verifies syntax and references, not that diagrams.net rendered the diagram correctly. Run [`scripts/check_drawio.py`](../scripts/check_drawio.py) for structure, label/icon overlap, explicit connector/label intersections, inline-label, connector-style, and route-crossing checks. Run [`scripts/render_drawio.py`](../scripts/render_drawio.py) for a preview when diagrams.net Desktop is available; only rendered visual review can assess dynamic line routing, icon rendering, text legibility, or visual similarity. The scripts need Python 3.10+ and no third-party packages:

```powershell
py -3 <skill-directory>/scripts/check_drawio.py docs/architecture/component-diagram.drawio docs/architecture/aws-infrastructure.drawio
py -3 <skill-directory>/scripts/render_drawio.py preview docs/architecture/aws-infrastructure.drawio %TEMP%\aws-infrastructure-preview.png
```

```sh
python3 <skill-directory>/scripts/check_drawio.py docs/architecture/component-diagram.drawio docs/architecture/aws-infrastructure.drawio
python3 <skill-directory>/scripts/render_drawio.py preview docs/architecture/aws-infrastructure.drawio /tmp/aws-infrastructure-preview.png
```

Report which levels of validation actually ran.
