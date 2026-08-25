from __future__ import annotations

import argparse
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PATTERN = re.compile(
    r"['\"](/(?:projects|labeled-media)/[^'\"]+\.(?:jpe?g|png|webp))['\"]",
    re.IGNORECASE,
)


def referenced_images() -> list[str]:
    references: set[str] = set()
    for pattern in ("*.svelte", "*.ts", "*.css", "*.html"):
        for source in (ROOT / "src").rglob(pattern):
            references.update(REFERENCE_PATTERN.findall(source.read_text(encoding="utf-8")))
    return sorted(references)


def focus_score(path: Path) -> float:
    encoded = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return 0.0
    height, width = image.shape
    scale = min(1.0, 1200 / max(width, height))
    if scale < 1:
        image = cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_AREA)
    return float(cv2.Laplacian(image, cv2.CV_64F).var())


def make_contact_sheet(rows: list[tuple[float, str, str, float, str]], output: Path, limit: int) -> None:
    selected = [row for row in sorted(rows) if Path(row[1]).suffix.lower() in {".jpg", ".jpeg", ".webp"}][:limit]
    cell_width, cell_height = 420, 330
    columns = 3
    rows_count = (len(selected) + columns - 1) // columns
    sheet = Image.new("RGB", (cell_width * columns, cell_height * rows_count), "#111827")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=14)

    for index, (score, reference, _dimensions, _megapixels, _display_ready) in enumerate(selected):
        source = ROOT / "public" / reference.lstrip("/")
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGB")
        image.thumbnail((cell_width - 20, cell_height - 58), Image.Resampling.LANCZOS)
        x = index % columns * cell_width
        y = index // columns * cell_height
        sheet.paste(image, (x + (cell_width - image.width) // 2, y + 8))
        label = f"{score:.1f}  {Path(reference).name}"
        draw.text((x + 10, y + cell_height - 38), label, fill="white", font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--contact-limit", type=int, default=18)
    args = parser.parse_args()
    rows = []
    for reference in referenced_images():
        path = ROOT / "public" / reference.lstrip("/")
        if not path.exists():
            rows.append((0.0, reference, "missing", 0.0, "missing"))
            continue
        with Image.open(path) as image:
            width, height = image.size
        megapixels = width * height / 1_000_000
        score = focus_score(path)
        display_ready = "yes" if width >= 1120 and height >= 720 else "no"
        rows.append((score, reference, f"{width}x{height}", megapixels, display_ready))

    print(f"Referenced raster images: {len(rows)}")
    print(f"Below 1120x720 gallery target: {sum(row[4] == 'no' for row in rows)}")
    print(f"Potentially soft (focus score < 70): {sum(row[0] < 70 for row in rows)}")
    print()
    print("focus\tmegapixels\tdisplay-ready\tdimensions\tasset")
    for score, reference, dimensions, megapixels, display_ready in sorted(rows):
        print(f"{score:7.1f}\t{megapixels:5.2f}\t{display_ready:>3}\t{dimensions:>11}\t{reference}")

    if args.contact_sheet:
        make_contact_sheet(rows, args.contact_sheet, args.contact_limit)


if __name__ == "__main__":
    main()
