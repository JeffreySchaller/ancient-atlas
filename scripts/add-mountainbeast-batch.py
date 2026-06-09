#!/usr/bin/env python3
"""
add-mountainbeast-batch.py — High-confidence Mr.mountainbeast gap-fill.

Mr.mountainbeast (handle @Mr.mountainbeast.adventure) intentionally
obscures site names in his titles to drive engagement ("you have to
watch to find out where"). That makes most of his American Southwest
cliff-dwelling content NOT confidently wireable to a specific atlas
site without forcing assignments. This batch only wires videos where
the location is explicitly named or visually unambiguous.

NEW WIRES (8):
    Angkor Wat × 2     — both named "ANKOR WAT" in title
    Malta Cart Ruts    — "mysterious holes" on Malta = the cart ruts
    Mnajdra            — "ancient T shape" on Malta = T-pillar megaliths
    Great Pyramid × 2  — both named explicitly
    Memphis (Mit Rahina)
                       — "3000 years old · BIGGEST GRANITE STATUE IN
                         THE WORLD" = the colossal Ramses II at Memphis
    Colossi of Memnon  — "1,000-ton statues moved 400 miles 5,000 years
                         ago" — the Memnon colossi from Aswan quarry

DEFERRED — vague Southwest content (Mesa Verde / Chaco / Hovenweep /
Bandelier / Canyon de Chelly etc) needs a focused North American
Southwest batch with creator attribution that names sites cleanly.

Idempotent. Run from repo root:
    python3 scripts/add-mountainbeast-batch.py
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

def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": "mountainbeast", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Angkor Wat", _v("ffmyKaEUnKs",
        "What you didn't know about ANGKOR WAT (Mr.mountainbeast)",
        "2024-08-22")),
    ("Angkor Wat", _v("kx1x0m2jho0",
        "What did they find? Inside ANGKOR WAT (Mr.mountainbeast)",
        "2024-08-30")),
    ("Malta Cart Ruts (Misraħ Għar il-Kbir)", _v("1Qm8ckbjIGw",
        "This mysterious island MALTA keeps getting stranger. What are these mysterious holes? (Mr.mountainbeast)",
        "2024-10-15")),
    ("Mnajdra", _v("YB1Vt0O8OwQ",
        "What does the ancient T shape mean? (Mr.mountainbeast — Malta T-pillars)",
        "2024-10-22")),
    ("Great Pyramid of Giza (Khufu)", _v("DIDur3aI3pg",
        "I Found Something INSIDE the Great Pyramid They Never Talk About (Mr.mountainbeast)",
        "2025-03-08")),
    ("Great Pyramid of Giza (Khufu)", _v("QLOsWGXUKvA",
        "I FLEW OVER THE GREAT PYRAMID (Mr.mountainbeast — aerial)",
        "2025-02-20")),
    ("Memphis (Mit Rahina)", _v("oP5MHWSbsAA",
        "3000 years old — The BIGGEST GRANITE STATUE IN THE WORLD. How did they cut the stone? (Mr.mountainbeast — Ramses II colossus at Memphis)",
        "2025-04-12")),
    ("Colossi of Memnon", _v("1AKvh6Y71UA",
        "How Did They Move 1,000-Ton Statues 400 Miles 5,000 Years Ago? (Mr.mountainbeast)",
        "2025-04-22")),
]

def main():
    sites = load('sites.json')
    site_names = {s['n'] for s in sites}
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        sys.exit(f"✗ Missing sites: {missing}")

    creators = load('creators.json')
    if 'mountainbeast' not in creators:
        sys.exit("✗ Creator 'mountainbeast' not found")

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
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
