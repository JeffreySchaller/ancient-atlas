#!/usr/bin/env python3
"""
add-look-closer-hardstone-batch.py — signal:open audit batch (2026-07-09)

Origin: Jeff flagged Sillustani as needing a Look Closer badge, which
triggered a full audit. Two findings:

1. DISPLAY BUG — five flagship sites carried `criteria` but were missing
   `signal:"open"`, and the front-end badge renders only on
   site.signal === 'open' (public/index.html ~L18433/18842). The Great
   Pyramid, Serapeum, Sacsayhuamán, Petra and Derinkuyu have been
   badge-less on the live site. Fixed by adding the signal field.

2. COVERAGE GAPS — 34 sites flagged signal:open under the editorial bar
   plus Jeff's hardness rule (2026-07-09): monoliths/caves worked in stone
   ≥6 on the Mohs scale (granite, basalt, andesite, diorite, quartzite,
   porphyry, dolerite, silcrete) get the badge with a `hardness` criterion.
   Soft-stone monuments (sandstone Abu Simbel, limestone Nemrut, Leshan)
   deliberately stay unflagged — restraint keeps the badge credible.

No site count changes (567). Idempotent — safe to re-run.
Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID = {"precision", "polygonal", "scale", "hardness",
         "stratigraphy", "geometry", "machining"}

# sites with existing criteria but missing signal (bug fix — keep criteria)
SIGNAL_ONLY_FIXES = [
    "Great Pyramid of Giza (Khufu)",
    "Serapeum of Saqqara",
    "Sacsayhuamán",
    "Petra",
    "Derinkuyu Underground City",
]

# name -> criteria (adds signal:open + criteria; does not overwrite existing criteria)
FLAGS = {
    "Sillustani": ["precision", "hardness", "geometry"],
    "Baalbek (Heliopolis)": ["scale", "precision"],
    "Puma Punku": ["precision", "machining", "hardness", "geometry"],
    "Great Sphinx of Giza": ["stratigraphy", "scale"],
    "Ollantaytambo": ["scale", "precision", "polygonal"],
    "Barabar Caves": ["precision", "hardness", "geometry"],
    "Unfinished Obelisk (Aswan)": ["scale", "hardness", "machining"],
    "Colossi of Memnon": ["scale", "hardness"],
    "Aksum Obelisks": ["scale", "hardness"],
    "Tiwanaku": ["precision", "geometry"],
    "Gate of the Sun (Tiwanaku)": ["precision", "hardness"],
    "Nan Madol": ["scale"],
    "Ishi-no-Hoden": ["scale", "geometry", "precision"],
    "Masuda no Iwafune": ["scale", "geometry", "hardness"],
    "Hypogeum of Ħal Saflieni": ["precision", "geometry"],
    "Stonehenge": ["scale", "hardness"],
    "Moai of Easter Island (Rapa Nui)": ["scale"],
    "Plain of Jars": ["scale", "geometry"],
    "Dolmens of the North Caucasus": ["precision", "geometry"],
    "Samaipata (El Fuerte)": ["geometry"],
    "Ellora Caves": ["hardness", "scale", "precision"],
    "Ha'amonga 'a Maui (Tonga Trilithon)": ["scale"],
    "Osaka Castle": ["scale", "hardness"],
    "Mamallapuram": ["hardness", "precision"],
    "Elephanta Caves": ["hardness", "precision"],
    "Ajanta Caves": ["hardness", "scale"],
    "Bhaja Caves": ["hardness", "precision"],
    "Brihadeeswarar Temple (Thanjavur)": ["hardness", "scale"],
    "Vettuvan Koil": ["hardness"],
    "Sakafune-ishi": ["hardness", "geometry"],
    "Kalavantin Durg": ["hardness"],
    "Panoias Sanctuary": ["hardness", "geometry"],
    "Abu Ghorab": ["precision", "hardness"],
    "Pyramid of Menkaure": ["hardness", "precision"],
}


def main():
    with open(DATA / "sites.json", encoding="utf-8") as f:
        sites = json.load(f)
    before = len(sites)
    by_name = {s["n"]: s for s in sites}

    for bad in [n for n in SIGNAL_ONLY_FIXES if n not in by_name] + \
               [n for n in FLAGS if n not in by_name]:
        sys.exit(f"ABORT: site {bad!r} not found")
    for n, crit in FLAGS.items():
        if set(crit) - VALID:
            sys.exit(f"ABORT: invalid criteria on {n!r}")

    fixed = flagged = 0
    for n in SIGNAL_ONLY_FIXES:
        s = by_name[n]
        if s.get("signal") != "open":
            s["signal"] = "open"
            fixed += 1
            print(f"  ✓ BUGFIX signal:open restored on {n!r} (criteria kept: {s.get('criteria')})")
        else:
            print(f"  · {n!r} already has signal")

    for n, crit in FLAGS.items():
        s = by_name[n]
        changed = False
        if s.get("signal") != "open":
            s["signal"] = "open"
            changed = True
        if "criteria" not in s:
            s["criteria"] = crit
            changed = True
        if changed:
            flagged += 1
            print(f"  ✓ flagged {n!r} {s['criteria']}")
        else:
            print(f"  · {n!r} already flagged")

    with open(DATA / "sites.json", "w", encoding="utf-8") as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total_open = sum(1 for s in sites if s.get("signal") == "open")
    print(f"\nsites {before} → {len(sites)} (unchanged) | bugfixes {fixed} | new flags {flagged}")
    print(f"signal:open sites now: {total_open}")
    if len(sites) != before:
        sys.exit("ABORT: count changed")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
