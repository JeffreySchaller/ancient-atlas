#!/usr/bin/env python3
"""
add-tarawasi-peru.py — Add Tarawasi (Limatambo, Cusco, Peru) as a new
open-question megalithic site. Wire Cassie Coppersmith's Secrets in Stone
walkthrough featuring Brien Foerster's first-time visit.

Site:
  Tarawasi (also Tarahuasi, Terowasi) — megalithic ceremonial complex
  70 km west of Cusco at ~2,700 m elevation. Honeycomb-pattern outer
  wall of volcanic tuff with bent-corner precision. Central platform
  with 28 trapezoidal niches. Northeast-southwest orientation, off-axis
  from cardinal directions and shared with Machu Picchu / Cusco core /
  Sacsayhuamán. Damage on north-facing stones described by independent
  investigators as consistent with high-heat exposure. Conventional:
  mid-15th c. Inca tampu. Independent: pre-Inca megalithic core, later
  Inca and Spanish reuse. Only ONE official excavation (1934).
  No peer-reviewed papers. No radiocarbon dates.

Walkthrough:
  CUGsT9KKErE — Secrets in Stone, published ~2026-05-17
  (3 weeks before today's deploy). Will trigger NEW badge.

Creator key resolution:
  Attempts 'secretsinstone' first; falls back to a name-based lookup
  if that key doesn't exist.

Idempotent.

Run from the repo root:
    python3 scripts/add-tarawasi-peru.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()
PUBLISHED = "2026-05-17"  # "3 weeks ago" relative to 2026-06-07
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

# ============================================================
def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)

def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# ============================================================
# Resolve Secrets in Stone creator key
# ============================================================
creators = load('creators.json')
candidates = ['secretsinstone', 'secrets_in_stone', 'cassiec', 'sis', 'cassiecoppersmith']
SIS_KEY = None
for k in candidates:
    if k in creators:
        SIS_KEY = k
        break
if not SIS_KEY:
    # Fallback: search by name
    for k, c in creators.items():
        name = (c.get('name') or '').lower()
        if 'secret' in name and 'stone' in name:
            SIS_KEY = k
            break
if not SIS_KEY:
    sys.exit("Could not find Secrets in Stone in creators.json. "
             "Add the creator first or pass the correct key by editing "
             "candidates list above.")
print(f"  · Secrets in Stone creator key: {SIS_KEY!r}")

# ============================================================
NEW_SITES = [
    {
        "n": "Tarawasi",
        "lat": -13.4953,
        "lng": -72.4555,
        "cat": "megalithic",
        "region": "South America",
        "tier": 2,
        "signal": "open",
        "criteria": ["precision", "polygonal", "scale", "geometry"],
        "desc": (
            "Megalithic ceremonial complex 70 km west of Cusco in Limatambo, "
            "Anta Province, at 2,700 m elevation along the ancient Inca road "
            "system. The site centers on a 100-meter outer wall of meticulously "
            "fitted volcanic tuff blocks in a distinctive honeycomb pattern, with "
            "bent-corner joinery comparable to the highest-quality work in the "
            "Cusco megalithic sector. A raised central platform carries 28 "
            "trapezoidal niches and shows unusual flaking and peeling damage on "
            "its north-facing stones, described by independent investigators as "
            "consistent with high-heat exposure rather than ordinary weathering. "
            "The complex is oriented northeast-southwest rather than to cardinal "
            "directions, sharing this off-axis alignment with Machu Picchu, parts "
            "of Cusco itself, and Sacsayhuamán. Conventional reading : mid-15th "
            "century Inca tampu (way station). Independent reading : pre-Inca "
            "megalithic core, adopted by the Inca and later reused by Spanish "
            "colonial builders who incorporated megalithic blocks into their "
            "hosienda foundations. Only ONE official excavation has been conducted "
            "(1934), no artifacts published. There are no peer-reviewed papers on "
            "the site and no radiocarbon dates. The official chronology rests "
            "entirely on architectural comparison and the site's position along a "
            "known Inca road."
        ),
    },
]

VIDEOS_TO_WIRE = [
    ("Tarawasi", {
        "id": "CUGsT9KKErE",
        "title": "Megalithic Tarawasi: Peru's Hidden Mystery with Brien Foerster",
        "cr": SIS_KEY,
        "added": TODAY,
        "published": PUBLISHED,
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

    # Sites
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

    # Videos
    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Video {v['id']} already wired to {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}")
            print(f"     added={v['added']}, published={v['published']} (NEW badge will fire)")
    if videos_wired:
        save('videos.json', videos)

    # Country
    if isinstance(countries, dict):
        countries.setdefault('Peru', [])
        if 'Tarawasi' not in countries['Peru']:
            countries['Peru'].append('Tarawasi')
            save('countries.json', countries)
            print(f"  ✓ Peru tagged with Tarawasi")

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
