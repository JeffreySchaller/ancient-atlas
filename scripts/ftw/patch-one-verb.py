#!/usr/bin/env python3
"""Feel the Weight: one verb, glyphs instead of word-pills, less whispering.

Measured before touching anything: on a 1440 desktop the first screen showed TWO
"Hold to push" buttons and thirty-two separate runs of text at 11.5px or smaller.
A toy with one verb was presenting two of it, and the instruction for how to play
was set smaller than the credits.

WHAT CHANGES

  One push. The desktop laid out a push button on the stone AND a second one in
  the rail under the striker bar. The rail pairing is the instrument, bar and
  button together, so the stage copy goes and its floating hint goes with it. The
  stone is now just the stone, the figure and the striker, which is what a person
  came to look at.

  Spin, Reset and Cinema become glyphs. Three word-pills in the corner of the
  viewer were competing with the one control that matters, and they are secondary
  by definition: nobody arrives wanting to reset a camera. Same line language as
  the pattern marks, with the words kept as aria-labels and tooltips so nothing
  is lost to anyone who cannot see them.

  The rule stops spoiling the ending. "No single person can move this stone. It
  has never been done alone." is the punchline of the experience, printed above
  the button that delivers it. The instruction survives, the spoiler does not,
  and the striker gets to do its job.

  Em dashes out of the interface strings.

Runs on scripts/ftw/app.html between extract.py and inject.py.
Idempotent: running twice is a no-op.
"""
import pathlib
import re
import sys

APP = pathlib.Path(__file__).parent / "app.html"
src = APP.read_text(encoding="utf-8")
orig = src

def one(needle, label):
    n = src.count(needle)
    if n != 1:
        sys.exit("ABORT: %s matched %d times, expected 1" % (label, n))
    return needle

# ---------------------------------------------------- 1. the duplicate push
STAGE_BTN = ('<div sc-camel-on-pointer-down="{{ startHold }}" role="button" tabindex="0" '
             'aria-label="Hold to push" style="pointer-events:auto;flex:none;')
# This exact tag appears twice, once in the mobile stage (M01) and once in the
# desktop stage (D01). Only the desktop one is a duplicate, because only desktop
# shows the stage and the rail at the same time. Target it by position inside
# the D01 section rather than by string, which would have hidden both.
if "display:none;pointer-events:none;flex:none;" not in src:
    if src.count(STAGE_BTN) != 2:
        sys.exit("ABORT: expected 2 stage push tags, found %d" % src.count(STAGE_BTN))
    d01 = src.find('data-screen-label="D01 Specimen"')
    d02 = src.find('data-screen-label="D02 Verdict"')
    if d01 < 0 or d02 < 0 or d02 < d01:
        sys.exit("ABORT: cannot locate the D01 section")
    at = src.find(STAGE_BTN, d01, d02)
    if at < 0:
        sys.exit("ABORT: no stage push inside D01")
    src = (src[:at]
           + STAGE_BTN.replace('style="pointer-events:auto;flex:none;',
                               'style="display:none;pointer-events:none;flex:none;')
           + src[at + len(STAGE_BTN):])

STAGE_HINT = ('backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);'
              'white-space:nowrap">{{ hintPush }}</span>')
if 'white-space:nowrap;display:none">{{ hintPush }}' not in src:
    one(STAGE_HINT, "the desktop stage push hint")
    src = src.replace(STAGE_HINT, STAGE_HINT.replace(
        'white-space:nowrap">{{ hintPush }}', 'white-space:nowrap;display:none">{{ hintPush }}'))

# ------------------------------------------------- 2. controls become glyphs
GLYPH = {
    "Toggle rotation": '<path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M19.4 2.6v3.6h-3.6"/>',
    "Reset view": '<path d="M12 4.2v6.1l4.4 2.6"/><circle cx="12" cy="12" r="8.4"/>',
    "Cinematic view": '<rect x="3.2" y="6.4" width="17.6" height="11.2" rx="1.6"/>'
                      '<path d="M3.2 10.1h17.6M3.2 13.9h17.6M8 6.4v11.2M16 6.4v11.2"/>',
}
def svg(paths):
    return ('<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" style="display:block">' + paths + "</svg>")

# each control renders "{{ xLabel }}" or a bare word as its only child text
LABELS = [("Toggle rotation", "{{ spinLabel }}"), ("Reset view", "Reset"),
          ("Cinematic view", "{{ cineLabel }}")]
# Every control exists twice, once per layout. The first pass here stopped at
# the first match and only ever reached the mobile copy, so the desktop pills
# stayed as words and the measurement caught it. Swap all of them.
swapped = 0
for aria, text in LABELS:
    while True:
        hit = None
        for m in re.finditer(r'aria-label="' + re.escape(aria) + r'"', src):
            seg_end = src.find("</div>", m.end())
            seg = src[m.end():seg_end]
            if text in seg and "<svg" not in seg:
                hit = (m.end(), seg_end, seg)
                break
        if not hit:
            break
        a, b, seg = hit
        src = src[:a] + seg.replace(text, svg(GLYPH[aria]), 1) + src[b:]
        swapped += 1

# tighten the pills now that they hold a 15px mark instead of a word
src = src.replace("padding:7px 11px;border-radius:9px;font-size:9px",
                  "padding:8px;border-radius:9px;font-size:9px")

# -------------------------------------------------- 3. the rule stops spoiling
SPOILERS = [
    # The live status line directly below already reads "Press and hold. Push as
    # hard as you can." and updates as you play, so the static block must not
    # repeat it. The first draft of this patch made them near-identical, which
    # the render caught. The rule now says only the thing the status cannot.
    ("No single person can move this stone.<br />It has never been done alone."
     "<br />The striker measures how close you get.",
     "The striker measures how close you get."),
    ("No one moves this stone alone.<br />The striker shows how close you get.",
     "The striker shows how close you get."),
]
# Idempotency is decided by the absence of the OLD string, not the presence of
# the NEW one. The replacement here is a substring of the text it replaces, so a
# "have I already done this" check on the new text matched before the edit ran
# and silently skipped it.
for old, new in SPOILERS:
    if old in src:
        src = src.replace(old, new)
    elif new not in src:
        sys.exit("ABORT: rule copy not found and not already applied: " + old[:48])

# ----------------------------------------------------------- 4. em dashes out
DASHES = [
    ("Hold PUSH \\u2014 the striker shows how close you get",
     "Hold PUSH. The striker shows how close you get"),
    ("The striker is honest \\u2014 for the heavy ones your whole",
     "The striker is honest, and for the heavy ones your whole"),
    ("Volume up \\u2014 you'", "Volume up, and you'"),
]
for old, new in DASHES:
    if new in src or old not in src:
        continue
    src = src.replace(old, new)
src = src.replace("Volume up — you'", "Volume up, and you'")
src = src.replace("Hold PUSH — the striker", "Hold PUSH. The striker")
src = src.replace("The striker is honest — for", "The striker is honest, and for")


# ------------------------------------- 5. em dashes in the copy a player reads
# Scoped to interface strings. The credits and the weights-and-materials block
# are a dense reference list where the dash separates a name from its spec, and
# rewriting those as commas would make them harder to read, not easier.
READS = [
    ("The average stone in the Great Pyramid of Giza \u2014 and there are 2.3 million of them.",
     "The average stone in the Great Pyramid of Giza, and there are 2.3 million of them."),
    ("The average stone in the Great Pyramid of Giza — and there are 2.3 million of them.",
     "The average stone in the Great Pyramid of Giza, and there are 2.3 million of them."),
    ("Make it personal — your weight", "Make it personal · your weight"),
    ("Feel the Weight — try to move it", "Feel the Weight · try to move it"),
]
for old, new in READS:
    if old in src:
        src = src.replace(old, new)

if src != orig:
    APP.write_text(src, encoding="utf-8")

# Assert the end state, not the work done this run. The first version checked
# the swap count and therefore failed on the second, idempotent run, when
# there was correctly nothing left to swap.
for aria in GLYPH:
    for m in re.finditer(r'aria-label="' + re.escape(aria) + r'"', src):
        seg = src[m.end():src.find("</div>", m.end())]
        assert "<svg" in seg, "control still shows a word: " + aria
assert src.count('aria-label="Hold to push"') == 4, "push controls lost or duplicated"
assert 'display:none;pointer-events:none;flex:none;' in src, "stage push still showing"
assert "It has never been done alone" not in src, "the spoiler survives"
# At least four. A later patch in this directory moves the verb onto the
# striker bar and adds a fifth, so an equality check here fails whenever the
# two are run in sequence against an already-patched bundle.
assert src.count("{{ startHold }}") >= 4, "a push handler was dropped"
for aria in GLYPH:
    assert src.count('aria-label="' + aria + '"') >= 1, "lost control: " + aria

print("One verb on the stage, three controls glyphed, the rule no longer spoils it.")
