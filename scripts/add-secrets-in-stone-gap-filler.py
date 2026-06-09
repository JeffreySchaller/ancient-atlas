#!/usr/bin/env python3
"""
add-secrets-in-stone-gap-filler.py

Comprehensive audit-and-fill batch for the Secrets in Stone channel
(Cassie Coppersmith / @CassieCoppersmith).

Current state: 11 unique Secrets in Stone video IDs wired across 21
site-mappings. Channel inventory: 19 full-length + 37 shorts = 56 videos.
Roughly half the channel's catalog is currently invisible to atlas users.

NEW SITES (7):
    Yeha — Ethiopia (Pre-Axumite)
    Marib Dam — Yemen
    Baraqish — Yemen
    Awwam Temple (Mahram Bilqis) — Yemen
    Barran Temple — Yemen
    Timna (Hajar Kuhlan) — Yemen
    Candi Sukuh — Java, Indonesia

NEW WIRES:
    9 missing full-length videos
    18 high-value shorts (the ones that map cleanly to a specific site)

Idempotent. Run from repo root:
    python3 scripts/add-secrets-in-stone-gap-filler.py
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
NEW_SITES = [
    # === Ethiopia (Pre-Axumite) ===
    {"n": "Yeha", "lat": 14.0936, "lng": 39.0428,
     "cat": "temple", "region": "Africa", "tier": 1, "signal": "open",
     "criteria": ["precision", "scale", "polygonal"],
     "desc": (
         "Pre-Axumite temple complex in Tigray Province, northern "
         "Ethiopia. The Great Temple at Yeha is the oldest standing "
         "building in Ethiopia, dated by mainstream archaeology to "
         "approximately 700 BCE — though the precision-cut limestone "
         "ashlar masonry (some blocks weighing several tonnes, fitted "
         "without mortar to sub-millimeter tolerance) prompts independent "
         "investigators to propose a foundation phase considerably "
         "earlier. The site shows strong Sabaean (south Arabian) "
         "architectural influence, suggesting cross-Red-Sea cultural "
         "exchange with what is now Yemen. Cassie Coppersmith's Ethiopia "
         "Part 2 documents the masonry parallels to the Yemeni "
         "Sabaean-era temples at Awwam and Barran."
     ),
    },
    # === Yemen ===
    {"n": "Marib Dam (Old Dam of Ma'rib)", "lat": 15.4136, "lng": 45.3514,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "polygonal"],
     "desc": (
         "Ancient hydraulic engineering monument near Marib, Yemen, "
         "capital of the Sabaean kingdom (c. 1200 BCE - 275 CE). The "
         "original dam was 580 m long and irrigated approximately 25,000 "
         "acres of cultivated land, supporting one of the wealthiest "
         "kingdoms of the ancient Near East. The sluice gates and "
         "spillway masonry feature precision-cut limestone blocks with "
         "interlocking joinery comparable to Greek and Roman engineering. "
         "Sabaean inscriptions document repeated dam failures and "
         "repairs across centuries; the final collapse c. 575 CE "
         "triggered the migration of the Arab tribes mentioned in the "
         "Quran. Recent reconstruction efforts have damaged the "
         "archaeological context."
     ),
    },
    {"n": "Baraqish (Yathill)", "lat": 16.0192, "lng": 44.8042,
     "cat": "city", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "polygonal"],
     "desc": (
         "Pre-Islamic fortified Minaean city in the Jawf region of "
         "northern Yemen. Originally called Yathill, occupied from "
         "approximately the 10th century BCE through Roman times. "
         "Massive defensive walls built of precision-cut limestone "
         "blocks fitted in cyclopean style, with inscriptions in the "
         "Minaean Old South Arabian script. The site was a major "
         "stop on the incense route between Arabia Felix and the "
         "Mediterranean. Multiple temples and a sophisticated water "
         "management system survive within the walls."
     ),
    },
    {"n": "Awwam Temple (Mahram Bilqis)", "lat": 15.4036, "lng": 45.3736,
     "cat": "temple", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "polygonal"],
     "desc": (
         "Largest Sabaean temple, dedicated to the moon god Almaqah, "
         "near Marib in Yemen. The oval temenos wall measures 100 × 75 m "
         "and stands up to 13 m tall — built of cyclopean limestone "
         "blocks fitted in polygonal masonry that recalls Mediterranean "
         "and Andean styles. Founded c. 8th century BCE, the temple "
         "continued in use for over a thousand years. Locally known as "
         "Mahram Bilqis (Sanctuary of the Queen of Sheba), tying the "
         "site to the biblical Sheba tradition. Excavations by the "
         "American Foundation for the Study of Man (1951-1952) and the "
         "University of Calgary (1990s onward) documented the precision "
         "of the joinery and the scale of the construction."
     ),
    },
    {"n": "Barran Temple", "lat": 15.4117, "lng": 45.3522,
     "cat": "temple", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": (
         "Sabaean temple complex near Marib, Yemen, also dedicated to "
         "the moon god Almaqah. Smaller than nearby Awwam but featuring "
         "the same precision-cut limestone masonry tradition with six "
         "monumental pillars still standing. Dated c. 7th century BCE."
     ),
    },
    {"n": "Timna (Hajar Kuhlan)", "lat": 14.0992, "lng": 45.8500,
     "cat": "city", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "polygonal"],
     "desc": (
         "Ancient capital of the Qatabanian kingdom in the Bayhan valley "
         "of southwestern Yemen. Occupied c. 5th century BCE - 1st "
         "century CE. The city walls and temple complexes use cyclopean "
         "polygonal masonry comparable to other South Arabian sites and "
         "to Mediterranean megalithic traditions. Featured prominently "
         "in Cassie Coppersmith's Yemen Part 1 walkthrough."
     ),
    },
    # === Java, Indonesia ===
    {"n": "Candi Sukuh", "lat": -7.6242, "lng": 111.1314,
     "cat": "pyramid", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["geometry", "precision", "stratigraphy"],
     "desc": (
         "15th-century Hindu pyramid temple on the western slope of "
         "Mount Lawu in Central Java, Indonesia. The truncated pyramid "
         "structure is stylistically unlike any other Javanese temple "
         "and bears striking resemblance to Mesoamerican step pyramids "
         "(Yucatán, Tikal). Reliefs depict the Sudamala legend and "
         "include unusual iconography of metalworking, fertility, and "
         "what appears to be advanced surveying instruments. "
         "Conventionally dated to the late Majapahit period but the "
         "underlying foundation may be substantially older. Cassie "
         "Coppersmith's walkthrough documents the architectural "
         "anomalies that have led to comparisons with the Mesoamerican "
         "pyramid tradition."
     ),
    },
]

# ============================================================
def _v(vid, title, published="2025-01-01"):
    return {"id": vid, "title": f"{title} | Secrets in Stone",
            "cr": "secretsinstone", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Missing full-length videos (9) ===
    ("Tarawasi", _v("CUGsT9KKErE",
        "Megalithic Tarawasi: Peru's Hidden Mystery with Brien Foerster",
        "2026-05-20")),
    ("Si Thep (Khao Klang Nok)", _v("nuA2OlPJW1s",
        "The Buried Pyramid of Thailand & The Mystery of Si Thep",
        "2026-04-15")),
    ("Koh Ker", _v("l4ep1QxufRc",
        "Koh Ker's HIDDEN 7-Tier Pyramid & Colossal Lingas — Part 1",
        "2026-03-10")),
    ("Vat Phou", _v("Sks7sXjLpcY",
        "Vat Phou's Shattered Megaliths: Clues to an Ancient Catastrophe in Laos",
        "2026-02-15")),
    ("Angkor Wat", _v("s7TqoLPfaqI",
        "Forgotten Angkor: LiDAR Reveals Hidden Technology",
        "2026-01-20")),
    # The Yemen masterclass — covers 4 sites in one video
    ("Marib Dam (Old Dam of Ma'rib)", _v("JUL73K3vDDQ",
        "Yemen's Hidden Megaliths: Baraqish, Awwam, Barran, and the Old Marib Dam",
        "2025-08-10")),
    ("Baraqish (Yathill)", _v("JUL73K3vDDQ",
        "Yemen's Hidden Megaliths: Baraqish, Awwam, Barran, and the Old Marib Dam",
        "2025-08-10")),
    ("Awwam Temple (Mahram Bilqis)", _v("JUL73K3vDDQ",
        "Yemen's Hidden Megaliths: Baraqish, Awwam, Barran, and the Old Marib Dam",
        "2025-08-10")),
    ("Barran Temple", _v("JUL73K3vDDQ",
        "Yemen's Hidden Megaliths: Baraqish, Awwam, Barran, and the Old Marib Dam",
        "2025-08-10")),
    # Yemen Part 1 — Timna deep-dive
    ("Timna (Hajar Kuhlan)", _v("Tho9vWg1Ne8",
        "Yemen's Ancient Megalithic Mysteries Part 1 — Timna's Cyclopean Architecture",
        "2025-07-15")),
    # Ethiopia Part 2 — Pre-Axumite + Yemen connections (Yeha is the anchor)
    ("Yeha", _v("qLRqPjXmK38",
        "Uncovering Ethiopia's Ancient Megaliths Part 2: Pre-Axumite Temples and Connections to Yemen",
        "2025-07-01")),
    # Indonesia / Java
    ("Candi Sukuh", _v("WxYYyGXOmR4",
        "Java's Unexplainable Pyramid Temple: Candi Sukuh",
        "2025-06-15")),
    # Bolivia
    ("Samaipata (El Fuerte)", _v("iK_670S3wkk",
        "Unveiling El Fuerte de Samaipata: Bolivia's Hidden Megalithic Mystery",
        "2025-06-01")),

    # === High-value shorts that map to specific sites (18) ===
    ("Hampi", _v("wUmCRmaGNs0",
        "Ancient relics at Hampi, India — granite artifact",
        "2026-04-01")),
    ("Hampi", _v("OdF5oCz8W3I",
        "Granite artifact in Hampi: evidence of ancient lathing?",
        "2026-03-25")),
    ("Hampi", _v("8FyQBkxam0w",
        "Stone nubs on megalithic granite blocks at Hampi",
        "2026-03-20")),
    ("Tarawasi", _v("UrBKXFctyic",
        "Was Tarawasi exposed to very high heat? (with Brien Foerster)",
        "2026-05-15")),
    ("Easter Island - Ahu Vinapu", _v("EqsQDTVBQkc",
        "A new unit of megalithic measure — Easter Island",
        "2026-02-10")),
    ("Si Thep (Khao Klang Nok)", _v("CVGQuRAwZKs",
        "Thailand lingam at Si Thep",
        "2026-04-05")),
    ("Easter Island - Ahu Vinapu", _v("rOpEMhGMnrg",
        "Basalt 'toki' tool from Easter Island",
        "2026-01-25")),
    ("Easter Island - Ahu Vinapu", _v("LqQ-dymZQ9o",
        "Private collection obsidian mata'a from Easter Island",
        "2026-01-15")),
    ("Si Thep (Khao Klang Nok)", _v("VrMiF8umGmE",
        "UNESCO site of Si Thep",
        "2026-02-05")),
    ("Si Thep (Khao Klang Nok)", _v("zNWgi3h_c9I",
        "Si Thep — UNESCO ancient site",
        "2026-02-01")),
    ("Vat Phou", _v("HxqtnJ3tYgg",
        "Toppled and scattered megalithic structures at Vat Phou",
        "2025-12-15")),
    ("Koh Ker", _v("Y95QhEBMOuw",
        "Koh Ker — remains of one of its famous statues up close",
        "2025-11-20")),
    ("Koh Ker", _v("8EuShqdivWM",
        "Massive linga hidden at Koh Ker, still in one piece",
        "2025-11-15")),
    ("Koh Ker", _v("oAFrbit-D1g",
        "Precision artifacts at Koh Ker",
        "2025-11-10")),
    ("Koh Ker", _v("XBqyCFJt9J4",
        "Megalithic Koh Ker overview",
        "2025-11-05")),
    ("Vat Phou", _v("BWDt0ljLJvo",
        "Vat Phou — collapsed structure carved from boulder",
        "2025-12-10")),
    ("Vat Phou", _v("fd0wedyd8DY",
        "Serpent carvings at Vat Phou — dating questions",
        "2025-12-20")),
    ("Phnom Bok", _v("jMEy98Xet90",
        "Horizontal grooves at the ruined towers of Phnom Bok",
        "2025-10-20")),
    ("Angkor Wat", _v("o8f6w3IHS1A",
        "Angkor lathed artifact — how did the Khmer Empire produce this?",
        "2025-09-15")),
    ("Angkor Wat", _v("HSME49K2ZAI",
        "The many clamp marks of Angkor Wat",
        "2025-08-20")),
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

    # 1. Sites
    print("=== NEW SITES ===")
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

    # 2. Video wires
    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        print(f"  ⚠ Wire targets not found:")
        for m in missing:
            print(f"      {m}")

    videos_wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if site_name not in site_names:
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
            if pub_days <= 90:
                new_badges += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}{new_tag}")
    save('videos.json', videos)

    # 3. Country tags
    if isinstance(countries, dict):
        country_map = {
            'Yemen': ["Marib Dam (Old Dam of Ma'rib)", 'Baraqish (Yathill)',
                      'Awwam Temple (Mahram Bilqis)', 'Barran Temple',
                      'Timna (Hajar Kuhlan)'],
            'Ethiopia': ['Yeha'],
            'Indonesia': ['Candi Sukuh'],
        }
        for country, names in country_map.items():
            countries.setdefault(country, [])
            for n in names:
                if n not in countries[country]:
                    countries[country].append(n)
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {sites_added} new sites, {videos_wired} wires, {new_badges} fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
