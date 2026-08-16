#!/usr/bin/env python3
"""Give a pattern page a way back up to the shelf.

/patterns/hardness/ had no route to /patterns/. The header nav listed Atlas,
Library, Studies and Sites but not the section you were standing in, and the
only sibling links sat below three long sections, past the full country index.
A reader who arrived from a shared card had no way to discover that six more
patterns existed without editing the URL.

Four routes added, cheapest first, because different readers reach for different
ones:

  1. The kicker's own word. "Patterns · No. 06 · Hardness" now has "Patterns"
     as a link. It already reads as a breadcrumb, so it should behave like one,
     and it sits where the eye lands before the headline.
  2. Header nav. Patterns joins Atlas / Library / Studies / Sites on every page
     in the section, marked as current on the index itself.
  3. A champagne "All seven patterns" chip leading the sibling row, so the one
     link that goes up is not styled identically to the six that go sideways.
  4. The footer link row.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-patterns.py"

src = BUILDER.read_text()
orig = src

# ------------------------------------------------------------------ header nav
NAV_OLD = ('<nav><a href="/">Atlas</a><a href="/library/">Library</a>'
           '<a href="/creators/">Studies</a><a href="/sites/">Sites</a></nav>')
NAV_PAGE = ('<nav><a href="/">Atlas</a><a href="/library/">Library</a>'
            '<a href="/patterns/">Patterns</a>'
            '<a href="/creators/">Studies</a><a href="/sites/">Sites</a></nav>')
NAV_INDEX = ('<nav><a href="/">Atlas</a><a href="/library/">Library</a>'
             '<a class="here" href="/patterns/" aria-current="page">Patterns</a>'
             '<a href="/creators/">Studies</a><a href="/sites/">Sites</a></nav>')

if NAV_PAGE not in src and NAV_INDEX not in src:
    if src.count(NAV_OLD) != 2:
        sys.exit(f"ABORT: expected 2 identical navs, found {src.count(NAV_OLD)}")
    # build() precedes build_index() in the file, so first occurrence is the
    # pattern page and second is the shelf's own index.
    src = src.replace(NAV_OLD, NAV_PAGE, 1)
    src = src.replace(NAV_OLD, NAV_INDEX, 1)

# ------------------------------------------------------------- kicker as a crumb
K_OLD = ("<p class=\"kicker\">{glyph(key, 40)}<span>Patterns · "
         "{e(spec['index'])} · {e(spec['name'])}</span></p>")
K_NEW = ("<p class=\"kicker\">{glyph(key, 40)}<span><a href=\"/patterns/\">Patterns</a> · "
         "{e(spec['index'])} · {e(spec['name'])}</span></p>")
if K_NEW not in src:
    if K_OLD not in src:
        sys.exit("ABORT: the pattern page kicker is not what this patch expects")
    src = src.replace(K_OLD, K_NEW)

# ------------------------------------------------------- "all seven" chip first
S_OLD = '<div class="siblings">{sibs}</div>'
S_NEW = ('<div class="siblings"><a class="all" href="/patterns/">All seven patterns</a>{sibs}</div>')
if S_NEW not in src:
    if S_OLD not in src:
        sys.exit("ABORT: the siblings row is not what this patch expects")
    src = src.replace(S_OLD, S_NEW)

# ------------------------------------------------------------------- footer row
F_OLD = ('<a href="/">Map</a> · <a href="/library/">Library</a> · '
         '<a href="/creators/">Creator Studies</a> ·')
F_NEW = ('<a href="/">Map</a> · <a href="/library/">Library</a> · '
         '<a href="/patterns/">Patterns</a> · <a href="/creators/">Creator Studies</a> ·')
if F_NEW not in src:
    if src.count(F_OLD) != 2:
        sys.exit(f"ABORT: expected 2 footer rows, found {src.count(F_OLD)}")
    src = src.replace(F_OLD, F_NEW)

# ------------------------------------------------------------------------- CSS
CSS_ANCHOR = ".siblings a.off{opacity:.42;pointer-events:none}"
CSS_ADD = """
/* The one link in this row that goes UP should not look like the six that go
   sideways. */
.siblings a.all{border-color:rgba(201,168,76,.45);color:var(--champagne)}
.siblings a.all:hover{border-color:var(--champagne);background:rgba(201,168,76,.08);
color:var(--ivory)}
/* The kicker already reads as a breadcrumb; this makes it behave like one. */
.kicker a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(201,168,76,.38)}
.kicker a:hover{color:var(--amber);border-bottom-color:var(--amber)}
header nav a.here{color:var(--champagne)}"""

if CSS_ADD.strip().splitlines()[-1] not in src:
    if CSS_ANCHOR not in src:
        sys.exit("ABORT: the siblings CSS block has moved")
    src = src.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_ADD)

if src != orig:
    BUILDER.write_text(src)

assert src.count('href="/patterns/"') >= 6, "not enough routes back"
assert 'class="here"' in src, "index nav not marked current"
assert src.count(NAV_PAGE) == 1 and src.count(NAV_INDEX) == 1, "nav variants wrong"
assert "All seven patterns" in src, "chip missing"
assert "header nav a.here" in src, "current-page style missing"

print("Four routes back to /patterns/ wired."
      if src != orig else "Already current.")
