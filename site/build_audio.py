#!/usr/bin/env python3
"""Record the public manuscript. Requires audio-requirements.txt and ffmpeg.

Example: python site/build_audio.py --cache /tmp/peopling-narration
Chunks are cached outside the repository so interrupted runs can resume.
"""
import argparse
import asyncio
import hashlib
import json
import re
import subprocess
import tempfile
import wave
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
VOICE = "en-AU-WilliamMultilingualNeural"
RATE = "-3%"
SAMPLE_RATE = 24000


class SpokenHTML(HTMLParser):
    """Retain prose and image descriptions; turn table cells into labelled speech."""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.headers = []
        self.cell = None
        self.column = 0

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.parts.append("\n\nFigure description. " + dict(attrs).get("alt", "") + ".\n\n")
        elif tag == "tr":
            self.column = 0
        elif tag in ("th", "td"):
            self.cell = [tag, ""]
        elif tag == "br":
            self.parts.append(" ")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell[1] += data
        else:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td"):
            value = self.cell[1].strip()
            if tag == "th":
                self.headers.append(value)
            else:
                self.parts.append(f"{self.headers[self.column]}: {value.rstrip('.')}. ")
                self.column += 1
            self.cell = None
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "blockquote", "tr"):
            if tag.startswith("h"):
                self.parts.append(".")
            self.parts.append("\n\n")

    def text(self):
        paragraphs = [re.sub(r"\s+", " ", p).strip() for p in "".join(self.parts).split("\n\n")]
        return "\n\n".join(p for p in paragraphs if p)


def spoken_text(source):
    parser = SpokenHTML()
    parser.feed(markdown.markdown(source, extensions=["tables"]))
    return parser.text()


def narration_plan(raw):
    blocks = re.split(r"(?m)^# ", raw)[1:]
    front = blocks[0].split("## Overview\n", 1)[1]
    intro = "Peopling. How Minds Stay in Sync, and Why Everything Depends on It. By Stefan van der Wel. This audiobook uses an AI narrator. Overview.\n\n"
    result = [{"id": "overview", "title": "Overview", "text": intro + spoken_text(front)}]
    for block in blocks[1:]:
        heading = block.splitlines()[0].strip()
        title = re.search(r"(?m)^## (.+)$", block).group(1)
        match = re.fullmatch(r"Chapter (\d+)", heading)
        chapter_id = "ch" + match.group(1) if match else heading.lower()
        result.append({"id": chapter_id, "title": f"{heading}: {title}", "text": spoken_text("# " + block)})
    expected = ["overview"] + [f"ch{i}" for i in range(1, 9)] + ["epilogue", "appendix"]
    if [c["id"] for c in result] != expected:
        raise ValueError("Manuscript chapter structure changed; review narration extraction")
    return result


def chunks(text, limit=3200):
    # Preserve every character of prose; split long paragraphs at sentence boundaries.
    pieces = []
    for paragraph in text.split("\n\n"):
        pieces.extend(re.split(r"(?<=[.!?])\s+", paragraph) if len(paragraph) > limit else [paragraph])
    current = ""
    for piece in pieces:
        if len(piece) > limit:
            raise ValueError("Sentence is too long for narration; split it deliberately")
        if current and len(current) + len(piece) + 2 > limit:
            yield current
            current = ""
        current += ("\n\n" if current else "") + piece
    if current:
        yield current


async def record(plan, cache, voice):
    import edge_tts
    semaphore = asyncio.Semaphore(2)
    jobs = []
    for chapter in plan:
        chapter["chunks"] = []
        for text in chunks(chapter["text"]):
            key = hashlib.sha256((voice + RATE + text).encode()).hexdigest()
            path = cache / (key + ".mp3")
            chapter["chunks"].append(str(path))
            jobs.append((text, path))

    async def one(index, text, path):
        async with semaphore:
            if path.exists() and path.stat().st_size > 1000:
                print(f"Cached {index}/{len(jobs)}", flush=True)
                return
            pending = path.with_suffix(".partial.mp3")
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(text, voice, rate=RATE).save(str(pending))
                    if pending.stat().st_size < 1000:
                        raise ValueError("Empty narration chunk")
                    pending.replace(path)
                    print(f"Recorded {index}/{len(jobs)}", flush=True)
                    return
                except Exception:
                    pending.unlink(missing_ok=True)
                    if attempt == 2:
                        raise
                    await asyncio.sleep(3 * (attempt + 1))
    await asyncio.gather(*(one(i, text, path) for i, (text, path) in enumerate(jobs, 1)))


def assemble(plan, cache, output, manuscript_hash, voice):
    wav_path = cache / "peopling.wav"
    frames = 0
    chapters = []
    with wave.open(str(wav_path), "wb") as book:
        book.setnchannels(1)
        book.setsampwidth(2)
        book.setframerate(SAMPLE_RATE)
        for chapter in plan:
            start = frames / SAMPLE_RATE
            for index, source in enumerate(chapter["chunks"]):
                pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", source, "-f", "s16le", "-ac", "1", "-ar", str(SAMPLE_RATE), "-"])
                if len(pcm) < SAMPLE_RATE * 2:
                    raise ValueError("Narration chunk shorter than one second")
                book.writeframesraw(pcm)
                frames += len(pcm) // 2
                pause = int(SAMPLE_RATE * (0.8 if index == len(chapter["chunks"]) - 1 else 0.2))
                book.writeframesraw(b"\0\0" * pause)
                frames += pause
            chapters.append({"id": chapter["id"], "title": chapter["title"], "start": round(start, 3), "end": round(frames / SAMPLE_RATE, 3)})
    metadata = [";FFMETADATA1", "title=Peopling", "artist=Stefan van der Wel", "album=Peopling", "comment=AI narration. Australian English. Includes all chapters, epilogue and appendix."]
    for chapter in chapters:
        safe_title = re.sub(r"([\\=;#])", r"\\\1", chapter["title"])
        metadata.extend(["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(chapter['start'] * 1000)}", f"END={round(chapter['end'] * 1000)}", "title=" + safe_title])
    meta_path = cache / "chapters.ffmeta"
    meta_path.write_text("\n".join(metadata) + "\n")
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as tmp:
        finished = Path(tmp) / 'recording.mp3'
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav_path), "-i", str(meta_path), "-map_metadata", "1", "-map_chapters", "1", "-codec:a", "libmp3lame", "-b:a", "64k", "-ar", str(SAMPLE_RATE), "-ac", "1", "-write_xing", "1", str(finished)], check=True)
        audio_hash = hashlib.sha256(finished.read_bytes()).hexdigest()
        filename = f"peopling-{audio_hash[:12]}.mp3"
        manifest = {"version": 1, "manuscript_sha256": manuscript_hash, "generated_at": datetime.now(timezone.utc).isoformat(), "narrator": {"provider": "Microsoft Edge text to speech", "voice": voice, "rate": RATE, "synthetic": True}, "file": filename, "bytes": finished.stat().st_size, "sha256": audio_hash, "duration": round(frames / SAMPLE_RATE, 3), "chapters": chapters}
        (output / filename).write_bytes(finished.read_bytes())
        manifest_path = output / "manifest.json"
        pending = manifest_path.with_suffix(".tmp")
        pending.write_text(json.dumps(manifest, indent=2) + "\n")
        pending.replace(manifest_path)
    print(json.dumps({"file": filename, "minutes": round(frames / SAMPLE_RATE / 60, 1), "bytes": manifest["bytes"], "chapters": len(chapters)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="Private scratch directory outside this repository")
    parser.add_argument("--voice", default=VOICE)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()
    cache = args.cache.resolve()
    if cache == ROOT or ROOT in cache.parents:
        parser.error("Keep narration cache outside the repository")
    cache.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "peopling_book.md").read_bytes()
    plan = narration_plan(source.decode())
    (cache / "narration-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    print(f"Narration: {sum(len(c['text'].split()) for c in plan):,} words, {len(plan)} chapters", flush=True)
    if not args.plan_only:
        asyncio.run(record(plan, cache, args.voice))
        assemble(plan, cache, ROOT / "audio", hashlib.sha256(source).hexdigest(), args.voice)


if __name__ == "__main__":
    main()
