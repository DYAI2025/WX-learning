#!/usr/bin/env python3
from pathlib import Path

VERSION = Path("public/version.txt")
MARKERS = {
    "BAZI_BUILD": "bazi-2026-07-19-v1",
    "BAZI_ROUTE": "/learn/bazi/",
    "BAZI_CANONICAL": "https://sizhuatelier.shop/learn/bazi/",
}


def main() -> int:
    lines = VERSION.read_text(encoding="utf-8").splitlines() if VERSION.exists() else []
    retained = [line for line in lines if line.split("=", 1)[0] not in MARKERS]
    retained.extend(f"{key}={value}" for key, value in MARKERS.items())
    VERSION.write_text("\n".join(retained) + "\n", encoding="utf-8")
    print("PASS: applied BaZi runtime metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
