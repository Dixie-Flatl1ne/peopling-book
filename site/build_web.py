#!/usr/bin/env python3
"""Build the public Peopling website from an explicit set of book inputs."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = 'https://peopling.vanderwel.au/'


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'Book layout changed: expected one {old!r}')
    return text.replace(old, new, 1)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links = set(), []
        self.figures = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'figure':
            self.figures += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def validate(output, expected_figures):
    output = output.resolve()
    pages = {p: Page(p.read_text()) for p in output.rglob('*.html')}
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (output / unquote(url.path).lstrip('/') if url.path.startswith('/')
                      else path.parent / unquote(url.path)) if url.path else path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.is_relative_to(output) or not target.is_file():
                raise ValueError(f'Broken local link in {path.name}: {link}')
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f'Broken section link in {path.name}: {link}')
    book = pages[output / 'index.html']
    required = {f'ch{i}' for i in range(1, 9)} | {'overview', 'epilogue', 'appendix'}
    if not required <= book.ids or book.figures != expected_figures:
        raise ValueError('Book is missing chapters or figures')
    print(f'Validated {len(pages)} pages, all local links, 8 chapters and {book.figures} figures')


def build(book, output):
    book, output = book.resolve(), output.resolve()
    # Refuse to mix generated output with sources or a previous build.
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='peopling-build-') as tmp:
        source = Path(tmp)
        shutil.copy2(book / 'peopling_book.md', source / 'peopling_book.md')
        shutil.copytree(book / 'images', source / 'images')
        (source / 'site').mkdir()
        for name in ('build.py', 'style.css', 'app.js'):
            shutil.copy2(book / 'site' / name, source / 'site' / name)
        # Only the manifest and its referenced recording are public audio inputs.
        # Caches, narration tooling and working material never enter the site.
        audio_manifest = book / 'audio/manifest.json'
        if audio_manifest.is_file():
            manifest = json.loads(audio_manifest.read_text())
            filename = manifest['file']
            if Path(filename).name != filename or not filename.endswith('.mp3'):
                raise ValueError('Invalid audiobook filename')
            (source / 'audio').mkdir()
            shutil.copy2(audio_manifest, source / 'audio/manifest.json')
            shutil.copy2(book / 'audio' / filename, source / 'audio' / filename)
        subprocess.run([sys.executable, str(source / 'site/build.py')], check=True)
        text = (source / 'peopling_book.html').read_text()
        if 'id="book-audio"' in text:
            shutil.copytree(source / 'audio', output / 'audio')
    text = replace_once(text, '<title>Peopling</title>', '<title>Peopling by Stefan van der Wel</title>')
    text = replace_once(text, '</head>', f'''<link rel="canonical" href="{CANONICAL}">
<meta property="og:title" content="Peopling by Stefan van der Wel">
<meta property="og:description" content="How Minds Stay in Sync, and Why Everything Depends on It. Read the complete book.">
<meta property="og:type" content="book">
<meta property="og:url" content="{CANONICAL}">
</head>''')
    if '@@FIGURE' in text:
        raise ValueError('Unrendered figure token in book')
    (output / 'index.html').write_text(text)
    revision = subprocess.check_output(['git', '-C', str(book), 'rev-parse', 'HEAD'], text=True).strip()
    (output / 'source.json').write_text(json.dumps({'repository': 'Dixie-Flatl1ne/peopling-book', 'commit': revision}) + '\n')
    (output / 'CNAME').write_text(urlsplit(CANONICAL).hostname + '\n')
    (output / '.nojekyll').touch()
    expected_figures = sum(line.startswith('![') for line in (book / 'peopling_book.md').read_text().splitlines())
    validate(output, expected_figures)
    print(f'Built {CANONICAL} from book commit {revision}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True, help='New, empty output directory')
    args = parser.parse_args()
    build(args.book.resolve(), args.output.resolve())
