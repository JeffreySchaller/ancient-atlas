#!/usr/bin/env python3
"""
wire-yonaguni-expedition-unknown.py — Add Expedition Unknown (Josh Gates /
Discovery Channel) as a creator and wire his Yonaguni S2E7 episode.

Adds:
    Creator: expeditionunknown — Expedition Unknown w/ Josh Gates
    Wire:    uVIzFm_PzcM → Yonaguni Monument
             "Japan's Underwater City Found? | Expedition Unknown S2 E7"

Idempotent. Run from repo root:
    python3 scripts/wire-yonaguni-expedition-unknown.py
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

CREATOR_KEY = "expeditionunknown"
CREATOR = {
    "name": "Expedition Unknown",
    "handle": "@DiscoveryChannelIndia",
    "subs": "Josh Gates · Discovery Channel · field-led investigations of ancient sites",
    "color": "#E0944F",
    "tier": 2,
}

VIDEO = {
    "id": "uVIzFm_PzcM",
    "title": "Japan's Underwater City Found? | Expedition Unknown S2 E7 | Discovery Channel India",
    "cr": CREATOR_KEY,
    "added": TODAY,
    "published": "2017-06-28",
}
SITE = "Yonaguni Monument"

def main():
    sites = load('sites.json')
    if not any(s['n'] == SITE for s in sites):
        sys.exit(f"✗ Site '{SITE}' not found in sites.json")

    # Add creator if missing
    creators = load('creators.json')
    if CREATOR_KEY in creators:
        print(f"  · Creator '{CREATOR_KEY}' already exists")
    else:
        creators[CREATOR_KEY] = CREATOR
        save('creators.json', creators)
        print(f"  ✓ Added creator: {CREATOR_KEY} → {CREATOR['name']}")

    # Wire the video
    videos = load('videos.json')
    videos.setdefault(SITE, [])
    if any(v['id'] == VIDEO['id'] for v in videos[SITE]):
        print(f"  · Already wired: {VIDEO['id']} → {SITE}")
    else:
        videos[SITE].append(VIDEO)
        save('videos.json', videos)
        print(f"  ✓ Wired: {VIDEO['id']} → {SITE}")

    total_creators = len(load('creators.json'))
    total_videos = sum(len(v) for v in load('videos.json').values())
    print(f"\n--- summary ---")
    print(f"  Total creators:     {total_creators}")
    print(f"  Total walkthroughs: {total_videos}")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
