#!/usr/bin/env python3
"""
generate-channel-assets.py — Ancient Atlas YouTube channel branding kit.

Generates from the site's own design tokens (public/index.html :root):
    obsidian #0D0D12 · charcoal #16161D · slate #1E1E28 · stone #2A2A35
    champagne #C9A84C · amber #E8B960 · ivory #F0EEE9 · mist #8A8A9A
    Fraunces (serif display) · Inter (sans) · JetBrains Mono

Outputs (this directory):
    avatar-800.png              YouTube profile picture (circular-crop safe)
    banner-2560x1440.png        Channel art; text inside 1546x423 safe area;
                                dot map = all sites plotted live from
                                data/sites.json (the atlas IS the banner)
    thumbnail-template-1280x720.png   Fieldwork episode thumbnail layout
    watermark-150.png           Video watermark (compass mark)

Run from repo root:
    python3 branding/youtube/generate-channel-assets.py
Fonts: expects TTFs in the path below (fontsource woff2 -> ttf).
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("AA_FONT_DIR", "/sessions/zealous-inspiring-bell/fonts/ttf"))

# ---- tokens ----
OBSIDIAN = (13, 13, 18)
CHARCOAL = (22, 22, 29)
SLATE = (30, 30, 40)
STONE = (42, 42, 53)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_DK = (143, 116, 48)
AMBER = (232, 185, 96)
IVORY = (240, 238, 233)
MIST = (138, 138, 154)

def F(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)

def fraunces(size, wght=700):
    return F(f"fraunces-latin-{wght}-normal.ttf", size)

def inter(size, wght=400):
    return F(f"inter-latin-{wght}-normal.ttf", size)

def mono(size, wght=400):
    return F(f"jetbrains-mono-latin-{wght}-normal.ttf", size)

def tracked_text(draw, xy, text, font, fill, tracking=0.0, anchor_center=False):
    """Letterspaced text. tracking = extra px per char."""
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + tracking
    return total

# ---- compass rose mark ----
def draw_compass(img, cx, cy, R, ring=True):
    """8-point compass rose, faceted champagne, matching icon-256."""
    d = ImageDraw.Draw(img)
    def point(angle_deg, length, half_width, light, dark):
        a = math.radians(angle_deg)
        tip = (cx + length * math.sin(a), cy - length * math.cos(a))
        perp = a + math.pi / 2
        l = (cx + half_width * math.sin(perp), cy - half_width * math.cos(perp))
        r = (cx - half_width * math.sin(perp), cy + half_width * math.cos(perp))
        d.polygon([tip, l, (cx, cy)], fill=light)
        d.polygon([tip, r, (cx, cy)], fill=dark)
    for ang in (45, 135, 225, 315):
        point(ang, R * 0.52, R * 0.075, CHAMPAGNE, CHAMPAGNE_DK)
    for ang in (0, 90, 180, 270):
        point(ang, R * 0.97, R * 0.10, AMBER, CHAMPAGNE_DK)
    # center hub
    hub = R * 0.075
    d.ellipse([cx - hub, cy - hub, cx + hub, cy + hub], fill=OBSIDIAN,
              outline=CHAMPAGNE, width=max(2, int(R * 0.02)))
    if ring:
        rr = R * 1.0
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(*CHAMPAGNE, 110), width=max(2, int(R * 0.015)))

# ---- 1. avatar ----
def make_avatar():
    S = 800
    img = Image.new("RGB", (S, S), OBSIDIAN)
    d = ImageDraw.Draw(img)
    # subtle radial warmth
    glow = Image.new("L", (S, S), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([S*0.18, S*0.18, S*0.82, S*0.82], fill=26)
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(Image.new("RGB", (S, S), (38, 32, 20)), img, glow)
    overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_compass(overlay, S/2, S/2, S*0.34, ring=False)
    od = ImageDraw.Draw(overlay)
    rr = S * 0.43
    od.ellipse([S/2-rr, S/2-rr, S/2+rr, S/2+rr], outline=(*CHAMPAGNE, 120),
               width=4)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(OUT / "avatar-800.png")

# ---- 2. banner ----
def make_banner():
    W, H = 2560, 1440
    img = Image.new("RGB", (W, H), OBSIDIAN)

    # site dot map from live data, equirectangular, full bleed
    sites = json.load(open(REPO / "data" / "sites.json"))
    lats = [s["lat"] for s in sites]
    lngs = [s["lng"] for s in sites]
    lng0, lng1 = min(lngs) - 8, max(lngs) + 8
    lat0, lat1 = min(lats) - 10, max(lats) + 10
    def proj(lat, lng):
        x = (lng - lng0) / (lng1 - lng0) * W
        y = (lat1 - lat) / (lat1 - lat0) * H
        return x, y
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for s in sites:
        x, y = proj(s["lat"], s["lng"])
        r = 3.2
        dd.ellipse([x-r, y-r, x+r, y+r], fill=(*AMBER, 200))
    halo = dots.filter(ImageFilter.GaussianBlur(7))
    img.paste(Image.new("RGB", (W, H), (60, 48, 22)), (0, 0),
              halo.split()[3].point(lambda a: int(a * 0.85)))
    img.paste((232, 200, 130), (0, 0), dots.split()[3].point(lambda a: int(a*0.5)))

    # dark scrim behind safe-area text so it reads on every device crop
    safe_w, safe_h = 1546, 423
    sx, sy = (W - safe_w)//2, (H - safe_h)//2
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle([sx-90, sy-70, sx+safe_w+90, sy+safe_h+70], 60, fill=215)
    scrim = scrim.filter(ImageFilter.GaussianBlur(70))
    img = Image.composite(Image.new("RGB", (W, H), OBSIDIAN), img, scrim)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cy = H/2
    # compass mark left of the wordmark, all inside safe area
    draw_compass(overlay, sx + 200, cy - 30, 95)
    tx = sx + 360
    f_title = fraunces(128, 700)
    d.text((tx, cy - 130), "THE ANCIENT ATLAS", font=f_title, fill=IVORY)
    d.line([tx + 4, cy + 32, sx + safe_w - 200, cy + 32],
           fill=(*CHAMPAGNE, 150), width=2)
    tracked_text(d, (tx + 4, cy + 58), "A MAP OF THE DEEP PAST",
                 mono(34, 500), (*CHAMPAGNE, 255), tracking=14)
    tracked_text(d, (tx + 4, cy + 122),
                 f"{len(sites)} SITES · ORIGINAL FIELDWORK · THEANCIENTATLAS.COM",
                 mono(23, 400), (*MIST, 235), tracking=6)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(OUT / "banner-2560x1440.png")

# ---- 3. thumbnail template ----
def make_thumbnail():
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), CHARCOAL)
    d = ImageDraw.Draw(img)
    # left 65%: footage placeholder
    fw = int(W * 0.65)
    d.rectangle([0, 0, fw, H], fill=SLATE)
    for i in range(-H, fw, 56):
        d.line([i, H, i + H, 0], fill=STONE, width=2)
    ph = mono(26, 400)
    d.text((fw/2, H/2 - 20), "FOOTAGE STILL", font=ph, fill=MIST, anchor="mm")
    d.text((fw/2, H/2 + 20), "(full-bleed site photo)", font=inter(20),
           fill=MIST, anchor="mm")
    # right panel
    px = fw
    d.rectangle([px, 0, W, H], fill=OBSIDIAN)
    d.line([px, 0, px, H], fill=CHAMPAGNE, width=6)
    pad = 36
    # FIELDWORK badge
    bf = mono(22, 500)
    bw = d.textlength("FIELDWORK", font=bf) + 36
    d.rounded_rectangle([px + pad, 56, px + pad + bw, 104], 8,
                        outline=CHAMPAGNE, width=3)
    d.text((px + pad + 18, 68), "FIELDWORK", font=bf, fill=CHAMPAGNE)
    # region
    tracked_text(d, (px + pad, 150), "TÜRKIYE", mono(30, 500), AMBER, tracking=10)
    # site name (two lines max, Fraunces 600)
    d.text((px + pad, 210), "Göbekli", font=fraunces(82, 600), fill=IVORY)
    d.text((px + pad, 305), "Tepe", font=fraunces(82, 600), fill=IVORY)
    d.line([px + pad, 430, W - pad, 430], fill=STONE, width=2)
    d.text((px + pad, 452), "Episode 01 · walked by Jeff",
           font=inter(26, 400), fill=MIST)
    # compass mark bottom-right of panel
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_compass(overlay, W - 96, H - 96, 52)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(OUT / "thumbnail-template-1280x720.png")

# ---- 4. watermark ----
def make_watermark():
    S = 150
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_compass(img, S/2, S/2, S*0.44)
    img.save(OUT / "watermark-150.png")

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_avatar()
    make_banner()
    make_thumbnail()
    make_watermark()
    print("Generated:", *[p.name for p in sorted(OUT.glob('*.png'))], sep="\n  ")
