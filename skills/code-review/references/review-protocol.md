# Review Protocol

Read before evidence collection. This is review guidance, not a universal checklist
that asserts every project uses the same patterns.

## Evidence and modes

Use local read-only Git with `GIT_OPTIONAL_LOCKS=0`, external diff/textconv disabled,
literal pathspecs and NUL-delimited status/path lists. Never run hooks or fetch to
resolve a missing base. Record unavailable refs and stop only PR comparison.

Quick: `status --porcelain=v1 -z --untracked-files=all` describes index/worktree
separately. Collect `diff --cached` and `diff` independently; untracked content
needs explicit safe reading. Renames carry previous and current names. Deletions
have old-side lines. Conflicts are disclosed and excluded from ordinary diffs.
Do not sum overlapping layers as unique source lines; Git statistics are per layer.
An unborn repository has no HEAD and still supports staged/untracked review.

PR: verify local base and head commits, use `merge-base base head`, then compare
merge-base to head and enumerate `merge-base..head` commits. Fail on multiple
merge bases rather than silently choosing one. Record branch, requested base,
resolved SHAs and local dirty status. Do not mix uncommitted changes into the PR
snapshot. Head defaults to HEAD, but may be specified; detached HEAD is explicit.

Full: list tracked/nonignored files (or inspect explicit paths in a non-Git folder),
then review declared modules. Bound file counts and bytes; declare truncation and
excluded files. A source snapshot is labeled as such, never as added code. Existing
debt remains `existing` only with provenance; without history use `unknown`. Recent
introduction requires a separately evidenced historical comparison.

Before collection inspect project-specific sensitive/generated/vendor paths and
pass additional exclusions to the collector. Default exclusions are conservative,
not exhaustive. Never follow symlinks into external folders, traverse submodules,
read ignored files automatically or print a secret to establish it exists. A
redacted location and safe explanation suffice. Recheck the snapshot after the
review; content changes invalidate line mappings and decisions.

## Context and evaluation prompts

Derive small, independently assessable rules with positive/negative evidence
criteria from instructions, specs and actual configurations. Identify rule source
and scope before assigning pass/fail; do not split passes to inflate a score.

| Dimension | Conditional prompts and evidence |
| --- | --- |
| architecture | Responsibilities, coupling/cohesion, layer dependency directions, established SOLID/Clean/hexagonal/DDD/pattern decisions; trace imports and actual call paths rather than judging folder names. |
| quality | DRY/KISS, readability, complexity, dead/duplicated code, errors, validation, typing/contracts, names and class/function responsibility. Avoid subjective style findings already covered by formatter rules. |
| security | Applicable OWASP authentication/authorization, injection, sensitive data, embedded secrets, input boundaries, configuration and dependency risks. Cite verified advisories and affected versions; do not equate a package name with a vulnerability. Use the security Skill when available. |
| testing | Relevant positive/negative/edge/regression tests, isolation/mocks, integration boundaries and consistency with project tools. Distinguish presence, quality and actual execution. Report measured coverage only with tool output and scope. |
| standards | Applicable AGENTS/specs/API contracts, architecture conventions, lint/formatter/type settings, testing patterns and Git rules. A config's existence is not proof the change passes it. |
| performance | Query plans/N+1, blocking work, unnecessary processing, resources, concurrency and measured bottlenecks. Explain the code path and workload preconditions; do not invent latency or benchmark claims. |

Read-only review does not authorize arbitrary test/lint scripts: they may write
caches, run formatters, access services or run hooks. Inspect executable content,
configuration and environment; if effects cannot be bounded, mark `not run` and
recommend a separately authorized check. Record command, scope, exit status,
redacted output summary and structural/functional/visual check type.

Severity: Critical = evidenced catastrophic compromise/data loss or similarly
urgent project-defined blocker; High = significant exploitability or core behavior
failure; Medium = material bounded defect; Low = limited-impact defect;
Suggestion = optional improvement. Explain impact, likelihood/preconditions and
mitigations. `potential` is uncertainty, not confirmation, regardless of severity.
Keep unsupported suspicions out of failed rules. Use `unverified` until evidence
supports pass/fail. Root-cause duplicates share one finding with related evidence.

## Commit Advisor

Use the project's explicit conventions first. Conventional Commits 1.0.0 is the
fallback reference: [official specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).
It defines a type, optional scope/`!`, description and optional body/footers. `feat`
and `fix` describe features and bug fixes; other project-approved types are allowed.
Breaking behavior needs the project's breaking marker and explanatory evidence.
The fallback syntax helper checks structure only; it is not Commitlint or proof
that the selected type accurately describes the change.

Inspect config files statically, including `.commitlintrc*`,
`commitlint.config.*`, package `commitlint`, `.husky/`, `core.hooksPath` and
`commit-msg`. Do not execute JavaScript configs/plugins automatically. Inspect
actual installed tool/version first. If safe and available, validate the proposed
message through the installed Commitlint API or trusted executable using stdin,
without npx downloads, Git writes or hook invocation. Capture real exit/output
evidence. Otherwise use `not run` with reason; finding a config is not compatibility.

Derive a group per independent intent with `type`, `scope`, `description`, optional
`body`, `footer`, full `message`, `include`, `exclude`, `rationale`, shell identity
and explicit commands. List sensitive/unrelated files to exclude with reasons;
write every proposed commit message (description, body and footer) in English,
independently of the chosen report language. Explain advice in the chosen language;
never translate actual historical commit messages or source evidence.
include both old and new paths for renames and deleted paths where appropriate.
Review staged content against each group; staging only some paths does not unstage
other staged work. Warn the user to inspect the index before committing. Do not
suggest automatic reset, broad staging, history rewriting or bypassing hooks.

The helper emits manual `git --literal-pathspecs add -- <quoted paths>`,
`git diff --cached --check`, `git diff --cached --stat` and `git commit -m ...`
for a selected shell. Commands are inert report text and must never be executed
by this Skill. If paths contain newlines/control characters, refuse command
generation and explain manual handling. Commit messages and shell metacharacters
must be quoted for the declared shell. Never infer that accepted findings, a high
score or a copied command authorizes a commit.

## Report presentation

JAC dark/light semantic colors, type stacks and spacing were adapted from
`skill/ui-ux-design-system` during authoring, specifically its palette, brand/UI
guidance and v4 catalog. A small owner-local CSS projection keeps the installed
package independent. Use local font fallbacks instead of the catalog's remote
font imports. Warning/focus/diff roles are documented derived roles. No logo
asset is needed or recreated. Target WCAG 2.2 AA; actual checks are listed in the
validation record, not a blanket conformance claim.

The dense file browser and diff workspace support review; the executive overview
precedes details. Severity always has a text label; controls have names and focus
states. Mobile defaults to unified diff; split view remains scrollable. User data
must enter the DOM as text. No external navigation, HTML from source, eval, Git
execution, source writes or automatic network access is permitted. Downloads are
explicit local exports. A VS Code preview's clipboard/download restrictions may
require the visible copy fallback and a local browser.
