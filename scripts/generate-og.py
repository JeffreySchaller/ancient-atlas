#!/usr/bin/env python3
"""
generate-og.py — Regenerable Open Graph image for the Ancient Atlas.

Reads ancient-atlas-v6.html, extracts SITES (name + coordinates) and the
walkthrough count from VIDEOS, then renders a 1200×630 PNG at
deploy/og-image.png that shows:

  • A stylized world map with every site plotted as a champagne dot
  • The Ancient Atlas compass mark + wordmark
  • The current site count + "ancient sites mapped" line
  • Tagline: "A map of the deep past"
  • theancientatlas.com footer

Re-run this before any deploy where the site count has changed:
    python3 generate-og.py

Then drag the deploy/ folder to Netlify as usual.

Dependencies: Pillow (`pip install --break-system-packages Pillow`)
"""
import re, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(PROJECT_DIR, 'ancient-atlas-v6.html')
DEST = os.path.join(PROJECT_DIR, 'deploy', 'og-image.png')

# Brand
OBSIDIAN = (13, 13, 18)
OBSIDIAN_2 = (22, 22, 32)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_PALE = (232, 213, 160)
CHAMPAGNE_GLOW = (245, 220, 160)
CLOUD = (197, 197, 208)
IVORY = (240, 238, 233)
MIST = (138, 138, 154)

# ============================================================
# 1. Read sites + walkthrough count from the atlas
# ============================================================
if not os.path.exists(SRC):
    print(f"Source not found: {SRC}")
    sys.exit(1)
with open(SRC) as f:
    html = f.read()

# Extract every {n:"...", lat:N, lng:N, ...}
site_pattern = re.compile(r'\{n:"([^"]+)",lat:(-?[\d.]+),lng:(-?[\d.]+)')
sites = [(m.group(1), float(m.group(2)), float(m.group(3))) for m in site_pattern.finditer(html)]
site_count = len(sites)

# Walkthrough count (videos)
vid_count = len(re.findall(r'\{id:"[^"]+",title:"', html))

print(f"Sites: {site_count}  Walkthroughs: {vid_count}")

# ============================================================
# 2. Canvas + background
# ============================================================
W, H = 1200, 630
img = Image.new('RGB', (W, H), OBSIDIAN)
draw = ImageDraw.Draw(img)

# Radial gradient glow (warm amber from upper-left)
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
# Map area: occupy most of the canvas, with margin for chrome
MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 80, 180, 1120, 540
MAP_W = MAP_RIGHT - MAP_LEFT
MAP_H = MAP_BOTTOM - MAP_TOP

def project(lat, lng):
    """Equirectangular projection: lng [-180,180] → x, lat [-90,90] → y (inverted)."""
    x = MAP_LEFT + (lng + 180) / 360 * MAP_W
    y = MAP_TOP + (90 - lat) / 180 * MAP_H
    return x, y

# Subtle continent outline using site density — draw a faint backdrop circle field first
# to suggest where land is, then plot the actual site dots in champagne on top.
# This avoids needing a separate map image while still reading as "world map."

# Step 1: each site plotted as a small champagne dot with a soft glow
for name, lat, lng in sites:
    x, y = project(lat, lng)
    # Glow
    for r, alpha in [(10, 25), (7, 50), (4, 110)]:
        glow_layer = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow_layer)
        gd.ellipse((x - r, y - r, x + r, y + r), fill=(*CHAMPAGNE, alpha))
        img.paste(glow_layer, (0,0), glow_layer)
    # Core dot
    core = Image.new('RGBA', (W, H), (0,0,0,0))
    cd = ImageDraw.Draw(core)
    cd.ellipse((x - 2.5, y - 2.5, x + 2.5, y + 2.5), fill=(*CHAMPAGNE_GLOW, 255))
    img.paste(core, (0,0), core)

draw = ImageDraw.Draw(img)

# ============================================================
# 4. Typography — try Fraunces, fall back to system serif
# ============================================================
def load_font(size, weight='regular'):
    """Find a serif font on macOS or Linux. Fraunces local install wins; Georgia/DejaVu fall through."""
    candidates = []
    if weight == 'bold':
        candidates += [
            # User-installed Fraunces wins
            os.path.expanduser('~/Library/Fonts/Fraunces-Bold.ttf'),
            os.path.expanduser('~/Library/Fonts/Fraunces.ttf'),
            '/Library/Fonts/Fraunces-Bold.ttf',
            # macOS system
            '/System/Library/Fonts/Supplemental/Georgia Bold.ttf',
            '/Library/Fonts/Georgia Bold.ttf',
            # Linux fallback
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
        ]
    else:
        candidates += [
            os.path.expanduser('~/Library/Fonts/Fraunces.ttf'),
            os.path.expanduser('~/Library/Fonts/Fraunces-Regular.ttf'),
            '/System/Library/Fonts/Supplemental/Georgia.ttf',
            '/Library/Fonts/Georgia.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
        ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

def load_mono(size):
    for c in [
        os.path.expanduser('~/Library/Fonts/JetBrainsMono-Regular.ttf'),
        '/System/Library/Fonts/Menlo.ttc',
        '/Library/Fonts/Monaco.ttf',
        '/System/Library/Fonts/SFNSMono.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
    ]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

font_brand = load_font(56, 'bold')
font_tag = load_font(28)
font_count = load_font(96, 'bold')
font_count_label = load_mono(18)
font_footer = load_mono(15)

# ============================================================
# 5. Compass mark (top-left)
# ============================================================
cx, cy = 86, 86
r_inner = 36
# Background circle
mark_bg = Image.new('RGBA', (W, H), (0,0,0,0))
mbd = ImageDraw.Draw(mark_bg)
mbd.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
            fill=(13, 10, 7, 255), outline=(*CHAMPAGNE, 100), width=1)
img.paste(mark_bg, (0,0), mark_bg)

# Compass diamonds (champagne)
def compass_polys(cx, cy, scale):
    return [
        # Vertical arms
        [(cx, cy), (cx - 6*scale, cy - 6*scale), (cx, cy - 32*scale), (cx + 6*scale, cy - 6*scale)],
        [(cx, cy), (cx - 5*scale, cy + 5*scale), (cx, cy + 26*scale), (cx + 5*scale, cy + 5*scale)],
        # Horizontal arms
        [(cx, cy), (cx + 5*scale, cy - 5*scale), (cx + 28*scale, cy), (cx + 5*scale, cy + 5*scale)],
        [(cx, cy), (cx - 5*scale, cy - 5*scale), (cx - 28*scale, cy), (cx - 5*scale, cy + 5*scale)],
    ]
for poly in compass_polys(cx, cy, 1):
    draw.polygon(poly, fill=CHAMPAGNE_GLOW)
# Center
draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=CHAMPAGNE_GLOW)
draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=(13, 10, 7))

# ============================================================
# 6. Wordmark + tagline (top, right of compass)
# ============================================================
WORDMARK_X = 156
draw.text((WORDMARK_X, 50), 'Ancient Atlas', font=font_brand, fill=IVORY)
draw.text((WORDMARK_X, 116), 'A map of the deep past', font=font_tag, fill=CHAMPAGNE)

# ============================================================
# 7. Site count headline + tagline (bottom-left)
# ============================================================
count_str = str(site_count)
bbox = draw.textbbox((0, 0), count_str, font=font_count)
count_w = bbox[2] - bbox[0]

COUNT_X = 80
COUNT_Y = 480
draw.text((COUNT_X, COUNT_Y), count_str, font=font_count, fill=CHAMPAGNE_GLOW)

# Sub-label next to the count
label_x = COUNT_X + count_w + 18
draw.text((label_x, COUNT_Y + 38), 'ANCIENT SITES', font=font_count_label, fill=CHAMPAGNE)
draw.text((label_x, COUNT_Y + 62), 'MAPPED', font=font_count_label, fill=CHAMPAGNE)

# ============================================================
# 8. Footer URL (bottom-right)
# ============================================================
url_text = 'theancientatlas.com'
bbox = draw.textbbox((0, 0), url_text, font=font_footer)
url_w = bbox[2] - bbox[0]
draw.text((W - 80 - url_w, H - 50), url_text, font=font_footer, fill=CHAMPAGNE)

# Subtle gold separator above footer
sep_y = H - 70
draw.line((W - 80 - 200, sep_y, W - 80, sep_y), fill=(*CHAMPAGNE, 80), width=1)

# ============================================================
# 9. Save
# ============================================================
os.makedirs(os.path.dirname(DEST), exist_ok=True)
img.save(DEST, 'PNG', optimize=True, quality=92)
print(f"Saved: {DEST}")
print(f"Size: {os.path.getsize(DEST) // 1024} KB")
