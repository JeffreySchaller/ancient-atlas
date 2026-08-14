#!/usr/bin/env python3
"""The Studies tile's horizontal padding was never reaching it.

`.stats > div, .stats > a{padding:4px 0}` is a child selector - specificity
(0,1,1) - and the Studies tile is a direct <a> child of .stats. That beats
`.stat-experiences{...padding:6px 15px}` at (0,1,0), so the tile rendered with
ZERO horizontal padding and the label sat on the stroke.

The Experiences tile looked correct the whole time for one reason only: it is
nested inside .fw-wrap, so it is not a direct child of .stats and the override
never applied to it. Measured on the built page at a 2400px viewport:

  Studies      61px wide  = label width, no padding
  Experiences 119px wide  = label width + 30px padding

So this is not "make the number bigger" - 10 -> 15 changed nothing visible.
It needs a selector that actually wins. Scoping to both placements keeps the
two tiles identical wherever they sit.

Idempotent.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"

html = INDEX.read_text()

OLD = (".stat-experiences{position:relative;border-color:rgba(201,168,76,.20);"
       "background:rgba(201,168,76,.05);padding:6px 15px}")
NEW = (".stat-experiences{position:relative;border-color:rgba(201,168,76,.20);"
       "background:rgba(201,168,76,.05)}\n"
       "/* `.stats > div, .stats > a` is (0,1,1) and would otherwise flatten this\n"
       "   to `padding:4px 0`. Scope it so the tile keeps its box whether it sits\n"
       "   directly in .stats (Studies) or inside .fw-wrap (Experiences). */\n"
       ".stats > .stat-experiences,.fw-wrap > .stat-experiences{padding:7px 15px}")

if ".stats > .stat-experiences" in html:
    print("Already patched - nothing to do.")
    sys.exit(0)

if html.count(OLD) != 1:
    sys.exit(f"ABORT: expected 1 occurrence of the tile rule, found {html.count(OLD)}")

html = html.replace(OLD, NEW, 1)

assert html.count(".stats > .stat-experiences") == 1, "scoped rule not unique"
assert html.count("\n.stat-experiences{") == 1, "base rule duplicated"
assert ".stats > div, .stats > a{padding:4px 0}" in html, "the override rule moved"

INDEX.write_text(html)
print("1 edit applied to public/index.html")
