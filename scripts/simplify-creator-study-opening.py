#!/usr/bin/env python3
"""Fewer voices in the opening, and one obvious way in.

The first screen was carrying twelve elements before any content: an issue line,
a "The question" label, the question, a rule, a "The answer" label, the answer in
two colours, a byline in a third, a reel label in a fourth, the reel, a paragraph
with three bolded fragments, a contents row and a scroll cue. Every one of them
in a different size, weight or colour. That is not emphasis, it is a page talking
over itself, and the reader has no idea where to start.

What comes out:

  The "The question" and "The answer" labels. A serif line ending in a question
  mark does not need to be told it is a question, and the answer follows it. Two
  small mono labels gone, and with them two of the twelve.

  Bold inside prose. The answer, the byline and the essay each split into two
  colours mid-sentence for no reason a reader could name. Prose is now one
  colour. The single italic champagne phrase in the question survives, because
  one accent on a page is emphasis and five is noise.

  The counts, per the same rule we applied to the hub. "296 episodes" is a
  database fact rendered where nobody will notice it going stale.

  The em dashes.

What goes in: the reel becomes the entry. It was already the best thing on the
page and it was labelled in ten-pixel mono, which is how you hide something. It
now carries a plain sentence at reading size that says what to do and what
happens: start anywhere, one episode per country, and you will see the pattern
before anyone explains it.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-creator-feature.py"

src = BUILDER.read_text()
orig = src

OLD = """    <div class="issue">The Ancient Atlas <span>·</span> Creator Study <span>·</span> No. 01</div>
    <div class="qlabel">The question</div>
    <h1 class="q">What repeats when you stop sorting these places by <em>where they are</em>?</h1>
    <div class="qrule"></div>
    <div class="alabel">The answer</div>
    <p class="answer">Four ways of working stone do — and <b>Bernie Ong has spent 296 episodes tracing them.</b></p>
    <p class="byline">{stats['videos']} narrated studies by <b>Bernie Ong</b> · <b>Ageless Rock</b> on YouTube · <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">{e(HANDLE)} ↗</a></p>

    <div class="strip-lead">
      <div class="lab"><span>Start anywhere · <b>{len(teasers)} of his {stats['videos']} episodes</b>, one per country</span><i>Drag the reel →</i></div>
      <div class="reel">{reel}</div>
    </div>

    <p class="answer-sub">Ageless Rock is not a travel channel. Each episode is a <b>researched visual study</b> — assembled, sequenced and narrated rather than shot on location — and that is precisely why the pattern is visible from it. A traveller is bound by an itinerary. A researcher can set Ethiopia beside Peru on the same screen. Across <b>{stats['sites']} sites in {stats['countries']} countries</b>, doing exactly that, the same four methods keep surfacing. What follows is those four, then every episode he has made.</p>

    <nav class="contents">{contents}</nav>
    <div class="scrollcue">The four methods, then all {stats['videos']} episodes <span></span></div>"""

NEW = """    <div class="issue">The Ancient Atlas <span>·</span> Creator Study No. 01</div>
    <h1 class="q">What repeats when you stop sorting these places by <em>where they are</em>?</h1>
    <div class="qrule"></div>
    <p class="answer">Four ways of working stone do, and Bernie Ong has spent years tracing them.</p>
    <p class="byline">Bernie Ong · Ageless Rock on YouTube · <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">{e(HANDLE)} ↗</a></p>

    <div class="strip-lead">
      <div class="lab"><span>Start anywhere. One episode per country, and the pattern turns up
      before anyone explains it.</span><i>Drag &rarr;</i></div>
      <div class="reel">{reel}</div>
    </div>

    <p class="answer-sub">Ageless Rock is not a travel channel. Each episode is assembled,
    sequenced and narrated rather than shot on location, and that is precisely why the pattern is
    visible from it. A traveller is bound by an itinerary. A researcher can set Ethiopia beside Peru
    on the same screen, and do that often enough and the same four methods keep surfacing. What
    follows is those four, and then every episode he has made.</p>

    <nav class="contents">{contents}</nav>
    <div class="scrollcue">The four methods, then every episode <span></span></div>"""

if NEW not in src:
    if OLD not in src:
        sys.exit("ABORT: the opening section is not what this patch expects")
    src = src.replace(OLD, NEW)

# ------------------------------------------------------------------------ CSS
EDITS = [
    # the reel label stops whispering: a sentence at reading size, not 10px mono
    (".strip-lead .lab{display:flex;align-items:baseline;justify-content:space-between;gap:16px;"
     "font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;"
     "color:var(--mist);padding-bottom:11px;border-bottom:1px solid rgba(42,42,53,.7);"
     "margin-bottom:16px}",
     "/* The reel is the way in. It was labelled in ten-pixel mono, which is how you\n"
     "   hide something. */\n"
     ".strip-lead .lab{display:flex;align-items:baseline;justify-content:space-between;gap:20px;"
     "font-family:var(--sans);font-size:14.5px;line-height:1.5;letter-spacing:0;"
     "text-transform:none;color:var(--cloud);padding-bottom:13px;"
     "border-bottom:1px solid rgba(42,42,53,.7);margin-bottom:16px;text-align:left}"),
    (".strip-lead .lab b{color:var(--champagne);font-weight:700}",
     ".strip-lead .lab span{max-width:52ch}"),
    (".strip-lead .lab i{font-style:normal;white-space:nowrap}",
     ".strip-lead .lab i{font-style:normal;white-space:nowrap;font-family:var(--mono);"
     "font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--mist);flex:none}"),
    # prose is one colour
    ("p.answer-sub b{color:var(--ivory);font-weight:600}",
     "/* Prose is one colour. Five accents on a screen is not emphasis. */\n"
     "p.answer-sub b{color:inherit;font-weight:inherit}"),
]
for old, new in EDITS:
    if new in src:
        continue
    if old not in src:
        sys.exit("ABORT: CSS anchor drifted: " + old[:60])
    src = src.replace(old, new)

# the two dropped labels leave their rules behind; harmless, but say so
src = src.replace(".qlabel{font-family:var(--mono)",
                  "/* .qlabel and .alabel are no longer emitted; kept in case a future study\n"
                  "   wants them back. */\n.qlabel{font-family:var(--mono)")

if src != orig:
    BUILDER.write_text(src)

for gone in ('class="qlabel"', 'class="alabel"', "296 episodes", "Drag the reel"):
    assert gone not in src.split("<section class=\"opening\">")[1].split("</section>")[0], \
        "still present in the opening: " + gone
op = src.split('<section class="opening">')[1].split("</section>")[0]
if "—" in op:
    sys.exit("ABORT: an em dash survives in the opening")
for token in ("{stats['videos']}", "{stats['sites']}", "{stats['countries']}", "{len(teasers)}"):
    if token in op:
        sys.exit("ABORT: %s still renders into the opening" % token)
assert "Start anywhere. One episode per country" in src, "the entry sentence is missing"

print("Opening simplified: two labels dropped, prose in one colour, the reel promoted.")
