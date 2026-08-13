#!/usr/bin/env python3
"""Replace the dead Stonehenge wire with a live, credited walkthrough.

kBu68hzQ4HI ("Stonehenge Avebury - Walking Through History") 404s on YouTube.
The title is the Channel 4 series "Walking Through History" (Tony Robinson) -
the Stonehenge/Avebury episode is "The Path to Stonehenge" (2014). It was a
broadcast rip on a third-party channel, not a creator walkthrough, and it is
gone. oEmbed returns 404, so the uploading channel is unrecoverable.

Replacement: MegalithomaniaUK's Stonehenge-landscape documentary, verified live
via oEmbed. That creator key already exists, so the wire lands in a real
per-creator total instead of the unkeyed bucket.

Idempotent: running twice is a no-op.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = REPO / "data" / "videos.json"
CREATORS = REPO / "data" / "creators.json"

SITE = "Stonehenge"
DEAD_ID = "kBu68hzQ4HI"
NEW = {
    "id": "YV785pzbE8E",
    "title": "Sonic Temple in the Stonehenge Landscape | Durrington Shafts Mystery | Megalithomania Documentary",
    "cr": "megalithomania",
    "added": "2026-08-13",
}

videos = json.loads(VIDEOS.read_text())
creators = json.loads(CREATORS.read_text())

if NEW["cr"] not in creators:
    sys.exit(f"ABORT: creator key {NEW['cr']!r} is not in creators.json")

wires = videos.get(SITE)
if wires is None:
    sys.exit(f"ABORT: no site {SITE!r} in videos.json")

for site, lst in videos.items():
    if site == SITE:
        continue
    if any(w["id"] == NEW["id"] for w in lst):
        sys.exit(f"ABORT: {NEW['id']} is already wired to {site!r}")

dead_at = [i for i, w in enumerate(wires) if w["id"] == DEAD_ID]
live_at = [i for i, w in enumerate(wires) if w["id"] == NEW["id"]]

if not dead_at and live_at:
    print("Already swapped - nothing to do.")
    sys.exit(0)
if not dead_at:
    sys.exit(f"ABORT: {DEAD_ID} not found on {SITE} and replacement not present")
if live_at:
    sys.exit(f"ABORT: both the dead wire and the replacement are on {SITE}")

before = len(wires)
wires[dead_at[0]] = dict(NEW)

assert len(wires) == before, "wire count changed"
assert not any(w["id"] == DEAD_ID for w in wires), "dead wire survived"
assert sum(1 for w in wires if w["id"] == NEW["id"]) == 1, "replacement not unique"
assert all(w.get("cr") for w in wires), "an unkeyed wire remains on this site"

VIDEOS.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")

total = sum(len(v) for v in videos.values())
unkeyed = sum(1 for v in videos.values() for w in v if not w.get("cr"))
print(f"Swapped {DEAD_ID} -> {NEW['id']} on {SITE} (position {dead_at[0]}).")
print(f"{total} wires total, {unkeyed} still unkeyed.")
