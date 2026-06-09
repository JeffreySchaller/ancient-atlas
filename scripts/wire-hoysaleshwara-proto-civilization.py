#!/usr/bin/env python3
"""
wire-hoysaleshwara-proto-civilization.py — Add Proto Civilization's
Halebidu (Hoysaleshwara Temple) walkthrough to the atlas.

Video: bWbFXdfUetE — "Living History in Stone | Halibidou | The Ruined City"
("Halibidou" is the channel's transliteration of Halebidu, the 12th-c.
Hoysala capital in Karnataka, India, home to Hoysaleshwara Temple.)

Proto Civilization questions the tool used to produce the temple's
extraordinarily intricate carving. Notable for editorial discipline:
they explicitly rule out 'laser technology' speculation while
documenting that the conventional iron-chisel explanation does not
account for the precision observed.

Idempotent. Run from repo root:
    python3 scripts/wire-hoysaleshwara-proto-civilization.py
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
    "id": "bWbFXdfUetE",
    "title": "Living History in Stone | Halibidou | The Ruined City (Proto Civilization, ru/en dub) — Hoysaleshwara Temple, Halebidu, Karnataka",
    "cr": "protocivilization",
    "added": TODAY,
    "published": "2021-06-15",
}
SITE = "Hoysaleshwara Temple"

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
