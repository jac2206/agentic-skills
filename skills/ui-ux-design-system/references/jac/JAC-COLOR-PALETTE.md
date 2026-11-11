# JAC — Color Palette & Design Tokens

> Official design token reference  
> Brand: **JAC**  
> Version: **1.0**  
> Scope: Web applications, mobile applications, documentation, and presentations

## 1. Purpose

This document defines JAC's official brand colors, semantic theme colors, typography, spacing, and shape tokens. It is the source of truth for color and token selection whenever JAC is selected, including as a fallback. For brand identity and logo usage, refer to `JAC-BRAND-GUIDELINES-FINAL-v2.md`; for component implementation rules, refer to `JAC-UI-GUIDELINES.md`; use `JAC-DESIGN-SYSTEM-v4.html` as the visual reference.

## 2. Core Brand Palette

| Token | Hex | Intended use |
|---|---|---|
| Electric Cyan | `#00B8F0` | Primary brand identity; highlights on dark backgrounds |
| Deep Blue | `#1E40AF` | Secondary brand color |
| Navy Blue | `#0B1E3C` | Dark surfaces, backgrounds, brand framing |
| Off White | `#F8FAFC` | Light content and backgrounds |
| Gold | `#FFCC15` | Optional, restrained accent |

The core palette represents the brand; semantic UI colors can vary by theme to ensure readability and accessible contrast. In particular, the light-theme interactive primary is a darker cyan (`#007EA8`) rather than the brighter brand cyan.

## 3. Light Theme

| Token | Hex | Usage |
|---|---|---|
| `primary` | `#007EA8` | Primary actions and links |
| `secondary` | `#1E40AF` | Secondary emphasis |
| `background` | `#F6F9FC` | Application background |
| `surface` | `#FFFFFF` | Cards and elevated content |
| `surfaceMuted` | `#EAF7FD` | Subtle highlighted surfaces |
| `textDark` | `#0B1E3C` | Main text (legacy token name) |
| `textMuted` | `#52657B` | Secondary text |
| `border` | `#D8E5EE` | Borders and dividers |
| `white` | `#FFFFFF` | Absolute white |
| `success` | `#15803D` | Success indicators |
| `successSurface` | `#DCFCE7` | Success backgrounds |
| `error` | `#B42318` | Error indicators |
| `errorSurface` | `#FEE4E2` | Error backgrounds |
| `accent` | `#B38600` | Optional accent |

## 4. Dark Theme

| Token | Hex | Usage |
|---|---|---|
| `primary` | `#00B8F0` | Primary highlights and actions |
| `secondary` | `#60A5FA` | Secondary emphasis |
| `background` | `#071323` | Application background |
| `surface` | `#0B1E3C` | Cards and panels |
| `surfaceMuted` | `#142B49` | Subtle highlighted surfaces |
| `textDark` | `#F8FAFC` | Main text (legacy token name) |
| `textMuted` | `#A4B7CA` | Secondary text |
| `border` | `#29435F` | Borders and dividers |
| `white` | `#FFFFFF` | Absolute white |
| `success` | `#4ADE80` | Success indicators |
| `successSurface` | `#14532D` | Success backgrounds |
| `error` | `#F87171` | Error indicators |
| `errorSurface` | `#450A0A` | Error backgrounds |
| `accent` | `#FFCC15` | Optional accent |

## 5. TypeScript Color Definitions

```typescript
export const lightColors = {
  primary: "#007EA8",
  secondary: "#1E40AF",
  background: "#F6F9FC",
  surface: "#FFFFFF",
  surfaceMuted: "#EAF7FD",
  textDark: "#0B1E3C",
  textMuted: "#52657B",
  border: "#D8E5EE",
  white: "#FFFFFF",
  success: "#15803D",
  successSurface: "#DCFCE7",
  error: "#B42318",
  errorSurface: "#FEE4E2",
  accent: "#B38600",
};

export const darkColors: typeof lightColors = {
  primary: "#00B8F0",
  secondary: "#60A5FA",
  background: "#071323",
  surface: "#0B1E3C",
  surfaceMuted: "#142B49",
  textDark: "#F8FAFC",
  textMuted: "#A4B7CA",
  border: "#29435F",
  white: "#FFFFFF",
  success: "#4ADE80",
  successSurface: "#14532D",
  error: "#F87171",
  errorSurface: "#450A0A",
  accent: "#FFCC15",
};

export type ThemeMode = "light" | "dark";
export type ThemeColors = typeof lightColors;
export type ColorToken = keyof ThemeColors;

export const themes: Record<ThemeMode, ThemeColors> = {
  light: lightColors,
  dark: darkColors,
};

export const brandColors = {
  cyan: "#00B8F0",
  blue: "#1E40AF",
  navy: "#0B1E3C",
  white: "#F8FAFC",
  gold: "#FFCC15",
} as const;
```

`textDark` is retained for compatibility with the initial JAC theme API. It means **primary text** in both themes, including dark mode.

## 6. Typography

| Purpose | Font family | Recommended weights |
|---|---|---|
| Brand and headings | Montserrat | 600, 700, 800 |
| UI and body text | Inter | 400, 500, 600 |
| Code and technical content | JetBrains Mono | 400, 500 |

```typescript
export const typography = {
  fontFamily: {
    heading: "Montserrat",
    body: "Inter",
    mono: "JetBrains Mono",
  },
  fontWeight: {
    regular: "400",
    medium: "500",
    semibold: "600",
    bold: "700",
    extrabold: "800",
  },
  fontSize: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 20,
    h3: 24,
    h2: 30,
    h1: 36,
    display: 48,
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.7,
  },
} as const;
```

The `lineHeight` values above are **unitless multipliers for web CSS**. React Native expects absolute line-height values; multiply the selected font size by the desired ratio.

## 7. Spacing and Radius Tokens

```typescript
export const designTokens = {
  spacing: {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    "2xl": 32,
    "3xl": 48,
  },
  radius: {
    sm: 6,
    md: 10,
    lg: 16,
    xl: 24,
    full: 9999,
  },
  typography,
  colors: themes,
} as const;
```

Spacing and radius values are expressed in pixels for web implementations and density-independent layout units for React Native, subject to platform conventions.

## 8. Accessibility and Usage Rules

- Target **WCAG 2.2 AA** for applicable UI components.
- Maintain at least **4.5:1** contrast for normal text and **3:1** for large text.
- Check **3:1 non-text contrast** for meaningful UI boundaries and states where required.
- Do not assume a brand color is automatically accessible in every foreground/background combination. Validate each pairing.
- Prefer `primary` and semantic tokens over hardcoded brand colors in application components.
- Use a dark foreground on bright cyan buttons in dark mode when white text does not meet contrast requirements.
- Never rely on color alone to convey errors, success, or status.
- Keep visible focus states and adequate interactive target sizes.
- Use gold sparingly, not as the primary call-to-action color.
- Do not add unrelated colors to JAC-branded experiences without a documented product-level need.

## 9. Implementation Guidance for AI Skills

When JAC is explicitly selected or used as the fallback because no other identity is established:

1. Read `JAC-BRAND-GUIDELINES-FINAL-v2.md` for identity rules.
2. Use this document as the canonical source for colors, typography, spacing, and radii.
3. Read `JAC-UI-GUIDELINES.md` for component and library conventions.
4. Implement semantic tokens for both light and dark modes.
5. Reuse official logo assets instead of recreating the logo.
6. Validate accessible color pairings in the final UI.
7. Preserve explicit or existing non-JAC identities and do not mix them with JAC.

Do not copy the token tables into multiple independent sources of truth. The application may translate these tokens into CSS variables, Tailwind theme variables, or React Native theme objects while preserving their semantic meaning.

---

**JAC — Official Color Palette & Design Tokens · v1.0**
