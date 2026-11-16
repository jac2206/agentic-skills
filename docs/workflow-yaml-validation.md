# YAML Workflow Change Validation

Date: 2026-11-16. Scope: declarative workflow profile `2.0`, authoring template,
one draft reference and repository documentation. This record concerns static
inspection; neither referenced Skill nor the workflow was executed.

## Decisions and compatibility

- Canonical workflow entry point: `workflows/<name>/workflow.yaml`. The previous
  `WORKFLOW.md` convention had no packages to migrate. The breaking representation
  change uses workflow profile `2.0`; agent profile `1.0` remains supported.
- The reference coordinates architecture analysis and security analysis. Two
  existing Skills retain their procedures; no new agent or Skill is required.
- `needs` owns ordering; named source references own data handoffs. Missing or
  failed required work blocks dependent completion without implicit retries.
- YAML is portable authoring data. There is no executor, host binding, CLI,
  framework configuration or automatic installation.
- Shared validator implementation and routing metadata remain deferred. This
  change adds no dependencies and does not modify Skill or agent packages.

## Performed checks

| Check | Method | Result |
| --- | --- | --- |
| YAML structure | One-off read-only Python inspection using already available PyYAML 6.0.2, without installation; reject duplicate/non-string mapping keys, tags, anchors and aliases | Passed: reference and authoring template parse; required field shapes and quoted versions match profile 2.0 |
| Discovery and identity | Inspect only `skills/*/SKILL.md`, `agents/*/AGENT.md` and `workflows/*/workflow.yaml`; resolve declared names, not assumed directories | Passed: 13 Skills, 2 agents and 1 draft workflow; unique identities; template excluded |
| Existing guide convention | Inspect canonical Skill packages for Spanish-first and English usage sections | Passed: all 13 packages have both sections in the expected order |
| Required dependencies | Resolve typed names against the canonical inventory and inspect the required component graph | Passed: both workflow dependencies resolve; no missing references or cycles |
| Step graph and mappings | Inspect unique IDs, predecessors, cycles, declared inputs/outputs, ancestor reachability and final source formats | Passed: 2 steps; architecture output reaches security review; both final outputs resolve |
| Template consistency | Compare required document/step shapes with the reference; exempt template placeholders from live dependency resolution | Passed: same profile and shapes; scaffold remains authoring material |
| Semantic review | Compare mappings, modes and authority with both canonical Skill definitions | Passed: Analyze modes accept scoped context; Markdown architecture context supports security analysis; constraints preserve read-only scope |
| Documentation | Inspect local Markdown link file targets and review current entry-point references | Passed after updating the historical template link to its successor; historical counts and results retained |
| Scope and whitespace | `git diff --check`, path review and separate new-file inspection | Passed: no Skill/agent package edits, runtime implementation or dependency installation; no whitespace errors |

The Python inspection ran from standard input with `py -3 -B -`; it did not add
a checker script, write bytecode or execute project code. PyYAML was an existing
inspection tool, not a newly added repository dependency. Local Markdown file
targets were checked automatically; anchor targets and semantic claims were
reviewed only where affected by this change.

## Not run and next acceptance gate

No host execution, native workflow discovery, installation, network checks or
Skill functional tests were performed. No shared validator is delivered, and
static inspection does not establish runtime correctness or security assurance.

Before changing the workflow from `draft` to `ready`, authorize a bounded host
pilot and record success, missing input, unavailable Skill and failed/blocked
predecessor cases. Confirm that scope, authority, source mappings, partial results
and final reporting survive actual interpretation. Build an executor or adapter
only if those pilots establish a concrete need.
