#!/usr/bin/env python3
"""Open on the Western Stone, drop the big button, bring the trucks up.

Landing on the 2.5-ton Giza block was the polite choice and the wrong one. It is
the smallest stone in the set, and a person who bounces before scrolling never
learns the set gets twenty-two times heavier. The page now opens on the Western
Stone, which is the one that makes the point on arrival.

The HOLD TO PUSH slab is gone from the first screen. In its place the striker bar
becomes the thing you press and hold, which is better than a button anyway: you
are pushing the instrument that measures you, and the bar fills under your thumb.
One control instead of a control plus a readout, and roughly a hundred pixels of
first screen handed back.

A NOTE ON WHAT I DID NOT DO. The brief was to remove the push from the first
screen entirely and let it live further down. Desktop has exactly one push
control left, so removing it outright would leave the layout with no verb at all,
and relocating it into the comparison section means duplicating nodes the runtime
writes into by selector, which is how you get a striker that never moves. The bar
is the smaller control, in place, at no risk. If the push should genuinely move
below the trucks, that is a section move and wants doing deliberately.

Everything under the stone rides up: the comparison section loses most of its top
padding and the four cards tighten, so the flour, the bowling balls, the crowd
and the pickups reach the fold instead of sitting a scroll away. That row is the
whole point of the page. It is silly and it is the only part a body understands.

Runs between extract.py and inject.py. Idempotent.
"""
import pathlib
import sys

APP = pathlib.Path(__file__).parent / "app.html"
src = APP.read_text(encoding="utf-8")
orig = src

# ------------------------------------------------- 1. open on the Western Stone
STONE = [
    ("state = { k:'giza',", "state = { k:'temple',"),
    ("return { k:this.props.stone || 'giza', at:null };",
     "return { k:this.props.stone || 'temple', at:null };"),
    ("const k = ALIAS[raw] || (SITES.some(s => s.k === raw) ? raw : 'giza');",
     "const k = ALIAS[raw] || (SITES.some(s => s.k === raw) ? raw : 'temple');"),
    # The prop default is the one that actually decides. Changing the three
    # code-level fallbacks moved nothing, because _readQuery returns
    # this.props.stone first and the component's declared default is giza. The
    # render is what caught it: the page still opened on the 2.5-ton block.
    ("&quot;options&quot;:[&quot;giza&quot;,&quot;ollan&quot;,&quot;temple&quot;,"
     "&quot;trilithon&quot;,&quot;pregnant&quot;,&quot;forgotten&quot;],"
     "&quot;default&quot;:&quot;giza&quot;",
     "&quot;options&quot;:[&quot;giza&quot;,&quot;ollan&quot;,&quot;temple&quot;,"
     "&quot;trilithon&quot;,&quot;pregnant&quot;,&quot;forgotten&quot;],"
     "&quot;default&quot;:&quot;temple&quot;"),
]
for old, new in STONE:
    if old in src:
        src = src.replace(old, new)
    elif new not in src:
        sys.exit("ABORT: default-stone anchor not found: " + old[:52])

# --------------------------------- 2. the bar becomes the press target, button off
BAR = ('<div style="position:relative;height:13px;border-radius:7px;background:#08070c;'
       'border:1px solid rgba(201,168,76,.22);overflow:hidden;'
       'box-shadow:inset 0 2px 6px rgba(0,0,0,.9)">')
BAR_LIVE = ('<div sc-camel-on-pointer-down="{{ startHold }}" role="button" tabindex="0" '
            'aria-label="Press and hold to push" style="position:relative;height:22px;'
            'border-radius:11px;background:#08070c;border:1px solid rgba(201,168,76,.34);'
            'overflow:hidden;cursor:pointer;user-select:none;-webkit-user-select:none;'
            'touch-action:none;box-shadow:inset 0 2px 6px rgba(0,0,0,.9),'
            '0 0 0 1px rgba(201,168,76,.08)">')
if BAR_LIVE not in src:
    if src.count(BAR) != 1:
        sys.exit("ABORT: expected 1 desktop striker bar, found %d" % src.count(BAR))
    src = src.replace(BAR, BAR_LIVE)

BTN = ('<div sc-camel-on-pointer-down="{{ startHold }}" role="button" tabindex="0" '
       'aria-label="Hold to push" style="align-self:flex-start;margin-top:8px;')
if 'aria-label="Hold to push" style="display:none;align-self:flex-start;' not in src:
    if src.count(BTN) != 1:
        sys.exit("ABORT: expected 1 desktop rail push button, found %d" % src.count(BTN))
    src = src.replace(BTN, BTN.replace('style="align-self:flex-start;',
                                       'style="display:none;align-self:flex-start;'))

# ------------------------------------------------- 3. bring the comparison up
PAD = ('<section data-screen-label="04 Scale" style="max-width:1120px;margin:0 auto;'
       'padding:clamp(56px,9vw,104px) clamp(20px,4vw,40px) 0;')
PAD_NEW = ('<section data-screen-label="04 Scale" style="max-width:1120px;margin:0 auto;'
           'padding:clamp(18px,2.4vw,30px) clamp(20px,4vw,40px) 0;')
if PAD_NEW not in src:
    if PAD not in src:
        sys.exit("ABORT: the comparison section padding is not what this patch expects")
    src = src.replace(PAD, PAD_NEW)

GAP = ('gap:clamp(20px,3vw,32px);scroll-snap-align:start"> <div data-rise="" '
       'style="display:flex;flex-direction:column;gap:9px;')
if GAP in src:
    src = src.replace(GAP, GAP.replace("gap:clamp(20px,3vw,32px)", "gap:clamp(12px,1.6vw,18px)"), 1)

CARDS = 'grid-template-columns:repeat(auto-fit,minmax(min(45%,190px),1fr));gap:clamp(10px,1.5vw,14px)'
if CARDS in src:
    src = src.replace(CARDS,
                      'grid-template-columns:repeat(auto-fit,minmax(min(45%,168px),1fr));'
                      'gap:clamp(8px,1.1vw,11px)', 1)

# ------------------------------------- 5. the comparison drops its own header
# "04 · You have held these" plus "Every one of these has been in your hands.
# Count them." costs 160px above the cards, and the cards say it themselves. A
# heading that restates its own contents is the cheapest 160px on the page.
HEAD = ('<span style="font-family:\'JetBrains Mono\',monospace;font-size:9.5px;'
        'letter-spacing:.3em;text-transform:uppercase;color:#C9A84C">04 · You have held these'
        '</span>')
if HEAD in src:
    a = src.rfind('<div data-rise=""', 0, src.find(HEAD))
    b = src.find("</div>", src.find("Count them.")) + len("</div>")
    src = src[:a] + src[b:]

# ------------------------------------------- 4. let the first screen be shorter
# Measuring showed the cards still landing ~470px below the fold, because the
# specimen section is pinned to min-height:100vh and the stage inside it takes
# 76vh on top of that. The app disables scroll snapping at runtime anyway, so
# the full-viewport floor is buying nothing but distance from the payoff.
d01 = src.find('data-screen-label="D01 Specimen"')
d02 = src.find('data-screen-label="D02 Verdict"')
if d01 < 0 or d02 < 0:
    sys.exit("ABORT: cannot bracket the specimen section")
seg = src[d01:d02]
if "min-height:100vh" in seg:
    seg = seg.replace("min-height:100vh", "min-height:auto", 1)
if "min-height:min(76vh,560px)" in seg:
    seg = seg.replace("min-height:min(76vh,560px)", "min-height:min(56vh,440px)", 1)
src = src[:d01] + seg + src[d02:]

if src != orig:
    APP.write_text(src, encoding="utf-8")

assert "state = { k:'temple'," in src, "default state stone did not change"
assert "&quot;default&quot;:&quot;temple&quot;" in src, "the prop default is still giza"
assert src.count('aria-label="Press and hold to push"') == 1, "striker is not the press target"
assert 'aria-label="Hold to push" style="display:none;align-self' in src, "the slab still shows"
# Five, not four: the four button handlers survive (one of them hidden) and
# the striker bar gains a fifth. The first version of this assert carried
# over the count from before this patch existed and failed on its own work.
assert src.count("{{ startHold }}") == 5, "expected 5 push handlers, got %d" % src.count("{{ startHold }}")
assert "clamp(18px,2.4vw,30px)" in src, "the comparison section did not move up"
assert "min-height:min(56vh,440px)" in src, "the stage was not shortened"
print("Opens on the Western Stone. The bar is the control. The trucks moved up.")
