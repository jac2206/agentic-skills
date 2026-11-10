# Optional light and dark palette

Illustrative user-provided reference only; use only when selected or otherwise appropriate, never as the default. Existing names and values are preserved for compatibility. Verify actual pairings and interactive states; define an appropriate `onPrimary` if needed. For a new system `textPrimary` may be clearer than `textDark`, but do not rename existing tokens without authorization. Propose any contrast changes rather than silently modifying this palette.

```typescript
export const lightColors = {
  primary: "#2563EB", secondary: "#3B82F6", background: "#F6F8FC",
  surface: "#FFFFFF", surfaceMuted: "#EEF4FF", textDark: "#172033",
  textMuted: "#64748B", border: "#D9E1EE", white: "#FFFFFF",
  success: "#15803D", successSurface: "#DCFCE7", error: "#B42318",
  errorSurface: "#FEE4E2", accent: "#6D28D9",
};
export const darkColors = {
  primary: "#60A5FA", secondary: "#3B82F6", background: "#0F172A",
  surface: "#1E293B", surfaceMuted: "#263449", textDark: "#F8FAFC",
  textMuted: "#94A3B8", border: "#334155", white: "#FFFFFF",
  success: "#4ADE80", successSurface: "#14532D", error: "#F87171",
  errorSurface: "#450A0A", accent: "#A78BFA",
};
```
