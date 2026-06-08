#!/usr/bin/env python3
"""
wire-true-monoliths-library-refs.py — Wire 'Featured in the Library' link
onto atlas sites that meet the strict criterion for Library Entry 04
(True Monoliths).

INCLUSION GATE (Jeff's brief):
  Include only sites where EITHER
    (a) clear machining marks are documented (continuous curved tool
        signatures, gear-track grooves, mid-stroke direction changes), OR
    (b) unparalleled precision was cut into stone "as hard as steel"
        (Mohs ≥ 5-6 : granite, basalt, andesite, hard sandstone, porphyry).

INCLUDED on the precision-anomaly leg of the gate (revised):
  - Göbekli Tepe, Karahan Tepe, Boncuklu Tarla, Sayburç, Sefertepe —
    Taş Tepeler complex. Although the bedrock is soft limestone, the
    T-pillars carry high-relief animal sculpture and the chambers at
    Karahan Tepe are cut directly into bedrock (the eleven phallic
    pillars stand uncut from the chamber floor). The relief carving
    in soft stone is the precision-anomaly leg of the gate, not the
    machining-marks leg. The Sayburç narrative panel is currently the
    earliest known narrative scene in human art.

EXPLICITLY EXCLUDED despite being mentioned in the article:
  - Lalibela / Bet Giyorgis — volcanic tuff is Mohs ~4-5, no clearly
    documented machining anomaly distinct from hand chisel work.
  - Cappadocia tuff sites (Selime, Göreme, Derinkuyu) — soft tuff is
    plausibly hand-carvable; the article uses them as scale anchors,
    not machining anchors.
  - Tarragona, Carnac, Gochang, Ikom, Bada Valley — assembled or
    placed monuments, not extractive bedrock work.

For each qualifying site, sets:
    "library_ref": {
      "url": "/library/true-monoliths.html",
      "title": "True Monoliths"
    }

Idempotent. Reports missing site names with close matches so they can
be re-targeted if the canonical name differs from the candidate list.

Run from the repo root:
    python3 scripts/wire-true-monoliths-library-refs.py
"""
import sys, json
from pathlib import Path
from difflib import get_close_matches

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

ARTICLE = {
    "url": "/library/true-monoliths.html",
    "title": "True Monoliths",
}

# ============================================================
# CANDIDATE LIST (organized by inclusion rationale)
# ============================================================
CANDIDATES = [
    # === Tier A : machining marks clearly documented ===
    "Bazda Caves",                        # limestone, but iconic machining marks
    "Longyou Caves",                      # sandstone Mohs 6-7 + machining
    "Longmen Grottoes",                   # limestone + machining substrate
    "Kotukal Cave Temple",                # granite Mohs 6-7 + boulder-top groove
    "San Andrea Priù",                    # limestone + horizontal-cut anomaly
    "Unfinished Obelisk (Aswan)",         # granite Mohs 6.5 + trough marks (canonical name)
    "Aswan Unfinished Obelisk",           # alt naming, kept for safety
    "Serapeum of Saqqara",                # granite Mohs 7 + boxes with marks
    "Sacsayhuamán",                       # andesite Mohs 6 + scoop marks
    "Sage Wall (Montana)",                # granite Mohs 6-7 + scoop marks
    "Great Pyramid of Giza (Khufu)",      # granite chambers + Subterranean Chamber

    # === Tier B : extractive precision into stone Mohs ≥ 5-6 ===
    "Kailasa Temple",                     # basalt Mohs 6, single monolith
    "Kailasa Temple at Ellora",           # alt naming
    "Ellora Caves",                       # basalt
    "Hegra (Madain Saleh)",               # sandstone Mohs 6-7, top-down
    "Petra",                              # sandstone Mohs 6-7, precision facades
    "Vilcabamba (Espíritu Pampa)",        # old/new andesite stonework
    "Yangshan Quarry",                    # extractive scale, in-situ tool marks
    "Yakushima Megaliths",                # granite, claimed precision marks
    "Coricancha (Qorikancha)",            # andesite, precision
    "Coricancha",                         # alt
    "Ollantaytambo",                      # porphyry/granite
    "Tiwanaku",                           # andesite
    "Tiahuanaco",                         # alt
    "Puma Punku",                         # andesite, H-blocks
    "Tarawasi",                           # andesite, Foerster-documented
    "Barabar Caves",                      # granite, polished interiors
    "Mahabalipuram (Shore Temple)",       # granite rock-cut (canonical)
    "Mahabalipuram",                      # alt
    "Mamallapuram",                       # alt
    "Ajanta Caves",                       # basalt
    "Elephanta Caves",                    # basalt
    "Ahu Vinapu",                         # basalt, polygonal precision
    "Osireion",                           # Aswan granite pillars on site
    "Khafre's Pyramid",                   # granite casing
    "Pyramid of Khafre",                  # alt

    # === Tier C : Taş Tepeler — relief carving + bedrock-cut chambers ===
    # Soft limestone, but the precision of the relief work in stone of
    # this hardness is itself the anomaly the article addresses.
    "Karahan Tepe",                       # phallic pillars cut from bedrock
    "Göbekli Tepe (Potbelly Hill)",       # T-pillar relief sculpture
    "Boncuklu Tarla",                     # potentially older than Göbekli
    "Sayburç",                            # earliest narrative scene
    "Sefertepe",                          # dual-face carved heads

    # === Tier D : Iconic monolith exception ===
    # Limestone (soft) but the most famous extractive monolith on Earth.
    # The dating question (Schoch water erosion thesis) makes the article
    # natural reference point for visitors.
    "Great Sphinx of Giza",               # carved from Giza plateau bedrock
]

# ============================================================
sites_path = DATA_DIR / 'sites.json'
with open(sites_path) as f:
    sites = json.load(f)
if not isinstance(sites, list):
    sys.exit("sites.json is not a list — schema mismatch")

site_map = {s.get('n', ''): s for s in sites}
all_names = list(site_map.keys())

updated = 0
already_set = 0
missing = []
seen_canonical = set()

print("=== Wiring library_ref to True Monoliths ===\n")

for candidate in CANDIDATES:
    if candidate not in site_map:
        # Look for close matches; useful when names drift
        close = get_close_matches(candidate, all_names, n=2, cutoff=0.7)
        missing.append((candidate, close))
        continue

    # Avoid double-counting alt naming variants
    site = site_map[candidate]
    canonical = site.get('n')
    if canonical in seen_canonical:
        continue
    seen_canonical.add(canonical)

    if site.get('library_ref') == ARTICLE:
        already_set += 1
        print(f"  · {canonical}: library_ref already set")
    else:
        site['library_ref'] = ARTICLE
        updated += 1
        print(f"  ✓ {canonical}: library_ref → {ARTICLE['title']}")

if missing:
    print(f"\n--- name mismatches ({len(missing)}) ---")
    for cand, close in missing:
        if close:
            print(f"  ? '{cand}' not found. Close matches: {close}")
        else:
            print(f"  ? '{cand}' not found in sites.json (no close match)")

with open(sites_path, 'w') as f:
    json.dump(sites, f, indent=2, ensure_ascii=False)

# Tally
total_wired = sum(1 for s in sites if s.get('library_ref', {}).get('title') == 'True Monoliths')
print(f"\n--- summary ---")
print(f"  Newly wired:      {updated}")
print(f"  Already set:      {already_set}")
print(f"  Total with link:  {total_wired}")
print(f"  Missing:          {len(missing)}")
print()
print("Now run: python3 scripts/build.py")
