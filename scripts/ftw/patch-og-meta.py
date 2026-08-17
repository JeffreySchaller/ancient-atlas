#!/usr/bin/env python3
# The bundle's OUTER wrapper carries a title and nothing else. Everything a
# crawler needs to build a share card lives in the inner document, which only
# exists after the unpacker has run. Some preview agents execute the script and
# find it; the ones that do not fall back to the URL. Put the card in the outer
# head where it does not depend on anyone running our JavaScript.
#
# Run AFTER inject.py, which rewrites the wrapper.
#
# Idempotent.

import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "public" / "experiences" / "feel-the-weight" / "index.html"
BASE = "https://theancientatlas.com/experiences/feel-the-weight/"
VER = "2"          # bump when the artwork changes; iMessage caches hard

TITLE = "Feel the Weight · try to move it · The Ancient Atlas"
DESC = ("Six of the heaviest stones ever cut. Turn each one with your hand, put "
        "a person beside it, and see the weight in the vehicle parked outside "
        "your own house.")
IMG = BASE + "og.png?v=" + VER
ALT = ("Stand next to it. Then count the trucks. Six stones from the Ancient "
       "Atlas, weighed in pickups.")

BLOCK = "\n".join([
    '  <!-- share card - patch-og-meta.py, re-run after inject.py -->',
    '  <meta name="description" content="%s">' % DESC,
    '  <link rel="canonical" href="%s">' % BASE,
    '  <meta property="og:type" content="website">',
    '  <meta property="og:site_name" content="The Ancient Atlas">',
    '  <meta property="og:title" content="%s">' % TITLE,
    '  <meta property="og:description" content="%s">' % DESC,
    '  <meta property="og:url" content="%s">' % BASE,
    '  <meta property="og:image" content="%s">' % IMG,
    '  <meta property="og:image:width" content="1200">',
    '  <meta property="og:image:height" content="630">',
    '  <meta property="og:image:alt" content="%s">' % ALT,
    '  <meta name="twitter:card" content="summary_large_image">',
    '  <meta name="twitter:title" content="%s">' % TITLE,
    '  <meta name="twitter:description" content="%s">' % DESC,
    '  <meta name="twitter:image" content="%s">' % IMG,
    '  <meta name="twitter:image:alt" content="%s">' % ALT,
    '  <!-- /share card -->',
])

src = OUT.read_text()
orig = len(src)

MARK_A = "  <!-- share card - patch-og-meta.py, re-run after inject.py -->"
MARK_B = "  <!-- /share card -->"

if MARK_A in src:
    a = src.index(MARK_A)
    b = src.index(MARK_B) + len(MARK_B)
    src = src[:a] + BLOCK + src[b:]
else:
    anchor = "  <title>"
    if anchor not in src:
        sys.exit("ABORT: the wrapper has no title to anchor to")
    end = src.index("</title>", src.index(anchor)) + len("</title>")
    src = src[:end] + "\n" + BLOCK + src[end:]

head = src[:src.index("</head>")]

fails = []
def want(c, m):
    if not c: fails.append(m)

want(src.count(MARK_A) == 1 and src.count(MARK_B) == 1, "the block did not land exactly once")
for prop in ["og:title", "og:description", "og:image", "og:url", "og:image:width",
             "twitter:card", "twitter:image", 'name="description"']:
    want(prop in head, "%s is not in the outer head" % prop)
want("?v=" + VER in head, "the image URL is not cache-busted")
want("You cannot lift it" not in src, "the wrapper still carries the old promise")
want(len(DESC) < 300 and len(ALT) < 300, "a meta value is too long to be used")

png = OUT.parent / "og.png"
want(png.exists() and png.stat().st_size > 40000,
     "og.png is missing or empty, so the card would 404")

if fails:
    for f in fails:
        print("  FAIL " + f)
    sys.exit("ABORT: %d check(s) failed, nothing written" % len(fails))

OUT.write_text(src)
print("wrapper %d -> %d chars; card at %s" % (orig, len(src), IMG))
