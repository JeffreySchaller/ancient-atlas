#!/usr/bin/env python3
"""
fix-region-taxonomy.py — One-shot region taxonomy cleanup (2026-06-09 audit).

AUDIT FINDINGS (559 sites, 13 region values → 10):

    "Americas" (6 sites)    → "Central America"
        Cuicuilco, Xochicalco, Comalcalco, Aké, Izamal Satellite
        Pyramids, Chaltun Ha — the Hugh Newman Mesoamerica triple-batch
        (d7c26b9) introduced this drift. All six are Mexican; their 33
        neighbors (Teotihuacán, Cholula, Templo Mayor, ...) use
        "Central America".
    "Mesoamerica" (1 site)  → "Central America"
        Tula (Tollan) — same conformity fix.
    "Russia" (1 site)       → "Asia"
        Gornaya Shoria Megaliths — Siberia (lng 87.9), belongs with
        the Asia bucket.

DECISION RECORD — "Pacific" stays:
    The handoff flagged Pacific-vs-Oceania as a possible mismatch. The
    audit found all 19 Pacific-basin sites uniformly tagged "Pacific",
    zero sites tagged "Oceania", and the UI region filter derived from
    data (ALL_REGIONS = [...new Set(...)]). "Pacific" is internally
    consistent and is kept as the canonical label. The lone "Oceania"
    string in index.html is a wishlist-dict country key, not region
    taxonomy.

Idempotent. Run from repo root:
    python3 scripts/fix-region-taxonomy.py
    python3 scripts/build.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SITES_PATH = REPO_ROOT / 'data' / 'sites.json'

RETAG = {
    # site name → corrected region
    "Cuicuilco": "Central America",
    "Xochicalco": "Central America",
    "Comalcalco": "Central America",
    "Aké": "Central America",
    "Izamal Satellite Pyramids": "Central America",
    "Chaltun Ha": "Central America",
    "Tula (Tollan)": "Central America",
    "Gornaya Shoria Megaliths": "Asia",
}

CANONICAL_REGIONS = {
    "Asia", "Türkiye", "Europe", "Middle East", "Egypt",
    "South America", "Africa", "Central America", "Pacific",
    "North America",
}


def main():
    with open(SITES_PATH) as f:
        sites = json.load(f)

    before = len(sites)
    changed = 0
    for s in sites:
        target = RETAG.get(s["n"])
        if target and s["region"] != target:
            print(f'  {s["n"]}: "{s["region"]}" → "{target}"')
            s["region"] = target
            changed += 1

    # Validate: every region now canonical, count preserved
    regions = Counter(s["region"] for s in sites)
    stray = set(regions) - CANONICAL_REGIONS
    if stray:
        sys.exit(f"ABORT: non-canonical regions remain: {stray}")
    if len(sites) != before:
        sys.exit("ABORT: site count changed")

    if changed:
        with open(SITES_PATH, 'w') as f:
            json.dump(sites, f, indent=2, ensure_ascii=False)

    print(f"\n{changed} sites retagged. {len(sites)} sites total.")
    print(f"{len(regions)} canonical regions:")
    for r, c in regions.most_common():
        print(f"  {c:4d}  {r}")


if __name__ == "__main__":
    main()
