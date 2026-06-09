#!/usr/bin/env python3
"""
add-proto-civilization-batch.py — Add Proto Civilization / ПротоЦивилизация
as a creator and wire 6 high-value videos.

Proto Civilization is a Russian-language YouTube channel doing empirical
experimental archaeology — they run the experiments that other channels
only speculate about. Auto-dubbed to English. The basalt experiment
video is the centerpiece: a real-life attempt to carve into basalt with
modern steel tools near Kailasa, which the researchers conclude renders
the conventional hand-chisel explanation mathematically impossible.

This batch deliberately skips the channel's Russian-Imperial alternate-
history thread (Hermitage, Petergof, Kronstadt "Baalbek," St. Petersburg
"alien granite") since it doesn't fit the atlas editorial frame.

CREATOR:
    protocivilization — Proto Civilization · @ProtoCivilization
    Empirical experimental archaeology · Russian, auto-dubbed in English

WIRES (6):
    Kailasa Temple (Ellora) × 3 — basalt experiment + Part 1 + Part 2
    Barabar Caves × 1 — Documentary
    Unfinished Obelisk (Aswan) × 1 — Aswan Quarry 3D doc
    Dendera Temple Complex × 1 — Hathor Temple "secret knowledge"

Idempotent. Run from repo root:
    python3 scripts/add-proto-civilization-batch.py
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

CREATOR_KEY = "protocivilization"
CREATOR = {
    "name": "Proto Civilization",
    "handle": "@ProtoCivilization",
    "subs": "Experimental archaeology · Russian, auto-dubbed · runs the tests others only theorize about",
    "color": "#8AB0D1",
    "tier": 2,
}

def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": CREATOR_KEY, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Kailasa Temple (Ellora) ===
    # The basalt experiment — the centerpiece. Empirical test of whether
    # modern steel can replicate the ancient tool marks. It cannot.
    ("Kailasa Temple (Ellora Cave 16)", _v("CM7l7g66BWs",
        "Is it possible to carve a temple in basalt? A real-life experiment",
        "2026-03-15")),
    ("Kailasa Temple (Ellora Cave 16)", _v("9PvgLjpjGjo",
        "Kailasa: The most inexplicable temple on Earth | Documentary Part 1 (Каилас, ru/en dub)",
        "2026-05-10")),
    ("Kailasa Temple (Ellora Cave 16)", _v("Rs2Af40D1Ig",
        "Kailasa. The Lost World in the Rocks | Documentary Part 2",
        "2026-05-20")),

    # === Barabar Caves ===
    ("Barabar Caves", _v("wbK0cK9U19g",
        "The Forbidden Caves of India: Barabar | Documentary (Запретные пещеры Индии, ru/en dub)",
        "2024-12-10")),

    # === Aswan ===
    ("Unfinished Obelisk (Aswan)", _v("A-wTHDMLSAk",
        "More mysterious than the pyramids: the Aswan Quarry 3D | Documentary (ru/en dub)",
        "2024-09-20")),

    # === Dendera (Hathor) ===
    ("Dendera Temple Complex", _v("b_dYzSmcMso",
        "Secret knowledge of ancient Egypt: Temple of Hathor Part 1 (Тайное знание древнего Египта, ru/en dub)",
        "2025-02-08")),
]

def main():
    sites = load('sites.json')
    site_names = {s['n'] for s in sites}

    # Check all wire targets exist
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        sys.exit(f"✗ Missing sites: {missing}")

    # Add creator
    creators = load('creators.json')
    if CREATOR_KEY in creators:
        print(f"  · Creator '{CREATOR_KEY}' already exists")
    else:
        creators[CREATOR_KEY] = CREATOR
        save('creators.json', creators)
        print(f"  ✓ Added creator: {CREATOR_KEY} → {CREATOR['name']}")

    # Wire videos
    print("\n=== VIDEO WIRES ===")
    videos = load('videos.json')
    wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        if any(x['id'] == v['id'] for x in videos[site_name]):
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90:
                new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}{tag}")
    save('videos.json', videos)

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         1 new creator, {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
