from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATTERN = re.compile(
    r"['\"](/(?:projects|labeled-media)/[^'\"]+\.(?:jpe?g|png|webp))['\"]",
    re.IGNORECASE,
)
WIDTHS = (640, 1200)


def referenced_images() -> list[str]:
    references: set[str] = set()
    for pattern in ("*.svelte", "*.ts", "*.css", "*.html"):
        for source in (ROOT / "src").rglob(pattern):
            references.update(SOURCE_PATTERN.findall(source.read_text(encoding="utf-8")))
    return sorted(references)


def destination_for(reference: str, width: int) -> Path:
    relative = Path(reference.lstrip("/"))
    return ROOT / "public" / "card-media" / relative.parent / f"{relative.stem}-{width}.webp"


def make_preview(source: Path, destination: Path, width: int) -> None:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
    if image.width > width:
        image.thumbnail((width, 10_000), Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "WEBP", quality=80, method=6)


def main() -> None:
    total = 0
    for reference in referenced_images():
        source = ROOT / "public" / reference.lstrip("/")
        if not source.exists():
            print(f"Skipping missing source: {reference}")
            continue
        for width in WIDTHS:
            destination = destination_for(reference, width)
            if destination.exists() and destination.stat().st_mtime >= source.stat().st_mtime:
                continue
            make_preview(source, destination, width)
            total += 1
    print(f"Generated {total} responsive WebP card previews.")


if __name__ == "__main__":
    main()
