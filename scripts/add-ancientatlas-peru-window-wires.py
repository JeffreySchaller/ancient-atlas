#!/usr/bin/env python3
"""
add-ancientatlas-peru-window-wires.py — first-party wires that premiered
during the Peru trip (2026-07-09 catch-up)

Channel audit of @AncientAtlasMap (6 public long-form videos): Ep01-03 were
already wired; Ep04 and Ep06 premiered while the team was in Peru and were
never wired. This adds:

- WqmEgFcN9s0  Ep04 "Serapeum of Saqqara with UnchartedX"  → Serapeum of Saqqara
- wpywqa71YRY  Ep06 "Step Pyramid of Saqqara with UnchartedX" → Step Pyramid of Djoser

SKIPPED deliberately: ecy2Lu_euOY (Grand Egyptian Museum · Museum
Walkthrough) — a modern museum building has no atlas site under current
editorial (ancient sites only). Revisit if a museums layer ever ships.
Ep05 is not yet public; wire it when it premieres.

Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

WIRES = [
    ("Serapeum of Saqqara", {
        "id": "WqmEgFcN9s0",
        "title": "Serapeum of Saqqara with UnchartedX | Fieldwork Walkthrough · Egypt",
        "cr": "ancientatlas",
        "added": "2026-07-09",
    }),
    ("Step Pyramid of Djoser", {
        "id": "wpywqa71YRY",
        "title": "Step Pyramid of Saqqara with UnchartedX | Fieldwork Walkthrough · Egypt",
        "cr": "ancientatlas",
        "added": "2026-07-09",
    }),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    sites = load("sites.json")
    creators = load("creators.json")
    videos = load("videos.json")
    if "ancientatlas" not in creators:
        sys.exit("ABORT: creator 'ancientatlas' missing")
    names = {s["n"] for s in sites}
    before = len(sites)

    for site_name, vid in WIRES:
        if site_name not in names:
            sys.exit(f"ABORT: site {site_name!r} not found")
        wires = videos.setdefault(site_name, [])
        if any(v.get("id") == vid["id"] for v in wires):
            print(f"  · {vid['id']} already wired to {site_name!r}")
        else:
            wires.append(vid)
            print(f"  ✓ wired {vid['id']} → {site_name!r} ({len(wires)} wires)")

    save("videos.json", videos)
    if len(load("sites.json")) != before:
        sys.exit("ABORT: site count changed")
    print(f"\nsites {before} → {before} (unchanged, floor 567)")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
