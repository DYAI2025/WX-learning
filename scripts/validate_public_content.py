#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path("public/learn/wu-xing/index.html")
VERSION = Path("public/version.txt")
EXPECTED_BUILD = "wu-xing-2026-07-18-v6-expert-review"

REQUIRED_TEXT = [
    "Rather than presenting the five categories only as inert substances",
    "Interpretive note:",
    "Bending and straightening; growth, extension, and flexible development.",
    "Blazing and rising; activity, warmth, visibility, and culmination.",
    "Sowing and harvesting; cultivation, transformation, stabilization, and support.",
    "Yielding and changing; contraction, delimitation, refinement, and structure.",
    "Moistening and descending; storage, depth, conservation, and adaptability.",
    "the Controlling, Restraining, or Overcoming Cycle",
    "A modern reflective analogy: balance, excess, and lack",
    "Wood-like expansion without sufficient Metal-like selection",
    "mnemonic explanations, not a physical mechanism",
    "Positions show relational order, not compass directions",
    "John S. Major, Sarah A. Queen, Andrew Seth Meyer, and Harold D. Roth",
    "https://cup.columbia.edu/book/the-huainanzi/9780231142045/",
    "https://www.dpm.org.cn/lemmas/244166.html",
    "https://sizhuatelier-shop-production.up.railway.app/",
    "https://bazodiac.space/",
    "Sizhu Learn",
]

FORBIDDEN_TEXT = [
    "Instead of defining five substances",
    "too much Wood and too little Metal",
    "It describes how each phase limits another so that growth does not continue without restraint",
    "Bazodiac Learn",
    "BAZODIAC LEARN",
    "BZG-",
]

TOKENS = {
    "五行": "wǔxíng",
    "木": "mù",
    "火": "huǒ",
    "土": "tǔ",
    "金": "jīn",
    "水": "shuǐ",
    "相生": "xiāngshēng",
    "相克": "xiāngkè",
}


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.img_count = 0
        self.img_missing_alt: list[str] = []
        self.json_ld_blocks: list[str] = []
        self._json_ld = False
        self._json_chunks: list[str] = []
        self.figure_labels: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            self.img_count += 1
            if not (data.get("alt") or "").strip():
                self.img_missing_alt.append(data.get("src", "<missing src>"))
        elif tag == "figure":
            self.figure_labels.append(data.get("aria-labelledby", ""))
        elif tag == "script" and data.get("type") == "application/ld+json":
            self._json_ld = True
            self._json_chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_ld:
            self.json_ld_blocks.append("".join(self._json_chunks))
            self._json_ld = False
            self._json_chunks = []

    def handle_data(self, data: str) -> None:
        if self._json_ld:
            self._json_chunks.append(data)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not PAGE.exists():
        fail(f"missing page: {PAGE}")
    html = PAGE.read_text(encoding="utf-8")

    for item in REQUIRED_TEXT:
        if item not in html:
            fail(f"required content missing: {item}")
    for item in FORBIDDEN_TEXT:
        if item in html:
            fail(f"forbidden legacy/internal content present: {item}")

    if html.count('data-review-note="gen-title gen-caption"') != 1:
        fail("generating-cycle interpretation note must appear exactly once")
    if html.count('data-review-note="ctl-title ctl-caption"') != 1:
        fail("controlling-cycle interpretation note must appear exactly once")
    if html.count("CTA_CARD_ALIGNMENT_V1") != 1:
        fail("CTA alignment CSS marker must appear exactly once")

    for hanzi, pinyin in TOKENS.items():
        if hanzi not in html:
            fail(f"verified Hanzi token missing: {hanzi}")
        if pinyin not in html:
            fail(f"tone-marked Pinyin missing: {pinyin}")

    parser = AuditParser()
    parser.feed(html)
    if parser.h1_count != 1:
        fail(f"expected one H1, found {parser.h1_count}")
    if parser.img_count < 2:
        fail(f"expected at least two cycle images, found {parser.img_count}")
    if parser.img_missing_alt:
        fail(f"images without alt text: {parser.img_missing_alt}")
    expected_figures = {"gen-title gen-caption", "ctl-title ctl-caption"}
    if not expected_figures.issubset(set(parser.figure_labels)):
        fail(f"cycle figure labels missing: {expected_figures - set(parser.figure_labels)}")
    if len(parser.json_ld_blocks) != 1:
        fail(f"expected one JSON-LD block, found {len(parser.json_ld_blocks)}")
    try:
        data = json.loads(parser.json_ld_blocks[0])
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON-LD: {exc}")
    graph = data.get("@graph")
    if not isinstance(graph, list) or not graph:
        fail("JSON-LD @graph missing or empty")

    if f"PUBLIC_BUILD: {EXPECTED_BUILD}" not in html:
        fail("HTML build marker missing")
    if f'content="{EXPECTED_BUILD}"' not in html:
        fail("meta build marker missing")
    if not VERSION.exists():
        fail("version.txt missing")
    version = VERSION.read_text(encoding="utf-8")
    if f"WU_XING_PUBLIC_BUILD={EXPECTED_BUILD}" not in version:
        fail("version.txt build marker missing")
    if "EXPERT_REVIEW=historical-nuance-classical-anchors-modern-analogy-source-precision" not in version:
        fail("version.txt expert-review marker missing")

    print("PASS: public Wu Xing content validated")
    print("- historical framing nuanced")
    print("- classical anchors and modern analogies separated")
    print("- cycle terminology and diagram notes validated")
    print("- source precision and JSON-LD validated")
    print("- Hanzi, Pinyin, CTA routes, images, and accessibility checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
