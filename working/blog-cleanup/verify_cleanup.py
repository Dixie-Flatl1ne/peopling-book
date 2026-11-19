#!/usr/bin/env python3
"""Validate cleaned Thought Mash drafts against the immutable export."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HANDLED = {
    "8195612788874834896",
    "5397553485906949888",
    "2675111350996349297",
}
REQUIRED_MEDIA = {
    "2076728422531757130": ("2PACX-1vSLE82XN8omNiV5DQrm7cxNmRhiWBMBX1qzNb405EI7v3BKOaIaX6wGiia4wqUNEJUWnx8U3PyXe6A7", "JfVjUu8scvs"),
    "5874481736599967280": ("transhumanism-and-the-problem-of-consciousness", "KPnuW6NNgP0"),
    "7300426704999117712": ("bGv2SPB8pNU",),
    "723205711008250347": ("7fYYPN0BdBw",),
    "9067798512113491779": ("KzGjEkp772s",),
    "4531264327426820161": ("L4HJmev5xg0",),
    "3739433736813708752": ("KXin82A6maM",),
    "8198780431924090618": ("hk38L1M5O7Y",),
    "1844580372135678888": ("oWUfw9Db2dE",),
}
AI_PHRASES = (
    "it is important to note",
    "in conclusion",
    "let's delve",
    "let's dive",
    "at its core",
    "the real question is",
    "i hope this helps",
    "let me know if",
)
URL_RE = re.compile(r'https?://[^\s)>"\']+')
SOURCE_IMAGE_RE = re.compile(r"\[IMAGE:[^\]]*\]\((https?://[^)]+)\)")
WORD_RE = re.compile(r"\b[\w'-]+\b")


def body(text: str) -> str:
    parts = text.split("\n\n", 3)
    return parts[3] if len(parts) == 4 else text


def normalized_urls(pattern: re.Pattern[str], text: str) -> set[str]:
    return {value.rstrip('"\'').strip() for value in pattern.findall(text)}


def output_image_urls(text: str) -> set[str]:
    values: set[str] = set()
    for line in text.splitlines():
        if "![" in line:
            values.update(value.rstrip('"\'').strip() for value in URL_RE.findall(line))
    return values


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    expected = [post for post in manifest if str(post["id"]) not in HANDLED]
    errors: list[str] = []
    warnings: list[str] = []
    metrics: list[dict[str, object]] = []

    for post in expected:
        name = f"{post['slug']}.md"
        source_path = ROOT / "source-text" / name
        output_path = ROOT / "cleaned" / name
        if not output_path.exists():
            errors.append(f"missing output: {name}")
            continue

        source = source_path.read_text(encoding="utf-8")
        output = output_path.read_text(encoding="utf-8")
        source_body = body(source)
        output_body = body(output)

        for field in ("Post ID:", "URL:", "Published:", "Labels:"):
            source_line = next((line for line in source.splitlines() if line.startswith(field)), None)
            output_line = next((line for line in output.splitlines() if line.startswith(field)), None)
            if (source_line or "").rstrip() != (output_line or "").rstrip():
                errors.append(f"{name}: metadata changed for {field}")

        missing_images = sorted(
            normalized_urls(SOURCE_IMAGE_RE, source)
            - output_image_urls(output)
        )
        if missing_images:
            errors.append(f"{name}: lost {len(missing_images)} image(s): {missing_images}")

        missing_urls = sorted(set(URL_RE.findall(source)) - set(URL_RE.findall(output)))
        if missing_urls:
            warnings.append(f"{name}: removed or changed {len(missing_urls)} URL(s): {missing_urls}")

        if "—" in output_body or "–" in output_body:
            errors.append(f"{name}: contains em/en dash")

        for token in REQUIRED_MEDIA.get(str(post["id"]), ()):
            if token not in output:
                errors.append(f"{name}: omitted embedded media token {token}")

        lowered = output_body.lower()
        hits = [phrase for phrase in AI_PHRASES if phrase in lowered]
        if hits:
            warnings.append(f"{name}: possible AI phrase(s): {hits}")

        source_words = len(WORD_RE.findall(source_body))
        output_words = len(WORD_RE.findall(output_body))
        ratio = output_words / source_words if source_words else 1.0
        if source_words >= 120 and not 0.70 <= ratio <= 1.20:
            warnings.append(
                f"{name}: word-count ratio {ratio:.2f} ({source_words} -> {output_words})"
            )
        metrics.append(
            {
                "id": str(post["id"]),
                "title": post["title"],
                "source_words": source_words,
                "cleaned_words": output_words,
                "ratio": round(ratio, 3),
                "images_preserved": not missing_images,
                "all_urls_preserved": not missing_urls,
            }
        )

    reports = sorted((ROOT / "batches").glob("batch-*-report.json"))
    if len(reports) != 5:
        errors.append(f"expected 5 batch reports, found {len(reports)}")
    for report_path in reports:
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {report_path.name}: {exc}")
            continue
        if isinstance(report, list):
            entries = report
        else:
            entries = report.get("articles", report.get("entries", []))
        if len(entries) != 9:
            errors.append(f"{report_path.name}: expected 9 entries, found {len(entries)}")

    summary = {
        "expected": len(expected),
        "present": len(metrics),
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }
    (ROOT / "verification-report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: summary[k] for k in ("expected", "present", "errors", "warnings")}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
