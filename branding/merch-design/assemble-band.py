#!/usr/bin/env python3
"""
assemble-band.py — canonical Capsule I band from an extracted chart.

Takes the chart-extract output (20px cells + gridlines), recovers the
stitch grid, isolates the animal rows, finds the true horizontal
repeat by autocorrelation, then frames the animal band with
deterministic peerie borders (compass stars above, strata zigzag
below) generated in code — clean, symmetric, seamlessly tiling.

Usage:
    python3 assemble-band.py /tmp/mammoth_chart.png --out PREFIX
Outputs: PREFIX_band.png (one repeat, 20px cells),
         PREFIX_band_tiled.png (4x tile, no gridlines, print look)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

PAL = {
    "obsidian": (13, 13, 18), "champagne": (201, 168, 76),
    "amber": (232, 185, 96), "ivory": (240, 238, 233),
}
NAMES = list(PAL)
S = 20  # px per stitch in chart-extract output

def load_grid(p):
    im = np.asarray(Image.open(p).convert("RGB"), dtype=float)
    rows, cols = im.shape[0] // S, im.shape[1] // S
    g = np.zeros((rows, cols), dtype=int)
    pal = np.array([PAL[n] for n in NAMES], dtype=float)
    for r in range(rows):
        for c in range(cols):
            cell = im[r*S+4:(r+1)*S-4, c*S+4:(c+1)*S-4].reshape(-1, 3)
            med = np.median(cell, axis=0)
            g[r, c] = ((pal - med) ** 2).sum(1).argmin()
    return g

def animal_rows(g):
    champ = NAMES.index("champagne")
    frac = (g == champ).mean(1)
    # the animal band = the widest contiguous run of rows that are
    # mostly ground+motif (low champagne in borders is dense/regular;
    # animal rows have champagne fraction that varies smoothly)
    core = frac > 0.06
    runs, start = [], None
    for i, v in enumerate(core):
        if v and start is None: start = i
        if not v and start is not None: runs.append((start, i)); start = None
    if start is not None: runs.append((start, len(core)))
    a, b = max(runs, key=lambda t: t[1] - t[0])
    return max(0, a - 2), min(g.shape[0], b + 2)   # breathing room

def find_period(band, lo=30, hi=50):
    best, bestp = None, None
    for p in range(lo, hi + 1):
        m = np.mean([
            (band[:, :-p] != band[:, p:]).mean()
        ])
        if best is None or m < best:
            best, bestp = m, p
    return bestp, best

# ---- deterministic peeries ----
def compass_peerie(width, period=14):
    """9 rows: 8-point star every `period` stitches, dot between."""
    h = 9
    g = np.zeros((h, width), dtype=int)
    champ, amber = NAMES.index("champagne"), NAMES.index("amber")
    for cx in range(period // 2, width, period):
        cy = 4
        for d in range(-4, 5):           # cardinals
            if 0 <= cx + d < width:
                g[cy, cx + d] = champ
            if 0 <= cy + d < h:
                g[cy + d, cx] = champ
        for d in range(-2, 3):           # diagonals
            if 0 <= cx + d < width and 0 <= cy + d < h:
                g[cy + d, cx + d] = champ
                g[cy - d, cx + d] = champ
        g[cy, cx] = amber
        dx = cx + period // 2
        if dx < width:
            g[cy, dx] = amber            # lone dot between stars
    return g

def strata_peerie(width, period=10, amp=3):
    """7 rows: zigzag strata line, amber dot in each valley."""
    h = 7
    g = np.zeros((h, width), dtype=int)
    champ, amber = NAMES.index("champagne"), NAMES.index("amber")
    for c in range(width):
        t = c % period
        y = amp - t if t <= amp else t - amp
        y = min(h - 2, 1 + y)
        g[y, c] = champ
        if t == amp:                     # valley bottom
            if y + 2 < h:
                g[y + 2, c] = amber
    return g

def solid_row(width, name="champagne"):
    return np.full((1, width), NAMES.index(name), dtype=int)

def spacer(width, n=2):
    return np.zeros((n, width), dtype=int)

def render(g, path, grid_lines=True, scale=S):
    rows, cols = g.shape
    out = Image.new("RGB", (cols * scale, rows * scale))
    d = ImageDraw.Draw(out)
    for r in range(rows):
        for c in range(cols):
            d.rectangle([c*scale, r*scale, (c+1)*scale-1, (r+1)*scale-1],
                        fill=PAL[NAMES[g[r, c]]])
    if grid_lines:
        for c in range(cols + 1):
            d.line([c*scale, 0, c*scale, rows*scale], fill=(60, 60, 66))
        for r in range(rows + 1):
            d.line([0, r*scale, cols*scale, r*scale], fill=(60, 60, 66))
    out.save(path)
    return out

def main():
    src = Path(sys.argv[1])
    prefix = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else str(src.with_suffix("")) + "_asm"
    g = load_grid(src)
    if "--rows" in sys.argv:
        a, b = map(int, sys.argv[sys.argv.index("--rows") + 1].split(":"))
    else:
        a, b = animal_rows(g)
    band = g[a:b]
    p, err = find_period(band)
    print(f"grid {g.shape}, animal rows {a}..{b}, period {p} (mismatch {err:.3f})")
    # cut one repeat starting in the emptiest gap between animals so the
    # seam never bisects a motif: score each start by motif density in
    # the 3 columns on each side of the seam
    density = (band != 0).mean(0)
    def seam_cost(s):
        cols = [(s + d) % band.shape[1] for d in (-2, -1, 0)] + \
               [(s + p + d) % band.shape[1] for d in (-1, 0, 1)]
        return sum(density[c] for c in cols)
    s0 = min(range(band.shape[1] - p), key=seam_cost)
    repeat = band[:, s0:s0 + p].copy()
    # drop stray fragments: connected components < 5 cells
    from scipy import ndimage
    lab, n = ndimage.label(repeat != 0)
    for i in range(1, n + 1):
        if (lab == i).sum() < 12:
            repeat[lab == i] = 0
    W = p * 3  # show 3 repeats in the canonical band file
    animal3 = np.tile(repeat, (1, 3))
    stack = np.vstack([
        solid_row(W), spacer(W), compass_peerie(W), spacer(W), solid_row(W),
        spacer(W, 3), animal3, spacer(W, 3),
        solid_row(W), spacer(W), strata_peerie(W), spacer(W), solid_row(W),
    ])
    render(stack, f"{prefix}_band.png", grid_lines=True)
    flat = render(stack, f"{prefix}_band_flat.png", grid_lines=False, scale=12)
    tiled = Image.new("RGB", (flat.width * 2, flat.height))
    tiled.paste(flat, (0, 0)); tiled.paste(flat, (flat.width, 0))
    tiled.save(f"{prefix}_band_tiled.png")
    print(f"✓ {prefix}_band.png / _band_flat.png / _band_tiled.png")

if __name__ == "__main__":
    main()
