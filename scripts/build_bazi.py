#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_SOURCE = ROOT / "src" / "pages" / "bazi"
CSS_SOURCE = ROOT / "src" / "styles" / "bazi"
OUTPUT = ROOT / "public" / "learn" / "bazi"


def concatenate(source: Path, pattern: str) -> str:
    parts = sorted(source.glob(pattern))
    if not parts:
        raise SystemExit(f"No source parts found in {source}")
    return "".join(part.read_text(encoding="utf-8") for part in parts)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(concatenate(HTML_SOURCE, "*.html"), encoding="utf-8")
    (OUTPUT / "styles.css").write_text(concatenate(CSS_SOURCE, "*.css"), encoding="utf-8")
    print(f"PASS: built {OUTPUT / 'index.html'} and {OUTPUT / 'styles.css'}")


if __name__ == "__main__":
    main()
