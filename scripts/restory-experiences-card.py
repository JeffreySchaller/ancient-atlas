#!/usr/bin/env python3
# The Experiences hover card was still selling a mechanic the page no longer
# has. It showed a pull meter, "it needs 5,000 lb", "0.04 %", "it does not
# move", and led on the smallest stone by tonnage.
#
# The page now runs essential -> weight -> detail -> the real thing, and states
# the weight in a vehicle the reader parks outside their own house. The card
# says that instead: a field of pickups, masked so it reads as "more than fits
# here", and no figure anywhere.
#
# Idempotent. Assertions read the finished file.

import re, sys
from pathlib import Path

IDX = Path(__file__).resolve().parent.parent / "public" / "index.html"
src = IDX.read_text()
orig = len(src)

# the F-150 drawn for the experience itself, so the card and the page agree
F150 = ("M1.6 6L23.5 6L24.6 1.8L37.6 1.8L40.4 5.8L57 5.8L58.2 6.6L58.2 14.6"
        "L50 14.6A4.4 3 0 0 0 41.2 14.6L17.4 14.6A4.4 3 0 0 0 8.6 14.6L1.6 14.6Z"
        "M3.6 7.4L21.7 7.4L21.7 10.8L3.6 10.8Z"
        "M26.6 3.4L32.8 3.4L32.8 6.8L26.6 6.8Z"
        "M34 3.4L36.2 3.4L38 7L34 7Z"
        "M9.7 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0"
        "M11.65 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0"
        "M42.3 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0"
        "M44.25 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0")

ROWS, PER = 3, 10
FLEET = "".join([
'<div class="fw-fleet">',
  '<div class="fw-frow"><span>One stone, in pickups</span><span class="fw-fride">Ford F-150</span></div>',
  '<svg class="fw-fdef" width="0" height="0" aria-hidden="true" focusable="false">',
  '<defs><path id="fw-truck" d="', F150, '"/></defs></svg>',
  '<div class="fw-ffield" aria-hidden="true">',
  "".join('<svg class="fw-fv" viewBox="0 0 60 20" fill-rule="evenodd"><use href="#fw-truck"/></svg>'
          for _ in range(ROWS * PER)),
  '</div>',
'</div>'])

OLD_GAUGE_RE = re.compile(r'\s*<div class="fw-gauge">.*?</div>\s*</div>', re.S)

if 'class="fw-fleet"' not in src:
    m = OLD_GAUGE_RE.search(src)
    if not m:
        sys.exit("ABORT: the pull gauge is not where it was")
    src = src[:m.start()] + "\n        " + FLEET + src[m.end():]

src = src.replace(
    '<div class="fw-bloom-title">2.5 tons. And that’s the smallest.</div>',
    '<div class="fw-bloom-title">Stand next to it. Then count the trucks.</div>')
src = src.replace(
    '<div class="fw-bloom-sub">Six stones. The largest is 1,500.</div>',
    '<div class="fw-bloom-sub">Weighed in the vehicle parked outside your own house.</div>')
src = src.replace('<span class="fw-stage-ft">6 stones</span>',
                  '<span class="fw-stage-ft">Six stones</span>')

# ---------------------------------------------------------------- the CSS
# The stylesheet is one long line, so a span regex from .fw-gauge to the
# reduced-motion query looks tidy and quietly eats .fw-bloom-title,
# .fw-bloom-sub and .fw-cta-full on the way past. It did, and the card
# rendered as unstyled black text with a blue link. Remove each rule by name.
GAUGE_RULES = [
    ".fw-gauge", ".fw-grow", ".fw-gneed", ".fw-track", ".fw-fill",
    ".fw-gpct", ".fw-gstill",
]
LITERALS = [
    ".fw-wrap:hover .fw-fill{animation:fwFill 1.4s cubic-bezier(.16,.9,.3,1) forwards}",
    "@keyframes fwFill{0%{width:0}100%{width:4%}}",
    "@media (prefers-reduced-motion:reduce){.fw-wrap:hover .fw-fill{animation:none;width:4%}}",
]

NEW_CSS = "".join([
".fw-fleet{margin-top:11px}",
".fw-frow{display:flex;align-items:baseline;justify-content:space-between;",
"font-family:var(--font-mono);font-size:9px;letter-spacing:.13em;text-transform:uppercase;",
"color:var(--mist);margin-bottom:7px}",
".fw-fride{color:var(--amber);letter-spacing:.06em;text-transform:none;font-size:10.5px;",
"font-family:var(--font-serif);font-weight:600}",
".fw-fdef{position:absolute;width:0;height:0;overflow:hidden}",
".fw-ffield{display:flex;flex-wrap:wrap;gap:4px 5px;",
"-webkit-mask-image:linear-gradient(180deg,#000 56%,rgba(0,0,0,.10));",
"mask-image:linear-gradient(180deg,#000 56%,rgba(0,0,0,.10))}",
".fw-fv{width:22px;height:7.4px;flex:none;fill:var(--champagne);opacity:0;",
"transform:translateY(3px);transition:opacity .3s ease,transform .3s cubic-bezier(.2,.8,.2,1)}",
".fw-wrap:hover .fw-fv{opacity:.92;transform:none}",
"".join(".fw-wrap:hover .fw-fv:nth-child(%d){transition-delay:%dms}" % (i + 1, i * 22)
       for i in range(ROWS * PER)),
"@media (prefers-reduced-motion:reduce){.fw-fv{opacity:.92;transform:none;transition:none}}",
])

if ".fw-fleet{" not in src:
    for sel in GAUGE_RULES:
        m = re.search(re.escape(sel) + r"\{[^{}]*\}", src)
        if not m:
            sys.exit("ABORT: rule %s is not where it was" % sel)
        src = src[:m.start()] + src[m.end():]
    for lit in LITERALS:
        if lit not in src:
            sys.exit("ABORT: %r is not where it was" % lit[:44])
        src = src.replace(lit, "")
    if ".fw-bloom-title{" not in src:
        sys.exit("ABORT: the card title rule vanished before the insert")
    src = src.replace(".fw-bloom-title{", NEW_CSS + ".fw-bloom-title{", 1)

# ---------------------------------------------------------- assertions
fails = []
def want(cond, msg):
    if not cond: fails.append(msg)

# "2.5 tons" also lives in a Giza site description, so every copy check has to
# be scoped to the card or it fires on data that is perfectly correct.
_a = src.index('<div class="fw-bloom"')
card = src[_a:src.index('</a>', src.index('fw-cta-full', _a))]

want("fw-gauge" not in src, "the pull gauge markup survives")
want("fw-fill" not in src, "the pull meter styling survives")
want("fwFill" not in src, "the pull animation survives")
for gone in ["Your pull", "It needs 5,000 lb", "It does not move", "0.04 %",
             "2.5 tons", "The largest is 1,500"]:
    want(gone not in card, "the card still says %r" % gone)
want(src.count('class="fw-fleet"') == 1, "the fleet strip is missing or doubled")
want(src.count('class="fw-fv"') == ROWS * PER,
     "expected %d silhouettes, found %d" % (ROWS * PER, src.count('class="fw-fv"')))
want(src.count('id="fw-truck"') == 1, "the truck path is missing or duplicated")
want("Stand next to it. Then count the trucks." in src, "the new headline is missing")
want("fw-cta-full" in src, "the card lost its way in")
for rule in [".fw-bloom-title{", ".fw-bloom-sub{", ".fw-cta-full{"]:
    want(rule in src, "the card lost its %s styling" % rule)
# A model name is not a figure. F-150 does not go stale; a tonnage does.
_copy = re.sub(r"F-150", " ", re.sub(r"<[^>]+>", " ", card))
want(not re.search(r"[0-9]", _copy),
     "the card copy still carries a figure: %r" % " ".join(_copy.split())[:200])

if fails:
    for f in fails:
        print("  FAIL " + f)
    sys.exit("ABORT: %d check(s) failed, nothing written" % len(fails))

IDX.write_text(src)
print("index.html %d -> %d chars" % (orig, len(src)))
print("Experiences card restoried: %d silhouettes, zero figures" % (ROWS * PER))
