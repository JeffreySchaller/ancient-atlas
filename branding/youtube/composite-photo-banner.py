#!/usr/bin/env python3
"""
composite-photo-banner.py — photographic YouTube banner: Gemini Giza plate
+ brand type from the site design tokens.

PLATE DECISION (2026-06-10): banner-plate-giza_centered.png (trio centered)
is the banner plate. The wider composition (banner-plate-giza.png) places
Gerald at 83% of frame width, which lands outside YouTube's mobile crop
band at any offset that also keeps the canvas filled; the centered plate
fits all three faces inside the band natively. The wide plate stays in the
repo as a poster/og asset.

Geometry:
  - Mobile + desktop both crop to the center 423px band; mobile further
    crops to the center 1546px. Everything essential lives in that band.
  - Plate shifted DOWN 170px so all eye-lines sit inside the band; top gap
    filled by stretching the plate's own sky.
  - Type stack sits at x 67..490 (left of the mobile band at x>=507):
    visible on desktop + TV, cropped on mobile, where YouTube shows the
    channel name as UI text anyway. Charcoal-on-sky, no scrim: honest.

Outputs: banner-photo-2560x1440.png, preview-mobile-band.png,
preview-desktop-band.png.
Run from repo root:
    python3 branding/youtube/composite-photo-banner.py
"""
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("AA_FONT_DIR", "/sessions/zealous-inspiring-bell/fonts/ttf"))

OBSIDIAN = (13, 13, 18)
CHARCOAL = (22, 22, 29)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_DK = (143, 116, 48)

W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SX, SY = (W - SAFE_W) // 2, (H - SAFE_H) // 2
SHIFT_Y = 170

def F(n, s):
    return ImageFont.truetype(str(FONT_DIR / n), s)

def tracked(d, xy, t, f, fill, tr):
    x, y = xy
    for c in t:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + tr

def compass(img, cx, cy, R):
    d = ImageDraw.Draw(img)
    def pt(a, L, hw, li, dk):
        a = math.radians(a)
        tip = (cx + L * math.sin(a), cy - L * math.cos(a))
        p = a + math.pi / 2
        l = (cx + hw * math.sin(p), cy - hw * math.cos(p))
        r = (cx - hw * math.sin(p), cy + hw * math.cos(p))
        d.polygon([tip, l, (cx, cy)], fill=li)
        d.polygon([tip, r, (cx, cy)], fill=dk)
    for a in (45, 135, 225, 315):
        pt(a, R * .52, R * .075, CHAMPAGNE, CHAMPAGNE_DK)
    for a in (0, 90, 180, 270):
        pt(a, R * .97, R * .10, CHAMPAGNE, CHAMPAGNE_DK)
    hub = R * .075
    d.ellipse([cx - hub, cy - hub, cx + hub, cy + hub],
              fill=(250, 248, 242), outline=CHAMPAGNE_DK, width=2)

def main():
    plate = Image.open(HERE / "banner-plate-giza_centered.png").convert("RGB")
    plate = plate.resize((W, round(plate.height * W / plate.width)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), OBSIDIAN)
    sky = plate.crop((0, 0, W, 80)).resize((W, SHIFT_Y + 8))
    canvas.paste(sky.filter(ImageFilter.GaussianBlur(8)), (0, 0))
    canvas.paste(plate, (0, SHIFT_Y))

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    tx, ty = 72, SY + 34
    f_big = F("fraunces-latin-700-normal.ttf", 88)
    compass(ov, tx + 40, ty + 40, 40)
    d.text((tx + 102, ty + 4), "THE",
           font=F("fraunces-latin-600-normal.ttf", 44), fill=(*CHARCOAL, 225))
    d.text((tx - 5, ty + 72), "ANCIENT", font=f_big, fill=(*CHARCOAL, 255))
    d.text((tx - 5, ty + 168), "ATLAS", font=f_big, fill=(*CHARCOAL, 255))
    d.line([tx, ty + 288, tx + 390, ty + 288], fill=(*CHAMPAGNE_DK, 210), width=3)
    tracked(d, (tx, ty + 306), "A MAP OF THE DEEP PAST",
            F("jetbrains-mono-latin-500-normal.ttf", 21), (*CHAMPAGNE_DK, 255), 5)
    tracked(d, (tx, ty + 346), "THEANCIENTATLAS.COM",
            F("jetbrains-mono-latin-400-normal.ttf", 17), (96, 94, 100, 235), 4)

    right = tx - 5 + d.textlength("ANCIENT", font=f_big)
    assert right < SX - 4, f"type bleeds into mobile band: {right}"

    out = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
    out.save(HERE / "banner-photo-2560x1440.png")
    out.crop((SX, SY, SX + SAFE_W, SY + SAFE_H)).save(HERE / "preview-mobile-band.png")
    out.crop((0, SY, W, SY + SAFE_H)).save(HERE / "preview-desktop-band.png")
    print("banner-photo-2560x1440.png + band previews written")

if __name__ == "__main__":
    main()
