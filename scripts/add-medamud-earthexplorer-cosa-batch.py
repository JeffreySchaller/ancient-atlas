#!/usr/bin/env python3
"""
add-medamud-earthexplorer-cosa-batch.py — Medamud + Earth Explorer (2026-09-14)

What this adds :
- 1 new site    : Medamud (Nag el-Madamud, Luxor Governorate — the Temple of
                  Montu, 8 km ENE of Luxor, partly buried and under active
                  excavation)
- 1 new creator : earthexplorer (Earth Explorer, @earthexplorer8256)
- 2 wires       : MDoY3R88C9Y → Medamud (primary)
                  fvlTrsosxiU → Cosa (existing site, existing creator)
- aux maps      : country Egypt, civilization, era -2150, tags for search

Source videos :
- MDoY3R88C9Y  "UNSEEN LUXOR The Buried Megaliths of Medamud Temple  Earth Explorer"
  Earth Explorer (@earthexplorer8256), published Sep 13 2026.
  Stored title tidied — trailing channel name dropped, doubled space closed,
  colon added. Third-party rows are outside check-title-drift.py's first-party
  scope, and the house pattern already tidies Stone Riddles titles the same way.
- fvlTrsosxiU  "An (almost) live glimpse of Cosa-Italy"
  Stone Riddles (@StoneRiddles), published Sep 13 2026. Title stored verbatim.

Why Medamud earns a record : the atlas holds seven sites inside 11 km of here
and not this one, which is the pattern the site exists to correct — Karnak and
Luxor at tier 1, and the temple 8 km up the road that the tour buses do not
reach absent entirely. It is also a genuine stratigraphic case. A walled
temple of the late Old Kingdom or First Intermediate Period lies sealed
beneath the present one; behind its two pylons was a double cave sanctuary
whose underground chambers were marked at the surface by earth mounds, read
by Bisson de la Roque as primeval mounds. The 12th Dynasty levelled that and
rebuilt at larger scale, and building continued through the Ptolemies into
the Roman period. That is four phases stacked in one footprint with the
earliest one buried, which is why signal is "open" rather than "convergent".

Coordinates : 25.7343 N, 32.7099 E. NOT Wikipedia's geodata, which gives
25.71667/32.65 — that is Karnak's longitude and would place Medamud inside
the Karnak precinct, 5 km from the village it names. Taken instead from the
two OSM features that agree to 20 m ("Temple of Montu (Medamud)" monument and
"Temple of Montu in Al Madamud" archaeological_site). Cross-check : the
result sits 8.1 km NE of Luxor Temple, against Wikipedia's prose "about 8 km
east-north from Luxor" and the video's 9 km by bicycle.

Note : Karnak's own Precinct of Montu (25.7201/32.6607) is a different
temple to the same god. Do not merge them.

Sites count : 619 → 620. Dedup verified 2026-09-14 : neither video id present
in videos.json; no existing Medamud record; nearest site is Karnak at 5.5 km;
creator key "earthexplorer" absent, "stoneriddles" already present.

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}
VALID_SIGNAL = {"open", "convergent", None}

NEW_CREATOR_KEY = "earthexplorer"
NEW_CREATOR = {
    "name": "Earth Explorer",
    "handle": "@earthexplorer8256",
    "subs": "Solo travel to obscure ancient sites · a ten-year journey, filmed in the field",
    # Vestigial: toneCreators() overwrites .color at runtime with the creator's
    # share of the atlas. Kept so the record matches the shape of the other 95.
    "color": "#9C7A4E",
    "tier": 3,
}

SITE_NAME = "Medamud"
SITE = {
    "n": SITE_NAME,
    "lat": 25.7343,
    "lng": 32.7099,
    "cat": "temple",
    "region": "Egypt",
    "tier": 3,
    "signal": "open",
    "criteria": ["stratigraphy", "scale"],
    "desc": (
        "Temple of Montu at Nag el-Madamud, 8 km east-north-east of Luxor, "
        "ancient Madu. Montu was the falcon war god of the Theban nome and "
        "the dynastic deity of the 11th Dynasty — four of its kings were "
        "named Mentuhotep, 'Montu is satisfied' — before Amun displaced him "
        "at Karnak. What makes the site worth the ride out is what is under "
        "it. Fernand Bisson de la Roque, excavating for the IFAO from 1925, "
        "found a walled temple of the late Old Kingdom or First Intermediate "
        "Period lying complete beneath the present one : two pylons set one "
        "behind the other, and past them a double cave sanctuary whose "
        "underground chambers were marked at the surface by mounds of earth, "
        "which he read as primeval mounds. The 12th Dynasty levelled that "
        "and rebuilt at much larger scale; work continued through the Second "
        "Intermediate Period and the New Kingdom, of which mostly "
        "inscriptions survive, and on into the Ptolemaic and Roman temples "
        "of Montu, Harpocrates and Raet-Tawy that stand today. The two "
        "monumental Ptolemaic gateways, of Ptolemy III and Ptolemy IV, were "
        "excavated by Alexandre Varille in 1939 and are now in the Musée des "
        "Beaux-Arts de Lyon. Conventional reading : an ordinary provincial "
        "cult centre, continuously rebuilt for some two and a half thousand "
        "years, of interest mainly for the Middle Kingdom statuary it "
        "produced. Independent reading : the earliest phase is the one that "
        "resists. A cave sanctuary marked by artificial mounds is not "
        "standard Old Kingdom temple vocabulary, the phase is known almost "
        "entirely from one excavator's reading of it, and the dating of that "
        "substructure has been argued back and forth between the Old and "
        "Middle Kingdoms ever since. The site is still partly buried and "
        "under active excavation, so the sequence is not closed."
    ),
}

WIRES = [
    (SITE_NAME, {
        "id": "MDoY3R88C9Y",
        "title": "UNSEEN LUXOR: The Buried Megaliths of Medamud Temple",
        "cr": NEW_CREATOR_KEY,
        "added": "2026-09-14",
        "published": "2026-09-13",
    }),
    ("Cosa", {
        "id": "fvlTrsosxiU",
        "title": "An (almost) live glimpse of Cosa-Italy",
        "cr": "stoneriddles",
        "added": "2026-09-14",
        "published": "2026-09-13",
    }),
]

AUX = {
    "countries.json":     "Egypt",
    "civilizations.json": "Egyptian (Old Kingdom through Roman)",
    "eras.json":          -2150,
    "tags.json":          "egypt luxor thebes medamud madamud madu montu "
                          "mentuhotep primeval mound cave sanctuary ptolemaic ifao",
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
    bad = set(SITE["criteria"]) - VALID_CRITERIA
    if bad:
        sys.exit(f"ABORT: invalid criteria {bad}")
    if SITE.get("signal") not in VALID_SIGNAL:
        sys.exit(f"ABORT: invalid signal {SITE.get('signal')!r}")

    cats = load("categories.json")
    ck = set(cats.keys()) if isinstance(cats, dict) else {c.get("key") for c in cats}
    if SITE["cat"] not in ck:
        sys.exit(f"ABORT: category {SITE['cat']!r} undefined — it would render as megalithic")

    sites = load("sites.json")
    before_count = len(sites)
    names = {s["n"] for s in sites}

    # A second Temple of Montu stands inside Karnak, 5 km away. If a record
    # for it ever lands, this is where the confusion would surface.
    import math
    for s in sites:
        d = math.hypot((s["lat"] - SITE["lat"]) * 111.0,
                       (s["lng"] - SITE["lng"]) * 111.0 * math.cos(math.radians(SITE["lat"])))
        if d < 1.0 and s["n"] != SITE_NAME:
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

    # ---------------------------------------------------------- wires
    videos = load("videos.json")
    changed = False
    seen = {v.get("id") for rows in videos.values() for v in rows}
    for target, video in WIRES:
        if target not in sites_now:
            sys.exit(f"ABORT: target site {target!r} not found")
        if video["cr"] not in creators:
            sys.exit(f"ABORT: creator key {video['cr']!r} not in creators.json")
        rows = videos.setdefault(target, [])
        if any(v.get("id") == video["id"] for v in rows):
            print(f"  · Video {video['id']!r} already wired to {target!r}.")
        elif video["id"] in seen:
            sys.exit(f"ABORT: {video['id']!r} is already wired to a different site")
        else:
            rows.append(dict(video))
            changed = True
            print(f"  ✓ Wired {video['id']!r} → {target!r}.")
    if changed:
        save("videos.json", videos)

    # ---------------------------------------------------------- pre-flight
    after_count = len(load("sites.json"))
    print(f"\nsites {before_count} → {after_count}")
    if after_count < before_count:
        sys.exit("ABORT: site count dropped")

    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
