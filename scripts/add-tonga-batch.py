#!/usr/bin/env python3
"""
add-tonga-batch.py — Tonga megalithic batch.

The atlas already has Ha'amonga 'a Maui (Tonga Trilithon) but with
zero wires. This batch fills it in and adds Tonga's second great
megalithic site cluster: the Langi pyramid platforms at Lapaha / Mu'a.

NEW SITES (1):
    Langi Pyramid Platforms (Lapaha)  — Tongatapu, Tonga

NEW CREATORS (3):
    onceuponasaga         — Thor Pedersen, "Once Upon A Saga" travel project
    magneticreversalnews  — Diamond's weathering-rates / alt-dating analysis
    horsfrontieres        — Hors Frontières, French world-tour channel

NEW WIRES (4):
    Ha'amonga 'a Maui (Tonga Trilithon):
        Thor Pedersen        — qfu9tb9SXbM (Sep 2022)
        Hors Frontières      — 2JzwQeNzQr4 (Nov 2015)
        Magnetic Reversal    — pt-BkEaamCg (weathering re-dating, 2022)
    Langi Pyramid Platforms (Lapaha):
        Hugh Newman / MegalithomaniaUK — Fdi1dcT3ofE (Feb 2016)

The Hugh Newman Langi video is the editorial anchor: he documents
~28 massive coral-slab pyramid platforms with cut notches comparable
to Stonehenge and Peruvian polygonal walls, in the ancient capital
Mu'a (linked by some to the lost continent of 'Mu' / Lemuria).

Idempotent. Run from repo root:
    python3 scripts/add-tonga-batch.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
TODAY = datetime.date.today().isoformat()
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal",
                  "stratigraphy", "geometry", "machining"}

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

NEW_CREATORS = {
    "onceuponasaga": {
        "name": "Thor Pedersen / Once Upon A Saga",
        "handle": "@OnceUponASaga",
        "subs": "Every country in the world without flying · 199+ countries",
        "color": "#6F9CC1",
        "tier": 3,
    },
    "magneticreversalnews": {
        "name": "Magnetic Reversal News",
        "handle": "@MagneticReversalNews",
        "subs": "Weathering-rate analysis · alt-dating of ancient sites",
        "color": "#A88B6E",
        "tier": 3,
    },
    "horsfrontieres": {
        "name": "Hors Frontières",
        "handle": "@HorsFrontieres",
        "subs": "French world-tour channel · 120+ countries on the ground",
        "color": "#8FA17E",
        "tier": 3,
    },
}

NEW_SITES = [
    {"n": "Langi Pyramid Platforms (Lapaha)",
     "lat": -21.1944, "lng": -175.1361,
     "cat": "pyramid", "region": "Pacific", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "precision"],
     "desc": (
         "Approximately 28 megalithic stepped pyramid platforms — "
         "langi — built of massive coral-limestone slabs at the ancient "
         "Tu'i Tonga capital of Mu'a (modern Lapaha), on the southern "
         "shore of the Fanga'uta lagoon in Tongatapu. Conventional "
         "dating places the langi tradition c. 1200-1500 CE during the "
         "high Tu'i Tonga dynasty, contemporary with the Ha'amonga 'a "
         "Maui Trilithon 10 km north. Several langi preserve precision-"
         "cut notches and L-shaped corner joinery comparable in form "
         "to the Stonehenge mortise-tenons and to Peruvian polygonal "
         "wall construction — the same engineering idea applied to "
         "soft coral limestone instead of granite or andesite. The "
         "largest blocks exceed 7 tons. Local tradition records that "
         "the coral slabs were transported by sea from quarries on "
         "neighbouring islands (some accounts cite 'Uvea and Samoa, "
         "~900 km of open ocean). Hugh Newman has documented the "
         "Mu'a / Lemuria etymological link explored in the alternative-"
         "history literature."
     ),
    },
]

def _v(vid, title, cr, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": cr, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Ha'amonga 'a Maui Trilithon (existing site, currently 0 wires) ===
    ("Ha'amonga 'a Maui (Tonga Trilithon)", _v("qfu9tb9SXbM",
        "Ha'amonga 'a Maui Trilithon, Kingdom of Tonga",
        "onceuponasaga", "2022-09-17")),
    ("Ha'amonga 'a Maui (Tonga Trilithon)", _v("2JzwQeNzQr4",
        "Tonga Tongatapu Guide de Ha'amonga'a Maui / Tonga Tongatapu Guide in Ha'amonga'a Maui",
        "horsfrontieres", "2015-11-19")),
    ("Ha'amonga 'a Maui (Tonga Trilithon)", _v("pt-BkEaamCg",
        "Ha‘amonga ‘a Maui — New Dating Revealed | A Massive Trilithon Nicknamed Stonehenge of the Pacific",
        "magneticreversalnews", "2022-04-08")),

    # === Langi Pyramid Platforms (new site, Hugh anchor) ===
    ("Langi Pyramid Platforms (Lapaha)", _v("Fdi1dcT3ofE",
        "Megalithic Technology in Ancient Tonga: The Mysterious 'Langi' Pyramid Platforms | Megalithomania",
        "megalithomania", "2016-02-07")),
]

def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    creators = load('creators.json')
    sites = load('sites.json')
    videos = load('videos.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

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

    print("\n=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            print(f"  ✗ Missing site: {site_name}")
            continue
        if v['cr'] not in creators:
            print(f"  ✗ Missing creator for {v['id']}: {v['cr']}")
            continue
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
            print(f"  ✓ Wired: {v['id']} → {site_name} [{v['cr']}]{tag}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        countries.setdefault('Tonga', [])
        for name in ["Ha'amonga 'a Maui (Tonga Trilithon)",
                     "Langi Pyramid Platforms (Lapaha)"]:
            if name not in countries['Tonga']:
                countries['Tonga'].append(name)
        save('countries.json', countries)
        print(f"\n  ✓ Tonga country tag updated")

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  This batch:         {added} new sites, {added_c} new creators, {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
