#!/usr/bin/env python3
"""
creator-sweep-batch.py — Big batch from the creator sweep.

Adds:
  2 NEW SITES:
    - Kbal Spean (Cambodia) - underwater lingam complex, Phnom Kulen
    - Phnom Bok (Cambodia) - hilltop temple with megalithic links
  1 NEW CREATOR:
    - SOLSTICE HUNTER (@SOLSTICEHUNTER)
  7 NEW WALKTHROUGHS WIRED:
    1. Lkt0N6jJvOY  → Kbal Spean (Praveen Mohan)
    2. zXNfDtAIa1Q  → Phnom Bok (SOLSTICE HUNTER)
    3. Vgy394g7S9g  → Spean Praptos (Praveen Fire Serpent — 2nd take)
    4. o06h0PhNWPY  → Tell el Roba (Mendes) (UnchartedX)
    5. VD1BIZCB-TA  → Nabta Playa (Hugh Newman / Robert Bauval interview)
    6. sFA7vf1Z2vQ  → Baalbek (Heliopolis) (UIY)
    7. G-f0KpxtOX4  → Hattusa (Brien Foerster)

All videos tagged with `added` (today) and `published` (verified from YouTube).
Recent ones (within 90 days of today) trigger the NEW badge.

Idempotent.

Run from the repo root:
    python3 scripts/creator-sweep-batch.py
"""
import json, sys, datetime, subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

TODAY = datetime.date.today().isoformat()

VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

# ============================================================
# NEW SITES
# ============================================================
NEW_SITES = [
    {
        "n": "Kbal Spean (Valley of a Thousand Lingams)",
        "lat": 13.6111,
        "lng": 104.0750,
        "cat": "megalithic",
        "region": "Asia",
        "tier": 2,
        "signal": "open",
        "criteria": ["precision", "scale", "geometry"],
        "desc": "Riverbed of carved sandstone in the Phnom Kulen mountains north of Angkor, where over a thousand Shiva lingams and yonis are cut directly into the living bedrock of the Stung Kbal Spean. Dated to the late 11th-early 12th century under King Suryavarman I. The carvings descend into and beneath the moving water, polished by centuries of flow yet retaining sharp precision-cylindrical and rectangular geometry. The site's purpose remains active : local pilgrims still light candles at specific lingams, and downstream water from Phnom Kulen feeds the Angkor temple complex hydrology. Independent investigators read the geometry as an engineered hydraulic system. Conventional archaeology reads it as a sacred Hindu site sanctifying water before it reaches the capital."
    },
    {
        "n": "Phnom Bok",
        "lat": 13.4667,
        "lng": 104.0167,
        "cat": "temple",
        "region": "Asia",
        "tier": 3,
        "signal": "open",
        "criteria": ["polygonal", "geometry"],
        "desc": "Late-9th-century hilltop temple at 235 meters above the Angkor plain, built by Yasovarman I around 900 CE atop a 750-foot sandstone hill. Three brick prasats arranged in a row dedicated to the Hindu trinity, with carved sandstone elements and a colossal lingam over four meters tall. The hill itself shows what some independent investigators describe as 'mini megalithic' stonework patterns that echo signatures found at distant sites on other continents. Conventional reading : standard early-Angkorian temple-mountain. Independent reading : the substrate carvings predate the Khmer construction and link to a broader pre-Angkorian network."
    },
]

# ============================================================
# NEW CREATOR
# ============================================================
NEW_CREATORS = {
    "solsticehunter": {
        "name": "SOLSTICE HUNTER",
        "handle": "@SOLSTICEHUNTER",
        "subs": "boots-on-ground megalithic field documentation, cross-continental signatures",
        "color": "#8B7DB8",
        "tier": 3
    }
}

# ============================================================
# VIDEOS TO WIRE
# Format: (site_name, video_dict)
# ============================================================
VIDEOS_TO_WIRE = [
    # 1. Kbal Spean — Praveen Lingam video
    ("Kbal Spean (Valley of a Thousand Lingams)", {
        "id": "Lkt0N6jJvOY",
        "title": "It's NOT Human: I Found an Active UFO Nuclear Reactor | Ravana's Lingam Exposed!",
        "cr": "praveenmohan",
        "added": TODAY,
        "published": "2026-04-26"
    }),
    # 2. Phnom Bok — SOLSTICE HUNTER
    ("Phnom Bok", {
        "id": "zXNfDtAIa1Q",
        "title": "Proof of Ancient Global Civilization - Finding Mini Megaliths at Phnom Bok, Cambodia",
        "cr": "solsticehunter",
        "added": TODAY,
        "published": "2026-05-26"
    }),
    # 3. Spean Praptos — Praveen Fire Serpent (2nd Praveen video on same site)
    ("Spean Praptos (Kampong Kdei Bridge)", {
        "id": "Vgy394g7S9g",
        "title": "The Rare 'Fire Serpent' Bridge of Cambodia | Praveen Mohan",
        "cr": "praveenmohan",
        "added": TODAY,
        "published": "2026-05-30"
    }),
    # 4. Tell el Roba (Mendes) — UnchartedX
    ("Tell el Roba (Mendes)", {
        "id": "o06h0PhNWPY",
        "title": "Finding More Than We Expected at the Rarely-Seen Ancient Megalithic Site of Mendes!",
        "cr": "unchartedx",
        "added": TODAY,
        "published": "2026-05-28"
    }),
    # 5. Nabta Playa — Hugh Newman / Bauval interview
    ("Nabta Playa", {
        "id": "VD1BIZCB-TA",
        "title": "Robert Bauval | Nabta Playa and the Origins of Egypt | Megalithomania Interview",
        "cr": "megalithomania",
        "added": TODAY,
        "published": "2026-05-25"
    }),
    # 6. Baalbek — UIY
    ("Baalbek (Heliopolis)", {
        "id": "sFA7vf1Z2vQ",
        "title": "Gigantic Ancient Structure our Technology Can't Replicate: Baalbek",
        "cr": "universeinside",
        "added": TODAY,
        "published": "2026-04-19"
    }),
    # 7. Hattusa — Brien Foerster
    ("Hattusa", {
        "id": "G-f0KpxtOX4",
        "title": "Ancient Hattusa In Turkey",
        "cr": "brienf",
        "added": TODAY,
        "published": "2026-05-01"
    }),
]

# ============================================================
def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)

def save_json(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def main():
    if not DATA_DIR.exists():
        sys.exit(f"data/ not found at {DATA_DIR}")

    # Validate criteria
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load_json('sites.json')
    videos = load_json('videos.json')
    creators = load_json('creators.json')
    countries = load_json('countries.json')
    site_names = {s['n'] for s in sites}

    # --- 1. Add creators ---
    creators_added = 0
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · Creator '{key}' already exists")
        else:
            creators[key] = info
            creators_added += 1
            print(f"  ✓ Added creator: {key} ({info['name']})")
    if creators_added:
        save_json('creators.json', creators)

    # --- 2. Add sites ---
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added site: {s['n']}")
            print(f"     signal={s.get('signal','convergent')}, criteria={s.get('criteria',[])}")
    if sites_added:
        save_json('sites.json', sites)

    # --- 3. Verify all creator refs in videos ---
    creators = load_json('creators.json')  # reload after adding
    for site_name, v in VIDEOS_TO_WIRE:
        if v['cr'] not in creators:
            sys.exit(f"✗ Video {v['id']} references unknown creator '{v['cr']}'")

    # --- 4. Wire videos ---
    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            # Update if missing dates
            for x in videos[site_name]:
                if x['id'] == v['id']:
                    updated = False
                    if not x.get('added'):
                        x['added'] = v['added']; updated = True
                    if not x.get('published'):
                        x['published'] = v['published']; updated = True
                    if updated:
                        print(f"  ↻ Updated dates on existing video {v['id']} → {site_name[:40]}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name[:40]} (pub: {v['published']})")
    if videos_wired or any(True for s, v in VIDEOS_TO_WIRE):
        save_json('videos.json', videos)

    # --- 5. Country tagging ---
    if isinstance(countries, dict):
        for s in NEW_SITES:
            countries.setdefault('Cambodia', [])
            if s['n'] not in countries['Cambodia']:
                countries['Cambodia'].append(s['n'])
        save_json('countries.json', countries)
        print(f"  ✓ Cambodia now has {len(countries.get('Cambodia', []))} sites")

    # --- Summary ---
    sites = load_json('sites.json')
    videos = load_json('videos.json')
    creators = load_json('creators.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")

    # --- Build ---
    print("\nRunning build.py…")
    r = subprocess.run(['python3', str(REPO_ROOT / 'scripts' / 'build.py')], capture_output=True, text=True)
    print(r.stdout[-400:])
    if r.returncode != 0:
        print("BUILD FAILED:", r.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
