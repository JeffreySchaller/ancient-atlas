#!/usr/bin/env python3
"""
cleanup-peru-duplicates-batch.py — Peru duplicate cleanup (2026-07-09)

Found during the Sorcerers of Stone channel sweep. Three duplicate pairs,
each resolved to a single entry keeping the richer content, the common
name, and web-verified coordinates. Wires merged; none lost.

1. "Pisac" + "Pisac (Pisaq)"  →  "Pisac"
   Keeps the (Pisaq) entry's content (tier 1, signal:open, cliff-necropolis
   desc) under the plain name. Wires merged (secretsinstone + brienf).

2. "Aramu Muru" + "Amaru Muru (Stargate)"  →  "Aramu Muru"
   Same doorway near Juli / Lake Titicaca. BOTH old entries had wrong
   coordinates; corrected to -16.1707, -69.5411 (mapcarta/OSM node,
   verified 2026-07-09). Keeps the Stargate entry's richer signal:open
   content; keeps the common spelling. Wire (brienf) moved. Existing aux
   (Peru / -500 / Pre-Inca disputed) already keyed to "Aramu Muru".

3. "Cumbe Mayo" + "Cumbemayo Aqueduct"  →  "Cumbe Mayo"
   Same aqueduct above Cajamarca. Coordinates corrected to
   -7.1897, -78.5739 (Wikipedia, verified 2026-07-09). Keeps the
   Aqueduct entry's richer signal:open desc. Wire (brienf) moved.

DELIBERATE COUNT DECREASE: 560 → 557 (documented; floor updates again
after the companion sorcerers-sweep batch adds 10 sites → 567).

Idempotent — safe to re-run. Run from repo root, then build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

# (keep_name, remove_name, overrides_for_keeper)
MERGES = [
    ("Pisac", "Pisac (Pisaq)", {
        "lat": -13.4144, "lng": -71.8489, "cat": "city", "tier": 1,
        "signal": "open", "criteria": ["polygonal", "precision", "scale"],
        "desc": ("Major Inca site in the Sacred Valley of Peru, 30 km north "
                 "of Cusco, occupying a 6 km mountain ridge above the "
                 "Urubamba river at elevations of 3,000-3,500 meters. The "
                 "site contains the largest pre-Columbian cliff necropolis "
                 "in the Americas (thousands of shaft tombs in the limestone "
                 "cliffs facing the valley), an extensive agricultural "
                 "terrace system still partly in use today, the "
                 "precision-polygonal Intihuatana ceremonial center, and the "
                 "Q'allaqasa fortified district. Two stylistically distinct "
                 "masonry traditions are present : fine Inca andesite ashlar "
                 "above, and a substantially older and more refined "
                 "polygonal substrate at the base of the principal walls."),
    }),
    ("Aramu Muru", "Amaru Muru (Stargate)", {
        "lat": -16.1707, "lng": -69.5411, "cat": "rock-cut", "tier": 2,
        "signal": "open", "criteria": ["precision", "geometry"],
        "desc": ("Carved doorway-shaped niche in a red sandstone outcrop on "
                 "the Hayu Marca plateau near Juli, on the Peruvian shore of "
                 "Lake Titicaca. The 7-meter-wide rectangular frame is cut "
                 "with sharp-edged precision into the bedrock, with a "
                 "smaller doorway at its base. Local Aymara tradition "
                 "describes the niche as the 'Gate of the Gods' through "
                 "which the priest Aramu Muru entered another reality during "
                 "the Spanish conquest. The geometric precision of the cut "
                 "and the absence of any associated structure (steps, walls, "
                 "approach path) place the site in a category by itself. "
                 "Independent investigators including Brien Foerster have "
                 "documented anomalous magnetometer readings at the niche."),
    }),
    ("Cumbe Mayo", "Cumbemayo Aqueduct", {
        "lat": -7.1897, "lng": -78.5739, "cat": "megalithic", "tier": 2,
        "signal": "open", "criteria": ["precision", "geometry", "scale"],
        "desc": ("Pre-Inca stone-cut aqueduct in the highlands above "
                 "Cajamarca, northern Peru, at approximately 3,500 meters "
                 "elevation. The channel is cut into the living volcanic "
                 "bedrock and extends for at least 8 kilometers, with "
                 "right-angle turns, switchbacks, and engineered drops cut "
                 "to maintain a specific gradient. Conventionally dated to "
                 "the Cajamarca culture (c. 1500-1000 BCE) on the basis of "
                 "associated rock-art and pottery, which would make it among "
                 "the oldest stone-engineered hydraulic systems in the "
                 "Americas. The precision of the cuts and the engineering of "
                 "the gradient have led independent investigators to propose "
                 "substantially earlier construction."),
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
    videos = load("videos.json")
    before_sites = len(sites)
    before_wires = sum(len(v) for v in videos.values())

    for keep, remove, overrides in MERGES:
        keeper = next((s for s in sites if s["n"] == keep), None)
        if keeper is None:
            sys.exit(f"ABORT: keeper {keep!r} not found")
        # apply overrides (idempotent)
        changed = False
        for k, v in overrides.items():
            if keeper.get(k) != v:
                keeper[k] = v
                changed = True
        if changed:
            print(f"  ✓ updated content/coords on {keep!r}")
        # remove dupe site
        if any(s["n"] == remove for s in sites):
            sites = [s for s in sites if s["n"] != remove]
            print(f"  ✓ deleted duplicate site {remove!r}")
        # merge wires
        if remove in videos:
            keep_wires = videos.setdefault(keep, [])
            keep_ids = {v.get("id") for v in keep_wires}
            for v in videos[remove]:
                if v.get("id") not in keep_ids:
                    keep_wires.append(v)
                    keep_ids.add(v.get("id"))
                    print(f"  ✓ moved wire {v.get('id')!r} → {keep!r}")
            del videos[remove]
            print(f"  ✓ removed orphan videos key {remove!r}")

    save("sites.json", sites)
    save("videos.json", videos)

    after_wires = sum(len(v) for v in videos.values())
    print(f"\nsites {before_sites} → {len(sites)}")
    print(f"total wires {before_wires} → {after_wires}")
    if after_wires < before_wires:
        sys.exit("ABORT: wires lost in merge")
    if len(sites) < 557:
        sys.exit("ABORT: count below documented floor 557")
    print("Next: sorcerers sweep batch, then build.py")


if __name__ == "__main__":
    sys.exit(main())
