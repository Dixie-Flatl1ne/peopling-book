"""Regression checks for lossless narration extraction and public audio builds.

Run: python -m unittest discover -s site -p 'test_*.py'
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_audio import ROOT, chunks, narration_plan, spoken_text


class NarrationTests(unittest.TestCase):
    def test_markup_preserves_prose_but_does_not_read_urls(self):
        source = '## A question\n\nKeep **every** word and [this reference](https://example.com/private-looking-path).\n\n![A circle around a person](images/figure.svg)\n\n*Its caption stays.*\n\n- One point.\n- Another point.'
        result = spoken_text(source)
        self.assertIn('Keep every word and this reference.', result)
        self.assertIn('Figure description. A circle around a person.', result)
        self.assertIn('Its caption stays.', result)
        self.assertIn('One point.', result)
        self.assertIn('Another point.', result)
        self.assertNotIn('example.com', result)
        self.assertNotIn('images/', result)

    def test_table_preserves_cell_relationships(self):
        result = spoken_text('| Scale | Question | Chapters |\n| --- | --- | --- |\n| Self | What matters? | 1 and 5 |\n| Group | Who decides? | 3 |')
        self.assertIn('Scale: Self. Question: What matters?. Chapters: 1 and 5.', re.sub(r'\s+', ' ', result))
        self.assertIn('Scale: Group. Question: Who decides?. Chapters: 3.', re.sub(r'\s+', ' ', result))

    def test_all_public_chapters_and_chunk_words_are_preserved(self):
        raw = (ROOT / 'peopling_book.md').read_text()
        plan = narration_plan(raw)
        self.assertEqual([p['id'] for p in plan], ['overview'] + [f'ch{i}' for i in range(1, 9)] + ['epilogue', 'appendix'])
        self.assertNotIn('Table of Contents', plan[0]['text'])
        self.assertEqual(sum(p['text'].count('Figure description.') for p in plan), len(re.findall(r'^!\[', raw, re.M)))
        for chapter in plan:
            split = list(chunks(chapter['text']))
            self.assertEqual(' '.join(split).split(), chapter['text'].split())
            self.assertTrue(all(len(c) <= 3200 for c in split))
        self.assertIn('Understanding can reveal a disagreement as well as resolve one.', plan[-1]['text'])

    @unittest.skipUnless((ROOT / 'audio/manifest.json').exists(), 'Generate audio first')
    def test_recording_integrity_and_stale_text_build(self):
        manifest = json.loads((ROOT / 'audio/manifest.json').read_text())
        audio = ROOT / 'audio' / manifest['file']
        self.assertEqual(hashlib.sha256(audio.read_bytes()).hexdigest(), manifest['sha256'])
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_chapters', '-of', 'json', str(audio)]))
        self.assertAlmostEqual(float(info['format']['duration']), manifest['duration'], delta=0.2)
        self.assertEqual(len(info['chapters']), 11)
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            (stage / 'site').mkdir()
            for name in ('build.py', 'app.js', 'style.css'):
                shutil.copy2(ROOT / 'site' / name, stage / 'site' / name)
            shutil.copytree(ROOT / 'images', stage / 'images')
            shutil.copytree(ROOT / 'audio', stage / 'audio')
            shutil.copy2(ROOT / 'peopling_book.md', stage / 'peopling_book.md')
            subprocess.run([sys.executable, str(stage / 'site/build.py')], check=True, capture_output=True)
            current = (stage / 'peopling_book.html').read_text()
            self.assertIn('id="book-audio" controls preload="metadata"', current)
            self.assertIn('download="Peopling - Stefan van der Wel.mp3"', current)
            self.assertIn('src="../audio/', (stage / 'site/peopling.html').read_text())
            with (stage / 'peopling_book.md').open('a') as source:
                source.write('\nA new sentence not yet narrated.\n')
            result = subprocess.run([sys.executable, str(stage / 'site/build.py')], check=True, capture_output=True, text=True)
            self.assertIn('Audiobook omitted', result.stdout)
            self.assertNotIn('id="book-audio"', (stage / 'peopling_book.html').read_text())


if __name__ == '__main__':
    unittest.main()
