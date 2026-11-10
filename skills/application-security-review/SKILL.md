---
name: application-security-review
description: >
  Assess application and software-delivery security risks, review changes,
  document evidence-based findings, and validate authorized remediations across
  technology stacks. Use for security analysis, change reviews, audits, and
  remediation validation; do not use as a certification or as authorization for
  active testing against systems.
metadata:
  version: "1.0.1"
---

# Application Security Review

Assess security risks across software requirements, design, implementation,
configuration, dependencies, and delivery using evidence from the authorized
scope. Produce actionable findings and help verify remediations when requested.

## Purpose

Provide a technology- and architecture-agnostic security review capability for
applications and their delivery environments. Identify supported risks, assess
controls, document uncertainty, recommend mitigations, and verify fixes with
proportionate evidence. The Skill does not replace security ownership, a
penetration-testing engagement, or a compliance assessment.

## When to use

Use this Skill when the user asks to:

- Assess or audit an application's security posture.
- Review the security impact of a requirement, story, specification, design,
  implementation, pull request, configuration, or dependency change.
- Identify security requirements or acceptance criteria for a planned change.
- Threat model a system or a material change.
- Help remediate a documented finding and verify whether it is resolved.
- Produce or update a project security findings register or review report.

Choose one mode from the request:

- **Analyze:** Inspect the authorized project scope and report findings without
  modifying project files.
- **Review:** Assess a supplied change and its directly relevant dependencies,
  contracts, and controls. Do not broaden into a full audit unless requested.
- **Audit:** Assess a broader, explicitly bounded system or project and produce
  a consolidated report.
- **Remediation:** Work on one or more existing findings. Explain and propose a
  fix; edit code or configuration only when the user authorized implementation.
  Validate the fix before changing finding status to Resolved.

If the mode is unstated, infer Review from a specific change, Audit from a
request for a broad assessment, Remediation from a request to fix findings, and
Analyze otherwise. State the inferred mode and scope.

## When not to use

Do not use this Skill to:

- Reconstruct a project's architecture, agent instructions, or repository
  structure; use `agentic-project-setup` for project readiness and context.
- Own backlog refinement or edit user stories and requirements; hand proposed
  security requirements and acceptance criteria to `requirements-engineering`.
- Manage specifications, OpenSpec, or a change lifecycle; hand off to
  `spec-driven-development` when available and respect the project's existing
  specification conventions.
- Replace specialist architecture, code review, test automation, database,
  deployment, or technical documentation work.
- Claim certification, guarantee absence of vulnerabilities, or substitute
  automated scanner output for contextual review.
- Perform active testing against external, production, or third-party systems
  without explicit authorization that identifies the targets and permitted
  methods.

## Core Principles

### Evidence before conclusions

Tie every confirmed finding to reproducible evidence in scope. Distinguish a
confirmed vulnerability from a potential risk, design weakness, control gap,
and improvement recommendation. A missing artifact or unavailable test is a
limitation, not proof that a control is absent or present.

### Least change and safe scope

Analyze, Review, and Audit are read-only. Remediation mode may change only the
authorized files and must preserve existing project conventions. Never run
destructive tests, change production systems, expose secrets, or attack systems
outside the approved scope.

### Contextual controls

Assess only dimensions relevant to the system and change. Adapt to the actual
languages, platforms, data, architecture, deployment, and trust boundaries.
Frontend checks do not replace server-side enforcement. Automated tools support
review but do not establish a security guarantee by themselves.

### Traceable risk decisions

Keep findings linked to the affected requirement, story, specification,
implementation, and tests when those artifacts exist. Preserve existing IDs and
history. Never mark a control Passed or a finding Resolved without evidence.

## Inputs

### Required

- An authorized target and scope: project/repository, change, files, design, or
  other supplied material.
- Mode, explicit or inferred using the rules above.

### Optional

- Project context and security policies, including relevant `.agents/` material.
- Architecture diagrams, data flows, specifications, user stories, threat
  assumptions, API contracts, infrastructure and CI/CD configuration.
- Existing findings, previous reports, scanner output, dependency inventory,
  test evidence, and authorized test accounts or environments.
- Applicable standards, risk appetite, severity rubric, output language, and
  requested report location.
- For active testing, explicit target, environment, allowed techniques, time
  bounds, and stop conditions. If any required authorization boundary is
  unclear, limit work to passive review and ask for the missing scope before
  active testing.

Do not request or copy secret values. If a secret is encountered, do not print,
quote, or include it in generated output; identify the location and type only,
and recommend rotation through the responsible owner.

## Outputs

Return findings and limits in the response. For a persisted project review,
prefer an existing equivalent structure; otherwise use:

```text
security/
├── findings/
│   └── findings.md
└── reports/
    ├── latest.md
    ├── latest.html
    └── history/
        ├── security-review-<date>-<review-id>.md
        └── security-review-<date>-<review-id>.html
```

Create only files needed for the requested work. Do not put operational agent
instructions under `security/`; project policies belong in the established
`.agents/security/` location when the project uses it. Do not create a competing
folder if an equivalent security register or report system already exists.

Use `templates/review-data.json` as the input format for the report generator.
That JSON is the canonical data source for the generated findings register,
Markdown report, and HTML report. Include the complete known finding set when
updating the register; reconcile older findings and preserve their history
before rendering. Never maintain Markdown and HTML as independent sources of
truth. A partial review may create a dated report but must not replace the
latest completed audit. Historical files are immutable; choose a new review ID
if the intended history filename already exists.

Each finding must include:

- Stable ID (`SEC-001`, `SEC-002`, ...), title, severity, category, status, and
  affected location.
- Evidence, description, credible exploitation scenario, impact, and
  likelihood/rationale. Redact sensitive data from evidence.
- Concrete recommendation and mitigation guidance.
- Relevant technical references (for example CWE, CVE, a versioned standard, or
  vendor advisory) when applicable.
- Detection date, review ID, and resolution date and validation evidence when
  resolved. Accepted risks include the rationale, accountable owner, and next
  review date when known.

Allowed severities: `Critical`, `High`, `Medium`, `Low`, `Informational`.
Allowed states: `Open`, `In Progress`, `Resolved`, `Accepted Risk`,
`False Positive`. Severity is the review's risk classification; it is distinct
from CVSS scoring and OWASP categories. Do not invent a CVSS score or vector.

## Workflow

1. **Set mode, target, and authority.** Record what is in scope, excluded, and
   authorized. In Review mode, focus on the change and dependencies that affect
   it. Do not probe a live system unless the user explicitly authorized the
   targets and methods.
2. **Read project context.** Follow applicable repository instructions. Inspect
   relevant architecture, security policies, specifications, tests, existing
   findings, and change history. Use current `agentic-project-setup` outputs if
   present; do not reconstruct project setup. Identify the actual technologies,
   data, actors, trust boundaries, and exposure from evidence.
   If `latest.md` or `latest.html` already exists, inspect both and the matching
   dated report/canonical JSON where available. Compare review ID, mode,
   completion and scope, including the summary's claims about prior state.
   Only a completed broad Audit is eligible for `latest.*`. Report mismatched,
   missing, partial, stale or unverifiable artifacts with their paths; do not
   infer which tool or version caused them. Preserve existing files in read-only
   modes and propose a reconciliation using verified history rather than
   silently overwriting it. A partial review that leaves `latest.*` unchanged
   must not describe its pre-existing contents as correct without evidence.
3. **Choose applicable coverage.** Select the relevant dimensions from
   [the review playbook](references/security-review-playbook.md). Select only
   standards and versions that fit the project and review question. Verify
   current editions from their official sources when version currency matters;
   record the exact version used.
4. **Map attack surface and controls.** Trace relevant entry points, data flows,
   identities, permissions, trust boundaries, integrations, and failure paths.
   Consider a proportionate threat model for material architectural changes,
   sensitive assets, multiple trust boundaries, or high-impact flows. Skip it
   for trivial changes and state why when useful.
5. **Gather evidence.** Inspect code, configuration, contracts, tests, and
   authorized tool output. Record file/line, setting, behavior, or test result.
   Label evidence as observed, tool-reported, user-provided, inferred, or
   unavailable. Avoid reproducing payloads or data that could cause harm.
6. **Validate candidate findings.** Check the full relevant flow and existing
   controls. Prefer a minimal, safe confirmation. If evidence is incomplete,
   report a potential risk and name what would confirm or dismiss it. Remove
   duplicates by matching root cause and affected control; reuse existing IDs
   for the same issue.
7. **Classify and recommend.** Choose severity from impact, likelihood,
   exposure, exploit prerequisites, affected data and scope, and compensating
   controls. Explain the rationale. Add a CVSS score only if sufficient
   evidence supports a valid vector under a named version and the score adds
   value. Recommend an actionable mitigation and any needed regression test.
8. **Trace security requirements.** For relevant stories, propose the missing
   security requirement and objectively verifiable acceptance criteria, linked
   to the story. For specifications, provide a `Security Review` section or
   suggested patch in the existing format. Do not edit requirements or
   specifications unless explicitly authorized. Do not create or restructure
   OpenSpec.
9. **Remediate only when authorized.** Explain affected files and the change,
   make the smallest safe fix, and add or update focused tests when authorized.
   Validate using existing safe project checks. Do not disable controls to pass
   checks. If validation is unavailable or incomplete, leave the finding open
   or In Progress and state the evidence gap.
10. **Reconcile records and report.** Preserve IDs, previous evidence, and
    history. Record accepted-risk owner and review date when known. Generate
    Markdown and HTML from the same structured data when requested. Only a
    completed broad Audit may replace `latest.*`; partial reviews remain dated
    and are identified as partial. Report any pre-existing `latest.*` conflict
    separately from the result of the current generator invocation. Do not
    restore or replace historical reports automatically to resolve a conflict.
11. **Summarize.** State scope, method, findings by severity, key limitations,
    remediation state, traceability handoffs, files changed, and validation
    performed. Never describe a review as certification or proof of security.

## Rules

The Skill must:

- Preserve existing project structure, controls, report conventions, and
  finding identifiers where practical.
- Use evidence tied to the assessed scope and distinguish confirmed issues,
  potential risks, design weaknesses, control gaps, and recommendations.
- Explain severity and uncertainty; use the organization's rubric if supplied.
- Use authoritative, current references where relevant and record versions.
- Keep reports free of secret values, credentials, tokens, personal data not
  needed to substantiate the issue, and exploit details beyond what the
  authorized audience needs to remediate it.
- Keep a control `Not Assessed` when evidence is insufficient; justify `Not
  Applicable` decisions. Never infer success from a clean scanner run.
- Preserve finding history and keep unresolved findings visible in later
  reports.
- Refer security requirement proposals to `requirements-engineering` and
  security review notes to the project's existing specification process.

The Skill must not:

- Invent vulnerabilities, proof, impact, exploitability, dates, test results,
  scores, percentages, controls, or stakeholder decisions.
- Modify code in Analyze, Review, or Audit mode.
- Mark a finding Resolved because code changed; require post-change validation
  evidence. Do not silently downgrade or close findings.
- Run destructive tests, exploit external systems, use real customer data, or
  conduct active testing outside explicit authorization.
- Reveal the value of secrets encountered in source, logs, test output, or
  scanner output.
- Change requirements, stories, security policies, or specification lifecycle
  records without authorization.
- Treat an automated scan or this report as proof of compliance, certification,
  or the absence of vulnerabilities.

## Constraints

- The requested language applies to generated project artifacts; this Skill and
  its supporting resources are written in English.
- Match tools and checks to the detected project. Do not assume a language,
  framework, cloud provider, scanner, test command, or runtime.
- Avoid exposing sensitive details in findings. State safe evidence locations
  and redact values and exploit payloads as needed.
- When online research is needed, prefer official standards, maintainers, and
  vendor advisories. If sources are unavailable, state the version uncertainty.
- This capability provides technical review assistance, not legal advice,
  compliance attestation, or a guarantee of security.

## Tools

No tool or scanner is required. Use static search, repository inspection,
dependency metadata, tests, and security tools only when available, safe, in
scope, and useful. Do not install tools or dependencies without authorization.

The standard-library report generator is optional:

```text
python scripts/render_report.py <review-data.json> --out <project-root>
```

On Windows installations where `python` is not on `PATH`, use `py -3` in place
of `python`.

It validates the data and renders the findings registry plus Markdown and
self-contained HTML reports. It does not inspect source code, discover
vulnerabilities, merge prior finding data, or sanitize secrets in input; the
reviewer must provide a complete, reconciled, redacted dataset. It refuses to
overwrite a history file. See the script help for its `--check` validation
option.

## Composition

### Upstream Skills

Optional inputs when present and relevant:

- `agentic-project-setup` for repository context, architecture, policies, test
  guidance, and security baseline. Consume its evidence; do not redo setup.
- `requirements-engineering` for backlog items that may need security
  requirements. Propose additions there; do not take over backlog ownership.
- `spec-driven-development` for the project's specification and change
  lifecycle, if installed. Review security within that lifecycle; do not
  administer it.
- Architecture, backend documentation, design, testing, API, database,
  deployment, code review, or technical documentation capabilities when
  available and pertinent. They remain optional and this Skill can run alone.

### Downstream Skills

- `requirements-engineering` may consume proposed security requirements and
  acceptance criteria.
- `spec-driven-development`, when available, may incorporate a security review
  into the affected change using its established conventions.
- Implementation, code review, and test Skills may consume approved
  remediations and regression-test recommendations.
- `agentic-project-setup` may consume recommendations for durable agent-facing
  security policies; keep those policies separate from findings and reports.

Do not claim that an unavailable Skill ran. Do not require any other Skill to
perform a review.

## Quality Criteria

The review is useful when:

- [ ] Mode, target, authorization boundary, exclusions, and evidence limits are
  stated.
- [ ] Coverage reflects the actual architecture and relevant attack surface.
- [ ] Each confirmed finding has in-scope evidence and a credible impact path;
      uncertain items are explicitly potential risks.
- [ ] Severity is reasoned and is not confused with CVSS or OWASP categories.
- [ ] Recommendations are specific, proportionate, and include validation
      guidance where useful.
- [ ] Finding IDs, statuses, dates, and history are stable and consistent.
- [ ] Requirements and specifications have traceable, non-invasive handoffs.
- [ ] No secret values or unnecessary sensitive data appear in output.
- [ ] Remediations are authorized and a finding is closed only with validation
      evidence.
- [ ] Generated Markdown and HTML represent the same canonical input; partial
      reviews do not replace a completed audit.
- [ ] Existing `latest.*` eligibility and consistency were checked when
      present, and mismatches or unverifiable history are disclosed.
- [ ] Limitations are explicit and the report makes no certification claim.

## Validation

Before returning results:

1. Re-read the in-scope evidence for each finding; confirm location, behavior,
   preconditions, impact, and existing mitigating controls.
2. Check that each conclusion is correctly labeled as confirmed, potential,
   weakness, gap, or recommendation and that evidence supports its status.
3. Check severity rationale, references and versions, unique stable IDs,
   statuses, required dates, accepted-risk fields, and resolution evidence.
4. Check that reports preserve older findings, history files are not overwritten,
   and only a complete Audit updates latest reports.
5. Compare Markdown and HTML content against the same input data; ensure HTML
   escapes untrusted content and opens without network access.
6. Check that proposed requirement/specification changes are traceable and were
   not applied without authorization.
7. In Remediation mode, run only authorized, relevant, safe checks and retain
   open status when verification evidence is insufficient.
8. Report the exact checks performed and any unavailable evidence or tool.

## References

- See [Security review playbook](references/security-review-playbook.md) for
  conditional coverage dimensions, threat modeling, and standards selection.
- See [Review data template](templates/review-data.json) for the canonical
  report input used by the optional generator.

## Examples

### Change review with unresolved access policy

**Input:** A change adds an endpoint that loads a record by a caller-supplied
identifier. The repository defines roles but no resource ownership rule.

**Expected behavior:** Inspect the lookup and authorization path. If code shows
that a caller can access another tenant's record, report a confirmed
authorization finding with evidence. If the rule or evidence is unavailable,
label it a potential risk and request the missing policy or test. Propose a
story-linked acceptance criterion, but do not invent policy or edit the story.

### Remediation without verification

**Input:** A developer says a finding was fixed, but no test or implementation
evidence is available.

**Expected behavior:** Keep the finding Open or In Progress. Identify the
evidence needed to verify the fix; do not infer resolution from the statement
alone.

