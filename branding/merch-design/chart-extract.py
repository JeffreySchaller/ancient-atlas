#!/usr/bin/env python3
"""
chart-extract.py — turn a Gemini fair-isle render into a canonical
stitch chart.

Pipeline position: Gemini supplies the motif (silhouette, composition);
this tool imposes the discipline Gemini can't hold: exact stitch grid,
flat 4-color palette, per-row color audit, seamless repeat extraction.

Usage:
    python3 chart-extract.py INPUT.png [--cols N] [--out PREFIX]

If --cols is omitted, the stitch pitch is estimated by scoring candidate
column counts (40..120) on within-cell color variance (true pitch
minimizes it). Outputs:
    PREFIX_chart.png    clean chart, 20px/stitch, thin grid lines
    PREFIX_tiled.png    3x horizontal tile preview (seam check)
    PREFIX_report.txt   rows with >2 palette colors (fair-isle audit),
                        detected grid, palette usage counts
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

PALETTE = {
    "obsidian":  (13, 13, 18),
    "champagne": (201, 168, 76),
    "amber":     (232, 185, 96),
    "ivory":     (240, 238, 233),
    # extra anchors so dark-gold / brown accents snap somewhere sane:
    "champagne_dk": (143, 116, 48),
}
# colors allowed in the final chart (champagne_dk folds into champagne)
FOLD = {"champagne_dk": "champagne"}
FINAL = ["obsidian", "champagne", "amber", "ivory"]

def quantize(img, cols):
    w, h = img.size
    pitch = w / cols
    rows = round(h / pitch)
    small = img.resize((cols, rows), Image.BOX)
    a = np.asarray(small.convert("RGB"), dtype=float)
    names = list(PALETTE)
    pal = np.array([PALETTE[n] for n in names], dtype=float)
    d = ((a[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1)
    grid = np.vectorize(lambda i: FOLD.get(names[i], names[i]))(idx)
    return grid, rows

def pitch_score(img, cols):
    """Lower = cells are internally flatter = better pitch guess."""
    w, h = img.size
    pitch = w / cols
    rows = int(round(h / pitch))
    a = np.asarray(img.convert("L"), dtype=float)
    small = np.asarray(img.resize((cols, rows), Image.BOX).convert("L"), float)
    up = np.asarray(Image.fromarray(small.astype(np.uint8)).resize(
        img.size, Image.NEAREST), float)
    hh = min(a.shape[0], up.shape[0])
    ww = min(a.shape[1], up.shape[1])
    return float(np.mean((a[:hh, :ww] - up[:hh, :ww]) ** 2))

def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    src = Path(args[0])
    cols = None
    prefix = src.with_suffix("")
    if "--cols" in args:
        cols = int(args[args.index("--cols") + 1])
    if "--out" in args:
        prefix = Path(args[args.index("--out") + 1])
    img = Image.open(src)

    if cols is None:
        cands = {c: pitch_score(img, c) for c in range(40, 121, 2)}
        cols = min(cands, key=cands.get)
        print(f"estimated columns: {cols}")

    grid, rows = quantize(img, cols)
    print(f"grid: {cols} x {rows}")

    # ---- audit: fair-isle row discipline ----
    report = []
    for r in range(rows):
        used = sorted(set(grid[r]))
        if len(used) > 2:
            counts = {u: int((grid[r] == u).sum()) for u in used}
            report.append(f"row {r:3d}: {len(used)} colors {counts}")
    usage = {n: int((grid == n).sum()) for n in FINAL}

    # ---- render chart ----
    S = 20
    out = Image.new("RGB", (cols * S, rows * S))
    d = ImageDraw.Draw(out)
    for r in range(rows):
        for c in range(cols):
            col = PALETTE[grid[r][c]]
            d.rectangle([c * S, r * S, (c + 1) * S - 1, (r + 1) * S - 1],
                        fill=col)
    for c in range(cols + 1):
        d.line([c * S, 0, c * S, rows * S], fill=(60, 60, 66), width=1)
    for r in range(rows + 1):
        d.line([0, r * S, cols * S, r * S], fill=(60, 60, 66), width=1)
    chart_p = Path(f"{prefix}_chart.png")
    out.save(chart_p)

    tiled = Image.new("RGB", (out.width * 3, out.height))
    for i in range(3):
        tiled.paste(out, (i * out.width, 0))
    tiled_p = Path(f"{prefix}_tiled.png")
    tiled.save(tiled_p)

    rep_p = Path(f"{prefix}_report.txt")
    rep_p.write_text(
        f"source: {src.name}\ngrid: {cols} x {rows}\n"
        f"palette usage: {usage}\n\nrows violating 2-color rule "
        f"({len(report)} of {rows}):\n" + "\n".join(report) + "\n")
    print(f"✓ {chart_p.name}, {tiled_p.name}, {rep_p.name}")
    print(f"rows violating 2-color rule: {len(report)}/{rows}")

if __name__ == "__main__":
    main()
