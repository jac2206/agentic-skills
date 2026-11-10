# Design guidance

Use only the sections relevant to the product and task. Verify current authoritative standards and platform guidance when their exact version or conformance is material: [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/), [Material Design](https://m3.material.io/), and [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/).

## Foundations and tokens

Inventory existing values and consumers before introducing tokens. Use primitive values for base colors, typography, spacing, size, radius and elevation; semantic aliases for purpose; and component aliases only when needed. Map applicable roles such as primary, secondary, accent, background, surface, text, border, feedback, on-primary, focus, disabled and overlay. Small changes need only the roles they use. Record theme mappings and test real foreground/background combinations, including interactive states. Respect supplied values and existing names; propose, rather than silently apply, accessibility adjustments.

Define typography family, hierarchy, weight, size, line height and numeric treatment as needed, preserving brand and dynamic text scaling. Establish appropriate spacing, grid, containers, breakpoints and safe areas based on content and existing conventions. Use shape, shadow, opacity, blur and motion deliberately; honor reduced motion. Avoid unnecessary effects.

## Components and flows

Inventory existing library and application components first. For each needed component define its purpose, variations, content, behavior, semantic roles, relevant states, platform adaptations, theme and interaction contract. Examples include forms, navigation, dialogs, tables, feedback, loaders and data visualizations. Reuse or extend before introducing a new component. Address empty, loading, error, success, validation, confirmation and recovery states only where relevant. Keep forms understandable and preserve data when errors occur. Consider content hierarchy, onboarding and task completion without adding unrequested functionality.

## Platform and verification

At relevant widths and orientations inspect layouts, navigation changes, overflow, touch and keyboard operation, safe areas and density. On Android consider Material patterns and dynamic color only if appropriate; on iOS consider native navigation, Dynamic Type and system conventions. Cross-platform identity does not require identical layouts or interaction. Check charts and interactive controls in every supported theme, including focus and error states.

For accessibility, select applicable WCAG level/version and platform criteria with the project. Measure contrast for actual rendered color pairs and states; review semantics, labels, focus order and visibility, keyboard, assistive technology, target sizes, text scaling, reduced motion and feedback beyond color. Automated checks cannot establish full conformance. Document method, environment, evidence and gaps. If a tool or platform is unavailable, mark the check unperformed.
