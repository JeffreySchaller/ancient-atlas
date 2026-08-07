#!/usr/bin/env python3
"""
add-norba-stoneriddles-batch.py — Norba + Stone Riddles wire batch (2026-08-07)

What this adds :
- 1 new site : Norba (Norma, Latina province, Lazio — Latin colony on the
  Monti Lepini scarp, 2.5+ km polygonal limestone circuit, destroyed 82/81 BCE
  and never reoccupied)
- 1 wire     : 3WyGs5eiEp4 → Norba (primary)
- aux maps   : country Italy, civilization "Latin colony (Roman)", era -492,
               tags for search

Source video :
- 3WyGs5eiEp4  "Norba: the Great Wall of Italy"
  Stone Riddles (@StoneRiddles), published Aug 7 2026

Why this site earns a record rather than a passing mention : Norba is the
control case for the Italian polygonal question. It is one of very few
polygonal circuits sealed at a known year — the town burned rather than
surrender to Sulla at the end of 82 BCE and was never rebuilt — which makes
it the yardstick against which the contested circuits at Orbetello, Alatri
and Cefalù have to be measured. Until now Norba appeared in the dataset only
as a comparison inside the Meydan Kalesi description.

Sites count : 616 → 617. Dedup verified 2026-08-07 : video id 3WyGs5eiEp4
absent from videos.json; no existing Norba site record; creator key
"stoneriddles" already present.

Coordinates : 41.5917 N, 12.9603 E (41°35′30″N 12°57′37″E, Wikipedia geodata).

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}

CREATOR_KEY = "stoneriddles"

SITE_NAME = "Norba"
SITE = {
    "n": SITE_NAME,
    "lat": 41.5917,
    "lng": 12.9603,
    "cat": "city",
    "region": "Europe",
    "tier": 2,
    "signal": "convergent",
    "criteria": ["polygonal", "scale", "geometry"],
    "desc": (
        "Latin colony on the western scarp of the Monti Lepini, southeast of "
        "Rome above the Pontine Plain, its highest point standing at roughly "
        "460 m. More than 2.5 km of mortarless polygonal limestone wall "
        "encloses about 38 hectares, reaching 12 m on the outer face where "
        "the ground falls away. The Porta Maggiore is framed by jambs over "
        "8 m high and 4.3 m wide, with a semicircular bastion still standing "
        "to 13 m; two acropolis platforms carry temple foundations, and the "
        "shrine of Juno Lucina looks west across the plain to the sea. "
        "Norba's value to the polygonal question is its date rather than its "
        "mystery : besieged in the civil war between Marius and Sulla, the "
        "inhabitants burned the town and killed themselves rather than "
        "surrender at the end of 82 BCE, and the site was never reoccupied. "
        "That makes it one of the few polygonal circuits sealed at a known "
        "year, and the natural control against which the contested Italian "
        "circuits at Orbetello, Alatri and Cefalù have to be measured. "
        "Conventional reading : member of the Latin League in 499 BCE, Roman "
        "colony from 492 BCE, the visible fabric assigned to the Roman period "
        "by the excavations begun in 1901. Independent reading : the same "
        "polygonal vocabulary found at the disputed sites appears here inside "
        "a securely dated context, which cuts both ways in the dating debate "
        "and is exactly why the comparison matters. Sparavigna has separately "
        "argued the street grid was laid out on solstitial alignments."
    ),
}

VIDEO = {
    "id": "3WyGs5eiEp4",
    "title": "Norba: the Great Wall of Italy",
    "cr": CREATOR_KEY,
    "added": "2026-08-07",
    "published": "2026-08-07",
}

WIRE_TARGETS = [SITE_NAME]

AUX = {
    "countries.json":     "Italy",
    "civilizations.json": "Latin colony (Roman)",
    "eras.json":          -492,
    "tags.json":          "italy lazio norma polygonal cyclopean lepini sulla latin colony",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  ✓ wrote data/{name}")


def main():
    # ---------------------------------------------------------- guards
    bad = set(SITE["criteria"]) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")

    creators = load("creators.json")
    if CREATOR_KEY not in creators:
        sys.exit(f"ABORT: creator key {CREATOR_KEY!r} not in creators.json")

    sites = load("sites.json")
    before_count = len(sites)
    names = {s["n"] for s in sites}

    # ---------------------------------------------------------- site
    if SITE_NAME in names:
        print(f"  · Site {SITE_NAME!r} already present.")
    else:
        sites.append(dict(SITE))
        save("sites.json", sites)
        print(f"  ✓ Added site {SITE_NAME!r}.")

    sites_now = {s["n"] for s in load("sites.json")}

    # ---------------------------------------------------------- aux maps
    for filename, value in AUX.items():
        m = load(filename)
        if m.get(SITE_NAME) == value:
            print(f"  · {filename}: {SITE_NAME!r} already set.")
            continue
        m[SITE_NAME] = value
        save(filename, m)

    # ---------------------------------------------------------- wires
    videos = load("videos.json")
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

    # ---------------------------------------------------------- pre-flight
    after_count = len(load("sites.json"))
    print(f"\nsites {before_count} → {after_count}")
    if after_count < before_count:
        sys.exit("ABORT: site count dropped")

    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
