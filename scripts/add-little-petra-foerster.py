#!/usr/bin/env python3
"""
add-little-petra-foerster.py

Adds Little Petra (Siq al-Barid) as a new atlas site and wires Brien
Foerster's field walkthrough to both Little Petra and Petra proper.

The video features close documentation of horizontal raking and parallel
groove tool marks on the Little Petra walls — the exact kinematic
signature anchored in Library Entry 04 §03 (the tool-mark anomaly).
Stills from this video are now embedded in the Entry 04 evidence strip.

Wires the True Monoliths library_ref onto the new Little Petra entry
since it meets the inclusion gate (machining marks documented).

Idempotent. Run from repo root:
    python3 scripts/add-little-petra-foerster.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

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
    {"n": "Little Petra (Siq al-Barid)", "lat": 30.3727, "lng": 35.4506,
     "cat": "rockcut", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["machining", "precision", "scale"],
     "library_ref": {
        "url": "/library/true-monoliths.html",
        "title": "True Monoliths",
     },
     "desc": (
         "Nabataean rock-cut complex 8 km north of Petra in Jordan. Known "
         "as Siq al-Barid (the 'cold canyon') for its narrow defile shaded "
         "from the sun. Conventionally dated to the 1st century CE as a "
         "caravan suburb of Petra, serving traders on the incense route. "
         "Features triclinia (dining halls), cisterns, a unique frescoed "
         "biclinium with surviving Hellenistic-style paintings, and a "
         "system of stairs and chambers carved directly into the sandstone "
         "cliffs. The interior wall surfaces preserve some of the clearest "
         "tool-mark evidence in the region : continuous diagonal raking, "
         "parallel vertical grooves running floor to ceiling without "
         "break, and curved sweeping arcs that do not match the chisel "
         "kinematics conventionally assigned to Nabataean stonecutting. "
         "Brien Foerster's field walkthrough documents the marks in close "
         "detail."
     ),
    },
]

# ============================================================
FOERSTER_VIDEO = {
    "id": "vVd-NOzPhC8",
    "title": "Little Petra : Strange Tool Marks in Stone | Brien Foerster",
    "cr": "brienfoerster", "added": TODAY, "published": "2025-09-01",
}
# Wire to Little Petra (new) + Petra (existing) — the marks at Little Petra
# are kinematically identical to marks observed in the main Petra complex
WIRES = [
    "Little Petra (Siq al-Barid)",
    "Petra",
]

# ============================================================
def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    # Ensure Brien Foerster creator exists (it should — used widely)
    if 'brienfoerster' not in creators:
        print("  ⚠ 'brienfoerster' creator not found in creators.json")
        print("    Expected to exist; please verify creator key naming")

    # Add Little Petra
    print("=== NEW SITE ===")
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

    # Wire video
    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in sites}
    videos_wired = 0
    new_badges = 0
    for site_name in WIRES:
        if site_name not in site_names:
            print(f"  ⚠ {site_name} not in sites — skipping")
            continue
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if FOERSTER_VIDEO['id'] in existing_ids:
            print(f"  · Already wired: {FOERSTER_VIDEO['id']} → {site_name}")
        else:
            videos[site_name].append(FOERSTER_VIDEO)
            videos_wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(FOERSTER_VIDEO['published'])).days
            new_tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90: new_badges += 1
            print(f"  ✓ Wired: {FOERSTER_VIDEO['id']} → {site_name}{new_tag}")
    if videos_wired:
        save('videos.json', videos)

    # Country tags
    if isinstance(countries, dict):
        countries.setdefault('Jordan', [])
        if 'Little Petra (Siq al-Barid)' not in countries['Jordan']:
            countries['Jordan'].append('Little Petra (Siq al-Barid)')
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated (Jordan +1)")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, {new_badges} fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
