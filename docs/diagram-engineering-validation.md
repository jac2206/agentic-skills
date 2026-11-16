# Diagram Engineering authoring and validation

Current revision: **2.4.0**, self-contained Python utilities and local validation.
The 1.0.0 and 1.1.0 records below are historical; current packaging and executed
checks are recorded in the final section. The former sibling-resource dependency,
absence of local scripts and JavaScript helper no longer describe this package.

## 2.4.0 cloud layout follow-up

The cloud-infrastructure workflow now requires authors to consult the package's
own provider example and arrange model-supported visual tiers without implying
additional network membership. On 2026-11-16, an employee AWS test added two
editable visual frames around existing access and service areas. XML comparison
preserved all previous semantic cells, relationships and containment; its Mermaid
source is unchanged. The local checker reported zero errors and 18 warnings,
including existing route crossings/shared segments and neutral SVG provenance.
The regression suite passed 44 tests. This is a static check of one AWS example,
not visual proof, a multi-provider execution, or a new Mermaid parser run. No
renderer was launched; the previous Draw.io launch had failed on Windows ACLs.

## 2.3.0 endpoint and regression review

The user-supplied rendered container diagram showed connectors entering endpoint
interiors despite passing older checks. Both Skills now warn about explicit paths
crossing source/target bounding boxes, and Architecture Documentation additionally
checks unrelated native components. Router-controlled paths remain estimates.
Both Skills instruct authors to retain the baseline and compare individual
findings and visual evidence rather than optimize warning counts. These tests and
instructions cannot establish rendered quality or automatically repair a layout.
The full Python regression suite passed 44 tests, including endpoint-interior,
border-contact, unrelated-component and router-estimate cases. Both packaged
checkers flagged the API and Contracts endpoint interiors in the employee C4
example. The Architecture Documentation checker processed five bundled reference
files with zero errors and 11–40 warnings each; these warnings require review.
No graphical renderer or editor was launched for this change, and the modified
Skills have not been exercised end-to-end on a newly rendered application diagram.

## 2.2.0 boundary and route review

On 2026-11-16, both Diagram Engineering and Architecture Documentation received
package-local layout heuristics for boundary-title collisions, explicit route
crossings and shared segments. The AWS employee example reproduced the reported
VPC title/edge-caption overlap as a warning. These heuristics cannot establish
actual rendered positions or determine whether a shared route is intentional.
The complete Python regression suite passed 42 tests, including checks of both
packages and identical helper copies. The Architecture Documentation checker
completed on all five bundled Draw.io reference files: zero errors, with 4 to 19
warnings per file requiring review. No editor or renderer was launched; the
existing screenshots are not evidence that the changed scripts repaired a view.

## 2.1.0 visual-layout follow-up

The supplied employee-system screenshots exposed overlapping connector captions,
congested routes and an excessively wide Mermaid view. The local Draw.io checker
now estimates label boxes on explicit routes, detects additional component
crossings and flags unknown automatic routes. These checks are heuristic, not
proof of a rendered layout. The Skill now calls for planned routes, label spacing
and compact Mermaid layouts. Existing architecture-documentation files were not
changed.

On 2026-11-16, the complete Python regression suite passed 39 tests. Two revised
local Draw.io examples passed the checker with zero errors and one warning each
about provider-neutral embedded SVG provenance. XML comparisons preserved all
cell identities, labels, containment and connection endpoints. A Mermaid copy
changed only the layout direction and label line breaks. These files are local
ignored examples. The revised files were not rendered, opened or visually
inspected, and the Mermaid parser was not run; their visual and syntax status
remain unverified. Existing screenshots are evidence of the earlier layouts only.

Date: 2026-11-15. Scope: create `skill/diagram-engineering` version `1.0.0`
using Skill Factory `1.2.1`, preserving existing Skills and repository architecture.
This is an authoring/resource-reuse record, not proof that every diagram type
has been rendered or that a specialist agent executed the Skill.

## Inspected evidence before authoring

- `AGENTS.md`, `docs/architecture.md`, `contracts/components.md`,
  `validators/README.md`, the root README and `.gitignore`.
- The explicitly requested installed Skill Factory and its bundled Skill and
  bilingual usage templates; repository Skill Factory conventions were compared.
- Architecture Documentation `1.8.13`: complete entry point, both Python scripts,
  Draw.io XML reference, AWS/Azure/Google Cloud references, document template,
  bilingual guide, Mermaid component source and all five reference Draw.io files.
  XML inspection included cells, styles, geometry, edges and embedded SVG content.
- Software Architecture Design `1.0.1`, its design considerations and scenario
  examples: architecture decisions remain upstream of diagram representation.
- Existing backend/frontend agent definitions were checked for diagram handoff
  context. Neither is changed; no `software-architect` definition is created.

Architecture Documentation authors Mermaid and native Draw.io XML through its
instructions and reference examples. Its scripts are a checker and an exporter,
not generators. Cloud icons are AWS4 stencils or SVGs embedded in XML; neutral
phone/laptop SVGs also live in those examples. There is no separate icon package
or Mermaid parser bundled with that Skill. Archify is a separate optional HTML
output path; it is outside the new Skill's Mermaid/Draw.io responsibility.

## Reuse decisions

| Existing resource/mechanism | Decision and reason |
| --- | --- |
| `architecture-documentation/references/drawio-xml.md` | Reuse by declared resource dependency. Preserve XML, editable objects, icon discovery, portability and boundary guidance. |
| `references/aws4-icons.md`, `references/azure-icons.md`, `references/google-cloud-icons.md` in that package | Reuse conditionally for the chosen provider. Do not copy or infer another provider's equivalent services. |
| `scripts/check_drawio.py` | Reuse unchanged. Add operational preflight and semantic checks in the new instructions because the checker is not a complete schema or notation validator. |
| `scripts/render_drawio.py` | Reuse unchanged, including sequential export and stop-after-failure behavior. No replacement renderer or automatic installation. |
| `examples/reference-application/component-diagram.mmd` and `.drawio` | Inspect for logical notation, colors, containers, actor/storage cues and edge conventions. Preserve supported source meaning rather than copy example technology. |
| Three provider reference diagrams | Reuse visual hierarchy, separate labels, icon geometry and applicable verified embedded resources. Example markup does not establish current provenance or glyph correctness. |
| `serverless-genai-agent.drawio` | Inspect as a denser AWS style reference and check with the existing validator. Do not make its topology a required template. |
| Architecture document template, full-package/default-AWS rules and Archify invocation | Do not reuse operationally: these belong to architecture documentation, not a selected diagram request. |
| Architecture connector house style | Retain for architecture views. Adapt for labeled sequence messages, ER cardinalities, process branches and data/event labels; document intentional warnings. |
| New automation | None. Existing artifact checks suffice with explicit additional review gates; a generic generator, duplicate validator or new dependency is unjustified here. |

The Draw.io resource dependency is `skill/architecture-documentation`; its root
must be resolved by declared name from the active catalog/checkout. No installed
sibling layout is assumed. Mermaid-only operation is independent. Missing required
Draw.io resources block that part, with independently selected Mermaid work still
possible. This is documented composition, not a new package manager or runtime.

## Delivered files

| File | Purpose |
| --- | --- |
| `skills/diagram-engineering/SKILL.md` | Canonical definition, inputs/outputs, guided selection, eight-stage workflow, icon rules, dependency, composition and quality gates |
| `skills/diagram-engineering/references/diagram-catalog.md` | All thirteen types, each with selection criteria, required information, visual conventions and representation rules |
| `skills/diagram-engineering/references/authoring-and-validation.md` | Common model, editable format rules, reused mechanisms/adaptations, commands and distinct validation levels |
| `skills/diagram-engineering/examples/usage.md` | Equivalent Spanish-first/English direct and agent handoff examples, prerequisites, review criteria and accurate execution status |
| `README.md` | Thirteen-Skill inventory, tree/catalog/guide links and installation example including the Draw.io resource dependency |
| `docs/diagram-engineering-validation.md` | This inspection and validation record |

All six files are intended for version control. No commit, staging, push,
installation, shared automation, agent, executable workflow or dependency change
was performed. Existing `.gitignore` rules were retained. Disposable synthetic
fixtures were placed under the already ignored root `examples/` for checks and
removed afterward; they are not installed examples or application deliverables.
An earlier Python-created scratch directory, whose first file write was denied,
could not be inspected or removed through PowerShell because of access controls.
It remains under the existing ignored `examples/diagrams/` path; no fixture was
successfully written into it. No ignore rule or filesystem permission was changed.

## Executed automated/static checks

Environment: Windows PowerShell, Python `3.13.2`, Node.js `24.20.0`.

| Check | Result and boundary |
| --- | --- |
| Skill identities and metadata | Passed: thirteen unique names discovered from `skills/*/SKILL.md`; new name/version and required sections present; no license field added. |
| Catalog coverage | Passed: exactly thirteen sequential entries with IDs present in the entry point; all have selection, required inputs, visual conventions and representation rules. This is instruction coverage, not thirteen rendered executions. |
| Links, bilingual structure and whitespace | Passed: new package links resolve; Spanish precedes English with both language anchors and required guide headings; new Markdown has no trailing whitespace. Guide semantic equivalence was also manually reviewed. |
| Reused resource closure | Passed: eleven explicitly required/conditional files resolve in Architecture Documentation; both reused scripts remain in their owner's package. |
| Preservation/scope | Passed: diff inspection confirms no changes to existing Skills, agents, contracts, root templates, validators or repository instructions; no new scripts, packages or runtime. |
| `git diff --check` | Passed for the tracked diff. New Markdown whitespace was checked separately before staging; Git's LF/CRLF notice is not a whitespace error. |

The inline checks used Python's standard library for identity/section/catalog/link
assertions, XML inspection and subprocess execution. No repository-wide validator
was implemented and no natural-language behavior was inferred from a regex check.

### Existing reference diagrams

Executed the existing checker with each file; provider diagrams used
`--require-provider-icons aws`, `azure` or `google` as appropriate:

```powershell
py -3 -B skills/architecture-documentation/scripts/check_drawio.py skills/architecture-documentation/examples/reference-application/component-diagram.drawio
py -3 -B skills/architecture-documentation/scripts/check_drawio.py --require-provider-icons aws skills/architecture-documentation/examples/reference-application/aws-infrastructure.drawio
py -3 -B skills/architecture-documentation/scripts/check_drawio.py --require-provider-icons azure skills/architecture-documentation/examples/reference-application/azure-infrastructure.drawio
py -3 -B skills/architecture-documentation/scripts/check_drawio.py --require-provider-icons google skills/architecture-documentation/examples/reference-application/google-cloud-infrastructure.drawio
py -3 -B skills/architecture-documentation/scripts/check_drawio.py --require-provider-icons aws skills/architecture-documentation/examples/reference-application/serverless-genai-agent.drawio
```

| Reference | Exit | Errors | Warnings |
| --- | --- | --- | --- |
| Component | 0 | 0 | 0 |
| AWS infrastructure | 0 | 0 | 0 |
| Azure infrastructure | 0 | 0 | 1 |
| Google Cloud infrastructure | 0 | 0 | 1 |
| Serverless GenAI AWS | 0 | 0 | 0 |

Both provider warnings state that embedded SVG markup is provider-neutral and
requires separate provenance/mapping verification. They are acknowledged, not
hidden or treated as visual evidence. No existing file was changed.

### Ten synthetic checker checks

A disposable XML fixture contained three pages with invented generic labels,
not an application model. `load_models` and `check_model` were loaded from the
unchanged checker using `runpy`; mutations were checked in memory. Its CLI was
also exercised on the three-page source, malformed XML and an empty `mxfile`.

| Case | Actual result |
| --- | --- |
| Component/actor/store page | 0 errors, 0 warnings |
| Sequence page, two labeled straight messages | 0 errors, 4 intentional architecture-style warnings: two labels and two non-orthogonal edges |
| ER page, numeric cardinality caption | 0 errors, 1 intentional edge-caption warning |
| Duplicate component ID mutation | Duplicate-ID error detected |
| Dangling target mutation | Missing-target error detected |
| Invalid embedded SVG root mutation | Invalid SVG-root error detected |
| Missing target attribute mutation | Warning only; gap confirmed and covered by mandatory preflight |
| CLI on three-page fixture | Exit 0; notation warnings retained |
| CLI on malformed XML | Exit 1; parse error rejected |
| CLI on empty `mxfile` | Exit 0; gap confirmed and covered by mandatory nonempty-model preflight |

All ten expectations passed. These check resource reuse and warning handling;
the sequence/ER pages are minimal checker fixtures, not full notation templates
or examples of finished visual quality. An editor, renderer and semantic review
remain distinct checks. Initial attempts to write disposable fixtures through
Python were denied by the environment; fixtures were prepared with the available
file-editing tool before running the successful checks.

### Parser, editor and visual checks

Mermaid package import resolution, `mmdc` discovery and global npm inventory did
not expose an available Mermaid parser/CLI in this session. Mermaid syntax
execution and Mermaid rendering: **not run**. Conservative grammar guidance was
manually compared with the official Mermaid documentation linked from the new
authoring reference. No package/browser download was performed.

Draw.io executable discovery found a Desktop installation outside `PATH`.
Exactly one preview attempt used the unchanged exporter on the synthetic file:

```powershell
py -3 -B skills/architecture-documentation/scripts/render_drawio.py preview examples/diagrams/diagram-engineering-validation/synthetic-notations.drawio examples/diagrams/diagram-engineering-validation/preview.png
```

Export **failed**, exit `1`, before producing a preview. Electron reported that
Windows sandbox access to `C:\Program Files\draw.io` was denied by its ACL because
the required application-package access entry was absent. No automatic retry,
ACL change, elevated launch or alternative exporter was attempted. This is an
environment failure, not an XML validation failure. No successful editor import,
rendered icon verification or visual inspection is claimed.

## Manual instruction walkthroughs

These are reviews of written behavior, not independent Skill/agent executions.

| Supplied situation | Instruction path reviewed |
| --- | --- |
| “Make diagrams”, no selection | Analyze context, recommend by category, request types/formats, wait; no automatic thirteen-view generation. |
| Types and both formats supplied | Skip recommendation/selection; create one model per view, produce both representations. |
| Type supplied, format absent | Ask only for the format. |
| Existing diagram layout improvement | Infer its type/format, preserve IDs/meaning and unrelated pages. |
| Agent/workflow supplies complete selection | Execute without asking again; return artifacts, inventory and actual checks. |
| Mermaid-only, resource dependency absent | Proceed; no assumed sibling resources. |
| Draw.io selected, dependency absent | Report affected work blocked, do not invent resource locations or duplicate the validator. |
| Icons unsupported in Mermaid | Use compatible symbols/labels/styles; no unverified icon syntax or CSS dependency. |
| Provider unspecified | Preserve provider-neutral/unknown scope; no implicit AWS design. |
| Sequence/ER house-style warnings | Keep required notation; inspect and document intentional warnings. |
| Unknown ER cardinality | Do not invent multiplicity; list the unresolved relation visibly in both formats. |
| Renderer fails | Stop exports, retain editable source, report rendering/visual checks unavailable. |

The thirteen catalog entries were manually reviewed for separate abstraction,
source needs and meaning in both formats. Direct usage and agent handoff prompts
remain illustrative. No real application diagram, full thirteen-type execution,
host registration or installed-package integration test was performed. Visual
quality requirements are defined and testable; visual parity with Architecture
Documentation has not been observed in a working renderer in this environment.

## Revision 1.1.0: local scripts, four providers and one-attempt rendering

The user requested independent packaging, collision scripts, AWS/Azure/Google/IBM
coverage and no second attempt when Draw.io or Mermaid cannot open. This explicitly
authorizes incorporating resources into the new package, replacing the earlier
cross-Skill dependency choice. Version `1.1.0` reflects compatible capability and
packaging additions; the thirteen selected-view types remain unchanged.

### Changes and scope

- Local `check_drawio.py` and `render_drawio.py` originate from Architecture
  Documentation `1.8.13`. The original Skill remains unchanged.
- The checker now rejects empty models, invalid base cells, parent cycles,
  invalid geometry and missing/nonvertex endpoints; fixes nested/relative
  geometry; checks native component collisions and parent containment in addition
  to inherited icon/text heuristics; and rejects external/active SVG resources.
- Provider enforcement covers AWS, Azure, Google and IBM. Embedded SVGs require
  an inventory mapping page/cell/provider/source, so a generic client-device SVG
  cannot fulfill a cloud-icon requirement. Inventory declarations and native
  prefixes still do not prove vendor authenticity or rendered glyph appearance.
- `render_diagram.mjs` uses Node.js built-ins to guard both renderers with a single
  task-wide attempt record. A file is attempted once; any failure/interruption
  blocks subsequent launches of that renderer, including other files. There is
  no fallback executable, browser download or automatic retry. The other renderer
  may have its own attempt. A previous failure in the same task is not retried.
- Four provider references, the XML guide, the logical source pair and three
  provider Draw.io files were incorporated as local instructional resources.
  The AWS copy had three component/icon/label collisions under the stronger
  checker; repositioning four service cards and one label removed them without
  changing nodes, edges or semantics. The source example was not modified.
- IBM guidance was added from IBM's official architecture-diagram documentation
  and public architecture-icons repository. No IBM icon pack or rendered IBM
  example is claimed. Native-library availability and per-service mapping must
  be verified in the destination environment.
- Entry point, bilingual guide and root catalog/install instructions now describe
  independent installation. Python adapts the existing XML/export mechanisms;
  new orchestration uses Node.js. No npm/pip dependency, new agent, workflow,
  repository CLI or installation was added.

See the package's `references/reuse-provenance.md` for source paths, adaptations
and maintenance boundaries. New local scripts, focused tests, references and
style fixtures are intended for version control; render receipts/previews remain
disposable task artifacts. Existing ignore rules were not broadened.

### Executed checks

```powershell
py -3 -B -m unittest discover -s skills/diagram-engineering/scripts/tests -p test_check_drawio.py -v
node --test --test-isolation=none skills/diagram-engineering/scripts/tests/render_diagram.test.mjs
py -3 -B skills/diagram-engineering/scripts/check_drawio.py skills/diagram-engineering/examples/reference-diagrams/component-diagram.drawio skills/diagram-engineering/examples/reference-diagrams/aws-infrastructure.drawio skills/diagram-engineering/examples/reference-diagrams/azure-infrastructure.drawio skills/diagram-engineering/examples/reference-diagrams/google-cloud-infrastructure.drawio
```

- **23 Python tests passed**, covering structure, cycles, endpoints, component/icon
  collisions, containment, nested/relative geometry, SVG encodings/resources and
  provider inventories for all four vendors. IBM markup tests deliberately use
  synthetic identifiers and do not establish availability of a real stencil.
- **8 Node.js tests passed**, covering failed-process suppression, one attempt per
  file, missing Mermaid CLI, interrupted/corrupt records, missing preview output
  and independent renderer failure states. Process results/previews were injected;
  these tests launch neither real diagram renderer.
- The default Node test runner initially failed to spawn a test subprocess
  (`EPERM`). Running its tests in-process passed; this was a test-harness change,
  not a retry of Draw.io or Mermaid. The documented direct `node <test-file>`
  command likewise runs the test module without the extra test process.
- All four packaged reference Draw.io files passed the local checker with **zero
  errors**. Each provider example emitted one expected warning that SVG markup
  alone cannot prove its provider; no visual or provenance pass is inferred.
  These baseline commands check structure/collisions without provider enforcement;
  per-provider inventory logic was exercised separately by the focused tests.
- A standalone temporary copy of only `diagram-engineering` passed its logical
  reference checker and Node script syntax check from outside the repository,
  with no sibling Skill installed. All 68 local Markdown links resolved and
  the 41 tracked original files checked remained unchanged.

No additional Draw.io launch was made after the earlier Electron access failure.
No real Mermaid renderer was launched or installed. Successful editor import,
rendered icon mapping, Mermaid syntax execution and visual inspection remain
**not run**. Static checks and passing unit tests cannot establish visual parity.

## Revision 2.0.0: Python utilities only; preserve Architecture Documentation

The user requested removing the JavaScript helper and asked whether the stable
Architecture Documentation Skill should be changed. Its existing behavior is
preserved; this revision changes only Diagram Engineering, its catalog description
and validation record. No integration or resource migration into the stable Skill
was performed. The existing local serverless reference diagram is preserved too.

`scripts/render_diagram.py` replaces the former JavaScript helper. Its tests are
now `scripts/tests/test_render_diagram.py`; both previous `.mjs` files were deleted.
All packaged utilities/tests use Python 3.10+ and the standard library. The
version increments to `2.0.0` because the documented helper entry point/command
changes; the diagram types, formats, icon policy and selected-view contract remain.

The Python guard preserves version-1 attempt records, per-file limits, cross-file
failure suppression, independent renderer states, interrupted-record/lock handling
and fresh preview requirements. It invokes the Draw.io backend with the current
Python interpreter. External Mermaid CLI remains an optional installed renderer
with its own Node.js requirement; Python reads its package manifest without
launching npm/Node for discovery. It does not replace the Mermaid parser or claim
that Python alone renders Mermaid. No dependency was installed.

Executed:

```powershell
py -3 -B -m unittest discover -s skills/diagram-engineering/scripts/tests -p 'test_*.py' -v
git diff --check
```

**36 Python tests passed**: 23 checker tests and 13 render-guard tests. The latter
cover the previous failure/receipt cases plus Node-free Draw.io orchestration,
external Mermaid runtime requirements, manifest discovery, active locks and
preservation of existing previews. Renderer execution and preview content were
simulated; neither renderer nor Node was launched by these tests. No additional
Draw.io attempt was made after its previously recorded environment failure.

The Python helper's `--help` and isolated-package smoke check are read-only
operations; they do not open an editor. Current local links/commands, the bilingual
guide, version and the absence of packaged `.mjs` files were reviewed. The source
Architecture Documentation package was compared with its tracked baseline and
remained unchanged. All revised source, tests and documentation are intended to
remain versionable; no ignore-rule change, installation, staging or commit occurred.

## Regenerated regression tests — 2026-11-16

The user requested regeneration after removing `scripts/tests/`. The replacement
suite was authored against the current Python scripts; it is not a byte-for-byte
recovery of the deleted files. It contains `test_check_drawio.py`,
`test_render_diagram.py` and a local `_support.py` fixture helper.

Executed:

```powershell
py -3 -B -m unittest discover -s skills/diagram-engineering/scripts/tests -p 'test_*.py' -v
py -3 -B validators/validate_components.py
git diff --check
```

Results: **36 tests passed**: 23 Draw.io checker tests and 13 render-guard tests,
including malformed-input subcases. Coverage includes compressed/native models,
hierarchy and endpoint errors, nonfinite geometry, nested/relative coordinates,
collisions and containment, SVG resource safety, four-provider markup and inventory
resolution, per-file limits, renderer failure isolation, interrupted/locked records,
preview preservation, Mermaid manifest discovery and runtime requirements.

All process launches are mocked or replaced with a synthetic preview writer.
Draw.io, Mermaid and Node were not launched; these tests do not establish visual
correctness, icon provenance or real renderer availability. Fixtures inherit the
workspace ACL, stay within the test directory and are deleted after each test;
cleanup checks the resolved absolute parent before recursive removal. No runtime
dependency or ignore rule was added.

Shared structural validation passed with 13 Skills, 2 agents and 1 workflow,
zero errors and zero warnings. SHA-256 comparisons confirmed that `SKILL.md` and
all three production scripts were unchanged. New test files were checked for
trailing whitespace and final newlines. Skill version `2.0.0` is retained because
this task restores regression coverage without changing instructions or behavior.
