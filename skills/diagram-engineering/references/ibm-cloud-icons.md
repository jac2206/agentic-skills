# IBM Cloud icons and boundaries

Read for IBM Cloud infrastructure or deployment views. Apply the entry point's
single-attempt rule to editor/render checks. Source inspection is separate from
opening a diagram. No IBM icon pack or rendered IBM example is bundled here.

## Sources and selection

Use the installed **IBM Cloud** library when its glyph matches the service.
IBM's [architecture-diagram guidance](https://cloud.ibm.com/docs/architecture-framework?topic=architecture-framework-architecture-diagram)
distinguishes it from the deprecated older **IBM** library. Inspect the actual
installation instead of guessing `mxgraph` identifiers.

For unavailable glyphs, inspect the official
[IBM Cloud architecture-icons repository](https://github.com/IBM-Cloud/architecture-icons)
and its [stencil inventory](https://github.com/IBM-Cloud/architecture-icons/blob/main/drawio/stencils/2.0/Index.tsv).
It supplies Draw.io libraries and SVG assets, with some resources awaiting native
editor release. Confirm product, icon generation and usage terms before reuse.
Do not automatically install libraries or clone the repository.

Prefer an exact current service glyph, then a truthful category glyph. If neither
can be verified, use a labeled generic service symbol/card and disclose the
unverified resource. Do not replace IBM Cloud with an AWS/Azure/Google icon.

## Representation and portability

Preserve IBM's native colors, proportions and grouping conventions. Distinguish
location/deployment containment from association groupings such as security
membership; one must not imply the other. Draw cloud, region, VPC/subnet and
external boundaries only when supported by the model, with unknowns marked TBD.

Embed the selected official SVG as a data URI when the native library is not
verified. Keep its label, containers and connectors editable. Do not leave remote
image URLs or local library paths in the delivered file.

## Checking

Run the local checker with `--require-provider-icons ibm`. Native markup is a
heuristic, not proof that a stencil exists. Embedded SVGs require
`--icon-inventory <file.json>` to associate page/cell IDs, `provider: ibm` and
source. Independently verify the glyph-to-service mapping; successful XML or
inventory checks cannot establish vendor authenticity or visual appearance.
