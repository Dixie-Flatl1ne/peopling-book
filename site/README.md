# site/ — the reading page

Builds `../peopling_book.html`, a single self-contained page of the whole manuscript:
title page, overview, contents, all chapters, epilogue, appendix. Open it in any
browser, or send the file to someone.

## Rebuild after editing the manuscript

```sh
python3 site/build.py
```

Needs Python 3 and the `markdown` package (`pip install markdown`). It reads
`peopling_book.md` and writes two files:

| Output | What it is |
|--------|------------|
| `peopling_book.html` | Standalone page. This is the one to open or share. |
| `site/peopling.html` | Body fragment only, for publishing as a Claude Artifact. |

## Files

- `build.py` — parses the manuscript and assembles the page
- `style.css` — typography, layout, light and dark themes
- `app.js` — contents rail highlighting, reading progress, mobile drawer

## How the manuscript is read

- `# Chapter N` starts a chapter; the `##` directly after it is the chapter title,
  and every `##` (or `###`) after that becomes a section in the contents.
- `# Epilogue` and `# Appendix` are handled the same way.
- The `## Table of Contents` block is skipped. The page builds its contents from the
  actual chapter headings instead, so it cannot drift out of date.
- Part groupings and the four-rung labels are set in `PART_OF`, `RUNG_OF` and `PARTS`
  near the top of `build.py`. Adding a chapter means adding it there.
- Horizontal rules between chapters are dropped.
- `smart_dashes` is off, so no em-dashes or en-dashes are ever introduced.

## The Chapter 2 diagram

`images/recursive-mutual-modelling.svg` is referenced by the manuscript but is not in
the repo. `build.py` substitutes a hand-drawn SVG (the `FIGURE` constant) in its place.
If the real diagram file ever lands, replace that constant.
