#!/usr/bin/env python3
"""
add-brien-foerster-batch.py — Major Brien Foerster gap-filler.

Brien is the #3 creator on the atlas (37 wires across 21 sites before
this batch). His main channel covers a much deeper Peruvian corpus than
the atlas had previously surfaced, plus a few key Lebanese and Egyptian
sites. This batch fills the biggest gaps.

NEW SITES (8):
    Killarumiyoq           — Peru, megalithic site near Cusco
    Vilcashuaman           — Peru, Inca imperial center, Vilcas province
    Amaru Muru (Stargate)  — Peru, doorway-shaped niche near Lake Titicaca
    Cumbemayo Aqueduct     — Peru, pre-Inca stone-cut water channel
    Pisaq (Pisac)          — Peru, Sacred Valley Inca site
    Saihuite Stone         — Peru, intricately carved megalith
    Byblos                 — Lebanon, oldest continuously inhabited city
    Amarna (Akhetaten)     — Egypt, Akhenaten's capital city

NEW WIRES (8):
    All 8 sites get one Brien walkthrough each.

Idempotent. Run from repo root:
    python3 scripts/add-brien-foerster-batch.py
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

# ============================================================
NEW_SITES = [
    {"n": "Killarumiyoq", "lat": -13.4225, "lng": -72.0667,
     "cat": "megalithic", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision"],
     "desc": (
         "Megalithic site approximately 30 km west of Cusco, Peru, in "
         "the Anta district at ~3,700 meters elevation. The site "
         "centers on a precision-cut andesite outcrop carved with "
         "concentric steps, niches, and a large flat altar surface. "
         "The polygonal masonry around the central feature is "
         "stylistically distinct from the Inca work above, suggesting "
         "two phases of construction. Local Quechua tradition holds "
         "the site as a place where rituals related to the moon "
         "('killa' in Quechua) were performed. Independent field "
         "investigators including Brien Foerster have documented "
         "tool-mark features inconsistent with the conventional "
         "Inca bronze-tool kit."
     ),
    },
    {"n": "Vilcashuaman", "lat": -13.6592, "lng": -73.9442,
     "cat": "city", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision", "scale"],
     "desc": (
         "Inca administrative and ceremonial center in the Ayacucho "
         "region of central Peru at 3,470 meters elevation. The site "
         "was one of the four most important provincial capitals of "
         "the Inca Empire, built atop and incorporating an earlier "
         "Wari-period substrate. The central feature is the "
         "Ushnu — a stepped truncated pyramid faced with precision-"
         "polygonal andesite masonry — the only example of its kind "
         "to survive intact in Peru. Brien Foerster has documented "
         "extensive cataclysmic damage to the upper courses that "
         "post-dates the original construction."
     ),
    },
    {"n": "Amaru Muru (Stargate)", "lat": -16.1633, "lng": -69.3367,
     "cat": "rock-cut", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["precision", "geometry"],
     "desc": (
         "Carved doorway-shaped niche in a sandstone outcrop on the "
         "Hayu Marca plateau, approximately 35 km west of Puno on the "
         "Peruvian shore of Lake Titicaca. The 7-meter-wide rectangular "
         "frame is cut with sharp-edged precision into the bedrock, "
         "with a smaller doorway at its base. Local Aymara tradition "
         "describes the niche as the 'Gate of the Gods' through which "
         "the priest Amaru Muru entered another reality during the "
         "Spanish conquest. The geometric precision of the cut and "
         "the absence of any associated structure (steps, walls, "
         "approach path) place the site in a category by itself. "
         "Independent investigators including Brien Foerster have "
         "documented anomalous magnetometer readings at the niche."
     ),
    },
    {"n": "Cumbemayo Aqueduct", "lat": -7.2317, "lng": -78.5803,
     "cat": "megalithic", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["precision", "geometry", "scale"],
     "desc": (
         "Pre-Inca stone-cut aqueduct in the highlands above Cajamarca, "
         "northern Peru, at approximately 3,500 meters elevation. The "
         "channel is cut into the living volcanic bedrock and extends "
         "for at least 8 kilometers, with right-angle turns, "
         "switchbacks, and engineered drops cut to maintain a "
         "specific gradient. Conventionally dated to the Cajamarca "
         "culture (c. 1500-1000 BCE) on the basis of associated "
         "rock-art and pottery, which would make it among the oldest "
         "stone-engineered hydraulic systems in the Americas. The "
         "precision of the cuts and the engineering of the gradient "
         "have led independent investigators to propose substantially "
         "earlier construction."
     ),
    },
    {"n": "Pisac (Pisaq)", "lat": -13.4144, "lng": -71.8489,
     "cat": "city", "region": "South America", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "precision", "scale"],
     "desc": (
         "Major Inca site in the Sacred Valley of Peru, 30 km north "
         "of Cusco, occupying a 6 km mountain ridge above the Urubamba "
         "river at elevations of 3,000-3,500 meters. The site contains "
         "the largest pre-Columbian cliff necropolis in the Americas "
         "(thousands of shaft tombs in the limestone cliffs facing the "
         "valley), an extensive agricultural terrace system still "
         "partly in use today, the precision-polygonal Intihuatana "
         "ceremonial center, and the Q'allaqasa fortified district. "
         "Two stylistically distinct masonry traditions are present : "
         "fine Inca andesite ashlar above, and a substantially older "
         "and more refined polygonal substrate at the base of the "
         "principal walls."
     ),
    },
    {"n": "Saihuite Stone", "lat": -13.7572, "lng": -72.7350,
     "cat": "megalithic", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["precision", "geometry"],
     "desc": (
         "Andesite boulder approximately 4 meters wide and 2 meters "
         "high, located in Apurímac province of southern Peru. The "
         "upper surface is carved with an intricate three-dimensional "
         "miniature relief depicting over 200 figures : terraced "
         "fields, water channels, animals, deities, and architectural "
         "structures, all rendered at scales between 1 and 15 cm and "
         "interconnected by a working hydraulic network of cut "
         "channels. The mainstream attribution is Inca (15th century) "
         "with ritual purpose, but the precision of the miniaturization "
         "(some details under 1 cm) and the integrated micro-hydraulics "
         "have led independent investigators — including Brien Foerster "
         "and engineer Arlan Andrews — to argue that the carving may "
         "be substantially older and to question the tools required "
         "to produce it."
     ),
    },
    {"n": "Byblos (Jbeil)", "lat": 34.1232, "lng": 35.6519,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "stratigraphy", "scale"],
     "desc": (
         "Ancient Phoenician port city on the Lebanese coast, 40 km "
         "north of Beirut. One of the oldest continuously inhabited "
         "cities in the world : pottery evidence places occupation at "
         "the site as far back as approximately 8,800 BCE, with "
         "substantial Neolithic, Chalcolithic, and Bronze Age strata "
         "preserved in superposition. The Phoenician name 'Gubla' is "
         "the source of the Greek 'Biblos' (book) — the city was the "
         "primary source of papyrus reaching Greece. The site preserves "
         "Phoenician megalithic temple foundations and Roman colonnade, "
         "and includes a series of cut-stone royal tombs whose entry "
         "shafts and chamber precision have drawn independent "
         "investigator attention as candidates for an earlier "
         "substrate. UNESCO World Heritage Site."
     ),
    },
    {"n": "Amarna (Akhetaten)", "lat": 27.6428, "lng": 30.8961,
     "cat": "city", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": (
         "Capital city built and inhabited under the heretic pharaoh "
         "Akhenaten (Amenhotep IV, c. 1346 BCE) on the east bank of "
         "the Nile in Middle Egypt, between Cairo and Luxor. Akhenaten "
         "moved the entire Egyptian court here from Thebes when he "
         "introduced the monotheistic worship of the Aten (sun disk) "
         "and abandoned the traditional pantheon. The city was built "
         "from scratch in a previously empty desert plain and "
         "completely abandoned within 25 years of its founding, "
         "after Akhenaten's death; subsequent pharaohs dismantled "
         "the structures and erased the site from the king lists. "
         "The plan of the city, its boundary stelae, the Great Aten "
         "Temple, and the royal tombs in the eastern cliffs survive. "
         "Independent investigators have documented anomalies in "
         "the bedrock-cut royal tombs not explained by the brief "
         "Amarna occupation."
     ),
    },
]

def _v(vid, title, published="2020-01-01"):
    return {"id": vid, "title": title,
            "cr": "brienf", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Killarumiyoq", _v("L9aCjChcXEQ",
        "Exploring Mysterious Ancient Killarumiyoq In Peru",
        "2023-05-12")),
    ("Vilcashuaman", _v("p90bPLkdIhE",
        "Megalithic Marvels And Ancient Cataclysmic Damage; Vilcashuaman In Peru",
        "2022-08-18")),
    ("Amaru Muru (Stargate)", _v("bF8Bh_1GjpE",
        "Mysterious Ancient Portal Of Amaru Muru Near Lake Titicaca In Peru",
        "2021-11-05")),
    ("Cumbemayo Aqueduct", _v("D2C7OyOXjtQ",
        "The Mysterious Ancient Cumbemayo Aqueduct Of Peru",
        "2022-03-22")),
    ("Pisac (Pisaq)", _v("t99792Z1e00",
        "Ancient Pisaq In The Sacred Valley Of Peru: Inca And Megalithic Aspects",
        "2024-06-10")),
    ("Saihuite Stone", _v("SJ373Pa2RU0",
        "Decoding The Mysterious Saihuite Stone In Peru With American Engineer Arlan Andrews",
        "2022-10-15")),
    ("Byblos (Jbeil)", _v("gokQHVPmwwk",
        "Lost Ancient High Technology Evidence At Byblos In Lebanon",
        "2023-04-08")),
    ("Amarna (Akhetaten)", _v("JjgvoVDoM5I",
        "Exploring Akhenaten's Fabled Capitol City At Amarna In Egypt",
        "2024-02-20")),
]

# ============================================================
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
            'Peru': ['Killarumiyoq', 'Vilcashuaman',
                     'Amaru Muru (Stargate)', 'Cumbemayo Aqueduct',
                     'Pisac (Pisaq)', 'Saihuite Stone'],
            'Lebanon': ['Byblos (Jbeil)'],
            'Egypt': ['Amarna (Akhetaten)'],
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
