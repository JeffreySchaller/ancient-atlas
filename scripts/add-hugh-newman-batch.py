#!/usr/bin/env python3
"""
add-hugh-newman-batch.py — Hugh Newman / Megalithomania gap-fill.

Hugh is the atlas's #1 creator (58 wires / 38 sites before this batch).
His coverage is UK + Mediterranean + Egypt + Mesoamerica + India. This
batch closes the highest-priority gaps in those territories.

NEW SITES (6):
    Cefalù Polygonal Walls          — Sicily, Italy
    Thornborough Henges             — North Yorkshire, England
    Stanton Drew Stone Circles      — Somerset, England
    Long Man of Wilmington          — East Sussex, England
    Nagarjuni Caves                 — Bihar, India (Barabar sister site)
    Hirebenakal Dolmen Necropolis   — Karnataka, India

NEW WIRES (8):
    6 anchoring the new sites
    + Great Sphinx fill: Second Sphinx SAR-scan revelations 2026
    + Great Pyramid fill: All three pyramids and the Sphinx — Khafre
      Project interview (the major 2025-2026 SAR-scan story)

Idempotent. Run from repo root:
    python3 scripts/add-hugh-newman-batch.py
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
    {"n": "Cefalù Polygonal Walls", "lat": 38.0395, "lng": 14.0228,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision"],
     "desc": (
         "Massive polygonal masonry foundations on the slopes of the "
         "Rocca above Cefalù, on Sicily's northern coast. The walls "
         "support the so-called Temple of Diana — a later Roman/Norman "
         "rebuild atop substantially older megalithic courses. The "
         "lower polygonal blocks match the cyclopean tradition seen at "
         "Cuzco, Alatri, and Delphi : irregular many-sided faces fitted "
         "to sub-millimeter seams without mortar. Local archaeology "
         "attributes the construction to a 9th-century BCE Sicel "
         "occupation, but Hugh Newman and other independent investigators "
         "have documented courses of substantially older style at the "
         "base of the cliff."
     ),
    },
    {"n": "Thornborough Henges", "lat": 54.2014, "lng": -1.5611,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Complex of three near-identical Neolithic henges in North "
         "Yorkshire, England, often called 'The Stonehenge of the "
         "North.' Each henge measures approximately 240 m in diameter "
         "with twin entrances oriented on the same line. The three are "
         "spaced and aligned with each other along a ritual landscape "
         "axis on the floodplain of the River Ure, built approximately "
         "3500-2500 BCE. The site narrowly escaped destruction by "
         "aggregate quarrying after a long preservation campaign that "
         "Hugh Newman's coverage helped publicize; English Heritage and "
         "the National Trust took the central monument into protective "
         "ownership in 2023."
     ),
    },
    {"n": "Stanton Drew Stone Circles", "lat": 51.3736, "lng": -2.5759,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Complex of three Neolithic stone circles in Somerset, "
         "England, including the Great Circle — the second-largest "
         "stone circle in the British Isles at 113 m in diameter, "
         "exceeded only by Avebury. Geophysical survey in 1997 "
         "revealed nine concentric rings of post holes within the "
         "Great Circle, suggesting a vast multi-phase timber structure "
         "predating the surviving stones. Conventional dating places "
         "the megalithic phase c. 3000 BCE. Maria Wheatley and Howard "
         "Crowhurst have documented landscape-scale geometric and "
         "lunar alignments connecting the three circles."
     ),
    },
    {"n": "Long Man of Wilmington", "lat": 50.8056, "lng": 0.1839,
     "cat": "geoglyph", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Chalk hill figure on Windover Hill in the South Downs of "
         "East Sussex, England — a 70-meter-tall outline of a standing "
         "human figure holding two staves. Conventionally dated to "
         "the early modern period (17th c.) on the basis of the "
         "earliest written record, but Stuart Mason and other "
         "investigators have documented summer-solstice alignment "
         "geometry and archaeoastronomical features that argue for "
         "substantially earlier origin. The figure's eastern staff "
         "aligns with the summer solstice sunrise at construction "
         "latitude; the western staff aligns with the winter solstice "
         "sunset."
     ),
    },
    {"n": "Nagarjuni Caves", "lat": 24.9183, "lng": 85.0814,
     "cat": "rock-cut", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal", "machining"],
     "desc": (
         "Group of three rock-cut Mauryan-period caves on a low "
         "granite hill 1 km north of the Barabar Caves in Bihar, "
         "India. Cut from solid granite in the 3rd century BCE under "
         "Emperor Ashoka's grandson Dasharatha, the caves preserve "
         "the same impossibly precise mirror-polished interior walls "
         "documented at Barabar. The Gopika, Vapiya and Vadithi-ka "
         "Kubha caves are inscribed in Brahmi and Ashokan Pali. "
         "Independent investigators including Hugh Newman document "
         "tool-mark surfaces that conventional iron-chisel technology "
         "of the period cannot replicate, in line with the Barabar "
         "anomaly."
     ),
    },
    {"n": "Hirebenakal Megalithic Necropolis", "lat": 15.6233, "lng": 76.1722,
     "cat": "tomb", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "polygonal"],
     "desc": (
         "Massive dolmen necropolis on a granite hill in Karnataka, "
         "India — over 1,000 dolmens scattered across approximately "
         "8 square kilometers, the largest such concentration in "
         "South Asia. The dolmens are constructed of slabs of locally-"
         "quarried granite, some up to 4 meters tall, supported on "
         "edge stones with capping slabs and surrounded by small "
         "stone circles. Conventional dating places the necropolis "
         "in the Iron Age (c. 1000-300 BCE) on the basis of "
         "associated material culture, but the precision-cut joinery "
         "and standardized dimensions have led Hugh Newman and others "
         "to question the conventional Iron-Age tool kit."
     ),
    },
]

def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": "megalithomania", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === New sites (6) ===
    ("Cefalù Polygonal Walls", _v("hNozmj2-J5E",
        "Ancient Polygonal Walls of Cefalù, Sicily | The Temple of Diana | Megalithomania",
        "2024-09-08")),
    ("Thornborough Henges", _v("GmaQhVihaG4",
        "Stonehenge of the North | Thornborough Henges 4K Aerial Film | Megalithomania",
        "2023-07-15")),
    ("Stanton Drew Stone Circles", _v("6_9YqFY0DGI",
        "Landscape Geometry and Alignments at Stanton Drew Stone Circle | Howard Crowhurst | Megalithomania",
        "2022-10-20")),
    ("Long Man of Wilmington", _v("kpWtoPbZmus",
        "Summer Solstice Discovery at the Long Man of Wilmington | Megalithomania",
        "2024-06-22")),
    ("Nagarjuni Caves", _v("W23uXz-aOg0",
        "Nagarjuni Caves | Precision Impossible | Barabar Pt 2 | Megalithomania",
        "2024-03-18")),
    ("Hirebenakal Megalithic Necropolis", _v("XXw8KcLQchk",
        "Who Built The Hirebenakal Dolmens of India? | Megalithomania Clip",
        "2023-11-10")),

    # === Existing-site fill: 2025-2026 Khafre / Sphinx SAR scan story ===
    ("Great Sphinx of Giza", _v("SKJsolWOAqc",
        "Is There Really A Second Sphinx? | More SAR Scan Revelations in 2026 | Megalithomania Podcast",
        "2026-04-22")),
    ("Pyramid of Khafre", _v("R_DIGdpxXCo",
        "NEWS | Beneath All Three Pyramids and the Sphinx! | Khafre Project Interview | Megalithomania",
        "2025-09-12")),
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
    new_badges = 0
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
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90:
                new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}{tag}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        country_map = {
            'Italy': ['Cefalù Polygonal Walls'],
            'United Kingdom': ['Thornborough Henges',
                                'Stanton Drew Stone Circles',
                                'Long Man of Wilmington'],
            'India': ['Nagarjuni Caves', 'Hirebenakal Megalithic Necropolis'],
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
    print(f"  This batch:         {added} new sites, {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
