# Component Validation

This directory owns cross-component static checks and the remaining manual review
checklist. [validate_components.py](validate_components.py) reads definitions and
reports structural findings without writing files, accessing the network,
installing dependencies or executing components.

## Run the validator

Use Python 3.10 or newer and PyYAML from [requirements.txt](requirements.txt).
This is a validator-only tooling dependency; component installation and execution
do not require it. No dependency installation happens automatically. If needed,
install it in your chosen tooling environment:

```sh
py -3 -m pip install -r validators/requirements.txt
```

From the repository root on Windows:

```sh
py -3 -B validators/validate_components.py
py -3 -B -m unittest discover -s validators/tests -v
```

On other systems, replace `py -3` with `python3`. The optional positional argument
selects a repository root; otherwise the validator uses its own repository,
independent of the working directory. Exit codes: `0` means no structural errors
(warnings may remain), `1` means invalid components, and `2` means an invalid root
or unavailable tooling. Paths and findings appear in the console.

## Automated scope and limits

- Discover only direct `skills/*/SKILL.md`, `agents/*/AGENT.md` and
  `workflows/*/workflow.yaml` packages, excluding hidden package directories.
  Reject legacy `WORKFLOW.md` entries rather than silently skipping them.
- Preserve the existing Skill profile and directory/name differences, including
  `skills/presentations/` declaring `html-presentations`. Validate name,
  description and version when declared. Do not infer Skill dependencies from prose.
- Check the seven common agent fields under profile `1.0`, workflow fields under
  profile `2.0`, duplicate identities, required reference resolution and cycles.
- Parse YAML safely and reject duplicate/non-string keys, tags, anchors, aliases
  and multiple documents. Use explicit `true`/`false` booleans; quote strings that
  YAML might otherwise interpret as numbers, dates or null values. This parser
  supports the authoring subset, not every YAML 1.2 feature.
- Check workflow step IDs, predecessors, failure policy, declared sources,
  ancestor reachability and final output format labels. Check the workflow
  authoring template's shape when present, without resolving its placeholders
  as installed components.
- Require each Skill's usage guide, Spanish-first and English headings, and
  Markdown language navigation. Translation equivalence and guide completeness
  still need human review.
- Check inline Markdown file links in component definitions, references and
  guides. Skip fenced examples, inline code and template payload links, which may
  address future generated outputs. Links to template files are still checked.
  Report links leaving a package as portability warnings; do not assume they are
  required or follow them into another package. This is not a complete Markdown
  parser; reference-style links, HTML links and fragment targets need manual review.

Passing cannot establish natural-language correctness, declared language, required
references hidden in agent prose, authority enforcement, input/output semantic
compatibility or evidence supporting `ready`. It does not verify the root catalog
or replace functional tests. Keep those checks in the manual review below.

## Review checklist

| Check | Method | Failure condition |
| --- | --- | --- |
| Scope | Inspect changed/new paths and diff | Unrequested runtime, CLI, dependencies, functional agents or executable workflows |
| Skill preservation | Compare paths, frontmatter and full resource contents against baseline | An unrequested change to an existing Skill or supporting resource |
| Discovery boundary | Inspect canonical entry-point paths | Templates, READMEs, examples or hidden files treated as components |
| Identity | Read frontmatter under the applicable profile | Duplicate kind/name, invalid new name, or new agent/workflow directory mismatch |
| Metadata | Apply the common and type-specific contracts | Missing/wrong field, unsupported contract version, or forced new fields on existing Skills |
| Dependencies | Resolve each required kind/name from actual definitions | Missing, ambiguous, wrong-kind, self or cyclic reference |
| Resource closure | Inspect local links and required component references | Required resource outside the package without a declared component dependency |
| Composition | Compare capability/step descriptions with owning Skill | Duplicated operational instructions or assumed unavailable capabilities |
| Agent authority | Review declared effects, tool needs and handoffs | Unbounded delegation, implicit privilege increase or absent failure behavior |
| Workflow graph | Check IDs, predecessors and named input/output mappings | Duplicate/missing IDs, cycles, unavailable outputs or incompatible formats |
| Documentation | Check local links, tree, catalog and status claims | Broken new link, misleading inventory or unsupported execution/compatibility claim |
| Template consistency | Compare placeholders and sections with contracts | Template omits required content or is counted as a live component |

Apply checks at the relevant scale. The script automates structural checks only;
the checklist also covers semantic and change-specific review.

## Workflow profile 2.0 checks

For `workflows/<name>/workflow.yaml`, parse the document with an available YAML
parser; text matching alone does not validate YAML. Check the required shapes in
[the workflow contract](../contracts/workflows.md), supported version, duplicate
keys, prohibited YAML features and dependency resolution from canonical names.
Check the component dependency graph separately from the workflow's step graph.

For each step, verify unique IDs, existing predecessors, acyclicity and that every
source mapping names a declared input or a reachable predecessor output. Final
outputs must resolve to declared step outputs. Confirm `uses` matches declared
dependencies and inspect data meaning and format compatibility manually. Parse
the authoring template too, but exclude its placeholders from component discovery.

The draft [reference workflow](../workflows/architecture-security-review/workflow.yaml)
is an inspection example, not evidence of a successful host run. Missing-input,
unavailable-Skill and blocked-predecessor behavior still needs a later authorized
host pilot. See [the YAML change record](../docs/workflow-yaml-validation.md) for
static checks actually performed.

## Existing Skill-owned checks

Keep artifact validation with its owner. The architecture documentation Skill
contains `scripts/check_drawio.py` and an optional renderer; the application
security review Skill contains `scripts/render_report.py` with input checking.
These validate their own artifact formats, not repository component contracts.
Do not move, duplicate, or run them merely to validate this architecture change.

## Reporting evidence

For each applicable check, record scope, method or exact command, result, findings
and limitations. Use `passed`, `failed`, `not run`, or `not applicable`. Distinguish
manual review, automated static inspection and functional execution. A missing
required check cannot be reported as passed. `git diff --check` covers tracked
diff whitespace; inspect newly created files separately before they are staged.

The initial architecture snapshot is in
[architecture validation](../docs/architecture-validation.md). Shared validator
execution results are in [validator validation](../docs/component-validator-validation.md).

## Automation boundary

Regression tests live under [tests/](tests/) and create isolated miniature
repositories inside that directory, then remove them. They exercise valid and
invalid packages, including the directory/name difference, source reachability,
cycles and template payload links. They do not run agents, Skills or workflows.
Use `-B` to avoid bytecode caches. Do not broaden validation into installation,
runtime execution, a generated registry or a host adapter without authorization.
