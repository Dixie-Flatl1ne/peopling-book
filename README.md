# Peopling — How Minds Stay in Sync, and Why Everything Depends on It

**Author:** Stefan van der Wel

Read it online: **https://peopling.vanderwel.au/**

## Repository Structure

### Root — The Book

| Path | Description |
|------|-------------|
| `peopling_book.md` | **Master manuscript** — the canonical single-source book file |
| `images/` | Figures referenced by the manuscript (SVG, theme-aware) |
| `audio/` | Published MP3 and chapter manifest for the current manuscript |
| `peopling_book.html` | Generated standalone reading page — do not edit by hand |
| `site/` | Builder for that page (`build.py`, `style.css`, `app.js`) |
| `working/` | Everything that isn't the book itself |

### Publishing

The reading site is published from this repository's `main` branch by
`.github/workflows/deploy.yml`. Push manuscript, figure or layout changes here to
publish them, or run **Deploy to GitHub Pages** manually in this repository.
Qualia Partners no longer hosts or builds the book. Its old `/peopling/` address
redirects readers to the new site, preserving chapter anchors in browsers.

`site/build_web.py` runs the existing reading-page builder in a temporary directory.
Only the rendered book and a matching audiobook are published. Working material,
Git metadata and build tools are excluded. Chapter anchors, figures and local links
are validated before deployment. `/source.json` records the deployed source commit.
The production canonical URL is `https://peopling.vanderwel.au/`.

```sh
python3 -m venv /tmp/peopling-web-venv
/tmp/peopling-web-venv/bin/pip install -r site/requirements.txt
/tmp/peopling-web-venv/bin/python site/build_web.py --output /tmp/peopling-web
```

Use a new output directory for each build. The standalone authoring command,
`python site/build.py`, still generates `peopling_book.html` and `site/peopling.html`.
It inlines the figures; listening also needs the adjacent `audio/` folder.

GitHub Pages uses the **GitHub Actions** build source and custom domain
`peopling.vanderwel.au`, with HTTPS enforced. DNS has a `peopling` CNAME pointing
to `dixie-flatl1ne.github.io`. The old `gh-pages` branch and
`working/publishing-site/` are historical and are no longer deployed.

### Audiobook

The player at the beginning of the book uses one continuous MP3, with chapter
selection, speed controls and 15-second skips. It saves your listening position
in this browser and supports media controls on compatible lock screens. The MP3
download includes chapter markers and can be saved to an offline audio app.
Narration uses Microsoft's stock Australian English William voice; it is labelled
as AI narration. It is not a recording or imitation of Stefan's voice.

To regenerate after changing the manuscript, use Python 3.10+ and `ffmpeg`:

```sh
python3 -m venv /tmp/peopling-audio-venv
/tmp/peopling-audio-venv/bin/pip install -r site/audio-requirements.txt
/tmp/peopling-audio-venv/bin/python site/build_audio.py --cache /tmp/peopling-narration
/tmp/peopling-audio-venv/bin/python site/build.py
```

Generation sends only the public manuscript to the online speech service. It
keeps reusable chunks and intermediate WAVs in the chosen cache, outside this
repository. `--plan-only` writes the exact spoken text there without recording.
The narration includes the overview, eight chapters, epilogue and appendix;
diagram descriptions and captions are spoken, tables become labelled sentences,
and the duplicate contents list and URL destinations are omitted.

Commit the new `audio/manifest.json`, its referenced MP3 and the generated HTML.
The manifest records the manuscript checksum, audio checksum and chapter times.
The builder omits the player if the manuscript checksum no longer matches, so
text edits can still deploy without presenting an old recording as current.
Audio generation is a separate authoring step; the website build only
copies the finished recording. Only the current recording is deployed; downloaded
copies remain available for offline use.

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
| `publishing-site/` | Historical Jekyll site source (not deployed) |
| `archive/` | Superseded versions. Dead — do not edit |

## Writing Conventions

- **No em-dashes or en-dashes.** Use full stop, comma, colon, or sentence split instead.
  This applies to figure labels and captions as well as prose.
- Voice skill: `stefan-writing` (grounded in named interview turns, original Thoughtmash prose and attributed correspondence). The older guide in `working/drafts/` is secondary reference material.
- The master manuscript is the single source of truth for "what's in the book"
- Extracts and per-chapter files under `working/` are for sharing and review, not canonical
