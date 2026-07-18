#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

PAGE = Path("public/learn/wu-xing/index.html")
VERSION = Path("public/version.txt")
CADDY = Path("Caddyfile")
REGISTRY = Path("config/cornerstone-links.json")
BUILD = "wu-xing-2026-07-19-v8-tcm-organs-link"
FENG_SHUI_MARKER = "CORNERSTONE_FENG_SHUI_LINK_V1"
TCM_MARKER = "CORNERSTONE_TCM_ORGANS_LINK_V1"

ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.I | re.S)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(?P<href>.*?)\1", re.I | re.S)
ANALYTICS_RE = re.compile(r"\bdata-analytics\s*=\s*([\"'])(?P<event>.*?)\1", re.I | re.S)
DIV_TOKEN_RE = re.compile(r"<div\b[^>]*>|</div>", re.I)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_registry() -> dict[str, str]:
    if not REGISTRY.exists():
        fail(f"missing link registry: {REGISTRY}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    required = {
        "sizhu_atelier",
        "sizhu_atelier_operational",
        "sizhu_atelier_etsy",
        "bazi_chart",
        "zi_wei_dou_shu_chart",
        "wu_xing_foundations",
        "wu_xing_foundations_operational",
        "wu_xing_feng_shui",
        "wu_xing_tcm_organs",
    }
    missing = sorted(required - data.keys())
    if missing:
        fail(f"link registry keys missing: {missing}")
    return {key: str(value) for key, value in data.items()}


def set_href(attrs: str, target: str) -> str:
    if HREF_RE.search(attrs):
        return HREF_RE.sub(lambda match: f'href="{target}"', attrs, count=1)
    return f' href="{target}"{attrs}'


def rewrite_anchors(html: str, links: dict[str, str]) -> str:
    legacy_targets = {
        "https://sizhuatelier-shop-production.up.railway.app/": links["sizhu_atelier"],
        "https://bazodiac.space/": links["bazi_chart"],
        "https://www.bazodiac.space/": links["bazi_chart"],
        "https://bazodiac.space/atlas/": links["bazi_chart"],
        "https://www.bazodiac.space/atlas/": links["bazi_chart"],
        "/atlas/": links["bazi_chart"],
    }

    def replace(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        probe = f"{attrs} {re.sub(r'<[^>]+>', ' ', body)}".lower()
        href_match = HREF_RE.search(attrs)
        analytics_match = ANALYTICS_RE.search(attrs)
        target = None

        if analytics_match and analytics_match.group("event") == "feng-shui":
            target = links["wu_xing_feng_shui"]
        elif analytics_match and analytics_match.group("event") == "tcm-organs":
            target = links["wu_xing_tcm_organs"]
        elif (
            'data-analytics="product"' in probe
            or "poster" in probe
            or "sizhu atelier shop" in probe
            or "shop the" in probe
        ):
            target = links["sizhu_atelier"]
        elif (
            'data-analytics="atlas"' in probe
            or 'data-analytics="bazodiac"' in probe
            or "calculate with bazodiac" in probe
            or "calculate your wu xing" in probe
            or ("bazodiac" in probe and "calculate" in probe)
        ):
            target = links["bazi_chart"]
        elif href_match:
            target = legacy_targets.get(href_match.group("href"))

        if target is None:
            return match.group(0)
        return f"<a{set_href(attrs, target)}>{body}</a>"

    return ANCHOR_RE.sub(replace, html)


def insert_before_matching_div(html: str, start_marker: str, addition: str) -> str:
    start = html.find(start_marker)
    if start < 0:
        fail(f"CTA grid not found: {start_marker}")
    depth = 0
    for token in DIV_TOKEN_RE.finditer(html, start):
        if token.group(0).lower().startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return html[: token.start()] + addition + html[token.start() :]
    fail("CTA grid closing div not found")


def ensure_feng_shui_card(html: str, links: dict[str, str]) -> str:
    if FENG_SHUI_MARKER in html:
        return html
    card = f'''<!-- {FENG_SHUI_MARKER} -->
<div class="cta"><h3>Continue with Wu Xing and Feng Shui</h3><p>See how the Five Phases are used to relate direction, season, colour and space in a source-oriented Feng Shui guide.</p><a class="button secondary" href="{links['wu_xing_feng_shui']}" data-analytics="feng-shui">Read the Feng Shui guide</a></div>'''
    return insert_before_matching_div(html, '<div class="cta-grid">', card)


def ensure_tcm_organs_card(html: str, links: dict[str, str]) -> str:
    if TCM_MARKER in html:
        return html
    card = f'''<!-- {TCM_MARKER} -->
<div class="cta"><h3>Wu Xing, TCM and organ systems</h3><p>Explore the historical correspondences among phases, zang-fu systems, seasons and emotions—with explicit medical limits.</p><a class="button secondary" href="{links['wu_xing_tcm_organs']}" data-analytics="tcm-organs">Read the TCM and organs guide</a></div>'''
    return insert_before_matching_div(html, '<div class="cta-grid">', card)


def update_build_markers(html: str) -> str:
    html = re.sub(r"PUBLIC_BUILD:\s*[A-Za-z0-9._-]+", f"PUBLIC_BUILD: {BUILD}", html)
    html = re.sub(
        r'(<meta\s+name=["\']x-public-build["\']\s+content=["\'])[^"\']+(["\'])',
        rf"\g<1>{BUILD}\g<2>",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'(data-content-version=["\'])[^"\']+(["\'])',
        rf"\g<1>{BUILD}\g<2>",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'("dateModified"\s*:\s*")[^"]+("\s*)',
        r'\g<1>2026-07-19T01:30:00+02:00\2',
        html,
        count=1,
    )
    return html


def update_runtime_metadata(links: dict[str, str]) -> None:
    VERSION.write_text(
        "\n".join(
            [
                f"WU_XING_PUBLIC_BUILD={BUILD}",
                "TCM_ORGANS_BUILD=wu-xing-tcm-organs-2026-07-19-v1",
                "EXPECTED_ROUTE=/learn/wu-xing/",
                "TCM_ORGANS_ROUTE=/learn/wu-xing/tcm-organs/",
                "SITE_BRAND=Sizhu Learn",
                f"PUBLIC_WU_XING_URL={links['wu_xing_foundations']}",
                f"OPERATIONAL_WU_XING_URL={links['wu_xing_foundations_operational']}",
                f"TCM_ORGANS_GUIDE={links['wu_xing_tcm_organs']}",
                f"FENG_SHUI_GUIDE={links['wu_xing_feng_shui']}",
                f"BAZIODIAC_CTA={links['bazi_chart']}",
                f"SIZHU_SHOP_CTA={links['sizhu_atelier']}",
                f"SIZHU_SHOP_OPERATIONAL={links['sizhu_atelier_operational']}",
                f"SIZHU_ETSY={links['sizhu_atelier_etsy']}",
                f"ZI_WEI_DOU_SHU_CHART={links['zi_wei_dou_shu_chart']}",
                "CTA_ALIGNMENT=equal-cards-top-copy-bottom-buttons",
                "EXPERT_REVIEW=historical-nuance-classical-anchors-modern-analogy-source-precision",
                "TCM_CLAIMS_POLICY=historical-correspondence-no-diagnosis-treatment-prevention-efficacy",
                "LINK_POLICY=config-cornerstone-links-json",
                "INTERNAL_TICKET_LABELS=removed",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if CADDY.exists():
        caddy = CADDY.read_text(encoding="utf-8")
        caddy = re.sub(r'X-Sizhu-Build\s+"[^"]+"', f'X-Sizhu-Build "{BUILD}"', caddy)
        caddy = re.sub(r'X-Bazodiac-Build\s+"[^"]+"', f'X-Sizhu-Build "{BUILD}"', caddy)
        CADDY.write_text(caddy, encoding="utf-8")


def main() -> int:
    links = load_registry()
    if not PAGE.exists():
        fail(f"missing page: {PAGE}")
    html = PAGE.read_text(encoding="utf-8")
    html = rewrite_anchors(html, links)
    html = ensure_feng_shui_card(html, links)
    html = ensure_tcm_organs_card(html, links)
    html = rewrite_anchors(html, links)
    html = update_build_markers(html)
    PAGE.write_text(html, encoding="utf-8")
    update_runtime_metadata(links)
    print(f"PASS: applied authoritative cornerstone links ({BUILD})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
