# Example: Diagnosis and Minimal Setup

This fictional example illustrates how the Skill reviews a current setup,
reports a recommendation without editing, and applies a follow-up request. It
is illustrative, not a required layout.

## Existing project evidence

- Root `AGENTS.md` states repository-wide rules and points to the documented
  validation command.
- `.agents/project-context.md` contains confirmed project terminology and
  module boundaries.
- CI runs the same validation command documented in `AGENTS.md`.
- The root instructions do not link to `.agents/project-context.md`.

## First request: review and recommend

The user asks: “Review whether the project is ready for agents and recommend
improvements.” Because no mode was named, the Skill uses Analyze mode.

| Dimension | Disposition | Evidence |
| --- | --- | --- |
| Project context | Keep | The context file contains confirmed terminology and module boundaries. |
| Testing and quality | Keep | The documented validation command matches CI. |
| Agent collaboration | Improve | The root entry point does not link to the existing context file. |

**APS-01 — P2:** Add a link from the relevant section of `AGENTS.md` to
`.agents/project-context.md`. This makes existing guidance discoverable without
copying or restructuring it.

Analyze mode ends with the recommendation and makes no file changes.

## Follow-up request: improve the setup

The user replies: “Apply APS-01” or “Improve the setup.” The Skill continues in
Setup mode, reinspects `AGENTS.md`, and adds the link in the relevant section.
That follow-up authorizes this low-risk documentation change. It does not
authorize unrelated restructuring or material policy decisions.

If the link already exists when Setup reinspects the file, the Skill reports
that APS-01 is already satisfied and makes no duplicate edit.

## Validation

- The relative link resolves to `.agents/project-context.md`.
- The existing context file remains the source of truth; its contents were not
  copied into `AGENTS.md`.
- No unrelated files or directories changed.
- Repeating Setup does not add another link.
