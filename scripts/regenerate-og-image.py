#!/usr/bin/env python3
"""
regenerate-og-image.py — Build the Open Graph preview image from current
sites.json + videos.json data.

Reads:
  data/sites.json
  data/videos.json

Writes:
  public/og-image.png  (1200×630, the size Apple/Facebook/X expect)

Run from the repo root after any content batch:
    python3 scripts/regenerate-og-image.py
    git add public/og-image.png
    git commit -m "Regenerate og-image with current site count"
    git push origin main

NOTE on Apple Messages caching: Apple's link preview service caches
og-image and og-description aggressively — sometimes 24-48 hours. To
force a refresh in iMessage:
  1. Deploy the new og-image.
  2. In iMessage, paste the URL again as a new message in a different
     chat. That re-triggers Apple's parser.
  3. Or wait ~24 hours and Apple's CDN will pick up the new image.
Old previews already in chats will not update — they're permanent.

Dependencies: pip install Pillow --break-system-packages
"""
import json, os, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
DEST = REPO_ROOT / 'public' / 'og-image.png'

# Brand palette
OBSIDIAN = (13, 13, 18)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_PALE = (232, 213, 160)
CHAMPAGNE_GLOW = (245, 220, 160)
CLOUD = (197, 197, 208)
IVORY = (240, 238, 233)
MIST = (138, 138, 154)

# ============================================================
# 1. Load current data
# ============================================================
sites_path = DATA_DIR / 'sites.json'
videos_path = DATA_DIR / 'videos.json'
if not sites_path.exists() or not videos_path.exists():
    sys.exit(f"Missing data files. Expected {sites_path} and {videos_path}")

with open(sites_path) as f:
    sites_data = json.load(f)
with open(videos_path) as f:
    videos_data = json.load(f)

# Pull coords for plotting
plot_sites = [(s.get('n', ''), float(s.get('lat', 0)), float(s.get('lng', 0)))
              for s in sites_data
              if s.get('lat') is not None and s.get('lng') is not None]
site_count = len(plot_sites)
vid_count = sum(len(v) for v in videos_data.values())

print(f"Sites: {site_count}  Walkthroughs: {vid_count}")

# ============================================================
# 2. Canvas + ambient glow
# ============================================================
W, H = 1200, 630
img = Image.new('RGB', (W, H), OBSIDIAN)

glow = Image.new('RGB', (W, H), OBSIDIAN)
gdraw = ImageDraw.Draw(glow)
for r in range(800, 0, -8):
    a = max(0, 1 - r / 800)
    rgb = (
        int(OBSIDIAN[0] + (58 - OBSIDIAN[0]) * a * 0.45),
        int(OBSIDIAN[1] + (45 - OBSIDIAN[1]) * a * 0.45),
        int(OBSIDIAN[2] + (29 - OBSIDIAN[2]) * a * 0.45),
    )
    gdraw.ellipse((280 - r, 100 - r, 280 + r, 100 + r), fill=rgb)
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.blend(img, glow, 0.6)
draw = ImageDraw.Draw(img)

# ============================================================
# 3. World map dots — equirectangular projection
# ============================================================
MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 80, 180, 1120, 540
MAP_W = MAP_RIGHT - MAP_LEFT
MAP_H = MAP_BOTTOM - MAP_TOP

def project(lat, lng):
    x = MAP_LEFT + (lng + 180) / 360 * MAP_W
    y = MAP_TOP + (90 - lat) / 180 * MAP_H
    return x, y

# Soft glow layer for dots
dot_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(dot_glow)
for name, lat, lng in plot_sites:
    x, y = project(lat, lng)
    gd.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(*CHAMPAGNE_GLOW, 50))
dot_glow = dot_glow.filter(ImageFilter.GaussianBlur(6))
img.paste(dot_glow, (0, 0), dot_glow)
draw = ImageDraw.Draw(img)

# Crisp dots on top
for name, lat, lng in plot_sites:
    x, y = project(lat, lng)
    draw.ellipse((x - 2.4, y - 2.4, x + 2.4, y + 2.4), fill=CHAMPAGNE_PALE)

# ============================================================
# 4. Fonts (try Fraunces, fall back to system)
# ============================================================
def load_font(candidates, size):
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

FRAUNCES_BOLD = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
], 72)
FRAUNCES_ITALIC = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/Library/Fonts/Fraunces-Italic.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
], 28)
MONO_REG = load_font([
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttc",
    "/System/Library/Fonts/Courier.ttc",
], 14)
MONO_BIG = load_font([
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttc",
    "/System/Library/Fonts/Courier.ttc",
], 96)

# ============================================================
# 5. Compass mark + brand
# ============================================================
def draw_compass(cx, cy, r):
    # Outer ring
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CHAMPAGNE, width=2)
    inner = int(r * 0.62)
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner),
                 outline=CHAMPAGNE, width=1)
    # Compass star (4-arm)
    arm_len = int(r * 0.85)
    arm_w = max(3, int(r * 0.10))
    draw.polygon([(cx, cy - arm_len), (cx + arm_w, cy), (cx, cy + arm_len), (cx - arm_w, cy)],
                 fill=CHAMPAGNE_PALE)
    draw.polygon([(cx - arm_len, cy), (cx, cy - arm_w), (cx + arm_len, cy), (cx, cy + arm_w)],
                 fill=CHAMPAGNE)
    draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=OBSIDIAN)

draw_compass(120, 96, 30)
draw.text((170, 60), "Ancient Atlas", font=FRAUNCES_BOLD, fill=IVORY)
draw.text((172, 132), "A map of the deep past", font=FRAUNCES_ITALIC, fill=CHAMPAGNE_PALE)

# ============================================================
# 6. Stat block (bottom-left)
# ============================================================
STAT_TOP = 565
COL_GAP = 290

# Site count
draw.text((85, STAT_TOP - 30), f"{site_count}",
          font=MONO_BIG, fill=IVORY)
draw.text((85, STAT_TOP + 65), "ANCIENT SITES MAPPED",
          font=MONO_REG, fill=MIST)

# Walkthrough count
draw.text((85 + COL_GAP, STAT_TOP - 30), f"{vid_count}",
          font=MONO_BIG, fill=IVORY)
draw.text((85 + COL_GAP, STAT_TOP + 65), "WALKTHROUGHS WIRED",
          font=MONO_REG, fill=MIST)

# URL on right
url_text = "theancientatlas.com"
url_bbox = draw.textbbox((0, 0), url_text, font=FRAUNCES_ITALIC)
url_w = url_bbox[2] - url_bbox[0]
draw.text((W - 80 - url_w, STAT_TOP + 30), url_text,
          font=FRAUNCES_ITALIC, fill=CHAMPAGNE)

# ============================================================
# 7. Save
# ============================================================
DEST.parent.mkdir(parents=True, exist_ok=True)
img.save(DEST, "PNG", optimize=True)
print(f"Saved: {DEST}  ({os.path.getsize(DEST) / 1024:.0f} KB)")
print()
print("Next steps:")
print(f"  git add public/og-image.png")
print(f"  git commit -m \"Regenerate og-image: {site_count} sites, {vid_count} walkthroughs\"")
print(f"  git push origin main")
