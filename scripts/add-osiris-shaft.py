#!/usr/bin/env python3
"""
add-osiris-shaft.py — Add the Osiris Shaft at Giza as a new atlas site
and wire Proto Civilization's "Giza Underground" walkthrough.

The Osiris Shaft is a deep three-level vertical shaft cut into the
bedrock beneath the Khafre causeway on the Giza Plateau. The upper
levels were first investigated in modern times by Selim Hassan
(1934). The lowest level — containing a black basalt sarcophagus
surrounded by water channels (the "Tomb of Osiris" chamber) — was
fully excavated by Zahi Hawass in 1999. The shaft is normally closed
to the public.

NEW SITE: Osiris Shaft (Giza Plateau)
WIRE:     hxq5QhSjX-g — Proto Civilization "Giza Underground: The
          Osiris Shaft and the Plateau's Forgotten Architecture"

Idempotent. Run from repo root:
    python3 scripts/add-osiris-shaft.py
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

NEW_SITE = {
    "n": "Osiris Shaft (Giza)",
    "lat": 29.9755,
    "lng": 31.1330,
    "cat": "underground",
    "region": "Egypt",
    "tier": 1,
    "signal": "open",
    "criteria": ["precision", "scale", "stratigraphy"],
    "desc": (
        "Three-level vertical shaft cut into the bedrock beneath the "
        "Khafre causeway on the Giza Plateau. The upper opening was "
        "investigated by Selim Hassan in 1934; the deepest chamber, "
        "30 meters below the surface, was fully excavated by Zahi "
        "Hawass in 1999. The lowest level contains a black basalt "
        "sarcophagus mounted at the center of a rock-cut platform, "
        "surrounded by a moat of standing groundwater fed by the "
        "aquifer beneath the plateau — the famous 'Tomb of Osiris' "
        "chamber. The shaft is conventionally dated to the Late "
        "Period (c. 600 BCE) on the basis of the sarcophagus and "
        "associated pottery, but the depth of the cut, the precision "
        "of the chambers, and the integration with the rest of the "
        "subterranean Giza system have led independent investigators "
        "to propose a substantially earlier origin date. Currently "
        "closed to the public."
    ),
}

VIDEO = {
    "id": "hxq5QhSjX-g",
    "title": "Giza Underground: The Osiris Shaft and the Plateau's Forgotten Architecture (Proto Civilization, ru/en dub)",
    "cr": "protocivilization",
    "added": TODAY,
    "published": "2020-08-15",
}

def main():
    invalid = [c for c in NEW_SITE.get('criteria', []) if c not in VALID_CRITERIA]
    if invalid:
        sys.exit(f"✗ Invalid criteria: {invalid}")

    sites = load('sites.json')
    creators = load('creators.json')
    if 'protocivilization' not in creators:
        sys.exit("✗ Creator 'protocivilization' not found — run add-proto-civilization-batch.py first")

    site_names = {s['n'] for s in sites}
    if NEW_SITE['n'] in site_names:
        print(f"  · Site already exists: {NEW_SITE['n']}")
    else:
        sites.append(NEW_SITE)
        save('sites.json', sites)
        print(f"  ✓ Added site: {NEW_SITE['n']}")

    videos = load('videos.json')
    videos.setdefault(NEW_SITE['n'], [])
    if any(v['id'] == VIDEO['id'] for v in videos[NEW_SITE['n']]):
        print(f"  · Already wired: {VIDEO['id']}")
    else:
        videos[NEW_SITE['n']].append(VIDEO)
        save('videos.json', videos)
        print(f"  ✓ Wired: {VIDEO['id']} → {NEW_SITE['n']}")

    try:
        countries = load('countries.json')
        if isinstance(countries, dict):
            countries.setdefault('Egypt', [])
            if NEW_SITE['n'] not in countries['Egypt']:
                countries['Egypt'].append(NEW_SITE['n'])
                save('countries.json', countries)
                print(f"  ✓ Tagged under Egypt")
    except FileNotFoundError:
        pass

    sites = load('sites.json')
    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
