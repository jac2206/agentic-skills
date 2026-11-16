# Incorporated diagram resources

On 2026-11-15 the user explicitly requested a self-contained Diagram Engineering
package, local diagram scripts and IBM Cloud coverage. This supersedes the
earlier choice to resolve resources through an installed sibling Skill.

Source baseline: this repository's `skills/architecture-documentation/`, declared
version `1.8.13` at the time of the original adaptation. The paths below are
relative to each package; incorporated resources are maintained independently.

| Source | Local destination | Adaptation |
| --- | --- | --- |
| `scripts/check_drawio.py` | Same relative path | Preserve XML/SVG parsing, style and collision mechanisms. Add native component collisions, hierarchy/geometry preflight, corrected nested/relative geometry, IBM markup, explicit SVG/provider inventory and resource checks. |
| `scripts/render_drawio.py` | Same relative path | Preserve executable discovery/export parameters. Remove retry advice; use only behind the new attempt guard. |
| `references/drawio-xml.md` | Same relative path | Preserve authoring/icon standards; adapt full-package/default-cloud wording, local commands and provider validation for this Skill. |
| `references/aws4-icons.md`, `azure-icons.md`, `google-cloud-icons.md` | Same relative paths | Preserve provider guidance; apply this Skill's single-attempt policy. |
| `examples/reference-application/component-diagram.mmd` and `.drawio` | `examples/reference-diagrams/` | Package the original logical style examples as instructional fixtures. |
| Three provider `*-infrastructure.drawio` files in that directory | `examples/reference-diagrams/` | Package native styles and embedded SVGs needed after installation. Adjust only AWS card/label geometry where the stronger checker found collisions. No topology change. |

New resources: IBM guidance, Python render-attempt guard and focused Python
regression tests. All bundled utilities use Python's standard library, including
orchestration. The former JavaScript helper and tests were replaced at the user's
request; version-1 task receipts remain readable and prior failures block retries.
Only an external Mermaid CLI retains its own Node.js runtime requirement.
There is no generic
diagram generator, repository CLI, agent runtime or automatic icon downloader.

The 2.2.0 boundary-title and connector layout heuristics, extended in 2.3.0 to
inspect source/target interiors, are also packaged in
Architecture Documentation's `scripts/layout_checks.py` at the user's request.
The identical small helper is intentionally bundled in each independent Skill;
compare both copies and run regression tests when changing it. Their main
checkers retain their own validation behavior.

The packaged reference diagrams are illustrative proposals, not verified
deployments or current vendor catalogs. Their embedded phone/laptop and provider
SVGs are locally available references, not evidence of icon provenance or a
rendered pass. Verify each selected resource for the actual deliverable. The AWS
geometry correction was statically checked; visual review remains unperformed.

Do not bring over Architecture Documentation's architecture-document template,
Archify artifacts or full-package/default-AWS behavior. They are unrelated to
selected-view authoring. When refreshing a copied resource, compare source and
local changes, preserve local fixes, rerun tests and review the Skill version;
do not overwrite the source package or blindly synchronize whole directories.
