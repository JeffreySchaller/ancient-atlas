#!/usr/bin/env python3
"""
generate-library-og-images.py — Build a unique Open Graph card per
Library article so iMessage / Facebook / X previews render distinct
visuals instead of all reusing the global atlas card.

Outputs (1200 x 630 PNGs):
    public/library/og/index.png           — Library hub
    public/library/og/megaliths.png       — Entry 01: What is a Megalith?
    public/library/og/stone-circles.png   — Entry 02: Stone Circles
    public/library/og/mini-megaliths.png  — Entry 03: Mini Megaliths
    public/library/og/true-monoliths.png  — Entry 04: True Monoliths

Each card uses the same brand palette as the main og-image.py but with
article-specific title, subtitle, and a custom SVG-style mark drawn to
match the article's theme.

Run from repo root:
    python3 scripts/generate-library-og-images.py
    git add public/library/og/
    git commit -m "Generate unique Library OG images"
    git push origin main

Dependencies: pip install Pillow --break-system-packages
"""
import os, sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).parent.parent
DEST_DIR = REPO_ROOT / 'public' / 'library' / 'og'
DEST_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Brand palette
# ============================================================
OBSIDIAN = (13, 13, 18)
CHARCOAL = (22, 22, 29)
SLATE = (30, 30, 40)
STONE = (42, 42, 53)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_PALE = (232, 213, 160)
CHAMPAGNE_GLOW = (245, 220, 160)
IVORY = (240, 238, 233)
CLOUD = (197, 197, 208)
MIST = (138, 138, 154)
AMBER = (232, 185, 96)

W, H = 1200, 630

# ============================================================
# Font loading
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
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
], 76)
FRAUNCES_BOLD_SMALL = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
], 56)
FRAUNCES_ITALIC = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/Library/Fonts/Fraunces-Italic.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
], 30)
MONO_REG = load_font([
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Courier.ttc",
], 14)
MONO_TAG = load_font([
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Courier.ttc",
], 16)

# ============================================================
# Drawing primitives
# ============================================================
def make_base():
    """Obsidian canvas with subtle radial glow + grain."""
    img = Image.new('RGB', (W, H), OBSIDIAN)
    glow = Image.new('RGB', (W, H), OBSIDIAN)
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2 - 100, H // 2
    for r in range(700, 0, -10):
        a = max(0, 1 - r / 700)
        rgb = (
            int(OBSIDIAN[0] + (60 - OBSIDIAN[0]) * a * 0.35),
            int(OBSIDIAN[1] + (48 - OBSIDIAN[1]) * a * 0.35),
            int(OBSIDIAN[2] + (30 - OBSIDIAN[2]) * a * 0.35),
        )
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb)
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.blend(img, glow, 0.55)
    return img

def draw_compass(draw, cx, cy, r, weight=2):
    """The Ancient Atlas compass-star mark."""
    draw.ellipse((cx - r, cy - r, cx + r, cy + r),
                 outline=CHAMPAGNE, width=weight)
    inner = int(r * 0.62)
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner),
                 outline=CHAMPAGNE, width=1)
    arm_len = int(r * 0.85)
    arm_w = max(3, int(r * 0.10))
    draw.polygon([(cx, cy - arm_len), (cx + arm_w, cy),
                  (cx, cy + arm_len), (cx - arm_w, cy)],
                 fill=CHAMPAGNE_PALE)
    draw.polygon([(cx - arm_len, cy), (cx, cy - arm_w),
                  (cx + arm_len, cy), (cx, cy + arm_w)],
                 fill=CHAMPAGNE)
    draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=OBSIDIAN)

def draw_top_brand(draw, entry_num=None):
    """Top-left brand mark + wordmark, optional tag pill."""
    draw_compass(draw, 110, 90, 26)
    draw.text((158, 65), "Ancient Atlas", font=FRAUNCES_BOLD_SMALL, fill=IVORY)
    draw.text((160, 132), "Library", font=FRAUNCES_ITALIC, fill=CHAMPAGNE_PALE)
    if entry_num:
        # Tag pill in top-right
        pad_x, pad_y = 16, 8
        tag = f"ENTRY {entry_num:02d}"
        bbox = draw.textbbox((0, 0), tag, font=MONO_TAG)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x0 = W - 80 - tw - pad_x * 2
        y0 = 80
        draw.rounded_rectangle(
            (x0, y0, x0 + tw + pad_x * 2, y0 + th + pad_y * 2),
            radius=18,
            outline=CHAMPAGNE,
            width=2,
        )
        draw.text((x0 + pad_x, y0 + pad_y - 2), tag,
                  font=MONO_TAG, fill=CHAMPAGNE_PALE)

def draw_url_corner(draw):
    """Bottom-right URL stamp."""
    url = "theancientatlas.com/library"
    bbox = draw.textbbox((0, 0), url, font=FRAUNCES_ITALIC)
    tw = bbox[2] - bbox[0]
    draw.text((W - 80 - tw, H - 70), url,
              font=FRAUNCES_ITALIC, fill=CHAMPAGNE)

def wrap_text(text, font, max_width, draw):
    """Break text into lines that fit within max_width."""
    words = text.split()
    lines = []
    cur = []
    for w in words:
        test = ' '.join(cur + [w])
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(' '.join(cur))
            cur = [w]
    if cur:
        lines.append(' '.join(cur))
    return lines

def draw_title_block(draw, title, subtitle, y_anchor=255):
    """Render the article title + italic subtitle."""
    title_lines = wrap_text(title, FRAUNCES_BOLD, 1040, draw)
    y = y_anchor
    for line in title_lines:
        draw.text((80, y), line, font=FRAUNCES_BOLD, fill=IVORY)
        y += 88
    y += 10
    sub_lines = wrap_text(subtitle, FRAUNCES_ITALIC, 1040, draw)
    for line in sub_lines:
        draw.text((80, y), line, font=FRAUNCES_ITALIC, fill=CHAMPAGNE_PALE)
        y += 42

# ============================================================
# Article-specific decorative marks
# ============================================================
def mark_polygonal_wall(draw):
    """Entry 01 mark: cyclopean polygonal blocks."""
    # Stack a tessellation of irregular polygonal blocks on the right
    poly1 = [(880, 460), (1020, 440), (1100, 490), (1080, 560), (940, 575), (870, 530)]
    poly2 = [(1020, 440), (1130, 420), (1170, 480), (1100, 490)]
    poly3 = [(870, 530), (940, 575), (920, 590), (855, 580)]
    poly4 = [(1080, 560), (1130, 555), (1140, 590), (1095, 595)]
    for poly in [poly1, poly2, poly3, poly4]:
        draw.polygon(poly, fill=STONE, outline=CHAMPAGNE)
    # Small accent stone (the "mini megalith" hint)
    poly_mini = [(1015, 510), (1045, 505), (1052, 530), (1025, 538)]
    draw.polygon(poly_mini, fill=CHARCOAL, outline=CHAMPAGNE_PALE)

def mark_stone_circle(draw):
    """Entry 02 mark: stone circle plan view."""
    cx, cy, r = 1010, 480, 95
    # Outer faint guideline
    draw.ellipse((cx - r, cy - r, cx + r, cy + r),
                 outline=STONE, width=1)
    # 12 standing stones around the ring
    for i in range(12):
        ang = -math.pi / 2 + (2 * math.pi * i / 12)
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        # Stone as a small upright rectangle, slightly varied height
        h_stone = 28 if i % 2 == 0 else 22
        w_stone = 12
        draw.rectangle((x - w_stone // 2, y - h_stone // 2,
                        x + w_stone // 2, y + h_stone // 2),
                       fill=STONE, outline=CHAMPAGNE)
    # Center stone (altar / sighting stone)
    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=CHAMPAGNE)

def mark_mini_megalith(draw):
    """Entry 03 mark: cyclopean wall with small interlocking stones."""
    # Two large blocks with a small stone wedged between
    big1 = [(840, 450), (980, 440), (995, 540), (855, 560)]
    big2 = [(995, 540), (1140, 530), (1150, 595), (1010, 605)]
    big3 = [(980, 440), (1140, 420), (1140, 530), (995, 540)]
    for poly in [big1, big2, big3]:
        draw.polygon(poly, fill=STONE, outline=CHAMPAGNE)
    # The mini stone — the punctuating detail
    mini = [(970, 525), (1010, 515), (1018, 555), (978, 565)]
    draw.polygon(mini, fill=CHAMPAGNE, outline=CHAMPAGNE_PALE)
    # Tiny highlight on the mini stone to draw the eye
    draw.ellipse((985, 535, 1003, 545), fill=CHAMPAGNE_GLOW)

def mark_true_monolith(draw):
    """Entry 04 mark: a temple carved out of a mountain (Kailasa style)."""
    # The mountain — large triangular silhouette
    mountain = [(820, 600), (1180, 600), (1000, 380)]
    draw.polygon(mountain, fill=CHARCOAL, outline=STONE)
    # The carved pit around the temple (lower-tone trapezoid in the mountain)
    pit = [(900, 600), (1100, 600), (1080, 510), (920, 510)]
    draw.polygon(pit, fill=OBSIDIAN, outline=STONE)
    # The temple — block standing in the pit, attached to bedrock at the base
    temple_base = [(945, 600), (1055, 600), (1055, 555), (945, 555)]
    temple_mid  = [(950, 555), (1050, 555), (1050, 525), (950, 525)]
    temple_top  = [(965, 525), (1035, 525), (1035, 495), (965, 495)]
    draw.polygon(temple_base, fill=STONE, outline=CHAMPAGNE)
    draw.polygon(temple_mid, fill=STONE, outline=CHAMPAGNE)
    draw.polygon(temple_top, fill=CHAMPAGNE, outline=CHAMPAGNE_PALE)
    # A small spire at the very top of the temple
    spire = [(995, 495), (1005, 495), (1000, 478)]
    draw.polygon(spire, fill=CHAMPAGNE_PALE)

def mark_library_hub(draw):
    """index.html mark: an open book with the compass-star above."""
    # Open book base
    page_l = [(870, 540), (995, 525), (1000, 600), (875, 605)]
    page_r = [(1000, 525), (1130, 540), (1125, 605), (1000, 600)]
    draw.polygon(page_l, fill=STONE, outline=CHAMPAGNE)
    draw.polygon(page_r, fill=STONE, outline=CHAMPAGNE)
    # Spine line
    draw.line([(1000, 525), (1000, 600)], fill=CHAMPAGNE, width=2)
    # Line decorations on pages (ruled lines)
    for i, dy in enumerate([544, 558, 572]):
        draw.line([(890, dy), (985, dy - 1)], fill=MIST, width=1)
        draw.line([(1015, dy - 1), (1110, dy)], fill=MIST, width=1)
    # Compass star floating above the book
    draw_compass(draw, 1000, 460, 36, weight=2)

# ============================================================
# Render each card
# ============================================================
CARDS = [
    dict(
        slug='index',
        entry=None,
        title='The Library',
        subtitle='Working frameworks for reading deep history sites well.',
        mark=mark_library_hub,
    ),
    dict(
        slug='megaliths',
        entry=1,
        title='What is a Megalith?',
        subtitle='Cyclopean, polygonal, mortarless. A working vocabulary of deep stone.',
        mark=mark_polygonal_wall,
    ),
    dict(
        slug='stone-circles',
        entry=2,
        title='Stone Circles',
        subtitle='Pythagorean geometry, the megalithic yard, and the patterns that repeat.',
        mark=mark_stone_circle,
    ),
    dict(
        slug='mini-megaliths',
        entry=3,
        title='Mini Megaliths',
        subtitle='Why does a hundred-ton wall need a hand-sized stone?',
        mark=mark_mini_megalith,
    ),
    dict(
        slug='true-monoliths',
        entry=4,
        title='True Monoliths',
        subtitle='Cities carved from mountains, and the chisel marks that do not act like chisels.',
        mark=mark_true_monolith,
    ),
]

# ============================================================
def render(card):
    img = make_base()
    draw = ImageDraw.Draw(img)
    # Subtle horizontal rule under the brand header
    draw.line([(80, 195), (W - 80, 195)], fill=STONE, width=1)
    # Title block — anchor depends on subtitle length
    y_anchor = 255 if len(card['title']) < 30 else 235
    draw_title_block(draw, card['title'], card['subtitle'], y_anchor=y_anchor)
    # Article-specific decorative mark
    if card.get('mark'):
        card['mark'](draw)
    # Common brand chrome
    draw_top_brand(draw, entry_num=card.get('entry'))
    draw_url_corner(draw)
    # Bottom-left footer label
    label = "THE ANCIENT ATLAS · LIBRARY"
    draw.text((80, H - 70), label, font=MONO_REG, fill=MIST)
    return img

for card in CARDS:
    img = render(card)
    out = DEST_DIR / f"{card['slug']}.png"
    img.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.relative_to(REPO_ROOT)}  ({os.path.getsize(out)/1024:.0f} KB)")

print(f"\n{len(CARDS)} Library OG cards generated at {DEST_DIR.relative_to(REPO_ROOT)}/")
