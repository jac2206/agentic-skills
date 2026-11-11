# JAC Iconography Guidelines

> **Brand:** JAC — The Tech Pirate  
> **Status:** Design decision  
> **Scope:** Web, mobile, documentation, presentations, and AI-generated interfaces  
> **Principle:** Preserve the JAC identity; use lightweight, consistent, platform-appropriate UI icons.

## 1. Decision

JAC adopts a **hybrid iconography system**:

1. **Brand identity assets** are JAC-specific and must come from the existing asset library.
2. **Functional and thematic icons** should come from maintained, lightweight icon libraries supported by the target platform.
3. **Custom illustrations or icons** are created only when a specific product or communication need cannot be served adequately by existing assets or a standard icon library.

This decision avoids duplicating the Jolly Roger across every UI icon, minimizes bundle overhead, and keeps web and mobile experiences consistent without requiring identical implementation libraries.

## 2. Brand Assets: Source of Truth

The JAC Jolly Roger is the established identity. It must **not** be regenerated, redrawn, or replaced with a generic pirate or skull icon.

Preferred existing raster assets include:

- `assets/Avatar pirata con calavera y huesos cruzados.png` — supplied raster isotype; the JAC Lealtad prototype uses an unchanged copy named `jac-isotype.png`.
- `assets/JAC-favicon-512.png` — existing favicon/app-mark reference.
- `assets/JAC-favicon.ico` — existing browser favicon.

Existing vector approximations include:

- `assets/jac-isotipo-dark.svg`
- `assets/jac-isotipo-transparent.svg`
- `assets/jac-logo-completo.svg`
- `assets/jac-favicon.svg`
- `assets/jac-wordmark.svg`

**Asset provenance:** These SVG files are approximate vectorizations, not confirmed original master vectors. Do not describe them as approved master artwork or replace higher-fidelity originals without visual review. Choose a suitable existing asset for the target size, background, and platform.

Never add a pirate hat, change facial details, alter the crossed bones, or substitute a newly generated Jolly Roger. Do not place the brand symbol on every functional icon.

## 3. Recommended Libraries by Platform

| Context | Preferred approach | Alternatives / notes |
| --- | --- | --- |
| React / Next.js | `lucide-react` with named imports | Tabler Icons or Heroicons when already used by the project |
| React Native / Expo | `@expo/vector-icons` using a consistent family, e.g. Feather or Ionicons | Follow the existing Expo-compatible icon stack when available |
| Other web frameworks | Framework-compatible SVG/icon package | Choose maintained equivalents; do not add React-only libraries |
| Documentation and presentations | Standard SVG symbols or established icon library | Export only the icons actually used; avoid embedding whole icon collections |

**Framework-agnostic rule:** Do not impose Lucide, Expo, Tailwind, shadcn/ui, or any other library on an existing project solely to apply JAC branding. Respect the project's current technology and dependency choices.

## 4. Suggested Semantic Icon Map

Use these meanings as a visual vocabulary, not as a hard requirement for identical icon names across libraries.

| Category | Web / Lucide suggestion | Mobile-equivalent concept |
| --- | --- | --- |
| Software architecture | `layers-3` or `blocks` | Layers / cubes |
| Cloud computing | `cloud` | Cloud |
| AI / GenAI | `brain` or `sparkles` | Brain / sparkles |
| AI agents | `bot` | Robot |
| DevOps / workflows | `workflow` or `infinity` | Workflow / infinite loop |
| Software development | `code-2` | Code |
| Databases / data | `database` | Database |
| Security | `shield-check` | Shield / check |
| Projects | `rocket` | Rocket |
| Documentation / articles | `book-open` | Open book |
| Presentations | `presentation` | Presentation screen |
| Platforms / modules | `boxes` | Stacked boxes |
| Integrations | `network` or `plug` | Connected nodes / plug |
| Goals | `target` | Target |
| Exploration | `compass` | Compass |

Check the installed icon package for actual exported icon names before implementation. Where a named icon is absent, select the closest semantic equivalent rather than adding an incompatible dependency.

## 5. Visual Rules

- **Style:** clean, modern, technical, minimal, and legible at small sizes.
- **Consistency:** favor one visual family per interface; keep stroke widths, optical sizes, and alignment consistent.
- **Brand palette:** Electric Cyan `#00B8F0`, Deep Blue `#1E40AF`, Navy `#0B1E3C`, Off White `#F8FAFC`, and restrained Gold `#FFCC15`.
- **Theming:** use semantic design tokens for icon colors rather than hardcoded values in every component. Check contrast in light and dark modes.
- **Accessibility:** decorative icons are hidden from assistive technologies; interactive icon-only controls receive accessible names and adequate touch targets.
- **Performance:** prefer tree-shakeable imports, local app assets, and platform-appropriate vector rendering. Avoid large icon sprites, unnecessary image requests, and high-resolution raster icons in routine controls.
- **Brand separation:** reserve the Jolly Roger for brand/signature contexts (such as app identity, profile, headers, or splash screens), not every category tile.

## 6. Usage Examples

### React / Next.js

```tsx
import { Brain, Cloud, Database, ShieldCheck } from "lucide-react";

export function TechnologyCategories() {
  return (
    <nav aria-label="Technology categories">
      <Cloud aria-hidden="true" />
      <Brain aria-hidden="true" />
      <Database aria-hidden="true" />
      <ShieldCheck aria-hidden="true" />
    </nav>
  );
}
```

For real application navigation, provide visible labels or accessible names for each actionable item; the example above only illustrates imports.

### React Native / Expo

```tsx
import { Feather } from "@expo/vector-icons";

export function CloudIcon() {
  return <Feather name="cloud" size={24} color="#00B8F0" />;
}
```

In production, read the icon color from the app's semantic theme tokens instead of hardcoding the brand value shown for illustration.

## 7. Rules for JAC AI Skills

When a skill generates a JAC-branded page, application, document, or presentation:

1. Read the JAC Brand Guidelines, Color Palette, UI Guidelines, and relevant Design System references.
2. Reuse original identity assets from `assets/` instead of generating a new logo.
3. Inspect the existing project stack and its installed icon packages before adding dependencies.
4. Prefer standard, lightweight icons for features, navigation, and technical categories.
5. Apply JAC semantic colors and the current theme without forcing cyan onto every icon.
6. Do not add the Jolly Roger to each thematic or functional icon.
7. Create new custom icon artwork only for a documented requirement and after checking existing alternatives.
8. Validate visual consistency, contrast, accessibility, responsive display, and mobile performance.

## 8. Explicit Non-Goals

- Creating an entire custom icon library for common UI actions.
- Redesigning the JAC Jolly Roger or the existing favicon.
- Requiring the same icon library across every framework.
- Bundling the full icon set when only a small selection is needed.
- Treating generated icon-suite mockups as approved master brand assets.

## 9. Related References

- `JAC-BRAND-GUIDELINES-FINAL-v2.md`
- `JAC-COLOR-PALETTE.md`
- `JAC-UI-GUIDELINES.md`
- `JAC-DESIGN-SYSTEM-v4.html`
- `REFERENCE-INDEX.md`
- `assets/`

**Outcome:** JAC stays recognizable through its original Jolly Roger while web and mobile products use practical, coherent, lightweight iconography.
