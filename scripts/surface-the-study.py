#!/usr/bin/env python3
"""Put the study one click from the map instead of two.

/creators/ageless-rock is the best long-form thing on the site and it sat two
clicks deep: header tile to the hub, hub to the study. The hover card on that
tile was pointing at the hub as well, so both routes spent a click on an index
page the reader did not ask for.

The split now does real work. The TILE still goes to the hub, because that is the
right destination for someone browsing the series. The CARD'S BUTTON goes
straight to the study, because someone who has paused long enough to read a hover
card has already decided they are interested and should not be made to choose
from a menu of one.

Touches the built page and the builder together, so a rebuild does not undo it.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TARGETS = [REPO / "public" / "index.html", REPO / "scripts" / "add-header-blooms.py"]

STUDY = "/creators/ageless-rock.html"
PAIRS = [
    # built page (entities) and builder source (escaped arrow), same swap
    ('<a class="hb-cta" href="creators/">Open the studies &rarr;</a>',
     f'<a class="hb-cta" href="{STUDY}">Read Study No. 01 &rarr;</a>'),
    ('("Open the studies &rarr;", \'href="creators/"\')',
     f'("Read Study No. 01 &rarr;", \'href="{STUDY}"\')'),
]

touched = []
for path in TARGETS:
    src = path.read_text()
    orig = src
    for old, new in PAIRS:
        if new in src:
            continue
        if old in src:
            src = src.replace(old, new)
    if src != orig:
        path.write_text(src)
        touched.append(path.name)

idx = TARGETS[0].read_text()
bld = TARGETS[1].read_text()
assert f'href="{STUDY}">Read Study No. 01' in idx, "the built page still routes to the hub"
assert f'\'href="{STUDY}"\'' in bld, "the builder still routes to the hub"
assert idx.count('href="creators/"') >= 2, "lost the Creators and Studies hub routes"
assert 'class="stat-action stat-experiences" href="creators/"' in idx or \
       'href="creators/" title="Creator Studies"' in idx, "the Studies tile no longer opens the hub"

print("Studies card now opens the study itself; the tile still opens the hub.")
print("Updated: " + (", ".join(touched) if touched else "nothing, already current"))
