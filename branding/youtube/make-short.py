#!/usr/bin/env python3
"""
make-short.py — Ancient Atlas Shorts pipeline (vertical 1080x1920).

Produces the house-style Short from any episode master:
  - center crop to 9:16, scaled 1080x1920, 24fps
  - five timed text cards (brand fonts, fade in/out, eof_action=pass —
    REQUIRED: without it, ffmpeg freezes each card's last not-quite-
    transparent frame and ghosts stack over the video)
  - synthesized ambient drone bed under loudness-normalized (-14 LUFS)
    location audio
  - 2.5s obsidian end card (compass + wordmark)

Proven on: Derinkuyu vent shaft Short, Osireion lintel Short
(both ~250 views in their first hours, June 2026).

SETUP in a fresh sandbox (fonts are NOT vendored in the repo):
    mkdir -p ~/fonts && cd ~/fonts && npm init -y \
      && npm install @fontsource/fraunces @fontsource/inter @fontsource/jetbrains-mono
    pip install fonttools brotli --break-system-packages
    python3 - <<'PY'
    from fontTools.ttLib import TTFont
    import glob, os
    os.makedirs(os.path.expanduser('~/fonts/ttf'), exist_ok=True)
    for w in glob.glob(os.path.expanduser('~/fonts/node_modules/@fontsource/*/files/*latin-[4567]00-normal.woff2')):
        f = TTFont(w); f.flavor=None
        f.save(os.path.expanduser('~/fonts/ttf/')+os.path.basename(w).replace('.woff2','.ttf'))
    PY
    export AA_FONT_DIR=~/fonts/ttf

USAGE:
    python3 make-short.py <episode-key>      # one episode
    python3 make-short.py --all              # the whole queue
Output: <key>_short.mp4 next to this script + copied to ~/Downloads if
the path in OUT_COPY exists.

EPISODE QUEUE (June 2026 season; windows chosen from contact sheets —
re-verify with a frame sheet if the cut feels off):
    osiris    SSD Osiris Shaft master,   window 1380s+40s  (flooded chamber)
    serapeum  SSD Serapeum master,       window 140s+40s   (gallery reveal)
    pyramid   SSD Great Pyramid master,  window 335s+40s   (Grand Gallery)
    step      SSD Step Pyramid master,   window 1750s+40s  (vault blocks)
    aswan     SSD Aswan Obelisk master,  window 388s+40s   (scoop channel)
    gem       SSD GEM master,            window 38s+40s    (statue hall)
    vases     SSD Diorite Vases master,  window 48s+40s    (the cases)
    sawmarks  SSD Saw Marks master,      window 100s+40s   (striations)

TODO (Peru season): splice the motion sting natively instead of the
static end card. Canonical asset: endcard_ident_vertical_720x1280.mp4
(this dir; 4.0s, 24fps, NO audio track: extend the drone bed under
it). Scale to 1080x1920, cut footage at 39.9s, sting from its own 0s.
Until then: post-splice via ffmpeg concat, donor cut at 39.98 (see
session notes 2026-06-12; eof_action=pass ghosting fix still applies).
Per-episode "cropx" (0=left, 0.5=center, 1=right) shifts the 9:16 crop
window. Added for pyramidC to keep Ben in frame.
"""
import math
import os
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = Path(os.environ.get("AA_FONT_DIR", os.path.expanduser("~/fonts/ttf")))
HERE = Path(__file__).resolve().parent
SSD = Path(os.environ.get("AA_SSD", "/Volumes/Samsung SSD"))
OUT_COPY = Path(os.path.expanduser("~/Downloads"))

OBSIDIAN = (13, 13, 18)
CHAMPAGNE = (201, 168, 76)
CHAMPAGNE_DK = (143, 116, 48)
AMBER = (232, 185, 96)
IVORY = (240, 238, 233)
W, H = 1080, 1920

# ---------------------------------------------------------------- episodes
# cards: (eyebrow or '', [lines], fontsize, y0) x5 — last card is the question
EPISODES = {
    "osiris": {
        "src": SSD / "2025_Osiris_Shaft_Giza_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 1380, "dur": 40,
        "cards": [
            ("OSIRIS SHAFT · GIZA, EGYPT", ["Three levels beneath", "the Giza plateau"], 62, 1200),
            ("", ["The lowest floor", "is underwater"], 62, 1240),
            ("", ["The granite boxes", "are still down there"], 60, 1240),
            ("", ["Almost nobody films this place"], 56, 1280),
            ("THE QUESTION THAT REMAINS", ["How did the boxes", "get down here?"], 78, 1130),
        ],
    },
    "serapeum": {
        "src": SSD / "2025_Serapeum_of_Saqqara_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 140, "dur": 40,
        "cards": [
            ("SERAPEUM · SAQQARA, EGYPT", ["An underground gallery", "of giant granite boxes"], 58, 1200),
            ("", ["Twenty-four boxes,", "up to 70 tons each"], 62, 1240),
            ("", ["Lids that still seal", "after thousands of years"], 58, 1240),
            ("", ["Officially: bull tombs"], 64, 1280),
            ("THE QUESTION THAT REMAINS", ["What needed a box", "this precise?"], 78, 1130),
        ],
    },
    "pyramidB": {
        # King's Chamber: Jeff asks Yusuf to rake his iPhone light across
        # the granite box — machining marks moment (starts ~14:30)
        "src": SSD / "2025_Great_Pyramid_Giza_Top_to_Bottom_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 866, "dur": 40,
        "cards": [
            ("KING'S CHAMBER · GREAT PYRAMID", ["We asked for", "one flashlight"], 62, 1200),
            ("", ["Raking light across", "the granite box"], 62, 1240),
            ("", ["Striations.", "Smooth, even planes."], 62, 1240),
            ("", ["Not chisel marks.", "No hieroglyphs."], 60, 1280),
            ("THE QUESTION THAT REMAINS", ["What left", "these marks?"], 78, 1130),
        ],
    },
    "pyramidC": {
        # Subterranean chamber: filming down the pit in the floor (~18:57)
        "src": SSD / "2025_Great_Pyramid_Giza_Top_to_Bottom_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 1132, "dur": 40, "cropx": 0.65,  # Ben (UnchartedX) descending, framed in
        "cards": [
            ("SUBTERRANEAN CHAMBER · GIZA", ["Beneath the pyramid,", "cut into bedrock"], 58, 1200),
            ("", ["There's a hole", "in the floor"], 64, 1240),
            ("", ["It keeps going down"], 64, 1240),
            ("", ["No one agrees", "what it was for"], 60, 1280),
            ("THE QUESTION THAT REMAINS", ["How deep does", "Giza go?"], 78, 1130),
        ],
    },
    "pyramid": {
        "src": SSD / "2025_Great_Pyramid_Giza_Top_to_Bottom_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 335, "dur": 40,
        "cards": [
            ("GREAT PYRAMID · GIZA, EGYPT", ["The most-studied", "building on Earth"], 62, 1200),
            ("", ["Granite hauled from", "800 kilometers away"], 60, 1240),
            ("", ["Beams overhead", "weigh up to 70 tons"], 62, 1240),
            ("", ["And it still keeps secrets"], 60, 1280),
            ("THE QUESTION THAT REMAINS", ["Why does the ceiling", "keep going?"], 78, 1130),
        ],
    },
    "step": {
        "src": SSD / "2025_Step_Pyramid_of_Saqqara_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 1750, "dur": 40,
        "cards": [
            ("STEP PYRAMID · SAQQARA, EGYPT", ["The oldest monumental", "stone building in Egypt"], 56, 1200),
            ("", ["5.7 kilometers of tunnels", "run beneath it"], 58, 1240),
            ("", ["A vault sealed with", "a 3.5-ton granite plug"], 58, 1240),
            ("", ["Six steps above ground"], 62, 1280),
            ("THE QUESTION THAT REMAINS", ["Why is the real engineering", "underground?"], 68, 1130),
        ],
    },
    "aswanB": {
        # Ray demonstrates sideways pounding with a dolerite stone (~9:36).
        # NOTE: source here is the 720p published edit, not the 4K master —
        # re-cut from SSD master for final if this test performs.
        "src": SSD / "Unfinished Obelisk of Aswan with UnchartedX _ Fieldwork · Egypt.mp4",
        "start": 578, "dur": 40, "cropx": 0.5,
        "cards": [
            ("ASWAN QUARRY · EGYPT", ["How do you carve", "a 1,000-ton obelisk?"], 56, 1200),
            ("", ["Our friend Ray", "shows one way"], 60, 1240),
            ("", ["A dolerite stone,", "pounded sideways"], 58, 1240),
            ("", ["Harder than the granite", "it shapes"], 56, 1280),
            ("THE QUESTION THAT REMAINS", ["Is this how", "they did it?"], 78, 1130),
        ],
    },
    "aswan": {
        "src": SSD / "2025_Aswan_Quarry_Unfinished_Obelisk_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 388, "dur": 40,
        "cards": [
            ("ASWAN QUARRY · EGYPT", ["A 1,000-ton obelisk,", "still attached to the bedrock"], 56, 1200),
            ("", ["Abandoned mid-extraction", "when cracks appeared"], 58, 1240),
            ("", ["The scoop marks", "are still crisp"], 62, 1240),
            ("", ["In granite"], 70, 1280),
            ("THE QUESTION THAT REMAINS", ["What made", "these marks?"], 82, 1130),
        ],
    },
    "gem": {
        "src": SSD / "2025_Grand_Egyptian_Museum_Cairo_Walkthrough_UnchartedX_Team_Unedited_4K_HEVC.m4v",
        "start": 38, "dur": 40,
        "cards": [
            ("GRAND EGYPTIAN MUSEUM · CAIRO", ["The largest archaeological", "museum on Earth"], 56, 1200),
            ("", ["Colossal statuary", "under one roof"], 62, 1240),
            ("", ["And the hard-stone artifacts", "the labels summarize"], 54, 1240),
            ("", ["We went case by case"], 62, 1280),
            ("THE QUESTION THAT REMAINS", ["What deserves", "a second look?"], 78, 1130),
        ],
    },
    "vases": {
        "src": SSD / "2025_Egyptian_Museum_Cairo_Granite_Diorite_Vases_UnchartedX_Unedited_4K_HEVC.m4v",
        "start": 48, "dur": 40,
        "cards": [
            ("EGYPTIAN MUSEUM · CAIRO", ["Stone vessels", "older than the pyramids"], 60, 1200),
            ("", ["Turned from diorite:", "harder than the tools of the time"], 52, 1240),
            ("", ["Wall symmetry we'd reach", "for a lathe to match"], 54, 1240),
            ("", ["Thousands of them exist"], 60, 1280),
            ("THE QUESTION THAT REMAINS", ["How do you turn stone", "you can't scratch?"], 68, 1130),
        ],
    },
    "sawmarks": {
        "src": SSD / "2025_Cairo_Museum_Granite_Sarcophagus_Saw_Marks_UnchartedX_HEVC_4K.m4v",
        "start": 100, "dur": 40,
        "cards": [
            ("EGYPTIAN MUSEUM · CAIRO", ["Saw planes on", "a granite sarcophagus"], 60, 1200),
            ("", ["The striations are regular.", "The cut is flat."], 56, 1240),
            ("", ["The official toolkit:", "copper and sand"], 60, 1240),
            ("", ["Look closely"], 70, 1280),
            ("THE QUESTION THAT REMAINS", ["Copper and sand...", "or something else?"], 70, 1130),
        ],
    },
}

# card schedule within the clip (start, visible duration) — 5 slots
SLOTS = [(1.0, 5.0), (8.0, 6.0), (16.0, 6.5), (25.5, 6.0), (33.5, 5.5)]

def F(n, s):
    return ImageFont.truetype(str(FONT_DIR / n), s)

def make_card(path, eyebrow, lines, big, y0):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    y = y0
    if eyebrow:
        f = F("jetbrains-mono-latin-500-normal.ttf", 30)
        total = sum(d.textlength(c, font=f) for c in eyebrow) + 10 * (len(eyebrow) - 1)
        x = (W - total) / 2
        for c in eyebrow:
            sd.text((x + 2, y + 3), c, font=f, fill=(0, 0, 0, 200))
            d.text((x, y), c, font=f, fill=(*AMBER, 255))
            x += d.textlength(c, font=f) + 10
        y += 64
    fb = F("fraunces-latin-600-normal.ttf", big)
    for ln in lines:
        wln = d.textlength(ln, font=fb)
        sd.text(((W - wln) / 2 + 3, y + 4), ln, font=fb, fill=(0, 0, 0, 210))
        d.text(((W - wln) / 2, y), ln, font=fb, fill=(*IVORY, 255))
        y += big + 16
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    Image.alpha_composite(sh, img).save(path)

def make_endcard(path):
    img = Image.new("RGB", (W, H), OBSIDIAN)
    d = ImageDraw.Draw(img)
    def compass(cx, cy, R):
        def pt(ang, L, hw, li, dk):
            ang = math.radians(ang)
            tip = (cx + L * math.sin(ang), cy - L * math.cos(ang))
            p = ang + math.pi / 2
            l = (cx + hw * math.sin(p), cy - hw * math.cos(p))
            rr = (cx - hw * math.sin(p), cy + hw * math.cos(p))
            d.polygon([tip, l, (cx, cy)], fill=li)
            d.polygon([tip, rr, (cx, cy)], fill=dk)
        for ang in (45, 135, 225, 315):
            pt(ang, R * .52, R * .075, CHAMPAGNE, CHAMPAGNE_DK)
        for ang in (0, 90, 180, 270):
            pt(ang, R * .97, R * .10, AMBER, CHAMPAGNE_DK)
        hub = R * .075
        d.ellipse([cx - hub, cy - hub, cx + hub, cy + hub], fill=OBSIDIAN,
                  outline=CHAMPAGNE, width=4)
    compass(W / 2, 760, 120)
    fb = F("fraunces-latin-700-normal.ttf", 96)
    d.text(((W - d.textlength("THE ANCIENT", font=fb)) / 2, 940), "THE ANCIENT", font=fb, fill=IVORY)
    d.text(((W - d.textlength("ATLAS", font=fb)) / 2, 1060), "ATLAS", font=fb, fill=IVORY)
    d.line([W / 2 - 360, 1230, W / 2 + 360, 1230], fill=CHAMPAGNE_DK, width=4)
    def tracked(y, t, f, fill, tr):
        total = sum(d.textlength(c, font=f) for c in t) + tr * (len(t) - 1)
        x = (W - total) / 2
        for c in t:
            d.text((x, y), c, font=f, fill=fill)
            x += d.textlength(c, font=f) + tr
    tracked(1266, "A MAP OF THE DEEP PAST", F("jetbrains-mono-latin-500-normal.ttf", 34), CHAMPAGNE, 10)
    tracked(1360, "FULL WALKTHROUGH ON THE CHANNEL", F("jetbrains-mono-latin-400-normal.ttf", 26), (180, 174, 160), 6)
    img.save(path)

def make_drone(path, T):
    sr = 44100
    t = np.linspace(0, T, int(sr * T), endpoint=False)
    def tone(f, a, lfo=0.05, ph=0):
        return a * (0.6 + 0.4 * np.sin(2 * np.pi * lfo * t + ph)) * np.sin(2 * np.pi * f * t)
    sig = tone(55, .30) + tone(110, .18, .07, 1.3) + tone(164.81, .10, .04, 2.1) + tone(220, .06, .09, .5)
    sig += np.convolve(np.random.randn(len(t)) * 0.012, np.ones(400) / 400, mode="same")
    env = np.minimum(1, np.minimum(t / 3.0, np.maximum(0, (T - t) / 3.5)))
    sig = np.clip(sig * env * 0.5, -1, 1)
    stereo = np.stack([sig, sig * 0.97]).T
    with wave.open(str(path), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())

def build(key):
    ep = EPISODES[key]
    src = str(ep["src"])
    dur = ep["dur"]; total = dur + 2.5
    tmp = Path("/tmp")
    # probe source size for crop math
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", src],
                       capture_output=True, text=True, timeout=60)
    sw, sh_ = map(int, r.stdout.strip().split(","))
    cw = round(sh_ * 9 / 16)
    cards = []
    for i, (eyebrow, lines, big, y0) in enumerate(ep["cards"]):
        p = tmp / f"sc_{key}_{i}.png"
        make_card(p, eyebrow, lines, big, y0)
        cards.append(p)
    endcard = tmp / "sc_endcard.png"
    make_endcard(endcard)
    drone = tmp / "sc_drone.wav"
    make_drone(drone, total)

    inputs = ["-ss", str(ep["start"]), "-t", str(dur), "-i", src,
              "-loop", "1", "-t", "2.5", "-i", str(endcard)]
    cropx = ep.get("cropx", 0.5)   # 0=left edge, 0.5=center, 1=right edge
    fc = [f"[0:v]crop={cw}:{sh_}:(iw-{cw})*{cropx}:0,scale=1080:1920,setsar=1,fps=24[base]"]
    for i, (st, vis) in enumerate(SLOTS):
        inputs += ["-loop", "1", "-t", str(vis + 0.6), "-i", str(cards[i])]
        idx = 2 + i
        fc.append(f"[{idx}:v]format=yuva420p,fade=t=in:st=0:d=0.6:alpha=1,"
                  f"fade=t=out:st={vis - 0.6:.1f}:d=0.6:alpha=1,setpts=PTS+{st}/TB[t{i}]")
    chain = "base"
    for i in range(5):
        nxt = f"v{i+1}"
        fc.append(f"[{chain}][t{i}]overlay=0:0:eof_action=pass[{nxt}]")
        chain = nxt
    fc.append("[1:v]scale=1080:1920,setsar=1,fps=24[vend]")
    fc.append(f"[{chain}][vend]concat=n=2:v=1:a=0[v]")
    fc.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[voice]")
    fc.append(f"[{2+len(SLOTS)}:a]volume=0.55[mus]")
    inputs += ["-i", str(drone)]
    fc.append(f"[voice][mus]amix=inputs=2:duration=first:weights=1 0.6,"
              f"afade=t=out:st={dur - 2}:d=2,apad=whole_dur={total}[a]")
    out = HERE / f"{key}_short.mp4"
    cmd = ["ffmpeg", "-v", "error"] + inputs + ["-filter_complex", ";".join(fc),
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
           "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-y", str(out)]
    subprocess.run(cmd, check=True)
    if OUT_COPY.exists():
        import shutil
        shutil.copy2(out, OUT_COPY / f"AncientAtlas_{key}_short.mp4")
    print(f"✓ {key}: {out.name}")

if __name__ == "__main__":
    keys = list(EPISODES) if "--all" in sys.argv else [a for a in sys.argv[1:] if a in EPISODES]
    if not keys:
        sys.exit(f"usage: make-short.py [--all | {' | '.join(EPISODES)}]")
    for k in keys:
        build(k)
