# Illustrative scenarios

These examples show possible choices, not required files or sequences.

## Small bug without a specification system

A confirmed display formatting defect has a clear expected result and low risk.
Inspect the affected code and existing tests, implement a bounded fix, run a
relevant test and report the command and result. A short plan is sufficient;
no proposal, design document, or new specification directory is needed.

## Complex authentication change with an active specification

An existing story and active change describe a new authentication flow. Reuse
their references and native lifecycle; identify unresolved policy before its
dependent implementation. Record a proportionate design and tasks in that
system. Link a security review and findings without copying them. Verify the
acceptance criteria, controls and contracts with evidence. If a mandatory test
fails or a task remains incomplete, retain the active state and report it;
close only after required gates pass and authorized decisions are resolved.
