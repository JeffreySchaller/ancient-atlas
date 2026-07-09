#!/usr/bin/env python3
"""
make-merch.py — Fourthwall launch product art for Ancient Atlas.

All assets generated from the site's design tokens + live data/sites.json,
same lineage as branding/youtube/generate-channel-assets.py. 300dpi,
print-ready. Transparent-background pieces are for DTG apparel/stickers;
full-bleed pieces are for mugs/posters.

Outputs (this directory):
    merch-tee-front-light.png    4500x5400  ivory/champagne art, transparent
                                 (for obsidian/dark garments)
    merch-tee-front-dark.png     4500x5400  obsidian ink variant
                                 (for sand/ivory garments)
    merch-back-dotmap.png        4500x5400  full atlas dot map back print,
                                 transparent
    merch-sticker-compass.png    1500x1500  die-cut compass disc
    merch-mug-wrap.png           2700x1100  full-color wrap, obsidian
    poster-egypt-18x24.png       5400x7200  region print, live site count
    poster-turkiye-18x24.png     5400x7200  region print, live site count
    poster-compass-18x24.png     5400x7200  minimal compass art print

Run from repo root:
    python3 branding/print/make-merch.py [--only key]
Keys: tee_light, tee_dark, back, sticker, mug, egypt, turkiye, compass
Fonts: AA_FONT_DIR (fontsource ttf set, same as the video pipeline).
"""
import json
import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("AA_FONT_DIR", os.path.expanduser("~/fonts/ttf")))

OBSIDIAN = (13, 13, 18)
CHARCOAL = (22, 22, 29)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_DK = (143, 116, 48)
AMBER = (232, 185, 96)
IVORY = (240, 238, 233)
MIST = (138, 138, 154)

def F(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)

def fraunces(s, w=700): return F(f"fraunces-latin-{w}-normal.ttf", s)
def mono(s, w=500): return F(f"jetbrains-mono-latin-{w}-normal.ttf", s)

def tracked(d, xy, text, font, fill, tr=0.0, center=False):
    widths = [d.textlength(c, font=font) for c in text]
    total = sum(widths) + tr * (len(text) - 1)
    x, y = xy
    if center:
        x -= total / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += w + tr
    return total

def draw_compass(img, cx, cy, R, light, dark, hub_fill, ring_alpha=110):
    d = ImageDraw.Draw(img)
    def point(ang, L, hw, a_light, a_dark):
        a = math.radians(ang)
        tip = (cx + L * math.sin(a), cy - L * math.cos(a))
        p = a + math.pi / 2
        l = (cx + hw * math.sin(p), cy - hw * math.cos(p))
        r = (cx - hw * math.sin(p), cy + hw * math.cos(p))
        d.polygon([tip, l, (cx, cy)], fill=a_light)
        d.polygon([tip, r, (cx, cy)], fill=a_dark)
    for ang in (45, 135, 225, 315):
        point(ang, R * .52, R * .075, light, dark)
    for ang in (0, 90, 180, 270):
        point(ang, R * .97, R * .10,
              tuple(min(255, int(c * 1.15)) for c in light[:3]) + (255,), dark)
    hub = R * .075
    d.ellipse([cx - hub, cy - hub, cx + hub, cy + hub], fill=hub_fill,
              outline=light, width=max(2, int(R * .02)))
    rr = R
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
              outline=light[:3] + (ring_alpha,), width=max(2, int(R * .015)))

def sites():
    return json.load(open(REPO / "data" / "sites.json"))

def project(lat, lng, bounds, w, h, pad):
    lat0, lat1, lng0, lng1 = bounds
    x = pad + (lng - lng0) / (lng1 - lng0) * (w - 2 * pad)
    y = pad + (lat1 - lat) / (lat1 - lat0) * (h - 2 * pad)
    return x, y

def plot_dots(img, data, bounds, w, h, pad, r_t1, r_other, glow=True):
    if glow:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        for s in data:
            x, y = project(s["lat"], s["lng"], bounds, w, h, pad)
            rr = (r_t1 if s["tier"] == 1 else r_other) * 3
            gd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*CHAMPAGNE, 38))
        gl = gl.filter(ImageFilter.GaussianBlur(r_t1 * 1.5))
        img.alpha_composite(gl)
    d = ImageDraw.Draw(img)
    for s in data:
        x, y = project(s["lat"], s["lng"], bounds, w, h, pad)
        r = r_t1 if s["tier"] == 1 else r_other
        col = (*AMBER, 255) if s["tier"] == 1 else (*CHAMPAGNE, 220)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)

# ---- apparel front (light ink for dark garments / dark ink for light) ----
def tee_front(light_ink=True):
    W, H = 4500, 5400
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    main = (*IVORY, 255) if light_ink else (*OBSIDIAN, 255)
    acc_l = (*CHAMPAGNE, 255)
    acc_d = (*CHAMPAGNE_DK, 255)
    hub = (0, 0, 0, 0)
    draw_compass(img, W / 2, 1450, 950, acc_l, acc_d, hub, ring_alpha=140)
    d = ImageDraw.Draw(img)
    fb = fraunces(430)
    t = "THE ANCIENT ATLAS"
    # two-line stack: fits the 15in width with presence
    d.text(((W - d.textlength("THE ANCIENT", font=fb)) / 2, 2620),
           "THE ANCIENT", font=fb, fill=main)
    d.text(((W - d.textlength("ATLAS", font=fb)) / 2, 3140),
           "ATLAS", font=fb, fill=main)
    d.line([W / 2 - 1100, 3850, W / 2 + 1100, 3850], fill=acc_d, width=12)
    tracked(d, (W / 2, 3960), "A MAP OF THE DEEP PAST", mono(130), acc_l,
            tr=46, center=True)
    name = "merch-tee-front-light.png" if light_ink else "merch-tee-front-dark.png"
    img.save(OUT / name)
    print("✓", name)

# ---- back print: the whole atlas as dots ----
def back_dotmap():
    W, H = 4500, 5400
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    data = sites()
    bounds = (-56, 71, -170, 179)   # world, trimmed poles
    # map occupies upper block, 2:1-ish aspect inside 4500 wide
    map_h = 2350
    plate = Image.new("RGBA", (W, map_h), (0, 0, 0, 0))
    plot_dots(plate, data, bounds, W, map_h, 160, 16, 9)
    img.alpha_composite(plate, (0, 900))
    d = ImageDraw.Draw(img)
    tracked(d, (W / 2, 3560), f"{len(data)} SITES", mono(150), (*AMBER, 255),
            tr=60, center=True)
    tracked(d, (W / 2, 3800), "THEANCIENTATLAS.COM", mono(110),
            (*CHAMPAGNE, 255), tr=40, center=True)
    img.save(OUT / "merch-back-dotmap.png")
    print("✓ merch-back-dotmap.png")

# ---- sticker ----
def sticker():
    S = 1500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = 30
    d.ellipse([m, m, S - m, S - m], fill=(*OBSIDIAN, 255),
              outline=(*CHAMPAGNE, 255), width=14)
    draw_compass(img, S / 2, S / 2 - 60, S * 0.30, (*CHAMPAGNE, 255),
                 (*CHAMPAGNE_DK, 255), (*OBSIDIAN, 255), ring_alpha=90)
    tracked(d, (S / 2, S - 360), "ANCIENT ATLAS", mono(86), (*IVORY, 255),
            tr=18, center=True)
    tracked(d, (S / 2, S - 230), "THEANCIENTATLAS.COM", mono(46),
            (*CHAMPAGNE, 255), tr=10, center=True)
    img.save(OUT / "merch-sticker-compass.png")
    print("✓ merch-sticker-compass.png")

# ---- mug wrap ----
def mug():
    W, H = 2700, 1100
    img = Image.new("RGBA", (W, H), (*OBSIDIAN, 255))
    data = sites()
    bounds = (-56, 71, -170, 179)
    plate = Image.new("RGBA", (W, 760), (0, 0, 0, 0))
    plot_dots(plate, data, bounds, W, 760, 70, 6, 3.5, glow=False)
    img.alpha_composite(plate, (0, 60))
    d = ImageDraw.Draw(img)
    fb = fraunces(96)
    t = "THE ANCIENT ATLAS"
    d.text(((W - d.textlength(t, font=fb)) / 2, 850), t, font=fb,
           fill=(*IVORY, 255))
    tracked(d, (W / 2, 990), "A MAP OF THE DEEP PAST", mono(40),
            (*CHAMPAGNE, 255), tr=14, center=True)
    img.convert("RGB").save(OUT / "merch-mug-wrap.png")
    print("✓ merch-mug-wrap.png")

# ---- region posters ----
# NOTE: Fraunces latin subset has no U+0130 (İ), so the Türkiye title uses
# plain I. Swap to a latin-ext cut if we ever want the dotted capital.
REGION_TITLES = {"Egypt": "EGYPT", "Türkiye": "TÜRKIYE"}

def region_poster(region, key):
    W, H = 5400, 7200
    img = Image.new("RGBA", (W, H), (*OBSIDIAN, 255))
    data = [s for s in sites() if s["region"] == region]
    lats = [s["lat"] for s in data]; lngs = [s["lng"] for s in data]
    plat = (max(lats) - min(lats)) * 0.12 + 0.4
    plng = (max(lngs) - min(lngs)) * 0.12 + 0.4
    bounds = (min(lats) - plat, max(lats) + plat,
              min(lngs) - plng, max(lngs) + plng)
    map_h = 4600
    plate = Image.new("RGBA", (W, map_h), (0, 0, 0, 0))
    plot_dots(plate, data, bounds, W, map_h, 380, 30, 17)
    # tier-1 labels with greedy collision avoidance: try right, left,
    # below, above; if every position collides, skip (dot still shows)
    pd = ImageDraw.Draw(plate)
    lf = mono(64, 400)
    placed = []

    def collides(box):
        return any(not (box[2] < b[0] or box[0] > b[2] or
                        box[3] < b[1] or box[1] > b[3]) for b in placed)

    for s in sorted([s for s in data if s["tier"] == 1],
                    key=lambda s: s["n"]):
        x, y = project(s["lat"], s["lng"], bounds, W, map_h, 380)
        label = s["n"].split("(")[0].strip().upper()
        if len(label) > 26:
            label = label[:24] + "…"
        tw = pd.textlength(label, font=lf)
        th = 70
        candidates = [
            (x + 52, y - th / 2),            # right
            (x - 52 - tw, y - th / 2),       # left
            (x - tw / 2, y + 44),            # below
            (x - tw / 2, y - 44 - th),       # above
        ]
        for lx, ly in candidates:
            box = (lx - 14, ly - 8, lx + tw + 14, ly + th + 8)
            if not collides(box) and 0 <= lx and lx + tw <= W:
                pd.text((lx, ly), label, font=lf, fill=(*MIST, 235))
                placed.append(box)
                break
    img.alpha_composite(plate, (0, 1250))
    d = ImageDraw.Draw(img)
    # header
    draw_compass(img, W / 2, 470, 210, (*CHAMPAGNE, 255), (*CHAMPAGNE_DK, 255),
                 (*OBSIDIAN, 255))
    fb = fraunces(420)
    t = REGION_TITLES[region]
    d.text(((W - d.textlength(t, font=fb)) / 2, 720), t, font=fb,
           fill=(*IVORY, 255))
    # footer
    d.line([W / 2 - 1500, 6280, W / 2 + 1500, 6280],
           fill=(*CHAMPAGNE_DK, 255), width=10)
    tracked(d, (W / 2, 6400),
            f"{len(data)} SITES OF THE DEEP PAST", mono(120), (*AMBER, 255),
            tr=48, center=True)
    tracked(d, (W / 2, 6640), "THE ANCIENT ATLAS · THEANCIENTATLAS.COM",
            mono(86), (*CHAMPAGNE, 255), tr=28, center=True)
    img.convert("RGB").save(OUT / f"poster-{key}-18x24.png")
    print(f"✓ poster-{key}-18x24.png ({len(data)} sites)")

# ---- minimal compass print ----
def compass_poster():
    W, H = 5400, 7200
    img = Image.new("RGBA", (W, H), (*OBSIDIAN, 255))
    # faint radial glow behind the mark
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W/2-1900, 2950-1900, W/2+1900, 2950+1900], fill=30)
    glow = glow.filter(ImageFilter.GaussianBlur(500))
    img = Image.composite(Image.new("RGBA", (W, H), (38, 32, 20, 255)),
                          img, glow)
    draw_compass(img, W / 2, 2950, 1500, (*CHAMPAGNE, 255),
                 (*CHAMPAGNE_DK, 255), (*OBSIDIAN, 255), ring_alpha=120)
    d = ImageDraw.Draw(img)
    fb = fraunces(300)
    t = "THE ANCIENT ATLAS"
    d.text(((W - d.textlength(t, font=fb)) / 2, 5150), t, font=fb,
           fill=(*IVORY, 255))
    d.line([W / 2 - 1250, 5640, W / 2 + 1250, 5640],
           fill=(*CHAMPAGNE_DK, 255), width=10)
    tracked(d, (W / 2, 5760), "A MAP OF THE DEEP PAST", mono(110),
            (*CHAMPAGNE, 255), tr=44, center=True)
    img.convert("RGB").save(OUT / "poster-compass-18x24.png")
    print("✓ poster-compass-18x24.png")

JOBS = {
    "tee_light": lambda: tee_front(True),
    "tee_dark": lambda: tee_front(False),
    "back": back_dotmap,
    "sticker": sticker,
    "mug": mug,
    "egypt": lambda: region_poster("Egypt", "egypt"),
    "turkiye": lambda: region_poster("Türkiye", "turkiye"),
    "compass": compass_poster,
}

if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    for k, fn in JOBS.items():
        if only and k != only:
            continue
        fn()
