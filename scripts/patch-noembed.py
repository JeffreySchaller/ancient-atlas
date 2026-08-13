#!/usr/bin/env python3
"""Route embed-disabled wires to a new tab instead of a dead iframe.

Four wires return 401 from YouTube's oEmbed endpoint - the uploader turned
embedding off. They play fine on YouTube and they are fine on the SEO site
pages (those are thumbnail links), but the map app's playVideo() builds a
youtube.com/embed/ iframe with no fallback, so YouTube serves "Video
unavailable" inside the card.

The app already has exactly the right branch for this: under file:// it
opens the watch URL in a new tab. This flags the four wires with
"noembed": true and widens that branch to cover them.

Re-run scripts/check-dead-wires.py to find new ones; add them to NOEMBED
below and run this again. Idempotent.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = REPO / "data" / "videos.json"
INDEX = REPO / "public" / "index.html"

# id -> the site it is wired to, for the pre-flight check only.
NOEMBED = {
    "6cEUjGnu91s": "Caral",
    "c130haajOJI": "Ōyu Stone Circles",
    "dTW47WWxxoo": "Sahasralinga (Shilmala River)",
    "gbPODG_venM": "Ishi-no-Hoden",
}

# ---------------------------------------------------------------- data
videos = json.loads(VIDEOS.read_text())
found = {vid: [] for vid in NOEMBED}
for site, lst in videos.items():
    for w in lst:
        if w["id"] in found:
            found[w["id"]].append(site)

missing = [v for v, s in found.items() if not s]
if missing:
    sys.exit(f"ABORT: these ids are no longer in videos.json: {missing}")

flagged = 0
for site, lst in videos.items():
    for w in lst:
        if w["id"] in NOEMBED and not w.get("noembed"):
            w["noembed"] = True
            flagged += 1

for vid, sites in found.items():
    for site in sites:
        w = next(x for x in videos[site] if x["id"] == vid)
        assert w.get("noembed") is True, f"{vid} on {site} did not get flagged"

total_flagged = sum(1 for lst in videos.values() for w in lst if w.get("noembed"))
assert total_flagged == sum(len(s) for s in found.values()), \
    "a wire outside the NOEMBED table carries the flag"

if flagged:
    VIDEOS.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- app
html = INDEX.read_text()

HELPER = """// Some uploaders disable embedding (oEmbed answers 401). YouTube serves those
// as "Video unavailable" inside an iframe, so they get routed to a new tab
// exactly the way file:// already is. The flag lives on the wire in
// data/videos.json as "noembed": true; scripts/check-dead-wires.py finds them.
let _noEmbed = null;
function noEmbedIds() {
  if (_noEmbed) return _noEmbed;
  _noEmbed = new Set();
  for (const list of Object.values(typeof VIDEOS === 'object' && VIDEOS ? VIDEOS : {})) {
    for (const w of list) if (w && w.noembed) _noEmbed.add(w.id);
  }
  return _noEmbed;
}

function playVideo(id, title, creatorName, cardEl, ts) {"""

OLD_ANCHOR = "function playVideo(id, title, creatorName, cardEl, ts) {"

OLD_BRANCH = """  // file:// can't embed YouTube iframes — open in new tab instead
  if (isLocal) {"""
NEW_BRANCH = """  // file:// can't embed YouTube iframes, and neither can embed-disabled
  // videos — open both in a new tab instead
  if (isLocal || noEmbedIds().has(id)) {"""

edits = 0
if "function noEmbedIds()" not in html:
    if html.count(OLD_ANCHOR) != 1:
        sys.exit(f"ABORT: expected 1 playVideo definition, found {html.count(OLD_ANCHOR)}")
    html = html.replace(OLD_ANCHOR, HELPER, 1)
    edits += 1

if NEW_BRANCH not in html:
    if html.count(OLD_BRANCH) != 1:
        sys.exit(f"ABORT: expected 1 isLocal branch, found {html.count(OLD_BRANCH)}")
    html = html.replace(OLD_BRANCH, NEW_BRANCH, 1)
    edits += 1

assert "noEmbedIds().has(id)" in html, "the guard did not land"
assert html.count("function playVideo(") == 1, "playVideo was duplicated"
assert html.count("function noEmbedIds()") == 1, "helper was duplicated"

if edits:
    INDEX.write_text(html)

print(f"data: {flagged} wire(s) newly flagged, {total_flagged} carry noembed")
print(f"app : {edits} edit(s) applied to public/index.html")
if not flagged and not edits:
    print("Already patched - nothing to do.")
