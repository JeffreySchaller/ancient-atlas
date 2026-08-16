#!/usr/bin/env python3
"""Give /patterns/ a way in from the map.

It shipped reachable only from the 23 site pages that carry the criterion,
which is no route at all for anyone who has not already landed deep in the
Atlas. Adds it beside Articles in the desktop stat row and in the mobile
mini-nav, counted the same way everything else there is — from the data.

Desktop tile is deliberately NOT a bordered .stat-experiences tile: that row
already clips at browser zoom, and one more boxed item makes it worse. It
matches the plain Articles/Creators treatment instead.

Idempotent.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"

sites = json.loads((REPO / "data" / "sites.json").read_text())
crit = set()
for s in sites:
    crit.update(s.get("criteria") or [])
N = len(crit)

html = INDEX.read_text()
if 'href="patterns/"' in html:
    print("Already patched - nothing to do.")
    sys.exit(0)

DESK_ANCHOR = '''    <a class="stat-action" href="library/index.html" title="Open the Library — 6 articles on reading deep history">
      <div class="stat-val" id="stat-articles">6</div>
      <div class="stat-lbl">Articles ↗</div>
    </a>'''
DESK_NEW = DESK_ANCHOR + f'''
    <a class="stat-action" href="patterns/" title="Patterns — the same engineering signatures across sites that never met">
      <div class="stat-val">{N}</div>
      <div class="stat-lbl">Patterns ↗</div>
    </a>'''

MOB_ANCHOR = '''    <a class="mf-mininav-link" href="library/index.html">
      <span class="mf-mininav-glyph" aria-hidden="true">6</span>
      <span class="mf-mininav-label">Articles</span>
    </a>'''
MOB_NEW = MOB_ANCHOR + f'''
    <span class="mf-mininav-sep" aria-hidden="true">·</span>
    <a class="mf-mininav-link" href="patterns/">
      <span class="mf-mininav-glyph" aria-hidden="true">{N}</span>
      <span class="mf-mininav-label">Patterns</span>
    </a>'''

edits = 0
for old, new in ((DESK_ANCHOR, DESK_NEW), (MOB_ANCHOR, MOB_NEW)):
    if html.count(old) != 1:
        sys.exit(f"ABORT: expected 1 anchor, found {html.count(old)} — the header markup moved")
    html = html.replace(old, new, 1)
    edits += 1

assert html.count('href="patterns/"') == 2, "expected exactly two entry points"
INDEX.write_text(html)
print(f"{edits} entry point(s) added · Patterns counts {N} criteria")
