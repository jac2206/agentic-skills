## Technology Decision — Supported UI Stacks

JAC supports two official web UI implementation approaches. Both must follow the same brand identity, design tokens, accessibility standards, typography, spacing, and visual guidelines.

### Option A — Tailwind CSS + shadcn/ui

- Applicable to React and Next.js projects when compatible with their existing setup.
- Styling: Tailwind CSS with JAC semantic design tokens.
- Components: shadcn/ui with Radix primitives where applicable.
- Icons: Lucide React.
- Forms: React Hook Form + Zod.
- Advanced tables: TanStack Table.
- Charts: Recharts when required.

**Recommended for:** personal portfolios, SaaS applications, custom interfaces, landing pages, and products requiring extensive visual customization.

### Option B — PrimeReact

- Applicable to React and Next.js projects when compatible with their existing setup.
- Components: PrimeReact, using APIs compatible with the installed version.
- Styling: PrimeReact theming with JAC semantic design tokens.
- Tailwind CSS: optional for layouts and utilities, provided style conflicts are controlled.
- Icons: PrimeIcons or Lucide React.
- Forms: PrimeReact components with Zod or another appropriate validation solution.
- Tables: PrimeReact DataTable.
- Charts: PrimeReact-compatible charting solutions when required.

**Recommended for:** enterprise applications, administrative platforms, CRUD systems, data-intensive dashboards, and applications requiring advanced UI components.

### Stack Selection Rules

1. Both approaches are officially supported. Neither is universally mandatory.
2. Inspect the existing project and dependencies before choosing a stack.
3. Preserve the project's existing UI foundation unless migration is explicitly requested.
4. Respect the user's explicitly requested stack and the product's requirements.
5. For new React/Next.js projects without an established UI stack or explicit preference, default to Tailwind CSS + shadcn/ui when a component stack is needed and compatible. Use PrimeReact when explicitly requested. Always preserve an existing stack unless migration is requested.
6. Do not mix shadcn/ui and PrimeReact component foundations without explicit architectural justification.
7. Do not assume that PrimeReact and shadcn/ui share component APIs.
8. Apply the same official JAC semantic tokens to either implementation.
9. Verify component APIs against the installed library version.

### Angular and other platforms

- Consider PrimeNG for Angular when appropriate and compatible with the existing project; preserve established libraries.
- Apply semantic JAC tokens in the format supported by the actual platform. Vue, Flutter, HTML/CSS and other ecosystems remain valid; do not impose React or a particular library.

### Mobile Applications

- For React Native and Expo, follow the existing project setup and use native-compatible components.
- Use native-compatible components and styling.
- Reuse JAC brand tokens and visual principles.
- Do not import PrimeReact, PrimeNG or shadcn/ui web components into React Native.

## Implementation Conventions

- In Next.js projects that support React Server Components, follow the project's conventions for server and client boundaries; use `"use client"` where required.
- Separate reusable UI components from domain and feature logic.
- Use typed component interfaces and reusable variants.
- Use semantic JAC design tokens instead of arbitrary hardcoded colors.
- Support responsive layouts, light and dark modes.
- Implement loading, error, empty, success, disabled, and focus states.
- Follow WCAG 2.2 AA accessibility requirements where applicable.
- Prefer composition over unnecessary component abstraction.
- Validate build, lint, TypeScript checks, and relevant tests.
- Use the project's existing testing tools and relevant tests; introduce tools only when justified and authorized.

## Skill Instructions

When JAC is explicitly selected or used as the fallback because no other identity is established:

1. Read `JAC-BRAND-GUIDELINES-FINAL-v2.md`.
2. Read `JAC-COLOR-PALETTE.md`.
3. Read `JAC-UI-GUIDELINES.md`.
4. Inspect the existing project architecture and installed dependencies.
5. Identify the existing framework and UI stack; select a suitable option only when needed.
6. Preserve the existing stack unless migration is requested.
7. Apply official JAC tokens, typography, spacing, icons, and approved assets.
8. Generate code using the selected component library and its installed version.
9. Do not mix component foundations without justification.
10. Verify responsiveness, accessibility, light/dark themes, and component states.
11. Execute available build, lint, type-checking, and relevant tests.
12. Treat `JAC-DESIGN-SYSTEM-v4.html` as the primary visual reference and an illustrative playground, not production-ready component source code.

Preserve explicit or existing non-JAC identities and do not mix them with JAC.
