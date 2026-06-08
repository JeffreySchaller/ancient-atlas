#!/usr/bin/env python3
"""
add-machining-criterion-architecture.py — Architecture + data batch.

Introduces a 7th criterion `machining` to the engineering-signature
taxonomy. Fixes the Bazda Caves badging problem and unlocks accurate
labeling for tool-mark-anomaly sites across the atlas.

  Code patches:
    1. public/index.html — append `machining` to SIGNAL_CRITERIA
    2. scripts/atlas-template.html (if present) — same patch for build persistence
    3. public/library/megaliths.html — add #machining anchor section

  Data updates:
    4. Bazda Caves: criteria REPLACED to ["machining", "scale"]
       (Old "precision"/"polygonal" badges don't fit subtractive rock-cut sites)
    5. Add `machining` to existing sites where applicable:
       - Longyou Caves, Sacsayhuamán, Serapeum of Saqqara, Yangshan Quarry,
         Sage Wall (Montana), Petra, Great Pyramid of Giza, Derinkuyu
    6. Add 3 new sites: Kotukal Cave Temple, San Andrea Priù, Longmen Grottoes
    7. Wire Bazda video (1ZjnsOl2OM8) to cross-reference sites:
       Longyou Caves, Longmen Grottoes, Kotukal Cave Temple, San Andrea Priù

Idempotent. Run from repo root:
    python3 scripts/add-machining-criterion-architecture.py
    python3 scripts/build.py
"""
import sys, json, datetime, re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry", "machining"}

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# ============================================================
# JS PATCH — append machining to SIGNAL_CRITERIA
# ============================================================
MACHINING_JS_ENTRY = """  machining: {
    label: 'Tool marks the period\\'s tools can\\'t produce',
    anchor: 'machining',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M3 8c4 2 5 -2 9 0s5 -2 9 0"/><path d="M3 14c4 2 5 -2 9 0s5 -2 9 0"/></svg>',
  },
"""

GEOMETRY_BLOCK_END_PATTERN = re.compile(
    r"(geometry:\s*\{[^}]+\},\s*)\n(\};)",
    re.DOTALL
)

def patch_signal_criteria_js(html_path: Path) -> bool:
    """Insert machining entry into SIGNAL_CRITERIA inline JS. Idempotent."""
    if not html_path.exists():
        return False
    txt = html_path.read_text()
    if "machining: {" in txt:
        print(f"  · {html_path.name}: machining entry already present")
        return False
    new_txt, n = GEOMETRY_BLOCK_END_PATTERN.subn(
        r"\1\n" + MACHINING_JS_ENTRY + r"\2", txt, count=1
    )
    if n == 0:
        print(f"  ✗ {html_path.name}: could not locate SIGNAL_CRITERIA insertion point")
        return False
    html_path.write_text(new_txt)
    print(f"  ✓ {html_path.name}: machining entry added to SIGNAL_CRITERIA")
    return True

# ============================================================
# LIBRARY PAGE PATCH — add #machining anchor section
# ============================================================
MACHINING_LIBRARY_SECTION = """
<section id="machining" class="library-criterion-section">
  <h2>Machining</h2>
  <p><strong>The signal :</strong> tool marks the period's tools cannot produce. Curved striations, gear-track grooves, scoop saddles, and motion patterns that hand chisels and copper saws cannot leave behind. These marks sit on the rock <em>before</em> any later smoothing or presentation layer was applied, which means they survive intact at sites where the finishing pass was never completed or has eroded away.</p>
  <p>The diagnostic is convergent : the same family of marks appears at Bazda Caves (Türkiye), Longyou Caves (China, 7,700 km away), the Serapeum of Saqqara (Egypt), Aswan's unfinished obelisk, Sacsayhuamán (Peru), Sage Wall (Montana), and Kotukal Cave Temple (India). Different rocks. Different climates. No documented contact. The marks are the same.</p>
  <p>Why this criterion is independent of <em>precision</em> and <em>polygonal</em> : those describe how blocks <em>fit</em>. Machining describes how blocks were <em>shaped</em>. A subtractive rock-cut site like Bazda has no joinery to evaluate, but it carries the tool-mark signature loudly. Conversely, a polygonal wall like Cusco fits the precision and polygonal criteria but also shows machining marks on individual block faces. The three criteria are orthogonal lenses on the same builder-toolkit puzzle.</p>
</section>
"""

def patch_library_page(html_path: Path) -> bool:
    """Append the #machining section to megaliths.html. Idempotent."""
    if not html_path.exists():
        return False
    txt = html_path.read_text()
    if 'id="machining"' in txt:
        print(f"  · {html_path.name}: #machining section already present")
        return False
    # Insert before the closing </main> tag if present, otherwise before </body>
    for closing in ['</main>', '</body>']:
        if closing in txt:
            txt = txt.replace(closing, MACHINING_LIBRARY_SECTION + '\n' + closing, 1)
            html_path.write_text(txt)
            print(f"  ✓ {html_path.name}: #machining section appended before {closing}")
            return True
    print(f"  ✗ {html_path.name}: no </main> or </body> found")
    return False

# ============================================================
# DATA — new sites
# ============================================================
NEW_SITES = [
    {"n": "Kotukal Cave Temple", "lat": 10.0500, "lng": 78.0500,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["machining", "precision"],
     "desc": (
         "Rock-cut Hindu cave temple in Tamil Nadu, southern India, "
         "carved into a boulder-like outcrop that emerges from the "
         "ground. The convergent triangulation interest lies in a "
         "specific feature: a deep horizontal groove cut across the "
         "top of the boulder, identical in form to grooves at Bazda "
         "Caves (Türkiye), San Andrea Priù (Sardinia), and several "
         "Chinese grotto sites. The conventional reading attributes the "
         "temple to medieval Hindu rock-cut tradition (~7th-9th c. CE). "
         "The independent reading flags the upper groove as a tool-mark "
         "signature of an earlier, cross-continental rock-cutting "
         "tradition that the temple was carved into."
     ),
    },
    {"n": "San Andrea Priù", "lat": 40.4083, "lng": 8.7833,
     "cat": "rockcut", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["machining", "scale"],
     "desc": (
         "Hypogeum (rock-cut tomb complex) in Bonorva, central Sardinia, "
         "Italy. Part of the broader domus de janas ('houses of the "
         "fairies') tradition of Sardinian rock-cut chambers, "
         "conventionally dated to the late Neolithic (c. 3500-2900 BCE). "
         "Notable for a long horizontal cut running across the cliff "
         "face in front of the cave entrances — a feature that has no "
         "obvious function for a tomb but matches similar horizontal "
         "cuts at Bazda Caves and Kotukal. The interior chambers show "
         "a mix of rock-cut chisel work and later Christian-era "
         "frescoes."
     ),
    },
    {"n": "Longmen Grottoes", "lat": 34.5550, "lng": 112.4740,
     "cat": "rockcut", "region": "China", "tier": 1, "signal": "convergent",
     "criteria": ["machining", "scale", "precision"],
     "desc": (
         "Buddhist cave temple complex on the Yi River near Luoyang, "
         "Henan Province, China. Over 100,000 Buddha statues carved "
         "into 2,345 caves along a 1 km cliff face. Construction "
         "primarily 493-1127 CE (Northern Wei through Northern Song "
         "dynasties). UNESCO World Heritage Site. While the figural "
         "carving is conventionally dated and well-documented, the "
         "underlying excavation technique — how the massive cliff "
         "chambers themselves were hollowed — shows the same horizontal "
         "raking tool marks documented at Longyou Caves and Bazda Caves. "
         "Bernie Ong (Ageless Rock) explicitly groups Longmen with "
         "Longyou as evidence of a pre-Buddhist subtractive tradition "
         "the medieval carvers worked into."
     ),
    },
]

# ============================================================
# DATA — criteria sweep (add machining to existing sites where applicable)
# ============================================================
ADD_MACHINING_TO = [
    "Longyou Caves",
    "Sacsayhuamán",
    "Serapeum of Saqqara",
    "Yangshan Quarry",
    "Sage Wall (Montana)",
    "Petra",
    "Great Pyramid of Giza (Khufu)",
    "Derinkuyu Underground City",
]

# Sites whose criteria need a hard REPLACEMENT, not append
REPLACE_CRITERIA = {
    "Bazda Caves": ["machining", "scale"],
}

# Sites whose signal should be flipped to "open" if it isn't already
PROMOTE_TO_OPEN = ["Longyou Caves", "Yangshan Quarry"]

# ============================================================
# DATA — video wires
# ============================================================
# The Bazda Caves video by Bernie Ong (Ageless Rock) draws explicit
# cross-references to these sites. Wire the same video to each of them
# so a viewer following the tool-mark thesis sees the connection in
# both directions.
BAZDA_VIDEO = {
    "id": "1ZjnsOl2OM8",
    "title": "Bazda Caves",
    "cr": "agelessrock", "added": TODAY, "published": "2025-10-19",
}
WIRE_BAZDA_TO = [
    "Longyou Caves",
    "Longmen Grottoes",
    "Kotukal Cave Temple",
    "San Andrea Priù",
]

# ============================================================
def main():
    for s in NEW_SITES:
        invalid = [c for c in s.get('criteria', []) if c not in VALID_CRITERIA]
        if invalid:
            sys.exit(f"✗ {s['n']}: invalid criteria {invalid}")

    print("=== CODE PATCHES ===")
    # Look for HTML files to patch
    html_candidates = [
        REPO_ROOT / 'public' / 'index.html',
        REPO_ROOT / 'scripts' / 'atlas-template.html',
    ]
    js_patched_any = False
    for p in html_candidates:
        if patch_signal_criteria_js(p):
            js_patched_any = True
    if not js_patched_any:
        print("  ⚠ No SIGNAL_CRITERIA patches applied. Atlas badge for")
        print("    'machining' won't render until JS is patched.")
        print("    (Will work after next build if atlas-template.html is patched.)")

    lib_candidates = [
        REPO_ROOT / 'public' / 'library' / 'megaliths.html',
    ]
    for p in lib_candidates:
        patch_library_page(p)

    print("\n=== DATA UPDATES ===")
    sites = load('sites.json')
    videos = load('videos.json')

    site_map = {s['n']: s for s in sites}

    # 1. REPLACEMENTS
    for name, new_crit in REPLACE_CRITERIA.items():
        if name not in site_map:
            print(f"  ⚠ {name} not found, skipping criteria replacement")
            continue
        old = site_map[name].get('criteria', [])
        if old == new_crit:
            print(f"  · {name}: criteria already {new_crit}")
        else:
            site_map[name]['criteria'] = new_crit
            print(f"  ✓ {name}: criteria {old} → {new_crit}")

    # 2. PROMOTE to open signal
    for name in PROMOTE_TO_OPEN:
        if name not in site_map:
            print(f"  ⚠ {name} not found, skipping signal promotion")
            continue
        if site_map[name].get('signal') == 'open':
            print(f"  · {name}: signal already open")
        else:
            old_sig = site_map[name].get('signal', '(none)')
            site_map[name]['signal'] = 'open'
            print(f"  ✓ {name}: signal {old_sig} → open")

    # 3. APPEND machining to existing criteria
    for name in ADD_MACHINING_TO:
        if name not in site_map:
            print(f"  ⚠ {name} not found, skipping machining addition")
            continue
        crit = list(site_map[name].get('criteria', []))
        if 'machining' in crit:
            print(f"  · {name}: machining already present")
        else:
            crit.append('machining')
            site_map[name]['criteria'] = crit
            print(f"  ✓ {name}: + machining → {crit}")

    # 4. New sites
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_map:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            site_map[s['n']] = s
            sites_added += 1
            print(f"  ✓ Added site: {s['n']}")

    save('sites.json', sites)

    # 5. Video wiring
    videos_wired = 0
    for site_name in WIRE_BAZDA_TO:
        if site_name not in site_map:
            print(f"  ⚠ {site_name} not in sites — skipping video wire")
            continue
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if BAZDA_VIDEO['id'] in existing_ids:
            print(f"  · Already wired: {BAZDA_VIDEO['id']} → {site_name}")
        else:
            videos[site_name].append(BAZDA_VIDEO)
            videos_wired += 1
            print(f"  ✓ Wired: {BAZDA_VIDEO['id']} → {site_name}")
    if videos_wired:
        save('videos.json', videos)

    # 6. Country tags
    try:
        countries = load('countries.json')
        if isinstance(countries, dict):
            countries.setdefault('India', [])
            if 'Kotukal Cave Temple' not in countries['India']:
                countries['India'].append('Kotukal Cave Temple')
            countries.setdefault('Italy', [])
            if 'San Andrea Priù' not in countries['Italy']:
                countries['Italy'].append('San Andrea Priù')
            countries.setdefault('China', [])
            if 'Longmen Grottoes' not in countries['China']:
                countries['China'].append('Longmen Grottoes')
            save('countries.json', countries)
            print(f"  ✓ Country tags updated (India, Italy, China)")
    except FileNotFoundError:
        pass

    sites = load('sites.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    machining_count = sum(1 for s in sites if 'machining' in s.get('criteria', []))
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Machining-tagged:   {machining_count}")
    print(f"  This batch:         {sites_added} new sites, {videos_wired} videos wired")
    print()
    print("Now run: python3 scripts/build.py")
    print()
    print("If atlas-template.html exists in scripts/, the SIGNAL_CRITERIA")
    print("patch will persist across rebuilds. If only public/index.html")
    print("was patched, next build will overwrite — apply the patch to")
    print("the template too for permanence.")

if __name__ == '__main__':
    main()
