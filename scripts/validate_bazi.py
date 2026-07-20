#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path("public/learn/bazi/index.html")
CSS = Path("public/learn/bazi/styles.css")
JS = Path("public/learn/bazi/app.js")
IMAGE = Path("public/learn/bazi/wuxing-ohne-kreis.webp")
VERSION = Path("public/version.txt")
SITEMAP = Path("public/sitemap.xml")
CANONICAL = "https://sizhuatelier.shop/learn/bazi/"
BUILD = "bazi-2026-07-19-v1"


class Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.landmarks: set[str] = set()
        self.tables = 0
        self.captions = 0
        self.jsonld: list[str] = []
        self._json = False
        self._chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "h1": self.h1 += 1
        if data.get("id"): self.ids.add(data["id"])
        if tag == "a" and data.get("href"): self.hrefs.append(data["href"])
        if tag in {"header", "nav", "main", "article", "footer"}: self.landmarks.add(tag)
        if tag == "table": self.tables += 1
        if tag == "caption": self.captions += 1
        if tag == "script" and data.get("type") == "application/ld+json":
            self._json = True; self._chunks = []

    def handle_data(self, data):
        if self._json: self._chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json:
            self.jsonld.append("".join(self._chunks)); self._json = False


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for path in (PAGE, CSS, JS, IMAGE, VERSION, SITEMAP):
        if not path.exists(): fail(f"missing artifact: {path}")
    html = PAGE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    audit = Audit(); audit.feed(html)
    if audit.h1 != 1: fail(f"expected one H1, found {audit.h1}")
    if not {"header", "nav", "main", "article", "footer"}.issubset(audit.landmarks): fail("semantic landmarks incomplete")
    if audit.tables < 2 or audit.tables != audit.captions: fail("tables require captions")
    if 'class="skip-link"' not in html: fail("skip link missing")
    if ":focus-visible" not in css or "prefers-reduced-motion" not in css: fail("focus or reduced-motion CSS missing")
    if "overflow-x:auto" not in css: fail("responsive table overflow missing")
    if 'src="/learn/bazi/wuxing-ohne-kreis.webp"' not in html: fail("replacement Wu Xing image reference missing")
    if "Wu Xing diagram showing Wood, Fire, Earth, Metal and Water" not in html: fail("replacement Wu Xing image alt text missing")
    if "<svg class=\"wuxing-diagram\"" in html: fail("legacy inline Wu Xing SVG still present")
    if IMAGE.read_bytes()[:4] != b"RIFF" or b"WEBP" not in IMAGE.read_bytes()[:16]: fail("Wu Xing image is not a valid WebP asset")
    for token in ["八字","四柱","干支","天干","地支","日主","藏干","五行","节气","立春","大运","合婚","bāzì","sìzhù","gānzhī","tiāngān","dìzhī","rìzhǔ","cánggān","wǔxíng","jiéqì","lìchūn","dà yùn","héhūn"]:
        if token not in html: fail(f"required terminology missing: {token}")
    for event in ["learn_hub_click","related_page_click","cta_shop_click","cta_etsy_click","cta_bazi_chart_click","section_view","scroll_depth_25","scroll_depth_50","scroll_depth_75","scroll_depth_100","diagram_interaction"]:
        if event not in html and event not in js: fail(f"analytics event missing: {event}")
    for pattern in [r"scientifically proven", r"guaranteed compatibility", r"will definitely", r"diagnoses? your"]:
        if re.search(pattern, html, re.I): fail(f"forbidden deterministic claim: {pattern}")
    for href in [item for item in audit.hrefs if item.startswith("#")]:
        if href[1:] not in audit.ids: fail(f"broken anchor: {href}")
    if len(audit.jsonld) != 1: fail("exactly one JSON-LD block required")
    json.loads(audit.jsonld[0])
    if f'<link rel="canonical" href="{CANONICAL}">' not in html: fail("canonical mismatch")
    version = VERSION.read_text(encoding="utf-8")
    if f"BAZI_BUILD={BUILD}" not in version or "BAZI_ROUTE=/learn/bazi/" not in version: fail("version markers missing")
    if CANONICAL not in SITEMAP.read_text(encoding="utf-8"): fail("sitemap route missing")
    print("PASS: BZG-35 BaZi static validation")
    print("- STATIC_VALIDATED: semantics, terminology, claims, SEO, links, replacement image, accessibility hooks and analytics hooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())