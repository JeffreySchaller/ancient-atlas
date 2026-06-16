#!/usr/bin/env python3
"""
add-stecci-batch.py — Croatian Stećci necropolis batch.

What this adds :
- 1 new creator : Institute for Croatian Heritage (small academic channel,
  443 subs as of June 2026, niche Croatian heritage documentaries)
- 1 new site   : Cista Velika Stećci Necropolis (Crljivica field, the largest
  Croatian Stećci site, part of the 2016 UNESCO cross-border listing)
- 1 wire       : MlT_9-Aye_U → Cista Velika

Note : Jeff's second URL (oqfDdgsiHDM) is the Secrets in Stone "Lightning
Pyramid of Ta Keo" video and was already wired to Ta Keo in a prior batch,
so this script does not re-wire it.

Source video :
- MlT_9-Aye_U  "Stećci - Ancient Megalithic Tombstones"
  Institute for Croatian Heritage, published Jan 6 2025
  Production credit : Marko Brkljačić / Institute for Croatian Heritage

Background : Stećci are monumental limestone tombstones carved between the
12th and 16th centuries across what is now Bosnia and Herzegovina, Croatia,
Serbia, and Montenegro. UNESCO inscribed 30 representative graveyards as a
serial cross-border World Heritage Site in 2016. Croatia's listed sites are
Cista Velika (Crljivica field) and Dubravka in Konavle. Cista Velika is the
largest and most-studied Croatian site, with nearly 100 stećci bearing
crosses, vines, kolo dance scenes, hunting reliefs, and weapons.

This script is idempotent — safe to re-run.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

# ---------------------------------------------------------------- creator
CREATOR_KEY = "croatianheritage"
CREATOR = {
    "name": "Institute for Croatian Heritage",
    "handle": "@InstituteForCroatianHeritage",
    "subs": "Croatian heritage documentaries · academic institution · short curated films on Stećci, Gomile, and other regional megalithic + ritual sites",
    "color": "#8B96A0",
    "tier": 3,
}

# ---------------------------------------------------------------- site
SITE_NAME = "Cista Velika Stećci Necropolis"
SITE = {
    "n": SITE_NAME,
    "lat": 43.4751,
    "lng": 16.9923,
    "cat": "tomb",
    "region": "Europe",
    "tier": 2,
    "desc": (
        "Largest Croatian necropolis of stećci — monumental limestone "
        "tombstones carved between the 12th and 16th centuries. The "
        "Crljivica field at Cista Velika contains nearly 100 stones bearing "
        "crosses, vines, hunting scenes, and the kolo dance. Part of the "
        "2016 UNESCO cross-border serial listing of 30 Stećci graveyards "
        "across Croatia, Bosnia and Herzegovina, Serbia, and Montenegro."
    ),
}

COUNTRY = "Croatia"

# ---------------------------------------------------------------- video
VIDEO = {
    "id": "MlT_9-Aye_U",
    "title": "Stećci · Ancient Megalithic Tombstones",
    "cr": CREATOR_KEY,
    "added": "2026-06-15",
    "published": "2025-01-06",
}


def load(name):
    with open(DATA / name) as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    # 1. creators
    creators = load("creators.json")
    if CREATOR_KEY in creators:
        print(f"  · Creator {CREATOR_KEY!r} already exists, leaving as-is.")
    else:
        creators[CREATOR_KEY] = CREATOR
        save("creators.json", creators)
        print(f"  ✓ Added creator {CREATOR_KEY!r}.")

    # 2. site
    sites = load("sites.json")
    existing_names = {s["n"] for s in sites}
    if SITE_NAME in existing_names:
        print(f"  · Site {SITE_NAME!r} already exists, leaving as-is.")
    else:
        sites.append(SITE)
        save("sites.json", sites)
        print(f"  ✓ Added site {SITE_NAME!r}.")

    # 3. country mapping
    countries = load("countries.json")
    if countries.get(SITE_NAME) != COUNTRY:
        countries[SITE_NAME] = COUNTRY
        save("countries.json", countries)
        print(f"  ✓ Mapped {SITE_NAME!r} → {COUNTRY!r}.")
    else:
        print(f"  · Country mapping for {SITE_NAME!r} already correct.")

    # 4. video wire
    videos = load("videos.json")
    wires = videos.get(SITE_NAME, [])
    if any(v["id"] == VIDEO["id"] for v in wires):
        print(f"  · Video {VIDEO['id']!r} already wired to {SITE_NAME!r}.")
    else:
        wires.append(VIDEO)
        videos[SITE_NAME] = wires
        save("videos.json", videos)
        print(f"  ✓ Wired {VIDEO['id']!r} → {SITE_NAME!r}.")

    print("\nNext step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
