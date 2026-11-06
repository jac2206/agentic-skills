# Google Cloud icon guidance for Draw.io

Use this reference when creating or reviewing a Google Cloud infrastructure diagram. An icon is visual notation; it does not prove that a service is deployed.

## Source and selection

Search the installed diagrams.net Google Cloud library first, then check Google's [official Google Cloud product icon library](https://cloud.google.com/icons) as the authoritative source. The library distinguishes core product icons from product category icons and also offers legacy console icons. Google's product iconography was updated in early 2025, so prefer verified current product/category assets, including a current `mxgraph.gcp3.*` stencil when it is available and matches the service, over legacy console marks and older `mxgraph.gcp2.*` stencils.

Choose a core product icon when available. Use a category icon only when the specific product has no suitable current icon, and keep the actual service name in an editable label so the category mark is not mistaken for a product logo. If neither an exact service icon nor a truthful category icon can be verified, use the labeled service-card fallback in [Draw.io XML guidance](drawio-xml.md) and record why it was needed. Do not infer service choices by translating an AWS or Azure design one-for-one, and do not borrow their icons.

## Embedding SVG in Draw.io

For portable `.drawio` files, embed only the SVG assets used by the diagram in `image` cells, using an encoded `data:image/svg+xml` URI. Do not use external URLs that require a network connection to render. Keep labels, boundaries, and connectors as editable Draw.io objects. An embedded SVG is a movable image object; it is not a collection of individually editable paths.

Preserve each icon's colors and proportions. Avoid redrawing or recoloring product marks. Check Google's current icon overview and package terms when selecting or distributing icons.

## Verification workflow

1. Confirm the product name and choose its current core product icon from Google's library. If using a category icon, mark the category nature in your design notes and label the service explicitly.
2. Open the `.drawio` in diagrams.net. Confirm each embedded SVG renders, is not clipped or distorted, and has a readable editable product label.
3. Review spacing, connector routes, and overlaps at normal zoom.
4. If no suitable core or category icon was found, use and disclose the labeled service-card fallback defined in [Draw.io XML guidance](drawio-xml.md).
5. Report whether validation was structural, rendered, or visually reviewed. XML parsing cannot verify SVG rendering or layout quality.
