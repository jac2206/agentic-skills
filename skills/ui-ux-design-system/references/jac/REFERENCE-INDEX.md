# JAC reference index

Read this index when JAC is explicitly selected or is the fallback selected by the Skill. The bundled guidance has been aligned with that rule; an explicit or existing non-JAC identity still takes precedence.

## Sources and precedence

- [Brand guidelines](JAC-BRAND-GUIDELINES-FINAL-v2.md): identity, logo treatment, personality and voice.
- [Color palette](JAC-COLOR-PALETTE.md): authoritative brand colors, semantic themes, typography, spacing, radii and contrast guidance.
- [UI guidelines](JAC-UI-GUIDELINES.md): component, platform and technology guidance, adapted to the project's actual stack.
- [Iconography guidelines](JAC-ICONOGRAPHY.md): consult for JAC brand artwork, functional icons, platform-compatible icon families, accessibility and performance. Existing project icon conventions take precedence over suggested packages.
- [Design system v4](JAC-DESIGN-SYSTEM-v4.html): primary visual and interaction catalog, illustrative rather than production code.
- [Original asset notes](README.md): states that the named SVG family are approximate vectorizations, not original master vectors. [Brand CSS](jac-brand-tokens.css) preserves five legacy brand variables and provides opt-in semantic tokens via `data-jac-theme="light"` or `data-jac-theme="dark"`; the palette is the authoritative source. An application must choose and apply its own theme, including system preference when needed. The supplied identity-board image shows different cyan and gold values; follow the palette and disclose the discrepancy where relevant.

The palette does not define every requested semantic role. Derive missing roles only for a concrete need, document them as additions and test contrast; do not claim they are official tokens. The UI guidance is authoritative for technology selection, subject to the current request and project evidence.

## Artwork inventory

All supplied images and SVGs are under [assets](assets/). The following are supplied raster artwork, not automatically interchangeable master logo files:

- [Circular avatar](assets/Avatar%20pirata%20con%20calavera%20y%20huesos%20cruzados.png), [neon isotype](assets/Calavera%20Ne%C3%B3n%20con%20Gafas%20y%20Huesos.png), [emblem with wordmark](assets/Emblema%20JAC%20con%20Calavera%20y%20Huesos%20Cruzados.png), and [favicon PNG](assets/JAC-favicon-512.png) / [ICO](assets/JAC-favicon.ico).
- [Brand identity board](assets/Panel%20de%20Identidad%20Tecnol%C3%B3gica%20JAC.png) and supplied banners [cloud/AI](assets/Arquitectura%20Cloud%20e%20IA%20en%20Alta%20Mar.png) and [software architect](assets/Arquitecto%20de%20Software_%20JAC%20en%20Ne%C3%B3n.png) are reference or communication artwork, not master logo files.
- The SVGs `jac-isotipo-dark.svg`, `jac-isotipo-transparent.svg`, `jac-logo-completo.svg`, `jac-favicon.svg` and `jac-wordmark.svg` are identified in the source asset notes as approximate vectorizations; do not describe them as original master artwork. The provenance and approval status of `JAC-logo-principal.svg` are not established by those notes. Inspect an asset for suitability before use. An approved original master vector, a confirmed monochrome version and an approved light-background master are not identified in the supplied inventory; request them when required rather than inventing them.
