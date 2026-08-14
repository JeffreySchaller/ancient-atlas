#!/usr/bin/env python3
"""Give the bordered header tiles (Studies, Experiences) room to breathe.

They inherit .stat-action's padding:6px 10px, which is right for the
borderless stats but too tight once a box is drawn around the label - the
text sits almost on the stroke. The NEW badge also straddled the corner.
Widen the horizontal padding and pull the badge clear of the border.

Idempotent.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"

html = INDEX.read_text()

OLD_TILE = (".stat-experiences{position:relative;border-color:rgba(201,168,76,.20);"
            "background:rgba(201,168,76,.05)}")
NEW_TILE = (".stat-experiences{position:relative;border-color:rgba(201,168,76,.20);"
            "background:rgba(201,168,76,.05);padding:6px 15px}")

OLD_BADGE = '.stat-experiences::after{content:"NEW";position:absolute;top:-4px;right:-3px;'
NEW_BADGE = '.stat-experiences::after{content:"NEW";position:absolute;top:-5px;right:-5px;'

edits = 0
for old, new in ((OLD_TILE, NEW_TILE), (OLD_BADGE, NEW_BADGE)):
    if new in html:
        continue
    if html.count(old) != 1:
        sys.exit(f"ABORT: expected 1 occurrence of {old[:48]!r}, found {html.count(old)}")
    html = html.replace(old, new, 1)
    edits += 1

assert html.count("padding:6px 15px}") == 1, "tile padding rule is not unique"
assert html.count(".stat-experiences{") == 1, "tile rule duplicated"
assert html.count('.stat-action stat-experiences"') == 0, "markup was touched"

if edits:
    INDEX.write_text(html)

print(f"{edits} edit(s) applied to public/index.html")
if not edits:
    print("Already patched - nothing to do.")
