# Peopling — How Minds Stay in Sync, and Why Everything Depends on It

**Author:** Stefan van der Wel

Read it online: **https://dixie-flatl1ne.github.io/peopling-book/**

## Repository Structure

### Root — The Book

| Path | Description |
|------|-------------|
| `peopling_book.md` | **Master manuscript** — the canonical single-source book file |
| `images/` | Figures referenced by the manuscript (SVG, theme-aware) |
| `peopling_book.html` | Generated standalone reading page — do not edit by hand |
| `site/` | Builder for that page (`build.py`, `style.css`, `app.js`) |
| `working/` | Everything that isn't the book itself |

### Publishing

Two reading surfaces are built from the one manuscript.

| Surface | Source | Output |
|---------|--------|--------|
| GitHub Pages site | `working/publishing-site/` (Jekyll) | the `gh-pages` branch |
| Standalone page | `peopling_book.md` + `images/` via `site/build.py` | `peopling_book.html`, `site/peopling.html` |

`site/build.py` needs the `markdown` package (`pip3 install markdown`). It inlines every
figure, so the standalone page stays a single file.

The Pages site is served from the `gh-pages` branch, not from `main`. Pushing to `main`
does not update it: copy `working/publishing-site/` onto `gh-pages` and push that too.
Figures live in two places for the same reason — `images/` for the manuscript and
`working/publishing-site/assets/` for the site. Keep them in step.

### `working/` — Supporting Material

Everything that isn't the book itself. Sorted by type. See `working/README.md`.

| Folder | What |
|--------|------|
| `drafts/` | Chapter work in progress, experimental sections, voice notes |
| `ch7-evidence/` | Research, queries and methodology behind Chapter 7 |
| `research/` | Perry, isolation and inner-peopling, published article reference |
| `transcripts/` | Talk and conversation transcripts, some mined, some pending |
| `reviews/` | Manuscript feedback |
| `feature-requests/` | Ideas and future book directions, not yet actioned |
| `publishing-site/` | Jekyll source for the GitHub Pages site |
| `archive/` | Superseded versions. Dead — do not edit |

## Writing Conventions

- **No em-dashes or en-dashes.** Use full stop, comma, colon, or sentence split instead.
  This applies to figure labels and captions as well as prose.
- Voice skill: `stefan-book-voice` (essay register, conversational academic)
- The master manuscript is the single source of truth for "what's in the book"
- Extracts and per-chapter files under `working/` are for sharing and review, not canonical
