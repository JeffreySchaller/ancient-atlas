#!/usr/bin/env python3
"""
add-iglesia-vieja-arxproject.py — Iglesia Vieja + The ARX Project (2026-09-17)

What this adds :
- 1 new site    : Iglesia Vieja (Tonalá, Chiapas — the Zoque regional capital
                  on the Cerro de la Cruz, 60+ ha of granite architecture)
- 1 new creator : arxproject (The ARX Project, @arxprojectmx)
- 1 wire        : fAdVzhJcdZM → Iglesia Vieja (primary)
- aux maps      : country Mexico, civilization, era -300, tags for search

Source video :
- fAdVzhJcdZM  "HUGE MEGALITHIC RUINS DISCOVERED in southern Mexico |
                Las misteriosas ruinas de Tonalá, Chiapas"
  The ARX Project (@arxprojectmx), published Jul 27 2025. Title stored
  verbatim; the "750" in the supplied filename is a download artefact and is
  not part of it.

Why this earns a record : the atlas held 28 sites in Mexico and every one of
them north of 16.9 — the whole Pacific slope of Chiapas, and with it the
entire Zoque archaeological province, was missing. Iglesia Vieja is its
capital: 60-plus hectares, 73 registered principal structures in five
architectural groups, an estimated 10,000 people at its height, and
according to its own excavators "a clear example of an entirely eclectic
architectural creation that breaks with the conventional urban model
established theoretically for the Late Preclassic in Mesoamerica". It is
also the atlas's first Zoque site and now its southernmost Mexican one.

ON THE VIDEO'S PREMISE. The description asks who built these platforms and
proposes "a civilization even older than the Maya, with possible ties with
the Andes of South America". Two different claims, and they do not fare the
same way. The builders are not unknown — this is the Zoque, Mixe-Zoquean
speakers, with a ceramic sequence (Doloritas differential-firing black,
Pichito polished black) that archaeologically defines their territory, and a
literature running from Seler-Sachs in 1900 through Ferdon's 1953 survey to
the INAH seasons from 2003. "Older than the Maya" does have a defensible
kernel and the desc says so plainly: the monumental project on the hill
begins in the Late Preclassic, centuries before the Classic Maya cities, and
Mixe-Zoquean is the leading candidate for the language of the Olmec. The
Andean tie has no evidence behind it and is not repeated here. Per the house
rule, signal is left unset rather than "open".

Tonnage : the video says blocks up to 8 tons. Not stated in the sources
consulted, so the desc says "megalithic slabs", which INAH's own phrasing
supports, and gives no figure.

Coordinates : 16.1313 N, 93.7472 W, the OSM archaeological_site polygon
"Zona arqueológica de Iglesia Vieja". es.wikipedia's decimal coordinate
agrees to 250 m — well inside a site 60 ha across — and the result sits
4.5 km north of Tonalá centre against the article's own "4 km al norte".
NOT corroborated by the UTM string in that article (419800 E, 177800 N);
that northing is short a digit, and even restored it falls 5.4 km south,
essentially on the modern town. Discarded rather than reconciled.

Sites count : 621 → 622. Dedup verified 2026-09-17 : fAdVzhJcdZM absent
from videos.json; no existing record within 120 km; creator key absent.

Not added : the Pijijiapan carvings, the video's secondary subject. They
are a separate site and their coordinates were not verified here.

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

NEW_CREATOR_KEY = "arxproject"
NEW_CREATOR = {
    "name": "The ARX Project",
    "handle": "@arxprojectmx",
    "subs": "Mesoamerican origins · bilingual field investigations across Mexico",
    # Vestigial: toneCreators() recomputes .color at runtime from the
    # creator's share of the atlas. Kept to match the shape of the other 96.
    "color": "#6E8C7A",
    "tier": 3,
}

SITE_NAME = "Iglesia Vieja"
SITE = {
    "n": SITE_NAME,
    "lat": 16.1313,
    "lng": -93.7472,
    "cat": "city",
    "region": "Central America",
    "tier": 3,
    "criteria": ["scale", "hardness"],
    "desc": (
        "Granite city on the Cerro de la Cruz at 700 m, 4.5 km north of "
        "Tonalá where the Sierra Madre de Chiapas drops to the Pacific "
        "plain. More than 60 hectares, 73 registered principal structures "
        "in five architectural groups, perhaps 10,000 people at its height, "
        "and unsurveyed ground still running a kilometre further south. "
        "Building material is the hill itself : granite cut as long thin "
        "slabs, as squared lajas dressed on one face with the natural tail "
        "left rounded, and as large blocks, with a thick red clay render "
        "binding the rougher walling. No two structures on the site are "
        "alike, the plazas are levelled with sand fill across four "
        "topographic levels, and two petroglyphs appear to be scale plans "
        "of buildings, avenues and water sources. From the edge of the "
        "Plaza del Sacrificio the town of Tonalá is clearly audible 4 km "
        "below, though not the reverse. Conventional reading : the Pacific "
        "coastal capital of the Zoque, Mixe-Zoquean speakers whose "
        "territory the black-ware sequence defines archaeologically; the "
        "monumental project begins in the Late Preclassic around 300 BCE, "
        "the megalithic slab facing goes on in the Early Classic over two "
        "earlier substructures, and radiocarbon puts the decline at 350-450 "
        "CE, after which power moves to Los Horcones. That reading is "
        "well founded and this entry does not dispute it. What is striking "
        "is that the site's own excavators call it an entirely eclectic "
        "creation that breaks the urban model theory had established for "
        "the Late Preclassic in Mesoamerica — the anomaly is in the "
        "literature, not outside it. Two further things are true and worth "
        "holding together : the hill was monumental centuries before the "
        "Classic Maya cities, and Mixe-Zoquean is the leading candidate for "
        "the language of the Olmec, which puts the builders close to the "
        "root of Mesoamerican civilisation rather than at its margin. The "
        "jaguar face carved into a natural boulder at the south end of the "
        "plaza, broken by fire, is described as post-Olmec. The site was "
        "surveyed by Ferdon in 1937 and 1949, then left alone for forty "
        "years for want of a road, and looted throughout; INAH bought six "
        "hectares of it in 2003."
    ),
}

VIDEO = {
    "id": "fAdVzhJcdZM",
    "title": "HUGE MEGALITHIC RUINS DISCOVERED in southern Mexico | "
             "Las misteriosas ruinas de Tonalá, Chiapas",
    "cr": NEW_CREATOR_KEY,
    "added": "2026-09-17",
    "published": "2025-07-27",
}

AUX = {
    "countries.json":     "Mexico",
    "civilizations.json": "Zoque (Mixe-Zoquean)",
    "eras.json":          -300,
    "tags.json":          "mexico chiapas tonala iglesia vieja zoque mixe-zoquean "
                          "olmec pacific coast sierra madre granite cyclopean "
                          "preclassic early classic los horcones inah",
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

    sites = load("sites.json")
    regions = {s["region"] for s in sites}
    if SITE["region"] not in regions:
        sys.exit(f"ABORT: region {SITE['region']!r} is not one the atlas already uses")

    before_count = len(sites)
    names = {s["n"] for s in sites}

    for s in sites:
        if s["n"] == SITE_NAME:
            continue
        d = math.hypot((s["lat"] - SITE["lat"]) * 111.0,
                       (s["lng"] - SITE["lng"]) * 111.0 * math.cos(math.radians(SITE["lat"])))
        if d < 1.0:
            sys.exit(f"ABORT: {s['n']!r} already sits {d:.2f} km away — resolve before adding")

    # ---------------------------------------------------------- creator
    creators = load("creators.json")
    if NEW_CREATOR_KEY in creators:
        print(f"  · Creator {NEW_CREATOR_KEY!r} already present.")
    else:
        creators[NEW_CREATOR_KEY] = dict(NEW_CREATOR)
        save("creators.json", creators)
        print(f"  ✓ Added creator {NEW_CREATOR_KEY!r}.")
    creators = load("creators.json")

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
    if VIDEO["cr"] not in creators:
        sys.exit(f"ABORT: creator key {VIDEO['cr']!r} not in creators.json")
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
