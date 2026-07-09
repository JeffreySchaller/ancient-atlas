#!/usr/bin/env python3
"""
add-bedse-caves-batch.py — Bedse Caves + Liam Richards wire batch (2026-07-09)

What this adds :
- 1 new creator : Liam Richards (@liam.richards, 181K subs as of July 2026,
  travel explorer, first-person walkthroughs; India series)
- 1 new site   : Bedse Caves (Maval taluka, Pune district, Maharashtra —
  Satavahana rock-cut Buddhist chaitya + vihara, ~1st century BCE)
- 2 wires      : ZpYqvukAoLo → Bedse Caves (primary)
                 ZpYqvukAoLo → Barabar Caves (secondary — the video devotes
                 substantial time to Barabar's micron-level "Mauryan polish"
                 precision as the deeper end of the Indian rock-cut question)

Source video :
- ZpYqvukAoLo  "This Ancient Structure Just BROKE My Camera"
  Liam Richards (@liam.richards), published May 21 2026 (102K views July 2026)

Sites count : 562 → 563. Dedup verified 2026-07-09: video id absent from
videos.json; no existing Bedse site; no existing Liam Richards creator.

Coordinates : 18.7244 N, 73.5361 E (trek.zone / Wikipedia geodata, Maval
taluka). Aux mappings mirror Bhaja Caves (country India, civ "Satavahana /
early Buddhist"); era -100 (1st century BCE — Bhaja is -200, Bedse is the
later of the two).

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py (pre-flight count guard included there and here).
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}

# ---------------------------------------------------------------- creator
CREATOR_KEY = "liamrichards"
CREATOR = {
    "name": "Liam Richards",
    "handle": "@liam.richards",
    "subs": "Travel explorer · first-person walkthroughs of overlooked ancient sites",
    "color": "#4FA37C",
    "tier": 2,
}

# ---------------------------------------------------------------- site
SITE_NAME = "Bedse Caves"
SITE = {
    "n": SITE_NAME,
    "lat": 18.7244,
    "lng": 73.5361,
    "cat": "rock-cut",
    "region": "Asia",
    "tier": 2,
    "signal": "open",
    "criteria": ["precision", "scale"],
    "desc": (
        "Rock-cut Buddhist complex carved into hard Deccan basalt in the "
        "Western Ghats of Maharashtra, dated to the Satavahana period around "
        "the 1st century BCE. The apsidal chaitya hall sits behind an "
        "entrance screen of tall columns with animal-and-rider capitals; "
        "inside, plain octagonal columns lean slightly inward — a rake "
        "inherited from the wooden architecture the form reproduces. The "
        "enclosed hall sustains a strong low-frequency vocal resonance "
        "(walkthrough footage documents chanting reinforced near 110 Hz), "
        "inviting comparison with other rock-cut chanting chambers. "
        "Institutional archaeology places Bedse within the hand-carved "
        "chaitya tradition between Bhaja and Karla; the open question is how "
        "consistently smooth interior geometry was achieved in basalt with "
        "the documented iron toolkit — a gentler cousin of the precision "
        "debate at Barabar's mirror-polished granite chambers."
    ),
}

COUNTRY = "India"
ERA = -100
CIV = "Satavahana / early Buddhist"

# ---------------------------------------------------------------- wires
VIDEO = {
    "id": "ZpYqvukAoLo",
    "title": "This Ancient Structure Just BROKE My Camera",
    "cr": CREATOR_KEY,
    "added": "2026-07-09",
    "published": "2026-05-21",
}
WIRE_TARGETS = [SITE_NAME, "Barabar Caves"]


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    bad = set(SITE["criteria"]) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")

    sites = load("sites.json")
    before_count = len(sites)

    # 1. creator (idempotent)
    creators = load("creators.json")
    if CREATOR_KEY in creators:
        print(f"  · Creator {CREATOR_KEY!r} already exists, leaving as-is.")
    else:
        creators[CREATOR_KEY] = CREATOR
        save("creators.json", creators)
        print(f"  ✓ Added creator {CREATOR_KEY!r}.")

    # 2. site (idempotent by name)
    if SITE_NAME in {s["n"] for s in sites}:
        print(f"  · Site {SITE_NAME!r} already exists, leaving as-is.")
    else:
        sites.append(SITE)
        save("sites.json", sites)
        print(f"  ✓ Added site {SITE_NAME!r}.")

    # 3. aux mappings (idempotent)
    for fname, key, value in (("countries.json", SITE_NAME, COUNTRY),
                              ("eras.json", SITE_NAME, ERA),
                              ("civilizations.json", SITE_NAME, CIV)):
        obj = load(fname)
        if obj.get(key) != value:
            obj[key] = value
            save(fname, obj)
            print(f"  ✓ {fname}: {key!r} → {value!r}")
        else:
            print(f"  · {fname}: {key!r} already correct.")

    # 4. wires (idempotent by video id within each site's list)
    videos = load("videos.json")
    sites_now = {s["n"] for s in load("sites.json")}
    changed = False
    for target in WIRE_TARGETS:
        if target not in sites_now:
            sys.exit(f"ABORT: target site {target!r} not found")
        wires = videos.setdefault(target, [])
        if any(v.get("id") == VIDEO["id"] for v in wires):
            print(f"  · Video {VIDEO['id']!r} already wired to {target!r}.")
        else:
            wires.append(dict(VIDEO))
            changed = True
            print(f"  ✓ Wired {VIDEO['id']!r} → {target!r}.")
    if changed:
        save("videos.json", videos)

    # pre-flight guard
    after_count = len(load("sites.json"))
    print(f"\nsites {before_count} → {after_count}")
    if after_count < before_count:
        sys.exit("ABORT: site count dropped")

    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
