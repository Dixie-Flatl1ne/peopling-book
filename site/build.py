#!/usr/bin/env python3
"""Build a reading-site HTML page from the Peopling manuscript."""
import re, html, json, pathlib
import markdown

HERE = pathlib.Path(__file__).resolve().parent
# repo layout: build lives in <repo>/site/, the manuscript in <repo>/
ROOT = HERE.parent if (HERE.parent / "peopling_book.md").exists() else HERE
SRC = ROOT / "peopling_book.md"
if not SRC.exists():                      # cloud session: manuscript comes from the staged upload
    SRC = pathlib.Path("/mnt/user-data/uploads/Documents/projects/book/peopling_book.md")
OUT = HERE / "peopling.html"              # body fragment, for publishing as an Artifact
OUT_DOC = ROOT / "peopling_book.html"     # standalone page, opens straight from disk

md = markdown.Markdown(extensions=["smarty", "attr_list"],
                       extension_configs={"smarty": {"smart_dashes": False,
                                                     "smart_quotes": True,
                                                     "smart_ellipses": False}})

def render(text):
    md.reset()
    return md.convert(text.strip())

raw = SRC.read_text(encoding="utf-8")
lines = raw.split("\n")

# ---------------------------------------------------------------- parse
IMG_TOKEN = "@@FIGURE_RECURSIVE_MIRROR@@"
# swap the missing image reference + its italic caption for a token
for i, l in enumerate(lines):
    if l.startswith("!["):
        cap = ""
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and lines[j].startswith("*") and lines[j].endswith("*"):
            cap = lines[j].strip("*").strip()
            lines[j] = ""
        lines[i] = IMG_TOKEN
        FIG_CAPTION = cap
        break

# split on H1
h1_idx = [i for i, l in enumerate(lines) if re.match(r"^# (?!#)", l)]
blocks = []
for n, start in enumerate(h1_idx):
    end = h1_idx[n + 1] if n + 1 < len(h1_idx) else len(lines)
    blocks.append(lines[start:end])

def strip_rules(ls):
    return [l for l in ls if l.strip() != "---"]

front = strip_rules(blocks[0])
title = re.sub(r"[*#]", "", front[0]).strip()
subtitle = front[1].strip().strip("*")

# overview body = everything after '## Overview'
ov = front.index("## Overview")
overview_md = "\n".join(front[ov + 1:]).strip()

PART_OF = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 4}
RUNG_OF = {1: [1], 2: [2], 3: [3], 4: [4], 5: [1], 6: [3], 7: [4], 8: [1, 2, 3, 4]}
PARTS = {
    1: ("Part One", "Foundation", "Understanding how this actually works"),
    2: ("Part Two", "Application", "Solving for you and your organisation"),
    3: ("Part Three", "Implementation", "Agents as participants"),
    4: ("Part Four", "Synthesis", "Where the ladder leads"),
}
RUNG_NAME = {1: "the self", 2: "the other", 3: "the organisation", 4: "the machine"}

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60]

chapters = []
for b in blocks[1:]:
    b = strip_rules(b)
    head = re.sub(r"[*#]", "", b[0]).strip()          # "Chapter 1" / "Epilogue" / "Appendix"
    # chapter title is the first H2
    ti = next(i for i, l in enumerate(b) if l.startswith("## "))
    ctitle = b[ti][3:].strip()
    body = b[ti + 1:]
    m = re.match(r"Chapter (\d+)", head)
    num = int(m.group(1)) if m else None
    kind = "chapter" if num else head.lower()

    # sections: subsequent ## or ### headings
    secs, cur, buf = [], None, []
    for l in body:
        hm = re.match(r"^(#{2,3}) (.+)$", l)
        if hm:
            if cur is not None:
                secs.append((cur, "\n".join(buf)))
            else:
                lead = "\n".join(buf).strip()
                if lead:
                    secs.append((None, lead))
            cur, buf = hm.group(2).strip(), []
        else:
            buf.append(l)
    if cur is not None:
        secs.append((cur, "\n".join(buf)))
    else:
        secs.append((None, "\n".join(buf)))

    chapters.append({
        "kind": kind, "num": num, "head": head, "title": ctitle,
        "id": f"ch{num}" if num else slug(head),
        "part": PART_OF.get(num), "rungs": RUNG_OF.get(num, []),
        "sections": [{"title": t, "id": slug(f"{head}-{t}") if t else None,
                      "md": body_md} for t, body_md in secs],
    })

# ---------------------------------------------------------------- diagram
FIGURE = '''<figure class="fig">
<svg viewBox="0 0 900 470" role="img" aria-label="Two people, Alice and Bob, each holding a nested model of the other and of the other's model of them. The models never touch: only words, tone and timing cross the interface between them." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <polygon class="accent-fill" points="0,1 10,5 0,9"></polygon>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="1.25">
    <rect x="28" y="56" width="346" height="352" rx="16" opacity=".9"></rect>
    <rect x="60" y="104" width="282" height="272" rx="12" opacity=".55"></rect>
    <rect x="92" y="152" width="218" height="192" rx="10" opacity=".34"></rect>
    <rect x="124" y="216" width="154" height="112" rx="8" opacity=".18"></rect>
    <rect x="526" y="56" width="346" height="352" rx="16" opacity=".9"></rect>
    <rect x="558" y="104" width="282" height="272" rx="12" opacity=".55"></rect>
    <rect x="590" y="152" width="218" height="192" rx="10" opacity=".34"></rect>
    <rect x="622" y="216" width="154" height="112" rx="8" opacity=".18"></rect>
    <line x1="450" y1="44" x2="450" y2="424" stroke-dasharray="3 6" opacity=".5"></line>
    <line class="accent" x1="378" y1="200" x2="518" y2="200" marker-end="url(#ah)" stroke-width="1.5"></line>
    <line class="accent" x1="522" y1="268" x2="382" y2="268" marker-end="url(#ah)" stroke-width="1.5"></line>
  </g>
  <g fill="currentColor" font-size="12.5">
    <text x="46" y="84" font-size="11" letter-spacing="1.4" opacity=".95">ALICE</text>
    <text x="76" y="130" opacity=".72">her model of Bob</text>
    <text x="108" y="178" opacity=".6">her model of Bob&#8217;s</text>
    <text x="108" y="195" opacity=".6">model of her</text>
    <text x="140" y="242" opacity=".45">and on down</text>
    <text x="140" y="262" opacity=".45" letter-spacing="2">· · ·</text>
    <text x="544" y="84" font-size="11" letter-spacing="1.4" opacity=".95">BOB</text>
    <text x="574" y="130" opacity=".72">his model of Alice</text>
    <text x="606" y="178" opacity=".6">his model of Alice&#8217;s</text>
    <text x="606" y="195" opacity=".6">model of him</text>
    <text x="638" y="242" opacity=".45">and on down</text>
    <text x="638" y="262" opacity=".45" letter-spacing="2">· · ·</text>
    <text x="450" y="30" text-anchor="middle" font-size="11" letter-spacing="1.6" opacity=".8">THE INTERFACE</text>
    <text x="440" y="188" font-size="11.5" text-anchor="end" opacity=".8">what she says</text>
    <text x="460" y="290" font-size="11.5" opacity=".8">what he says</text>
    <text x="28" y="452" font-size="11" opacity=".55">Fainter box, lower fidelity: each rung inward predicts the real person less well.</text>
  </g>
</svg>
<figcaption>__CAP__</figcaption>
</figure>'''

# ---------------------------------------------------------------- html
def rungs_html(rungs):
    if not rungs:
        return ""
    ticks = "".join(f'<span class="{"on" if r in rungs else ""}"></span>' for r in (1, 2, 3, 4))
    if len(rungs) == 4:
        label = "all four rungs"
    else:
        label = f"rung {['one','two','three','four'][rungs[0]-1]}: {RUNG_NAME[rungs[0]]}"
    return f'<span class="rungs" aria-label="{label}"><span class="ladder">{ticks}</span>{label}</span>'

body_parts = []
nav_parts = []
cur_part = None

for c in chapters:
    # ---- nav
    if c["kind"] == "chapter" and c["part"] != cur_part:
        cur_part = c["part"]
        pn, pt, _ = PARTS[cur_part]
        nav_parts.append(f'<li class="nav-part">{pn} <span>{pt}</span></li>')
    if c["kind"] != "chapter":
        nav_parts.append(f'<li class="nav-part">{html.escape(c["head"])}</li>')
    subs = "".join(
        f'<li><a href="#{s["id"]}">{html.escape(s["title"])}</a></li>'
        for s in c["sections"] if s["title"])
    label = f'<em>{c["num"]}</em> {html.escape(c["title"])}' if c["num"] else html.escape(c["title"])
    nav_parts.append(
        f'<li class="nav-ch" data-ch="{c["id"]}"><a href="#{c["id"]}">{label}</a>'
        f'<ul class="nav-secs">{subs}</ul></li>')

    # ---- chapter body
    if c["kind"] == "chapter":
        pn, pt, _ = PARTS[c["part"]]
        eyebrow = f'<span>{pn} &middot; {pt}</span>{rungs_html(c["rungs"])}'
        numeral = f'<div class="numeral" aria-hidden="true">{c["num"]}</div>'
        kicker = f'<div class="kicker">Chapter {c["num"]}</div>'
    else:
        eyebrow = f'<span>{html.escape(c["head"])}</span>'
        numeral = ""
        kicker = ""
    secs_html = []
    for s in c["sections"]:
        inner = render(s["md"]) if s["md"].strip() else ""
        if IMG_TOKEN in inner:
            inner = inner.replace(f"<p>{IMG_TOKEN}</p>",
                                  FIGURE.replace("__CAP__", html.escape(FIG_CAPTION).replace("'", "’")))
        if s["title"]:
            secs_html.append(f'<section class="sec" id="{s["id"]}">'
                             f'<h3>{html.escape(s["title"])}</h3>{inner}</section>')
        elif inner:
            secs_html.append(f'<div class="sec lead-in">{inner}</div>')
    body_parts.append(f'''<article class="chapter" id="{c["id"]}">
  <header class="ch-head">
    <div class="eyebrow">{eyebrow}</div>
    {numeral}
    {kicker}
    <h2>{html.escape(c["title"])}</h2>
  </header>
  {"".join(secs_html)}
</article>''')

# contents page
toc_rows = []
cur_part = None
for c in chapters:
    if c["kind"] == "chapter" and c["part"] != cur_part:
        cur_part = c["part"]
        pn, pt, pd = PARTS[cur_part]
        toc_rows.append(f'<div class="toc-part"><span>{pn}</span><b>{pt}</b><i>{pd}</i></div>')
    if c["kind"] != "chapter":
        toc_rows.append(f'<div class="toc-part"><span>{html.escape(c["head"])}</span></div>')
    n = f'<em>{c["num"]}</em>' if c["num"] else '<em class="dot">&bull;</em>'
    cnt = sum(1 for s in c["sections"] if s["title"])
    meta = f'{cnt} sections' if cnt else ''
    toc_rows.append(
        f'<a class="toc-row" href="#{c["id"]}">{n}<span>{html.escape(c["title"])}</span>'
        f'<i>{meta}</i></a>')

words = len(raw.split())
minutes = round(words / 230)
readtime = f"{minutes // 60} hr {minutes % 60} min" if minutes >= 60 else f"{minutes} min"

CSS = (HERE / "style.css").read_text()
JS = (HERE / "app.js").read_text()

page = f'''<title>Peopling</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..700&family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..600&display=swap">
<style>{CSS}</style>

<div class="progress" aria-hidden="true"><i id="bar"></i></div>

<div class="topbar">
  <a class="tb-title" href="#top">Peopling</a>
  <button class="tb-btn" id="tocBtn" aria-expanded="false" aria-controls="rail">Contents</button>
</div>

<nav class="rail" id="rail" aria-label="Contents">
  <div class="rail-in">
    <a class="rail-title" href="#top"><b>Peopling</b><span>Stefan van der Wel</span></a>
    <ul class="nav">
      <li class="nav-ch" data-ch="overview"><a href="#overview">Overview</a></li>
      {"".join(nav_parts)}
    </ul>
    <div class="rail-foot"><span id="pct">0%</span> read &middot; {readtime}</div>
  </div>
</nav>
<div class="scrim" id="scrim" hidden></div>

<main class="page" id="top">

  <header class="titlepage">
    <div class="tp-rule" aria-hidden="true"></div>
    <div class="tp-eyebrow">Self &middot; Other &middot; Organisation &middot; Machine</div>
    <h1>Peopling</h1>
    <p class="tp-sub">{html.escape(subtitle)}</p>
    <p class="tp-author">Stefan van der Wel</p>
    <p class="tp-thesis">You don&#8217;t work with your colleagues. You work with the version of them you
      carry in your head, and they work with the version of you they carry in theirs. The work goes well
      exactly to the degree those two models line up.</p>
    <div class="tp-meta"><span>{words:,} words</span><span>{readtime} read</span><span>8 chapters</span></div>
  </header>

  <section class="frontmatter" id="overview">
    <div class="fm-label">Overview</div>
    {render(overview_md)}
  </section>

  <section class="contents" id="contents">
    <div class="fm-label">Contents</div>
    {"".join(toc_rows)}
  </section>

  {"".join(body_parts)}

  <footer class="colophon">
    <div class="tp-rule" aria-hidden="true"></div>
    <p><b>Peopling</b> &middot; {html.escape(subtitle)}</p>
    <p>Stefan van der Wel</p>
    <p class="back"><a href="#top">Back to the top</a></p>
  </footer>
</main>

<script>{JS}</script>
'''

OUT.write_text(page, encoding="utf-8")

# standalone document: the same page wrapped so it opens straight from disk
body_only = page.replace("<title>Peopling</title>\n", "", 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
       '<title>Peopling</title>\n'
       '<meta name="description" content="Peopling: How Minds Stay in Sync, and Why Everything '
       'Depends on It. By Stefan van der Wel.">\n'
       '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
       '</head>\n<body>\n' + body_only + '\n</body>\n</html>\n')
OUT_DOC.write_text(doc, encoding="utf-8")

print("source  ", SRC)
print("fragment", OUT, len(page), "bytes")
print("document", OUT_DOC, len(doc), "bytes")
print("chapters:", [(c["kind"], c["num"], c["title"], len(c["sections"])) for c in chapters])
print("words:", words)
