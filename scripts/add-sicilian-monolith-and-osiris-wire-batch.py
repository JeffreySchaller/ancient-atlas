#!/usr/bin/env python3
"""
Batch: Sicilian Channel monolith + Osiris Shaft first-party wire (2026-06-13)

Two operations, both idempotent (safe to re-run):

1. Osiris Shaft (Giza) — existing site — gets a first-party fieldwork wire
   to EP03 (Ancient Atlas channel, "with UnchartedX"). Mirrors the
   Derinkuyu / Osireion pattern (cr = ancientatlas).

2. Pantelleria Vecchia Bank Monolith — NEW signal:open site in the Sicilian
   Channel — plus a NEW creator (MegalithHunter) and a wire to that creator's
   video. Description pairs the anthropogenic case (Lodolo & Ben-Avraham 2015)
   against the natural-origin case (Tusa; Galili et al. 2024), per the
   signal:open dual-perspective editorial rule.

Reads and writes data/*.json only. Run from repo root, then build.py.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def save(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---- new creator -----------------------------------------------------------
NEW_CREATOR_KEY = "megalithhunter"
NEW_CREATOR = {
    "name": "MegalithHunter",
    "handle": "@megalithhunter",
    "subs": "Megalithic field research · weighs the anthropogenic and natural cases",
    "color": "#6B8E9C",
    "tier": 2,
}

# ---- new site --------------------------------------------------------------
NEW_SITE = {
    "n": "Pantelleria Vecchia Bank Monolith",
    "lat": 37.1,
    "lng": 11.98,
    "cat": "megalithic",
    "region": "Europe",
    "tier": 3,
    "signal": "open",
    "criteria": ["scale", "geometry", "machining"],
    "desc": (
        "A 12-metre limestone block resting at a depth of about 40 metres on "
        "the Pantelleria Vecchia Bank in the Sicilian Channel, roughly 60 km "
        "south of Sicily. During the Last Glacial Maximum this bank stood "
        "above water as part of a land bridge toward Sicily; rising seas "
        "submerged it around 9,300 years ago. In 2015 marine geologists "
        "Emanuele Lodolo and Zvi Ben-Avraham reported the block as "
        "human-modified — citing its regular elongated shape and three "
        "similar circular holes, one passing entirely through the stone — and "
        "proposed it was quarried from a nearby ridge and stood upright as a "
        "menhir before the area drowned. Archaeologist Sebastiano Tusa "
        "challenged that reading the same year, and a 2024 study (Galili et "
        "al., Journal of Marine Science and Engineering) argued for a natural "
        "origin: beachrock detached and displaced by coastal erosion and "
        "storms, with the holes formed by bioerosion and weathering. No "
        "artifacts have been recovered from the surrounding seabed, so the "
        "case currently rests on the shapes of the features themselves. The "
        "debate over whether Mesolithic people raised it remains unresolved."
    ),
}

# ---- video wires -----------------------------------------------------------
# (site name) -> video object
WIRES = [
    (
        "Osiris Shaft (Giza)",
        {
            "id": "T5T3ty0-jbs",
            "title": "Osiris Shaft with UnchartedX | Fieldwork Walkthrough · Egypt",
            "cr": "ancientatlas",
            "added": "2026-06-13",
            "published": "2026-06-13",
        },
    ),
    (
        "Pantelleria Vecchia Bank Monolith",
        {
            "id": "iAkmucsp4rY",
            "title": "Submerged Monolith · Sicilian Channel",
            "cr": "megalithhunter",
            "added": "2026-06-13",
            "published": "2026-06-13",
        },
    ),
]


def main():
    sites = load("sites.json")
    creators = load("creators.json")
    videos = load("videos.json")

    before = (len(sites), len(creators), sum(len(v) for v in videos.values()))

    # validate new site criteria
    bad = set(NEW_SITE["criteria"]) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")

    # 1. creator (idempotent)
    if NEW_CREATOR_KEY not in creators:
        creators[NEW_CREATOR_KEY] = NEW_CREATOR
        print(f"  + creator: {NEW_CREATOR_KEY}")
    else:
        print(f"  = creator {NEW_CREATOR_KEY} already present, skipped")

    # 2. site (idempotent by name)
    site_names = {s["n"] for s in sites}
    if NEW_SITE["n"] not in site_names:
        sites.append(NEW_SITE)
        print(f"  + site: {NEW_SITE['n']}")
    else:
        print(f"  = site {NEW_SITE['n']!r} already present, skipped")

    # 3. wires (idempotent by video id within the site's list)
    for site_name, vid in WIRES:
        if not any(s["n"] == site_name for s in sites):
            sys.exit(f"ABORT: target site {site_name!r} not found")
        lst = videos.setdefault(site_name, [])
        if any(v.get("id") == vid["id"] for v in lst):
            print(f"  = wire {vid['id']} -> {site_name!r} already present, skipped")
        else:
            lst.append(vid)
            print(f"  + wire {vid['id']} ({vid['cr']}) -> {site_name!r}")

    save("sites.json", sites)
    save("creators.json", creators)
    save("videos.json", videos)

    after = (len(sites), len(creators), sum(len(v) for v in videos.values()))
    print(f"\nsites   {before[0]} -> {after[0]}")
    print(f"creators {before[1]} -> {after[1]}")
    print(f"walkthroughs {before[2]} -> {after[2]}")
    if after[0] < before[0] or after[1] < before[1]:
        sys.exit("ABORT: counts dropped")


if __name__ == "__main__":
    main()
