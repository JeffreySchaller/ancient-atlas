#!/usr/bin/env python3
"""
render.py — Feel the Weight OG share cards, 1200x630, with the 2026 logo lockup.

Rebuild of the Aug 6 card rig. Layout, palette and copy are preserved from the
shipped cards; the only change is the brand row, which now leads with the
compass-star medallion at 74px, the wordmark in gold, and "Feel the Weight"
stepped back to grey.

Fonts (Fraunces variable + JetBrains Mono) and the logo are inlined as base64
so the render is hermetic and needs no network.
"""
import asyncio
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


import base64

FONTS = {
    "fraunces": "node_modules/@fontsource-variable/fraunces/files/fraunces-latin-full-normal.woff2",
    "frauncesi": "node_modules/@fontsource-variable/fraunces/files/fraunces-latin-full-italic.woff2",
    "jbm400": "node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2",
    "jbm500": "node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2",
}


def b64(rel):
    path = HERE / rel
    if not path.exists():
        sys.exit(
            f"missing asset: {path}\n"
            "Run once inside scripts/og-cards/ :\n"
            "  npm install @fontsource-variable/fraunces @fontsource/jetbrains-mono"
        )
    return base64.b64encode(path.read_bytes()).decode()


LOGO = b64("logo.png")
FRAUNCES = b64(FONTS["fraunces"])
FRAUNCES_I = b64(FONTS["frauncesi"])
JBM400 = b64(FONTS["jbm400"])
JBM500 = b64(FONTS["jbm500"])

# ------------------------------------------------------------------ palette
GOLD = "#E8B84B"
CREAM = "#F5E1A9"
BODY = "#EDE6DA"
MUTED = "#8A8378"
DIM = "#6E675C"
ROSE = "#C4726A"

# ------------------------------------------------------------------ content
# The old set led with "You cannot lift it" over a stat row that ended in
# "YOU MOVE IT / 0 in". That was the push mechanic, which the page no longer
# has, and it sold a dead end: the reader arrives having already been told the
# answer is no. The cards now offer the three things the page actually lets
# you do, and every stone leads with its own simile, one word of it in italic
# champagne, exactly as the page sets it.

# ---------------------------------------------------------------- content
# The previous set was a paragraph, a stat row and a headline that wrapped to
# two lines. At the size a share card is actually seen, that is a grey block.
#
# Each card is now one short line and two drawings: the stone at true
# proportions with a person beside it, and the whole weight as a field of
# pickups. Nothing is implied or truncated - if a stone is 259 trucks, the card
# draws 259 trucks and picks a size that fits them.

HUMAN_M = 1.8288
F150_LB = 2.2 * 2204.62

CARDS = [
    {"file": "og.png",       "where": "SIX STONES \u00b7 GIZA TO BAALBEK",
     "line": "Stand next to it.",       "dim": [13.6, 3.5, 3.3], "lb": 1256850},
    {"file": "og-giza.png",  "where": "GIZA BLOCK \u00b7 EGYPT",
     "line": "And then two million more.", "dim": [1.3, 1.15, 1.5], "lb": 5000},
    {"file": "og-ollan.png", "where": "OLLANTAYTAMBO \u00b7 PERU",
     "line": "Carried up a mountain.",  "dim": [1.7, 4.0, 0.9], "lb": 110250},
    {"file": "og-temple.png", "where": "THE WESTERN STONE \u00b7 JERUSALEM",
     "line": "Longer than a bus.",      "dim": [13.6, 3.5, 3.3], "lb": 1256850},
    {"file": "og-trilithon.png", "where": "THE TRILITHON \u00b7 BAALBEK",
     "line": "Three of these, in a row.", "dim": [19.0, 4.2, 3.6], "lb": 1764000},
    {"file": "og-pregnant.png", "where": "THE PREGNANT WOMAN \u00b7 BAALBEK",
     "line": "Left where it was cut.",  "dim": [20.5, 4.3, 4.7], "lb": 2205000},
    {"file": "og-forgotten.png", "where": "THE FORGOTTEN STONE \u00b7 BAALBEK",
     "line": "Still in the ground.",    "dim": [19.6, 5.5, 6.0], "lb": 3307500},
]

# the F-150 the experience itself draws, so the card and the page agree
TRUCK = ("M1.6 6L23.5 6L24.6 1.8L37.6 1.8L40.4 5.8L57 5.8L58.2 6.6L58.2 14.6"
         "L50 14.6A4.4 3 0 0 0 41.2 14.6L17.4 14.6A4.4 3 0 0 0 8.6 14.6L1.6 14.6Z"
         "M3.6 7.4L21.7 7.4L21.7 10.8L3.6 10.8Z"
         "M26.6 3.4L32.8 3.4L32.8 6.8L26.6 6.8Z"
         "M34 3.4L36.2 3.4L38 7L34 7Z"
         "M9.7 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0"
         "M11.65 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0"
         "M42.3 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0"
         "M44.25 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0")

FIGURE = (
    "M0 1.4a7.4 7.4 0 1 1-.1 0Z"
    "M-3.6 17h7.2c5.1 0 9.2 3.5 9.8 8.6l2.2 20.4c.3 2.7-1.2 4.5-3.5 4.7"
    "-2.2.2-4.1-1.4-4.4-4.1l-1.5-12.3-.8 20.5h-1.3l-2.4 45.9h-4.7l-1.6-34.6"
    "-1.6 34.6h-4.7l-2.4-45.9h-1.3l-.8-20.5-1.5 12.3c-.3 2.7-2.2 4.3-4.4 4.1"
    "-2.3-.2-3.8-2-3.5-4.7l2.2-20.4c.6-5.1 4.7-8.6 9.8-8.6Z")


def stone_svg(dim, box_w=500, box_h=252):
    """The block at true proportions with a six-foot figure beside it."""
    length, height, depth = dim
    tall = max(height, HUMAN_M)
    scale = min(box_w * 0.80 / (length + 1.7), box_h * 0.86 / tall)
    L, H = length * scale, height * scale
    D = min(depth * scale * 0.42, H * 0.55)          # foreshortened top face
    fig_h = HUMAN_M * scale
    ground = box_h - 8
    x0, y0 = 4, ground - H
    fx = x0 + L + max(20, scale * 0.9)
    return (
      '<svg class="draw" viewBox="0 0 %d %d">' % (box_w, box_h) +
      '<line class="gnd" x1="0" y1="%.1f" x2="%d" y2="%.1f"/>' % (ground, box_w, ground) +
      '<path class="face" d="M%.1f %.1f h%.1f v%.1f h-%.1f Z"/>' % (x0, y0, L, H, L) +
      '<path class="top" d="M%.1f %.1f l%.1f -%.1f h%.1f l-%.1f %.1f Z"/>'
        % (x0, y0, D * 0.85, D, L, D * 0.85, D) +
      '<g class="fig" transform="translate(%.1f %.1f) scale(%.4f)">' % (fx, ground - fig_h, fig_h / 100.0) +
      '<path d="%s"/></g>' % FIGURE +
      '</svg>')


def truck_field(n, box_w=580, box_h=250, gap=4):
    """Every truck, at whatever size makes every truck fit."""
    best = None
    for w in range(236, 5, -1):
        h = w / 3.0
        cols = max(1, int((box_w + gap) // (w + gap)))
        rows = -(-n // cols)
        if rows * (h + gap) - gap <= box_h:
            best = (w, h, cols, rows)
            break
    if best is None:
        sys.exit("ABORT: %d trucks will not fit the field at any size" % n)
    w, h, cols, rows = best
    cells = "".join(
        '<svg class="tk" viewBox="0 0 60 20" fill-rule="evenodd" '
        'style="width:%.2fpx;height:%.2fpx"><path d="%s"/></svg>' % (w, h, TRUCK)
        for _ in range(n))
    return ('<div class="field" style="gap:%dpx;max-width:%dpx">%s</div>'
            % (gap, cols * (w + gap) - gap, cells)), (w, cols, rows)

CSS = f"""
@font-face {{
  font-family: 'Fraunces';
  src: url(data:font/woff2;base64,{FRAUNCES}) format('woff2-variations');
  font-weight: 100 900;
}}
@font-face {{
  font-family: 'Fraunces';
  src: url(data:font/woff2;base64,{FRAUNCES_I}) format('woff2-variations');
  font-weight: 100 900; font-style: italic;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM400}) format('woff2'); font-weight: 400;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM500}) format('woff2'); font-weight: 500;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1200px; height:630px; }}
body {{ background:#080706; padding:9px; -webkit-font-smoothing:antialiased; }}
.frame {{
  width:100%; height:100%;
  border:1px solid rgba(232,184,75,0.30);
  background:
    radial-gradient(1100px 620px at 12% -8%, rgba(196,142,52,0.16) 0%, rgba(196,142,52,0.05) 38%, rgba(0,0,0,0) 72%),
    radial-gradient(700px 420px at 96% 106%, rgba(120,86,32,0.10) 0%, rgba(0,0,0,0) 70%),
    #0d0b09;
  padding:30px 60px 34px 60px;
  display:flex; flex-direction:column;
}}
.brand {{ display:flex; align-items:center; gap:20px; flex:0 0 auto; }}
.brand img {{ width:64px; height:64px; display:block; }}
.brand .words {{
  font-family:'JetBrains Mono',monospace; font-weight:500; font-size:17px;
  letter-spacing:0.26em; white-space:nowrap;
}}
.brand .mark {{ color:{GOLD}; }}
.brand .sep {{ color:rgba(232,184,75,0.45); padding:0 2px; }}
.brand .sub {{ color:{MUTED}; }}

.body {{ flex:1 1 auto; display:flex; align-items:stretch; gap:40px; padding-top:4px; }}
.left {{ width:500px; flex:0 0 auto; display:flex; flex-direction:column;
  justify-content:space-between; padding:6px 0 2px; }}
.line {{
  font-family:'Fraunces',Georgia,serif; font-weight:700;
  font-variation-settings:'opsz' 144,'SOFT' 0,'WONK' 1;
  color:{CREAM}; font-size:60px; line-height:0.98; letter-spacing:-0.018em;
}}
.where {{
  font-family:'JetBrains Mono',monospace; font-size:15px; letter-spacing:0.2em;
  color:{MUTED}; margin-top:14px;
}}
.draw {{ width:500px; height:252px; display:block; overflow:visible; }}
.draw .gnd {{ stroke:rgba(237,230,218,0.16); stroke-width:1; }}
.draw .face {{ fill:rgba(232,184,75,0.16); stroke:{GOLD}; stroke-width:1.6; }}
.draw .top {{ fill:rgba(232,184,75,0.30); stroke:{GOLD}; stroke-width:1.6; }}
.draw .fig path {{ fill:{CREAM}; stroke:none; }}

.right {{ flex:1 1 auto; display:flex; flex-direction:column;
  align-items:flex-start; justify-content:center; }}
.tag {{
  font-family:'JetBrains Mono',monospace; font-size:14px; letter-spacing:0.2em;
  color:{MUTED}; margin-bottom:14px;
}}
.tag b {{ color:{GOLD}; font-weight:500; }}
.field {{ display:flex; flex-wrap:wrap; align-content:flex-start; }}
.field .tk {{ display:block; flex:0 0 auto; fill:{GOLD}; opacity:0.92; }}

.foot {{
  flex:0 0 auto; font-family:'JetBrains Mono',monospace; font-size:14px;
  letter-spacing:0.15em; color:{DIM}; padding-top:10px;
}}
"""


def html_for(card):
    n = max(1, round(card["lb"] / F150_LB))
    field, _grid = truck_field(n)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="frame">
  <div class="brand">
    <img src="data:image/png;base64,{LOGO}" alt="">
    <div class="words"><span class="mark">THE ANCIENT ATLAS</span><span class="sep"> \u00b7 </span><span class="sub">FEEL THE WEIGHT</span></div>
  </div>
  <div class="body">
    <div class="left">
      <div><div class="line">{card['line']}</div>
      <div class="where">{card['where']}</div></div>
      {stone_svg(card['dim'])}
    </div>
    <div class="right">
      <div class="tag">ONE STONE, IN <b>FORD F-150s</b></div>
      {field}
    </div>
  </div>
  <div class="foot">THEANCIENTATLAS.COM \u00b7 EXPERIENCES</div>
</div>
</body></html>"""


# Playwright is not installed on the machine that has Chrome, and the fonts and
# logo are inlined as base64, so the documents need no network and no
# automation layer.
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    """Render each card, then stop waiting for Chrome to admit it is finished.

    Chrome writes the PNG and then sits there. --virtual-time-budget with
    --screenshot does not reliably exit on this build, so a blocking run()
    hangs for the full timeout on every card and the whole job stalls after
    the first one. Launch it, watch for the file to appear and stop growing,
    then kill it. The bytes are already on disk by then.
    """
    import shutil, subprocess, tempfile, time
    if not pathlib.Path(CHROME).exists():
        sys.exit("ABORT: Chrome is not at %s" % CHROME)

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ogcards-"))
    written = []
    for card in CARDS:
        page = tmp / (card["file"].replace(".png", ".html"))
        page.write_text(html_for(card))
        dest = OUT / card["file"]
        if dest.exists():
            dest.unlink()
        proc = subprocess.Popen([
            CHROME, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            "--user-data-dir=%s/profile-%s" % (tmp, card["file"]),
            "--screenshot=%s" % dest,
            "--window-size=1200,630",
            "--virtual-time-budget=2500",
            page.as_uri(),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        size, stable, waited = -1, 0, 0.0
        while waited < 40:
            time.sleep(0.4); waited += 0.4
            now = dest.stat().st_size if dest.exists() else -1
            stable = stable + 1 if (now == size and now > 0) else 0
            size = now
            if stable >= 3:
                break
        proc.kill()
        proc.wait()
        if not dest.exists() or dest.stat().st_size < 40000:
            sys.exit("ABORT: %s did not render (%s bytes)"
                     % (card["file"], dest.stat().st_size if dest.exists() else "no"))
        written.append((card["file"], dest.stat().st_size))

    # seven identical files means seven blank frames, which is still seven files
    sizes = [b for _, b in written]
    if len(set(sizes)) < len(sizes) - 1:
        sys.exit("ABORT: the cards are suspiciously identical: %r" % written)
    for name, size in written:
        print("  ok %-22s %8d bytes" % (name, size))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
    print("\n%d cards -> %s" % (len(CARDS), OUT))
