#!/usr/bin/env python3
"""
add-ancientatlas-fieldwork-batch.py — first-party fieldwork wires.

The atlas becomes a creator in its own dataset: Ancient Atlas channel
episodes wire to their site cards exactly like every other creator.
No special treatment (editorial pattern: first-party walkthroughs follow
the same rules; signal:open cards keep their paired perspectives).

Channel: https://www.youtube.com/@AncientAtlasMap
Creator key: ancientatlas · tier 1 · champagne (#C9A84C, the brand token)

WIRES (verified live on channel):
    Ep01  bnslsxXi3RY  Derinkuyu Underground City — published 2026-06-10
    (Ep02+ append here as they publish: Osireion, Osiris Shaft,
    Serapeum, Great Pyramid, Step Pyramid of Djoser, Unfinished
    Obelisk (Aswan). One entry per episode, same pattern.)

Idempotent. Run from repo root:
    python3 scripts/add-ancientatlas-fieldwork-batch.py
    python3 scripts/build.py
"""
import sys, json, datetime
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

NEW_CREATORS = {
    "ancientatlas": {
        "name": "Ancient Atlas",
        "handle": "@AncientAtlasMap",
        "subs": "First-party fieldwork · the channel of theancientatlas.com",
        "color": "#C9A84C",
        "tier": 1,
    },
}

def _v(vid, title, published):
    return {"id": vid, "title": title,
            "cr": "ancientatlas", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Derinkuyu Underground City", _v("bnslsxXi3RY",
        "Derinkuyu Underground City | Fieldwork Walkthrough · Türkiye",
        "2026-06-10")),
]

def main():
    creators = load('creators.json')
    videos = load('videos.json')
    sites = load('sites.json')
    site_names = {s['n'] for s in sites}

    print("=== CREATOR ===")
    added_c = 0
    for k, v in NEW_CREATORS.items():
        if k in creators:
            print(f"  · Already exists: {k}")
        else:
            creators[k] = v
            added_c += 1
            print(f"  ✓ Added: {k} → {v['name']}")
    save('creators.json', creators)

    print("\n=== FIRST-PARTY WIRES ===")
    wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            print(f"  ✗ Missing site: {site_name}")
            continue
        videos.setdefault(site_name, [])
        if any(x['id'] == v['id'] for x in videos[site_name]):
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name} [ancientatlas]")
    save('videos.json', videos)

    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(load('creators.json'))}")
    print(f"  This batch:         {added_c} new creators, {wired} wires")

if __name__ == "__main__":
    main()
