#!/usr/bin/env python3
"""
wire-cappadocia-pair-2.py — Wire two more Cappadocia Page Turkey
walkthroughs.

  Derinkuyu Underground City (already in atlas, 0 videos):
    qAx8NbA5Y0E — pub 2026-05-01 → NEW badge will fire

  Nevşehir Underground City (already in atlas, 1 video from prior batch):
    6f4qG6QxSfI — pub 2025-11-10 → Kayaşehir is the Turkish name for
    the same 2014-discovered complex beneath Nevşehir Castle

Both videos use the cappadociapage creator key from the prior batch.

Idempotent. Run from the repo root:
    python3 scripts/wire-cappadocia-pair-2.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

VIDEOS_TO_WIRE = [
    ("Derinkuyu Underground City", {
        "id": "qAx8NbA5Y0E",
        "title": "Cappadocia Derinkuyu Underground City: Secrets Hidden in the Depths",
        "cr": "cappadociapage",
        "added": TODAY,
        "published": "2026-05-01",
    }),
    ("Nevşehir Underground City", {
        "id": "6f4qG6QxSfI",
        "title": "Kayaşehir Nevsehir Underground World – Hidden Secrets Beneath Cappadocia, Turkey",
        "cr": "cappadociapage",
        "added": TODAY,
        "published": "2025-11-10",
    }),
]

def main():
    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')

    site_names = {s['n'] for s in sites}
    for site_name, _ in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            sys.exit(f"✗ Site not found: {site_name!r}. "
                     "Run wire-cappadocia-underground.py first.")

    for _, v in VIDEOS_TO_WIRE:
        if v['cr'] not in creators:
            sys.exit(f"✗ Creator {v['cr']!r} not found. "
                     "Run wire-cappadocia-underground.py first to add it.")

    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            new_flag = "→ NEW badge" if pub_days <= 90 else ""
            print(f"  ✓ Wired: {v['id']} → {site_name}  ({pub_days}d ago) {new_flag}")
    if videos_wired:
        save('videos.json', videos)

    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Derinkuyu videos:   {len(videos.get('Derinkuyu Underground City', []))}")
    print(f"  Nevşehir videos:    {len(videos.get('Nevşehir Underground City', []))}")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
