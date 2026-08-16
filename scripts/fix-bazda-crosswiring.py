#!/usr/bin/env python3
"""Un-wire the Bazda Caves video from four sites it has nothing to do with.

Bernie Ong caught this on the creator study page: the China card's link opened
the Bazda Caves video. The cause is worse than the symptom — 1ZjnsOl2OM8
("Bazda Caves", Türkiye) was wired to FIVE sites in FOUR countries:

    Longyou Caves        China     <- wrong
    Longmen Grottoes     China     <- wrong
    Kotukal Cave Temple  India     <- wrong
    San Andrea Priù      Italy     <- wrong
    Bazda Caves          Türkiye   <- correct, keep

A video legitimately belongs to several sites when it actually covers them
(the Göbekli Tepe / Karahan Tepe walkthroughs, "Yonaguni Monument and the
Plain of Jars"). This is not that: it is a paste that walked. The giveaway is
that the copies disagree about the publish date - 2025-10-19 on the strays,
2025-11-17 on the real one.

Idempotent.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = REPO / "data" / "videos.json"

VID  = "1ZjnsOl2OM8"
KEEP = "Bazda Caves"
STRIP = ["Longyou Caves", "Longmen Grottoes", "Kotukal Cave Temple", "San Andrea Priù"]

videos = json.loads(VIDEOS.read_text())

if KEEP not in videos or not any(w["id"] == VID for w in videos[KEEP]):
    sys.exit(f"ABORT: {VID} is not wired to {KEEP!r} — refusing to strip the copies "
             "when the canonical one is missing")

removed, emptied = [], []
for site in STRIP:
    lst = videos.get(site)
    if not lst:
        continue
    before = len(lst)
    videos[site] = [w for w in lst if w["id"] != VID]
    if len(videos[site]) < before:
        removed.append(site)
    if not videos[site]:
        # A site with no walkthrough is honest. A site with someone else's
        # walkthrough is a lie. Drop the key so the builders treat it as
        # "none yet" rather than rendering an empty section.
        del videos[site]
        emptied.append(site)

still = [s for s, lst in videos.items() if any(w["id"] == VID for w in lst)]
assert still == [KEEP], f"{VID} still wired to {still}"

if removed:
    VIDEOS.write_text(json.dumps(videos, indent=2, ensure_ascii=False) + "\n")

total = sum(len(v) for v in videos.values())
print(f"stripped from {len(removed)} site(s): {removed or 'none — already clean'}")
print(f"{VID} now wired to: {still}")
print(f"{total} wires total")
if emptied:
    print(f"NOTE: now carry no walkthrough at all: {emptied}")
