---
name: html-presentations
description: >
  Creates presentation-grade, self-contained HTML slide decks with a consistent
  dark technology design system, visual composition patterns, responsive 16:9
  staging, navigation, animation, and overflow-safe layouts. Use when the user
  asks for a browser-based presentation, keynote, workshop, technical talk,
  educational deck, executive deck, or visual slide deck. Do not use for
  ordinary websites, dashboards, or non-HTML presentation formats.
metadata:
  version: "2.0.0"
---

# HTML Presentations

Create self-contained HTML presentations that behave like real slide decks rather
than vertically scrolling web pages. The deck must communicate a narrative,
explain ideas visually when useful, and remain reliable when presented directly
from a browser.

## Purpose

Transform a brief, topic, document, or set of ideas into a complete HTML deck
with:

- A clear narrative and one primary idea per slide.
- A 16:9 presentation stage based on 1600 x 900.
- A stable visual design system shared across the entire deck.
- Reusable layouts selected according to the content.
- Diagrams, code, UI mockups, statistics, or editorial compositions when they
  improve understanding.
- One visible slide at a time, keyboard controls, visible navigation, progress,
  fullscreen, responsive scaling, and controlled transitions.
- Optional speaker notes when they add presentation value.
- No external runtime dependency unless the user explicitly requests one.

## When to use

Use this Skill when the user asks to:

- Create or improve an HTML presentation or slide deck.
- Build a keynote, workshop, masterclass, technical talk, or educational deck.
- Turn documentation, research, or a topic into browser-presentable slides.
- Create an executive presentation with visual storytelling.
- Generate an interactive presentation with navigation and fullscreen support.

## When not to use

Do not use this Skill when the primary output is:

- A normal website, landing page, dashboard, or documentation site.
- A long-form article, PDF-only document, Word document, or spreadsheet.
- A PowerPoint, PPTX, or another non-HTML presentation format, unless HTML is
  explicitly requested as an intermediate artifact.

## Inputs

### Required

- Presentation topic, source material, or brief.
  - Preserve factual meaning and the user's requested language.
- Intended audience and objective when provided.
  - Infer a reasonable audience only when it is not specified.

### Optional

- Desired slide count or duration.
- Tone: technical, educational, executive, persuasive, or workshop-oriented.
- Content hierarchy, required sections, examples, metrics, code, or diagrams.
- Brand constraints, logos, images, or existing visual references.
- A custom theme palette, for example:

  ```text
  Background: #08111D
  Primary: #68E5DF
  Secondary: #A893FF
  Accent: #FFB76F
  ```

If no palette is supplied, use `default-theme` below. If a palette is partial,
derive the missing roles from the supplied colors while preserving contrast and
semantic state colors.

## Outputs

Produce a self-contained `.html` file that:

- Opens directly in a browser.
- Contains the complete HTML, CSS, SVG, and JavaScript needed to present it.
- Displays one slide at a time on a 16:9 stage.
- Provides previous/next controls, keyboard navigation, a slide counter or
  progress indicator, fullscreen, and responsive scaling.
- Includes speaker notes only when useful and keeps them out of the visual stage.
- Does not rely on vertical scrolling to move between slides.

When the user asks for a file, place it in the repository's appropriate
`examples/<category>/` directory or another user-specified location, never at
the repository root. Explain how to open and present it.

## Core Principles

### 1. Communication before content volume

Every slide has one primary idea, a clear title, a visible hierarchy, and only
the minimum text needed to support the idea. If content does not fit, reduce it,
split it into another slide, change the layout, or simplify the visual. Never
make text illegibly small merely to fit more content.

### 2. Visualize when visualization improves understanding

Ask whether the idea is better understood as text, a comparison, a diagram, a
sequence, a statistic, code, a UI mockup, a metaphor, or an editorial statement.
Use a visual representation when it makes relationships, dependencies, process,
architecture, decisions, or change easier to understand. Do not add diagrams or
cards merely to make a slide look busy.

### 3. Consistency is a system property

Treat the deck as one product. Reuse the same spacing, typography, surfaces,
borders, radii, footer, numbering, controls, motion language, and diagram style
across slides. A new deck should belong to the same visual family unless the
user explicitly requests a different theme.

### 4. Presentation first

Use discrete slides, not page sections pretending to be slides. The browser
viewport must show a single stage, and the deck must be usable with keyboard and
on-screen controls.

## Default Design System

Use this design system unless the user supplies a custom palette. Treat it as
the stable `default-theme`, not as a suggestion to invent a new style per deck.

- Stage: 1600 x 900, 16:9.
- Background: deep navy or charcoal with subtle tonal variation.
- Primary: cyan for key actions, active states, and important connections.
- Secondary: violet for supporting emphasis and secondary groups.
- Accent: orange for highlights, contrast, and calls to action.
- Semantic colors: pink, green, and red only when meaning requires them, such as
  status, success, warning, or error.
- Surfaces: dark translucent cards and panels used selectively.
- Treatment: subtle borders, restrained gradients, and restrained glows.
- Typography: modern, legible, high contrast, with a clear scale.
- Composition: editorial and technological, with generous negative space.
- Motion: smooth, short, and subordinate to reading and explanation.

### Custom palette rules

When the user provides colors:

1. Map them to semantic roles such as background, primary, secondary, and accent.
2. Derive tints, muted surfaces, borders, text colors, and glows from those roles.
3. Check contrast before applying them to text or small UI elements.
4. Keep semantic colors for success, warning, and error when needed; do not
   replace every semantic color with a brand color.
5. Apply the system consistently to backgrounds, diagrams, borders, controls,
   buttons, highlights, and animations.

Do not treat a palette as a list of unrelated hex values.

## Typography and Safe Area

Use a consistent hierarchy:

```text
H1       Cover or hero title
H2       Slide title
H3       Section or block heading
Lead     Short explanatory statement
Body     Main supporting content
Label    Metadata, tags, or small interface text
Caption  Secondary explanation or source
```

Choose sizes that remain readable at presentation distance. For a long title,
shorten or rephrase it first, then change its composition, then reduce its size
slightly within the established scale. Do not let a title force an illegible
layout.

Define a `slide-safe-area` inside the 1600 x 900 stage. Use consistent margins
for title, body, footer, controls, and visual content. Every positioned element,
including SVG nodes, labels, arrows, footer, and controls, must remain inside the
safe area unless it is an intentional background treatment.

## Visual Composition Engine

Before writing each slide, classify its dominant communication need and choose
the simplest suitable pattern. Available patterns include:

- `hero` / cover
- `statement` / central idea
- `split` content
- `grid-2` and `grid-3`
- `comparison`
- `timeline`
- `process-flow`
- `architecture`
- `system-diagram`
- `sequence-diagram`
- `decision-tree`
- `cycle`
- `layers`
- `pyramid`
- `matrix`
- `before-after`
- `funnel`
- `pipeline`
- `relationship-map` / `knowledge-graph`
- `code`
- `ui-mockup`
- `checklist`
- `metrics`
- `case-study`
- `closing`

Use cards only when the content is genuinely a set of parallel items. Do not
default every slide to a card grid. Layouts must reuse the same spacing,
typography, surfaces, borders, shadows, animation, footer, and numbering.

### Pattern selection guide

| Content relationship | Preferred pattern |
| --- | --- |
| One memorable idea | `statement`, editorial composition, or quote |
| Ordered steps or change over time | `process-flow`, `timeline`, or `sequence-diagram` |
| Architecture or dependencies | `architecture` or `system-diagram` |
| Alternatives or trade-offs | `comparison` or `matrix` |
| Branching choices | `decision-tree` |
| Repeating behavior | `cycle` |
| Hierarchy or abstraction | `layers`, `pyramid`, or `funnel` |
| Relationships among entities | `relationship-map` or `knowledge-graph` |
| Implementation detail | `code`, `ui-mockup`, or `split` |
| Evidence or outcomes | `metrics`, `case-study`, or `before-after` |
| Final takeaway | `closing` or `statement` |

The table guides decisions; it does not require a diagram when a simpler visual
communicates better.

## Diagram Rules

Use HTML, CSS, and SVG for diagrams so they remain self-contained and scale with
the stage. A diagram is appropriate when it clarifies relationships, process,
dependencies, architecture, sequence, hierarchy, or decisions.

When creating a diagram:

- Establish a clear reading direction and visual hierarchy.
- Align nodes to a grid and keep spacing generous.
- Use short labels and a small number of meaningful groups.
- Use directed arrows when direction matters.
- Avoid unnecessary crossings, overlapping lines, and ambiguous connectors.
- Use the active theme and no more than 3-5 semantic colors simultaneously.
- Keep density low enough that the main relationship is understandable in a few
  seconds.
- Prefer progressive reveal only when it helps explain the relationship.

Do not use diagrams by obligation. A powerful sentence, comparison, statistic,
quote, demonstration, code sample, UI mockup, or metaphor may be the better
visual treatment.

## Workflow

Execute this process before returning the HTML:

1. Understand the audience, objective, source material, constraints, and desired
   language.
2. Define the narrative arc: opening, development, and close.
3. Divide the material into slides and write one primary idea for each slide.
4. Choose or derive the design system. Use `default-theme` unless a custom
   palette is supplied, then validate its contrast and role mapping.
5. Classify each slide and select a reusable layout from the composition engine.
6. Decide whether each slide needs text, a diagram, a comparison, code, a UI,
   metrics, or another visual treatment.
7. Generate the stage, shared CSS tokens, reusable layout styles, slides, and
   navigation behavior.
8. Add controlled transitions and reveal animations. Include a
   `prefers-reduced-motion` alternative.
9. Validate content density, hierarchy, layout bounds, text fit, overlap, and
   consistency before considering the deck complete.
10. Open or render the deck when possible and inspect representative slides at
    the target 16:9 ratio. Fix visual issues rather than documenting them as
    limitations.

## Presentation Controls and Runtime

The generated deck must preserve these capabilities:

- Previous and next controls.
- Keyboard navigation, including left/right arrows and a sensible escape path
  from fullscreen.
- Current slide number and total slide count or equivalent progress.
- Fullscreen control when supported by the browser.
- Responsive scaling that preserves the 16:9 stage without introducing page
  scrolling between slides.
- A single visible slide at a time.
- Graceful behavior when JavaScript is unavailable or a control is unsupported,
  where practical.

Animations may use fade, slide, reveal, light scale, or meaningful diagram
motion. Keep them short and quiet. Respect:

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable or minimize non-essential motion. */
}
```

## Rules

The Skill must:

- Preserve the self-contained HTML, 16:9, navigation, fullscreen, responsive
  scaling, transitions, animations, controls, and optional speaker-note
  capabilities of the original Skill.
- Use the default design system consistently unless the user supplies a custom
  theme.
- Select layouts based on the idea and relationship being explained.
- Keep one primary idea, one clear title, and a visible hierarchy per slide.
- Prefer diagrams when they materially improve comprehension, but never add them
  merely for decoration.
- Reuse design tokens and layout primitives instead of inventing slide-specific
  styles without a reason.
- Validate the stage, safe area, text fit, diagrams, footer, controls, and
  consistency before delivery.

The Skill must not:

- Turn the deck into a vertically scrolling page.
- Change the visual identity arbitrarily from slide to slide or deck to deck.
- Make every slide a collection of cards.
- Force every concept into a diagram.
- Hide overflow, clip content, or reduce text until it is difficult to read.
- Use excessive colors, glows, gradients, or decorative animation.
- Allow titles, diagrams, controls, footers, or content to escape the stage.
- Add dependencies, external assets, or network calls unless the user requests
  them and the resulting deck remains presentable offline when feasible.

## Constraints

- Target stage: 1600 x 900, 16:9.
- All slide content must fit inside a consistent safe area.
- A slide should be split, simplified, or redesigned when it cannot fit clearly.
- Diagrams should use SVG/HTML/CSS and remain legible at presentation size.
- Use at most 3-5 semantic colors in a single diagram unless the content truly
  requires more and the legend makes the mapping clear.
- Preserve the requested language for generated content while keeping code,
  selectors, and technical identifiers valid.
- Keep source snippets short enough to read; move supporting detail to notes or
  a follow-up slide.

## Composition

### Upstream Skills

This Skill may consume outputs from research, content-development, technical
documentation, or presentation-design Skills. It owns the transformation into
the final HTML deck, not the upstream research process.

### Downstream Skills

The HTML deck may be consumed by browser preview, presentation QA, publishing,
or artifact delivery workflows. Keep the output self-contained so those
workflows can inspect or serve it without reconstructing missing pieces.

## Quality Criteria

The result is valid when:

- [ ] The deck has a coherent opening, development, and close.
- [ ] Every slide has one primary idea and a clear title or intentional title
      treatment.
- [ ] The default theme or custom theme is applied as a coherent system.
- [ ] Layouts vary according to content and do not default to card grids.
- [ ] Diagrams are used only where they improve understanding and are readable
      within a few seconds.
- [ ] Text is concise, readable, and not used to compensate for poor layout.
- [ ] Every element remains inside the 1600 x 900 stage and safe area.
- [ ] There are no unintended overlaps, clipped labels, or off-canvas diagrams.
- [ ] Footer, controls, progress, and numbering remain visible and safe.
- [ ] The deck presents one slide at a time without vertical scrolling.
- [ ] Keyboard navigation, fullscreen, and responsive scaling work as intended.
- [ ] Animation is restrained and reduced-motion behavior is defined.
- [ ] Shared visual tokens and reusable layouts make the deck feel like one
      product.

## Validation

Before returning the result, run this quality gate.

### Narrative

1. Confirm that each slide has a function in the story.
2. Confirm that the sequence progresses logically toward a takeaway.
3. Remove duplicate ideas and split overloaded slides.

### Visual and content

1. Check that the theme is consistent and custom palette roles have sufficient
   contrast.
2. Check that there is enough negative space and that the deck is not a sequence
   of visually identical cards.
3. Check that the dominant visual supports the slide's primary idea.
4. Check title length, body density, label size, and code readability.

### Layout and overflow

1. Inspect each slide at 1600 x 900 or an equivalent 16:9 viewport.
2. Check element bounds, safe-area margins, text overflow, clipping, and
   unintended overlap.
3. Check SVG viewBox bounds, connector paths, footer, controls, and progress.
4. If anything does not fit, reduce content, split the slide, change the layout,
   or simplify the visual. Do not ship a clipped slide.

### Runtime

1. Open the HTML directly in a browser.
2. Test previous/next controls, keyboard navigation, progress, fullscreen, and
   responsive scaling.
3. Confirm that only one slide is visible and that the page does not scroll
   vertically between slides.
4. Confirm that reduced motion disables non-essential animation.

### Final acceptance

Do not consider the deck complete until the narrative, visual system, diagrams,
legibility, layout, and runtime checks all pass. If browser rendering is
available, inspect at least the cover, densest content slide, diagram slide, and
closing slide rather than relying only on source inspection.

## Examples

### Technical presentation

For a Clean Architecture or Prompt Engineering deck, use the default dark theme,
an architecture or relationship diagram for dependencies, a process or sequence
layout for workflows, code only when it can be read, and a closing statement that
captures the practical takeaway. Avoid turning every principle into a card grid.

### Executive presentation

For a strategy or business-results deck, use a concise narrative, statement and
metrics slides, comparison or before/after layouts, and a clear decision or
closing slide. Use diagrams only for relationships, process, or decision logic;
do not substitute decorative diagrams for evidence.

## References

No external reference is required for the default workflow. When repository
templates, existing decks, or visual examples are provided, inspect them as
compatibility references and preserve their valid presentation behavior.

---

> Keep this Skill focused on generating presentation-grade HTML decks. Preserve
> valid existing behavior while improving clarity, visual composition,
> consistency, and validation.
