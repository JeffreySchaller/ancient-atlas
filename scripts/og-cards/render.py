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

DO = [("TURN IT", "With your hand", BODY),
      ("SCALE IT", "A person at six feet", BODY),
      ("WEIGH IT", "In the truck outside", GOLD)]

CARDS = [
    {
        "file": "og.png",
        "eyebrow": "SIX STONES \u00b7 TURN THEM WITH YOUR HAND",
        "display": "Stand next to it. Then <em>count the trucks</em>.",
        "display_size": 82,
        "lead": "Six of the heaviest stones ever cut. Turn each one, put a "
                "person beside it, and see the weight in the vehicle parked "
                "outside your own house.",
        "lead_width": 980,
        "stats": DO,
    },
    {
        "file": "og-giza.png",
        "eyebrow": "GIZA BLOCK \u00b7 EGYPT",
        "display": "One block. And then <em>two million</em> more.",
        "display_size": 86,
        "lead": "About what you could park on your driveway. Then the pyramid "
                "needed it again, and again.",
        "stats": DO,
    },
    {
        "file": "og-ollan.png",
        "eyebrow": "OLLANTAYTAMBO MONOLITH \u00b7 PERU",
        "display": "Carried up a <em>mountain</em>.",
        "display_size": 104,
        "lead": "A row of them nose to tail, the length of a street, and every "
                "one went uphill across a river.",
        "stats": DO,
    },
    {
        "file": "og-temple.png",
        "eyebrow": "THE WESTERN STONE \u00b7 JERUSALEM",
        "display": "Longer than a <em>bus</em>, and lifted into a wall.",
        "display_size": 82,
        "lead": "Enough to fill a supermarket car park, twice over, fused into "
                "one piece and set above head height.",
        "stats": DO,
    },
    {
        "file": "og-trilithon.png",
        "eyebrow": "THE TRILITHON \u00b7 BAALBEK, LEBANON",
        "display": "Three of these, <em>side by side</em>, twenty feet up.",
        "display_size": 78,
        "lead": "A queue that would run out of the town. And then there are "
                "three of them, matched, in a row.",
        "stats": DO,
    },
    {
        "file": "og-pregnant.png",
        "eyebrow": "STONE OF THE PREGNANT WOMAN \u00b7 BAALBEK",
        "display": "Still lying where it was <em>cut</em>.",
        "display_size": 96,
        "lead": "Dressed on every face and left in the quarry at an angle, as "
                "though the job stopped mid-sentence.",
        "stats": DO,
    },
    {
        "file": "og-forgotten.png",
        "eyebrow": "THE FORGOTTEN STONE \u00b7 BAALBEK",
        "display": "The heaviest one is <em>still down there</em>.",
        "display_size": 86,
        "lead": "Found under the quarry floor within living memory, beneath "
                "the stone everybody already knew about.",
        "stats": DO,
    },
]

CSS = f"""
@font-face {{
  font-family: 'Fraunces';
  src: url(data:font/woff2;base64,{FRAUNCES}) format('woff2-variations');
  font-weight: 100 900;
}}
@font-face {{
  font-family: 'Fraunces';
  src: url(data:font/woff2;base64,{FRAUNCES_I}) format('woff2-variations');
  font-weight: 100 900;
  font-style: italic;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM400}) format('woff2');
  font-weight: 400;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM500}) format('woff2');
  font-weight: 500;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; }}
body {{
  background: #080706;
  padding: 9px;
  -webkit-font-smoothing: antialiased;
}}
.frame {{
  width: 100%; height: 100%;
  border: 1px solid rgba(232,184,75,0.30);
  background:
    radial-gradient(1100px 620px at 12% -8%, rgba(196,142,52,0.16) 0%, rgba(196,142,52,0.05) 38%, rgba(0,0,0,0) 72%),
    radial-gradient(700px 420px at 96% 106%, rgba(120,86,32,0.10) 0%, rgba(0,0,0,0) 70%),
    #0d0b09;
  padding: 30px 68px 47px 68px;
  display: flex;
  flex-direction: column;
}}
/* ---------------------------------------------------------- brand row */
.brand {{
  display: flex;
  align-items: center;
  gap: 22px;
  flex: 0 0 auto;
}}
.brand img {{ width: 74px; height: 74px; display: block; }}
.brand .words {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 19px;
  letter-spacing: 0.28em;
  white-space: nowrap;
}}
.brand .mark {{ color: {GOLD}; }}
.brand .sep  {{ color: rgba(232,184,75,0.45); padding: 0 2px; }}
.brand .sub  {{ color: {MUTED}; }}
/* ---------------------------------------------------------- middle */
.middle {{
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 6px;
}}
.eyebrow {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: 17px;
  letter-spacing: 0.22em;
  color: {MUTED};
  margin-bottom: 18px;
}}
.display {{
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 700;
  font-variation-settings: 'opsz' 144, 'SOFT' 0, 'WONK' 1;
  color: {CREAM};
  line-height: 0.92;
  letter-spacing: -0.012em;
  margin-bottom: 20px;
}}
.display em {{ font-style: italic; color: {GOLD}; }}
.lead {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: 27px;
  line-height: 1.44;
  color: {BODY};
}}
/* ---------------------------------------------------------- footer */
.rule {{
  flex: 0 0 auto;
  height: 1px;
  background: rgba(237,230,218,0.13);
  margin-bottom: 22px;
}}
.stats {{
  flex: 0 0 auto;
  display: grid;
  grid-template-columns: 357px 355px 1fr;
  margin-bottom: 54px;
}}
.stats .label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  letter-spacing: 0.18em;
  color: #7C756A;
  margin-bottom: 12px;
}}
.stats .value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 25px;
  letter-spacing: 0.01em;
}}
.foot {{
  flex: 0 0 auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  letter-spacing: 0.15em;
  color: {DIM};
}}
"""


def html_for(card):
    stats = "".join(
        f'<div><div class="label">{lab}</div>'
        f'<div class="value" style="color:{col}">{val}</div></div>'
        for lab, val, col in card["stats"]
    )
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="frame">
  <div class="brand">
    <img src="data:image/png;base64,{LOGO}" alt="">
    <div class="words"><span class="mark">THE ANCIENT ATLAS</span><span class="sep"> · </span><span class="sub">FEEL THE WEIGHT</span></div>
  </div>
  <div class="middle">
    <div class="eyebrow">{card['eyebrow']}</div>
    <div class="display" style="font-size:{card['display_size']}px">{card['display']}</div>
    <div class="lead" style="max-width:{card.get('lead_width', 1044)}px">{card['lead']}</div>
  </div>
  <div class="rule"></div>
  <div class="stats">{stats}</div>
  <div class="foot">THEANCIENTATLAS.COM · EXPERIENCES</div>
</div>
</body></html>"""


# Playwright is not installed on the machine that has Chrome, and the fonts and
# logo are already inlined as base64, so the page needs no network and no
# automation layer. Write the seven documents and let Chrome screenshot them.
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
