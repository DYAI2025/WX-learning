#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

PAGE = Path("public/learn/wu-xing/tcm-organs/index.html")
CONTENT = Path("content/tcm-organs.json")
MANIFEST = Path("content/content_manifest.json")
CLAIMS = Path("research/claim_matrix.csv")
SOURCES = Path("research/source_inventory.md")
SITEMAP = Path("public/sitemap.xml")
ROBOTS = Path("public/robots.txt")
REGISTRY = Path("config/cornerstone-links.json")
BUILD = "wu-xing-tcm-organs-2026-07-19-v1"
CANONICAL = "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/"
HUB = "https://sizhuatelier.shop/learn/wu-xing/"
FENG_SHUI = "https://sizhuatelier.shop/learn/wu-xing/feng-shui/"
SHOP = "https://sizhuatelier.shop/"
ETSY = "https://www.etsy.com/de/shop/SizhuAtelier?ref=profile_header"
BAZI = "https://bazi-custom-app-production.up.railway.app/"

REQUIRED_TEXT = [
    "Wu Xing, TCM and Organs",
    "Educational and historical—not medical guidance",
    "not interchangeable with a modern anatomical organ",
    "The correspondence matrix",
    "Contextual variant",
    "What this model cannot establish",
    "A named qualified human reviewer",
    "Five Phases",
    "zang",
    "fu",
    "Huangdi Neijing",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    r"\bcures?\b",
    r"\bheals?\b",
    r"\bprevents? disease\b",
    r"\btreats? (?:depression|anxiety|cancer|diabetes|eczema|pain|autism|ptsd|arthritis)\b",
    r"\bproven to (?:treat|prevent|cure|heal)\b",
    r"\bimproves? (?:symptoms|clinical outcomes)\b",
    r"\breduces? medication dosage\b",
    r"\buse this table to diagnose\b",
    r"\bidentifies? your organ imbalance\b",
    r"\bscientifically proven correspondence\b",
]

TOKENS = {
    "五行": "wǔxíng",
    "木": "mù",
    "火": "huǒ",
    "土": "tǔ",
    "金": "jīn",
    "水": "shuǐ",
}

REQUIRED_EVENTS = {
    "learn_hub_click",
    "related_page_click",
    "cta_shop_click",
    "cta_etsy_click",
    "cta_bazi_chart_click",
    "section_view",
    "scroll_depth_25",
    "scroll_depth_50",
    "scroll_depth_75",
    "scroll_depth_100",
}

REQUIRED_SCHEMA_TYPES = {
    "Organization",
    "WebSite",
    "WebPage",
    "Article",
    "BreadcrumbList",
    "DefinedTermSet",
}


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.landmarks: set[str] = set()
        self.hrefs: set[str] = set()
        self.events: set[str] = set()
        self.json_ld: list[str] = []
        self._json = False
        self._chunks: list[str] = []
        self.tables = 0
        self.table_captions = 0
        self.th_scopes: list[str] = []
        self.lang_zh = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag in {"header", "main", "nav", "article", "footer"}:
            self.landmarks.add(tag)
        if tag == "a":
            self.hrefs.add(data.get("href", ""))
            if data.get("data-event"):
                self.events.add(data["data-event"] or "")
        if data.get("lang") == "zh-Hans":
            self.lang_zh += 1
        if tag == "table":
            self.tables += 1
        if tag == "caption":
            self.table_captions += 1
        if tag == "th":
            self.th_scopes.append(data.get("scope", ""))
        if tag == "script" and data.get("type") == "application/ld+json":
            self._json = True
            self._chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json:
            self.json_ld.append("".join(self._chunks))
            self._json = False
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._json:
            self._chunks.append(data)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def collect_types(value: object, found: set[str]) -> None:
    if isinstance(value, dict):
        t = value.get("@type")
        if isinstance(t, str):
            found.add(t)
        elif isinstance(t, list):
            found.update(item for item in t if isinstance(item, str))
        for child in value.values():
            collect_types(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_types(child, found)


def main() -> int:
    for path in (PAGE, CONTENT, MANIFEST, CLAIMS, SOURCES, SITEMAP, ROBOTS, REGISTRY):
        if not path.exists():
            fail(f"missing required artifact: {path}")

    html = PAGE.read_text(encoding="utf-8")
    for text in REQUIRED_TEXT:
        if text not in html:
            fail(f"required text missing: {text}")
    for pattern in FORBIDDEN_POSITIVE_CLAIMS:
        if re.search(pattern, html, flags=re.I):
            fail(f"forbidden positive medical claim matched: {pattern}")

    if f"PUBLIC_BUILD: {BUILD}" not in html or f'content="{BUILD}"' not in html:
        fail("build markers missing or inconsistent")
    if f'<link rel="canonical" href="{CANONICAL}">' not in html:
        fail("canonical URL missing")
    if '<meta name="robots" content="index,follow' not in html:
        fail("index/follow metadata missing")
    if "prefers-reduced-motion" not in html or ":focus-visible" not in html:
        fail("reduced-motion or focus-visible CSS missing")
    if "min-width:790px" not in html or "overflow-x:auto" not in html:
        fail("responsive table overflow handling missing")

    for hanzi, pinyin in TOKENS.items():
        if hanzi not in html or pinyin not in html:
            fail(f"verified token missing: {hanzi} / {pinyin}")

    parser = AuditParser()
    parser.feed(html)
    if parser.h1_count != 1:
        fail(f"expected one H1, found {parser.h1_count}")
    if not {"header", "main", "nav", "article", "footer"}.issubset(parser.landmarks):
        fail(f"semantic landmarks missing: {sorted({'header','main','nav','article','footer'} - parser.landmarks)}")
    if parser.tables != 1 or parser.table_captions != 1:
        fail("exactly one captioned correspondence table required")
    if "col" not in parser.th_scopes or "row" not in parser.th_scopes:
        fail("table header scopes incomplete")
    if parser.lang_zh < 6:
        fail("Chinese language tagging incomplete")
    for target in (CANONICAL, HUB, FENG_SHUI, SHOP, ETSY, BAZI):
        if target not in parser.hrefs and target != CANONICAL:
            fail(f"required route missing from anchors: {target}")
    if not {"learn_hub_click", "related_page_click", "cta_shop_click", "cta_etsy_click", "cta_bazi_chart_click"}.issubset(parser.events):
        fail("CTA analytics attributes incomplete")
    for event in REQUIRED_EVENTS:
        if event not in html:
            fail(f"analytics event missing: {event}")

    if len(parser.json_ld) != 1:
        fail(f"expected one JSON-LD block, found {len(parser.json_ld)}")
    try:
        structured = json.loads(parser.json_ld[0])
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON-LD: {exc}")
    types: set[str] = set()
    collect_types(structured, types)
    if not REQUIRED_SCHEMA_TYPES.issubset(types):
        fail(f"JSON-LD types missing: {sorted(REQUIRED_SCHEMA_TYPES - types)}")

    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    if content.get("region_policy") != "CN_SIMPLIFIED":
        fail("content region policy must be CN_SIMPLIFIED")
    if len(content.get("correspondences", [])) != 5:
        fail("five correspondence rows required in structured source")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("ticket") != "BZG-33" or manifest.get("canonical_url") != CANONICAL:
        fail("content manifest ticket or canonical mismatch")
    if manifest.get("page_type") != "supporting_deep_dive":
        fail("page type must be supporting_deep_dive")

    with CLAIMS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 10:
        fail("claim matrix requires at least 10 material claims")
    allowed_status = {"VERIFIED", "CONTEXTUAL_VARIANT", "SOURCE_NEEDED", "MISSING", "BLOCKED", "ASSUMPTION"}
    for row in rows:
        if row.get("status") not in allowed_status:
            fail(f"invalid claim status: {row.get('claim_id')} {row.get('status')}")
        try:
            confidence = int(row.get("confidence", "0"))
        except ValueError:
            fail(f"invalid confidence: {row.get('claim_id')}")
        if confidence not in range(1, 6):
            fail(f"confidence outside 1-5: {row.get('claim_id')}")

    sitemap = SITEMAP.read_text(encoding="utf-8")
    if CANONICAL not in sitemap or HUB not in sitemap or FENG_SHUI not in sitemap:
        fail("sitemap routes incomplete")
    robots = ROBOTS.read_text(encoding="utf-8")
    if "User-agent: *" not in robots or "Sitemap: https://sizhuatelier.shop/sitemap.xml" not in robots:
        fail("robots.txt incomplete")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry.get("wu_xing_tcm_organs") != CANONICAL:
        fail("authoritative TCM organs route missing")
    for key, value in registry.items():
        parsed = urlparse(str(value))
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"invalid HTTPS route in registry: {key}")

    print("PASS: BZG-33 TCM organs static validation")
    print("- source, claim and content artifacts validated")
    print("- medical-claim exclusion patterns passed")
    print("- Hanzi/Pinyin and CN_SIMPLIFIED policy passed")
    print("- SEO, JSON-LD, accessibility structure and analytics hooks passed")
    print("- canonical routes, sitemap and robots passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
