#!/usr/bin/env python3
"""
apply-russia-batch.py — Russia content batch v1 + signal/criteria schema rollout.

What this does:
  1. Appends 5 Russia sites to data/sites.json
  2. Wires 5 UIY videos to data/videos.json
  3. Adds "Russia" to data/countries.json
  4. Applies "signal": "open" + "criteria" arrays to 13 sites (3 new + 10 existing)
  5. Validates everything (no dupes, all refs resolve)
  6. Runs build.py to rebuild public/index.html + mirror public/data/

Editorial principle: "signal" + "criteria" stay scarce. Only mark sites where
readings genuinely diverge. Closed taxonomy of 6 criteria matches the megalith
library exactly: precision, hardness, scale, polygonal, stratigraphy, geometry.

Run from the repo root:
    python3 scripts/apply-russia-batch.py
"""
import json, sys, subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

# ============================================================
# 5 new Russia sites
# ============================================================
NEW_SITES = [
    {
        "n": "Dolmens of the North Caucasus",
        "lat": 44.5500, "lng": 38.0833,
        "cat": "megalithic", "region": "Europe", "tier": 1,
        "desc": "Bronze Age megalithic tomb complex spanning the Krasnodar and Adygea regions near the Black Sea. Roughly 3,000 documented dolmens, constructed from precisely cut stone slabs weighing up to 20 tons, many featuring carved portholes and ornamental relief work. Carbon-dated to the 3rd-2nd millennium BCE. The masonry precision rivals Western European megalithic traditions and predates them in several places."
    },
    {
        "n": "Arkaim",
        "lat": 52.6394, "lng": 59.5614,
        "cat": "settlement", "region": "Asia", "tier": 1,
        "desc": "Sintashta-culture fortified settlement in the Southern Urals, dated to 2000-1700 BCE. Concentric circular walls, 60 dwellings in radial pattern, sophisticated drainage. Discovered 1987. Astronomical alignments at the perimeter prompted the 'Russian Stonehenge' label; the comparison is loose but the site's geometric precision is its own argument. Genetic evidence links the population to early Indo-Iranian migrations."
    },
    {
        "n": "Gornaya Shoria",
        "lat": 53.0167, "lng": 88.8500,
        "cat": "megalithic", "region": "Asia", "tier": 3,
        "signal": "open",
        "criteria": ["scale", "precision"],
        "desc": "Granite formations at the summit of Mount Kuylyum in the Kemerovo Oblast, Siberia. Individual blocks reach reported weights of 3,000+ tons with flat faces and joinery-tight seams along multiple planes. The engineering question is whether the seam regularity and block scale fall within the range natural granite outcrop produces, or outside it. Geological surveys read the formation as fractured natural outcrop. Field expeditions, including the 2014 Lakhta Foundation visit, argue the precision warrants treating the site as worked stone. Among the largest claimed megalithic blocks on earth."
    },
    {
        "n": "Khara-Hora Shaft",
        "lat": 63.0000, "lng": 67.5000,
        "cat": "megalithic", "region": "Asia", "tier": 3,
        "signal": "open",
        "criteria": ["scale", "precision", "geometry"],
        "desc": "A roughly 100-meter vertical shaft in the Khanty-Mansi region of Russia's Far East. Polished interior surfaces with dimensional regularity along the full descent. The geometry (uniform diameter, true vertical, finished wall texture) sits at the edge of what groundwater karst processes typically produce. Geological readings interpret it as a natural shaft. Independent field investigators argue the precision and surface finish read as worked construction. Currently outside mainstream academic discussion."
    },
    {
        "n": "Chusovo Wall",
        "lat": 58.2000, "lng": 57.8167,
        "cat": "megalithic", "region": "Asia", "tier": 3,
        "signal": "open",
        "criteria": ["scale", "precision", "polygonal"],
        "desc": "A polygonal stonework retaining wall ~85 meters long and up to 4 meters high along the Chusovaya River in the Middle Urals (Sverdlovsk Oblast). Built from granite blocks, some over 2 meters in length and weighing in excess of 10 tons, fitted along irregular but tight seams in the concave-convex joinery characteristic of mortarless megalithic construction at Cusco, Ahu Vinapu (Easter Island), the Osirion (Egypt), and Osaka Castle (Japan). Conventionally attributed to the 1720s-1730s Demidov iron-smelting factory. Three engineering signals resist that attribution: the wall is absent from the surviving 1735 factory plans, the surrounding geology contains no granite source within transport range, and a pin hole on one block matches the bronze-rod joinery technique documented at Baalbek and the Osirion. Independent investigators argue the structure was inherited rather than built by the Demidovs. Brought to wider attention by the 2014 documentary 'The Miracle of Chusovoe.'"
    },
]

# ============================================================
# Videos to wire (site name → list of new entries)
# ============================================================
NEW_VIDEOS = {
    "Dolmens of the North Caucasus": [
        { "id": "qBin7G3n4eE", "title": "Giant Prehistoric Dolmens in the Caucasus Built with Advanced Technology", "cr": "universeinside" },
        { "id": "NvzxNm3Mxcs", "title": "Pre-Historic Megastructures of Russia In The Remote Wilderness", "cr": "universeinside" },
    ],
    "Arkaim": [
        { "id": "85cDo54GFlo", "title": "Lost City in Siberia BREAKS History - Arkaim", "cr": "universeinside" },
        { "id": "NvzxNm3Mxcs", "title": "Pre-Historic Megastructures of Russia In The Remote Wilderness", "cr": "universeinside" },
    ],
    "Gornaya Shoria": [
        { "id": "NvzxNm3Mxcs", "title": "Pre-Historic Megastructures of Russia In The Remote Wilderness", "cr": "universeinside" },
    ],
    "Khara-Hora Shaft": [
        { "id": "J1QDP-Oqcr0", "title": "Pre-Historic Underground Megastructure Found in Russia - Khara-Hora Shaft", "cr": "universeinside" },
    ],
    "Chusovo Wall": [
        { "id": "n-at6AZIsoI", "title": "ANOTHER Pre-Historic Mega Structure in Russia", "cr": "universeinside" },
        { "id": "aPyw-yiKTMY", "title": "Pre-Historic Hyperborean Civilization of Russia - Documentary", "cr": "universeinside" },
    ],
}

# ============================================================
# Existing sites to tag with signal + criteria
# ============================================================
EXISTING_OPEN = {
    "Yonaguni Monument":       ["scale", "precision", "geometry"],
    "Mt. Kuromata":            ["scale", "geometry"],
    "Baigong Pipes":           ["stratigraphy"],
    "Gunung Padang":           ["scale", "geometry", "stratigraphy"],
    "Adam's Calendar":         ["geometry", "stratigraphy"],
    "Bimini Road":             ["scale", "geometry"],
    "Osireion":                ["hardness", "scale", "precision"],
    "Osireion (Abydos)":       ["hardness", "scale", "precision"],  # alt name fallback
    "Naupa Huaca":             ["hardness", "precision", "geometry"],
    "Karahunj (Zorats Karer)": ["scale", "geometry"],
    "Xi'an Pyramids":          ["scale", "geometry"],
}

# ============================================================
# Country tag for Russia
# ============================================================
RUSSIA_SITES = [
    "Dolmens of the North Caucasus",
    "Arkaim",
    "Gornaya Shoria",
    "Khara-Hora Shaft",
    "Chusovo Wall",
]

# ============================================================
# Valid criteria taxonomy (closed set, matches library/megaliths.html)
# ============================================================
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

# ============================================================
def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)

def save_json(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def main():
    if not DATA_DIR.exists():
        sys.exit(f"data/ not found at {DATA_DIR}")

    # 1. Load
    print("Loading current data…")
    sites = load_json('sites.json')
    videos = load_json('videos.json')
    creators = load_json('creators.json')
    countries = load_json('countries.json')

    existing_names = {s['n'] for s in sites}
    creator_keys = set(creators.keys())

    # 2. Validate new criteria
    print("\nValidating new sites…")
    for s in NEW_SITES:
        if s['n'] in existing_names:
            sys.exit(f"  ✗ Site already exists: {s['n']}")
        crits = s.get('criteria', [])
        invalid = [c for c in crits if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"  ✗ {s['n']}: invalid criteria {invalid}")
        print(f"  ✓ {s['n']:35s}  signal={s.get('signal','convergent')}  criteria={s.get('criteria',[])}")

    # 3. Validate video creator refs
    print("\nValidating video wirings…")
    for site_name, vids in NEW_VIDEOS.items():
        for v in vids:
            if v['cr'] not in creator_keys:
                sys.exit(f"  ✗ Unknown creator key: {v['cr']} for video {v['id']}")
        print(f"  ✓ {site_name:35s}  {len(vids)} video(s)")

    # 4. Apply: append new sites
    print("\nAppending Russia sites…")
    sites.extend(NEW_SITES)
    save_json('sites.json', sites)
    print(f"  sites.json: {len(sites)-len(NEW_SITES)} → {len(sites)} entries")

    # 5. Apply: signal + criteria to existing sites
    print("\nTagging existing sites with signal/criteria…")
    sites = load_json('sites.json')  # reload for stable iteration
    applied = 0
    for s in sites:
        if s['n'] in EXISTING_OPEN:
            crits = EXISTING_OPEN[s['n']]
            invalid = [c for c in crits if c not in VALID_CRITERIA]
            if invalid:
                sys.exit(f"  ✗ {s['n']}: invalid criteria in EXISTING_OPEN")
            s['signal'] = 'open'
            s['criteria'] = crits
            print(f"  ✓ {s['n']:35s}  criteria={crits}")
            applied += 1
    save_json('sites.json', sites)
    print(f"  Tagged {applied} existing sites")

    # 6. Apply: video wirings
    print("\nWiring videos…")
    for site_name, vids in NEW_VIDEOS.items():
        existing = videos.get(site_name, [])
        existing_ids = {v['id'] for v in existing}
        added = 0
        for v in vids:
            if v['id'] not in existing_ids:
                existing.append(v)
                added += 1
        videos[site_name] = existing
        print(f"  ✓ {site_name:35s}  +{added} (total {len(existing)})")
    save_json('videos.json', videos)

    # 7. Apply: Russia → countries.json
    print("\nAdding Russia country tag…")
    if isinstance(countries, dict):
        # Country tags map: country name → list of site names
        if 'Russia' in countries:
            # Merge if already present
            existing_sites = set(countries['Russia'])
            for s in RUSSIA_SITES:
                if s not in existing_sites:
                    countries['Russia'].append(s)
        else:
            countries['Russia'] = list(RUSSIA_SITES)
        save_json('countries.json', countries)
        print(f"  ✓ Russia: {countries['Russia']}")
    else:
        # If schema is different, write a hint and let humans fix it
        print(f"  ⚠  countries.json shape unexpected (type {type(countries).__name__}). Russia entry skipped — add manually.")

    # 8. Final summary
    print("\n" + "=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)
    sites = load_json('sites.json')
    videos = load_json('videos.json')
    open_count = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"  Total sites:       {len(sites)}")
    print(f"  Sites with signal='open': {open_count}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Russia sites:      {len(RUSSIA_SITES)}")

    # 9. Run build.py
    print("\nRunning build.py to rebuild HTML + mirror data/ → public/data/…")
    build_script = REPO_ROOT / 'scripts' / 'build.py'
    if build_script.exists():
        result = subprocess.run(['python3', str(build_script)], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("BUILD FAILED:")
            print(result.stderr)
            sys.exit(1)
    else:
        print("  ⚠  scripts/build.py not found — run it manually before commit.")

    print("\n✓ Russia batch applied.")
    print("\nNext steps:")
    print("  1. python3 scripts/audit-videos.py    # sanity check")
    print("  2. python3 scripts/inject-badge-ui.py # add badge UI to public/index.html (run once)")
    print("  3. python3 scripts/add-library-anchors.py  # add section anchors to library/megaliths.html (run once)")
    print("  4. open public/index.html             # eyeball it")
    print("  5. git add -A && git commit -m 'Russia batch v1 + signal schema + open-question badge'")
    print("  6. git push origin main")

if __name__ == '__main__':
    main()
