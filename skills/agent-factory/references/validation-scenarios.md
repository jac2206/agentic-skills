# Agent Factory Validation Scenarios

Read when validating abstraction decisions, composition, authority, or failure
paths. These are review inputs and expected outcomes, not agent definitions,
executable fixtures, or evidence of execution. Operational rules remain in
`SKILL.md`; metadata and handoff requirements remain in the target's contracts.

For a manual walkthrough, choose a row, trace the applicable Skill instructions,
and record the decision and supporting sections. For host execution, separately
record the definition/version, host and capability mapping, scoped inputs,
authorization, actual outputs and checks, and remaining limits. Do not label a
walkthrough as runtime testing.

## Abstraction and scope

| ID | Input or condition | Expected outcome |
| --- | --- | --- |
| A1 | A single request to summarize a document, with no continuing responsibility | Recommend a prompt; create no agent package |
| A2 | A stable procedure repeatedly transforms the same input format | Prefer a Skill; offer the relevant authoring handoff without creating an unrequested component |
| A3 | Several known capabilities run in a fixed sequence with explicit handoffs | Prefer a workflow; do not invent an agent to own ordering alone |
| A4 | A bounded responsibility needs independent context and judgment among applicable capabilities | Explain those decisions and design an agent using the existing contract and template |
| A5 | A request to validate an existing agent includes actionable defects | Report findings and fixes; leave the package unchanged |
| A6 | The Skill is installed separately and the target lacks authoritative contracts or a template | Report missing authoring inputs; block contract-conformant creation and label any provisional design unverified |

## Composition and structure

| ID | Input or condition | Expected outcome |
| --- | --- | --- |
| C1 | A required reference is `skill/html-presentations` and the package directory is `presentations` | Resolve the declared name to the actual canonical entry point; do not report a missing Skill from the folder mismatch |
| C2 | A required reference is missing, ambiguous, wrong-kind, or self-referential | Report a blocking structural finding; do not invent an alias, download, or fallback |
| C3 | Required components form a transitive dependency cycle | Identify the cycle and block conformance until it is removed |
| C4 | The body requires a capability absent from direct dependencies, or assumes an optional one is available | Report the dependency mismatch or implicit availability assumption |
| C5 | A template or instructional example contains metadata resembling a live component | Exclude it from discovery and reference resolution |
| C6 | The agent copies a selected Skill's procedure or links into its sibling resources | Replace duplication with typed reuse during authorized improvement; report it during validation only |
| C7 | The definition leaves placeholders, omits a required section, or retains root authoring links needed at runtime | Report incomplete packaging; retain draft status |
| C8 | A revision changes output meaning or permitted effects | Apply the common contract's compatibility/version rules and recheck affected consumers and evidence |

## Authority, execution, and evidence

| ID | Input or condition | Expected outcome |
| --- | --- | --- |
| E1 | A required write operation is unavailable or exceeds current authorization | Block dependent work, preserve useful partial results, and do not use a more privileged substitute |
| E2 | Local edits are already authorized and fit the definition's scope | Preserve that authorization without introducing blanket reconfirmation |
| E3 | Delegation would give a receiver broader access or omit review ownership | Reject the handoff design until authority and ownership are bounded |
| E4 | The host cannot perform the required delegation or enforce tool restrictions | Report incompatibility before dependent work; do not claim a handoff happened |
| E5 | A valid portable file is presented as directly runnable in Codex or another host | Separate declarative conformance from verified integration; report runtime support as unverified |
| E6 | Static checks pass but representative host execution evidence is absent | Report static results separately; keep the agent draft and list pending execution checks |
| E7 | A remote operation has an uncertain outcome and retry could duplicate effects | Require outcome evidence and authorized recovery before repeating the effect |
| E8 | A result claims completion while required evidence or a dependent task is missing | Report partial, blocked, or failed work as applicable; do not accept completion |

## Recording results

Use the repository's validation reporting convention. Record the scenario ID,
scope, method, observed decision or output, result, findings, and limits. Group
related scenarios when a single inspection supplies the evidence. A row in this
document describes intended behavior; it is not a passed test.
