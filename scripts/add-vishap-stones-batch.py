#!/usr/bin/env python3
"""
add-vishap-stones-batch.py — Wire 4 walkthroughs to the existing
Vishap Stones (Armenia) atlas entry, adding 3 new creators in the
process.

The Vishapakar ("dragon stones") of Armenia are Bronze Age basalt steles
carved with fish or bull motifs, distributed across the Armenian
highlands (Geghama, Aragats, Vardenis mountains) near springs and
upland water sources. Currently under serious academic investigation
by Dr. Arsen Bobokhyan and an Armenian / international team.

NEW CREATORS (3):
    cotsenucla   — Cotsen Institute of Archaeology at UCLA
    naasr        — NAASR Armenian Studies
    echoofashes  — Echo of Ashes (atmospheric short-form)

WIRES (4):
    eU9X-P3DcTM → cotsenucla — Recent Excavations of Armenia's Ancient Vishap
    nKEPS7N0T9Y → prehistoryguys — The Vishapakar Stones: Strangest Megalithic Mystery
    VCpHFJLnZLI → naasr — Arsen Bobokhyan: Vishapakars: Dragon Stones (lecture)
    wuvBj8Mrf_g → echoofashes — The Dragon Stones of Armenia: Guardians (short)

Idempotent. Run from repo root:
    python3 scripts/add-vishap-stones-batch.py
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
    "cotsenucla": {
        "name": "Cotsen Institute of Archaeology at UCLA",
        "handle": "@CotsenUCLA",
        "subs": "Academic field reports · ancient world archaeology · UCLA",
        "color": "#7A9BBC",
        "tier": 2,
    },
    "naasr": {
        "name": "NAASR Armenian Studies",
        "handle": "@NAASRArmenianStudies",
        "subs": "National Association for Armenian Studies and Research · scholarly lectures",
        "color": "#C97A57",
        "tier": 2,
    },
    "echoofashes": {
        "name": "Echo of Ashes",
        "handle": "@EchoofAshes",
        "subs": "Atmospheric short-form mysteries · ancient sites",
        "color": "#9B8FAA",
        "tier": 3,
    },
}

SITE = "Vishap Stones"

def _v(vid, title, cr, published="2023-01-01"):
    return {"id": vid, "title": title,
            "cr": cr, "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    _v("eU9X-P3DcTM",
       "Recent Excavations Of Armenia's Ancient Vishap Dragon Stones | Cotsen Institute UCLA",
       "cotsenucla",
       "2020-04-22"),
    _v("nKEPS7N0T9Y",
       "The Vishapakar Stones: Armenia's Strangest Megalithic Mystery | The Prehistory Guys",
       "prehistoryguys",
       "2024-09-15"),
    _v("VCpHFJLnZLI",
       "Arsen Bobokhyan: Vishapakars: Dragon Stones of Armenia's Mountains | NAASR lecture",
       "naasr",
       "2019-11-08"),
    _v("wuvBj8Mrf_g",
       "The Dragon Stones of Armenia: Guardians of the Ancient Sky | Echo of Ashes (Short)",
       "echoofashes",
       "2025-08-12"),
]

def main():
    sites = load('sites.json')
    if not any(s['n'] == SITE for s in sites):
        sys.exit(f"✗ Site '{SITE}' not found")

    creators = load('creators.json')
    added_creators = 0
    for k, v in NEW_CREATORS.items():
        if k in creators:
            print(f"  · Creator already exists: {k}")
        else:
            creators[k] = v
            added_creators += 1
            print(f"  ✓ Added creator: {k} → {v['name']}")
    if 'prehistoryguys' not in creators:
        sys.exit("✗ Expected existing creator 'prehistoryguys' is missing")
    save('creators.json', creators)

    videos = load('videos.json')
    videos.setdefault(SITE, [])
    wired = 0
    new_badges = 0
    for v in VIDEOS_TO_WIRE:
        if any(x['id'] == v['id'] for x in videos[SITE]):
            print(f"  · Already wired: {v['id']}")
        else:
            videos[SITE].append(v)
            wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90:
                new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {SITE} (cr={v['cr']}){tag}")
    save('videos.json', videos)

    sites = load('sites.json')
    creators = load('creators.json')
    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {added_creators} creators, {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
