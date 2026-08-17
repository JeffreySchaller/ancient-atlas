#!/usr/bin/env python3
"""Say the number once, and give the reader a reason to open the door.

Two problems Jeff caught, and the second is the expensive one.

THE INDEX. The block announced itself twice: a mono kicker reading "Study No. 01"
and then a hundred-pixel serif 01 directly beneath it. The numeral is the better
object, so the kicker loses its visible form and survives as a screen-reader
heading, which keeps the document outline intact without saying the same thing to
the eye twice. The numeral now sits on the same baseline as the name, so it reads
as an index against an entry rather than as a headline of its own. That is also
the shape the page needs when No. 02 arrives.

THE DOORS. "Read the study" and "Browse by place" describe mechanism. Nobody
clicks a mechanism. Worse, they were two identical pills, which says the choice
does not matter, when in fact the choice is the whole point: the same body of
work sorted by argument or sorted by map. That is the Atlas's central move,
offered here in miniature, and it was being thrown away on button labels.

So they become two doors, side by side, each naming what is behind it:

  Follow the argument       What repeats when you stop sorting these places by
                            where they are. Four answers, each with the footage
                            that makes its case.

  Start where you already   Every episode filed by the place it studies rather
  care                      than the day it was posted.

Both payoffs are read off the destination pages rather than invented. And on
whether there needs to be a click at all: yes, but not because of No. 02. The
study pages carry hundreds of thumbnails between them. The hub cannot hold that,
and should not try. Its job is to make the choice legible.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-creators-hub.py"

src = BUILDER.read_text()
orig = src

# ------------------------------------------------------------------ the index
OLD_HEAD = """  <h2>Study No. {STUDY["no"]}</h2>
  <div class="study">
    <div>
      <div class="no">{STUDY["no"]}</div>
      <h3>{STUDY["name"]}</h3>"""
NEW_HEAD = """  <h2 class="sr-only">Study No. {STUDY["no"]}: {STUDY["name"]}</h2>
  <div class="study">
    <div>
      <div class="hd"><span class="no">{STUDY["no"]}</span><h3>{STUDY["name"]}</h3></div>"""
if NEW_HEAD not in src:
    if OLD_HEAD not in src:
        sys.exit("ABORT: the study heading is not what this patch expects")
    src = src.replace(OLD_HEAD, NEW_HEAD)

# ------------------------------------------------------------------ the doors
OLD_BTNS = """      <div class="btns">
        <a class="btn btn-solid" href="/creators/ageless-rock.html">Read the study</a>
        <a class="btn btn-ghost" href="/creators/ageless-rock-by-place.html">Browse by place</a>
      </div>"""
NEW_BTNS = """      <p class="doors-lede">Two ways in</p>
      <div class="doors">
        <a class="door" href="/creators/ageless-rock.html">
          <b>Follow the argument <i>&rarr;</i></b>
          <p>What repeats when you stop sorting these places by where they are. Four answers,
          each with the footage that makes its case.</p></a>
        <a class="door" href="/creators/ageless-rock-by-place.html">
          <b>Start where you already care <i>&rarr;</i></b>
          <p>Every episode filed by the place it studies rather than the day it was posted.
          Begin with a country you know and let it lead you outward.</p></a>
      </div>"""
if NEW_BTNS not in src:
    if OLD_BTNS not in src:
        sys.exit("ABORT: the button row is not what this patch expects")
    src = src.replace(OLD_BTNS, NEW_BTNS)

# ------------------------------------------------------------------------ CSS
NO_OLD = ('.no{{font-family:var(--serif);font-size:clamp(56px,9vw,104px);line-height:.85;'
          'color:var(--stone);font-weight:600}}')
NO_NEW = ('/* An index against an entry, not a headline of its own. Baseline-aligned with\n'
          '   the name so the pair reads as one object. */\n'
          '.hd{{display:flex;align-items:baseline;gap:clamp(12px,1.6vw,20px);flex-wrap:wrap}}\n'
          '.no{{font-family:var(--serif);font-size:clamp(38px,5.4vw,62px);line-height:.9;'
          'color:var(--stone);font-weight:600;flex:none}}\n'
          '.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
          'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}}')
if ".hd{{display:flex" not in src:
    if NO_OLD not in src:
        sys.exit("ABORT: the .no rule is not what this patch expects")
    src = src.replace(NO_OLD, NO_NEW)

BTN_ANCHOR = ".btns{{display:flex;gap:12px;flex-wrap:wrap}}"
DOORS_CSS = """
/* Two doors, not two pills. Identical buttons say the choice does not matter;
   the choice is the point. Each names what is behind it. */
.doors-lede{{font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;
text-transform:uppercase;color:var(--amber);margin:30px 0 11px}}
.doors{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.door{{display:block;text-decoration:none;border:1px solid rgba(201,168,76,.22);
border-radius:12px;padding:15px 16px 14px;background:rgba(201,168,76,.035);
transition:border-color .16s,background .16s,transform .16s}}
.door:hover{{border-color:rgba(201,168,76,.55);background:rgba(201,168,76,.08);
transform:translateY(-2px)}}
.door b{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
color:var(--amber);font-weight:500;line-height:1.35}}
.door b i{{font-style:normal;flex:none;transition:transform .16s}}
.door:hover b i{{transform:translateX(4px)}}
.door p{{margin:9px 0 0;font-size:13.5px;line-height:1.5;color:var(--cloud)}}
@media(max-width:860px){{.doors{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{.door,.door b i{{transition:none}}
.door:hover{{transform:none}}.door:hover b i{{transform:none}}}}"""
if ".doors{{display:grid" not in src:
    if BTN_ANCHOR not in src:
        sys.exit("ABORT: the .btns CSS anchor is missing")
    src = src.replace(BTN_ANCHOR, BTN_ANCHOR + DOORS_CSS)

if src != orig:
    BUILDER.write_text(src)

TQ = chr(39) * 3
tpl = src.split("html = f" + TQ, 1)[1].rsplit(TQ, 1)[0]
assert tpl.count('class="door"') == 2, "expected exactly 2 doors"
assert 'class="sr-only"' in tpl, "the heading lost its accessible form"
assert tpl.count('class="no"') == 1, "the index number should appear once"
assert "Study No. {STUDY[" in tpl, "the h2 no longer identifies the study"
assert "Read the study" not in tpl and "Browse by place" not in tpl, "old labels survive"
for phrase in ("Follow the argument", "Start where you already care",
               "Two ways in", "Four answers"):
    assert phrase in tpl, "missing: " + phrase
if "—" in tpl:
    sys.exit("ABORT: an em dash crept back into the page")

print("Index said once. Two doors, each naming what is behind it.")
