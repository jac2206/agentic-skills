# Authoring and validation

Read for generation, modification, conversion or validation. The catalog owns
type-specific rules; this reference owns the shared model, format differences
and practical checks. All resource/script paths below resolve from this Skill's
own package. Architecture Documentation does not need to be installed.

## Common conceptual model

Keep one model per selected view, at one stated abstraction level. A table is
sufficient; use a file only when useful to the requester or repeated editing.

| Record | Minimum content |
| --- | --- |
| View | Type ID, purpose, scope/level, current/reported/proposed status, source revision when available, selected formats |
| Node | Stable semantic ID, name, role/type, responsibility, enclosing boundary, evidence/status |
| Relationship | Stable ID, source/target semantic IDs, meaning, direction, supplied protocol/data/event, evidence/status |
| Boundary | Stable ID, meaning and parent, members, evidence/status; never infer network membership from drawing proximity |
| Notation details | Sequence: ordered message IDs, return/async kind, guards/fragments; ER: attributes, keys, multiplicities, optionality and identifying status; DFD: level, processes, stores and named data flows |
| Format mapping | Semantic ID → Mermaid ID and Draw.io page/cell IDs, including separate labels, icons, anchors and containers |
| Icon inventory | Node ID, exact stencil or SVG source/library, exact/category/generic symbol, availability/provenance checks, fallback reason and rendered status |

Keep stylistic/helper cells outside the semantic node inventory. Containment,
messages, entity rows and cardinalities are part of the model, not decoration.
Repeated instances of one participant or component must map back to its identity.

For modifications, first reconcile the existing diagram with the supplied change.
Preserve stable IDs, unaffected elements/pages and prior meaningful styling.
For conversions, report any unsupported construct before representing it with a
clearly labeled equivalent; do not silently drop messages, entity attributes,
groups or relationship meanings. A style-only request must preserve the model.

## Mermaid profile and limitations

Use stable, conservative syntax supported by the actual destination. Read the
target's configured Mermaid version when available; never claim universal host
compatibility from the current website alone.

- Flowchart: explicit `flowchart LR` or `flowchart TD`, stable ASCII identifiers,
  quoted human labels, basic rectangles/rounded nodes/diamonds/cylinders, named
  subgraphs and consistent `classDef`/`class` styling.
- C4: typed flowchart nodes and enclosing subgraphs preserve C4 semantics without
  enabling its experimental grammar. Label people, systems, containers or
  components at the selected level.
- Sequence: `sequenceDiagram`, explicit participants/actors and aliases, ordered
  messages, differentiated returns/async messages, supported guards/fragments.
  Do not paste flowchart `classDef` or subgraph syntax into this grammar.
- ER: `erDiagram`, explicit entities, attributes/keys and relationship labels,
  optionality/cardinality at both ends. Use only features the target version
  supports; do not assume flowchart styling or icon syntax works here.
- Default to ordinary labels instead of HTML, Markdown labels, newer icon/image
  node syntax, remote images, custom fonts, initialization directives or extra
  layout engines. Use those only when the destination supports them and they
  improve the requested result. Quote/escape punctuation according to the grammar;
  avoid reserved identifiers such as an unquoted lowercase `end` in flowcharts.
- Preserve semantic identity if a node label is shortened; put extra explanation
  in the delivery record or an appropriate diagram note.
- Mermaid chooses its own geometry. Subgraph directions may be overridden by
  connections to outside nodes; fixed positions, identical routing and exact
  Draw.io spacing are not portable guarantees. Reduce density rather than
  adding fake relationships as layout constraints.
- Apply a consistent readable palette with classes where supported. Sequence
  and ER have different styling capabilities; use supported themes only when
  the host exposes them. Never force flowchart classes into other grammars.
- Icons depend on host support and installed/registered packs or CSS. Check the
  actual rendering path and inspect a successful render before claiming icons
  work. Otherwise use labels such as `API`, `Queue`, `External system` and
  compatible shapes. Emoji and unregistered icon tokens do not prove icon support.

Official references, checked during authoring on 2026-11-15; verify the target
renderer rather than assuming it matches their current version:

- [Flowchart syntax and icon prerequisites](https://mermaid.js.org/syntax/flowchart.html).
- [Sequence notation](https://mermaid.js.org/syntax/sequenceDiagram.html).
- [ER notation and attributes](https://mermaid.js.org/syntax/entityRelationshipDiagram.html).
- [Parser API](https://mermaid.js.org/config/usage.html): `mermaid.parse` validates
  definitions without rendering; it cannot prove layout or glyph appearance.

### Parser and render execution

Prefer the project's existing Mermaid checks. If its existing Node.js environment
can import `mermaid`, initialize it according to that renderer's documentation
and validate each file with `await mermaid.parse(source)`; catch exceptions and
treat a `false` result as failure. Record the actual package version and runtime.
Some versions/grammars need DOM facilities even during parsing; a missing DOM is
a tooling failure, not evidence that the diagram is invalid. Do not invent a
regex-based syntax validator or install a package silently.

If Mermaid CLI is already available, invoke the single-attempt guard:

```sh
python3 <skill-directory>/scripts/render_diagram.py --tool mermaid --input docs/diagrams/<view>.mmd --output <temporary-preview-directory>/<view>.svg --attempt-record <task-scratch-directory>/render-attempts.json
```

Replace angle-bracket placeholders. The helper resolves the installed package
from the working directory (or `--tooling-directory`), or accepts its existing
JavaScript executable with `--mermaid-cli <path>`. Do not pass a `.cmd` wrapper.
On Windows use `py -3` instead of `python3`. All bundled utilities use Python;
only the external Mermaid CLI requires its own existing Node.js runtime. The
helper reads installed package manifests without running npm or Node for discovery.
Use `--node <executable>` only to select an existing runtime for that CLI.
Use the CLI's existing browser configuration;
do not download Chromium, add layout engines or weaken browser security just to
obtain a preview. After one discovery/startup/render failure stop using that
renderer for this task; do not switch to another executable, browser or host.
For a standalone parser startup/environment failure, likewise do not retry the
tool; continue manual source review. A successful
render also exercises syntax, but visual validation additionally requires opening
and inspecting the resulting image. Inspect SVG using a supported viewer or
render to PNG if necessary; source inspection alone is not a visual review.

## Draw.io reuse and notation adaptations

Use the bundled `references/drawio-xml.md` for XML structure, icon discovery,
SVG embedding and layout. Read the relevant provider reference conditionally.
Inspect `examples/reference-diagrams/component-diagram.drawio` or the chosen
provider's file for concrete styles and geometry. The examples contain embedded
SVGs, not a separate installed icon library or a general-purpose generator.

Generation means authoring native XML from the model using these conventions.
`check_drawio.py` checks existing XML; `render_diagram.py` guards attempts and
calls `render_drawio.py` for Draw.io export. None of these utilities
script designs a diagram, selects services, downloads icons or creates XML.

Directly reusable mechanisms:

- Standard `mxfile` → `diagram` → `mxGraphModel` → `root` → cells structure,
  stable IDs and editable labels/geometry; uncompressed XML is easiest to inspect.
- Native software cards, actors, cylinders and grouping; embedded neutral client
  SVGs in the provider examples may be reused for the same device meaning.
- Verified AWS4 stencils, exact-service or truthful category SVGs, independent
  labels and a recorded source/fallback. Existing example assets establish local
  availability, not current vendor provenance or correct glyph mapping.
- Tiered layout, explicit external zones, relevant provider/network scopes,
  whitespace, restrained palette and primarily orthogonal architecture connectors.

The incorporated resources are adapted here without editing Architecture Documentation:

| Concern | Diagram Engineering adaptation |
| --- | --- |
| Scope | Only selected views/formats. No full architecture document, implicit AWS target or Archify output. |
| Palette | Reuse logical role colors: client `#DAE8FC` / `#6C8EBF`, API `#FFF2CC` / `#D6B656`, component `#E2F0D9` / `#82B366`, data `#E1D5E7` / `#9673A6`, neutral boundary `#F8F9FA` / `#7F8C8D`; dark readable text and restrained connectors. Preserve vendor icon colors. Add textual roles/status so color is not the only cue. |
| Spacing | Start from a 10 px grid, roughly 20–30 px boundary padding and room for titles; use consistent icon/label gaps and expand to fit. Architecture labels typically 12–14 px, titles 20–24 px. These are starting values, not a substitute for inspection. |
| AWS icon geometry | Reuse 78×78 primary / 46×46 secondary `resourceIcon` treatment and white stroke where applicable. Preserve native aspect ratio for other vendors and neutral symbols. |
| Containment | Prefer true parent/member relationships for movable groups, using parent-relative coordinates. Existing provider examples also use visually enclosing frames with cells on the base layer; inspect and explicitly check membership rather than copying that arrangement as semantic containment. |
| Architecture edge captions | Reuse sharp orthogonal routing and separate editable annotations. Map each annotation to its relationship; keep captions clear of routes and adjacent icons. |
| Sequence | Horizontal labeled messages, dashed vertical lifelines, return arrows and fragment frames. Use native attached anchors/lifelines and editable text; preserve semantic order. Straight connectors and message labels can cause intentional architecture-style warnings. |
| ER | Entity tables, attribute/key rows, relationship captions and crow's-foot endpoints. No flowchart arrowheads standing in for cardinalities. If verified native crow's-foot markers are unavailable, use explicit editable `0..1`, `1`, `0..*`, `1..*` labels in both the model and drawing. |
| Other semantics | Decision branch captions, event names, integration contracts and DFD data labels are required when meaningful. A house-style warning about edge text must never remove required meaning. |

Prefer native vector symbols verified in the target library. For provider SVGs,
follow discovery and provenance rules rather than redrawing a trademark. Record
the exact source/stencil, checks and fallback for every component representation,
including generic symbols. A single inventory row may cover repeated uses of the
same verified resource if all corresponding node IDs are named.

## Validation gates

### 1. Selection and evidence

Confirm requested types, formats, scope, language and destination. Compare all
modeled elements against supplied material or explicit proposal labels. Check
sources against the actual workspace/revision when available; flag unavailable
or conflicting references. Do not infer that a dependency is actively used just
because it appears in a manifest.

### 2. Mermaid syntax

Run the actual parser or renderer for each `.mmd` when available. Report parser
version, operation and outcome. Without it, manually review grammar, declarations,
IDs, escaping, blocks and selected catalog rules; record `not run` for parser
validation and report manual review separately. Do not call that a syntax pass.

### 3. Draw.io structure and local checker

Run the local checker on each created/modified file. It parses and preflights
every page before calculating geometry: nonempty model/root, base cells `0` and
`1`, unique nonempty IDs, finite geometry, valid parents without cycles, and
relationship endpoints resolving to vertices/anchors. It checks native component
cards as well as icon/text collisions and children extending outside parents.
Windows:

```powershell
py -3 '<skill-directory>/scripts/check_drawio.py' 'docs/diagrams/<view>.drawio'
py -3 '<skill-directory>/scripts/check_drawio.py' --require-provider-icons ibm --icon-inventory 'docs/diagrams/<view>.icons.json' 'docs/diagrams/<view>.drawio'
```

On macOS/Linux, use `python3` in place of `py -3`. Replace placeholders with the
actual package and output paths. `--require-provider-icons` accepts
`aws`, `azure`, `google` or `ibm`; use it for a provider-specific infrastructure or
deployment view. For a multi-provider view check each present supported provider;
do not impose a nonexistent option on other vendors or provider-neutral views.
For other providers, verify their library/assets and provenance manually and
report the checker's enforcement limitation.

Exit `0` means no reported errors; exit `1` means reported errors; argument errors
use exit `2`. Record file/tool access failures and repair static inputs when
within scope. Python 3.10+ is required; no packages are installed. Static
validation may be repeated after a repair; it never opens either editor.

The checker validates parseability, IDs, parents, endpoints, geometry,
component/icon/text overlaps, SVG XML and selected provider markup. It reports
architecture-style warnings on geometry, caption placement, non-orthogonal edges
and some route intersections. Read every warning. Document intentional notation
exceptions with the affected cell/message/relationship IDs; fix genuine overlaps
and incorrect references. Do not filter all warnings or claim intentional
non-orthogonal ER/sequence connections as a structural failure.

Mark native frame objects `data-role="boundary"`, attachment vertices
`data-role="anchor"` and intentionally free-ended nonsemantic lines
`data-role="decoration"` when needed. These are local authoring hints, not standard
notation semantics. Prefer real parent/member relationships. The checker also
recognizes swimlanes, parent containers and the existing visual frame style;
never mark a component as a boundary to conceal a collision.

Nested geometry uses original parent offsets, including relative anchors, without
double-counting ancestors. Component boxes are geometric estimates; text fit,
auto-routed connectors and arbitrary custom stencils still need visual review.
Object-wrapper cell IDs/custom editor constructs outside the plain `mxCell`
profile may require careful normalization while preserving metadata or an explicit
unsupported-input report. An exit code of zero does not prove sequence/ER
semantics, icon authenticity, complete library availability or rendered quality.

### 4. Resources and icons

Inspect each used native stencil/library or asset. Parse each embedded SVG and
check its source/mapping, aspect ratio and separate editable label. Verify SVG
content has no external image/font/style references needed for offline display;
check native `image=` properties for remote or local file paths. Inspect embedded
resources as data; do not execute scripts or follow active links in supplied SVG.
Source and library verification may require browsing official catalogs, but no
network request should be needed merely to display the delivered diagram.

SVG markup is provider-neutral and cannot satisfy a provider requirement alone.
When provider icons are embedded SVGs, supply one JSON inventory for that Draw.io
file using `--icon-inventory`. Each row identifies exactly one icon cell by its
page name and ID; require unique page names for inventory-backed checks:

```json
{
  "icons": [
    {
      "page": "Infrastructure",
      "cell_id": "service-icon",
      "provider": "ibm",
      "source": "<actual official asset URL or verified library identifier>"
    }
  ]
}
```

Replace the example fields with the real icon mapping. Supported provider values
are `aws`, `azure`, `google`, `ibm`. Use one row per cell, including repeated uses.
Other inventory details (kind, fallback, check status) can be recorded alongside.
Generic devices must not be declared as provider services. The checker verifies
references, SVG validity and incompatible native-provider declarations; source
strings are declarations, not automatic verification of authenticity. It neither
contacts URLs nor verifies the glyph-to-service mapping. Keep that manual check
separate. No provider mark must be fabricated to obtain a pass.

### 5. Semantics and equivalence

For every selected format, reconcile against the model:

- Node identities, names, types, evidence status and boundary membership.
- Edge source, target, direction and meaning, not just counts or visual proximity.
- Sequence messages including repeated calls, order, replies, guards and fragments.
- ER attributes/types/keys, both-end multiplicity/optionality and identifying status.
- Process branch conditions and loops; DFD levels and data labels; event routing
  and delivery semantics only when supplied.

For both formats, map each semantic record to its actual diagram objects. Helper
labels, pictograms, lifelines, table rows or repeated display nodes need not have
matching cell counts. Keep unresolved information visible in both. Record any
unrepresentable difference explicitly; do not claim full equivalence while losing
meaning.

### 6. Editor compatibility and visual quality

The Draw.io checker estimates inline edge-label boxes for explicit orthogonal
routes and warns about overlaps with components, boundary titles and other estimated labels. It
also compares separate text-cell bounds with estimated boundary titles. It
also warns when explicit routes cross titles or other routes, share segments,
or cross another edge's estimated label. Crossings and shared segments may be
intentional; inspect them in context rather than treating warnings as errors. It
also checks explicit connector segments against components and reports automatic
or implicit routes and unsupported label offsets as unverified. Treat these as
heuristics: font metrics, routing, label positions and line crossings in the
editor may differ. Zero warnings is not a visual pass. Review every warning,
adjust ports, waypoints or label offsets and rerun static checks after layout
changes. Avoid long unbroken Mermaid labels and unnecessarily wide layouts.

Use an available safe editor/renderer and inspect generated previews when
possible. Do not launch Desktop merely because its executable exists. Use the
guard when visual review was requested or the exporter is confirmed working:

```powershell
py -3 '<skill-directory>/scripts/render_diagram.py' --tool drawio --input 'docs/diagrams/<view>.drawio' --output '<temporary-preview-directory>/<view>.png' --attempt-record '<task-scratch-directory>/render-attempts.json'
```

The Python guard requires Python 3.10+ and the standard library only. It calls
the bundled exporter with the same Python interpreter; that exporter discovers
the installed Draw.io executable (or `DRAWIO`) and has a 90-second timeout.
The guard enforces a 100-second outer process deadline; it never
retries. Its exit `0` means a nonempty preview was produced, `1` an attempt failed,
`2` bad arguments/record/preconditions, and `3` an attempt was skipped.

Reuse the same task-wide record for **both** renderers. A file is rendered at
most once; after any discovery/startup/export failure or interruption, every
later attempt for that renderer is skipped, including other files. Successful
exports permit other selected files once each. A lock prevents concurrent calls;
an interrupted attempt/lock blocks further launches until explicitly reviewed.
Do not bypass the guard by calling `render_drawio.py`/`mmdc` directly, switch
backends or reset the record after failure. If the current task already has a
known failure, report it and do not launch again. Explicit user authorization is
required for a new attempt after failure. Keep the record in disposable task
storage, outside the Skill package; it is validation evidence, not runtime setup.
Source and preview destinations must differ and the preview path must be fresh.
No project upload or dependency installation is performed.

Record editor/version and whether the actual file opened/imported. An exporter
success with an inspected preview is rendering evidence, not proof that every
object was edited successfully. Inspect visible glyphs, separate labels, grouping,
arrowheads/cardinalities, order, alignment, boundary titles, spacing, overlaps,
route crossings and legibility at normal zoom and fit-to-page scale. Repair and
repeat static checks within scope; do not rerender a file automatically. If no editor/renderer works, report editor compatibility and
visual validation as `not run`, even when syntax/structural checks pass.

### 7. Delivery record

For each view report files/formats and model/evidence status. For checks report
`passed`, `failed`, `not run` or `not applicable`, method/tool/version, findings,
intentional warning exceptions and limits. Separate syntax, structural, semantic,
equivalence, resource, editor/import, rendering and visual results. Include the
icon inventory and remaining gaps. Return only actual artifact paths; never claim
that an unexecuted check or a documented example passed.

## Script regression checks

These commands test the local checker and render-attempt state machine without
launching either graphical renderer or downloading anything:

```powershell
py -3 -B -m unittest discover -s '<skill-directory>/scripts/tests' -p 'test_*.py' -v
```

Use `python3` on macOS/Linux. Python's standard-library test runner runs these
checks without launching Node, either editor, or any diagram renderer.
The render tests inject process outcomes and temporary preview content; passing
them is not evidence of an actual editor launch or inspected diagram.
