#!/usr/bin/env python3
"""
add-saudi-arabia-megastructures-batch.py

Wires two long-form Saudi Arabia walkthroughs to the atlas:

  1) Epoch Mysteries — "Saudi Arabia's Lost Megastructures From a
     Civilization We Can't Explain" (uB98YAE1kCM, Dec 11 2025, 123K views)
     Chapter timestamps wired so each site gets the viewer dropped into
     the relevant segment.

  2) BBC REEL — "The mysterious 'other Petra' of Saudi Arabia"
     (m-B0cO-mM5s) wired to Madain Saleh (Hegra).

Also adds 7 new Saudi Arabia sites that the Epoch Mysteries chapters
cover: AlUla (Dadan + Lihyanite), Elephant Rock, Tayma Oasis, Harat
Khaybar, Dumat al-Jandal, Qaryat al-Faw, Jubbah Rock Art.

DEDUPLICATION FIX:
  My earlier batch added 'Hegra (Madain Saleh)' as a new site, but the
  canonical name in atlas is 'Madain Saleh (Hegra)'. This script merges
  the duplicate into the canonical entry (preserving the richer
  description, criteria, signal, and library_ref from the recent batch)
  and removes the duplicate.

Idempotent. Run from repo root:
    python3 scripts/add-saudi-arabia-megastructures-batch.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

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
NEW_CREATORS = {
    "epochmysteries": {
        "name": "Epoch Mysteries",
        "handle": "@EpochMysteries",
        "subs": "Cinematic deep-dives into ancient sites, lost civilizations, and unresolved archaeological questions across the world",
        "color": "#7C4D2A",  # warm sand
        "tier": 3,
    },
    "bbcreel": {
        "name": "BBC REEL",
        "handle": "@BBCReel",
        "subs": "BBC's documentary short-form channel covering culture, history, science, and travel with field cinematography",
        "color": "#BB1919",  # BBC red
        "tier": 2,
    },
}

# ============================================================
NEW_SITES = [
    {"n": "AlUla (Dadan & Lihyanite Capitals)", "lat": 26.6280, "lng": 37.9244,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["precision", "scale", "stratigraphy"],
     "desc": (
         "Pre-Nabataean kingdom capital in the AlUla valley, northwestern "
         "Saudi Arabia, occupied by the Dadanite and later Lihyanite "
         "kingdoms from approximately the 8th century BCE through the 1st "
         "century BCE. Predates Madain Saleh (Hegra) by several centuries. "
         "Features rock-cut tomb facades carved high into the sandstone "
         "cliffs of Jabal al-Khuraibah, Lihyanite-period inscriptions in "
         "Dadanitic script, the Lion Tombs, and the monumental lion "
         "guardian statues at Jabal Ikmah's open-air library. Excavations "
         "have revealed earlier Bronze Age enclosures and well systems "
         "indicating continuous occupation across multiple millennia, with "
         "subsurface foundations that don't align with later street grids "
         "— suggesting cycles of reoccupation that left incomplete "
         "stratigraphic signatures."
     ),
    },
    {"n": "Elephant Rock (Jabal AlFil)", "lat": 26.6878, "lng": 38.0297,
     "cat": "monolithic", "region": "Middle East", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Isolated sandstone formation in the AlUla region, named for its "
         "natural elephant-shaped silhouette. The broad arch and rounded "
         "contours were shaped by wind-driven abrasion and thermal "
         "expansion cycles over deep geological time. While the formation "
         "itself is natural, faint petroglyphs and weathered inscriptions "
         "at the base indicate that the rock served as a way-marker or "
         "gathering point along ancient caravan routes. Stylistic affinities "
         "to distant regions (northern Arabia, Jubbah-basin geometric "
         "patterns) suggest repeated visits across long intervals."
     ),
    },
    {"n": "Tayma Oasis", "lat": 27.6322, "lng": 38.5436,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Major Bronze Age and Iron Age oasis settlement in northwestern "
         "Arabia, anchored by deep wells tapping ancient aquifers. Famous "
         "as the second residence of the Neo-Babylonian king Nabonidus, "
         "who spent approximately a decade here (c. 552-543 BCE). The "
         "monumental Tayma Stone bears Aramaic inscription. The massive "
         "city wall stretches in tiered courses with foundations resting "
         "on earlier fortifications. Stratified deposits show transitions "
         "in food production, storage, and ceramic styles spanning multiple "
         "millennia. Some construction phases coincide with drier intervals "
         "— suggesting adaptive labor redistribution rather than environmental "
         "determinism. Subsurface anomalies reveal foundations that don't "
         "align with later street grids."
     ),
    },
    {"n": "Harat Khaybar", "lat": 25.6800, "lng": 39.7500,
     "cat": "geoglyph", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Vast basalt lava field southeast of Khaybar in northwestern Saudi "
         "Arabia, containing thousands of mostly-undated stone structures: "
         "keyhole-shaped monuments, circular cairns, low-walled alignments, "
         "and the long converging guide-walls of so-called desert kites used "
         "for coordinated hunting. The keyhole monuments comprise a circular "
         "mound linked to a tapering tail — their function unresolved, with "
         "some containing burials and others empty. The structures follow "
         "topography, seasonal water courses, and vantage points across the "
         "lava field. Radiocarbon ranges overlap broadly, resisting a clean "
         "chronology. Visible from satellite as one of the densest "
         "concentrations of ancient stone work on Earth."
     ),
    },
    {"n": "Dumat al-Jandal", "lat": 29.8128, "lng": 39.8730,
     "cat": "city", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Frontier oasis town in northern Saudi Arabia near the Jordan "
         "border. Visible monuments include Qasr Marid, the stepped "
         "limestone fortress, and the Mosque of Omar, among the earliest "
         "known mosques in Arabia. Beneath the visible architecture lie "
         "Iron Age and earlier occupation layers whose foundations do not "
         "align with the later urban grid, creating subtle discontinuities. "
         "Multiple building campaigns are visible in the fortress's "
         "irregular limestone courses. Some construction expansions appear "
         "to coincide with drier intervals — community resilience through "
         "deeper wells and labor redistribution rather than environmental "
         "determinism. Sits at a crossroads connecting Mesopotamia, the "
         "Levant, and inner Arabia."
     ),
    },
    {"n": "Qaryat al-Faw", "lat": 19.7333, "lng": 45.1500,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "stratigraphy"],
     "desc": (
         "Pre-Islamic capital of the Kingdom of Kinda, deep in the Rub' "
         "al-Khali threshold of southern Saudi Arabia. Flourished c. 4th "
         "century BCE through 4th century CE as a major caravan-route "
         "city linking south Arabia with central and northern regions. "
         "Features broad avenues, multi-room courtyard houses, market "
         "areas, a substantial temple complex with plastered floors, an "
         "expansive necropolis, and inscriptions in the ancient South "
         "Arabian script. Earlier alignments beneath later buildings don't "
         "always correspond with the final street grid, suggesting gradual "
         "shifts in planning. Mixed influences from South Arabian, Nabataean, "
         "and local traditions produce architectural hybrids that resist "
         "precise classification."
     ),
    },
    {"n": "Jubbah Rock Art (Jabal Umm Sinman)", "lat": 28.0250, "lng": 40.9333,
     "cat": "geoglyph", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "UNESCO World Heritage rock-art complex on Jabal Umm Sinman in the "
         "Nefud Desert, northern Saudi Arabia, where ancient lakes once "
         "mirrored a greener Arabia. The carvings span tens of millennia, "
         "with the oldest panels depicting large bovids, hippos, and "
         "elongated human forms consistent with Pleistocene or early "
         "Holocene conditions when the basin supported wildlife now rarely "
         "associated with the region. Later layers introduce camels, "
         "equids, standardized human silhouettes, and inscriptions in early "
         "North Arabian scripts. Stylistic transitions are not uniform — "
         "some panels show abrupt adoption of new motifs while others "
         "preserve older styles long after environmental conditions changed."
     ),
    },
]

# ============================================================
# DEDUPLICATION — merge 'Hegra (Madain Saleh)' INTO 'Madain Saleh (Hegra)'
# ============================================================
DUPLICATE_NAME = "Hegra (Madain Saleh)"
CANONICAL_NAME = "Madain Saleh (Hegra)"

# ============================================================
# Epoch Mysteries — chapter timestamps wired to each site
# ============================================================
EPOCH_VIDEO_META = {
    "id": "uB98YAE1kCM",
    "title": "Saudi Arabia's Lost Megastructures From a Civilization We Can't Explain | Epoch Mysteries",
    "cr": "epochmysteries", "added": TODAY, "published": "2025-12-11",
}
# (site_name, chapter_start_seconds)
EPOCH_CHAPTER_WIRES = [
    ("AlUla (Dadan & Lihyanite Capitals)", 75),     # 01:15
    (CANONICAL_NAME, 535),                          # 08:55 — Madain Salih
    ("Elephant Rock (Jabal AlFil)", 924),           # 15:24
    ("Tayma Oasis", 1368),                          # 22:48
    ("Harat Khaybar", 1872),                        # 31:12
    ("Dumat al-Jandal", 2314),                      # 38:34
    ("Qaryat al-Faw", 2709),                        # 45:09
    ("Jubbah Rock Art (Jabal Umm Sinman)", 3134),   # 52:14
    # Note: 1:00:24 Qaryat al-Faw Tombs is covered within the Qaryat al-Faw site
]

BBC_REEL_VIDEO = {
    "id": "m-B0cO-mM5s",
    "title": "The mysterious 'other Petra' of Saudi Arabia | BBC REEL",
    "cr": "bbcreel", "added": TODAY, "published": "2024-08-15",
}
BBC_WIRES = [(CANONICAL_NAME, BBC_REEL_VIDEO)]

# ============================================================
def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    try:
        countries = load('countries.json')
    except FileNotFoundError:
        countries = {}

    # ---- Creators ----
    print("=== CREATORS ===")
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · '{key}' already exists")
        else:
            creators[key] = info
            print(f"  ✓ Added: {key} ({info['name']})")
    save('creators.json', creators)

    # ---- Deduplicate Hegra ----
    print("\n=== DEDUPLICATION ===")
    site_map = {s['n']: s for s in sites}
    if DUPLICATE_NAME in site_map and CANONICAL_NAME in site_map:
        dup = site_map[DUPLICATE_NAME]
        canon = site_map[CANONICAL_NAME]
        # Promote richer fields from duplicate to canonical
        for field in ('desc', 'criteria', 'signal', 'library_ref', 'tier'):
            if field in dup and (field not in canon or len(str(canon.get(field, ''))) < len(str(dup.get(field, '')))):
                canon[field] = dup[field]
                print(f"  ✓ Migrated '{field}' to canonical")
        # Remove the duplicate from the sites list
        sites[:] = [s for s in sites if s['n'] != DUPLICATE_NAME]
        site_map = {s['n']: s for s in sites}  # rebuild
        # Move any videos wired to duplicate over to canonical
        if DUPLICATE_NAME in videos:
            existing_canon_ids = {v['id'] for v in videos.get(CANONICAL_NAME, [])}
            for v in videos[DUPLICATE_NAME]:
                if v['id'] not in existing_canon_ids:
                    videos.setdefault(CANONICAL_NAME, []).append(v)
                    print(f"  ✓ Moved video {v['id']} from dup → canonical")
            del videos[DUPLICATE_NAME]
        # Patch country tags
        if isinstance(countries, dict):
            for country, names in countries.items():
                if DUPLICATE_NAME in names:
                    names.remove(DUPLICATE_NAME)
                    if CANONICAL_NAME not in names:
                        names.append(CANONICAL_NAME)
                    print(f"  ✓ Country tag '{country}': dup → canonical")
        print(f"  ✓ Deleted duplicate site '{DUPLICATE_NAME}'")
    elif DUPLICATE_NAME in site_map:
        print(f"  ⚠ Found '{DUPLICATE_NAME}' but no '{CANONICAL_NAME}' — skipping merge")
    else:
        print(f"  · No duplicate found (already deduplicated or never existed locally)")

    # ---- New sites ----
    print("\n=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

    # ---- Video wires ----
    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in sites}
    videos_wired = 0
    new_badges = 0

    # Epoch Mysteries — one video, multiple chapter timestamps
    for site_name, t in EPOCH_CHAPTER_WIRES:
        if site_name not in site_names:
            print(f"  ⚠ {site_name} not in sites — skipping")
            continue
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if EPOCH_VIDEO_META['id'] in existing_ids:
            print(f"  · Already wired: {EPOCH_VIDEO_META['id']} → {site_name}")
        else:
            entry = dict(EPOCH_VIDEO_META)
            entry['t'] = t
            videos[site_name].append(entry)
            videos_wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(EPOCH_VIDEO_META['published'])).days
            new_tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90: new_badges += 1
            print(f"  ✓ Wired: {EPOCH_VIDEO_META['id']}@{t}s → {site_name}{new_tag}")

    # BBC REEL — single wire to canonical Hegra
    for site_name, v in BBC_WIRES:
        if site_name not in site_names:
            print(f"  ⚠ {site_name} not in sites — skipping")
            continue
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            pub_days = (datetime.date.today() - datetime.date.fromisoformat(v['published'])).days
            new_tag = " [NEW]" if pub_days <= 90 else ""
            if pub_days <= 90: new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}{new_tag}")

    save('videos.json', videos)

    # ---- Country tags ----
    if isinstance(countries, dict):
        countries.setdefault('Saudi Arabia', [])
        sa_new = [s['n'] for s in NEW_SITES]
        for n in sa_new:
            if n not in countries['Saudi Arabia']:
                countries['Saudi Arabia'].append(n)
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated (Saudi Arabia +{sites_added})")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, {new_badges} fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
