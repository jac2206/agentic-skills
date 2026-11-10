# Validation Scenarios

Use these cases to check whether the Skill adapts its review decisions to
evidence, authorization, project artifacts, and prior state. They are not
claims that any particular project has been tested. The report generator's
deterministic checks can be exercised with `scripts/render_report.py`; the
security judgment cases require reviewer reasoning against supplied fixtures
or a real authorized project.

| # | Scenario | Expected behavior |
|---:|---|---|
| 1 | Backend uses JWT | Inspect issuer, audience, signature validation, expiry, key handling, and authorization only where evidence and scope permit. Do not assume JWT is secure or insecure by itself. |
| 2 | API may have broken resource authorization | Trace caller identity, resource lookup, and ownership/tenant check. Confirm with code or authorized tests; otherwise label potential and identify missing policy/evidence. |
| 3 | Frontend contains a possible XSS path | Trace untrusted value to the rendering context and relevant encoding/CSP controls. Do not call it confirmed from an unsafe-looking string alone. |
| 4 | Dependency advisory applies | Verify package identity, affected version, reachability/context, advisory source, and available fix. A scanner alert alone is tool-reported evidence, not proof of exploitability. |
| 5 | Secret-like value is found | Do not print or copy the value. Identify file and secret type, assess exposure context, and recommend revocation/rotation through the owner. |
| 6 | Mobile application | Consider local storage, cryptography, authentication, network, platform interactions, privacy, and applicable MASVS/MASTG guidance. Keep remote API review in scope only when authorized. |
| 7 | Docker and cloud infrastructure | Inspect the supplied deployment/configuration evidence for identity, network, exposure, image, secret, and storage controls. Do not infer live cloud state from IaC alone. |
| 8 | CI/CD permissions appear broad | Trace workflow triggers, identity permissions, secret access, approvals, and artifact flow. Distinguish configuration evidence from deployed behavior. |
| 9 | RAG application with tool-using agents | Assess untrusted content influence, retrieval isolation, tool allowlists, authorization, output validation, and data egress. Avoid running adversarial prompts against live systems absent explicit scope. |
| 10 | No vulnerability is evident in inspected scope | Report no confirmed findings in that scope, list checks and limitations, and explicitly avoid claiming the system is vulnerability-free. |
| 11 | Suspected issue lacks sufficient evidence | Keep it a potential risk with the missing evidence and safe confirmation method stated. Do not invent a finding or severity proof. |
| 12 | Prior finding appears fixed | Preserve its ID and prior history. Require post-change evidence; otherwise keep it Open or In Progress. |
| 13 | Story lacks relevant security acceptance criteria | Give a concise story-linked requirement and verifiable criteria proposal; do not edit the backlog without authorization. |
| 14 | SDD change needs security conditions | Review the change's relevant assets and controls, propose security scenarios, and hand lifecycle management to `spec-driven-development` if present. |
| 15 | Project uses OpenSpec | Follow its existing structure and change artifacts. Do not create or reshape OpenSpec content independently. |
| 16 | Project has a custom specification process | Preserve its format and vocabulary; do not migrate it to another methodology. |
| 17 | Historical reports and finding register exist | Reconcile prior findings, preserve stable IDs and immutable history, do not overwrite a dated report, and update latest only for a completed broad Audit. |
| 18 | HTML report receives untrusted text | Generator must escape user-supplied report text, accept only HTTPS links for references, and open without external assets or scripts. |
| 19 | Duplicate finding ID or unresolved `Resolved` state | Generator validation must fail before writing files when IDs duplicate or resolution date/evidence is missing. |
| 20 | Partial review | Create a clearly labeled dated review when requested; do not replace latest completed audit reports. |
| 21 | `latest.md` matches a partial/remediation history entry while a completed audit also exists | Compare both latest formats, review IDs, mode, completion and matching historical/canonical data. Flag the pre-existing inconsistency and preserve it during read-only review; do not claim the current generator caused it or that an unchanged latest is a valid audit. |
| 22 | Completed audit followed by partial review | In an isolated root, save hashes of both `latest.*` files, render a partial review with a new ID, and compare hashes and the printed status. Both latest files must remain byte-identical and the message must say they were left unchanged; the dated partial report must identify its own mode and ID. |

## Generator checks

From this Skill directory, validate a completed JSON input without writing:

```sh
python scripts/render_report.py path/to/review-data.json --check
```

On Windows, use `py -3` in place of `python` when needed.

Then generate into an isolated temporary project root and inspect that the
Markdown, HTML, and register reflect one input. Repeat with a different review
ID to confirm historical outputs coexist. Repeat using a partial review to
confirm `latest.*` is not changed. Finally run with a duplicate finding ID,
invalid state, unresolved `Resolved` finding, and non-HTTPS reference; each must
fail with no report files created. For HTML escaping, use a harmless string such
as `<script>alert(1)</script>` in a temporary title and confirm it appears only
as escaped text in the output.

The script validates data shape and report generation; it does not inspect the
pre-existing semantic correctness of `latest.*`. The reviewer must perform the
preflight comparison above and disclose missing or conflicting metadata. It does not test
security controls in the target application or merge/reconcile finding history;
those remain reviewer responsibilities.

