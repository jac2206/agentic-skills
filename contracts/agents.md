# Agent Definition Contract

Applies to future `agents/<name>/AGENT.md` definitions using
[common contract 1.0](components.md). No functional agent is supplied in this phase.

## Responsibility

An agent owns one bounded delegated responsibility requiring judgment or context
isolation. Explain why a prompt, existing Skill, or fixed workflow is insufficient.
Do not require an orchestrator, subagents, persistent memory, or a particular model.

## Required body

| Section | Required information |
| --- | --- |
| Purpose | One responsibility and reason for using an agent |
| When to use / When not to use | Observable selection signals and exclusions |
| Inputs | Required/optional context, scope, preconditions and missing-input behavior |
| Outputs | Deliverable format, evidence and completion criteria |
| Capabilities | Required typed component references, selection conditions and expected results; explicit optional suggestions if useful |
| Tools and authority | Required/optional tool capabilities, allowed effects, prohibited actions and missing-tool behavior |
| Coordination | How inputs reach selected capabilities and how results are checked; no copied Skill procedures |
| Handoffs | Whether delegation is used and, if so, ownership and bounded task transfer |
| Failure behavior | What blocks work, how partial results are reported and when recovery is permitted |
| Quality criteria / Validation | Observable criteria and how to verify them |

## Skill reuse

Resolve the referenced Skill, read its entry point and conditionally required
resources, pass scoped inputs, then validate the result using its own criteria.
Respect its modes and limits. Never present a rewritten summary as a replacement
for its operational instructions. Dependency availability is checked before use.

## Tools and authority

Describe tools by operation, required inputs, possible local/remote effects and
failure behavior. The host maps these descriptions to concrete available tools.
Selection does not grant permissions: actual actions remain bounded by user
authorization, host policy and the referenced component's limits.

Distinguish read-only work, authorized local writes and authorized remote writes
when relevant. Preserve existing authorization; do not add blanket confirmation
requirements for already authorized operations. An unavailable required operation
blocks its dependent work; do not silently substitute a more privileged tool.

## Handoff and result

If delegation is needed, state whether the caller retains coordination or transfers
the task to the receiver. No universal concurrency or transport protocol is
required. A handoff preserves:

- Objective, target workspace/context, scope and exclusions.
- Available inputs and evidence locations, output format and completion criteria.
- Permitted effects, constraints, unresolved decisions and required capabilities.
- Caller/receiver responsibility for reviewing the returned result.

A returned result states `completed`, `partial`, `blocked`, or `failed`, with scope,
outputs, evidence, actual checks, changes made and remaining issues. `completed`
requires the applicable completion criteria; partial work cannot be labeled
complete. This is a reporting convention, not an implemented message schema.

No agent may broaden its authority through delegation. If the host cannot enforce
the declared ownership or tool restrictions, report that incompatibility before
dependent work. Do not claim delegation happened merely because it is documented.
