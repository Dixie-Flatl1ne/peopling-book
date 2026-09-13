# Peopling — How Minds Stay in Sync, and Why Everything Depends on It

**Author:** Stefan van der Wel

Read it online: **https://qualiapartners.com.au/peopling/**

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

The main reading site is hosted on Qualia Partners. Its GitHub Action reads this
repository's `main` branch and builds the book automatically. Commit and push
manuscript or figure changes here; the website picks them up on its next hourly
run (GitHub may delay scheduled runs). For an immediate update, run **Deploy to
GitHub Pages** manually in [the website repository](https://github.com/Qualia-Partners/qualia-partners-website/actions/workflows/deploy.yml).
Dixie already has Maintain access there. No account transfer or additional token
is required. The workflow and publishing instructions live in that repository.

The local standalone builder and the older GitHub Pages site also remain available:

| Surface | Source | Output |
|---------|--------|--------|
| GitHub Pages site | `working/publishing-site/` (Jekyll) | the `gh-pages` branch |
| Standalone page | `peopling_book.md` + `images/` via `site/build.py` | `peopling_book.html`, `site/peopling.html` |

`site/build.py` needs the `markdown` package (`pip3 install markdown`). It inlines every
figure, so the standalone page stays a single file.

The older `dixie-flatl1ne.github.io/peopling-book/` site is served from `gh-pages`,
not from `main`. To update that legacy site separately: copy `working/publishing-site/` onto `gh-pages` and push that too.
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
- Voice skill: `stefan-writing` (grounded in named interview turns, original Thoughtmash prose and attributed correspondence). The older guide in `working/drafts/` is secondary reference material.
- The master manuscript is the single source of truth for "what's in the book"
- Extracts and per-chapter files under `working/` are for sharing and review, not canonical
