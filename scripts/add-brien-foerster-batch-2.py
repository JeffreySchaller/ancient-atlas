#!/usr/bin/env python3
"""
add-brien-foerster-batch-2.py — Brien Foerster Batch 2.

Combines Shorts catalog insights with main-channel gap-fill. After Batch 1
Brien sat at 45 wires / 29 sites. This batch adds 5 new sites and 8
existing-site wires.

NEW SITES (5):
    Sillustani              — Peru, megalithic chullpa funerary towers
    Chuquito (Inca Uyo)     — Peru, lakeside "fertility temple"
    Nazca Puquios           — Peru, spiral stone-cut aquifer wells
    Wari                    — Peru, pre-Inca empire capital
    Memphis (Mit Rahina)    — Egypt, ancient capital of Lower Egypt

NEW WIRES (8):
    5 anchoring the new sites
    + Karnak: Massive Ancient Complex / Dynastic Masterworks + Older Megalithic
    + Sphinx: Older Than The Dynastic Egyptians?
    + Saqqara Necropolis: Megalithic Serapeum April 2025
    + Step Pyramid: Deep Under The Step Pyramid April 2025
    + Easter Island: A Thorough Exploration / Who Was There Before The Polynesians
    + Unfinished Obelisk (Aswan): Carved Into The Mountains / Tombs of the Nobles

Idempotent. Run from repo root:
    python3 scripts/add-brien-foerster-batch-2.py
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

NEW_SITES = [
    {"n": "Sillustani", "lat": -15.7167, "lng": -70.1500,
     "cat": "tomb", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision"],
     "desc": (
         "Pre-Inca burial complex of the Colla people on a peninsula "
         "in Lake Umayo, 34 km north of Puno on the Peruvian altiplano. "
         "The site is dominated by chullpas — cylindrical funerary "
         "towers up to 12 meters tall built of precision-polygonal "
         "andesite and basalt blocks fitted without mortar. The largest, "
         "the Lizard Chullpa, shows the highest masonry quality in the "
         "complex and is conventionally attributed to a single "
         "construction phase under Inca influence (c. 1450 CE), but "
         "the polygonal seams in the base courses are stylistically "
         "distinct from the regular ashlar above. Independent "
         "investigators including Brien Foerster have documented "
         "cataclysmic damage to the upper courses of several towers "
         "consistent with seismic or impact-shock events."
     ),
    },
    {"n": "Chucuito (Inca Uyo)", "lat": -15.8956, "lng": -69.8867,
     "cat": "temple", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal"],
     "desc": (
         "Lakeside ceremonial complex on the southern shore of Lake "
         "Titicaca, 18 km south of Puno, Peru. Local tradition names "
         "the central enclosure 'Inca Uyo' — the fertility temple — "
         "for its dozens of vertically-mounted phallic stone columns "
         "of varying sizes arranged inside the precision-cut "
         "rectangular enclosure walls. The walls themselves use the "
         "same fitted polygonal masonry tradition seen at Coricancha "
         "and Sacsayhuamán. Conventional Inca attribution (15th c.) "
         "for the upper construction is broadly accepted; the question "
         "of whether the foundation courses predate that period remains "
         "open. Brien Foerster's coverage examines the unusual "
         "concentration of stone phallic forms in the context of "
         "comparable artefacts at other Andean sites."
     ),
    },
    {"n": "Nazca Puquios", "lat": -14.8260, "lng": -74.9377,
     "cat": "underground", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["precision", "geometry", "scale"],
     "desc": (
         "Network of more than 40 spiral stone-cut access wells "
         "(puquios) distributed across the Nazca desert in southern "
         "Peru, providing year-round access to the aquifer beneath. "
         "Each puquio is a precision-cut spiral funnel descending up "
         "to 15 meters, with the walls reinforced by stacked "
         "limestone slabs cut to fit the curve. The system is "
         "conventionally attributed to the Nazca culture (c. 200-700 "
         "CE) and is still in active use today by local farmers, but "
         "the engineering precision (uniform spiral pitch across "
         "different individual wells, consistent inclination angles) "
         "has led independent investigators to question the conventional "
         "tool kit and date."
     ),
    },
    {"n": "Wari (Huari)", "lat": -13.0556, "lng": -74.3489,
     "cat": "city", "region": "South America", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "scale", "precision"],
     "desc": (
         "Capital city of the Wari Empire in central Peru, 22 km "
         "northeast of Ayacucho, occupied from approximately 500 to "
         "1000 CE. The Wari were the first large-scale Andean empire "
         "and the institutional template the Inca later inherited and "
         "expanded. The city covered up to 4 square kilometers at "
         "peak, with massive cyclopean enclosure walls up to 12 meters "
         "tall built of fitted polygonal stone. Much of the site has "
         "been damaged by post-collapse cataclysm and by colonial-era "
         "stone removal; what survives includes the Vegachayoq Moqo "
         "ritual precinct and extensive subterranean galleries. "
         "Independent investigators have documented two distinct "
         "construction phases with materially different masonry "
         "quality between them."
     ),
    },
    {"n": "Memphis (Mit Rahina)", "lat": 29.8478, "lng": 31.2536,
     "cat": "city", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": (
         "Ancient capital of Lower Egypt, founded c. 3100 BCE by "
         "Menes (Narmer) at the strategic Nile delta head. Memphis "
         "served as the principal royal residence and administrative "
         "center for most of the Old Kingdom and continued in use "
         "through the Late Period — the necropolis at Saqqara, the "
         "Giza Plateau, and Dahshur all served Memphis directly. The "
         "site today (Mit Rahina, 24 km south of Cairo) preserves "
         "the colossal limestone Statue of Ramses II (originally over "
         "10 m tall, broken horizontally and now reclining), an "
         "Alabaster Sphinx, and the New Kingdom Temple of Ptah. Most "
         "of the city itself was disassembled in antiquity for stone "
         "to build medieval Cairo. UNESCO World Heritage Site."
     ),
    },
]

def _v(vid, title, published="2022-06-01"):
    return {"id": vid, "title": title,
            "cr": "brienf", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === New sites (5) ===
    ("Sillustani", _v("JOHIRKvWOlo",
        "Sillustani, Lake Titicaca, Peru: Ancient Peruvian Graveyard Of Wizards And Mystics",
        "2022-09-12")),
    ("Chucuito (Inca Uyo)", _v("wyQVflckmpk",
        "Megalithic Fertility Temple At Chucuito Near Lake Titicaca In Peru",
        "2023-03-15")),
    ("Nazca Puquios", _v("gib7XWsQMzg",
        "The Amazing Ancient Puquio Wells Of Nazca Peru",
        "2022-08-20")),
    ("Wari (Huari)", _v("5wbpREE-BUY",
        "The Curious Ancient Site Of Wari In The Highlands Of Peru",
        "2023-11-08")),
    ("Memphis (Mit Rahina)", _v("t8tfk1u8usI",
        "The Bent And Red Pyramids Of Dashur And Ancient Memphis In Egypt",
        "2024-04-25")),

    # === Existing-site fill (6) ===
    ("Karnak Temple Complex", _v("eqmAuczgvA8",
        "Massive Ancient Complex Of Karnak In Egypt; Dynastic Masterworks And Older Megalithic Expressions",
        "2024-09-08")),
    ("Great Sphinx of Giza", _v("8QUd7eTZnBg",
        "The Sphinx: Older Than The Dynastic Egyptians?",
        "2024-01-15")),
    ("Saqqara Necropolis", _v("a4DS1U3B0X4",
        "The Megalithic Serapeum At Saqqara In Egypt April 2025",
        "2025-04-12")),
    ("Step Pyramid of Djoser", _v("s6KLDlxTJ_c",
        "Deep Under The Step Pyramid At Saqqara In Egypt April 2025",
        "2025-04-18")),
    ("Moai of Easter Island (Rapa Nui)", _v("UvlErNXBHy4",
        "A Thorough Exploration Of Easter Island: Who Was There Before The Polynesians?",
        "2023-08-22")),
    ("Unfinished Obelisk (Aswan)", _v("x_X-VRU5m1s",
        "Exploring Out Of Bounds At The Megalithic Quarry In Aswan Egypt",
        "2024-11-05")),
]

def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load('sites.json')
    videos = load('videos.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    print("=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            added += 1
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
            print(f"  ✓ Wired: {v['id']} → {site_name}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        country_map = {
            'Peru': ['Sillustani', 'Chucuito (Inca Uyo)',
                     'Nazca Puquios', 'Wari (Huari)'],
            'Egypt': ['Memphis (Mit Rahina)'],
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
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {added} new sites, {wired} wires")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
