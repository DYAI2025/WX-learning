#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path("config/cornerstone-links.json")
PUBLIC_ROOT = Path("public")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    if not REGISTRY.exists():
        fail(f"missing link registry: {REGISTRY}")
    links = json.loads(REGISTRY.read_text(encoding="utf-8"))
    bazi_chart = str(links.get("bazi_chart", "")).strip()
    sizhu_atelier = str(links.get("sizhu_atelier", "")).strip()
    if not bazi_chart or not sizhu_atelier:
        fail("link registry must define bazi_chart and sizhu_atelier")

    replacements = {
        "https://bazodiac.space/atlas/": bazi_chart,
        "https://www.bazodiac.space/atlas/": bazi_chart,
        "https://bazodiac.space/": bazi_chart,
        "https://www.bazodiac.space/": bazi_chart,
        "https://sizhuatelier-shop-production.up.railway.app/": sizhu_atelier,
    }

    changed_files = 0
    for path in sorted(PUBLIC_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt", ".json"}:
            continue
        original = path.read_text(encoding="utf-8")
        updated = original
        for legacy, canonical in replacements.items():
            updated = updated.replace(legacy, canonical)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1

    print(f"PASS: normalized legacy public URLs from shared registry ({changed_files} files changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
