# Azure icon guidance for Draw.io

Use this reference when creating or reviewing an Azure infrastructure diagram. Provider icons communicate the design; they do not prove that a resource is deployed.

## Source and selection

Use Microsoft's current [Azure Architecture Center icon collection](https://learn.microsoft.com/en-us/azure/architecture/icons/) as the authoritative source. The collection is updated over time, so check it when selecting icons instead of relying on an old local copy or legacy Draw.io stencil. Prefer a service-specific icon; if the official pack has only a category icon, keep the exact Azure service name in an editable label.

Do not invent one-to-one Azure equivalents from AWS or Google Cloud. Choose services based on the documented requirements and behavior, and mark unconfirmed choices as proposed. Keep each icon's native color and proportions. Microsoft's guidance says not to crop, flip, rotate, or distort the icons.

## Embedding SVG in Draw.io

For a portable `.drawio` file, embed only the SVG assets used by the diagram as image cells. Use a data URI with SVG media type and URL-encoded or base64-encoded SVG content. Keep labels, boundaries, and connectors as editable Draw.io objects. An embedded SVG remains a movable image object; it is not an editable collection of vector paths.

Do not paste an external image URL that requires network access to render. Preserve attribution or usage requirements that apply to Microsoft's icon package; its icon terms permit use in architecture diagrams and documentation subject to those terms.

## Verification workflow

1. Select the service icon from the current official package and confirm the service name in Microsoft's source.
2. Open the `.drawio` in diagrams.net. Confirm each embedded icon renders, retains its proportions and colors, and is not clipped or distorted.
3. Review the diagram at normal zoom for readable labels, consistent spacing, connector routing, and overlaps.
4. Record whether validation was structural, rendered, or visually reviewed. XML parsing cannot verify an embedded SVG or layout quality.

The Draw.io Azure stencil library may lag behind Microsoft's official package. When it does, use the official SVG rather than a generic cloud symbol or an obsolete service mark.
