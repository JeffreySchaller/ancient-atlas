#!/usr/bin/env python3
"""
add-bimini-batch.py — Bimini Road walkthrough fill.

Bimini Road already exists in the atlas (signal:open, scale + geometry
criteria) but had zero wires. This batch anchors it with two cleanly
opposing perspectives:

    Mystery History     — UMu3uccb-f4 — alt-history framing of the site
                          as suppressed evidence of pre-flood civilization
    National Geographic — v8xX6DgLwrE — institutional "The Truth Behind:
                          Atlantis" Mediterranean-tsunami episode that
                          features the Bimini dive expedition

Pairing them honors the editorial open-question stance: an alt-history
case and a mainstream-documentary case on the same screen, neither
allowed to monopolize the narrative.

NEW CREATORS (1):
    mysteryhistory — Mystery History, 594K subs, alt-history channel

NEW WIRES (2):
    Bimini Road × Mystery History
    Bimini Road × National Geographic

Idempotent. Run from repo root:
    python3 scripts/add-bimini-batch.py
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
    "mysteryhistory": {
        "name": "Mystery History",
        "handle": "@MysteryHistory",
        "subs": "Alt-history dives · pre-flood civilization framing",
        "color": "#7E6BAA",
        "tier": 3,
    },
}

def _v(vid, title, cr, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": cr, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Bimini Road", _v("UMu3uccb-f4",
        "The Bimini Road ~ Deliberately Hidden By Academia?",
        "mysteryhistory", "2018-06-15")),
    ("Bimini Road", _v("v8xX6DgLwrE",
        "Ancient Tsunami? | The Truth Behind: Atlantis",
        "natgeo", "2011-12-22")),
]

def main():
    creators = load('creators.json')
    sites = load('sites.json')
    videos = load('videos.json')

    print("=== NEW CREATORS ===")
    added_c = 0
    for k, v in NEW_CREATORS.items():
        if k in creators:
            print(f"  · Already exists: {k}")
        else:
            creators[k] = v
            added_c += 1
            print(f"  ✓ Added: {k} → {v['name']}")
    save('creators.json', creators)

    site_names = {s['n'] for s in sites}
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        sys.exit(f"✗ Missing sites: {missing}")

    print("\n=== VIDEO WIRES ===")
    wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if v['cr'] not in creators:
            print(f"  ✗ Missing creator for {v['id']}: {v['cr']}")
            continue
        videos.setdefault(site_name, [])
        if any(x['id'] == v['id'] for x in videos[site_name]):
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name} [{v['cr']}]")
    save('videos.json', videos)

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  This batch:         {added_c} new creators, {wired} wires")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
