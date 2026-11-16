# Component Validator Validation

Date: 2026-11-16. Scope: shared structural validator, regression tests and current
repository documentation. This task authorizes static automation, not component
execution or a distribution CLI.

## Implementation and dependency boundary

The validator reads canonical Skill metadata, agent profile `1.0` and workflow
profile `2.0`. Required component references and workflow step graphs are checked
separately. Skill prose is not converted into required dependencies.

Python tooling uses PyYAML `6.0.2`, already available during this task and recorded
in `validators/requirements.txt`. No package installation was performed. This is
an explicit validator-only dependency, not a dependency of installed components.
The checker performs no writes, network calls, dependency installation or component
execution. Its default root is derived from the script location.

Skill and usage templates remain canonical under `skills/skill-factory/templates/`.
The root README links to them. No copies were added under root `templates/`:
installing Skill Factory must include its templates, and duplicate sources would
create maintenance drift. Existing Skill and agent packages were not edited.

## Executed checks

| Check | Command or method | Result |
| --- | --- | --- |
| Repository structure | `py -3 -B validators/validate_components.py` | Passed: 13 Skills, 2 agents, 1 workflow; zero errors and zero warnings |
| Regression suite | `py -3 -B -m unittest discover -s validators/tests -v` | Passed: 20 test methods, including malformed-input subcases |
| Discovery and profiles | Isolated package tests | Passed: declared Skill name can differ from directory; nested templates and hidden packages are excluded; legacy workflow entry points are reported |
| Graphs and mappings | Valid and invalid dependency/step fixtures, including a 2,000-node DAG | Passed: missing nodes, cycles, self edges, unreachable or absent outputs and incompatible final format labels are detected |
| YAML and malformed data | Duplicate keys, aliases, anchors, tags, multiple documents, syntax errors and wrong field types | Passed: rejected without executing payloads; explicit YAML 1.2 boolean spellings remain distinguished from yes/no strings |
| Packaging and usage | Missing resources, external package links, language headings/navigation and template payload tests | Passed: package-local missing links are errors; external links are warnings; output-relative template links are not mistaken for installed resources |
| Read-only behavior | Compare every file's path and bytes in an isolated fixture before and after validation | Passed: no additions or content changes |
| Workflow scaffold | Valid/invalid template test with unresolved placeholder capability | Passed: structure is checked, placeholder dependencies are exempt from live resolution and the template is not cataloged |
| Exit behavior | Exercise successful validation, invalid components, invalid root and missing parser | Passed: exit codes 0, 1 and 2 as documented |
| Source hygiene | `git diff --check`, new-file whitespace inspection and path review | Passed: no Skill/agent package changes or component execution |

An initial run found output-relative links inside existing backlog templates.
The checker was corrected to inspect links to templates without interpreting
their payload links as package resources; no Skill was changed to satisfy the
checker. Initial fixture runs also exposed restrictive Windows ACLs on Python
temporary directories. Fixtures now inherit the test workspace ACL and use an
explicitly checked cleanup boundary; failed workspace fixtures were removed.

## Limits

Tests ran with Python `3.13.2` and PyYAML `6.0.2` on Windows. Other operating
systems and Python versions were not exercised. The checker is structural:
semantic compatibility, equivalent translations, agent prose requirements,
permissions and evidence supporting `ready` still require review. Markdown checks
cover inline file links, not a complete Markdown syntax or all anchors.

The workflow remains `draft`. No Skill, agent or workflow functional execution,
host integration, installer, CLI, extension or web interface was tested or added.
Historical architecture and YAML records describe their original snapshots; this
record documents the later shared-automation change.
