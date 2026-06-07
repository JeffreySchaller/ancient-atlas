#!/usr/bin/env python3
"""
add-ageless-rock-theme-1-italy-iran.py — Theme 1 of the Ageless Rock
multi-batch mining series.

THEME: Cyclopean Wall Continuity (Italy + Iran).

This batch directly extends the Mini Megaliths article thesis by adding the
Italian polygonal/cyclopean wall corpus that Hugh Newman invokes as the
European parallel to Cusco, plus the Achaemenid Persian corpus that bridges
Mediterranean cyclopean tradition into Iran.

  New sites (9):
    Italy:
      - Vetulonia       (Tuscany, cyclopean wall, "Lost Megalithic City of Gold")
      - Rusellae        (Tuscany, cyclopean wall)
      - Orbetello       (Tuscany coast, cyclopean wall with water erosion dating)
    Iran:
      - Cube of Zoroaster (Ka'bah-ye Zartosht)    at Naqsh-e Rustam
      - Tall-e Takht (Cyclopean Wall of Pasargadae)
      - Tomb of Cyrus the Great                    at Pasargadae
      - Zendan-e Soleyman (Tomb of Cambyses I?)    at Pasargadae
      - Qadamgah                                   (Maku, NW Iran)
      - Gur Dokthar (Daughter's Tomb)              (Bushehr area)

  Existing sites wired (4):
    Italy:  Cosa
    Iran:   Persepolis (2 videos), Pasargadae, Naqsh-e Rustam

  Total: 15 walkthroughs from agelessrock (added in Turkey batch).

None of the videos qualify for NEW badge (all 1-3 years old).

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-1-italy-iran.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run from repo root.")

TODAY = datetime.date.today().isoformat()
VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

def load(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)
def save(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# Verify agelessrock creator exists
creators = load('creators.json')
if 'agelessrock' not in creators:
    sys.exit("agelessrock creator not found — run add-ageless-rock-turkey-batch.py first.")

# ============================================================
NEW_SITES = [
    # --- Italy (3) ---
    {
        "n": "Vetulonia",
        "lat": 42.8500, "lng": 10.9650,
        "cat": "megalithic", "region": "Europe",
        "tier": 2, "signal": "open",
        "criteria": ["polygonal", "scale", "geometry"],
        "desc": (
            "Etruscan cyclopean-wall city in Tuscany, on a hill above Castiglione "
            "della Pescaia. Known locally as the 'Lost Megalithic City of Gold' for "
            "the abundance of gold jewelry recovered from its necropolis. The visible "
            "polygonal masonry shows bent corners and tight bedrock joinery directly "
            "comparable to the Andean tradition documented in Cusco. Conventional "
            "reading : 8th-3rd c. BCE Etruscan. Independent reading : the wall "
            "tradition extends across the Tyrrhenian coast at sites whose oldest "
            "construction phases have been dated by erosion patterns to earlier "
            "than the Etruscan presence."
        ),
    },
    {
        "n": "Rusellae",
        "lat": 42.8167, "lng": 11.1333,
        "cat": "megalithic", "region": "Europe",
        "tier": 2, "signal": "open",
        "criteria": ["polygonal", "scale", "geometry"],
        "desc": (
            "Etruscan-Roman city in Tuscany, near Grosseto, with one of Italy's "
            "longest surviving cyclopean walls (~3 km perimeter). Polygonal masonry "
            "with bent-corner joinery comparable to Vetulonia and Cosa. Multiple "
            "construction phases visible. Conventional dating: 7th c. BCE Etruscan, "
            "Roman expansion in 3rd c. BCE. Independent reading: the cyclopean phase "
            "predates the Etruscan attribution and aligns with the broader "
            "Mediterranean polygonal masonry tradition that Hugh Newman documents "
            "from Türkiye through Greece and Italy."
        ),
    },
    {
        "n": "Orbetello",
        "lat": 42.4361, "lng": 11.2150,
        "cat": "megalithic", "region": "Europe",
        "tier": 1, "signal": "open",
        "criteria": ["polygonal", "scale", "stratigraphy"],
        "desc": (
            "Cyclopean-walled coastal site on the Tyrrhenian sea, where portions of "
            "the wall descend below the current waterline. Water-erosion dating of "
            "submerged sections has placed the oldest construction phase at 6,000-"
            "7,000+ years old by some independent investigators, predating any "
            "Etruscan presence by millennia and pointing to a much earlier "
            "Mediterranean polygonal masonry tradition. Directly invoked by Hugh "
            "Newman and others as evidence that the Hellenistic / Etruscan "
            "attribution for cyclopean walls across Italy is too conservative. "
            "Conventional reading: Etruscan, then Roman. Independent reading: "
            "Neolithic or earlier substrate, later cultures built upon."
        ),
    },

    # --- Iran (6) ---
    {
        "n": "Cube of Zoroaster (Ka'bah-ye Zartosht)",
        "lat": 29.9889, "lng": 52.8758,
        "cat": "monolithic", "region": "Middle East",
        "tier": 2, "signal": "open",
        "criteria": ["precision", "scale", "geometry"],
        "desc": (
            "Square stone tower at Naqsh-e Rustam, across from the rock-cut tomb of "
            "Darius I. Carved from precision-fitted ashlar blocks with internal "
            "chamber accessible by an external stair. Function disputed: variously "
            "interpreted as a Zoroastrian fire temple, royal mausoleum, calendar "
            "tower, or archive. The precision of the joinery on hard limestone is "
            "remarked upon as exceptional even by Achaemenid standards. "
            "Conventional dating: 6th-5th c. BCE Achaemenid. Independent reading: "
            "the joinery quality and the function ambiguity invite older or "
            "alternative interpretations."
        ),
    },
    {
        "n": "Tall-e Takht (Cyclopean Wall of Pasargadae)",
        "lat": 30.1969, "lng": 53.1683,
        "cat": "megalithic", "region": "Middle East",
        "tier": 2, "signal": "open",
        "criteria": ["polygonal", "scale", "precision"],
        "desc": (
            "Massive cyclopean platform at Pasargadae, just north of the Tomb of "
            "Cyrus. Built of precisely-fitted polygonal limestone blocks of "
            "exceptional scale (some over 5 m long), with bent-corner joinery that "
            "directly mirrors the Cusco and Sacsayhuamán tradition. Conventional "
            "reading: Achaemenid platform begun under Cyrus the Great in the mid-6th "
            "c. BCE. Independent reading: the cyclopean phase shows precision and "
            "block scale inconsistent with other Achaemenid construction at the "
            "site, suggesting a much older substrate that Cyrus's masons inherited."
        ),
    },
    {
        "n": "Tomb of Cyrus the Great",
        "lat": 30.1944, "lng": 53.1672,
        "cat": "monolithic", "region": "Middle East",
        "tier": 1, "signal": "convergent",
        "criteria": ["precision", "scale"],
        "desc": (
            "Stepped stone monument at Pasargadae, the burial place of Cyrus II the "
            "Great. A gabled limestone chamber on a six-stepped pyramidal podium, "
            "approximately 11 m tall. The blocks are precisely cut and dry-fitted "
            "without mortar. The structure survived Alexander the Great's conquest "
            "in 330 BCE specifically because Alexander ordered it protected and "
            "restored. One of the few Achaemenid royal monuments preserved nearly "
            "intact."
        ),
    },
    {
        "n": "Zendan-e Soleyman (Tomb of Cambyses I?)",
        "lat": 30.2017, "lng": 53.1731,
        "cat": "monolithic", "region": "Middle East",
        "tier": 3, "signal": "open",
        "criteria": ["precision", "geometry"],
        "desc": (
            "Square tower at Pasargadae of nearly identical design to the Cube of "
            "Zoroaster at Naqsh-e Rustam. Local tradition associates it with "
            "Cambyses I (Cyrus the Great's father); some interpret it as a fire "
            "temple or sacred archive. The two paired structures (this one and "
            "Ka'bah-ye Zartosht 60 km south) raise questions about a shared "
            "tradition that mainstream Achaemenid chronology does not fully "
            "explain. Substantially ruined; only a partial wall remains."
        ),
    },
    {
        "n": "Qadamgah",
        "lat": 39.2944, "lng": 44.4936,
        "cat": "rockcut", "region": "Middle East",
        "tier": 3, "signal": "open",
        "criteria": ["precision", "geometry"],
        "desc": (
            "Rock-cut monument complex in West Azerbaijan Province near Maku, "
            "northwestern Iran. The site includes a Mithraic temple carved into the "
            "cliff face with precise rectangular niches and chambers, and an "
            "isolated monumental staircase carved into bedrock. Local tradition "
            "interprets the staircase as a 'footstep' of a sacred figure (qadamgah "
            "means 'place of the footstep' in Persian). The Mithraic association "
            "places the visible work in the 1st-3rd c. CE Parthian era, but the "
            "scale and precision of the rock-cutting invite earlier dating."
        ),
    },
    {
        "n": "Gur Dokthar (Daughter's Tomb)",
        "lat": 28.8000, "lng": 51.0000,
        "cat": "monolithic", "region": "Middle East",
        "tier": 3, "signal": "convergent",
        "criteria": ["precision"],
        "desc": (
            "Stepped stone monument in the Bushehr region of southwestern Iran, of "
            "similar design to the Tomb of Cyrus at Pasargadae but smaller. Local "
            "tradition associates it with the daughter of a king; mainstream "
            "scholarship attributes it to an early Achaemenid royal family member, "
            "possibly Cambyses or a related Cyaxares-era figure. Dry-fit precision "
            "masonry, no mortar."
        ),
    },
]

# ============================================================
# Videos to wire
# ============================================================
VIDEOS_TO_WIRE = [
    # --- Italy ---
    ("Cosa", {
        "id": "6tyAZMqTok8",
        "title": "Is the Cyclopean Wall of Cosa man-made?",
        "cr": "agelessrock", "added": TODAY, "published": "2023-04-15"}),
    ("Rusellae", {
        "id": "E0FKiizs86M",
        "title": "Mysterious Cyclopean Wall of Rusellae",
        "cr": "agelessrock", "added": TODAY, "published": "2023-04-22"}),
    ("Vetulonia", {
        "id": "51coNJLDx5s",
        "title": "[ Cyclopean Wall of ] Vetulonia - Lost [ Megalithic ] City of Gold",
        "cr": "agelessrock", "added": TODAY, "published": "2023-05-01"}),
    ("Orbetello", {
        "id": "mpc6eIDU59U",
        "title": "When was Cyclopean Wall in Orbetello built?",
        "cr": "agelessrock", "added": TODAY, "published": "2023-05-08"}),

    # --- Iran ---
    ("Qadamgah", {
        "id": "bZuLboPOpwE",
        "title": "Qadamgah Mithra Temple",
        "cr": "agelessrock", "added": TODAY, "published": "2025-04-01"}),
    ("Qadamgah", {
        "id": "c74fUFW_NPY",
        "title": "Qadamgah Monument : Awesome but Alone without story",
        "cr": "agelessrock", "added": TODAY, "published": "2025-04-15"}),
    ("Persepolis", {
        "id": "vZVC1yopTJ8",
        "title": "Mysterious Unfinished Tomb of King Darius III",
        "cr": "agelessrock", "added": TODAY, "published": "2025-04-29"}),
    ("Persepolis", {
        "id": "X84t7LR7AO4",
        "title": "Persepolis : Persian remnants of unknown origin",
        "cr": "agelessrock", "added": TODAY, "published": "2025-05-06"}),
    ("Pasargadae", {
        "id": "VuiDRW52vl4",
        "title": "Pasargadae Archaeological Site : Area 51 of Iran",
        "cr": "agelessrock", "added": TODAY, "published": "2025-05-13"}),
    ("Naqsh-e Rustam", {
        "id": "EAKa-ZOYR9o",
        "title": "Naqsh-e Rustam : Fantastic Four of Persia",
        "cr": "agelessrock", "added": TODAY, "published": "2025-05-20"}),
    ("Tall-e Takht (Cyclopean Wall of Pasargadae)", {
        "id": "4_LEdZwhRUo",
        "title": "Tall-e Takht Wall (Cyclopean Wall of Pasargadae)",
        "cr": "agelessrock", "added": TODAY, "published": "2025-05-27"}),
    ("Zendan-e Soleyman (Tomb of Cambyses I?)", {
        "id": "VUf1Qo7JK1s",
        "title": "Tomb of Cambyses I ( or Cube of Zoroaster? )",
        "cr": "agelessrock", "added": TODAY, "published": "2025-06-03"}),
    ("Cube of Zoroaster (Ka'bah-ye Zartosht)", {
        "id": "LmY6HkAg6tg",
        "title": "Cube of Zoroaster (Ka'abah-e Zarthost)",
        "cr": "agelessrock", "added": TODAY, "published": "2025-06-10"}),
    ("Gur Dokthar (Daughter's Tomb)", {
        "id": "opg30waN_yY",
        "title": "Persia : Daughter's Tomb ( Gur Dokthar )",
        "cr": "agelessrock", "added": TODAY, "published": "2025-06-17"}),
    ("Tomb of Cyrus the Great", {
        "id": "HFgMrpzkDG8",
        "title": "Persia : Tomb of Cyrus The Great",
        "cr": "agelessrock", "added": TODAY, "published": "2025-06-24"}),
]

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

    site_names = {s['n'] for s in sites}
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added site: {s['n']}")
    if sites_added:
        save('sites.json', sites)

    # Verify all wire targets exist
    site_names = {s['n'] for s in load('sites.json')}
    missing = [sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names]
    if missing:
        sys.exit(f"✗ Wire targets not in sites.json: {missing}")

    videos_wired = 0
    for site_name, v in VIDEOS_TO_WIRE:
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}")
    if videos_wired:
        save('videos.json', videos)

    if isinstance(countries, dict):
        for s in NEW_SITES:
            country = 'Italy' if s['n'] in ['Vetulonia', 'Rusellae', 'Orbetello'] else 'Iran'
            countries.setdefault(country, [])
            if s['n'] not in countries[country]:
                countries[country].append(s['n'])
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (Italy + Iran)")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
