#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

PUBLIC = Path("public")
ORIGIN = "https://wx-learning-production-48d2.up.railway.app"
EXPECTED = {
    PUBLIC / "learn" / "wu-xing" / "index.html": f"{ORIGIN}/learn/wu-xing/",
    PUBLIC / "learn" / "wu-xing-tcm-organs" / "index.html": f"{ORIGIN}/learn/wu-xing-tcm-organs/",
    PUBLIC / "learn" / "bazi" / "index.html": f"{ORIGIN}/learn/bazi/",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    for path, canonical in EXPECTED.items():
        if not path.exists():
            fail(f"missing operational route artifact: {path}")
        html = path.read_text(encoding="utf-8")
        if f'<link rel="canonical" href="{canonical}">' not in html:
            fail(f"operational canonical missing in {path}: {canonical}")
        if "<h1" not in html:
            fail(f"page identity missing in {path}")

    legacy = PUBLIC / "learn" / "wu-xing" / "tcm-organs" / "index.html"
    if not legacy.exists():
        fail("legacy nested TCM route must remain available")

    sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    for canonical in EXPECTED.values():
        if canonical not in sitemap:
            fail(f"sitemap missing operational route: {canonical}")

    version = (PUBLIC / "version.txt").read_text(encoding="utf-8")
    for marker in (
        f"PUBLIC_ORIGIN={ORIGIN}",
        "WU_XING_OPERATIONAL_ROUTE=/learn/wu-xing/",
        "BAZI_OPERATIONAL_ROUTE=/learn/bazi/",
        "TCM_ORGANS_OPERATIONAL_ROUTE=/learn/wu-xing-tcm-organs/",
        "TCM_ORGANS_LEGACY_ROUTE=/learn/wu-xing/tcm-organs/",
    ):
        if marker not in version:
            fail(f"version marker missing: {marker}")

    print("PASS: Railway operational route contract validated")
    print("- /learn/wu-xing/")
    print("- /learn/wu-xing-tcm-organs/")
    print("- /learn/bazi/")
    print("- nested TCM route retained for backwards compatibility")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
