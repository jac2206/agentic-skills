---
name: html-presentations
description: >
  Creates presentation-grade HTML slide decks that behave like real presentations.
  Use when the user asks to create, structure, design, or generate a presentation,
  keynote, workshop, masterclass, technical talk, educational presentation,
  executive presentation, or visual slide deck. The output is a self-contained
  HTML presentation with slide navigation, responsive 16:9 layout, visual
  storytelling, transitions, animations, and presentation controls.
metadata:
  version: "1.0.0"
---

# HTML Presentations

Create presentation-grade HTML slide decks that behave like real presentations rather than ordinary web pages.

The primary output is a self-contained HTML file that can be opened directly in a browser and presented fullscreen.

## Purpose

Transform a presentation brief, topic, document, or set of ideas into a complete HTML presentation with:

- Clear narrative structure
- Presentation-quality slide composition
- 16:9 visual stage
- One slide visible at a time
- Keyboard navigation
- Visual navigation controls
- Slide progress
- Transitions
- Controlled animations
- Visual diagrams and illustrations using HTML/CSS/SVG
- Speaker notes when useful
- Responsive scaling
- No vertical page scrolling between slides

The presentation should feel like a presentation, not like a long scrolling website.

---

## When to use

Use this Skill when the user asks to:

- Create a presentation
- Create slides
- Build a keynote
- Create a workshop deck
- Create a masterclass
- Create a technical presentation
- Create an educational presentation
- Create an executive presentation
- Turn content into slides
- Turn documentation into a presentation
- Create an interactive HTML presentation
- Create a browser-based slide deck
- Create a presentation that can be presented directly from a browser

---

## When not to use

Do not use this Skill when the primary output is:

- A normal website
- A landing page
- A dashboard
- A documentation site
- A long-form article
- A PDF-only document
- A Word document
- A spreadsheet

If the user specifically requests PowerPoint, PPTX, or another presentation format, use an appropriate generation capability instead of forcing HTML.

HTML may still be used as an intermediate representation when useful.

---

# Core Principles

## 1. Presentation first

The result must behave as a presentation.

Do not create a vertically scrolling document with sections that merely look like slides.

The user should be able to move through discrete slides.

---

## 2. One visual stage

Use a presentation stage with a 16:9 aspect ratio.

Preferred base resolution:

```text
1600 × 900