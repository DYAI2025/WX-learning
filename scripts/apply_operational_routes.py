#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

PUBLIC = Path("public")
ORIGIN = "https://wx-learning-production-48d2.up.railway.app"
WU_XING_ROUTE = "/learn/wu-xing/"
BAZI_ROUTE = "/learn/bazi/"
TCM_SOURCE_ROUTE = "/learn/wu-xing/tcm-organs/"
TCM_PUBLIC_ROUTE = "/learn/wu-xing-tcm-organs/"
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>', re.I)


def replace_all(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for old in sorted(replacements, key=len, reverse=True):
        text = text.replace(old, replacements[old])
    path.write_text(text, encoding="utf-8")


def set_canonical(path: Path, canonical: str) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f'<link rel="canonical" href="{canonical}">'
    text, count = CANONICAL_RE.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"expected exactly one canonical link in {path}; found {count}")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    wu_xing = PUBLIC / "learn" / "wu-xing" / "index.html"
    bazi = PUBLIC / "learn" / "bazi" / "index.html"
    tcm_source = PUBLIC / "learn" / "wu-xing" / "tcm-organs"
    tcm_public = PUBLIC / "learn" / "wu-xing-tcm-organs"
    sitemap = PUBLIC / "sitemap.xml"
    version = PUBLIC / "version.txt"

    for path in (wu_xing, bazi, tcm_source / "index.html", sitemap):
        if not path.exists():
            raise SystemExit(f"missing required build artifact: {path}")

    if tcm_public.exists():
        shutil.rmtree(tcm_public)
    shutil.copytree(tcm_source, tcm_public)

    replace_all(
        wu_xing,
        {
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}{WU_XING_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": f"{ORIGIN}{TCM_PUBLIC_ROUTE}",
        },
    )
    replace_all(
        bazi,
        {
            "https://sizhuatelier.shop/learn/bazi/": f"{ORIGIN}{BAZI_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}{WU_XING_ROUTE}",
        },
    )
    replace_all(
        tcm_public / "index.html",
        {
            "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": f"{ORIGIN}{TCM_PUBLIC_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}{WU_XING_ROUTE}",
        },
    )

    set_canonical(wu_xing, f"{ORIGIN}{WU_XING_ROUTE}")
    set_canonical(bazi, f"{ORIGIN}{BAZI_ROUTE}")
    set_canonical(tcm_public / "index.html", f"{ORIGIN}{TCM_PUBLIC_ROUTE}")

    replace_all(
        sitemap,
        {
            "https://sizhuatelier.shop/learn/bazi/": f"{ORIGIN}{BAZI_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}{WU_XING_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": f"{ORIGIN}{TCM_PUBLIC_ROUTE}",
        },
    )

    lines = version.read_text(encoding="utf-8").splitlines() if version.exists() else []
    markers = {
        "PUBLIC_ORIGIN": ORIGIN,
        "WU_XING_OPERATIONAL_ROUTE": WU_XING_ROUTE,
        "BAZI_OPERATIONAL_ROUTE": BAZI_ROUTE,
        "TCM_ORGANS_OPERATIONAL_ROUTE": TCM_PUBLIC_ROUTE,
        "TCM_ORGANS_LEGACY_ROUTE": TCM_SOURCE_ROUTE,
    }
    retained = [line for line in lines if line.split("=", 1)[0] not in markers]
    retained.extend(f"{key}={value}" for key, value in markers.items())
    version.write_text("\n".join(retained) + "\n", encoding="utf-8")

    print("PASS: applied Railway operational routes")
    print(f"- Wu Xing: {ORIGIN}{WU_XING_ROUTE}")
    print(f"- BaZi: {ORIGIN}{BAZI_ROUTE}")
    print(f"- TCM organs: {ORIGIN}{TCM_PUBLIC_ROUTE}")
    print(f"- legacy TCM route retained: {TCM_SOURCE_ROUTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
