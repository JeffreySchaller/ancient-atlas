#!/usr/bin/env python3
"""
patch-secrets-orphans.py

Mop-up for three wire targets that didn't exist in the iCloud copy of
sites.json after the gap-filler batch:

  · Tarawasi — was added to the GitHub repo directly in a previous
    session; iCloud copy never received it.
  · Phnom Bok — Cambodian Bakheng-period temple, never on the atlas.
  · Easter Island - Ahu Vinapu — Cassie's shorts cover Vinapu masonry
    specifically, but the only Easter Island site on the atlas is the
    Moai entry, so redirect the wires there.

Idempotent. Run from repo root:
    python3 scripts/patch-secrets-orphans.py
    python3 scripts/build.py
"""
import json, datetime, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
TODAY = datetime.date.today().isoformat()

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

NEW_SITES = [
    {"n": "Tarawasi", "lat": -13.4408, "lng": -72.5928,
     "cat": "temple", "region": "South America", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision", "hardness"],
     "desc": (
         "Inca-period ceremonial site near Limatambo in the Cuzco region "
         "of Peru, sitting at the entrance to the Apurimac valley along "
         "the Inca road. The site is dominated by a massive retaining "
         "wall built of polygonal andesite blocks fitted without mortar "
         "to a precision matching Sacsayhuaman and Coricancha. The wall "
         "also bears unusual surface features (nubs, depressions, scoop "
         "marks) that independent researchers including Brien Foerster "
         "and Jesús Gamarra cite as evidence of an earlier, "
         "non-Inca construction phase that the Inca subsequently "
         "reused. Some block faces show signs of intense heat exposure."
     ),
    },
    {"n": "Phnom Bok", "lat": 13.4583, "lng": 103.9417,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["precision", "geometry"],
     "desc": (
         "Bakheng-period (late 9th century CE) Khmer mountain temple in "
         "Siem Reap Province, Cambodia, built by King Yasovarman I as "
         "one of three sister hill-top temples (with Phnom Bakheng and "
         "Phnom Krom). The four ruined towers feature unexplained "
         "horizontal grooves around their sandstone blocks — independent "
         "researchers note these as inconsistent with documented Khmer "
         "tooling traditions and consistent with surfaces seen at other "
         "anomalous Asian sites."
     ),
    },
]

# Three Easter Island shorts redirected from non-existent
# "Easter Island - Ahu Vinapu" to canonical "Moai of Easter Island (Rapa Nui)".
def _v(vid, title, published="2025-01-01"):
    return {"id": vid, "title": f"{title} | Secrets in Stone",
            "cr": "secretsinstone", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # Tarawasi
    ("Tarawasi", _v("CUGsT9KKErE",
        "Megalithic Tarawasi: Peru's Hidden Mystery with Brien Foerster",
        "2026-05-20")),
    ("Tarawasi", _v("UrBKXFctyic",
        "Was Tarawasi exposed to very high heat? (with Brien Foerster)",
        "2026-05-15")),
    # Phnom Bok
    ("Phnom Bok", _v("jMEy98Xet90",
        "Horizontal grooves at the ruined towers of Phnom Bok",
        "2025-10-20")),
    # Easter Island — redirected to the canonical Rapa Nui entry
    ("Moai of Easter Island (Rapa Nui)", _v("EqsQDTVBQkc",
        "A new unit of megalithic measure — Easter Island",
        "2026-02-10")),
    ("Moai of Easter Island (Rapa Nui)", _v("rOpEMhGMnrg",
        "Basalt 'toki' tool from Easter Island",
        "2026-01-25")),
    ("Moai of Easter Island (Rapa Nui)", _v("LqQ-dymZQ9o",
        "Private collection obsidian mata'a from Easter Island",
        "2026-01-15")),
]

def main():
    sites = load('sites.json')
    videos = load('videos.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    print("=== NEW SITES ===")
    names = {s['n'] for s in sites}
    for s in NEW_SITES:
        if s['n'] in names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    print("\n=== VIDEO WIRES ===")
    names = {s['n'] for s in load('sites.json')}
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in names:
            print(f"  ✗ Missing site: {site_name}")
            continue
        videos.setdefault(site_name, [])
        existing = {x['id'] for x in videos[site_name]}
        if v['id'] in existing:
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            print(f"  ✓ Wired: {v['id']} → {site_name}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        country_map = {
            'Peru': ['Tarawasi'],
            'Cambodia': ['Phnom Bok'],
        }
        for country, items in country_map.items():
            countries.setdefault(country, [])
            for n in items:
                if n not in countries[country]:
                    countries[country].append(n)
        save('countries.json', countries)
        print("  ✓ Country tags updated")

    sites = load('sites.json')
    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
