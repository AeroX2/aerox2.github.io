from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "public/labeled-media/img_20250604_232341029.jpg",
    "public/labeled-media/img_20250430_224614575.jpg",
    "public/projects/wallet.jpg",
    "public/labeled-media/img_20260708_141219876.jpg",
    "public/labeled-media/img_20260708_141144067.jpg",
    "public/labeled-media/img_20230829_014111730.jpg",
    "public/labeled-media/img_20250820_163458670.jpg",
    "public/labeled-media/img_20260325_005031637.jpg",
    "public/labeled-media/img_20240103_231144818.jpg",
    "public/labeled-media/img_20250430_224321506.jpg",
    "public/labeled-media/img_20250820_163454397.jpg",
    "public/labeled-media/20211225_233717.jpg",
    "public/labeled-media/img_20260325_005025569.jpg",
]


def focus_score(image: Image.Image) -> float:
    grayscale = np.asarray(image.convert("L"))
    height, width = grayscale.shape
    scale = min(1.0, 1200 / max(width, height))
    if scale < 1:
        grayscale = cv2.resize(
            grayscale,
            (round(width * scale), round(height * scale)),
            interpolation=cv2.INTER_AREA,
        )
    return float(cv2.Laplacian(grayscale, cv2.CV_64F).var())


def settings(score: float) -> tuple[float, int, int]:
    if score < 25:
        return 1.5, 105, 4
    if score < 45:
        return 1.35, 95, 4
    return 1.15, 80, 4


def enhance(source: Path, destination: Path) -> tuple[float, float]:
    with Image.open(source) as opened:
        exif = opened.getexif()
        icc_profile = opened.info.get("icc_profile")
        image = ImageOps.exif_transpose(opened).convert("RGB")
    before = focus_score(image)
    radius, percent, threshold = settings(before)
    result = image.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )
    after = focus_score(result)
    destination.parent.mkdir(parents=True, exist_ok=True)
    save_options = {
        "quality": 91,
        "optimize": True,
        "progressive": True,
    }
    if exif:
        exif[274] = 1
        save_options["exif"] = exif.tobytes()
    if icc_profile:
        save_options["icc_profile"] = icc_profile
    result.save(destination, "JPEG", **save_options)
    return before, after


def comparison_sheet(
    results: list[tuple[Path, Path, float, float]], destination: Path
) -> None:
    cell_width, image_height = 520, 310
    row_height = 360
    sheet = Image.new("RGB", (cell_width * 2, row_height * len(results)), "#111827")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=14)
    for row, (source, enhanced, before, after) in enumerate(results):
        for column, (path, label) in enumerate(((source, "original"), (enhanced, "enhanced"))):
            with Image.open(path) as opened:
                image = ImageOps.exif_transpose(opened).convert("RGB")
            image.thumbnail((cell_width - 20, image_height - 10), Image.Resampling.LANCZOS)
            x = column * cell_width + (cell_width - image.width) // 2
            y = row * row_height + 5
            sheet.paste(image, (x, y))
            draw.text(
                (column * cell_width + 10, row * row_height + image_height + 7),
                f"{label}: {source.name}  focus {before:.1f} -> {after:.1f}",
                fill="white",
                font=font,
            )
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--comparison-sheet", type=Path)
    args = parser.parse_args()

    results = []
    for relative in TARGETS:
        source = ROOT / relative
        destination = args.output_dir / relative.removeprefix("public/")
        before, after = enhance(source, destination)
        results.append((source, destination, before, after))
        print(f"{relative}: {before:.1f} -> {after:.1f}")

    if args.comparison_sheet:
        comparison_sheet(results, args.comparison_sheet)


if __name__ == "__main__":
    main()
