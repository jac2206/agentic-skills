# Component Validation

This directory owns cross-component review rules. There is no repository-wide
validator executable in this phase. Apply the checklist manually with available
file, search and version-control tools; do not present this document as an
automated check or as evidence that a component was executed.

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

Check requirements at the relevant scale: agent/workflow checks are not applicable
to an architecture phase containing only guides and templates. A schema or static
checker cannot establish that natural-language instructions will behave correctly.

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

The current phase's evidence is in
[architecture validation](../docs/architecture-validation.md).

## Future automation boundary

When separately authorized, place small shared static validators here and document
their supported contract version, invocation, inputs, scope and findings. Keep
focused valid/invalid fixtures with the validator. Return nonzero on structural
errors, distinguish warnings, and avoid writes, network access, dependency
installation or component execution during validation.

Automate identity, required fields, reference resolution, cycles, local resources
and template exclusions before considering catalog generation. Test the existing
Skill profile, including the `html-presentations` directory/name difference.
Choose tooling from actual consumer needs; no runtime is selected now.
