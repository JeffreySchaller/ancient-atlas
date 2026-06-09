#!/usr/bin/env python3
"""
add-praveen-curated-batch.py

Curated Praveen Mohan additions — strict editorial filter applied to a
~250-video catalog. Only walkthroughs where (a) the title names a
specific archaeological site unambiguously and (b) the content is site
documentation rather than pure theory speculation. Provocative framing
on top of a real site walkthrough is permitted ("toe in the fringe" —
Jeff's editorial call); pure theory pieces, UFO/Anunnaki/Brahmastra
content, and iconography-only deep-dives without a specific site are
excluded.

NEW SITES (3):
    Phimai (Prasat Hin Phimai) — Thailand, Khmer 11th-12th c.
    Phanom Rung — Thailand, Khmer 10th-12th c.
    Banteay Samré — Cambodia, Angkor 12th c.

NEW WIRES (10):
    3 Phimai walkthroughs
    2 Phanom Rung walkthroughs
    1 Banteay Samré walkthrough
    1 additional Angkor Wat
    1 additional Hampi
    1 Phnom Bok (the world's largest lingam, framed as "Cosmic Antenna")
    1 Stonehenge cross-channel collaboration (Hugh Newman + Praveen)

Idempotent. Run from repo root:
    python3 scripts/add-praveen-curated-batch.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}")

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
    {"n": "Phimai (Prasat Hin Phimai)", "lat": 15.2206, "lng": 102.4953,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["precision", "polygonal", "geometry"],
     "desc": (
         "Largest Khmer sandstone temple complex in Thailand, located "
         "in Nakhon Ratchasima province. The architectural prototype "
         "for Angkor Wat. Built primarily during the reign of "
         "Jayavarman VI (late 11th c.) on the foundations of an "
         "earlier Mahayana Buddhist sanctuary, with massive sandstone "
         "blocks fitted to precision tolerances comparable to the "
         "Cuzco Inca walls. The site's central prang anchored the "
         "northern terminus of the Khmer royal road that ran south "
         "to Angkor. Independent investigators including Praveen "
         "Mohan have documented evidence of repeating tool-mark "
         "signatures that mainstream archaeology attributes to "
         "iron chisels but that some researchers argue are too "
         "uniform for hand work."
     ),
    },
    {"n": "Phanom Rung", "lat": 14.5328, "lng": 102.9408,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["precision", "geometry", "stratigraphy"],
     "desc": (
         "Khmer Hindu temple built on the rim of an extinct volcano "
         "in Buri Ram province, northeastern Thailand. Constructed "
         "between the 10th and 13th centuries from local pink "
         "sandstone and laterite, with the inner sanctuary dating "
         "to the reign of King Suryavarman II (early 12th c.). "
         "Famous for the solar alignment that admits sunlight "
         "directly through all 15 doorways of the inner shrine on "
         "four days each year — only documented in the modern era "
         "but clearly engineered into the original design. Bas-"
         "reliefs depict Vishnu Anantashayana and the Ramayana cycle."
     ),
    },
    {"n": "Banteay Samré", "lat": 13.4445, "lng": 103.9461,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal"],
     "desc": (
         "Outlying Khmer temple in the Angkor complex, Cambodia, "
         "approximately 400 m east of the East Baray reservoir. "
         "Stylistically and chronologically aligned with Angkor Wat "
         "(early 12th c., reign of Suryavarman II) and dedicated to "
         "Vishnu. Notable for its concentric enclosure walls and the "
         "preservation of its central sanctuary tower. The precision-"
         "cut sandstone blocks are fitted without mortar in the "
         "Angkor style. Smaller and less restored than Angkor Wat, "
         "which makes it a cleaner study of the unembellished "
         "construction technique."
     ),
    },
]

# ============================================================
def _v(vid, title, published="2025-01-01"):
    return {"id": vid, "title": title,
            "cr": "praveenmohan", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Phimai (new site, 3 wires) ===
    ("Phimai (Prasat Hin Phimai)", _v("KAqew1kywPw",
        "Phimai Temple - The Greatest Mystery of Thailand | Part 1 | Praveen Mohan",
        "2025-07-15")),
    ("Phimai (Prasat Hin Phimai)", _v("Zuj4A4yWzPc",
        "Evidence of Ancient Technology - Phimai Temple Part II, Thailand",
        "2025-08-20")),
    ("Phimai (Prasat Hin Phimai)", _v("MKkca7y7scI",
        "Was This Temple Built 12,000 Years Ago? Phimai Temple, Thailand | Part 3 | Praveen Mohan",
        "2025-09-25")),

    # === Phanom Rung (new site, 2 wires) ===
    ("Phanom Rung", _v("tGYWUc9BqHY",
        "Phanom Rung Temple - Ancient Underground Technology Uncovered?",
        "2025-10-10")),
    ("Phanom Rung", _v("W8TnK0x3ogY",
        "The Strangest Hindu Temple on Earth? Phanom Rung, Thailand | Praveen Mohan",
        "2025-10-20")),

    # === Banteay Samré (new site, 1 wire) ===
    ("Banteay Samré", _v("c8vMwkJSinI",
        "Ancient Stone Box Found in Cambodia? Mystery of Banteay Samré Temple",
        "2025-11-05")),

    # === Existing-site additions ===
    ("Phnom Bok", _v("SojXLgMn158",
        "10 Ton 'Cosmic Antenna' Found in Cambodia? World's Largest Lingam at Phnom Bok Mountain",
        "2025-09-10")),
    ("Angkor Wat", _v("exJMd8JBLhE",
        "This is inside the MAIN CHAMBER of Angkor Wat? Evidence of Ancient Technology",
        "2024-12-15")),
    ("Hampi", _v("360nASlkcf0",
        "Narasimha's Ancient Secrets Revealed? | Hampi",
        "2025-03-20")),

    # === Cross-channel collab (Hugh Newman x Praveen, Stonehenge) ===
    ("Stonehenge", _v("E8ADC7PwAZ8",
        "He Found England's Most Impossible Ancient Site | Hugh Newman Vs Praveen Mohan",
        "2026-06-03")),
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
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        print(f"  ⚠ Wire targets not found:")
        for m in missing:
            print(f"      {m}")

    videos_wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            continue
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            new_tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90:
                new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}{new_tag}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        country_map = {
            'Thailand': ['Phimai (Prasat Hin Phimai)', 'Phanom Rung'],
            'Cambodia': ['Banteay Samré'],
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
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {sites_added} new sites, {videos_wired} wires, {new_badges} fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
