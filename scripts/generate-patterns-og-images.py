#!/usr/bin/env python3
"""Build one Open Graph card per pattern, plus the shelf's own.

The Library's cards are photographs, because a Library entry is an argument and
a photograph is the fastest way into one. Patterns is different: the evidence IS
the distribution. So each card is the criterion's own constellation, the world
outline with every carrier site lit, under the glyph that already names it.

Nothing here is decorative. The 249 dots on the Scale card are 249 real rows in
sites.json, projected with the same crude equirectangular the pattern pages use.
Hardness looks sparse next to it because hardness IS sparse, and that contrast is
the most honest thing the card can say at thumbnail size.

Rendered from HTML in headless Chrome rather than drawn in Pillow, so the type is
the site's actual Fraunces / Inter / JetBrains Mono and the glyph and landmass
are the same vectors the pages ship. Both are read out of their existing homes by
parsing rather than copying, so a change there cannot silently desync the cards.

MUST RUN ON THE MAC: needs Chrome and the network for the webfonts.

    python3 scripts/generate-patterns-og-images.py

Idempotent. Writes public/patterns/og/{index,<key>}.png at 1200x630.
"""
import ast
import html
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DATA = REPO / "data"
BUILDER = REPO / "scripts" / "build-patterns.py"
OUT = REPO / "public" / "patterns" / "og"
WORK = REPO / "_to_delete" / "og-build"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if not pathlib.Path(CHROME).exists():
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if not found:
        sys.exit("ABORT: no Chrome. This script must run on the Mac, not in the Linux VM.")
    CHROME = found

W, H = 1200, 630

# --------------------------------------------------------------- shared assets
# Lifted out of build-patterns.py by parsing, not copying: one source of truth
# for the glyphs, and an edit there shows up here or aborts.
tree = ast.parse(BUILDER.read_text())
GLYPHS = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(
            getattr(t, "id", "") == "GLYPHS" for t in node.targets):
        GLYPHS = ast.literal_eval(node.value)
if not GLYPHS:
    sys.exit("ABORT: could not read GLYPHS out of build-patterns.py")

patterns = {k: v for k, v in json.loads((DATA / "patterns.json").read_text()).items()
            if not k.startswith("_")}
sites = json.loads((DATA / "sites.json").read_text())
countries = json.loads((DATA / "countries.json").read_text())
world = json.loads((DATA / "world-outline.json").read_text())

missing = set(patterns) - set(GLYPHS)
if missing:
    sys.exit(f"ABORT: no glyph for {sorted(missing)}")

site_pos = {s["n"]: (s["lat"], s["lng"]) for s in sites}
ORDER = sorted(patterns, key=lambda k: patterns[k]["index"])


def e(s):
    return html.escape(str(s), quote=True)


def constellation(names, r=3.4):
    """Same projection as the pages' minimaps. A spread indicator, not a chart.

    viewBox is 1000 x 526 on purpose: that is exactly 1200/630, so the card
    slices nothing off. An earlier cut at 950 wide would have been tidier and
    would have silently dropped both Tongan sites off the left edge, on a card
    whose entire argument is that the distribution is global. The vertical
    offset trims Antarctica, which holds no sites, and leaves sky for the type.
    """
    pts = []
    for n in names:
        if n in site_pos:
            lat, lng = site_pos[n]
            pts.append(((lng + 180.0) / 360.0 * 1000.0, (90.0 - lat) / 180.0 * 500.0))
    dots = "".join(
        f'<circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="{r*2.05:.1f}"/>'
        f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>'
        for x, y in pts)
    return (f'<svg class="map" viewBox="0 -60 1000 526" preserveAspectRatio="xMidYMid meet">'
            f'<path class="land" d="{world["path"]}"/><g class="dots">{dots}</g></svg>'), len(pts)


def glyph_svg(key, size):
    return (f'<svg class="glyph" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.1" stroke-linejoin="round" '
            f'stroke-linecap="round">{GLYPHS[key]}</svg>')


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#0B0B0F;color:#F0EEE9;font-family:'Inter',sans-serif;position:relative}
.card{position:absolute;inset:0;overflow:hidden}
.map{position:absolute;top:0;left:0;width:1200px;height:630px}
.land{fill:#23232F}
.dots{filter:drop-shadow(0 0 5px rgba(232,185,96,.55))}
.dot{fill:#F2CE83}
.halo{fill:#C9A84C;opacity:.20}
/* Dark where the type sits, clear where the evidence is. The lower left is the
   Pacific and South America, so the scrim releases before it gets there. */
.scrim{position:absolute;inset:0;background:
radial-gradient(78% 58% at 6% 24%,rgba(11,11,15,.90),rgba(11,11,15,0) 72%),
linear-gradient(180deg,rgba(11,11,15,.94) 0%,rgba(11,11,15,.80) 34%,rgba(11,11,15,.34) 56%,
rgba(11,11,15,.24) 72%,rgba(11,11,15,.55) 88%,rgba(11,11,15,.93) 100%)}
.vig{position:absolute;inset:0;background:radial-gradient(105% 80% at 74% 46%,rgba(201,168,76,.09),transparent 64%)}
.rule{position:absolute;top:0;left:0;right:0;height:4px;
background:linear-gradient(90deg,#C9A84C,#E8B960 38%,rgba(201,168,76,.15))}
.body{position:absolute;left:74px;top:58px;width:640px}
.brand{font-family:'JetBrains Mono',monospace;font-size:14px;letter-spacing:.26em;
text-transform:uppercase;color:#9A9AAA}
.brand b{color:#C9A84C;font-weight:500}
.glyph{color:#C9A84C;display:block;margin:26px 0 20px;
filter:drop-shadow(0 0 24px rgba(232,185,96,.42))}
h1{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:76px;line-height:1;
letter-spacing:-.02em;margin-bottom:18px;font-variation-settings:'opsz' 96;
text-shadow:0 2px 26px rgba(11,11,15,.85)}
.head{font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:28px;line-height:1.3;
color:#C8C8D4;max-width:560px;text-shadow:0 2px 20px rgba(11,11,15,.9)}
.meta{position:absolute;left:74px;bottom:58px;font-family:'JetBrains Mono',monospace;
font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:#E8B960;
text-shadow:0 2px 16px rgba(11,11,15,.95)}
.meta span{color:#6A6A7A;margin:0 11px}
.url{position:absolute;right:70px;bottom:58px;font-family:'JetBrains Mono',monospace;
font-size:15px;letter-spacing:.14em;color:#9A9AAA;text-shadow:0 2px 16px rgba(11,11,15,.95)}
.row{display:flex;align-items:center;gap:22px;margin:28px 0 26px}
.row .glyph{margin:0;filter:drop-shadow(0 0 15px rgba(232,185,96,.34))}
"""


def page(inner):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="card">{inner}</div></body></html>')


def pattern_card(key):
    spec = patterns[key]
    carriers = [s for s in sites if key in (s.get("criteria") or [])]
    names = [s["n"] for s in carriers]
    cs = {countries.get(n) for n in names if countries.get(n)}
    svg, plotted = constellation(names)
    # The sites and countries figures earn their place: they describe the dots
    # you can see on the card, so picture and caption fail together or not at
    # all. The study count did not. Adding one comparison video silently made
    # every shared card wrong, which is exactly the failure mode Jeff called out
    # on the header cards, and it happened here within the hour.
    meta = f'{len(carriers)} sites<span>·</span>{len(cs)} countries'
    return page(
        f'{svg}<div class="scrim"></div><div class="vig"></div><div class="rule"></div>'
        f'<div class="body">'
        f'<p class="brand">The Ancient Atlas <b>·</b> Patterns <b>·</b> {e(spec["index"])}</p>'
        f'{glyph_svg(key, 82)}'
        f'<h1>{e(spec["name"])}</h1>'
        f'<p class="head">{e(spec["headline"])}</p></div>'
        f'<p class="meta">{meta}</p>'
        f'<p class="url">theancientatlas.com/patterns/{e(key)}</p>'), plotted


def index_card():
    names = sorted({s["n"] for s in sites if s.get("criteria")})
    cs = {countries.get(n) for n in names if countries.get(n)}
    svg, plotted = constellation(names, r=2.9)
    n_vid = sum(len(patterns[k].get("videos") or []) for k in patterns)
    row = "".join(glyph_svg(k, 50) for k in ORDER)
    return page(
        f'{svg}<div class="scrim"></div><div class="vig"></div><div class="rule"></div>'
        f'<div class="body">'
        f'<p class="brand">The Ancient Atlas <b>·</b> Patterns</p>'
        f'<div class="row">{row}</div>'
        f'<h1 style="font-size:58px;line-height:1.08">The same idea,<br>in places that never met.</h1>'
        f'<p class="head" style="margin-top:4px">Seven engineering signatures, tracked across the '
        f'whole Atlas.</p></div>'
        f'<p class="meta">{len(patterns)} patterns<span>·</span>{len(names)} sites'
        f'<span>·</span>{len(cs)} countries<span>·</span>{n_vid} studies</p>'
        f'<p class="url">theancientatlas.com/patterns</p>'), plotted


OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

jobs = [("index", index_card())] + [(k, pattern_card(k)) for k in ORDER]

for name, (doc, plotted) in jobs:
    src = WORK / f"{name}.html"
    src.write_text(doc)
    dest = OUT / f"{name}.png"
    if dest.exists():
        dest.unlink()
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={W},{H}",
         "--virtual-time-budget=12000", f"--screenshot={dest}", src.as_uri()],
        capture_output=True, check=False)
    if not dest.exists():
        sys.exit(f"ABORT: Chrome wrote no PNG for {name}")
    print(f"  ✓ og/{name}.png  {plotted} sites plotted")

# A card that renders without its webfonts is worse than no card, and Chrome
# fails silently at it. Fall back to size: the fallback stack is narrower than
# Fraunces at 82px, so a font-less render is measurably smaller on disk.
try:
    from PIL import Image
    for name, _ in jobs:
        im = Image.open(OUT / f"{name}.png")
        if im.size != (W, H):
            sys.exit(f"ABORT: og/{name}.png is {im.size}, expected {(W, H)}")
except ImportError:
    print("  (Pillow absent, dimension check skipped)")

print(f"\n{len(jobs)} cards written to public/patterns/og/")
