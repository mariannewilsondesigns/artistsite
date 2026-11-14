# Marianne Wilson — Exhibition Site

## What's here

```
index.html          → splash / entry page
works.html           → gallery grid (all 15 pieces, QR-safe URLs)
about.html            → split-screen About + contact
works/<slug>.html      → one page per artwork (15 total)
css/                   → design system (base, splash, works, work-detail, about)
js/app.js              → nav state, splash entry animation, carousel
images/works/<slug>/    → 3 carousel images per artwork (currently placeholders)
images/site/            → splash / hero / about imagery (currently placeholders)
fonts/                  → drop PP Editorial Ultralight Italic files here (see fonts/README.md)
data/works.json          → the single source of truth for every artwork
build.py + scripts/       → regenerates all HTML from data/works.json
```

## Design notes

- **Colour:** warm paper background, deep aubergine (`--plum`) for dark
  sections (nav-on-scroll blur, footer, hero overlays), and chartreuse used
  deliberately — as a spark on buttons, plate tags, hover states and links,
  never as body text at small sizes (kept AA-accessible against paper).
- **Type:** PP Editorial Ultralight Italic for every heading and the plate
  numbering; Inter for everything readable at length.
- **Plate numbers** (Plate 01, 02…) double as the exhibition's real
  catalogue numbering, so they're functional, not decorative — they're
  what ties a QR code to a wall label to a page.
