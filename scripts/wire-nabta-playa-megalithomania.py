#!/usr/bin/env python3
"""
wire-nabta-playa-megalithomania.py — Add the Megalithomania (Hugh Newman)
walkthrough of Nabta Playa to the Nabta Playa atlas entry.

Video: qR23zjLwYvM — "Nabta Playa | 8000 Year Old Stone Circles in
Southern Egypt & the Orion Connection | Megalithomania"

Idempotent. Run from repo root:
    python3 scripts/wire-nabta-playa-megalithomania.py
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

VIDEO = {
    "id": "qR23zjLwYvM",
    "title": "Nabta Playa | 8000 Year Old Stone Circles in Southern Egypt & the Orion Connection | Megalithomania",
    "cr": "megalithomania",
    "added": TODAY,
    "published": "2023-08-15",
}
SITE = "Nabta Playa"

def main():
    sites = load('sites.json')
    if not any(s['n'] == SITE for s in sites):
        sys.exit(f"✗ Site '{SITE}' not found in sites.json")

    videos = load('videos.json')
    videos.setdefault(SITE, [])
    if any(v['id'] == VIDEO['id'] for v in videos[SITE]):
        print(f"  · Already wired: {VIDEO['id']} → {SITE}")
    else:
        videos[SITE].append(VIDEO)
        print(f"  ✓ Wired: {VIDEO['id']} → {SITE}")
        save('videos.json', videos)

    total_videos = sum(len(v) for v in load('videos.json').values())
    print(f"\n--- summary ---")
    print(f"  Total walkthroughs: {total_videos}")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
