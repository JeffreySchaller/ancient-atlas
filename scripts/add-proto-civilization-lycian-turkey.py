#!/usr/bin/env python3
"""
add-proto-civilization-lycian-turkey.py — Add 5 Lycian/Pisidian/Pamphylian
sites from southern Turkey and wire Proto Civilization's empirical
walkthroughs.

The channel's Turkey series matches the same editorial frame Jeff flagged
for Praveen Mohan: provocative click titles that hook viewers, then an
actual empirical-archaeology body that respects the site, including
live tool tests showing steel chisels are ineffectual against the
materials these monuments were cut from.

NEW SITES (5):
    Telmessos (modern Fethiye) — Lycian rock-cut tombs (Tomb of Amyntas)
    Tlos — Lycian/Roman river-valley city with cliff tombs
    Limyra — Eastern Lycian capital, rock-cut cliff necropolis
    Termessos — Pisidian mountain city Alexander could not conquer
    Aspendos — Pamphylian city, Roman theater + 19km arched aqueduct

NEW WIRES (6):
    Telmessos: rmdiwT68USw  — Hydraulics of the Ancient World s05e06
    Tlos:      _F88M17zgDQ  — Buried where it shouldn't be s05e07
    Limyra:    AqRi0yqMupk  — Megaliths on the Summit s02e16
    Limyra:    8NdJZ95hjLU  — Ancient Bomb Shelter? s02e03
    Termessos: Xp0HVEwCvRc  — Most Fierce City of the Ancient World s03e18
    Aspendos:  dhmz-10UVtI  — Giant City-Mountain with Strange Aqueduct s03e16

Idempotent. Run from repo root:
    python3 scripts/add-proto-civilization-lycian-turkey.py
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

# ============================================================
NEW_SITES = [
    {"n": "Telmessos (Fethiye)", "lat": 36.6228, "lng": 29.1252,
     "cat": "rock-cut", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal"],
     "desc": (
         "Ancient Lycian port city on the southwestern Mediterranean "
         "coast of Turkey, near modern Fethiye. Famous for the rock-cut "
         "necropolis carved directly into the cliff face above the bay, "
         "including the Tomb of Amyntas (c. 350 BCE) — a temple-form "
         "tomb cut as a single monolithic facade from the living rock. "
         "The interior chambers are cut to such precision that the "
         "doors close perfectly against the stone jambs. The cliff "
         "complex contains dozens of similar tombs in various scales, "
         "all carved using techniques that mainstream archaeology "
         "attributes to iron chisels but that independent investigators "
         "(Proto Civilization, others) have demonstrated cannot be "
         "replicated by modern steel against the same stone."
     ),
    },
    {"n": "Tlos", "lat": 36.5530, "lng": 29.4356,
     "cat": "rock-cut", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal"],
     "desc": (
         "Ancient Lycian city in the Xanthos river valley of southern "
         "Turkey, occupied from approximately the 14th century BCE "
         "(Hittite-era 'Dalawa') through the Ottoman period. The site "
         "is dominated by a fortified acropolis on a 500-meter "
         "promontory with a cliff-face necropolis of rock-cut tombs "
         "below. The Tomb of Bellerophon, carved as a temple facade "
         "with relief sculpture, is among the finest in Lycia. "
         "Proto Civilization's coverage examines surface evidence "
         "suggesting an earlier substrate beneath the visible "
         "Lycian-Roman work."
     ),
    },
    {"n": "Limyra", "lat": 36.3508, "lng": 30.1850,
     "cat": "rock-cut", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["precision", "polygonal", "scale"],
     "desc": (
         "Eastern Lycian capital city near modern Finike on Turkey's "
         "Mediterranean coast. Rose to importance under King "
         "Pericles of Lycia (c. 380-360 BCE). The site is dominated "
         "by a cliff-face necropolis of over 400 rock-cut tombs, "
         "including the Heroon of Pericles — a unique temple-tomb at "
         "the summit of the acropolis. The lower city contains a "
         "preserved Roman theater and the Cenotaph of Gaius Caesar, "
         "Augustus's adopted grandson who died here in 4 CE. "
         "Independent field investigators have documented megalithic "
         "courses near the summit and unusual rock-cut chamber networks "
         "below the visible city."
     ),
    },
    {"n": "Termessos", "lat": 36.9892, "lng": 30.4664,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision", "polygonal"],
     "desc": (
         "Pisidian mountain city at 1,050 meters elevation in the "
         "Taurus Mountains near Antalya, Turkey. Famously the city "
         "Alexander the Great chose not to besiege in 333 BCE, "
         "describing it as 'an eagle's nest' that could not be taken. "
         "The site preserves a remarkable hilltop theater, gymnasium, "
         "agora, and an extensive cliff-face necropolis with elaborate "
         "rock-cut sarcophagi visible against the mountain. The "
         "construction integrates cyclopean and polygonal masonry "
         "fitted to the native bedrock — making distinction between "
         "natural cliff and worked stone difficult in places. Never "
         "destroyed by conquest; abandoned after a 3rd-century CE "
         "earthquake destroyed the aqueduct."
     ),
    },
    {"n": "Aspendos", "lat": 36.9389, "lng": 31.1722,
     "cat": "city", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["precision", "scale", "geometry"],
     "desc": (
         "Pamphylian city on the Eurymedon River in Antalya Province, "
         "Turkey. Home to the best-preserved Roman theater in the "
         "Mediterranean (c. 155 CE, capacity 12,000), with acoustic "
         "properties so refined that a coin dropped on the stage can "
         "be heard in the upper rows. The site is equally notable for "
         "its 19-kilometer Roman aqueduct, which crosses the Eurymedon "
         "valley on a series of arched bridges and uses an inverted "
         "siphon to maintain hydraulic head across the depression. "
         "The siphon engineering is centuries ahead of contemporary "
         "Roman waterworks and remains incompletely explained. Proto "
         "Civilization's coverage examines the mountain itself and the "
         "case for a substantially older substrate beneath the Roman "
         "construction."
     ),
    },
]

# ============================================================
def _v(vid, title, published="2022-06-01"):
    return {"id": vid, "title": title,
            "cr": "protocivilization", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    ("Telmessos (Fethiye)", _v("rmdiwT68USw",
        "Hydraulics of the Ancient World. The Remains of Telmessos | s05e06 (Proto Civilization, ru/en dub)",
        "2024-08-10")),
    ("Tlos", _v("_F88M17zgDQ",
        "Buried where it shouldn't be. Tlos | s05e07 (Proto Civilization, ru/en dub)",
        "2024-08-25")),
    ("Limyra", _v("AqRi0yqMupk",
        "Megaliths on the Summit. Limyra | s02e16 (Proto Civilization, ru/en dub)",
        "2023-04-12")),
    ("Limyra", _v("8NdJZ95hjLU",
        "Ancient Bomb Shelter? Limyra | s02e03 (Proto Civilization, ru/en dub)",
        "2022-11-08")),
    ("Termessos", _v("Xp0HVEwCvRc",
        "The Most Fierce City of the Ancient World. Termessos | s03e18 (Proto Civilization, ru/en dub)",
        "2022-09-30")),
    ("Aspendos", _v("dhmz-10UVtI",
        "The Giant City-Mountain with a Strange Aqueduct. Aspendos | s03e16 (Proto Civilization, ru/en dub)",
        "2022-09-15")),
]

# ============================================================
def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load('sites.json')
    videos = load('videos.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    print("=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    creators = load('creators.json')
    if 'protocivilization' not in creators:
        sys.exit("✗ Creator 'protocivilization' not found — run add-proto-civilization-batch.py first")

    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
            print(f"  ✗ Missing site: {site_name}")
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
            print(f"  ✓ Wired: {v['id']} → {site_name}{tag}")
    save('videos.json', videos)

    if isinstance(countries, dict):
        countries.setdefault('Türkiye', [])
        for n in ['Telmessos (Fethiye)', 'Tlos', 'Limyra', 'Termessos', 'Aspendos']:
            if n not in countries['Türkiye']:
                countries['Türkiye'].append(n)
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated")

    sites = load('sites.json')
    videos = load('videos.json')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {sites_added} new sites, {wired} wires")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
