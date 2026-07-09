#!/usr/bin/env python3
"""
generate-fourthwall-og.py — Custom OG card for the Fourthwall store.

Default Fourthwall sharing image is a blank-white fallback. This
generates a brand-coherent 1200x630 PNG that mirrors the atlas
design language : dark moonlight background, gold compass star,
Fraunces serif wordmark, italic "Editions" subtitle.

Output goes to two places :
    1. The repo at branding/fourthwall/og-card.png (versioned)
    2. iCloud root at AncientAtlas_Fourthwall_OG.png (for upload)

Upload destination : Fourthwall → Settings → General → Site details
                     → Social sharing image (1200x630 recommended)
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).parent.parent
REPO_OUT = REPO_ROOT / "branding" / "fourthwall" / "og-card.png"

# Resolve iCloud Drive root robustly — Path.home() lies inside sandboxes.
def _resolve_icloud():
    real_home = Path("/Users/jeffreyschaller/Library/Mobile Documents/com~apple~CloudDocs")
    sandbox_mount = Path("/sessions/dreamy-kind-mayer/mnt/com~apple~CloudDocs")
    sandbox_home = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
    for candidate in (real_home, sandbox_mount, sandbox_home):
        if candidate.exists():
            return candidate
    return sandbox_home  # final fallback

ICLOUD_OUT = _resolve_icloud() / "AncientAtlas_Fourthwall_OG.png"

W, H = 1200, 630

# Brand palette — pulled from the atlas
INK_TOP = (10, 19, 32)
INK_BOTTOM = (21, 32, 43)
GOLD = (201, 168, 76)
GOLD_BRIGHT = (232, 200, 150)
CREAM = (242, 230, 200)
DIM = (148, 156, 168)

FONTS_BOLD = [
    "/Library/Fonts/Fraunces-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
FONTS_ITALIC = [
    "/Library/Fonts/Fraunces-Italic.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
]
FONTS_REGULAR = [
    "/Library/Fonts/Fraunces-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]

def find_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def gradient_bg():
    img = Image.new("RGB", (W, H), INK_TOP)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(INK_TOP[0] + (INK_BOTTOM[0] - INK_TOP[0]) * t)
        g = int(INK_TOP[1] + (INK_BOTTOM[1] - INK_TOP[1]) * t)
        b = int(INK_TOP[2] + (INK_BOTTOM[2] - INK_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def draw_compass_star(draw, cx, cy, radius, color):
    """Eight-point gold compass star with long N/S/E/W and short diagonal points."""
    long_pts = []
    short_pts = []
    inner = radius * 0.18
    short_r = radius * 0.55
    for i in range(4):
        angle = i * math.pi / 2 - math.pi / 2
        long_pts.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    for i in range(4):
        angle = i * math.pi / 2 + math.pi / 4 - math.pi / 2
        short_pts.append((cx + math.cos(angle) * short_r, cy + math.sin(angle) * short_r))

    # Long points (N, E, S, W) — diamond petals
    for i, (px, py) in enumerate(long_pts):
        prev_short = short_pts[(i - 1) % 4]
        next_short = short_pts[i]
        poly = [(cx, cy), prev_short, (px, py), next_short]
        draw.polygon(poly, fill=color)

    # Short points (NE, SE, SW, NW)
    short_color = tuple(int(c * 0.75) for c in color)
    for i, (px, py) in enumerate(short_pts):
        prev_long = long_pts[i]
        next_long = long_pts[(i + 1) % 4]
        poly = [(cx, cy), prev_long, (px, py), next_long]
        draw.polygon(poly, fill=short_color)

    # Center jewel
    jewel_r = int(inner * 1.3)
    draw.ellipse([cx - jewel_r, cy - jewel_r, cx + jewel_r, cy + jewel_r], fill=GOLD_BRIGHT)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 30, 12))

def main():
    REPO_OUT.parent.mkdir(parents=True, exist_ok=True)
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    # Compass star — upper third, centered
    star_cx = W // 2
    star_cy = 195
    star_r = 78
    draw_compass_star(draw, star_cx, star_cy, star_r, GOLD)

    # Wordmark — "Ancient Atlas"
    wordmark_font = find_font(FONTS_BOLD, 96)
    wm_text = "Ancient Atlas"
    bbox = draw.textbbox((0, 0), wm_text, font=wordmark_font)
    wm_w = bbox[2] - bbox[0]
    draw.text(((W - wm_w) // 2, 320), wm_text, font=wordmark_font, fill=CREAM)

    # Subtitle — "Editions" in italic
    sub_font = find_font(FONTS_ITALIC, 56)
    sub_text = "Editions"
    bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = bbox[2] - bbox[0]
    draw.text(((W - sub_w) // 2, 430), sub_text, font=sub_font, fill=GOLD)

    # Hairline separator above tagline
    line_w = 120
    line_y = 510
    draw.line(
        [((W - line_w) // 2, line_y), ((W + line_w) // 2, line_y)],
        fill=GOLD, width=1
    )

    # Tagline — small italic at the bottom
    tag_font = find_font(FONTS_ITALIC, 24)
    tag_text = "Curated goods for the deep past"
    bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = bbox[2] - bbox[0]
    draw.text(((W - tag_w) // 2, 535), tag_text, font=tag_font, fill=DIM)

    # URL marker bottom-right (corner of the canvas)
    url_font = find_font(FONTS_REGULAR, 18)
    url_text = "theancientatlas.com"
    bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_w = bbox[2] - bbox[0]
    draw.text((W - url_w - 32, H - 38), url_text, font=url_font, fill=DIM)

    img.save(REPO_OUT, optimize=True)
    print(f"✓ Saved to repo: {REPO_OUT}")

    try:
        ICLOUD_OUT.parent.mkdir(parents=True, exist_ok=True)
        img.save(ICLOUD_OUT, optimize=True)
        print(f"✓ Saved to iCloud: {ICLOUD_OUT}")
    except Exception as e:
        print(f"  · Skipped iCloud save: {e}")

    print(f"\n  Upload at: Fourthwall → Settings → General → Social sharing image")

if __name__ == "__main__":
    main()
