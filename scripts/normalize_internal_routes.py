#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

PUBLIC_ROOT = Path("public")
ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.I | re.S)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(?P<href>.*?)\1", re.I | re.S)

ROUTE_MAP = {
    "https://sizhuatelier.shop/learn/wu-xing/": "/learn/wu-xing/",
    "https://sizhuatelier.shop/learn/wu-xing/tcm-organs/": "/learn/wu-xing/tcm-organs/",
}


def rewrite_anchor(match: re.Match[str]) -> str:
    attrs = match.group("attrs")
    body = match.group("body")
    href_match = HREF_RE.search(attrs)
    if not href_match:
        return match.group(0)
    replacement = ROUTE_MAP.get(href_match.group("href"))
    if replacement is None:
        return match.group(0)
    attrs = HREF_RE.sub(lambda _: f'href="{replacement}"', attrs, count=1)
    return f"<a{attrs}>{body}</a>"


def main() -> int:
    changed = 0
    for path in sorted(PUBLIC_ROOT.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        updated = ANCHOR_RE.sub(rewrite_anchor, original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"PASS: normalized same-service Learn anchors to relative routes ({changed} files changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
