# Adding PP Editorial Ultralight Italic

The site is already wired up to use this font for every heading — it just
needs the actual font files, which weren't in the upload.

Drop these two files into this `fonts/` folder, named exactly like this:

    fonts/PPEditorial-UltralightItalic.woff2
    fonts/PPEditorial-UltralightItalic.woff

That's it — no code changes needed. `css/base.css` already declares:

    @font-face{
      font-family:"PP Editorial";
      src:url("../fonts/PPEditorial-UltralightItalic.woff2") format("woff2"),
          url("../fonts/PPEditorial-UltralightItalic.woff") format("woff");
      font-weight:200;
      font-style:italic;
    }

Until the files are added, headings fall back to an italic serif (Georgia)
so the layout still looks intentional in the meantime — nothing will look
broken, it just won't be PP Editorial yet.

If your licensed files have different weight/style variants (e.g. a second
cut for larger display sizes), list them and I can wire those in too.
