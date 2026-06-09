#!/usr/bin/env python3
"""
add-southwest-puebloan-cluster.py — Close the largest North American
geographic gap on the atlas: the Ancestral Puebloan (Anasazi) cluster
of the Four Corners region.

Five UNESCO/NPS-grade sites that the atlas had completely missed:

    Mesa Verde National Park       — Colorado
    Chaco Culture National Historical Park — New Mexico
    Hovenweep National Monument    — CO/UT border
    Bandelier National Monument    — New Mexico
    Canyon de Chelly National Monument — Arizona

Brien Foerster's main Peru/Egypt focus left him almost no NA Southwest
coverage (only Montezuma's Castle), so this batch anchors with the
field-walker and archaeology-focused creators who actually live in
the SW corpus, plus the canonical National Geographic doc for Mesa
Verde as a high-credibility editorial anchor.

NEW CREATORS (5):
    natgeo            — National Geographic (institutional)
    jimeighmey        — Jim Eighmey's Archeology Videos
    truthfultraveler  — Truthful Traveler
    towanderfreely    — To Wander Freely
    cactusatlas       — Cactus Atlas

WIRES (6):
    Mesa Verde × 2 (Ancient Architects already a creator + National Geographic)
    Chaco Canyon × 1
    Canyon de Chelly × 1
    Bandelier × 1
    Hovenweep × 1

Idempotent. Run from repo root:
    python3 scripts/add-southwest-puebloan-cluster.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
TODAY = datetime.date.today().isoformat()
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal",
                  "stratigraphy", "geometry", "machining"}

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

NEW_CREATORS = {
    "natgeo": {
        "name": "National Geographic",
        "handle": "@NationalGeographic",
        "subs": "Institutional documentary · global field reporting · UNESCO-grade coverage",
        "color": "#F2C500",
        "tier": 1,
    },
    "jimeighmey": {
        "name": "Jim Eighmey's Archeology Videos",
        "handle": "@JimEighmey",
        "subs": "Field archaeology walkthroughs · American Southwest specialty",
        "color": "#A87644",
        "tier": 2,
    },
    "truthfultraveler": {
        "name": "Truthful Traveler",
        "handle": "@TruthfulTraveler",
        "subs": "Respectful on-site coverage · indigenous-perspective travel",
        "color": "#7BAE7F",
        "tier": 2,
    },
    "towanderfreely": {
        "name": "To Wander Freely",
        "handle": "@ToWanderFreely",
        "subs": "Ancestral Puebloan field-walking · National Monument deep-dives",
        "color": "#C2826B",
        "tier": 3,
    },
    "cactusatlas": {
        "name": "Cactus Atlas",
        "handle": "@CactusAtlas",
        "subs": "Southwest desert archaeology · National Monument coverage",
        "color": "#B97A3A",
        "tier": 3,
    },
}

NEW_SITES = [
    {"n": "Mesa Verde", "lat": 37.1853, "lng": -108.4861,
     "cat": "rock-cut", "region": "North America", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "stratigraphy"],
     "desc": (
         "Mesa Verde National Park in southwest Colorado preserves "
         "the largest and best-known cliff-dwelling complex of the "
         "Ancestral Puebloan people. Occupied approximately 600-1300 "
         "CE; the cliff dwellings themselves date primarily to the "
         "Pueblo III period (1150-1300 CE). The site holds over "
         "5,000 known archaeological sites and 600 cliff dwellings "
         "tucked into south-facing alcoves of the canyon walls. "
         "Cliff Palace, the largest, contains 150 rooms and 23 kivas. "
         "The reasons for the rapid late-13th-century abandonment "
         "remain incompletely resolved : prolonged megadrought is "
         "documented but does not by itself explain the speed or "
         "the totality of the departure. UNESCO World Heritage Site "
         "since 1978, one of the original 12 inscribed."
     ),
    },
    {"n": "Chaco Canyon (Chaco Culture)", "lat": 36.0561, "lng": -107.9711,
     "cat": "city", "region": "North America", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "polygonal"],
     "desc": (
         "Chaco Culture National Historical Park in northwestern New "
         "Mexico was the political, ceremonial, and economic center "
         "of the Ancestral Puebloan world from approximately 850-1150 "
         "CE. The canyon preserves a dozen massive 'Great Houses' — "
         "multi-story masonry complexes of which Pueblo Bonito (650+ "
         "rooms, 4 stories tall, built in a precise D-shape over more "
         "than two centuries) is the largest. The site is laid out "
         "with documented astronomical alignments — Casa Rinconada's "
         "great kiva is oriented to the cardinal directions to within "
         "fractions of a degree, and the Sun Dagger petroglyph on "
         "Fajada Butte marks solstices and the 18.6-year lunar "
         "standstill. A 400-mile network of engineered straight roads "
         "radiates from Chaco across the Colorado Plateau. UNESCO "
         "World Heritage Site since 1987."
     ),
    },
    {"n": "Hovenweep", "lat": 37.3839, "lng": -109.0764,
     "cat": "city", "region": "North America", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal", "geometry"],
     "desc": (
         "Hovenweep National Monument on the Colorado-Utah border "
         "preserves six clusters of Ancestral Puebloan stone towers "
         "built at the heads of small box canyons. Occupied from "
         "approximately 1200-1300 CE — the same late-Pueblo III "
         "horizon as Mesa Verde — and abandoned in the same "
         "depopulation episode. The towers themselves are "
         "architecturally unusual : square, circular, oval, and "
         "D-shaped masonry forms built with precision-fitted "
         "sandstone blocks, several incorporating apparent "
         "astronomical alignments at solstices and equinoxes. The "
         "Holly Group and Square Tower complex are the best-preserved. "
         "The purpose of the towers — defensive, ceremonial, "
         "astronomical, or some combination — remains an open "
         "question."
     ),
    },
    {"n": "Bandelier", "lat": 35.7811, "lng": -106.2706,
     "cat": "rock-cut", "region": "North America", "tier": 2, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Bandelier National Monument on the Pajarito Plateau of "
         "northern New Mexico preserves the cliff dwellings and "
         "pueblos of the Ancestral Puebloan ancestors of the modern "
         "Cochiti and San Ildefonso Pueblo peoples. The site was "
         "occupied from approximately 1150-1550 CE. The Frijoles "
         "Canyon main loop preserves Tyuonyi (a circular pueblo of "
         "400 rooms at canyon bottom), the Long House (a series of "
         "cavates carved into the soft volcanic tuff of the cliff "
         "face), and Alcove House (reached by 140 feet of wooden "
         "ladders 140 feet above the canyon floor). The carved "
         "cavates show the precision-cut detail characteristic of "
         "rock-cut architecture, with smoke-blackened ceilings still "
         "intact 500 years after abandonment."
     ),
    },
    {"n": "Canyon de Chelly", "lat": 36.1542, "lng": -109.4683,
     "cat": "rock-cut", "region": "North America", "tier": 1, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Canyon de Chelly National Monument in northeastern Arizona "
         "is the only NPS unit owned and lived-in by an indigenous "
         "community — the Navajo Nation. The canyon has been "
         "continuously occupied for at least 5,000 years, with "
         "Archaic, Basketmaker, Ancestral Puebloan, Hopi, and Navajo "
         "occupation phases all preserved in stratigraphic context. "
         "The cliff dwellings of White House Ruin and Antelope House "
         "(Pueblo III, c. 1100-1300 CE) sit tucked into the soaring "
         "1,000-foot sandstone walls. Spider Rock — an 800-foot "
         "freestanding sandstone spire — is sacred to the Navajo. "
         "Public access remains restricted; nearly all interior "
         "canyon access requires a Navajo guide, a deliberate "
         "preservation choice."
     ),
    },
]

def _v(vid, title, cr, published="2023-01-01"):
    return {"id": vid, "title": title,
            "cr": cr, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Mesa Verde", _v("1jkp-_Gfa44",
        "The Mystery of the Ancient Cliff Palace in Mesa Verde, Colorado, USA | Ancient Architects",
        "ancientarch", "2021-08-12")),
    ("Mesa Verde", _v("XPI68mdz2HY",
        "Mesa Verde's Cliffside Dwellings Show a Glimpse of History | National Geographic",
        "natgeo", "2020-04-15")),
    ("Chaco Canyon (Chaco Culture)", _v("_m0CuBsytz8",
        "Chaco Canyon Tour — A Walkthrough of Pueblo Bonito | Jim Eighmey's Archeology Videos",
        "jimeighmey", "2022-06-20")),
    ("Canyon de Chelly", _v("J-2d3Tb7doo",
        "Canyon de Chelly: Secrets of a Living Navajo Landscape | Truthful Traveler",
        "truthfultraveler", "2024-03-10")),
    ("Bandelier", _v("zQsqXVIVWcw",
        "Bandelier National Monument — A look at ancestral puebloan life | To Wander Freely",
        "towanderfreely", "2023-09-15")),
    ("Hovenweep", _v("4OS1YX7oG_0",
        "Are These RUINS or CASTLES? Hovenweep National Monument, Utah | Cactus Atlas",
        "cactusatlas", "2024-05-08")),
]

def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load('sites.json')
    creators = load('creators.json')
    videos = load('videos.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    print("=== NEW CREATORS ===")
    added_creators = 0
    for k, v in NEW_CREATORS.items():
        if k in creators:
            print(f"  · Already exists: {k}")
        else:
            creators[k] = v
            added_creators += 1
            print(f"  ✓ Added: {k} → {v['name']}")
    save('creators.json', creators)

    print("\n=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    added_sites = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            added_sites += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            print(f"  ✗ Missing site: {site_name}")
            continue
        videos.setdefault(site_name, [])
        if any(x['id'] == v['id'] for x in videos[site_name]):
            print(f"  · Already wired: {v['id']}")
        else:
            videos[site_name].append(v)
            wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name} (cr={v['cr']})")
    save('videos.json', videos)

    if isinstance(countries, dict):
        country_map = {
            'United States': ['Mesa Verde', 'Chaco Canyon (Chaco Culture)',
                              'Hovenweep', 'Bandelier', 'Canyon de Chelly'],
        }
        for country, names in country_map.items():
            countries.setdefault(country, [])
            for n in names:
                if n not in countries[country]:
                    countries[country].append(n)
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated")

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {added_sites} new sites, {added_creators} new creators, {wired} wires")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
