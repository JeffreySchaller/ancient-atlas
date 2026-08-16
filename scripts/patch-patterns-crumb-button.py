#!/usr/bin/env python3
"""Make the breadcrumb look like the control it is.

An underline says "link". It does not say "this goes back up a level", and on a
line that is already champagne, uppercase and letterspaced, an underline is the
quietest possible signal. So the crumb becomes a chip: bordered, back-chevron,
faint champagne wash, the same rounded vocabulary as the sibling pills at the
foot of the page. Two controls, one shape language, top and bottom of the page.

The trailing crumbs drop to mist. Standard breadcrumb hierarchy: the part you can
act on carries the accent colour, the part that only tells you where you are
recedes. It also means the chip is the only champagne object on the line other
than the glyph, which is what makes it read as a button without raising its
volume.

The chevron slides 2px left on hover. Small, but it is the difference between a
tag and a door.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-patterns.py"

src = BUILDER.read_text()
orig = src

CHEV = ('<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M6.2 1.4 L2.4 5 L6.2 8.6"/></svg>')

K_OLD = ("<p class=\"kicker\">{glyph(key, 40)}<span><a href=\"/patterns/\">Patterns</a> · "
         "{e(spec['index'])} · {e(spec['name'])}</span></p>")
K_NEW = ("<p class=\"kicker\">{glyph(key, 40)}"
         "<a class=\"crumb\" href=\"/patterns/\">" + CHEV + "<span>Patterns</span></a>"
         "<span class=\"where\">{e(spec['index'])} · {e(spec['name'])}</span></p>")

if K_NEW not in src:
    if K_OLD not in src:
        sys.exit("ABORT: the kicker is not what this patch expects; "
                 "run patch-patterns-way-back.py first")
    src = src.replace(K_OLD, K_NEW)

# The underline rule this replaces
CSS_OLD = (".kicker a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(201,168,76,.38)}\n"
           ".kicker a:hover{color:var(--amber);border-bottom-color:var(--amber)}")
CSS_NEW = """/* The crumb is a control, so it wears the same rounded chip the sibling
   pills wear at the foot of the page. One shape language, both ends. */
.kicker{gap:13px}
.crumb{display:inline-flex;align-items:center;gap:7px;flex:none;
color:var(--champagne);text-decoration:none;border:1px solid var(--stone);
border-radius:999px;padding:6px 13px 6px 11px;background:rgba(201,168,76,.05);
transition:border-color .16s,background .16s,color .16s}
.crumb svg{width:9px;height:9px;flex:none;transition:transform .16s}
.crumb:hover{border-color:rgba(201,168,76,.55);background:rgba(201,168,76,.11);color:var(--amber)}
.crumb:hover svg{transform:translateX(-2px)}
/* Where you are should not compete with where you can go. */
.where{color:var(--mist)}"""

if ".crumb{display:inline-flex" not in src:
    if CSS_OLD not in src:
        sys.exit("ABORT: the kicker link CSS from the previous patch is not present")
    src = src.replace(CSS_OLD, CSS_NEW)

if src != orig:
    BUILDER.write_text(src)

assert 'class="crumb"' in src, "crumb chip missing"
assert 'class="where"' in src, "location span missing"
assert ".crumb:hover svg{transform:translateX(-2px)}" in src, "chevron nudge missing"
assert ".siblings a.all{" in src, "sibling chip vocabulary lost"
assert src.count('href="/patterns/"') >= 6, "lost a route back"

print("Crumb is a chip." if src != orig else "Already current.")
