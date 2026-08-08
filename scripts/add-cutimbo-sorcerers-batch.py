#!/usr/bin/env python3
"""
add-cutimbo-sorcerers-batch.py — Cutimbo + Sillustani alignment (2026-08-07)

What this adds :
- 1 new site : Cutimbo (Pichacani district, Puno, Peru — chullpa necropolis on
  a volcanic promontory 22 km south of Puno, square and cylindrical towers with
  carved animal reliefs, over rock shelters holding ~8,000-year-old paintings)
- 1 wire     : vtIOrI1DWQ0 → Cutimbo (primary)
- aux maps   : country Peru, civilization "Lupaca / Colla, then Inca",
               era 1200, tags for search

What this also fixes :
- Sillustani was filed cat "tomb" with criteria precision / hardness / geometry
  and no `polygonal`. Jeff's call is that both chullpa sites read as megalithic
  and polygonal, and Sillustani is the reference the new record is measured
  against, so it moves to cat "megalithic" and gains the polygonal criterion.
  The two sites are 52 km apart and belong to one building tradition; filing
  them under different types made the pair invisible to each other.
- Sillustani had no era, civilization or tag mapping at all (country only).
  Filled to match Cutimbo so the pair behaves consistently under every filter.

Both sites are wired to Library Entry 08, The Convergence Question, which is
where the polygonal corpus is argued. Polygonal corpus 82 -> 84.

Source video :
- vtIOrI1DWQ0  "Mystery Cutimbo: The Giant Towers of Lake Titicaca"
  Sorcerers of Stone (@sorcerersofstone), published Aug 7 2026.
  Their 31st wire and their first outside the Cusco region.

Coordinates : 16.0333 S, 70.0667 W. Cross-checked against the published
"22 km along the Puno-Moquegua highway": this point is 22.0 km from Puno's
centre, which matches. Treat as site-centre, not survey grade.

Sites count : 617 -> 618. Dedup verified 2026-08-07 : video id absent from
videos.json; no existing Cutimbo record; creator key "sorcerersofstone"
already present.

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

CREATOR_KEY = "sorcerersofstone"

LIBRARY_REF = {
    "url": "/library/the-convergence-question.html",
    "title": "The Convergence Question",
}

# ---------------------------------------------------------------- new site
SITE_NAME = "Cutimbo"
SITE = {
    "n": SITE_NAME,
    "lat": -16.0333,
    "lng": -70.0667,
    "cat": "megalithic",
    "region": "South America",
    "tier": 2,
    "signal": "open",
    "criteria": ["polygonal", "precision", "geometry"],
    "desc": (
        "Chullpa necropolis on a flat-topped volcanic promontory rising off "
        "the altiplano 22 km south of Puno, its summit at about 4,060 m. The "
        "burial towers are the reason to come : unlike the uniformly "
        "cylindrical chullpas at Sillustani 52 km north, Cutimbo carries both "
        "round and square-to-rectangular towers on the same plateau, built of "
        "fitted volcanic blocks laid without mortar, several of them carved "
        "with relief figures of Andean animals including the puma, the condor "
        "and the serpent. Conventional reading : a Lupaca and Colla "
        "necropolis of the Late Intermediate period, roughly the 13th to 15th "
        "centuries, taken over and added to under Inca rule after about 1450. "
        "The detail that makes the site worth an entry of its own is "
        "underneath all of that : the rock shelters in the same promontory "
        "hold paintings estimated at over 8,000 years old. The hill was in "
        "use eight millennia before the towers went up on it, which makes "
        "Cutimbo a stratigraphic question rather than only a funerary one, "
        "and raises the same question the square and round towers raise : "
        "how many separate building phases are stacked here, and who built "
        "the earliest of them."
    ),
    "library_ref": dict(LIBRARY_REF),
}

VIDEO = {
    "id": "vtIOrI1DWQ0",
    "title": "Mystery Cutimbo: The Giant Towers of Lake Titicaca",
    "cr": CREATOR_KEY,
    "added": "2026-08-07",
    "published": "2026-08-07",
}

WIRE_TARGETS = [SITE_NAME]

AUX_CUTIMBO = {
    "countries.json":     "Peru",
    "civilizations.json": "Lupaca / Colla, then Inca",
    "eras.json":          1200,
    "tags.json":          "peru puno titicaca chullpa burial tower altiplano lupaca colla rock art",
}

# ------------------------------------------------------- Sillustani alignment
SIBLING = "Sillustani"
SIBLING_CAT = "megalithic"
SIBLING_CRITERIA = ["polygonal", "precision", "hardness", "geometry"]
AUX_SILLUSTANI = {
    "civilizations.json": "Colla, then Inca",
    "eras.json":          1200,
    "tags.json":          "peru puno titicaca chullpa burial tower altiplano colla umayo",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  ✓ wrote data/{name}")


def main():
    for crit in (SITE["criteria"], SIBLING_CRITERIA):
        bad = set(crit) - VALID_CRITERIA
        if bad:
            sys.exit(f"ABORT: invalid criteria {bad}")

    creators = load("creators.json")
    if CREATOR_KEY not in creators:
        sys.exit(f"ABORT: creator key {CREATOR_KEY!r} not in creators.json")

    sites = load("sites.json")
    before_count = len(sites)
    names = {s["n"] for s in sites}

    # ------------------------------------------------------------ new site
    if SITE_NAME in names:
        print(f"  · Site {SITE_NAME!r} already present.")
    else:
        sites.append(dict(SITE))
        print(f"  ✓ Added site {SITE_NAME!r}.")

    # ------------------------------------------------------ sibling alignment
    sib = next((s for s in sites if s["n"] == SIBLING), None)
    if sib is None:
        sys.exit(f"ABORT: {SIBLING!r} not found — expected it to exist")
    if sib.get("cat") != SIBLING_CAT:
        print(f"  ✓ {SIBLING}: cat {sib.get('cat')!r} → {SIBLING_CAT!r}")
        sib["cat"] = SIBLING_CAT
    else:
        print(f"  · {SIBLING}: cat already {SIBLING_CAT!r}")
    if sib.get("criteria") != SIBLING_CRITERIA:
        print(f"  ✓ {SIBLING}: criteria {sib.get('criteria')} → {SIBLING_CRITERIA}")
        sib["criteria"] = list(SIBLING_CRITERIA)
    else:
        print(f"  · {SIBLING}: criteria already aligned")
    if not sib.get("library_ref"):
        sib["library_ref"] = dict(LIBRARY_REF)
        print(f"  ✓ {SIBLING}: wired to Entry 08")
    else:
        print(f"  · {SIBLING}: keeps {sib['library_ref'].get('title')!r}")

    save("sites.json", sites)
    sites_now = {s["n"] for s in load("sites.json")}

    # ---------------------------------------------------------- aux maps
    for target, aux in ((SITE_NAME, AUX_CUTIMBO), (SIBLING, AUX_SILLUSTANI)):
        for filename, value in aux.items():
            m = load(filename)
            if m.get(target) == value:
                print(f"  · {filename}: {target!r} already set.")
                continue
            m[target] = value
            save(filename, m)

    # ------------------------------------------------------------- wires
    videos = load("videos.json")
    changed = False
    for target in WIRE_TARGETS:
        if target not in sites_now:
            sys.exit(f"ABORT: target site {target!r} not found")
        wires = videos.setdefault(target, [])
        if any(v.get("id") == VIDEO["id"] for v in wires):
            print(f"  · Video {VIDEO['id']!r} already wired to {target!r}.")
        else:
            wires.append(dict(VIDEO))
            changed = True
            print(f"  ✓ Wired {VIDEO['id']!r} → {target!r}.")
    if changed:
        save("videos.json", videos)

    # --------------------------------------------------------- pre-flight
    after = load("sites.json")
    if len(after) < before_count:
        sys.exit("ABORT: site count dropped")
    corpus = [s for s in after if "polygonal" in (s.get("criteria") or [])]
    print(f"\nsites {before_count} → {len(after)}")
    print(f"polygonal corpus : {len(corpus)}")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
