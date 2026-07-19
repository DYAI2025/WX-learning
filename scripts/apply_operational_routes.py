#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

PUBLIC = Path("public")
ORIGIN = "https://wx-learning-production-48d2.up.railway.app"
BAZI_ROUTE = "/learn/bazi/"
TCM_SOURCE_ROUTE = "/learn/wu-xing/tcm-organs/"
TCM_PUBLIC_ROUTE = "/learn/wu-xing-tcm-organs/"


def replace_all(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    bazi = PUBLIC / "learn" / "bazi" / "index.html"
    tcm_source = PUBLIC / "learn" / "wu-xing" / "tcm-organs"
    tcm_public = PUBLIC / "learn" / "wu-xing-tcm-organs"
    sitemap = PUBLIC / "sitemap.xml"
    version = PUBLIC / "version.txt"

    if not bazi.exists():
        raise SystemExit(f"missing BaZi output: {bazi}")
    if not (tcm_source / "index.html").exists():
        raise SystemExit(f"missing TCM source route: {tcm_source}")

    if tcm_public.exists():
        shutil.rmtree(tcm_public)
    shutil.copytree(tcm_source, tcm_public)

    replace_all(
        bazi,
        {
            "https://sizhuatelier.shop/learn/bazi/": f"{ORIGIN}{BAZI_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}/learn/wu-xing/",
        },
    )

    replace_all(
        tcm_public / "index.html",
        {
            "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": f"{ORIGIN}{TCM_PUBLIC_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}/learn/wu-xing/",
        },
    )

    replace_all(
        sitemap,
        {
            "https://sizhuatelier.shop/learn/bazi/": f"{ORIGIN}{BAZI_ROUTE}",
            "https://sizhuatelier.shop/learn/wu-xing/": f"{ORIGIN}/learn/wu-xing/",
            "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": f"{ORIGIN}{TCM_PUBLIC_ROUTE}",
        },
    )

    lines = version.read_text(encoding="utf-8").splitlines() if version.exists() else []
    markers = {
        "PUBLIC_ORIGIN": ORIGIN,
        "BAZI_OPERATIONAL_ROUTE": BAZI_ROUTE,
        "TCM_ORGANS_OPERATIONAL_ROUTE": TCM_PUBLIC_ROUTE,
        "TCM_ORGANS_LEGACY_ROUTE": TCM_SOURCE_ROUTE,
    }
    retained = [line for line in lines if line.split("=", 1)[0] not in markers]
    retained.extend(f"{key}={value}" for key, value in markers.items())
    version.write_text("\n".join(retained) + "\n", encoding="utf-8")

    print("PASS: applied Railway operational routes")
    print(f"- BaZi: {ORIGIN}{BAZI_ROUTE}")
    print(f"- TCM organs: {ORIGIN}{TCM_PUBLIC_ROUTE}")
    print(f"- legacy TCM route retained: {TCM_SOURCE_ROUTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
