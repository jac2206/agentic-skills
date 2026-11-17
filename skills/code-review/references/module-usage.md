# Module Usage

These are imported Node.js functions, not a CLI, server or automatic reviewer.
Resolve module paths relative to the installed `SKILL.md`. Examples below assume
the library root as the current directory; replace paths for another installation.
Node.js 20+ and Git are needed for collection. No dependencies are installed.

## Collect and assess

Use a host JavaScript tool or an ephemeral Node module outside the analyzed project:

```js
import { collectReview } from './skills/code-review/scripts/collect.mjs';
const quick = collectReview({ root: '/absolute/backend', mode: 'quick' });
const pr = collectReview({ root: '/absolute/backend', mode: 'pr', base: 'release/next' });
const full = collectReview({ root: '/absolute/backend', mode: 'full', modules: ['src/billing'] });
```

These are independent examples; select only the requested mode. `head` defaults
to HEAD. Optional `exclude` is a list of repository-relative path prefixes,
`maxFiles` defaults to 500 and `maxBytes` to 200000 per source/diff. Additional
project-specific sensitive paths must be excluded before collection. Large omitted
content is not reviewed; split into bounded modules and disclose remaining scope.
Full collection uses tracked/nonignored files, including relevant untracked ones;
it does not traverse ignored files, external links or submodules automatically.

Git commands use no shell, optional locks disabled, external diff/textconv disabled,
fsmonitor disabled, configured clean/process filters disabled and lazy fetch disabled.
Partial/promisor clones are refused before object access, including on older Git
versions that do not honor the no-lazy-fetch environment flag. Use complete local
evidence or perform an explicit bounded manual review without fetching.
No hooks, application code or remote services are intentionally invoked. Limit
failures are explicit omissions, not clean results. PR with unresolved/invalid refs,
multiple merge bases or changed status/HEAD during collection fails. Failed calls
throw; do not reinterpret them as a successful empty review.

Collection does not inspect project standards or create findings. Read context,
evaluate actual source and construct an assessment using the
[data contract](data-contract.md). Mark only evaluated files `reviewed: true`.
The next shape shows wiring, not sample findings or a ready-to-score assessment:

```js
import { validateReview, calculateScore } from './skills/code-review/scripts/model.mjs';
import { writeReport } from './skills/code-review/scripts/report.mjs';

const assessment = {
  schemaVersion: '1.0',
  snapshot: quick,
  context: { standards: observedStandardReferences, description: observedProjectContext },
  summary: observedSummary,
  rules: evaluatedRules,
  findings: verifiedFindings,
  validations: actualValidationResults,
  strengths: evidencedStrengths,
  limitations: actualLimitations,
  nextSteps: recommendedNextSteps,
  commitAdvisor: actualCommitAdvice
};
validateReview(assessment);
const score = calculateScore(assessment.rules, assessment.scorePolicy);
const output = writeReport(assessment); // HTML only by default
// Optional: writeReport(assessment, { json: true, markdown: true });
console.log(output); // Exact temporary directory, report path and review ID
```

All undeclared names above are reviewer-supplied evidence, never generated defaults.
Keep canonical input in host context or a private temporary file, not the target.
`renderHtml`/`renderMarkdown` return strings without writing; `prepareReport`
validates/redacts and derives score/status. Redaction is conservative and incomplete
by nature: inspect the whole assessment before writing, including comments, source,
paths, commit messages and tool outputs. Never pass complete known secrets simply
to test whether a heuristic removes them.

## Inspect and return decisions

Open `output.report` in a trusted VS Code HTML preview or local browser. A preview
may block scripts/clipboard/downloads; prefer a local browser if needed. The HTML
uses no network and has no direct Codex event channel. Browser state lives only in
memory, so copy/export decisions before refresh/close. Rejection requires a reason;
acceptance/defer may include one. Copy exports all finding decisions and identities.

```js
import { importDecisions } from './skills/code-review/scripts/model.mjs';
const checked = importDecisions(assessment, userSuppliedParsedJson);
```

Reject stale/foreign payloads, missing/duplicate IDs and mismatched files. Even a
valid payload authorizes no changes. A downstream authorized task must confirm the
current snapshot still matches and decide its own implementation permissions.

For installed Commitlint, `checkCommitlint` in `model.mjs` accepts `message`, an
already inspected `lint` API function, resolved `config`, `toolEvidence` and
`configEvidence`. It forwards rules, parser options, plugins, ignores and default
ignore policy according to the [official API](https://commitlint.js.org/api/lint.html).
It never loads executable project configuration itself. Missing tools/config or API
errors return `not run`; actual returned validation determines passed/failed and
preserves warnings/errors. An API-contract spy in tests proves forwarding/error
handling only, not installed Commitlint compatibility. Validate each proposed
message with actual project evidence when the required tools are safely available.

## Cleanup

The writer creates `<os.tmpdir()>/agentic-code-review/<review-id>-<unique>/` with
exclusive files and an ownership marker. It refuses a temp location inside the
analyzed target. Repeated generation creates another directory; it never overwrites
a report. No `.gitignore` change is needed. Reports are sensitive local artifacts;
portable permissions are requested, but OS ACLs and temporary storage policy still
apply. There is no automatic retention timer or VS Code close detection.

```js
import { cleanupReview } from './skills/code-review/scripts/report.mjs';
// Call only after the user explicitly confirms this specific review is finished.
const result = cleanupReview({ ...output, confirmed: true });
console.log(result); // deleted absolute path, verified: true
```

Cleanup resolves/validates the system temp root and exact immediate review directory,
checks its marker and ID, rejects links/unknown children and verifies disappearance.
It never accepts an arbitrary directory or clears the temp root. Do not delete
unknown files to make cleanup pass; disclose the refusal and inspect ownership.
There is no promise of race-free deletion against a hostile concurrent local process.

## Checks

Functional tests create isolated temporary Git repositories by authoring objects,
refs and index directly with Node. All invoked Git commands are read-only. Fixtures
have no external dependencies. Automatic cleanup of test-owned fixtures and reports
is authorized by running the test, separate from a user's active review lifecycle.

```sh
node --test skills/code-review/scripts/tests/review.test.mjs
```

Optional browser test: set `CODE_REVIEW_PLAYWRIGHT` to an installed Playwright
`index.mjs` and `CODE_REVIEW_BROWSER` to its existing Chromium executable, then:

```sh
node --test skills/code-review/scripts/tests/browser.test.mjs
```

It explicitly skips without paths. `CODE_REVIEW_KEEP_REPORT=1` keeps its synthetic
report/screenshots for manual inspection; otherwise they are removed after testing.
It does not install or download browsers. Review screenshots separately; browser
DOM assertions alone are not visual review or full accessibility conformance.
In a restricted host, spawning Git/browser may need host permission; report the
limitation and do not weaken isolation or claim execution. Node 24+ supports
`--test-isolation=none` if only the test-runner child spawn is blocked, but Git
collection and browser tests still require their subprocess capabilities.
