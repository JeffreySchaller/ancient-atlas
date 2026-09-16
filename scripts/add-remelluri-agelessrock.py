#!/usr/bin/env python3
"""
add-remelluri-agelessrock.py — Necropolis of Remelluri (2026-09-16)

What this adds :
- 1 new site : Necropolis of Remelluri (Labastida / Bastida, Rioja Alavesa,
               Álava, Basque Country — roughly 300 graves cut into the bare
               sandstone at the deserted settlement of Remelluri)
- 1 wire     : 4L7w1SlQAoU → Necropolis of Remelluri (primary)
- aux maps   : country Spain, civilization, era 900, tags for search

Source video :
- 4L7w1SlQAoU  "Necropolis of Remelluri in Bastida"
  Ageless Rock (@AgelessRock888), published Sep 16 2026. Creator key
  "agelessrock" already present — this is its 283rd wire.

Why this earns a record : Spain held three sites before this one — Menga,
Tarragona, Naveta des Tudons — and nothing at all within 60 km of the Ebro
in Rioja Alavesa, which is one of the densest rock-cut landscapes in Europe.
Within about 3 km of these graves OSM alone carries two more necropolises,
at least five rock-cut eremitorios, a dozen rock-cut wine presses, two
dolmens and a menhir. The single necropolis is the way in; the landscape is
the reason it matters.

ON THE VIDEO'S PREMISE — recorded here so nobody has to re-derive it. The
description asks how 300 tombs were hewn on bedrock "and we still have no
clue how it got there." That is not the state of the evidence, and this
record does not repeat it. Anthropomorphic (olerdolana) rock-cut graves are
a well documented early-medieval Iberian type, characteristic of the 9th to
11th centuries, east-facing, head to the west; the rectangular and
trapezoidal forms run earlier, 6th to 9th. Remelluri itself is documented
from the 9th century and the necropolis is generally put in the 10th. The
open questions here are real but they are different ones, and the desc
states those instead. Per the standing house rule against overclaiming,
signal is left unset rather than "open".

Coordinates : 42.5992 N, 2.7740 W, the OSM archaeological_site named
Remelluri. Cross-check : Spanish Wikipedia's coordinate for the Remelluri
despoblado is 42.60008/-2.77512, 120 m away, and the result sits 1.8 km
NE of Labastida town centre.

Sites count : 620 → 621. Dedup verified 2026-09-16 : 4L7w1SlQAoU absent
from videos.json; no existing record within 60 km; creator key present.

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py
"""
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}
VALID_SIGNAL = {"open", "convergent", None}

CREATOR_KEY = "agelessrock"

SITE_NAME = "Necropolis of Remelluri"
SITE = {
    "n": SITE_NAME,
    "lat": 42.5992,
    "lng": -2.7740,
    "cat": "tomb",
    "region": "Europe",
    "tier": 3,
    "criteria": ["scale"],
    "desc": (
        "Roughly 300 graves cut into bare sandstone on the slope below the "
        "Sierra de Toloño, at Remelluri — a settlement documented from the "
        "9th century, deserted at an unknown date, now inside the Labastida "
        "municipality in the Rioja Alavesa. The graves are of the "
        "anthropomorphic or olerdolana type : cut 30 to 40 cm into the "
        "exposed rock, shaped to the body they held, heads to the west and "
        "feet to the east. Conventional reading : an early medieval "
        "cemetery of the 10th century beside a hermitage, one node in a "
        "well-studied Iberian tradition that runs from the 9th to the 11th "
        "century across Álava, La Rioja, Burgos and Cantabria, with the "
        "rounded head-niche of the western variant rather than the "
        "right-angled eastern one. That reading is not seriously contested "
        "and this entry does not contest it. What is genuinely open is "
        "everything after the how. The dating rests largely on typology "
        "rather than absolute dates, and the type is broad. The burials are "
        "mostly Christian but Islamic burials were made here too, while the "
        "region belonged to al-Andalus, which is harder to fit to a clean "
        "frontier narrative than the reconquista framing allows. And the "
        "density is the real anomaly : within about 3 km of this outcrop "
        "sit two further rock-cut necropolises, at least five eremitorios "
        "hollowed into the rock, a dozen rupestrian wine presses, two "
        "dolmens and a menhir. A population that cut its graves, its "
        "chapels and its winemaking into living stone, at that "
        "concentration, is a habit of building rather than a single "
        "monument — and the habit is the thing worth explaining."
    ),
}

VIDEO = {
    "id": "4L7w1SlQAoU",
    "title": "Necropolis of Remelluri in Bastida",
    "cr": CREATOR_KEY,
    "added": "2026-09-16",
    "published": "2026-09-16",
}

AUX = {
    "countries.json":     "Spain",
    "civilizations.json": "Early medieval Iberian (Christian, with Islamic burials)",
    "eras.json":          900,
    "tags.json":          "spain basque country euskadi alava rioja alavesa labastida "
                          "bastida remelluri necropolis anthropomorphic olerdolana "
                          "rock-cut graves early medieval",
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
    bad = set(SITE.get("criteria", [])) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")
    if SITE.get("signal") not in VALID_SIGNAL:
        sys.exit(f"ABORT: invalid signal {SITE.get('signal')!r}")

    cats = load("categories.json")
    ck = set(cats.keys()) if isinstance(cats, dict) else {c.get("key") for c in cats}
    if SITE["cat"] not in ck:
        sys.exit(f"ABORT: category {SITE['cat']!r} undefined — it would render as megalithic")

    creators = load("creators.json")
    if CREATOR_KEY not in creators:
        sys.exit(f"ABORT: creator key {CREATOR_KEY!r} not in creators.json")

    sites = load("sites.json")
    before_count = len(sites)
    names = {s["n"] for s in sites}

    # This corner of Rioja Alavesa is thick with near-identical rock-cut
    # necropolises. If one of the neighbours ever lands, catch the collision.
    for s in sites:
        if s["n"] == SITE_NAME:
            continue
        d = math.hypot((s["lat"] - SITE["lat"]) * 111.0,
                       (s["lng"] - SITE["lng"]) * 111.0 * math.cos(math.radians(SITE["lat"])))
        if d < 1.0:
            sys.exit(f"ABORT: {s['n']!r} already sits {d:.2f} km away — resolve before adding")

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

    # ---------------------------------------------------------- wire
    videos = load("videos.json")
    seen = {v.get("id") for rows in videos.values() for v in rows}
    if SITE_NAME not in sites_now:
        sys.exit(f"ABORT: target site {SITE_NAME!r} not found")
    rows = videos.setdefault(SITE_NAME, [])
    if any(v.get("id") == VIDEO["id"] for v in rows):
        print(f"  · Video {VIDEO['id']!r} already wired.")
    elif VIDEO["id"] in seen:
        sys.exit(f"ABORT: {VIDEO['id']!r} is already wired to a different site")
    else:
        rows.append(dict(VIDEO))
        save("videos.json", videos)
        print(f"  ✓ Wired {VIDEO['id']!r} → {SITE_NAME!r}.")

    # ---------------------------------------------------------- pre-flight
    after_count = len(load("sites.json"))
    print(f"\nsites {before_count} → {after_count}")
    if after_count < before_count:
        sys.exit("ABORT: site count dropped")

    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
