# Frontend Engineer Pilot

Status: `frontend-engineer` 0.1.0 is ready based on representative web and mobile
host evidence, with the limits recorded below. The mobile project change itself
remains open under that project's completion rules.

The first representative task used version 0.1.0 of the portable definition in
Codex on the existing Loyalty Web Next.js/TypeScript project. The caller authorized
local changes to the profile-editing flow. Project instructions, the local UI and
testing Skills, and `ui-ux-design-system` informed the work; no backend changes or
new dependencies were requested. Files were applied to the separately located
project after sandbox authorization.

The change adds retry after profile loading fails, disables saving until a user is
loaded, associates validation errors with their fields, and tests loading recovery,
invalid input, successful saving and save failure with mocked services.

Evidence from the target project:

- `npm test -- --run src/features/user/components/UpdateUserForm.test.tsx`: passed,
  four tests.
- `npx tsc --noEmit --incremental false`: passed.
- `npm run lint`: passed.
- `npm test -- --run`: failed, 41 passed and four failed in two transaction test
  files. Their expectations differ from the existing transaction implementation;
  no transaction files were changed in this pilot.
- Visual and keyboard inspection, a real backend integration and a React Native/Expo
  task were not performed. Missing-tool and unauthorized-effect scenarios were not
  executed as behavioral trials.

These results do not prove automatic host discovery, mobile portability, or
accessibility conformance. Reassess readiness after resolving the applicable failed
checks and recording representative remaining execution evidence.

## Extended web pilot

The caller subsequently authorized addressing the other web review findings. The
local backend source was inspected read-only: its transaction endpoint returns a
complete history without server pagination; user updates use document number,
JWT and a user scope. The deployed backend was not independently verified.

The frontend now tests local history pagination, rejects responses that explicitly
indicate an incomplete server-paginated collection, clears the cached history on
refresh, removes the client-supplied role header, and uses document number for
profile updates. Concurrent profile reads for the same session share only their
in-flight request; no persistent profile cache is introduced. Transaction tests
were updated against the inspected implementation and backend routes.

After those changes, `npm test -- --run` passed 50 tests across 15 files,
`npm run lint` passed, and `npx tsc --noEmit --incremental false` passed. This
supersedes the four failing transaction tests reported above; it does not change
the historical results of the first run. Tests use mocks, not the live backend.
Visual and keyboard inspection, mobile/Expo execution, and the other host failure
scenarios remained unverified at that point. No automated check alone proves
accessibility or security.

## Mobile pilot

The caller authorized a second implementation using the same definition in
Codex on the existing Loyalty App Expo/React Native/TypeScript project. The scoped
change preserves the transactions API and UI while ignoring obsolete responses
after a filter, session, reload, or screen lifecycle change. The existing domain
specification was updated with those acceptance criteria. Local mobile, UI and
testing guidance was consulted; no new runtime or test dependency was installed.

Checks performed on the changed project:

- `npx tsc --noEmit`: passed.
- `npx biome check src/hooks/useTransactions.ts`: passed.
- A temporary Node harness transpiled the actual hook and substituted React hooks,
  authentication and the service. It passed simulated out-of-order success, stale
  error, retry, session removal and unmount. This is a mocked hook simulation, not a React
  Native renderer, device test, or proof of native lifecycle behavior.
- `npm run check`: failed with 11 errors and 16 warnings. The baseline before the
  change had 11 errors and 17 warnings; the changed hook's targeted check passed.
- `git diff --check`: passed. At the time of the agent-run checks, no Android or
  iOS device/emulator, real API, screen-reader, or native visual inspection was
  available or exercised by the agent.

Subsequently the caller reported manually testing the requested filter changes,
loading, connection failure and retry, and leaving the screen or ending the session
during a request, as well as the wider application, successfully in Expo. The
caller supplied screenshots of mobile screens, including Movimientos; they support
the visual record but do not independently establish the dynamic scenarios. Exact
device model and OS version were not supplied. This is caller-reported execution,
not a device test performed by the agent. iOS, screen-reader checks and the other
host failure-path trials remain unexecuted.

The mobile project's own completion rules do not allow closing a change with
required checks failed. Its global Biome failure remains open and the mobile change
is not marked complete. That project-level limitation is distinct from component
readiness: the agent has representative execution evidence in two technology
contexts, reported results and limitations, and its written quality review. Marking
the portable definition ready does not claim the project check passed, native
compatibility across devices, accessibility conformance or automatic host discovery.
