#!/usr/bin/env python3
"""
assemble-ident.py — Ancient Atlas channel ident from the four Utopai clips.

Sequence (per the approved treatment):
    clip_megalithic_wall  2.6s   →xfade 0.4s→
    clip_weathered_pyramid 2.2s  →xfade 0.4s→
    clip_carved_tunnel    2.2s   →xfade 0.4s→
    clip_obsidian_void    3.6s   (wordmark composited over it)
Total ≈ 9.4s. Output 1920x1080 24fps H.264 + synthesized audio bed
(low drone + one soft chime when the title lands). No AI text anywhere:
the compass + THE ANCIENT ATLAS + tagline are PIL-rendered brand tokens.

Fonts: same setup as make-short.py (AA_FONT_DIR). Clips are read from
~/Downloads/ident-clips/ (override with AA_IDENT_DIR). Trims are taken
from the MIDDLE of each clip; if a chosen stretch looks wrong, adjust
TRIMS below.

Run:  python3 branding/youtube/assemble-ident.py
Out:  ~/Downloads/AncientAtlas_ident_v1.mp4
"""
import math
import os
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path(os.environ.get("AA_FONT_DIR", os.path.expanduser("~/fonts/ttf")))
CLIP_DIR = Path(os.environ.get("AA_IDENT_DIR", os.path.expanduser("~/Downloads/ident-clips")))
OUT = Path(os.path.expanduser("~/Downloads/AncientAtlas_ident_v1.mp4"))

OBSIDIAN = (13, 13, 18)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_DK = (143, 116, 48)
AMBER = (232, 185, 96)
IVORY = (240, 238, 233)
W, H = 1920, 1080
XF = 0.4

# (filename, trim seconds)
TRIMS = [
    ("clip_megalithic_wall.mp4", 2.6),
    ("clip_weathered_pyramid.mp4", 2.2),
    ("clip_carved_tunnel.mp4", 2.2),
    ("clip_obsidian_void.mp4", 3.6),
]

def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, timeout=60)
    return float(r.stdout.strip())

def F(n, s):
    return ImageFont.truetype(str(FONT_DIR / n), s)

def make_title(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    def compass(cx, cy, R):
        def pt(ang, L, hw, li, dk):
            ang = math.radians(ang)
            tip = (cx + L * math.sin(ang), cy - L * math.cos(ang))
            p = ang + math.pi / 2
            l = (cx + hw * math.sin(p), cy - hw * math.cos(p))
            rr = (cx - hw * math.sin(p), cy + hw * math.cos(p))
            d.polygon([tip, l, (cx, cy)], fill=(*li, 255))
            d.polygon([tip, rr, (cx, cy)], fill=(*dk, 255))
        for ang in (45, 135, 225, 315):
            pt(ang, R * .52, R * .075, CHAMPAGNE, CHAMPAGNE_DK)
        for ang in (0, 90, 180, 270):
            pt(ang, R * .97, R * .10, AMBER, CHAMPAGNE_DK)
        hub = R * .075
        d.ellipse([cx - hub, cy - hub, cx + hub, cy + hub],
                  fill=(*OBSIDIAN, 255), outline=(*CHAMPAGNE, 255), width=3)
    compass(W / 2, 330, 95)
    fb = F("fraunces-latin-700-normal.ttf", 120)
    t = "THE ANCIENT ATLAS"
    d.text(((W - d.textlength(t, font=fb)) / 2, 460), t, font=fb, fill=(*IVORY, 255))
    d.line([W / 2 - 430, 640, W / 2 + 430, 640], fill=(*CHAMPAGNE_DK, 255), width=4)
    f2 = F("jetbrains-mono-latin-500-normal.ttf", 36)
    t2 = "A MAP OF THE DEEP PAST"
    total = sum(d.textlength(c, font=f2) for c in t2) + 12 * (len(t2) - 1)
    x = (W - total) / 2
    for c in t2:
        d.text((x, 678), c, font=f2, fill=(*CHAMPAGNE, 255))
        x += d.textlength(c, font=f2) + 12
    img.save(path)

def make_audio(path, T, chime_at):
    sr = 44100
    t = np.linspace(0, T, int(sr * T), endpoint=False)
    def tone(f, a, lfo=0.05, ph=0):
        return a * (0.6 + 0.4 * np.sin(2 * np.pi * lfo * t + ph)) * np.sin(2 * np.pi * f * t)
    sig = tone(55, .26) + tone(110, .15, .07, 1.3) + tone(164.81, .08, .04, 2.1)
    sig += np.convolve(np.random.randn(len(t)) * 0.010, np.ones(400) / 400, mode="same")
    # one soft chime (A5 + harmonic, exponential decay) when the title lands
    ct = t - chime_at
    chime = np.where(ct > 0, np.exp(-ct * 2.2), 0) * (
        0.16 * np.sin(2 * np.pi * 880 * t) + 0.07 * np.sin(2 * np.pi * 1760 * t))
    sig = sig + chime
    env = np.minimum(1, np.minimum(t / 1.5, np.maximum(0, (T - t) / 1.8)))
    sig = np.clip(sig * env * 0.55, -1, 1)
    stereo = np.stack([sig, sig * 0.97]).T
    with wave.open(str(path), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())

def main():
    clips = []
    for name, trim in TRIMS:
        p = CLIP_DIR / name
        if not p.exists():
            raise SystemExit(f"missing clip: {p}")
        full = probe_dur(p)
        start = max(0, (full - trim) / 2)   # middle of the clip
        clips.append((p, start, trim))

    durs = [c[2] for c in clips]
    offs = []
    acc = 0.0
    for dur in durs[:-1]:
        acc += dur - XF
        offs.append(round(acc, 3))
    total = acc + durs[-1]
    title_in = offs[-1] + 0.8           # 0.8s into the void
    title_png = Path("/tmp/ident_title.png")
    make_title(title_png)
    audio = Path("/tmp/ident_audio.wav")
    make_audio(audio, total, title_in + 0.4)

    inputs = []
    for p, start, trim in clips:
        inputs += ["-ss", str(start), "-t", str(trim), "-i", str(p)]
    title_dur = total - title_in
    inputs += ["-loop", "1", "-t", str(title_dur), "-i", str(title_png),
               "-i", str(audio)]

    fc = []
    for i in range(4):
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},setsar=1,fps=24[c{i}]")
    fc.append(f"[c0][c1]xfade=transition=fade:duration={XF}:offset={offs[0]}[x1]")
    fc.append(f"[x1][c2]xfade=transition=fade:duration={XF}:offset={offs[1]}[x2]")
    fc.append(f"[x2][c3]xfade=transition=fade:duration={XF}:offset={offs[2]}[plate]")
    fc.append(f"[4:v]format=yuva420p,fade=t=in:st=0:d=0.8:alpha=1,"
              f"setpts=PTS+{title_in}/TB[title]")
    fc.append("[plate][title]overlay=0:0:eof_action=pass[v]")

    cmd = (["ffmpeg", "-v", "error"] + inputs +
           ["-filter_complex", ";".join(fc),
            "-map", "[v]", "-map", "5:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-y", str(OUT)])
    subprocess.run(cmd, check=True)
    print(f"✓ ident: {OUT} ({total:.1f}s)")

if __name__ == "__main__":
    main()
