---
name: ui-ux-design-system
description: >
  Designs, implements, audits, and evolves user interfaces and design systems
  across web and mobile, adapting to the product, existing stack, brand, and
  accessibility needs without prescribing a visual style or technology.
metadata:
  version: "1.1.1"
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

- For a request to design screens or flows, create a reviewable HTML prototype by default when no output format is specified. Use the existing project's conventions or its designated artifact location; otherwise use an appropriate non-root output location. Keep it proportionate to the requested scope, usable locally when practical, and clearly identify simulated interactions or placeholder data. Demonstrate relevant screens, navigation, states and responsive behavior without inventing business functionality. A prototype is not production implementation.
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
2. **Determine scope and identity.** Prioritize explicit user colors, themes and preferences; existing design system; brand; supplied references; then a context-specific proposal. Resolve conflicts explicitly: honor a direct request while identifying affected consistency or accessibility tradeoffs. Do not silently replace supplied colors. If no identity exists, propose a suitable distinctive direction and explain principal choices; do not default to a fixed palette or trend.
3. **Design proportionately.** Map relevant requirements to screens and flows. Define navigation, hierarchy, responsive adaptations, components, states, feedback, error prevention and recovery as needed. Reuse existing patterns; create only missing foundations or components. Produce the visual deliverables above when applicable. Consider usability, accessibility, visual quality, performance and maintainability together. Use optional presets as inspiration, never as mandatory templates.
4. **Implement when requested.** Inspect and follow the existing stack and architecture. Reuse components and semantic tokens, preserve business behavior and state, and avoid duplicating styles, dependencies or components. Apply changes incrementally; consider compatibility and downstream consumers before changing tokens or public components. Do not rename existing tokens without authorization. Include appropriate tests when valuable.
5. **Validate and report.** Match checks to scope and risk. Inspect actual combinations and states across relevant sizes and themes, and run available project checks. Where tools permit, open and inspect the HTML prototype or app, including navigation, forms, errors and overflow. For a Figma deliverable, verify that the actual editable file and intended frames exist when access permits. Check relevant accessibility criteria using automated and manual methods where available. Report artifact paths or links, exact evidence, checks and untested areas; never claim visual inspection, conformance, a Figma file, or test execution without evidence.

## Rules

- Prioritize usability, consistency, accessibility, hierarchy, clarity, brand, reuse, adaptability, maintainability, performance and visual finish. Avoid unnecessary visual effects or workflow steps. Do not invent functionality.
- Define tokens only at useful scale. Prefer semantic names; separate primitive, semantic and component levels when they add value. Avoid scattered hardcoded colors; adapt token formats to the existing technology. Preserve compatibility during evolution.
- Respect requested light and dark themes, mapping semantic roles consistently across surfaces, text, controls, charts, feedback and overlays. Support system preference with the framework's appropriate mechanism when requested; consider custom branding or white label only when needed. Never require dark mode.
- Consider purpose, variants, sizes, relevant states, interaction, accessibility, themes and responsive behavior for each component; don't create a catalog by default. Include loading, empty, error and recovery states where relevant. Use existing libraries and platform conventions without imposing one.
- Design responsive layouts around content, interaction and navigation, not only shrinking dimensions. Consider touch, keyboard, orientation, safe areas, text scaling and data density as relevant.
- For Android consider current Material guidance, native navigation and optional dynamic color when appropriate; preserve fixed brand identity when required. For iOS consider current Apple Human Interface Guidelines, Dynamic Type, safe areas, gestures and native navigation. Share identity and tokens where useful while adapting interaction per platform; do not impose Android conventions on iOS or vice versa.
- Apply relevant WCAG and platform accessibility guidance, with an explicit target where relevant. Check actual foreground/background pairs, component contrast, focus, semantics, labels, keyboard and screen readers, touch targets, motion preferences, text scaling and non-color feedback as applicable. Record criterion, method and evidence; do not claim compliance from automated checks alone.
- Consider sensitive data exposure, authorization states, safe errors and session interactions. A hidden or disabled control is not an authorization mechanism; refer security assessment to the specialist capability.

## Constraints

- Do not impose a framework, library, palette, aesthetic, universal token hierarchy, full design system, project structure, documentation package or dependency. Respect established choices and avoid unrelated business logic changes or wholesale rewrites.

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
- [ ] The interface adapts to relevant platforms, sizes and themes.
- [ ] Accessibility considerations are addressed with appropriate evidence.
- [ ] Colors and themes are coherent, and token and component changes preserve intended compatibility.
- [ ] No unnecessary structures or dependencies were introduced.
- [ ] Audit findings distinguish observations, risks and unassessed areas.

## Validation

1. Check the deliverable against the requested scope, relevant flows, states and existing design conventions.
2. Inspect actual layouts, navigation, forms, errors, overflow, themes and responsive behavior where tools permit.
3. Check applicable accessibility criteria with available manual and automated methods; record the target, method and evidence.
4. Verify affected token and component consumers and compatibility where relevant; review new dependencies and structures.
5. For a Figma deliverable, verify the editable file and intended frames when access permits.
6. Report actual checks, environments, themes, viewports and assistive technologies tested, along with failures, constraints and untested areas. A design or static inspection alone does not prove runtime behavior or accessibility conformance.
