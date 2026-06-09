#!/usr/bin/env python3
"""
generate-library-og-images.py — Build a unique Open Graph card per
Library article so iMessage / Facebook / X previews render distinct
visuals instead of all reusing the global atlas card.

Each card uses a PHOTOGRAPH from the article as the dominant visual
(magazine-cover treatment): full-bleed photo background, soft dark
gradient overlay for text legibility, compass mark + brand text at top,
entry tag, large serif title at the bottom, URL stamp.

Outputs (1200 x 630 PNGs):
    public/library/og/index.png           — Library hub (uses global atlas image)
    public/library/og/megaliths.png       — Entry 01: Cusco stepped interlock
    public/library/og/stone-circles.png   — Entry 02: atmospheric vector (no photo available)
    public/library/og/mini-megaliths.png  — Entry 03: Ollantaytambo bent corner
    public/library/og/true-monoliths.png  — Entry 04: Kailasa Ellora aerial

Run from repo root:
    python3 scripts/generate-library-og-images.py
    git add public/library/og/
    git commit -m "Generate photo-based Library OG images"
    git push origin main

Dependencies: pip install Pillow --break-system-packages
"""
import os, sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

REPO_ROOT = Path(__file__).parent.parent
DEST_DIR = REPO_ROOT / 'public' / 'library' / 'og'
PHOTOS_DIR = REPO_ROOT / 'public' / 'library' / 'photos'
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

W, H = 1200, 630

# ============================================================
# Font loading (Mac + Linux candidates)
# ============================================================
def load_font(candidates, size):
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

TITLE_FONT = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
], 86)
TITLE_FONT_SHORT = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
], 104)
# v4 sizes — Jeff feedback on True Monoliths card:
# - BRAND keep size but rendered with stroke for thicker weight
# - ENTRY tag doubled (22 → 44)
# - Subtitle doubled (32 → 64) to carry the JTBD question
# - URL stamp removed entirely
BRAND_FONT = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
], 48)
ITALIC_FONT = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/Library/Fonts/Fraunces-Italic.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
], 32)
SUBTITLE_FONT = load_font([
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/Library/Fonts/Fraunces-Italic.ttf",
    "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
], 56)
MONO_TAG = load_font([
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Courier.ttc",
], 38)

# ============================================================
# Photo-background card composition
# ============================================================
def cover_crop(photo_path):
    """Open photo and crop-fit to W×H preserving aspect."""
    img = Image.open(photo_path).convert('RGB')
    img = ImageOps.fit(img, (W, H), method=Image.LANCZOS, centering=(0.5, 0.45))
    return img

def darken(img, factor=0.65):
    """Multiply the photo by a darkness factor for legibility."""
    enh = ImageEnhance.Brightness(img)
    return enh.enhance(factor)

def apply_gradient_overlay(img):
    """Layer a dark bottom-up gradient so the title and URL are readable."""
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Top section: very mild dark for brand chrome
    for y in range(0, 200):
        alpha = int(180 * (1 - y / 200))
        od.line([(0, y), (W, y)], fill=(13, 13, 18, alpha))
    # Bottom section: v4.1 — band starts later (340 instead of 280) so
    # more of the enigmatic photo shows above the title block.
    for y in range(340, H):
        progress = (y - 340) / (H - 340)
        alpha = int(40 + 200 * progress)
        od.line([(0, y), (W, y)], fill=(13, 13, 18, min(255, alpha)))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def draw_compass(draw, cx, cy, r, color=CHAMPAGNE_PALE, weight=2):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=weight)
    inner = int(r * 0.62)
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner),
                 outline=color, width=1)
    arm_len = int(r * 0.85)
    arm_w = max(3, int(r * 0.10))
    draw.polygon([(cx, cy - arm_len), (cx + arm_w, cy),
                  (cx, cy + arm_len), (cx - arm_w, cy)],
                 fill=CHAMPAGNE_PALE)
    draw.polygon([(cx - arm_len, cy), (cx, cy - arm_w),
                  (cx + arm_len, cy), (cx, cy + arm_w)],
                 fill=CHAMPAGNE)

def wrap_text(text, font, max_width, draw):
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

def compose_photo_card(photo_path, title, subtitle, entry_num):
    """Magazine-cover treatment: photo, gradient, brand chrome, title."""
    bg = cover_crop(photo_path)
    bg = darken(bg, factor=0.68)
    img = apply_gradient_overlay(bg)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Top brand chrome — v4 keeps size, thickens via stroke_width
    draw_compass(draw, 110, 100, 38, color=CHAMPAGNE_PALE, weight=4)
    draw.text((168, 60), "Ancient Atlas", font=BRAND_FONT, fill=IVORY,
              stroke_width=2, stroke_fill=IVORY)
    draw.text((170, 122), "Library", font=ITALIC_FONT, fill=CHAMPAGNE_PALE,
              stroke_width=1, stroke_fill=CHAMPAGNE_PALE)

    # Entry tag pill — doubled per Jeff's v4, text centered via anchor='mm' v4.1
    if entry_num is not None:
        tag = f"ENTRY {entry_num:02d}"
        pad_x, pad_y = 30, 18
        bbox = draw.textbbox((0, 0), tag, font=MONO_TAG)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pill_w = tw + pad_x * 2
        pill_h = th + pad_y * 2
        x0 = W - 80 - pill_w
        y0 = 70
        draw.rounded_rectangle(
            (x0, y0, x0 + pill_w, y0 + pill_h),
            radius=38,
            outline=CHAMPAGNE_PALE,
            fill=(13, 13, 18, 180),
            width=4,
        )
        # anchor='mm' = middle-middle, so the text geometric center
        # lands exactly on the pill geometric center
        draw.text((x0 + pill_w // 2, y0 + pill_h // 2), tag,
                  anchor='mm',
                  font=MONO_TAG, fill=CHAMPAGNE_PALE,
                  stroke_width=1, stroke_fill=CHAMPAGNE_PALE)

    # Big serif title in the bottom third
    use_font = TITLE_FONT_SHORT if len(title) < 18 else TITLE_FONT
    title_lines = wrap_text(title, use_font, 1040, draw)
    line_h = 100 if use_font == TITLE_FONT_SHORT else 92
    # v4: subtitle is doubled (56px) so reserve more vertical space
    sub_line_h = 72
    if subtitle:
        sub_lines = wrap_text(subtitle, SUBTITLE_FONT, 1040, draw)
    else:
        sub_lines = []
    total_h = line_h * len(title_lines) + (sub_line_h * len(sub_lines) + 18 if sub_lines else 0)
    # v4.1: tightened bottom margin from 70 → 40 so the title block sits
    # lower on the card and more of the enigmatic photo shows above it.
    y = H - 40 - total_h
    for line in title_lines:
        draw.text((80, y), line, font=use_font, fill=IVORY)
        y += line_h
    if sub_lines:
        y += 14
        for line in sub_lines:
            draw.text((80, y), line, font=SUBTITLE_FONT, fill=CHAMPAGNE_PALE,
                      stroke_width=1, stroke_fill=CHAMPAGNE_PALE)
            y += sub_line_h
    # URL stamp removed (v4) — redundant with the link text in the message client

    return img.convert('RGB')

# ============================================================
# Vector-only cards (for entries that lack a hero photo)
# ============================================================
def compose_atmospheric_vector(title, subtitle, entry_num, mark_fn):
    """Soft atmospheric vector card with the article's brand mark."""
    img = Image.new('RGB', (W, H), OBSIDIAN)
    # Layered radial glow background
    glow = Image.new('RGB', (W, H), OBSIDIAN)
    gd = ImageDraw.Draw(glow)
    cx, cy = 980, 380
    for r in range(800, 0, -8):
        a = max(0, 1 - r / 800)
        rgb = (
            int(OBSIDIAN[0] + (50 - OBSIDIAN[0]) * a * 0.50),
            int(OBSIDIAN[1] + (42 - OBSIDIAN[1]) * a * 0.50),
            int(OBSIDIAN[2] + (28 - OBSIDIAN[2]) * a * 0.50),
        )
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb)
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img = Image.blend(img, glow, 0.65)

    draw = ImageDraw.Draw(img, 'RGBA')
    # Top brand chrome — v4 thickened via stroke_width
    draw_compass(draw, 110, 100, 38, color=CHAMPAGNE_PALE, weight=4)
    draw.text((168, 60), "Ancient Atlas", font=BRAND_FONT, fill=IVORY,
              stroke_width=2, stroke_fill=IVORY)
    draw.text((170, 122), "Library", font=ITALIC_FONT, fill=CHAMPAGNE_PALE,
              stroke_width=1, stroke_fill=CHAMPAGNE_PALE)
    # Entry tag — doubled v4, centered v4.1
    if entry_num is not None:
        tag = f"ENTRY {entry_num:02d}"
        pad_x, pad_y = 30, 18
        bbox = draw.textbbox((0, 0), tag, font=MONO_TAG)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pill_w = tw + pad_x * 2
        pill_h = th + pad_y * 2
        x0 = W - 80 - pill_w
        y0 = 70
        draw.rounded_rectangle(
            (x0, y0, x0 + pill_w, y0 + pill_h),
            radius=38, outline=CHAMPAGNE_PALE, width=4,
        )
        draw.text((x0 + pill_w // 2, y0 + pill_h // 2), tag,
                  anchor='mm',
                  font=MONO_TAG, fill=CHAMPAGNE_PALE,
                  stroke_width=1, stroke_fill=CHAMPAGNE_PALE)

    # Decorative mark
    if mark_fn:
        mark_fn(draw)

    # Title block
    use_font = TITLE_FONT_SHORT if len(title) < 18 else TITLE_FONT
    title_lines = wrap_text(title, use_font, 720, draw)
    line_h = 100 if use_font == TITLE_FONT_SHORT else 92
    sub_line_h = 72
    sub_lines = wrap_text(subtitle, SUBTITLE_FONT, 720, draw) if subtitle else []
    total_h = line_h * len(title_lines) + (sub_line_h * len(sub_lines) + 18 if sub_lines else 0)
    y = (H - total_h) // 2 + 24
    for line in title_lines:
        draw.text((80, y), line, font=use_font, fill=IVORY)
        y += line_h
    if sub_lines:
        y += 14
        for line in sub_lines:
            draw.text((80, y), line, font=SUBTITLE_FONT, fill=CHAMPAGNE_PALE,
                      stroke_width=1, stroke_fill=CHAMPAGNE_PALE)
            y += sub_line_h
    return img.convert('RGB')

def mark_stone_circle(draw):
    cx, cy, r = 950, 380, 130
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=STONE, width=1)
    for i in range(13):
        ang = -math.pi / 2 + (2 * math.pi * i / 13)
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        h_stone = 42 if i % 2 == 0 else 32
        w_stone = 18
        # Subtle stone shadow
        draw.rectangle((x - w_stone // 2 + 2, y - h_stone // 2 + 3,
                        x + w_stone // 2 + 2, y + h_stone // 2 + 3),
                       fill=(0, 0, 0, 100))
        draw.rectangle((x - w_stone // 2, y - h_stone // 2,
                        x + w_stone // 2, y + h_stone // 2),
                       fill=STONE, outline=CHAMPAGNE_PALE, width=2)
    # Center altar stone
    draw.ellipse((cx - 14, cy - 14, cx + 14, cy + 14),
                 fill=CHAMPAGNE, outline=CHAMPAGNE_PALE, width=2)
    # Faint outer ring of seasonal sight-lines
    for i in range(8):
        ang = (2 * math.pi * i / 8)
        x1 = cx + (r + 20) * math.cos(ang)
        y1 = cy + (r + 20) * math.sin(ang)
        x2 = cx + (r + 50) * math.cos(ang)
        y2 = cy + (r + 50) * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=CHAMPAGNE, width=2)

# ============================================================
# Hub card — uses the global atlas image as a starting point
# ============================================================
def compose_hub_card():
    """Hub card uses the global atlas og-image as background with Library overlay."""
    global_og = REPO_ROOT / 'public' / 'og-image.png'
    if global_og.exists():
        bg = Image.open(global_og).convert('RGB')
        bg = bg.resize((W, H), Image.LANCZOS)
        bg = darken(bg, factor=0.18)  # Heavy darken — only the dot constellation should remain
        # Stronger top + bottom bands to fully hide the underlying chrome
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for y in range(0, 240):
            alpha = int(230 * (1 - y / 240))
            od.line([(0, y), (W, y)], fill=(13, 13, 18, alpha))
        for y in range(260, H):
            progress = (y - 260) / (H - 260)
            alpha = int(80 + 220 * progress)
            od.line([(0, y), (W, y)], fill=(13, 13, 18, min(255, alpha)))
        img = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')
    else:
        img = compose_atmospheric_vector("The Library",
                                         "Working frameworks for reading deep history.",
                                         None, None)
        return img
    draw = ImageDraw.Draw(img, 'RGBA')
    draw_compass(draw, 110, 100, 38, color=CHAMPAGNE_PALE, weight=4)
    draw.text((168, 60), "Ancient Atlas", font=BRAND_FONT, fill=IVORY,
              stroke_width=2, stroke_fill=IVORY)
    draw.text((170, 122), "Library", font=ITALIC_FONT, fill=CHAMPAGNE_PALE,
              stroke_width=1, stroke_fill=CHAMPAGNE_PALE)

    # Title — JTBD question subtitle pulled from CARDS config
    title = "The Library"
    subtitle = "How do you know what you're standing on when you arrive?"
    use_font = TITLE_FONT_SHORT
    title_lines = wrap_text(title, use_font, 1040, draw)
    line_h = 100
    sub_line_h = 72
    sub_lines = wrap_text(subtitle, SUBTITLE_FONT, 1040, draw)
    total_h = line_h * len(title_lines) + sub_line_h * len(sub_lines) + 18
    y = H - 40 - total_h
    for line in title_lines:
        draw.text((80, y), line, font=use_font, fill=IVORY)
        y += line_h
    y += 14
    for line in sub_lines:
        draw.text((80, y), line, font=SUBTITLE_FONT, fill=CHAMPAGNE_PALE,
                  stroke_width=1, stroke_fill=CHAMPAGNE_PALE)
        y += sub_line_h
    return img.convert('RGB')

# ============================================================
# Card definitions
# ============================================================
# v4 subtitle rule: each subtitle MUST be a JTBD-framed question (Jobs-To-Be-Done).
# The title says what the entry IS. The subtitle says what curiosity job
# the visitor would hire this page to do — phrased as a question that
# enhances rather than restates the title. If the subtitle were removed
# the article should be discoverable from the title alone; with the
# subtitle the click intent gets sharpened.
CARDS = [
    dict(
        slug='index',
        mode='hub',
        # Hub subtitle is set inside compose_hub_card so the whole config
        # stays a single source of truth — see that function.
    ),
    dict(
        slug='megaliths',
        mode='photo',
        entry=1,
        title='What is a Megalith?',
        subtitle="When does a stone stop being a rock and start being engineering?",
        photo=PHOTOS_DIR / 'megaliths' / '01-sacsayhuaman-wall-sweep.jpg',
    ),
    dict(
        slug='stone-circles',
        mode='photo',
        entry=2,
        title='Stone Circles',
        subtitle="What were they keeping time of, two thousand years before Pythagoras?",
        photo=PHOTOS_DIR / 'stone-circles' / '01-nabta-playa-calendar-circle.jpg',
    ),
    dict(
        slug='mini-megaliths',
        mode='photo',
        entry=3,
        title='Mini Megaliths',
        subtitle='Why does a hundred-ton wall need a hand-sized stone?',
        photo=PHOTOS_DIR / 'mini-megaliths' / '01-ollantaytambo-bent-corner-inset.jpg',
    ),
    dict(
        slug='true-monoliths',
        mode='photo',
        entry=4,
        title='True Monoliths',
        subtitle="What kind of tool turns a mountain into a working city?",
        photo=PHOTOS_DIR / 'true-monoliths' / '06-kailasa-ellora-top-down.jpg',
    ),
]

# ============================================================
def render(card):
    if card['mode'] == 'hub':
        return compose_hub_card()
    if card['mode'] == 'photo':
        if not card['photo'].exists():
            print(f"  ⚠ Photo not found: {card['photo']} — falling back to vector")
            return compose_atmospheric_vector(card['title'], card['subtitle'],
                                              card.get('entry'),
                                              card.get('mark'))
        return compose_photo_card(card['photo'], card['title'],
                                  card['subtitle'], card.get('entry'))
    if card['mode'] == 'vector':
        return compose_atmospheric_vector(card['title'], card['subtitle'],
                                          card.get('entry'),
                                          card.get('mark'))

for card in CARDS:
    img = render(card)
    out = DEST_DIR / f"{card['slug']}.png"
    img.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.relative_to(REPO_ROOT)}  ({os.path.getsize(out)/1024:.0f} KB)")

print(f"\n{len(CARDS)} Library OG cards generated at {DEST_DIR.relative_to(REPO_ROOT)}/")
