#!/usr/bin/env python3
"""Tell the story on /creators/, and stop opening with a headcount.

The page led with three figures in its first sentence. Figures are the wrong
opening for this page in particular, because the thing being sold is not the size
of the archive, it is what happens when you look at one person's whole body of
work instead of one video. Nobody ever stayed on a page because the number was
large.

So the counts come out of the prose and the argument goes in. The new deck says
why a reader should spend an evening here: a site page shows you a place, a body
of work shows you a habit of mind. That is the product.

The three big numeric tiles under the study become three analogs, because the
quantities they described are digital and therefore invisible. "281 walkthroughs"
is a database fact. "Weeks of evenings, if you started tonight" is the same fact
rendered at human scale, and it stays true as the archive grows.

The contributor table keeps every channel and every handle, which is the credit
that matters, and swaps its two count columns for one proportional bar. The bar
IS the analog: it says "one channel carries most of this" faster than a number
does, and unlike a number it cannot go stale. Same move as the region bars on the
header card.

Em dashes cleared from everything the page renders.

Idempotent: running twice is a no-op.
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-creators-hub.py"
COPY = REPO / "_to_delete" / "creators_copy.py"

ns = {}
exec(COPY.read_text(), ns)

src = BUILDER.read_text()
orig = src

EM = "—"

# ------------------------------------------------------------------ 1. the deck
old_deck = """  <p class="deck">The Atlas is {TOTAL_SITES} places. Almost none of them would be watchable without the
  channels that documented them — <b>{TOTAL_V} walkthroughs from {len(creators)} creators</b>. A Creator Study
  is a close reading of one of those bodies of work: what it covers, what it keeps returning to,
  and what it lets you see that a single site page never could.</p>"""
new_deck = '  <p class="deck">' + ns["DECK"] + "</p>"
if new_deck not in src:
    if old_deck not in src:
        sys.exit("ABORT: the deck is not what this patch expects")
    src = src.replace(old_deck, new_deck)

# --------------------------------------------------------------- 2. the study
old_line = '"line": "Four ways of working stone, traced across 296 narrated studies.",'
new_line = '"line": "%s",' % ns["STUDY_LINE"]
if new_line not in src:
    if old_line not in src:
        sys.exit("ABORT: the study line is not what this patch expects")
    src = src.replace(old_line, new_line)

old_body = """      <p class="body">{STUDY["line"]} Not a travel channel — each episode is a researched visual study,
      assembled and narrated rather than shot on location, which is precisely why the pattern is visible
      from it. A traveller is bound by an itinerary. A researcher can set Ethiopia beside Peru on the
      same screen.</p>"""
new_body = '      <p class="body">{STUDY["line"]} ' + ns["STUDY_BODY"] + "</p>"
if new_body not in src:
    if old_body not in src:
        sys.exit("ABORT: the study body is not what this patch expects")
    src = src.replace(old_body, new_body)

# ------------------------------------------------- 3. numbers become analogs
old_stats = """      <div class="stats">
        <div class="stat"><b>{AR_V}</b><span>Walkthroughs wired</span></div>
        <div class="stat"><b>{AR_S}</b><span>Atlas sites covered</span></div>
        <div class="stat"><b>{share:.0f}%</b><span>Of all Atlas footage</span></div>
      </div>"""
new_stats = ('      <div class="facts">\n'
             + "\n".join(f'        <div class="fact"><span>{k}</span><p>{v}</p></div>'
                         for k, v in ns["FACTS"])
             + "\n      </div>")
if new_stats not in src:
    if old_stats not in src:
        sys.exit("ABORT: the stat tiles are not what this patch expects")
    src = src.replace(old_stats, new_stats)

# ------------------------------------------------------ 4. the table gets bars
old_rows = """        f'<tr{lead}><td><i style="background:{col}"></i>{nm}</td>'
        f'<td class="hnd">{handle}</td><td class="num">{n}</td><td class="num">{len(sites[k])}</td></tr>')"""
new_rows = """        f'<tr{lead}><td><i style="background:{col}"></i>{nm}</td>'
        f'<td class="hnd">{handle}</td>'
        f'<td class="bar"><i style="width:{max(4, round(n / top_n * 100))}%;'
        f'background:linear-gradient(90deg,{col},rgba(232,185,96,.85))"></i></td></tr>')"""
if new_rows not in src:
    if old_rows not in src:
        sys.exit("ABORT: the table row builder is not what this patch expects")
    src = src.replace(old_rows, new_rows)
    src = src.replace("rows = []\nfor k, n in wires.most_common(14):",
                      "rows = []\ntop_n = wires.most_common(1)[0][1]\n"
                      "for k, n in wires.most_common(14):")

old_head = ('<thead><tr><th>Channel</th><th>Handle</th><th class="num">Walkthroughs</th>'
            '<th class="num">Sites</th></tr></thead>')
new_head = ('<thead><tr><th>Channel</th><th>Handle</th>'
            '<th class="barh">Share of the Atlas</th></tr></thead>')
if new_head not in src:
    if old_head not in src:
        sys.exit("ABORT: the table head is not what this patch expects")
    src = src.replace(old_head, new_head)

old_note = """  <p class="note">Counted from the Atlas itself, not from subscriber counts. Ageless Rock carries more of
  the map than any other single channel — {AR_V} walkthroughs against {runner_up[1]} for the next largest.</p>"""
new_note = '  <p class="note">' + ns["TABLE_NOTE"] + "</p>"
if new_note not in src:
    if old_note not in src:
        sys.exit("ABORT: the table note is not what this patch expects")
    src = src.replace(old_note, new_note)

# ---------------------------------------------------------------- 5. Editions
old_ed = """      <p>The Atlas is free and always will be. Editions is what keeps it that way — prints and pieces
      for people who would rather look at this every day than scroll past it.</p>"""
new_ed = "      <p>" + ns["EDITIONS"] + "</p>"
if new_ed not in src:
    if old_ed not in src:
        sys.exit("ABORT: the Editions block is not what this patch expects")
    src = src.replace(old_ed, new_ed)

# ------------------------------------------------- 6. head tags and the footer
src = src.replace(
    'content="Close readings of the channels documenting the ancient world. Study No. 01: '
    'Ageless Rock ' + EM + ' {AR_V} walkthroughs across {AR_S} sites on The Ancient Atlas."',
    'content="Close readings of the channels documenting the ancient world. A site page shows you '
    'a place. A body of work shows you a habit of mind."')
src = src.replace('content="Creator Studies ' + EM + ' The Ancient Atlas"',
                  'content="Creator Studies · The Ancient Atlas"')
src = src.replace(
    'content="Study No. 01: Ageless Rock. {AR_V} narrated studies across {AR_S} sites."',
    'content="Study No. 01: Ageless Rock. Four ways of working stone, traced across one body '
    'of work."')
src = src.replace('<a href="/">The Ancient Atlas</a> ' + EM + ' a hand-curated map of the deep past',
                  '<a href="/">The Ancient Atlas</a>, a hand-curated map of the deep past')

# ------------------------------------------------------------------------ CSS
CSS_ANCHOR = """.stat span{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist)}}"""
CSS_ADD = """
/* Three analogs where three counts used to be. A digital quantity is invisible,
   so it gets rendered at a scale a body understands, and unlike a figure it does
   not go stale as the archive grows. */
.facts{{display:flex;flex-direction:column;gap:0;margin:24px 0 28px;
border-top:1px solid rgba(201,168,76,.16);border-bottom:1px solid rgba(201,168,76,.16)}}
.fact{{display:flex;align-items:baseline;gap:18px;padding:13px 2px}}
.fact + .fact{{border-top:1px solid rgba(201,168,76,.09)}}
.fact span{{font-family:var(--mono);font-size:9.5px;letter-spacing:.17em;text-transform:uppercase;
color:var(--amber);flex:none;width:74px}}
.fact p{{margin:0;font-size:14.5px;line-height:1.5;color:var(--cloud)}}
/* The bar IS the analog. It says "one channel carries most of this" faster than
   a number, and it cannot go stale. */
th.barh{{text-align:left;width:44%}}
td.bar{{padding:11px 10px}}
td.bar i{{display:block;height:5px;border-radius:4px;min-width:6px;
box-shadow:0 0 10px rgba(232,185,96,.16)}}
@media(max-width:640px){{.fact{{flex-direction:column;gap:5px}}.fact span{{width:auto}}}}"""

if ".facts{{display:flex" not in src:
    if CSS_ANCHOR not in src:
        sys.exit("ABORT: the stat CSS anchor is missing")
    src = src.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_ADD)

if src != orig:
    BUILDER.write_text(src)

for marker in ('class="facts"', 'class="fact"', 'class="bar"', "top_n = wires.most_common",
               "habit of mind", "Weeks of evenings"):
    assert marker in src, "missing after patch: " + marker
# Scope the no-counts check to the HTML template, not the whole file. The first
# version of this assert failed on a console print at the bottom of the script,
# which is developer output and never reaches a reader. A check that fires on the
# wrong thing trains you to ignore it.
TQ = chr(39) * 3  # the builder's template delimiter, spelled out so this
                  # line can survive being written by another script
tpl = src.split("html = f" + TQ, 1)[1].rsplit(TQ, 1)[0]
for token in ("{AR_V}", "{AR_S}", "{share", "{TOTAL_V}", "{TOTAL_SITES}", "{runner_up"):
    if token in tpl:
        sys.exit("ABORT: %s still renders into the page" % token)
if EM in tpl:
    for ln in tpl.split("\n"):
        if EM in ln:
            print("  EM DASH:", ln.strip()[:100])
    sys.exit("ABORT: em dashes survive in the rendered page")

print("Creators hub restoried. Counts out of the prose, analogs and bars in.")
