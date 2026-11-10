---
name: ui-ux-design-system
description: >
  Designs, implements, audits, and evolves user interfaces and design systems
  across web and mobile, adapting to the product, existing stack, brand, and
  accessibility needs without prescribing a visual style or technology.
metadata:
  version: "1.0.0"
---

# UI/UX Design System

Design and maintain coherent, usable, accessible user experiences and their reusable visual foundations, proportionate to the requested work.

## When to use

Use for UI or UX design, interaction flows, visual identity, design tokens, themes, components, interface implementation, visual audits, or design-system maintenance for new or existing graphical products. Applicable to web, mobile, enterprise, dashboards, SaaS, fintech, and other interfaces.

## When not to use

Do not use for requirements ownership, technical architecture redesign, security audits, or change-lifecycle administration. Consume their outputs and hand off specialist work. Do not use for a purely backend change with no interface impact.

## Inputs and outputs

Required: the requested outcome or interface scope. Inspect available project evidence; ask only when a missing decision blocks safe or meaningful progress. Optional inputs include users, tasks, requirements and acceptance criteria, brand and visual references, platforms, accessibility targets, existing UI and architecture, stack, constraints, and available validation tools. Separate confirmed facts, assumptions, and pending decisions; do not invent business behavior.

Produce only deliverables appropriate to the request: analysis or evidence-based findings, visual/interaction specifications, tokens or components, implementation changes, or maintenance recommendations. Record relevant decisions, affected requirements, validation performed, findings, and limitations. Use the [UI specification template](templates/ui-specification.md) only when a written handoff adds value.

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
3. **Design proportionately.** Map relevant requirements to screens and flows. Define navigation, hierarchy, responsive adaptations, components, states, feedback, error prevention and recovery as needed. Reuse existing patterns; create only missing foundations or components. Consider usability, accessibility, visual quality, performance and maintainability together. Use optional presets as inspiration, never as mandatory templates.
4. **Implement when requested.** Inspect and follow the existing stack and architecture. Reuse components and semantic tokens, preserve business behavior and state, and avoid duplicating styles, dependencies or components. Apply changes incrementally; consider compatibility and downstream consumers before changing tokens or public components. Do not rename existing tokens without authorization. Include appropriate tests when valuable.
5. **Validate and report.** Match checks to scope and risk. Inspect actual combinations and states across relevant sizes and themes, and run available project checks. Where tools permit, run the app and inspect visually, including navigation, forms, errors and overflow. Check relevant accessibility criteria using automated and manual methods where available. Report exact evidence, checks and untested areas; never claim visual inspection, conformance, or test execution without evidence.

## Design and implementation rules

- Prioritize usability, consistency, accessibility, hierarchy, clarity, brand, reuse, adaptability, maintainability, performance and visual finish. Avoid unnecessary visual effects or workflow steps. Do not invent functionality.
- Define tokens only at useful scale. Prefer semantic names; separate primitive, semantic and component levels when they add value. Avoid scattered hardcoded colors; adapt token formats to the existing technology. Preserve compatibility during evolution.
- Respect requested light and dark themes, mapping semantic roles consistently across surfaces, text, controls, charts, feedback and overlays. Support system preference with the framework's appropriate mechanism when requested; consider custom branding or white label only when needed. Never require dark mode.
- Consider purpose, variants, sizes, relevant states, interaction, accessibility, themes and responsive behavior for each component; don't create a catalog by default. Include loading, empty, error and recovery states where relevant. Use existing libraries and platform conventions without imposing one.
- Design responsive layouts around content, interaction and navigation, not only shrinking dimensions. Consider touch, keyboard, orientation, safe areas, text scaling and data density as relevant.
- For Android consider current Material guidance, native navigation and optional dynamic color when appropriate; preserve fixed brand identity when required. For iOS consider current Apple Human Interface Guidelines, Dynamic Type, safe areas, gestures and native navigation. Share identity and tokens where useful while adapting interaction per platform; do not impose Android conventions on iOS or vice versa.
- Apply relevant WCAG and platform accessibility guidance, with an explicit target where relevant. Check actual foreground/background pairs, component contrast, focus, semantics, labels, keyboard and screen readers, touch targets, motion preferences, text scaling and non-color feedback as applicable. Record criterion, method and evidence; do not claim compliance from automated checks alone.
- Consider sensitive data exposure, authorization states, safe errors and session interactions. A hidden or disabled control is not an authorization mechanism; refer security assessment to the specialist capability.
- Do not impose a framework, library, palette, aesthetic, universal token hierarchy, full design system, project structure, documentation package or dependency. Respect established choices and avoid unrelated business logic changes or wholesale rewrites.

For practical token, component and platform checks, read [Design guidance](references/design-guidance.md) when relevant. For the supplied palette, read the [optional theme example](examples/optional-theme.md) only when selected or useful as an illustration.

## Composition

- Consume `agentic-project-setup` context and local instructions without recreating setup.
- Use `requirements-engineering` stories, rules and acceptance criteria; retain traceability where useful and do not change requirements without authorization.
- Feed UI states, flows and validation evidence to `spec-driven-development` without duplicating its change lifecycle.
- Respect `software-architecture-design` decisions and module boundaries; hand architecture decisions back when needed.
- Refer specialized security assessment to `application-security-review`; UI visibility is not a security control.

These handoffs are optional; do not claim another Skill ran merely because its outputs were used.

## Quality criteria and validation

The result is ready when it addresses the requested task and relevant flows and states, follows established identity and architecture, reuses appropriate assets, adapts to target platforms and sizes, and considers accessibility with evidence. Confirm that colors and themes remain coherent, token and component changes preserve intended compatibility, and no unnecessary structures or dependencies were introduced. For audits, separate observed findings from risks and unassessed areas. Report failures and constraints explicitly, and identify the actual checks, environments, themes, viewports and assistive technologies tested. A design or static inspection alone does not prove runtime behavior or accessibility conformance.
