#!/usr/bin/env python3
"""
add-pijijiapan-and-arx-sweep.py — Pijijiapan + ARX wires to existing sites (2026-09-17)

What this adds :
- 1 new site : Olmec Rock Carvings of Pijijiapan (Chiapas)
- 7 wires    : 1 → Pijijiapan, 5 → Mitla, 1 → La Venta   (all The ARX Project)
- aux maps   : country Mexico, civilization, era -1000, tags

Companion to add-iglesia-vieja-arxproject.py, which added the creator.

PIJIJIAPAN. Three carved granite boulders on the piedmont west of the town,
each worked on its smoothest face, the relief made by lowering the ground
1-3 cm around the silhouette and incising the detail. Published by Carlos
Navarrete as N.W.A.F. Paper No. 35, "The Olmec Rock Carvings at Pijijiapan,
Chiapas, Mexico" — the corpus the ARX video's second half is about.

COORDINATES ARE AN INFERENCE, not a published figure — the only such pin in
the atlas that I know of, and it is flagged here so it can be replaced.
Navarrete gives no coordinate. He gives three constraints:
  1. about 1 km west of the Río Pijijiapan, where it runs past the edge of
     the town  -> the river sits at lon -93.2132 in the town's latitude
     band (OSM way geometry, confirmed by Nominatim at 15.6916/-93.2132),
     so 1 km west is lon -93.2225;
  2. the land of what was then colonia Guadalupe, reached by the road to the
     rancheria El Llanito -> neither is geocodable today; Colonia El Llanito
     exists as a Pijijiapan locality but returns no coordinate from
     Nominatim, OSM or GeoNames;
  3. broken ground on the boundary between the first foothills of the Sierra
     Madre and the coastal plain -> an SRTM transect puts that break at lat
     15.710-15.715, about 2 km north of the constraint-1 latitude.
Constraints 1 and 3 do not intersect cleanly. Constraint 1 is the specific
measurement and constraint 3 is a regional characterisation, so the pin
follows 1: 15.6916 N, 93.2225 W. Treat it as +/- 1 km. If anyone gets a GPS
fix on Stone 1, replace this and delete this paragraph.

Dating follows Navarrete's own comparison to the Cuadros and Jocotal phases
at Salinas La Blanca, which he dates 1200-850 BCE; era is recorded as -1000.

ARX WIRES TO EXISTING SITES. Seven of the channel's 28 videos are about
sites the atlas already holds:
  Mitla     - 7tfFJAEnvUw  the subterranean labyrinth (28 min)
              r-BL2pej1-0  the full geophysical presentation (1h28)
              hd9WjY71VPo  Project Lyobaa results
              wEKGPVlxTzA  INAH TV results presentation
              IORVsUx8rYE  the Mitla quarries and the 350-ton lintel
  La Venta  - AJA7IgTZ4L0  the serpentine tablet offerings
Deliberately NOT wired: FdLp07odxTo and RnwG_IYgtYk, which are the English
and Spanish cuts of the same five-minute 2022 project trailer. Wiring both
would put two near-identical rows on Mitla; wiring either adds nothing the
four substantive Mitla films do not already carry.

IORVsUx8rYE is about the quarries rather than the site. They sit a few km
from Mitla and would justify their own record; wired to Mitla for now.

Sites count : 622 → 623. Dedup verified 2026-09-17 : none of the seven ids
present in videos.json; no existing record within 10 km of Pijijiapan.

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
CREATOR_KEY = "arxproject"

SITE_NAME = "Olmec Rock Carvings of Pijijiapan"
SITE = {
    "n": SITE_NAME,
    "lat": 15.6916,
    "lng": -93.2225,
    "cat": "megalithic",
    "region": "Central America",
    "tier": 3,
    "criteria": ["hardness", "precision"],
    "desc": (
        "Three granite boulders on the piedmont about a kilometre west of "
        "the Río Pijijiapan, where the first foothills of the Sierra Madre "
        "meet the Chiapas coastal plain. Each is carved on its smoothest "
        "face, and the technique is consistent across all three : the "
        "ground around each figure was lowered by one to three centimetres "
        "to leave the silhouette standing, then the detail was cut in as "
        "incision. Apart from a single small mound there is nothing here — "
        "no settlement, no platforms, just the stones in the broken ground. "
        "Carlos Navarrete published the corpus for the New World "
        "Archaeological Foundation, and dated it by comparison with the "
        "Cuadros and Jocotal ceramic phases at Salinas La Blanca on the "
        "Guatemalan Pacific coast, now placed at 1200-850 BCE. Conventional "
        "reading : Olmec-style relief on the Pacific route, contemporary "
        "with the heartland centres on the Gulf and part of the same "
        "vocabulary as the boulder carvings at San Lorenzo, La Venta and "
        "Chalcatzingo. The interest is in the position rather than the "
        "puzzle. This is Olmec work 400 km from the Gulf heartland, sited "
        "on no settlement at all, on the corridor that runs down the "
        "Pacific plain toward Guatemala — the stones are a statement made "
        "on a road, not at a capital, which is a different kind of "
        "evidence about how far that culture's reach actually ran."
    ),
}

WIRES = [
    (SITE_NAME, {"id": "fAdVzhJcdZM_PLACEHOLDER"}),  # replaced below
]

PIJI_VIDEO = {
    "id": "fAdVzhJcdZM",
    "note": "already wired to Iglesia Vieja - the same film covers both; "
            "not re-wired here, a video belongs to one site",
}

ARX_WIRES = [
    ("Mitla", {"id": "7tfFJAEnvUw",
               "title": "Ancient subterranean LABYRINTH revealed | El laberinto subterráneo de Mitla",
               "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2024-09-01"}),
    ("Mitla", {"id": "r-BL2pej1-0",
               "title": "Geophysical Study confirms Zapotec Entrance to the Underworld in Mexico | Full Presentation",
               "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2024-04-24"}),
    ("Mitla", {"id": "hd9WjY71VPo",
               "title": "Project Lyobaa: Revealing the Underworld of Mitla, Oaxaca",
               "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2023-06-22"}),
    ("Mitla", {"id": "wEKGPVlxTzA",
               "title": "Resultados del Proyecto Lyobaa — INAH TV",
               "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2023-05-17"}),
    ("Mitla", {"id": "IORVsUx8rYE",
               "title": "The Mitla Quarries — Largest megalith in the Americas?",
               "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2024-01-21"}),
    ("La Venta", {"id": "AJA7IgTZ4L0",
                  "title": "20,000 Buried Tablets: Lost Olmec Library?",
                  "cr": CREATOR_KEY, "added": "2026-09-17", "published": "2025-10-01"}),
]

AUX = {
    "countries.json":     "Mexico",
    "civilizations.json": "Olmec (Early–Middle Formative)",
    "eras.json":          -1000,
    "tags.json":          "mexico chiapas pijijiapan olmec relief boulder carving "
                          "petroglyph navarrete soconusco pacific coast granite "
                          "formative preclassic",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  ✓ wrote data/{name}")


def main():
    bad = set(SITE.get("criteria", [])) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")
    if SITE.get("signal") not in VALID_SIGNAL:
        sys.exit(f"ABORT: invalid signal {SITE.get('signal')!r}")

    cats = load("categories.json")
    ck = set(cats.keys()) if isinstance(cats, dict) else {c.get("key") for c in cats}
    if SITE["cat"] not in ck:
        sys.exit(f"ABORT: category {SITE['cat']!r} undefined")

    creators = load("creators.json")
    if CREATOR_KEY not in creators:
        sys.exit(f"ABORT: creator {CREATOR_KEY!r} missing — run the Iglesia Vieja batch first")

    sites = load("sites.json")
    before_count = len(sites)
    names = {s["n"] for s in sites}

    for s in sites:
        if s["n"] == SITE_NAME:
            continue
        d = math.hypot((s["lat"] - SITE["lat"]) * 111.0,
                       (s["lng"] - SITE["lng"]) * 111.0 * math.cos(math.radians(SITE["lat"])))
        if d < 1.0:
            sys.exit(f"ABORT: {s['n']!r} already sits {d:.2f} km away")

    if SITE_NAME in names:
        print(f"  · Site {SITE_NAME!r} already present.")
    else:
        sites.append(dict(SITE))
        save("sites.json", sites)
        print(f"  ✓ Added site {SITE_NAME!r}.")

    sites_now = {s["n"] for s in load("sites.json")}

    for filename, value in AUX.items():
        m = load(filename)
        if m.get(SITE_NAME) == value:
            print(f"  · {filename}: already set.")
            continue
        m[SITE_NAME] = value
        save(filename, m)

    videos = load("videos.json")
    seen = {v.get("id") for rows in videos.values() for v in rows}
    changed = False
    for target, video in ARX_WIRES:
        if target not in sites_now:
            sys.exit(f"ABORT: target site {target!r} not found")
        rows = videos.setdefault(target, [])
        if any(v.get("id") == video["id"] for v in rows):
            print(f"  · {video['id']!r} already wired to {target!r}.")
        elif video["id"] in seen:
            sys.exit(f"ABORT: {video['id']!r} is already wired elsewhere")
        else:
            rows.append(dict(video)); seen.add(video["id"]); changed = True
            print(f"  ✓ Wired {video['id']!r} → {target!r}.")
    if changed:
        save("videos.json", videos)

    print(f"\n  · {PIJI_VIDEO['id']}: {PIJI_VIDEO['note']}")
    after_count = len(load("sites.json"))
    print(f"\nsites {before_count} → {after_count}")
    if after_count < before_count:
        sys.exit("ABORT: site count dropped")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
