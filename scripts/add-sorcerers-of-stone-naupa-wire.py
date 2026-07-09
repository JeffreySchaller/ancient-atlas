#!/usr/bin/env python3
"""
add-sorcerers-of-stone-naupa-wire.py — Sorcerers of Stone + Naupa Huaca wire (2026-07-09)

What this adds :
- 1 new creator : Sorcerers of Stone (@sorcerersofstone — Camille Sauve,
  author of "Sorcerers of Stone: Architects of the Three Ages"; ~2.5K subs
  as of July 2026; Andean precision-stonework deep dives)
- 1 wire        : py2A03eg-q8 → Naupa Huaca (EXISTING site — the video calls
  it Ñaupa Iglesia; same shrine above Pachar, aka Choquequilla)

Source video :
- py2A03eg-q8  "Deep Dive Naupa Iglesia: Ceremony site or Interdimensional
  Portal?"  Sorcerers of Stone, published Jul 1 2026 (2.6K views at add time)
  Chaptered on-site walkthrough: Ukupacha grotto, Kaypacha stairway,
  four-niche temple, blue-andesite portal + musical-ratio acoustics,
  chicana cross, Spanish/dynamite destruction history, geopolymer debate.

Dedup verified 2026-07-09: video id absent; site "Naupa Huaca" present with
3 wires (all brienf — this adds a second creator perspective); no existing
Sorcerers of Stone creator. NO site/aux changes; count stays 560.

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

CREATOR_KEY = "sorcerersofstone"
CREATOR = {
    "name": "Sorcerers of Stone",
    "handle": "@sorcerersofstone",
    "subs": "Camille Sauve · Andean precision-stonework deep dives · author, Sorcerers of Stone",
    "color": "#6B7FB3",
    "tier": 3,
}

SITE_NAME = "Naupa Huaca"
VIDEO = {
    "id": "py2A03eg-q8",
    "title": "Deep Dive Naupa Iglesia: Ceremony Site or Interdimensional Portal?",
    "cr": CREATOR_KEY,
    "added": "2026-07-09",
    "published": "2026-07-01",
}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    sites = load("sites.json")
    before = len(sites)
    if not any(s["n"] == SITE_NAME for s in sites):
        sys.exit(f"ABORT: target site {SITE_NAME!r} not found")

    creators = load("creators.json")
    if CREATOR_KEY in creators:
        print(f"  · Creator {CREATOR_KEY!r} already exists, leaving as-is.")
    else:
        creators[CREATOR_KEY] = CREATOR
        save("creators.json", creators)
        print(f"  ✓ Added creator {CREATOR_KEY!r}.")

    videos = load("videos.json")
    wires = videos.setdefault(SITE_NAME, [])
    if any(v.get("id") == VIDEO["id"] for v in wires):
        print(f"  · Video {VIDEO['id']!r} already wired to {SITE_NAME!r}.")
    else:
        wires.append(VIDEO)
        save("videos.json", videos)
        print(f"  ✓ Wired {VIDEO['id']!r} → {SITE_NAME!r} ({len(wires)} wires).")

    if len(load("sites.json")) != before:
        sys.exit("ABORT: site count changed — this batch must not touch sites")
    print(f"\nsites {before} → {before} (unchanged, floor 560 respected)")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
