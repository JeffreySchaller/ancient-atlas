#!/usr/bin/env python3
"""Wire the Atlas's own two new films, and stop claiming we filmed none of this.

The Creators hover card read "The Atlas filmed none of this." That was wrong when
it shipped: Ancient Atlas already carried five fieldwork walkthroughs, and it is
listed in the sidebar alongside every other creator. The line was written to make
a point about credit and overshot into a false claim about ourselves. Replaced
with one that makes the same point and is true.

Two films added, both Ancient Atlas, both verified live through YouTube's oEmbed
endpoint rather than typed from the URL:

  7dAYDoCtIAU  "Nobody Has Seen Petrie's Labyrinth Since 1889"
               -> Hawara Pyramid & Labyrinth, which already exists as a site and
               already carries an UnchartedX wire. An unambiguous home.

  2OSddPnrShw  "Why Are There So Many Underground Cities? In Conversation with
               Ageless Rock"
               -> the stratigraphy pattern, per Jeff: the argument is that the
               deeper layers are the older ones, and stratigraphy is the criterion
               where the evidence sits under the building rather than in it.

The interview gets no `sites` list. It is a conversation ranging across several
places and the per-video coverage index is only allowed to claim what has been
checked; guessing would put dots on a minimap that nobody verified.

Idempotent: running twice is a no-op.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = REPO / "data" / "videos.json"
PATTERNS = REPO / "data" / "patterns.json"
CREATORS = REPO / "data" / "creators.json"
ADDED = "2026-08-17"

creators = json.loads(CREATORS.read_text())
if "ancientatlas" not in creators:
    sys.exit("ABORT: no 'ancientatlas' key in creators.json")

# ------------------------------------------------------- 1. the Labyrinth film
videos = json.loads(VIDEOS.read_text())
SITE = "Hawara Pyramid & Labyrinth"
LAB = {
    "id": "7dAYDoCtIAU",
    "title": "Nobody Has Seen Petrie's Labyrinth Since 1889",
    "cr": "ancientatlas",
    "added": ADDED,
}
if SITE not in videos:
    sys.exit(f"ABORT: {SITE!r} is not a site in videos.json")
for s, lst in videos.items():
    if any(w["id"] == LAB["id"] for w in lst) and s != SITE:
        sys.exit(f"ABORT: {LAB['id']} is already wired to {s!r}")

added_wire = False
if not any(w["id"] == LAB["id"] for w in videos[SITE]):
    videos[SITE].append(dict(LAB))
    added_wire = True
assert sum(1 for w in videos[SITE] if w["id"] == LAB["id"]) == 1, "duplicate wire"

# ------------------------------------------------------- 2. the conversation
patterns = json.loads(PATTERNS.read_text())
KEY = "stratigraphy"
CONV = {
    "id": "2OSddPnrShw",
    "title": "Why Are There So Many Underground Cities? In Conversation with Ageless Rock",
    "cr": "ancientatlas",
    "note": "In conversation · what the deeper layers keep turning out to be",
}
if KEY not in patterns:
    sys.exit(f"ABORT: no {KEY!r} pattern")
for k, spec in patterns.items():
    if k.startswith("_"):
        continue
    for w in spec.get("videos", []):
        if w["id"] == CONV["id"] and k != KEY:
            sys.exit(f"ABORT: {CONV['id']} is already on the {k!r} pattern")

added_conv = False
if not any(w["id"] == CONV["id"] for w in patterns[KEY]["videos"]):
    patterns[KEY]["videos"].insert(0, dict(CONV))
    added_conv = True

assert "sites" not in CONV, "the interview must not claim per-site coverage"
for w in patterns[KEY]["videos"]:
    assert w.get("cr") in creators, f"unkeyed creator on {w['id']}"

VIDEOS.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")
PATTERNS.write_text(json.dumps(patterns, indent=2, ensure_ascii=False) + "\n")

own = sum(1 for lst in videos.values() for w in lst if w.get("cr") == "ancientatlas")
print(f"Labyrinth film: {'added to' if added_wire else 'already on'} {SITE}.")
print(f"Conversation: {'added to' if added_conv else 'already on'} /patterns/{KEY}/ "
      f"({len(patterns[KEY]['videos'])} studies).")
print(f"Ancient Atlas now carries {own} wires of its own, which is why the Creators card "
      "no longer says we filmed none of it.")
