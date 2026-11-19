#!/usr/bin/env python3
"""Normalize HTML-export residue in cleaned Thought Mash Markdown drafts."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "cleaned"
PLACEHOLDER = re.compile(r"^\[IMAGE:\s*(.*?)\]\((.*)\)$")
BARE_URL = re.compile(r"^\((https?://.*)\)$")


def clean_url(value: str) -> str:
    return value.rstrip('"\'').strip()


def normalize(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        match = PLACEHOLDER.match(lines[index].strip())
        if not match:
            output.append(lines[index])
            index += 1
            continue

        alt = match.group(1).strip()
        source = clean_url(match.group(2))
        wrapper = None
        if index + 1 < len(lines):
            next_match = BARE_URL.match(lines[index + 1].strip())
            if next_match:
                wrapper = clean_url(next_match.group(1))
                index += 1

        image = f"![{alt}]({source})"
        if wrapper and wrapper != source:
            image = f"[{image}]({wrapper})"
        output.append(image)
        index += 1

    cleaned = "\n".join(output).rstrip() + "\n"
    if cleaned == original:
        return False
    path.write_text(cleaned, encoding="utf-8")
    return True


def main() -> None:
    changed = [path.name for path in sorted(ROOT.glob("*.md")) if normalize(path)]
    print(f"normalized {len(changed)} file(s)")


if __name__ == "__main__":
    main()
