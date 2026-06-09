#!/usr/bin/env python3
"""
wire-myra-proto-civilization.py — Add Proto Civilization's Myra
walkthrough to the Myra atlas entry.

Video: 0_3rITmJwsc — "Forbidden Tombs of the Giants. World | s03e12"
Covers the "other side" of Myra mountain (Lycian rock-cut tombs in
southern Turkey) where tourists are not allowed. Part of the channel's
Turkey series, auto-dubbed in English.

Idempotent. Run from repo root:
    python3 scripts/wire-myra-proto-civilization.py
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
    "id": "0_3rITmJwsc",
    "title": "Forbidden Tombs of the Giants. World | s03e12 (Proto Civilization, ru/en dub) — the off-limits side of Myra mountain",
    "cr": "protocivilization",
    "added": TODAY,
    "published": "2022-10-15",
}
SITE = "Myra"

def main():
    sites = load('sites.json')
    if not any(s['n'] == SITE for s in sites):
        sys.exit(f"✗ Site '{SITE}' not found")

    creators = load('creators.json')
    if 'protocivilization' not in creators:
        sys.exit(f"✗ Creator 'protocivilization' not found — run add-proto-civilization-batch.py first")

    videos = load('videos.json')
    videos.setdefault(SITE, [])
    if any(v['id'] == VIDEO['id'] for v in videos[SITE]):
        print(f"  · Already wired: {VIDEO['id']} → {SITE}")
    else:
        videos[SITE].append(VIDEO)
        save('videos.json', videos)
        print(f"  ✓ Wired: {VIDEO['id']} → {SITE}")

    total = sum(len(v) for v in load('videos.json').values())
    print(f"\n--- summary ---")
    print(f"  Total walkthroughs: {total}")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
