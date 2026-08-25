from __future__ import annotations

import re
import subprocess
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
VIDEO_PATTERN = re.compile(
    r"src:\s*['\"](/(?:projects|labeled-media)/[^'\"]+\.mp4)['\"]",
    re.IGNORECASE,
)


def referenced_videos() -> list[str]:
    references: set[str] = set()
    for source in (ROOT / "src").glob("*.ts"):
        references.update(VIDEO_PATTERN.findall(source.read_text(encoding="utf-8")))
    return sorted(references)


def destination_for(reference: str) -> Path:
    return ROOT / "public" / "video-media" / reference.lstrip("/")


def poster_for(reference: str) -> Path:
    return destination_for(reference).with_suffix(".webp")


def needs_regeneration(destination: Path, source: Path) -> bool:
    return not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    generated = 0
    for reference in referenced_videos():
        source = ROOT / "source-media" / reference.lstrip("/")
        if not source.exists():
            print(f"Skipping missing source: {reference}")
            continue
        destination = destination_for(reference)
        poster = poster_for(reference)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if needs_regeneration(destination, source):
            run([
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
                "-vf", "scale='min(960,iw)':-2:flags=lanczos", "-c:v", "libx264", "-crf", "30",
                "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k",
                "-movflags", "+faststart", str(destination),
            ])
            generated += 1
        if needs_regeneration(poster, source):
            run([
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-ss", "0.5", "-i", str(source),
                "-frames:v", "1", "-vf", "scale='min(1200,iw)':-2:flags=lanczos", "-c:v", "libwebp",
                "-quality", "80", str(poster),
            ])
            generated += 1
    print(f"Generated {generated} optimised video files and posters.")


if __name__ == "__main__":
    main()
