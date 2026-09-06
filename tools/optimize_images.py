#!/usr/bin/env python3
"""Turn the docs' PNG screenshots into responsive AVIF/WebP.

Why this exists: every screenshot on the site is a full-resolution PNG — 99 of
them, 71 MB, the largest 3.1 MB — and every page served them at that size to
every device, all of them eagerly, with no `srcset` and no `loading="lazy"`.
A phone opening one page pulled 1.25 MB for a single image. That, and not the
static-site generator, is why the site felt slow on mobile.

The same picture at 480 px in AVIF is 9 KB.

Run it after adding or replacing a screenshot:

    python3 tools/optimize_images.py

It writes `assets/img/opt/<name>-<width>.{avif,webp}` plus a manifest that
build.py reads to emit a <picture> with the right srcset and the image's
intrinsic size (so the layout does not jump while it loads). Output is
committed: the encode is slow enough that doing it in CI would add minutes to
every deploy, and the results are deterministic.

Existing variants are skipped unless the source is newer, so a re-run after one
new screenshot costs a second.
"""

from __future__ import annotations

import base64
import io
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "img"
OUT = SRC / "opt"
MANIFEST = OUT / "manifest.json"

# 480 covers a phone at 1x and is what most readers will actually download;
# 1920 covers a retina laptop showing the image across the content column.
# Anything wider than the source is skipped rather than upscaled.
WIDTHS = (480, 960, 1440, 1920)

# Quality picked by eye on the densest screenshot (a full dashboard, small type
# on glass): below these the text in the UI starts to smear.
AVIF_Q = 58
WEBP_Q = 78

# The placeholder that stands in until the real image arrives: a small WebP as
# a data URI, shipped inside the HTML, so it is on screen in the first paint —
# no request, no decode wait, no second round trip.
#
# A real BlurHash would need its decoder shipped and run in JavaScript before
# anything appeared; this is the same idea with the browser's own image decoder
# doing the work, and it costs no script at all.
#
# 20 px was too few. Stretched across a phone it is not "a blurred version of
# the screenshot", it is a smear — and because the real image is lazy, that
# smear is what a reader looks at for as long as it takes to arrive. 48 px is
# still under a kilobyte and actually resembles the picture.
LQIP_WIDTH = 48


def variants(img: Image.Image) -> list[int]:
    """The widths worth writing for this image, largest first.

    Capped at the largest entry in [WIDTHS] rather than carrying the source
    width as well. The masters run to 4220 px; a `sizes` of 780 px in the
    content column asks for 1560 at 2x and 2340 at 3x, so a 2880-wide variant
    exists to serve the handful of readers on a 3x desktop display — at the
    price of doubling what the repository carries. 1920 is a screenshot of a
    user interface either way.
    """
    keep = [w for w in WIDTHS if w < img.width]
    # An image smaller than the smallest width still needs one variant.
    return sorted(keep or [img.width], reverse=True)


def placeholder(img: Image.Image) -> str:
    """A data URI of the image at [LQIP_WIDTH], for the blur-up placeholder.

    Alpha is carried through. Flattening it to RGB is what put a solid black
    rectangle behind the transparent device frames on the landing page: the
    placeholder sits *behind* the image, so wherever the image is see-through,
    the placeholder is what you see — and a flattened one is not see-through.
    """
    tiny = img.resize(
        (LQIP_WIDTH, max(1, round(img.height * LQIP_WIDTH / img.width))),
        Image.LANCZOS,
    )
    buf = io.BytesIO()
    tiny.save(buf, "WEBP", quality=60, method=6, exact=True)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def encode(img: Image.Image, path: pathlib.Path, width: int) -> None:
    scaled = (
        img
        if width == img.width
        else img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    )
    if path.suffix == ".avif":
        scaled.save(path, "AVIF", quality=AVIF_Q)
    else:
        scaled.save(path, "WEBP", quality=WEBP_Q, method=6)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict] = {}
    written = skipped = 0
    saved_from = saved_to = 0

    for src in sorted(SRC.glob("*.png")):
        img = Image.open(src)
        # Keep alpha where there is any — badges and logos need it; flatten
        # nothing, the encoders handle RGBA.
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        stem = src.stem
        widths = variants(img)
        manifest[src.name] = {
            "w": img.width,
            "h": img.height,
            "widths": widths,
            "lqip": placeholder(img),
            # Whether the source has any see-through pixels. A transparent image
            # must not be given an opaque backdrop of any kind — see placeholder().
            "alpha": img.mode == "RGBA",
        }
        saved_from += src.stat().st_size

        for width in widths:
            for ext in (".avif", ".webp"):
                dst = OUT / f"{stem}-{width}{ext}"
                if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                    skipped += 1
                    saved_to += dst.stat().st_size if width == widths[0] else 0
                    continue
                encode(img, dst, width)
                written += 1
                if width == widths[0]:
                    saved_to += dst.stat().st_size
        print(f"  {src.name}: {img.width}x{img.height} → {len(widths)} widths")

    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print(
        f"\n{len(manifest)} images · {written} written, {skipped} up to date\n"
        f"largest variant per image: {saved_to/1024/1024:.1f} MB "
        f"against {saved_from/1024/1024:.1f} MB of PNG"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
