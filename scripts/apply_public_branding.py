#!/usr/bin/env python3
from pathlib import Path
import re

PAGE = Path("public/learn/wu-xing/index.html")
ROOT = Path("public/index.html")
VERSION = Path("public/version.txt")
CADDY = Path("Caddyfile")

SHOP_URL = "https://sizhuatelier-shop-production.up.railway.app/"
BAZIODIAC_URL = "https://bazodiac.space/"
BUILD = "wu-xing-2026-07-18-v5-cta-alignment"
CTA_ALIGNMENT_MARKER = "/* CTA_CARD_ALIGNMENT_V1 */"
CTA_ALIGNMENT_CSS = """
    /* CTA_CARD_ALIGNMENT_V1 */
    .cta-grid {
      align-items: stretch;
    }
    .cta {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    .cta > h3 {
      margin-top: 0;
    }
    .cta > p {
      margin-bottom: 1.25rem;
    }
    .cta > .button {
      margin-top: auto;
      align-self: flex-start;
      justify-content: center;
      text-align: center;
    }
"""


def replace_anchor_href(html: str, predicate, target: str) -> str:
    pattern = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.I | re.S)

    def repl(match: re.Match) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        probe = f"{attrs} {re.sub(r'<[^>]+>', ' ', body)}".lower()
        if not predicate(probe):
            return match.group(0)
        if re.search(r'\bhref\s*=\s*([\"\']).*?\1', attrs, re.I | re.S):
            attrs = re.sub(
                r'\bhref\s*=\s*([\"\']).*?\1',
                f'href="{target}"',
                attrs,
                count=1,
                flags=re.I | re.S,
            )
        else:
            attrs = f' href="{target}"{attrs}'
        return f"<a{attrs}>{body}</a>"

    return pattern.sub(repl, html)


def ensure_cta_alignment(html: str) -> str:
    if CTA_ALIGNMENT_MARKER in html:
        return html
    if "</style>" not in html:
        raise SystemExit("Cannot inject CTA alignment CSS: closing style tag missing")
    return html.replace("</style>", f"{CTA_ALIGNMENT_CSS}\n  </style>", 1)


def update_page() -> None:
    html = PAGE.read_text(encoding="utf-8")

    # Public publisher / navigation brand.
    html = html.replace("Bazodiac Learn", "Sizhu Learn")
    html = html.replace("BAZODIAC LEARN", "SIZHU LEARN")

    # Keep both CTA cards equal in height, their copy aligned at the top,
    # and their buttons aligned to the shared bottom edge.
    html = ensure_cta_alignment(html)

    # Build provenance.
    html = re.sub(
        r"PUBLIC_BUILD:\s*[A-Za-z0-9._-]+",
        f"PUBLIC_BUILD: {BUILD}",
        html,
    )
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

    # Known legacy destinations.
    legacy_product_targets = [
        "/products/wu-xing-cycle-poster/",
        "/products/wu-xing-poster/",
        "https://sizhuatelier.shop/",
    ]
    for old in legacy_product_targets:
        html = html.replace(old, SHOP_URL)

    legacy_calc_targets = [
        "/atlas/",
        "https://bazodiac.space/atlas/",
        "https://www.bazodiac.space/atlas/",
    ]
    for old in legacy_calc_targets:
        html = html.replace(old, BAZIODIAC_URL)

    # Semantic fallback: correct any CTA even if legacy wording changed.
    html = replace_anchor_href(
        html,
        lambda p: (
            'data-analytics="product"' in p
            or "poster" in p
            or "sizhu atelier shop" in p
            or "shop the" in p
        ),
        SHOP_URL,
    )
    html = replace_anchor_href(
        html,
        lambda p: (
            'data-analytics="atlas"' in p
            or 'data-analytics="bazodiac"' in p
            or "calculate with bazodiac" in p
            or "calculate your wu xing" in p
            or ("bazodiac" in p and "calculate" in p)
        ),
        BAZIODIAC_URL,
    )

    # Normalize CTA analytics naming without changing editorial content.
    html = html.replace('data-analytics="atlas"', 'data-analytics="bazodiac"')
    html = html.replace("learn_wuxing_cta_atlas_click", "learn_wuxing_cta_bazodiac_click")

    if "Bazodiac Learn" in html or "BAZODIAC LEARN" in html:
        raise SystemExit("Public header still contains Bazodiac Learn")
    if SHOP_URL not in html:
        raise SystemExit("Sizhu Atelier shop CTA missing")
    if BAZIODIAC_URL not in html:
        raise SystemExit("Bazodiac calculation CTA missing")
    if CTA_ALIGNMENT_MARKER not in html:
        raise SystemExit("CTA alignment CSS missing")

    PAGE.write_text(html, encoding="utf-8")


def update_root() -> None:
    html = ROOT.read_text(encoding="utf-8")
    html = html.replace("Bazodiac Learn", "Sizhu Learn")
    html = html.replace("BAZODIAC LEARN", "SIZHU LEARN")
    ROOT.write_text(html, encoding="utf-8")


def update_runtime_metadata() -> None:
    VERSION.write_text(
        "\n".join(
            [
                f"WU_XING_PUBLIC_BUILD={BUILD}",
                "EXPECTED_ROUTE=/learn/wu-xing/",
                "SITE_BRAND=Sizhu Learn",
                f"BAZIODIAC_CTA={BAZIODIAC_URL}",
                f"SIZHU_SHOP_CTA={SHOP_URL}",
                "CTA_ALIGNMENT=equal-cards-top-copy-bottom-buttons",
                "INTERNAL_TICKET_LABELS=removed",
                "",
            ]
        ),
        encoding="utf-8",
    )

    caddy = CADDY.read_text(encoding="utf-8")
    caddy = re.sub(
        r"X-Bazodiac-Build\s+\"[^\"]+\"",
        f'X-Sizhu-Build "{BUILD}"',
        caddy,
    )
    caddy = re.sub(
        r"X-Sizhu-Build\s+\"[^\"]+\"",
        f'X-Sizhu-Build "{BUILD}"',
        caddy,
    )
    CADDY.write_text(caddy, encoding="utf-8")


if __name__ == "__main__":
    update_page()
    update_root()
    update_runtime_metadata()
    print(f"Applied public Sizhu Learn build: {BUILD}")
