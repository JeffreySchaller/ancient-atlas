#!/usr/bin/env python3
"""
wire-cappadocia-underground.py — Wire two walkthroughs onto existing
Cappadocia underground city sites. Adds two new creators.

Both existing sites have zero walkthroughs wired — these are the first.

Site 1: Özkonak Underground City (already in atlas)
  - HISTORY Channel, Cities of the Underworld S1, "Secrets of the Ancient Metropolis"
  - HJ2LNYUV0SA, published 2021-10-20
  - Covers the 1972 farmer-discovers-water-draining story (Latif Acar at Özkonak)
  - Andrew Collins + Martin Sweatman invoked for pre-Hittite / Younger Dryas reading
  - Connects Cappadocia underground network to Göbekli Tepe and the late-Pleistocene
    comet-impact hypothesis (Sweatman's Vulture Stone work)

Site 2: Nevşehir Underground City (already in atlas)
  - Cappadocia Page Turkey, small local channel (~2.16K subs)
  - 9lCxDgCd7dc, published ~2025 (1 year ago)
  - Tunnel-and-chamber walkthrough of the Nevşehir Castle underground complex
    (largest underground city found to date; discovered ~2014 during construction)

Two new creators:
  - history: HISTORY Channel (mainstream documentary, tier 2)
  - cappadociapage: Cappadocia Page Turkey (small local channel, tier 3)

Neither video qualifies for NEW badge (both too old by published date), but
both will surface in the Creator Hub Latest sort.

Idempotent.

Run from the repo root:
    python3 scripts/wire-cappadocia-underground.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()

# ============================================================
def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

NEW_CREATORS = {
    "history": {
        "name": "HISTORY",
        "handle": "@HISTORY",
        "subs": "mainstream documentary network; ancient civilizations + archaeology specials",
        "color": "#C9A84C",  # champagne — matches the network's gold-on-black H logo
        "tier": 2,
    },
    "cappadociapage": {
        "name": "Cappadocia Page Turkey",
        "handle": "@CappadociaPageTurkey",
        "subs": "small local channel documenting Cappadocia's underground cities and rock-cut sites",
        "color": "#A66B4A",  # cappadocian earth tone
        "tier": 3,
    },
}

VIDEOS_TO_WIRE = [
    ("Özkonak Underground City", {
        "id": "HJ2LNYUV0SA",
        "title": "Ancient Underground City Discovered in Turkey | Cities of the Underworld (Season 1) | History",
        "cr": "history",
        "added": TODAY,
        "published": "2021-10-20",
    }),
    ("Nevşehir Underground City", {
        "id": "9lCxDgCd7dc",
        "title": "Nevsehir Turkey Underground City | Cappadocia's Ancient Mystery",
        "cr": "cappadociapage",
        "added": TODAY,
        "published": "2025-05-01",
    }),
]

# ============================================================
def main():
    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')

    site_names = {s['n'] for s in sites}
    for site_name, _ in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            sys.exit(f"✗ Site not found in sites.json: {site_name!r}")

    # 1. Creators
    creators_added = 0
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · Creator '{key}' already exists")
        else:
            creators[key] = info
            creators_added += 1
            print(f"  ✓ Added creator: {key} ({info['name']})")
    if creators_added:
        save('creators.json', creators)

    # 2. Wire videos
    creators = load('creators.json')
    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if v['cr'] not in creators:
            sys.exit(f"✗ Video {v['id']} references unknown creator '{v['cr']}'")
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Video {v['id']} already wired to {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}")
            print(f"     pub: {v['published']} ({(datetime.date.today() - datetime.date.fromisoformat(v['published'])).days}d ago)")
    if videos_wired:
        save('videos.json', videos)

    # Summary
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
