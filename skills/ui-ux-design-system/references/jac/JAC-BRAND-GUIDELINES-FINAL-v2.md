# JAC — Brand Guidelines

> **Brand:** JAC  
> **Concept:** The Tech Pirate  
> **Version:** 1.0  
> **Status:** Brand reference  
> **Language:** English

---

## 1. Brand Overview

**JAC** is a personal technology brand focused on software engineering, software architecture, cloud computing, artificial intelligence, automation, and digital product development.

The brand combines technical expertise, creativity, independent thinking, and a commitment to solving real-world problems.

### Mission

Design and build useful, reliable, innovative technology solutions that simplify people's lives and generate meaningful value.

### Vision

Establish JAC as a recognizable technology identity associated with quality engineering, software architecture, artificial intelligence, and purposeful digital products.

### Brand personality

- **Technical:** precise, capable, and engineering-oriented.
- **Innovative:** curious, modern, and forward-looking.
- **Independent:** willing to explore new approaches.
- **Creative:** original without sacrificing usability.
- **Professional:** dependable and trustworthy.
- **Human-centered:** accessible and focused on real needs.
- **Minimalist:** clear, structured, and intentional.

## 2. Brand Concept — The Tech Pirate

The JAC identity draws inspiration from the adventurous, independent spirit of pirate symbolism through a **personalized Jolly Roger**.

The concept represents freedom to explore technology, curiosity, technical craftsmanship, and the courage to build original solutions. Pirate imagery should be stylized and professional, not aggressive or cartoonishly exaggerated.

**“The Tech Pirate” is a brand concept and optional tagline, not mandatory text on every asset.** Clean layouts, such as a minimal LinkedIn banner, may omit it.

## 3. Official Visual Identity

### 3.1 Jolly Roger

The recognizable JAC symbol is a stylized skull-like portrait with:

- Dark, swept-back hair.
- Round dark sunglasses.
- Distinctive beard and mustache.
- Small hoop earrings.
- Crossed bones behind the portrait.
- Strong outlines and white highlights.
- A circular electric-cyan frame on a deep navy background.

**Do not add a pirate hat or straw hat.**

### 3.2 Logo family

| Asset | Description | Preferred use |
|---|---|---|
| Primary logo | Jolly Roger with JAC wordmark | Portfolio, GitHub, presentations |
| Isotype | Jolly Roger without letters | Avatars, application icons, compact UI |
| Horizontal logo | Symbol beside JAC wordmark | Headers, navigation, signatures |
| Monochrome logo | Single-color official artwork | Printing and restricted-color applications |
| Favicon | Simplified official isotype | Browser tabs and bookmarks |

Use the **approved master artwork** for every export. Do not regenerate each variant independently or substitute a generic skull icon. Any variant that does not yet have an approved asset should be considered a proposed format, not an existing official file.

### 3.3 Logo protection and scaling

- Keep clear space around the logo, ideally at least 25% of the symbol width when layout permits.
- Preserve proportions and orientation.
- Maintain legibility at small sizes; simplify only from the approved master.
- Avoid cropping hair, bones, earrings, or the circular outline.
- Use high-resolution or vector source assets when available.
- Choose a background that preserves contrast.

### 3.4 Incorrect use

Do not stretch, recolor arbitrarily, add hats, change facial characteristics, apply excessive glow, place on visually noisy backgrounds, or redraw the symbol differently across products.

## 4. Official Brand Colors

The approved brand palette is:

| Name | HEX | Role |
|---|---|---|
| Electric Cyan | `#00B8F0` | Signature brand color and dark-theme highlights |
| Deep Blue | `#1E40AF` | Supporting technology color |
| Navy Blue | `#0B1E3C` | Dark surfaces and brand framing |
| Off White | `#F8FAFC` | Light surfaces and high-contrast text |
| Gold | `#FFCC15` | Restrained optional accent |

For complete light/dark semantic colors, accessibility combinations, and TypeScript tokens, **`JAC-COLOR-PALETTE.md` is the source of truth**.

In light interfaces, the accessible primary action token may differ from signature cyan; use the semantic theme token rather than forcing brand cyan on every button.

## 5. Typography

| Typeface | Purpose | Preferred weights |
|---|---|---|
| **Montserrat** | Brand titles, hero text, headings | 600, 700, 800 |
| **Inter** | UI labels, paragraphs, forms, documentation | 400, 500, 600 |
| **JetBrains Mono** | Code, terminal snippets, technical identifiers | 400, 500 |

Use consistent hierarchy, readable line heights, and restrained capitalization. Avoid decorative fonts and using monospace for long prose.

## 6. Visual Language

JAC interfaces should feel **modern, minimal, technical, confident, and approachable**.

### Composition

- Use clear hierarchy, generous whitespace, and consistent alignment.
- Favor responsive grids and predictable spacing.
- Use moderate corner radii, subtle borders, and controlled elevation.
- Use navy layers in dark mode instead of indiscriminate pure black.
- Keep electric cyan as a meaningful highlight, not a glow on every element.
- Reserve gold for selective emphasis.
- Use architecture and technology illustrations only when they improve understanding.

### Icons and imagery

Use coherent, simple iconography with consistent stroke weight. Product icons may use PrimeIcons or Lucide according to the platform design guidelines. Brand artwork must come from official assets, not icon libraries.

Pirate-themed visuals may appear in storytelling, banners, and campaign material; product interfaces should remain task-oriented and restrained.

## 7. Light and Dark Experiences

Both themes are official. Dark mode is particularly suitable for brand pages, technical portfolios, and presentation covers. Light mode is equally valid for forms, productivity tools, dashboards, and content-heavy screens.

Implement colors using semantic tokens from `JAC-COLOR-PALETTE.md`, not one-off hardcoded HEX values in components.

## 8. Product and UI Experience

JAC products should:

- Solve user problems with minimal unnecessary steps.
- Provide clear actions, feedback, and error recovery.
- Keep forms and navigation predictable.
- Support desktop, tablet, and mobile experiences.
- Provide loading, empty, error, success, and disabled states.
- Target **WCAG 2.2 AA** where applicable.
- Support keyboard navigation, visible focus, accessible labels, and reduced motion.
- Never communicate state through color alone.

Detailed component contracts, library choices, and implementation rules belong in **`JAC-UI-GUIDELINES.md`**, not in this brand document.

## 9. Brand Applications

### GitHub and developer profiles

Use the official logo or isotype, a clean navy/cyan visual language, and concise descriptions of technical expertise.

### Portfolio and personal website

Emphasize software architecture, cloud, AI and agents, technical leadership, and real-world digital products. Prefer clear project stories, diagrams, and outcomes over decorative effects.

### Web applications

Apply the same JAC tokens and visual principles while respecting the existing web stack, component conventions, and accessibility. Tailwind CSS with shadcn/ui and PrimeReact are supported options; follow the selection rules in the UI guidelines.

### Mobile applications

Share JAC colors, typography, icons, and experience principles, but use native-appropriate components for **React Native and Expo**. PrimeReact web components are not React Native components.

### Presentations and documentation

Use consistent headings, cyan highlights, readable diagrams, well-spaced layouts, and accurate technical explanations. Visual branding must never obscure content.

### LinkedIn and social banners

Prefer minimal, panoramic compositions with a legible JAC identity. A subtle pirate ship silhouette or nautical reference can support the theme without overwhelming professional messaging. The optional tagline may be omitted.

## 10. Brand Voice

JAC communication is **professional, direct, technically accurate, practical, and approachable**.

- Explain complex topics clearly.
- Use concrete examples and real-world context.
- Prefer substance over exaggerated marketing claims.
- Be confident without overpromising.
- Use Spanish or English according to the audience, keeping technical terms consistent.

## 11. Brand Architecture

JAC is the parent identity for personal projects, products, educational material, and technical content.

Individual products may have their own names and supporting visuals, but should preserve the recognizable JAC identity when presented as JAC products. Example names such as “JAC Finance” are illustrative, not approved product names.

JAC branding must **not** be imposed on unrelated client projects.

## 12. Integration with AI Skills

When JAC is explicitly selected or used as the fallback because no other identity is established, agents should:

1. Read this document for identity, personality, logo usage, and brand voice.
2. Read `JAC-COLOR-PALETTE.md` for exact colors, typography, and tokens.
3. Read `JAC-UI-GUIDELINES.md` for web/mobile implementation conventions.
4. Use approved artwork from the `assets/` directory.
5. Preserve consistency across pages, components, and deliverables.
6. Verify accessibility, responsive behavior, and visual states.
7. Treat `JAC-DESIGN-SYSTEM-v4.html` as the primary visual reference and illustrative playground, **not** as production component source code.
8. Avoid inventing or claiming unapproved logo assets, colors, or component implementations.

Preserve any explicit user identity or existing project identity; do not impose JAC on it.

## 13. Governance and Source of Truth

| Reference | Authority |
|---|---|
| `JAC-BRAND-GUIDELINES-FINAL-v2.md` | Identity, voice, logo and usage rules |
| `JAC-COLOR-PALETTE.md` | Exact color, typography and design tokens |
| `JAC-UI-GUIDELINES.md` | Component behavior, technology and implementation |
| Approved assets | Exact logo/isotype artwork |
| `JAC-DESIGN-SYSTEM-v4.html` | Visual examples and interaction demonstrations |

If references disagree, do not silently redefine the brand. Follow the specialized source for the disputed topic and flag the conflict for review.

Suggested directory:

```text
brand/
└── jac/
    ├── JAC-BRAND-GUIDELINES-FINAL-v2.md
    ├── JAC-COLOR-PALETTE.md
    ├── JAC-UI-GUIDELINES.md
    ├── JAC-DESIGN-SYSTEM-v4.html
    └── assets/
        └── [approved logo, isotype and favicon files]
```

## 14. Brand Principles

**Engineering excellence. Technology with purpose. Creative independence. Consistent design. Human-centered innovation.**

> **JAC — The Tech Pirate**  
> Build with purpose. Explore without limits.

---

*JAC Brand Guidelines · v1.0*
