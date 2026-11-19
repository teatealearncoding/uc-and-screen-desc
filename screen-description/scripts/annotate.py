#!/usr/bin/env python3
"""Overlay numbered callout circles on a screen mockup image.

Usage:  python annotate.py mockup.png callouts.json out.png

callouts.json: [{"n": 1, "x": 430, "y": 258}, {"n": 2, "x": 430, "y": 313}, ...]
x, y are pixel coordinates of the circle CENTER in the source image, placed just to the
right of (or beside) the component being numbered. Always view the output and nudge any
circle that covers a control or sits next to the wrong one.
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

FILL, EDGE, TEXT = (232, 146, 154), (150, 60, 70), (60, 20, 25)


def font(size):
    for p in ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main(src, spec_path, out):
    img = Image.open(src).convert("RGB")
    with open(spec_path, encoding="utf8") as f:
        callouts = json.load(f)
    r = max(10, round(min(img.size) * 0.017))  # radius scales with the image
    f = font(int(r * 1.15))
    d = ImageDraw.Draw(img)
    for c in callouts:
        x, y, label = c["x"], c["y"], str(c["n"])
        d.ellipse([x - r, y - r, x + r, y + r], fill=FILL, outline=EDGE, width=2)
        d.text((x, y), label, fill=TEXT, font=f, anchor="mm")
    img.save(out)
    print("Saved", out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
