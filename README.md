# Marianne Wilson — Exhibition Site

Everything needed to preview, finish, and deploy. Open `index.html` in a
browser (or drag the whole folder onto Netlify/Vercel/any static host) to
see it live — no build tools required to just *view* it.

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

## Before this goes live — three things to finish

**1. Real artwork content.** `data/works.json` has your two real pieces
("Rain on my Window", "Blue Horizon") plus 13 clearly-marked placeholder
entries (title, medium, dimensions, description) so the full 15-page
catalogue previews correctly. Replace the placeholder text with the real
details for the rest of the show.

**2. Real photography.** Every image right now is a generated placeholder
watermarked "ADD IMAGE" so nothing gets mistaken for final art. Replace the
files in `images/works/<slug>/01.jpg`, `02.jpg`, `03.jpg` with real photos
of each piece (any number of images works — the carousel adapts). Same for
`images/site/splash.jpg`, `hero.jpg`, and `artist.jpg`.

**3. PP Editorial Ultralight Italic.** The font is already wired into every
heading — see `fonts/README.md` for the two files to drop in. Until then,
headings gracefully fall back to an italic serif, so nothing looks broken.

## How to update content

Easiest path — edit `data/works.json` (titles, mediums, dimensions,
descriptions, image paths) then, if you have Python installed, run:

```
python3 build.py
```

This regenerates all 15 artwork pages plus the grid and index from that one
file, so you never hand-edit repeated HTML. If you'd rather not touch a
terminal, message me the corrected list and I'll rebuild it for you, or
just hand-edit the relevant `works/<slug>.html` file directly — the markup
is plain and commented.

## QR codes for the gallery

Each artwork has a clean, permanent URL for its own page, e.g.:

```
yourdomain.com/works/rain-on-my-window.html
yourdomain.com/works/blue-horizon.html
```

Once the site is deployed, point each wall label's QR code at the piece's
URL — everything (title, medium, size, story, enquiry link) is already
laid out on that page.

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
