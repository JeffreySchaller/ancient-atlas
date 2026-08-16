#!/usr/bin/env python3
"""Wire the Patterns cards into the builder's <head>.

Patterns shipped with og:title, og:description and og:url but no og:image and no
twitter tags at all, so every share of /patterns/ rendered as a bare text stub.
This adds the image, its dimensions, an alt string, and the full twitter block,
matching the convention the Library already uses.

The ?v= cache buster matters: Facebook, LinkedIn and iMessage all cache OG images
aggressively and by URL, so a card regenerated without a new query string can
keep serving the old picture for days.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-patterns.py"
CARDS = REPO / "public" / "patterns" / "og"
V = 1

src = BUILDER.read_text()
orig = src

expected = {"index", "machining", "precision", "polygonal", "geometry",
            "scale", "hardness", "stratigraphy"}
have = {p.stem for p in CARDS.glob("*.png")}
if expected - have:
    sys.exit(f"ABORT: missing cards {sorted(expected - have)}; "
             "run scripts/generate-patterns-og-images.py on the Mac first")

# ---------------------------------------------------------------- pattern page
PAGE_ANCHOR = '<meta property="og:url" content="https://theancientatlas.com/patterns/{key}/">'
PAGE_ADD = f'''
<meta property="og:image" content="https://theancientatlas.com/patterns/og/{{key}}.png?v={V}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{{e(spec['name'])}} on The Ancient Atlas: {{len(carriers)}} sites in {{n_countries}} countries, marked on a world map.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{e(spec['name'])}} · The Ancient Atlas">
<meta name="twitter:description" content="{{e(spec['claim'])}}">
<meta name="twitter:image" content="https://theancientatlas.com/patterns/og/{{key}}.png?v={V}">'''

# ------------------------------------------------------------------ index page
IDX_ANCHOR = '<meta property="og:url" content="https://theancientatlas.com/patterns/">'
IDX_ADD = f'''
<meta property="og:image" content="https://theancientatlas.com/patterns/og/index.png?v={V}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Patterns on The Ancient Atlas: seven engineering signatures, every carrier site marked on a world map.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Patterns · The Ancient Atlas">
<meta name="twitter:description" content="Seven engineering signatures tracked across 618 ancient sites, each with the comparative studies that argue it.">
<meta name="twitter:image" content="https://theancientatlas.com/patterns/og/index.png?v={V}">'''

for anchor, add in ((PAGE_ANCHOR, PAGE_ADD), (IDX_ANCHOR, IDX_ADD)):
    if add.strip().splitlines()[0] in src:
        continue
    if src.count(anchor) != 1:
        sys.exit(f"ABORT: expected exactly 1 of {anchor!r}, found {src.count(anchor)}")
    src = src.replace(anchor, anchor + add)

if src != orig:
    BUILDER.write_text(src)

assert src.count('property="og:image"') == 2, "expected one og:image per template"
assert src.count('name="twitter:card"') == 2, "expected one twitter:card per template"
assert src.count("summary_large_image") == 2, "wrong twitter card type count"

print("Wired og:image + twitter cards into both templates."
      if src != orig else "Already current.")
