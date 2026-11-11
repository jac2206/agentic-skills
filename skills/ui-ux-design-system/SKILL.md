---
name: ui-ux-design-system
description: >
  Designs, implements, audits, and evolves user interfaces and design systems
  across web and mobile, respecting existing identities and technology while
  using the JAC Design System when no other identity is established.
metadata:
  version: "1.4.1"
---

# UI/UX Design System

## Purpose

Design and maintain coherent, usable, accessible user experiences and their reusable visual foundations, proportionate to the requested work.

## When to use

Use for UI or UX design, interaction flows, visual identity, design tokens, themes, components, interface implementation, visual audits, or design-system maintenance for new or existing graphical products. Applicable to web, mobile, enterprise, dashboards, SaaS, fintech, and other interfaces.

## When not to use

Do not use for requirements ownership, technical architecture redesign, security audits, or change-lifecycle administration. Consume their outputs and hand off specialist work. Do not use for a purely backend change with no interface impact.

## Inputs

Required: the requested outcome or interface scope. Inspect available project evidence; ask only when a missing decision blocks safe or meaningful progress. Optional inputs include users, tasks, requirements and acceptance criteria, brand and visual references, platforms, accessibility targets, existing UI and architecture, stack, constraints, and available validation tools. Separate confirmed facts, assumptions, and pending decisions; do not invent business behavior.

## Outputs

Produce only deliverables appropriate to the request: analysis or evidence-based findings, visual/interaction specifications, tokens or components, implementation changes, or maintenance recommendations. Record relevant decisions, affected requirements, validation performed, findings, and limitations. Use the [UI specification template](templates/ui-specification.md) only when a written handoff adds value.

### Visual design deliverables

- For a request to design screens or flows, create a reviewable HTML prototype by default when no output format is specified. Use one proportionate, navigable prototype for related screens rather than automatically creating an HTML file per screen. Use the existing project's conventions or its designated artifact location; otherwise use an appropriate non-root output location. Keep it usable locally when practical, and clearly identify simulated interactions or placeholder data. Demonstrate relevant screens, navigation, states and responsive behavior without inventing business functionality. A prototype is not production implementation.
- If the user explicitly requests Figma, deliver both an editable Figma design and the HTML prototype. Discover available Figma tools and their actual write capabilities and access; use a specified destination or an authorized available workspace. If native creation is unavailable, deliver the HTML and a concise Figma handoff with relevant layout, components, tokens and interactions, and clearly state that no Figma file was created. Do not label an image, HTML file, link or description as an editable Figma file.
- Honor an explicit alternative format or request not to create HTML. Analyze and Audit remain read-only; a code-only change, small improvement, implementation or design-system maintenance does not automatically require a separate prototype. An existing runnable interface may serve as the reviewable deliverable when it fulfills the request.
- Use existing assets and image-generation tools when imagery is requested or materially improves the design and a suitable tool is available. Treat generated images as optional visual assets, not editable design files or substitutes for accessible interactive elements. If unavailable, identify the limitation and use suitable placeholders when helpful.

## Modes

Select the requested mode or combination; infer the smallest appropriate mode from the outcome. Analyze and Audit are read-only. Design work may produce requested specifications, while implementation and maintenance change files only within authorized scope.

- **Analyze:** inspect the existing interface, stack, structure, components, tokens, styles, themes, navigation, responsive behavior and accessibility evidence; report inconsistencies and opportunities without modifying files.
- **Create Design System:** establish only needed foundations, tokens, components, patterns, themes and conventions, building on existing assets.
- **Design Interface:** design the requested screens and flows, their content hierarchy, states and interactions.
- **Implement Interface:** implement the agreed scope using the existing stack, components, tokens, navigation and architecture.
- **Improve:** make targeted improvements while preserving established identity and behavior unless change is requested.
- **Audit:** evaluate in-scope usability, visual consistency, components, states, interaction, themes, responsive behavior and accessibility; give evidence, impact, priority and unassessed areas without changing files.
- **Maintain:** evolve the existing system, assess affected consumers and compatibility, and validate changes.
- **Full Workflow:** analyze, design, implement and validate as needed; scale or omit stages to fit the request and authorization.

## Workflow

1. **Establish context.** Read applicable `AGENTS.md`, local guidance, architecture, requirements and project conventions. Identify product, users, platform, tasks, flows, devices, brand, visual references, existing components, tokens, themes, libraries, framework, constraints and accessibility goals. Inspect actual code and rendered UI when available. Record unknowns; don't rebuild agent configuration or impose a directory layout.
2. **Determine scope and identity.** Apply this order: explicit user brand, colors, typography, design system and preferences; existing project design system; established product identity or supplied visual references; otherwise JAC by default. An explicit partial palette or typography choice is an identity constraint: build a coherent direction around it without adding JAC branding by default. If another identity exists, preserve it; do not blend JAC assets, palette or components into it. Do not silently change existing colors or components. Identify conflicts and accessibility tradeoffs, and honor explicit choices. When JAC applies, use the conditional references below and report missing or conflicting assets.
3. **Choose a visual direction.** For design work, identify product type, audience, primary task, brand, platform and appropriate visual expressiveness and density. State a concise direction and explain the main composition choices when useful. Translate the existing identity into a composition suited to the task; do not apply the same layout across products. For audit or improvement, evaluate the existing direction before proposing changes. See [Design guidance](references/design-guidance.md) for conditional composition and platform prompts.
4. **Design proportionately.** Map relevant requirements to screens and flows. Plan the information hierarchy, typography, content grouping, whitespace, navigation and responsive adaptations around the user's tasks. Choose surfaces, cards, tables, data visualization, imagery and asymmetry only when they help the content; avoid repeating a heading, uniform cards and table as a default. Define relevant states, feedback, error prevention and recovery. Reuse established components and supported customization mechanisms before introducing new ones. Produce the visual deliverables above when applicable; do not invent business behavior.
5. **Implement when requested.** Inspect and follow the existing stack and architecture. Reuse components and semantic tokens, preserve business behavior and state, and avoid duplicating styles, dependencies or components. Select libraries according to the rules below and installed versions. Apply changes incrementally; consider compatibility and downstream consumers before changing tokens or public components. Do not rename existing tokens without authorization. Include appropriate tests when valuable.
6. **Validate and report.** Match checks to scope and risk. For a visual design, inspect main screens in a browser or platform tool when available, including relevant desktop, tablet and mobile sizes, supported themes, navigation, states and overflow. Review the visual direction and correct observed issues using the quality criteria below; inspect actual color combinations and run relevant checks. A prototype may simulate behavior but must identify that limitation. For a Figma deliverable, verify that the actual editable file and intended frames exist when access permits. Report artifact paths or links, exact evidence, checks and untested areas; never claim visual inspection, conformance, a Figma file, or test execution without evidence. If rendering or inspection is unavailable, explicitly say so.

## Rules

- Prioritize usability, consistency, accessibility, hierarchy, clarity, brand, reuse, adaptability, maintainability, performance and visual finish. Avoid unnecessary visual effects or workflow steps. Do not invent functionality.
- Make visual choices purposeful: vary grouping, density and hierarchy to match content, rather than decorating for novelty. Avoid unnecessary repeated cards or borders, indistinguishable sections, tiny text, unexplained whitespace, generic gradients and superficial use of brand. Correct issues that inspection reveals without compromising accessibility or established identity.
- Define tokens only at useful scale. Prefer semantic names; separate primitive, semantic and component levels when they add value. Avoid scattered hardcoded colors; adapt token formats to the existing technology. Preserve compatibility during evolution.
- Respect requested light and dark themes, mapping semantic roles consistently across surfaces, text, controls, charts, feedback and overlays. Support system preference with the framework's appropriate mechanism when requested; consider custom branding or white label only when needed. Never require dark mode.
- Consider purpose, variants, sizes, relevant states, interaction, accessibility, themes and responsive behavior for each component; don't create a catalog by default. Include loading, empty, error and recovery states where relevant. Use existing libraries and platform conventions without imposing one.
- Design responsive layouts around content, interaction and navigation, not only shrinking dimensions. Consider touch, keyboard, orientation, safe areas, text scaling and data density as relevant.
- For Android consider current Material guidance, native navigation and optional dynamic color when appropriate; preserve fixed brand identity when required. For iOS consider current Apple Human Interface Guidelines, Dynamic Type, safe areas, gestures and native navigation. Share identity and tokens where useful while adapting interaction per platform; do not impose Android conventions on iOS or vice versa.
- Apply relevant WCAG and platform accessibility guidance, with an explicit target where relevant. Check actual foreground/background pairs, component contrast, focus, semantics, labels, keyboard and screen readers, touch targets, motion preferences, text scaling and non-color feedback as applicable. Record criterion, method and evidence; do not claim compliance from automated checks alone.
- Consider sensitive data exposure, authorization states, safe errors and session interactions. A hidden or disabled control is not an authorization mechanism; refer security assessment to the specialist capability.

### JAC identity and sources

When JAC is selected or is the default, read the [JAC reference index](references/jac/REFERENCE-INDEX.md) first, then the specialized brand, palette and UI documents and the v4 HTML visual catalog as relevant. For conflicts in identity/logo, colors/tokens or component/technology guidance, use the respective specialized document as authority and report the discrepancy. The catalog is the primary visual and interactive reference, not mandatory production code. Do not copy its styles or dependencies indiscriminately. For a requested JAC component catalog, adapt the existing catalog as an authorized starting point, covering relevant light/dark examples; do not modify the bundled reference merely to fulfill a project request.

Use official provided artwork appropriate to context; respect aspect ratio, clear space and identity. Check provenance in the index: approximate vectorizations are not original master vectors; unconfirmed variants must not be represented as approved. Never recreate a supplied official logo, substitute a generic skull, or treat a banner as a logo or a default enterprise background. If the required master or variant is missing, state the gap instead of inventing it.

For JAC iconography, consult the [iconography guidelines](references/jac/JAC-ICONOGRAPHY.md) when selecting or implementing icons. Reserve the JAC emblem for identity; use consistent functional icons from the project's existing, platform-compatible family. Treat suggested packages and semantic mappings as options, not dependencies; verify exports and versions. Use semantic theme colors, hide decorative icons from assistive technology, and give icon-only controls accessible names and appropriate target sizes. Create custom icons only when existing assets or icons do not meet a documented need.

Use the palette's semantic light/dark colors, typography, spacing and radius guidance when JAC applies. Separate brand colors from functional roles; add only needed semantic roles such as focus, disabled, info or warning if missing, document them as derived, and validate their actual foreground/background pairs. Do not rename existing tokens without authorization. Support system and custom themes when requested; dark presentation is not mandatory. Target WCAG 2.2 AA for applicable JAC UI, without claiming conformance without evidence.

### Technology selection

Inspect existing project dependencies, framework, architecture and conventions first; preserve them unless a migration is requested. For a new React or Next.js project with no established UI stack or explicit preference, default to Tailwind CSS with shadcn/ui when a component stack is needed and compatible. Use PrimeReact when explicitly requested, or another explicitly selected stack; do not introduce either for a task that does not need it. For Angular, consider PrimeNG when appropriate and compatible. For React Native and Expo use native-compatible components; never import PrimeReact, PrimeNG or shadcn/ui web components into React Native. Adapt other ecosystems without forcing a framework or introducing unnecessary dependencies. Confirm installed versions and APIs, and share semantic tokens across platforms only where appropriate.

## Constraints

- Do not impose a framework, library, universal token hierarchy, full design system, project structure, documentation package or dependency. JAC is the fallback only when no other identity is established; never impose it on an existing or explicitly branded product. Respect established choices and avoid unrelated business logic changes or wholesale rewrites.

For practical token, component and platform checks, read [Design guidance](references/design-guidance.md) when relevant. For the supplied palette, read the [optional theme example](examples/optional-theme.md) only when selected or useful as an illustration.

## Composition

- Consume `agentic-project-setup` context and local instructions without recreating setup.
- Use `requirements-engineering` stories, rules and acceptance criteria; retain traceability where useful and do not change requirements without authorization.
- Feed UI states, flows and validation evidence to `spec-driven-development` without duplicating its change lifecycle.
- Respect `software-architecture-design` decisions and module boundaries; hand architecture decisions back when needed.
- Refer specialized security assessment to `application-security-review`; UI visibility is not a security control.

These handoffs are optional; do not claim another Skill ran merely because its outputs were used.

## Quality criteria

The result is ready when applicable criteria are supported by evidence:

- [ ] The requested task, relevant flows, interactions and states are addressed.
- [ ] Existing identity, architecture and appropriate assets are respected.
- [ ] JAC is applied only when selected or no other identity exists; source conflicts and missing artwork are disclosed.
- [ ] The interface adapts to relevant platforms, sizes and themes.
- [ ] Visual direction fits the product, audience and platform; hierarchy, typography, composition, density and brand use support the main task.
- [ ] Repeated cards, borders, effects, small text and empty space are justified by content and usability; issues observed in visual review are corrected or reported.
- [ ] Accessibility considerations are addressed with appropriate evidence.
- [ ] Colors and themes are coherent, and token and component changes preserve intended compatibility.
- [ ] No unnecessary structures or dependencies were introduced.
- [ ] Audit findings distinguish observations, risks and unassessed areas.

## Validation

1. Check the deliverable against the requested scope, relevant flows, states and existing design conventions.
   Check identity precedence, asset provenance and actual source conflicts; for a non-JAC identity check that JAC tokens and marks do not leak into the result.
2. When rendering tools are available, inspect the main screens at relevant desktop, tablet and mobile sizes and in supported themes. Review hierarchy, section differentiation, readability, spacing, repeated surfaces, visual effects, brand expression, navigation, forms, states and overflow; correct in-scope defects and recheck. Distinguish screenshots or DOM checks from visual inspection. If a platform, tool or screen was unavailable, report it explicitly.
3. Check applicable accessibility criteria with available manual and automated methods; record the target, method and evidence.
4. Verify affected token and component consumers and compatibility where relevant; review new dependencies and structures.
5. For a Figma deliverable, verify the editable file and intended frames when access permits.
6. Report actual checks, environments, themes, viewports and assistive technologies tested, along with failures, constraints and untested areas. A design or static inspection alone does not prove runtime behavior or accessibility conformance.
