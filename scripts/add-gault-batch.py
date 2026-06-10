#!/usr/bin/env python3
"""
add-gault-batch.py — Gault Site (Texas): North America's stratigraphy card.

WHY THIS SITE (editorial decision record, 2026-06-10):
    The atlas's signal:open grammar already covers stratigraphic-dating
    controversies (Gunung Padang is the flagship). Gault is the North
    American version: the densest Clovis assemblage on the continent
    PLUS pre-Clovis layers (Area 15) dating ~16,000-20,000 years old,
    which broke the Clovis-first model in the published literature.
    North America held only 6 sites before this batch, none carrying
    the deep-chronology question.

    Caveat handled in desc: no monumental architecture, and the
    Archaeological Conservancy restricts access, so wires are
    documentaries/lectures, not walkthroughs. Coordinates are
    approximate by design (the Conservancy keeps the precise location
    soft).

WIRES (all verified via YouTube oEmbed 2026-06-10, Bimini pairing
pattern: institutional + independent on the same signal:open card):
    The Archaeological Conservancy (land steward, institutional)
        K1uHmLVg-7k — "The Gault Site and the Peopling of the Americas"
    cf-apps7865 (independent / alternative analysis)
        EIPsDMc3NIE — "Texas' 18,000(!?!) Year Old Gault Site"
    Archaeology Podcast Network (institutional-adjacent)
        fnCja1qo1Ks — "The Stones are Speaking: Gault Site Documentary - Ep 316"
    REJECTED: IEbE8Y5iScI (Shop LC) — retail network content arm,
    weakest provenance. Honesty over completeness.

SCHEMA NOTE (corrected 2026-06-10): countries.json intentionally mixes
two shapes — site→country strings for atlas sites AND country→[names]
lists (the wishlist/coverage dictionary embedded in the UI). 39 countries
use the list form. Do NOT "normalize" it; an earlier draft of this script
tried and was aborted by its own validation.

Idempotent. Run from repo root:
    python3 scripts/add-gault-batch.py
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
    "archconservancy": {
        "name": "The Archaeological Conservancy",
        "handle": "@TheArchaeologicalConservancy",
        "subs": "Nonprofit steward of 580+ archaeological preserves, including Gault",
        "color": "#7B9F8E",
        "tier": 2,
    },
    "cfapps7865": {
        "name": "cf-apps7865",
        "handle": "@cfapps7865",
        "subs": "Independent deep-history analysis · alternative chronology",
        "color": "#A88B6E",
        "tier": 3,
    },
    "archpodnet": {
        "name": "Archaeology Podcast Network",
        "handle": "@archaeologypodcastnetwork",
        "subs": "Working archaeologists on the record · documentary coverage",
        "color": "#6BA3BE",
        "tier": 3,
    },
}

NEW_SITES = [
    {"n": "Gault Site (Buttermilk Creek)",
     "lat": 30.88, "lng": -97.72,
     "cat": "settlement", "region": "North America", "tier": 2,
     "signal": "open",
     "criteria": ["stratigraphy"],
     "desc": (
         "Open-air site on Buttermilk Creek near Florence, Texas, with "
         "one of the densest Clovis assemblages in the Americas — and, "
         "beneath it, the reason it matters: Area 15 yielded an "
         "assemblage stratigraphically below the Clovis horizon, with "
         "OSL dates of roughly 16,000-20,000 years, published as the "
         "Gault Assemblage. Together with the adjacent Debra L. "
         "Friedkin site, it broke the Clovis-first model of the "
         "peopling of the Americas in the mainstream literature. No "
         "monumental architecture: the open question here is purely "
         "stratigraphic — how deep does the human horizon go? Managed "
         "by the Archaeological Conservancy with research by UT Austin "
         "and Texas A&M; access is restricted, so coverage is "
         "documentary rather than walkthrough. Coordinates approximate."
     ),
    },
]

def _v(vid, title, cr, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": cr, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Gault Site (Buttermilk Creek)", _v("K1uHmLVg-7k",
        "The Gault Site and the Peopling of the Americas",
        "archconservancy", "2021-05-20")),
    ("Gault Site (Buttermilk Creek)", _v("EIPsDMc3NIE",
        "Texas' 18,000(!?!) Year Old Gault Site",
        "cfapps7865", "2022-08-15")),
    ("Gault Site (Buttermilk Creek)", _v("fnCja1qo1Ks",
        "The Stones are Speaking: Gault Site Documentary - Ep 316",
        "archpodnet", "2025-03-01")),
]

COUNTRY_TAGS = {
    "Gault Site (Buttermilk Creek)": "United States",
}

def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    creators = load('creators.json')
    sites = load('sites.json')
    videos = load('videos.json')
    countries = load('countries.json')

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
            print(f"  ✓ Wired: {v['id']} → {site_name} [{v['cr']}]")
    save('videos.json', videos)

    print("\n=== COUNTRY TAGS ===")
    for site_name, country in COUNTRY_TAGS.items():
        if countries.get(site_name) != country:
            countries[site_name] = country
            print(f"  ✓ Tagged: {site_name} → {country}")
    save('countries.json', countries)

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  This batch:         {added} new sites, {added_c} new creators, {wired} wires")

if __name__ == "__main__":
    main()
