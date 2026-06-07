#!/usr/bin/env python3
"""
add-turkey-megalithic-pair.py — Add two underexamined Turkish megalithic
sites with the same Hugh Newman / Megalithomania thesis : polygonal walls
in Turkey that mirror Peru, Italy, and Greece, suggesting a much older
construction phase than the mainstream chronology assigns.

Site 1 — Meydan Kalesi (Mersin Province, southern Turkey)
  Cliff-edge megalithic complex stretching ~1 km. Cyclopean polygonal
  walls with bent corners and megalithic doorways comparable to the Sun
  Gate at Tiwanaku. Single mega-stones spanning corners (50-60+ tons).
  Rock-cut tombs and caves carved into solid bedrock. Officially
  Hellenistic / Seleucid Empire (~2,300 years old). Independent reading
  cites parallels to the Hellenicon Pyramid in Greece (2720 BCE) and the
  Orbetello walls in Italy (6,000-7,000+ years old by water erosion
  dating). Hugh Newman invokes pre-Etruscan and pre-Phoenician origins.

Site 2 — Alaca Höyük (Çorum Province, central Turkey)
  Hattian/Hittite site centered on the Spring of Arinna. Sphinx Gate,
  Royal Graves of the Hattian culture (~2000-2500 BCE) with elaborate
  bronze/gold/electrum grave goods. Postern tunnel with cyclopean
  vaulted construction. Multiple "portal stones" / hold stones with
  parallels to Göbekli Tepe and Karahan Tepe (potentially Mesolithic).
  Mortise-and-tenon joints comparable to Stonehenge. Mega-blocks with
  nubs comparable to Peru's polygonal masonry. Recent dating pushes
  the original construction phase into the early Neolithic.

Both videos are MegalithomaniaUK uploads. Hugh Newman directly invokes
cross-continental polygonal pattern, which ties into the Mini Megaliths
thesis. Neither video qualifies for the NEW badge (Meydan = Jun 2023,
Alaca = Mar 2025), but both will surface in the Latest sort.

Idempotent.

Run from the repo root:
    python3 scripts/add-turkey-megalithic-pair.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

# ============================================================
def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# Resolve creator key
creators = load('creators.json')
if 'megalithomania' not in creators:
    sys.exit("Megalithomania creator not found. Check creators.json.")
CR = 'megalithomania'

# ============================================================
NEW_SITES = [
    {
        "n": "Meydan Kalesi",
        "lat": 36.5333,
        "lng": 33.8500,  # near Silifke, Mersin Province
        "cat": "megalithic",
        "region": "Türkiye",
        "tier": 2,
        "signal": "open",
        "criteria": ["polygonal", "scale", "geometry"],
        "desc": (
            "Cliff-edge megalithic complex along Turkey's southern coast in Mersin "
            "Province, near Silifke. The site stretches approximately one kilometer "
            "with cyclopean polygonal walls, megalithic doorways, and single "
            "mega-stones spanning corners (50-60+ tons by visual estimate). The "
            "doorway construction is directly comparable to the Sun Gate at "
            "Tiwanaku, Bolivia, and the polygonal joinery mirrors sites at Norba "
            "and Saturnia in Italy. Rock-cut tombs and chamber caves are carved "
            "into the surrounding bedrock. Conventional reading : Hellenistic, "
            "built under the Seleucid Empire approximately 2,300 years ago. "
            "Independent reading : the masonry style matches sites that have been "
            "dated as much older elsewhere : the Hellenicon Pyramid in Greece "
            "(2720 BCE by sonoluminescence) and the Orbetello walls in Italy "
            "(6,000-7,000+ years old by water-erosion dating). Hugh Newman "
            "proposes a much earlier construction phase, potentially Neolithic, "
            "with later Hellenistic occupation built on top."
        ),
    },
    {
        "n": "Alaca Höyük",
        "lat": 40.2333,
        "lng": 34.6833,  # Çorum Province, central Turkey
        "cat": "megalithic",
        "region": "Türkiye",
        "tier": 2,
        "signal": "open",
        "criteria": ["polygonal", "scale", "geometry", "precision"],
        "desc": (
            "Hattian and Hittite site in central Anatolia, centered on the Spring "
            "of Arinna (still flowing). The Sphinx Gate (30 ft wide) is flanked "
            "by 3D relief carvings of sphinxes, bulls, the storm god, and a king "
            "and queen. Behind the gate stand gigantic polygonal walls with "
            "puffy bent-corner stones directly comparable to Cusco and "
            "Sacsayhuamán. The site preserves 13 royal graves of the Hattian "
            "culture (~2000-2500 BCE) with elaborate bronze, gold, and electrum "
            "grave goods, including bronze deer and sun-disc rosettes. A "
            "postern tunnel with cyclopean vaulted construction runs to the "
            "west, with mortise-and-tenon joints comparable to Stonehenge "
            "lintels and multiple portal stones reminiscent of Göbekli Tepe "
            "and Karahan Tepe. Conventional reading : Hattian then Hittite "
            "Bronze Age (3rd-2nd millennium BCE). Independent reading : the "
            "polygonal masonry and the portal stones suggest a much earlier "
            "construction phase that the Hatti inherited and the Hittites "
            "reused. Recent dating is being pushed into the early Neolithic, "
            "with possible cultural continuity from Göbekli Tepe and Karahan "
            "Tepe."
        ),
    },
]

VIDEOS_TO_WIRE = [
    ("Meydan Kalesi", {
        "id": "SU2JhCOJ6X0",
        "title": "Meydan Kalesi | Giant Polygonal and Cyclopean Walls in Turkey | Megalithomania",
        "cr": CR,
        "added": TODAY,
        "published": "2023-06-10",
    }),
    ("Alaca Höyük", {
        "id": "p5iRgWqXykw",
        "title": "This Is Not Peru! | Massive Polygonal Walls in Turkey | Megalithomania",
        "cr": CR,
        "added": TODAY,
        "published": "2025-03-11",
    }),
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

    site_names = {s['n'] for s in sites}

    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added site: {s['n']}")
            print(f"     signal={s.get('signal')}, criteria={s.get('criteria')}")
    if sites_added:
        save('sites.json', sites)

    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Video {v['id']} already wired to {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name} (pub: {v['published']})")
    if videos_wired:
        save('videos.json', videos)

    if isinstance(countries, dict):
        for key in ['Türkiye', 'Turkey']:
            if key in countries:
                for s in NEW_SITES:
                    if s['n'] not in countries[key]:
                        countries[key].append(s['n'])
                save('countries.json', countries)
                print(f"  ✓ {key} tagged with both new sites")
                break
        else:
            countries['Türkiye'] = [s['n'] for s in NEW_SITES]
            save('countries.json', countries)
            print(f"  ✓ Created Türkiye country tag")

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
