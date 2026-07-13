#!/usr/bin/env python3
"""
update-creator-tiers-20260713.py — Editorial Picks revisit (Jeff-approved 2026-07-13)

Tier semantics (Creator Hub + homepage sidebar): 1 = Editorial Picks,
2 = Featured Voices, 3 = Emerging & New. Tier 1 also populates the
homepage creator sidebar, so these are high-visibility slots.

Jeff's decisions:
  PROMOTE to Editorial Picks (t1):
    stoneriddles      3→1   66 wires, #3 overall, Mediterranean field surveys
    sorcerersofstone  3→1   30 wires, Camille Sauve, Andean deep dives
  MOVE DOWN to Featured Voices (t2):
    natgeo            1→2   2 wires, institutional — frees a sidebar slot
  TIER-3 TIDY → Featured Voices (t2) (established, not "Emerging & New"):
    agelessrock       3→2   247 wires — largest single source on the atlas
    turkiyetoday      3→2   25 wires
    wanderingwolf     3→2   15 wires
  EXPLICITLY UNCHANGED: ancientatlas t1 (Jeff: keep), randallcarlson t1
  (name-weight over coverage), archaiclens t2.

Idempotent — safe to re-run. Run from repo root, then build.py.
Keys are resolved by handle/name so the script aborts loudly if a key drifts.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

# (identifier, expected-name-substring, new_tier)
CHANGES = [
    ("Stone Riddles", 1),
    ("Sorcerers of Stone", 1),
    ("National Geographic", 2),
    ("Ageless Rock", 2),
    ("Türkiye Today", 2),
    ("Wandering Wolf", 2),
]
MUST_STAY = [("Ancient Atlas", 1), ("Randall Carlson", 1)]


def main():
    path = DATA / "creators.json"
    with open(path, encoding="utf-8") as f:
        creators = json.load(f)

    by_name = {c["name"]: (k, c) for k, c in creators.items()}

    for name, tier in CHANGES:
        if name not in by_name:
            sys.exit(f"ABORT: creator named {name!r} not found")
        key, c = by_name[name]
        if c.get("tier") == tier:
            print(f"  · {name} ({key}) already tier {tier}")
        else:
            print(f"  ✓ {name} ({key}) tier {c.get('tier')} → {tier}")
            c["tier"] = tier

    for name, tier in MUST_STAY:
        key, c = by_name[name]
        if c.get("tier") != tier:
            sys.exit(f"ABORT: {name} expected tier {tier}, found {c.get('tier')}")
        print(f"  · {name} confirmed tier {tier} (unchanged)")

    t1 = sorted(c["name"] for c in creators.values() if c.get("tier") == 1)
    print(f"\nEditorial Picks ({len(t1)}): " + " · ".join(t1))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(creators, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
