#!/usr/bin/env python3
"""
add-mountainbeast-malta-wire.py — Mr.mountainbeast Malta wire (2026-07-11)

- 1 wire : i27bBVWZH7E "The Most Mysterious Island on Earth… What I Found
  Changed Everything." (Mr.mountainbeast, pub 2026-07-10, fresh upload)
  → Malta Cart Ruts (Misraħ Għar il-Kbir) — EXISTING tier-1 signal:open site.
  The video centers on the limestone track network ("cart ruts"), sea caves,
  and a network of unexcavated underground chambers; becomes the site's 3rd
  wire and mountainbeast's 2nd on it (first-person deep-dive vs his earlier
  survey). Dedup verified: id absent; site + creator exist.

Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

SITE = "Malta Cart Ruts (Misraħ Għar il-Kbir)"
VIDEO = {
    "id": "i27bBVWZH7E",
    "title": "The Most Mysterious Island on Earth… What I Found Changed Everything.",
    "cr": "mountainbeast",
    "added": "2026-07-11",
    "published": "2026-07-10",
}


def main():
    with open(DATA / "sites.json", encoding="utf-8") as f:
        sites = json.load(f)
    before = len(sites)
    if not any(s["n"] == SITE for s in sites):
        sys.exit(f"ABORT: site {SITE!r} not found")
    with open(DATA / "creators.json", encoding="utf-8") as f:
        if "mountainbeast" not in json.load(f):
            sys.exit("ABORT: creator 'mountainbeast' missing")
    with open(DATA / "videos.json", encoding="utf-8") as f:
        videos = json.load(f)
    wires = videos.setdefault(SITE, [])
    if any(v.get("id") == VIDEO["id"] for v in wires):
        print(f"  · {VIDEO['id']} already wired")
    else:
        wires.append(VIDEO)
        print(f"  ✓ wired {VIDEO['id']} → {SITE!r} ({len(wires)} wires)")
    with open(DATA / "videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"sites {before} → {before} (unchanged, floor 567)")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
