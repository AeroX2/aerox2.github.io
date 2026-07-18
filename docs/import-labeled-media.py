"""Optimise user-labelled project media and generate Svelte gallery data."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\James\Downloads\my-projects")
LABELS = ROOT / "docs" / "media-labels.json"
OUTPUT = ROOT / "public" / "labeled-media"
GENERATED = ROOT / "src" / "generatedShowcaseMedia.ts"
REPORT = ROOT / "docs" / "media-import-report.json"

PROJECT_SLUGS = {
    "Robot dog": "robodog",
    "LED display": "led-display",
    "Wireless light gun": "light-gun",
    "Moon lamp": "moon-lamp",
    "Mechanical wallet": "wallet",
    "Motor controller": "motor-controller",
    "Nintendo DS": "nintendo-ds",
    "Brother cartridge emulator": "brother-cart",
    "JRB8 computer": "jrb8",
    "Single-key keyboard": "single-key-keyboard",
    "Flare-On": "flare-on",
    "Ethereal ink frame": "epaper-frame",
    "E-paper smart watch": "epaper-smart-watch",
    "Sand table": "sand-table",
    "Moon lamp / LED display": "moon-lamp",
    "Other / unknown": "side-quests",
}

EXCLUDE = re.compile(
    r"\b(ignore|dont use|do not use|bad image|bad video|not a great video|wouldn.t use)\b",
    re.IGNORECASE,
)

# Curated near-duplicates. These are distinct source files, so a filename list is
# more reliable than exact hashing and keeps them excluded on future imports.
DUPLICATE_MEDIA = {
    "20220316_174504.jpg",        # represented by the curated project cover
    "20220316_174516.jpg",        # near-identical cartridge teardown angle
    "20220319_162423.jpg",        # blurrier version of the Arduino dump rig
    "IMG_20220904_205316969.jpg", # duplicate embroidery-machine proof shot
    "IMG_20250816_005944831.jpg", # duplicate light-gun assembly shot
    "IMG_20250817_125158359.jpg", # redundant wiring-reference close-up
    "IMG_20250817_125206545.jpg", # redundant wiring-reference close-up
    "IMG_20250817_125216657.jpg", # redundant wiring-reference close-up
    "IMG_20250505_114708888.jpg", # represented by curated sand-table media
    "IMG_20250505_114716565.jpg", # represented by curated sand-table media
    "IMG_20250604_232319486.jpg", # near-identical moon-lamp shot
    "IMG_20250604_232315307.jpg", # redundant opening moon-lamp shot
    "IMG_20250622_235128196.jpg", # redundant full-lamp angle
    "IMG_20260712_192907966.jpg", # represented by curated watch front image
    "IMG_20260712_192957692.jpg", # represented by curated watch reverse image
    "IMG_20240710_173832548.jpg", # redundant 2023 Flare-On pennant photo
    "IMG_20240910_102425855.jpg", # older wallet photo superseded by cleaner finished views
    "IMG_20250430_224124298.jpg", # redundant front-on wallet photo
    "IMG_20240104_115219476.jpg", # redundant e-paper frame display angle
    "IMG_20240104_115228831.jpg", # redundant e-paper frame display angle
    "VID_20230129_103551087.mp4", # troubleshooting footage, not portfolio evidence
    "VID_20250505_114931340.mp4", # redundant LED animation footage
}

CAPTION_OVERRIDES = {
    "20220322_172518.jpg": "The Arduino Mega test rig wired directly to the cartridge memory bus.",
    "IMG_20220904_205323758.jpg": "The replacement cartridge running custom Kirby artwork on the original embroidery machine.",
    "IMG_20220904_205342009.jpg": "The finished Kirby embroidery produced from the reverse-engineered cartridge format.",
    "IMG_20240103_231144818.jpg": "The rear of the e-paper frame, showing the compact hand-built enclosure.",
    "IMG_20240104_115219476.jpg": "The completed e-paper frame displaying a generated artwork.",
    "IMG_20240104_115228831.jpg": "A second generated composition rendered on the persistent e-paper display.",
    "IMG_20240104_115253224.jpg": "The frame's rear assembly and concealed display electronics.",
    "IMG_20231127_190526180.jpg": "The ninth annual Flare-On medal, awarded for completing the full challenge set.",
    "IMG_20240710_173832548.jpg": "The 2023 Flare-On reverse-engineering finisher pennant.",
    "IMG_20240710_173842766.jpg": "The 2023 finisher pennant, marking another completed Flare-On challenge.",
    "IMG_20250205_194546494.jpg": "The 2024 Flare-On medal, earned by completing the challenge for a fourth year.",
    "IMG_20260708_141450040.jpg": "The manufactured JRB8 on its Tiny Tapeout carrier, with external QSPI program storage.",
    "IMG_20260710_230016453.jpg": "A Tang Nano 9K FPGA used to validate the Verilog design before fabrication.",
    "VID_20250204_230808166.mp4": "An early bench test of the fabricated CPU driving its LED program display.",
    "VID_20250205_113352383.mp4": "A stable bench test of the original 8-bit computer running its display program.",
    "VID_20260712_003752420.mp4": "The fabricated JRB8 running a compiled spinning-cube demonstration.",
    "VID_20260712_025501152.mp4": "A slower spinning-cube build with the JRB8 identity rendered on screen.",
    "20211225_234441.jpg": "The first low-resolution prototype exposed severe light bleed between pixels.",
    "20230122_192240.jpg": "The ESP32 HUB75 driver schematic behind the display controller.",
    "IMG_20230129_213119097.jpg": "The next revision running the clock with a full-colour spectrum treatment.",
    "IMG_20230130_160102525.jpg": "The compact controller wiring tucked behind the HUB75 panel.",
    "IMG_20260408_112333152.jpg": "The display running a Frieren animation beneath the moon lamp.",
    "VID_20230129_213119905.mp4": "An early clock revision testing a smoothly shifting rainbow palette.",
    "VID_20230130_151111512.mp4": "A spectrum animation running on the revised display hardware.",
    "VID_20230130_151518415.mp4": "The spectrum renderer sweeping colour across the full panel.",
    "VID_20240902_210527607.mp4": "A later build revisiting the animated rainbow clock face.",
    "VID_20250612_013910584.mp4": "The current web interface controlling modes and animations in real time.",
    "IMG_20250816_005809066.jpg": "The open light-gun enclosure during wiring and final assembly.",
    "IMG_20250816_005832203.jpg": "The foot pedal and its compact battery enclosure during assembly.",
    "IMG_20250816_005950219.jpg": "The completed internal layout, including display, controls, and wireless electronics.",
    "IMG_20250817_125206545.jpg": "A wiring reference captured while building the second light gun.",
    "IMG_20250817_125216657.jpg": "A close-up of the ESP32 module and compact internal harness.",
    "IMG_20250820_163442058.jpg": "The finished wireless light gun in its printed enclosure.",
    "IMG_20250820_163454397.jpg": "The rear display provides calibration and on-device feedback.",
    "IMG_20250820_163458670.jpg": "The opposite side of the completed enclosure and control layout.",
    "IMG_20250825_015203622.jpg": "The finished foot pedal used for cover and auxiliary input.",
    "P1660999.mp4": "The wireless light gun running Time Crisis with working recoil feedback.",
    "IMG_20250604_232326646.jpg": "The moon lamp paired with an earlier revision of the LED clock.",
    "IMG_20250604_232341029.jpg": "The exposed lamp mechanism with the printed globe removed.",
    "IMG_20250612_182448668.jpg": "The illuminated moon globe on its motorised printed stand.",
    "IMG_20250622_235133126.jpg": "The completed moon lamp lit against a clear background.",
    "IMG_20260708_141050081.jpg": "The revised moon shell taking shape during a continuous 3D print.",
    "IMG_20260708_141144067.jpg": "The first lamp revision with its globe removed, exposing the motor and mount.",
    "VID_20250622_232319227.mp4": "The illuminated globe rotating on the finished stand.",
    "VID_20260708_141009787.mp4": "The revised moon shell being produced on the 3D printer.",
    "IMG_20260325_005025569.jpg": "The controller clamped to the bench for motor and robot-leg testing.",
    "IMG_20260325_005031637.jpg": "The controller mounted behind the motor during closed-loop testing.",
    "IMG_20260325_005037843.jpg": "The complete bench setup used to validate the controller against a robot leg.",
    "IMG_20260708_171726261.jpg": "The first controller revision with rework added while isolating power and sensing faults.",
    "IMG_20260708_172055064.jpg": "A Moteus controller and motor used as a known-good reference assembly.",
    "IMG_20260708_172104100.jpg": "The reverse of the reference Moteus controller.",
    "IMG_20260708_172213370.jpg": "A separate controller used to verify the motor independently during debugging.",
    "VID_20250905_221318387.mp4": "The first successful motor rotation under control of the custom board.",
    "IMG_20250910_104542261.jpg": "The damaged Nintendo DS connector secured for precision hot-air rework.",
    "IMG_20250910_105543316.jpg": "The failed connector removed cleanly before fitting its replacement.",
    "VID_20250919_155151386.mp4": "The repaired console passing its display, touch, and audio checks.",
    "VID_20250919_155316304.mp4": "A second functional test confirming the completed Nintendo DS repair.",
    "IMG_20241111_122352651.jpg": "The first complete leg assembly with motor, joints, and printed structure.",
    "IMG_20241111_122401748.jpg": "The leg assembly inverted to inspect its joint spacing and belt paths.",
    "IMG_20241111_122437126.jpg": "A side view of the first articulated leg module.",
    "IMG_20250505_114508245.jpg": "Two assembled legs during the first half-chassis fit check.",
    "IMG_20250505_114518195.jpg": "The paired leg modules before their chassis alignment was corrected.",
    "IMG_20250712_195157605.jpg": "The aluminium spine and paired leg modules taking shape on the workbench.",
    "IMG_20250712_211802667.jpg": "Assembly work on the central frame and leg mounts.",
    "IMG_20250713_014440354.jpg": "One assembled half showing the aluminium spine, paired joints, and controller mounting.",
    "IMG_20250713_014445742.jpg": "The half-chassis from the opposite side, showing the motor and belt layout.",
    "IMG_20250720_021517729.jpg": "All four legs connected for the first full-chassis wiring and fit check.",
    "IMG_20250721_233253211.jpg": "The first four-legged assembly before the rear geometry was revised.",
    "IMG_20260304_014120708.jpg": "A half-chassis test assembly with two articulated legs installed.",
    "IMG_20260304_014125093.jpg": "The robot dog undergoing frame and wiring work at the bench.",
    "IMG_20260325_005041598.jpg": "The paired leg assembly used during controller bring-up.",
    "IMG_20260325_005055913.jpg": "A single articulated leg prepared for motor-control testing.",
    "IMG_20260417_221157940.jpg": "The full quadruped assembled on the revised aluminium frame.",
    "IMG_20260524_220322875.jpg": "The nearly complete quadruped during final bench integration.",
    "IMG_20260708_141350321.jpg": "The nearly complete quadruped showing final leg spacing and the full aluminium frame.",
    "IMG_20260708_141406457.jpg": "The completed underside with all four legs, controllers, and wiring visible.",
    "IMG_20260708_141408312.jpg": "A close view of the rear joints, belt reductions, and power connections.",
    "20211225_233717.jpg": "An internet-connected motor assembly built to automate a set of window blinds.",
    "20211226_143945.jpg": "A workbench snapshot of the electronics, fabrication tools, and experiments in progress.",
    "20211226_144000.jpg": "Soldering, crimping, and prototyping tools gathered for a run of small builds.",
    "20211226_155530.jpg": "A Raspberry Pi HDMI capture setup driving reactive ambient lighting behind a television.",
    "20211226_160458.jpg": "The reactive TV-lighting controller during wiring and soldering.",
    "20211226_164852.mp4": "Hyperion matching the surrounding LED strip to the television image in real time.",
    "20230406_0004.jpg": "Infrared photography captured with a camera converted for full-spectrum imaging.",
    "20230406_0008.jpg": "A second infrared study from the full-spectrum camera conversion.",
    "20230406_0480.jpg": "An alternate infrared filter revealing a different balance of foliage and sky.",
    "20230406_0481.jpg": "Full-spectrum camera testing with a second infrared lens and filter combination.",
    "20230406_0482.jpg": "A further infrared composition used to compare converted-camera filters.",
    "IMG_20230131_214225304.jpg": "The ESP32 schematic for the air-quality clock and sensor interface.",
    "IMG_20260417_221202847.jpg": "The main project bench, tool storage, and active electronics workspace.",
    "IMG_20260708_141219876.jpg": "An ESP32 kitchen assistant combining animated clock faces with voice-triggered queries.",
    "IMG_20260712_140121760.jpg": "The sensor, display, and controller wiring inside the air-quality clock.",
    "IMG_20260712_140149943.jpg": "The assembled air-quality clock running on the bench.",
    "VID_20240613_182950394.mp4": "A mechanical segment clock advancing its motor-driven display by one minute.",
    "VID_20260622_202840254.mp4": "The kitchen assistant cycling through its ported Dwitter animations.",
    "VID_20260622_203013682.mp4": "A voice-triggered kitchen query demonstrated on the ESP32 assistant.",
    "IMG_20230829_014051610.jpg": "The controller and key PCBs before they were joined into the finished keyboard.",
    "IMG_20230829_014111730.jpg": "The assembled single-key keyboard with its custom round controller board.",
    "IMG_20231107_180616106.jpg": "A small production run of single-key keyboards prepared as giveaways.",
    "VID_20231019_152026895.mp4": "The single key triggering its programmed multi-character output.",
    "IMG_20240910_102425855.jpg": "The daily-use wallet and its cascading five-card mechanism.",
    "IMG_20250430_223514652.jpg": "The lever lifting the loaded cards into a staggered, selectable stack.",
    "IMG_20250430_223634873.jpg": "The hinged rear compartment for notes, coins, and other bulky items.",
    "IMG_20250430_224124298.jpg": "The compact front face with the card stack fully retracted.",
    "IMG_20250430_224321506.jpg": "The finished wallet closed for everyday carry.",
    "IMG_20250430_224614575.jpg": "The raised lever and fully deployed cascade of cards.",
    "VID_20240628_014412453.mp4": "The compact wallet demonstrated in everyday use.",
    "VID_20240628_014445998.mp4": "The cascading card lift and rear compartment demonstrated together.",
}

# Windows source names are not consistently cased across label exports. Keep
# caption curation stable regardless of how the labeller serialises a filename.
CAPTION_OVERRIDES = {filename.lower(): caption for filename, caption in CAPTION_OVERRIDES.items()}

IMAGE_CROPS = {
    "IMG_20230829_014111730.jpg": (0.28, 0.25, 0.74, 0.82),
    "IMG_20250604_232319486.jpg": (0.24, 0.00, 1.00, 1.00),
    "IMG_20250604_232326646.jpg": (0.00, 0.00, 0.64, 1.00),
    "IMG_20250612_182448668.jpg": (0.00, 0.00, 1.00, 0.86),
    "IMG_20250622_235133126.jpg": (0.00, 0.00, 0.72, 1.00),
    "IMG_20250622_235128196.jpg": (0.00, 0.00, 0.72, 1.00),
    "IMG_20250816_005832203.jpg": (0.00, 0.00, 1.00, 0.88),
    "IMG_20260325_005055913.jpg": (0.22, 0.00, 1.00, 1.00),
}

VIDEO_PROFILES = {
    "P1660999.mp4": {"start": 60, "duration": 100, "crop": "crop=iw*0.72:ih:iw*0.28:0", "audio": "afftdn=nf=-25"},
    "VID_20231019_152026895.mp4": {"start": 2.0, "duration": 5.4},
    "VID_20240628_014412453.mp4": {"duration": 9.5},
    "VID_20240628_014445998.mp4": {"duration": 13.0},
    "VID_20250205_113352383.mp4": {"crop": "crop=iw*0.88:ih:iw*0.12:0"},
    "VID_20260622_202840254.mp4": {"stabilize": True},
    "VID_20260712_003752420.mp4": {"stabilize": True},
    "VID_20260712_025501152.mp4": {"stabilize": True},
}


def slug_for(name: str, caption: str) -> str:
    if name:
        return PROJECT_SLUGS.get(name, "side-quests")
    lowered = caption.lower()
    if "kirby" in lowered or "embroidery" in lowered:
        return "brother-cart"
    if "robot dog" in lowered:
        return "robodog"
    return "side-quests"


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem.lower()
    return re.sub(r"[^a-z0-9_-]+", "-", stem).strip("-")


def crop_from_label(label: dict) -> tuple[float, float, float, float] | None:
    if not label.get("cropReviewed"):
        return None
    crop = label.get("crop") or {}
    try:
        left = max(0.0, min(0.99, float(crop.get("left", 0))))
        top = max(0.0, min(0.99, float(crop.get("top", 0))))
        right = max(left + 0.01, min(1.0, float(crop.get("right", 1))))
        bottom = max(top + 0.01, min(1.0, float(crop.get("bottom", 1))))
        return left, top, right, bottom
    except (TypeError, ValueError):
        return 0.0, 0.0, 1.0, 1.0


def optimise_image(source: Path, destination: Path, crop_override: tuple[float, float, float, float] | None = None) -> None:
    with Image.open(source) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGB")
        crop = crop_override if crop_override is not None else IMAGE_CROPS.get(source.name)
        if crop and crop != (0.0, 0.0, 1.0, 1.0):
            left, top, right, bottom = crop
            image = image.crop((round(image.width * left), round(image.height * top), round(image.width * right), round(image.height * bottom)))
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        image.save(destination, "JPEG", quality=84, optimize=True, progressive=True)


def optimise_video(source: Path, destination: Path, crop_override: tuple[float, float, float, float] | None = None) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    profile = VIDEO_PROFILES.get(source.name, {})
    input_args = []
    if profile.get("start") is not None:
        input_args += ["-ss", str(profile["start"])]
    if profile.get("duration") is not None:
        input_args += ["-t", str(profile["duration"])]
    transform = destination.with_suffix(".trf")
    filters = []
    if profile.get("stabilize"):
        detect = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *input_args, "-i", str(source), "-vf", f"vidstabdetect=shakiness=5:accuracy=15:result={transform.name}", "-f", "null", "NUL"]
        subprocess.run(detect, check=True, cwd=OUTPUT)
        filters.append(f"vidstabtransform=input={transform.name}:smoothing=18:optzoom=1:zoom=3")
    if crop_override is not None and crop_override != (0.0, 0.0, 1.0, 1.0):
        left, top, right, bottom = crop_override
        filters.append(f"crop=iw*{right - left:.8f}:ih*{bottom - top:.8f}:iw*{left:.8f}:ih*{top:.8f}")
    elif crop_override is None and profile.get("crop"):
        filters.append(profile["crop"])
    filters.append("scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2")
    command = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *input_args, "-i", str(source),
        "-vf", ",".join(filters),
        "-c:v", "libx264", "-preset", "medium", "-crf", "27",
    ]
    if profile.get("audio"):
        command += ["-af", profile["audio"]]
    command += ["-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(destination)]
    try:
        subprocess.run(command, check=True, cwd=OUTPUT)
    finally:
        if transform.exists():
            transform.unlink()


def ts_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    captions_only = "--captions-only" in sys.argv
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    galleries: dict[str, list[dict[str, str]]] = {}
    included: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []

    for filename, label in data.get("labels", {}).items():
        caption = CAPTION_OVERRIDES.get(Path(filename).name.lower(), (label.get("caption") or "").strip())
        notes = (label.get("notes") or "").strip()
        source = SOURCE / filename
        reason = ""
        if not source.exists():
            reason = "source missing"
        elif filename in DUPLICATE_MEDIA:
            reason = "curated duplicate"
        elif not caption:
            reason = "no description"
        elif EXCLUDE.search(f"{caption} {notes}"):
            reason = "explicitly marked poor or ignored"
        if reason:
            excluded.append({"name": filename, "reason": reason})
            continue

        project = slug_for((label.get("project") or "").strip(), caption)
        kind = label.get("kind") or ("video" if source.suffix.lower() in {".mp4", ".mov"} else "image")
        crop_override = crop_from_label(label)
        stem = safe_stem(filename)
        if kind == "video":
            output_name = f"{stem}.mp4"
            destination = OUTPUT / output_name
            if not captions_only and (label.get("cropReviewed") or source.name in VIDEO_PROFILES or not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime):
                optimise_video(source, destination, crop_override)
            entry = {"type": "video", "src": f"/labeled-media/{output_name}", "caption": caption}
        else:
            output_name = f"{stem}.jpg"
            destination = OUTPUT / output_name
            if not captions_only and (label.get("cropReviewed") or source.name in IMAGE_CROPS or not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime):
                optimise_image(source, destination, crop_override)
            entry = {"type": "image", "src": f"/labeled-media/{output_name}", "alt": caption, "caption": caption}
        galleries.setdefault(project, []).append(entry)
        included.append({"name": filename, "project": project, "kind": kind, "output": output_name})

    lines = ["import type { ShowcaseMedia } from './showcaseMedia';", "", "export const generatedShowcaseMedia: Record<string, ShowcaseMedia[]> = {"]
    for project, items in sorted(galleries.items()):
        lines.append(f"  {ts_string(project)}: [")
        for item in items:
            fields = ", ".join(f"{key}: {ts_string(value)}" for key, value in item.items())
            lines.append(f"    {{ {fields} }},")
        lines.append("  ],")
    lines.extend(["};", ""])
    GENERATED.write_text("\n".join(lines), encoding="utf-8")
    REPORT.write_text(json.dumps({"included": included, "excluded": excluded, "counts": {"included": len(included), "excluded": len(excluded)}}, indent=2), encoding="utf-8")
    print(f"Imported {len(included)} media files across {len(galleries)} project groups.")
    print(f"Excluded {len(excluded)} files. Report: {REPORT}")


if __name__ == "__main__":
    main()
