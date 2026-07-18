from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont


VIDEO_EXTENSIONS = {'.mp4', '.mov', '.m4v', '.avi', '.webm'}


def frame_at(capture: cv2.VideoCapture, position: float) -> Image.Image | None:
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        return None
    capture.set(cv2.CAP_PROP_POS_FRAMES, max(0, int((frame_count - 1) * position)))
    ok, frame = capture.read()
    if not ok:
        return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame)


def cover(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()

    files = sorted(
        path for path in args.source.rglob('*')
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    )
    columns = 3
    thumb_width = 420
    thumb_height = 236
    label_height = 42
    rows = len(files)
    sheet = Image.new('RGB', (columns * thumb_width, rows * (thumb_height + label_height)), '#f2f0e8')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)

    for row, path in enumerate(files):
        capture = cv2.VideoCapture(str(path))
        fps = capture.get(cv2.CAP_PROP_FPS) or 0
        frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        duration = frame_count / fps if fps else 0
        for column, position in enumerate((0.18, 0.5, 0.82)):
            frame = frame_at(capture, position)
            if frame is not None:
                frame = cover(frame, thumb_width, thumb_height)
                sheet.paste(frame, (column * thumb_width, row * (thumb_height + label_height)))
        capture.release()
        label = f'{path.name}   {duration:.1f}s'
        draw.text((8, row * (thumb_height + label_height) + thumb_height + 9), label, fill='#111827', font=font)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=88, optimize=True)


if __name__ == '__main__':
    main()
