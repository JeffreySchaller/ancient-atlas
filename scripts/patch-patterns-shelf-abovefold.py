#!/usr/bin/env python3
"""Fit all seven patterns above the fold, and say what a click gets you.

Two problems, one layout.

Seven cards in two columns is four scroll-lengths of page. A shelf you have to
scroll is not a shelf, it is a list, and the whole argument of this page is that
you can see the seven signatures at once. Three columns at a 1140px measure puts
all seven in one view on a 1440x900 laptop, which is the machine to design for.

And nothing on a card said what clicking does. "6 studies" is a fact, not a job.
So each card now ends with the verb: "Watch 6 studies ->" in champagne, opposite
the quiet sites-and-countries count in mist. Same split as the crumb chip at the
top of a pattern page: the actionable half carries the accent, the descriptive
half recedes. A reader who scans only the champagne text on this page reads seven
instructions.

The intro drops from five lines to two and now states the job outright. The line
it lost, which was the best line on the page, moves into the eighth grid cell as
a quiet note, so it costs no vertical space at all.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-patterns.py"

src = BUILDER.read_text()
orig = src

# ------------------------------------------------------- card markup: add a verb
CARD_OLD = """        inner = (
            f'<p class="pk">{glyph(k, 34)}<span>{e(spec["index"])} · {e(spec["name"])}</span></p>'
            f'<h3>{e(head)}</h3>'
            f'<p class="pb">{e(blurb)}</p>'
            f'<p class="pm">{len(carriers)} sites · {len(cs)} countries'
            + (f' · {nvid} studies' if nvid else " · no study yet") + "</p>"
        )"""
CARD_NEW = """        go = (f'Watch {nvid} studies <i>→</i>' if nvid else "Not yet written")
        inner = (
            f'<p class="pk">{glyph(k, 34)}<span>{e(spec["index"])} · {e(spec["name"])}</span></p>'
            f'<h3>{e(head)}</h3>'
            f'<p class="pb">{e(blurb)}</p>'
            f'<p class="pfoot"><span class="pm">{len(carriers)} sites · {len(cs)} countries</span>'
            f'<span class="pgo">{go}</span></p>'
        )"""
if CARD_NEW not in src:
    if CARD_OLD not in src:
        sys.exit("ABORT: the index card builder is not what this patch expects")
    src = src.replace(CARD_OLD, CARD_NEW)

# --------------------------------------------- the eighth cell keeps the best line
GRID_OLD = '<div class="pgrid">{"".join(cards)}</div>'
GRID_NEW = ('<div class="pgrid">{"".join(cards)}'
            '<p class="pnote">Sort by country and these never appear together. '
            'Sort by method and you are looking at one idea.</p></div>')
if GRID_NEW not in src:
    if GRID_OLD not in src:
        sys.exit("ABORT: the grid wrapper is not what this patch expects")
    src = src.replace(GRID_OLD, GRID_NEW)

# ------------------------------------------------------------------ intro copy
INTRO_OLD = """  <p class="claim">The Atlas is normally sorted by where things are. This shelf sorts it by how they
were made: seven engineering signatures tracked across 618 sites, each with the studies that
argue it. Sort by country and these never appear together. Sort by method and you are looking
at one idea.</p>"""
INTRO_NEW = """  <p class="claim">Seven engineering signatures, tracked across 618 sites.
Open one to watch the studies that argue it.</p>"""
if INTRO_NEW not in src:
    if INTRO_OLD not in src:
        sys.exit("ABORT: the index intro is not what this patch expects")
    src = src.replace(INTRO_OLD, INTRO_NEW)

# ------------------------------------------------------------------------ CSS
CSS_OLD = """.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}}
.pcard{{display:block;text-decoration:none;color:inherit;border:1px solid var(--stone);
border-radius:12px;padding:19px 20px 17px;background:var(--charcoal);transition:.18s}}
.pcard:hover{{border-color:rgba(201,168,76,.5);transform:translateY(-2px)}}
.pcard.off{{opacity:.5}}"""
CSS_NEW = """/* Three columns at a 1140px measure fits all seven in one view on a 1440x900
   laptop. Two columns made a shelf you had to scroll, which is a list. */
main{{max-width:1140px;padding:30px 22px 70px}}
h1{{font-size:clamp(27px,3.6vw,41px);margin:0 0 11px}}
.claim{{font-size:16px;line-height:1.55;max-width:56ch;margin:0 0 21px}}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:13px}}
.pcard{{display:block;text-decoration:none;color:inherit;border:1px solid var(--stone);
border-radius:12px;padding:15px 17px 13px;background:var(--charcoal);transition:.18s}}
.pcard:hover{{border-color:rgba(201,168,76,.5);transform:translateY(-2px)}}
.pcard.off{{opacity:.5}}
/* The eighth cell. Costs no vertical space and keeps the page's best sentence. */
.pnote{{align-self:center;margin:0;padding:2px 6px;font-size:13px;line-height:1.55;
color:var(--mist);max-width:34ch}}"""
if "main{{max-width:1140px" not in src:
    if CSS_OLD not in src:
        sys.exit("ABORT: the index grid CSS is not what this patch expects")
    src = src.replace(CSS_OLD, CSS_NEW)

# --------------------------------------------------- card internals + the verb
FOOT_OLD = """.pk{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
color:var(--champagne);margin:0 0 12px;display:flex;align-items:center;gap:13px}}
.pcard h3{{font-family:var(--font-serif);font-weight:600;font-size:20px;line-height:1.2;margin:0 0 9px}}
.pb{{font-size:13.5px;line-height:1.5;color:var(--cloud);margin:0 0 12px;
display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;
overflow:hidden;text-overflow:ellipsis}}
.pm{{font-family:var(--font-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);margin:0}}"""
FOOT_NEW = """.pk{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
color:var(--champagne);margin:0 0 9px;display:flex;align-items:center;gap:12px}}
.pcard h3{{font-family:var(--font-serif);font-weight:600;font-size:18.5px;line-height:1.22;
margin:0 0 7px}}
.pb{{font-size:13px;line-height:1.46;color:var(--cloud);margin:0 0 11px;
display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;
overflow:hidden;text-overflow:ellipsis}}
/* "6 studies" is a fact. "Watch 6 studies ->" is the job. The accent goes on the
   half you can act on, the count recedes, and a reader scanning only the
   champagne text down this page reads seven instructions. */
.pfoot{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:0}}
.pm{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);margin:0}}
.pgo{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
color:var(--champagne);white-space:nowrap}}
.pgo i{{font-style:normal;display:inline-block;transition:transform .16s}}
.pcard:hover .pgo{{color:var(--amber)}}
.pcard:hover .pgo i{{transform:translateX(3px)}}"""
if ".pgo{{" not in src:
    if FOOT_OLD not in src:
        sys.exit("ABORT: the card internals CSS is not what this patch expects")
    src = src.replace(FOOT_OLD, FOOT_NEW)

if src != orig:
    BUILDER.write_text(src)

for marker in ('class="pgo"', 'class="pfoot"', 'class="pnote"',
               "main{{max-width:1140px", "minmax(300px,1fr)",
               "-webkit-line-clamp:2", "{glyph(k, 34)}"):
    assert marker in src, f"missing after patch: {marker}"

print("Shelf recut for one view, with the job named on every card."
      if src != orig else "Already current.")
