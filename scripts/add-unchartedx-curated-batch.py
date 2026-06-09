#!/usr/bin/env python3
"""
add-unchartedx-curated-batch.py

Curated UnchartedX additions — relationship-aware audit (Jeff is friends
with Ben Van Kerkwyk and Yousef Awyan). UnchartedX leans grounded
archaeological documentation with occasional speculative framing on
machining + precision themes, so the editorial filter is looser than
Praveen's: any site-specific walkthrough is admissible.

NEW SITES (8):
    Abu Sir — Egyptian Old Kingdom pyramid complex
    Abu Ghorab (Sun Temple of Niuserre) — Egypt, Old Kingdom
    Elephantine Island — Aswan, Egypt
    Coricancha — Cusco, Peru (Inca sacred temple)
    Tanis — Egypt, Ramesside capital
    Sphinx Temple — Giza, Egypt
    Khafre Valley Temple — Giza, Egypt
    Temple of Bastet (Bubastis) — Egypt

NEW WIRES (~20):
    Major UnchartedX walkthroughs across new and existing sites,
    including: Saqqara precision jars, Step Pyramid Djoser rare footage,
    Meidum Broken Pyramid, Osireion Live Walkthrough, Tiwanaku/Puma Punku
    studies, Khafre Causeway chamber.

Idempotent. Run from repo root:
    python3 scripts/add-unchartedx-curated-batch.py
    python3 scripts/build.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}")

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
    {"n": "Abu Sir (Pyramid Complex)", "lat": 29.8967, "lng": 31.2050,
     "cat": "pyramid", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["precision", "machining", "hardness"],
     "desc": (
         "Old Kingdom pyramid complex on the west bank of the Nile "
         "between Giza and Saqqara, used as the royal necropolis of "
         "the 5th Dynasty (c. 2494-2345 BCE). Contains the pyramids "
         "of Sahure, Neferirkare, Neferefre, and Niuserre, plus the "
         "sun temples of Userkaf and Niuserre. Independent researchers "
         "including UnchartedX have documented precision-machined "
         "granite artifacts including paired stone boxes with "
         "inner/outer precision tolerances that mainstream "
         "archaeology has not fully explained. The Abu Sir Papyri "
         "(found here in the 1890s) are among the oldest surviving "
         "administrative documents from ancient Egypt."
     ),
    },
    {"n": "Abu Ghorab (Sun Temple of Niuserre)", "lat": 29.9008, "lng": 31.2058,
     "cat": "temple", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["precision", "machining", "hardness"],
     "desc": (
         "Sun temple of the 5th Dynasty pharaoh Niuserre (c. 2400 BCE) "
         "located between Abu Sir and Saqqara, on the desert edge above "
         "the Nile floodplain. The site is famous for an exceptional "
         "collection of machined granite, basalt, and alabaster "
         "artifacts that show tool-mark signatures associated with "
         "rotary cutting and tube drilling. UnchartedX has documented "
         "what appears to be evidence of advanced precision work "
         "incongruent with the conventional Old Kingdom tool kit. "
         "The site is rarely visited and poorly published in "
         "mainstream Egyptology literature."
     ),
    },
    {"n": "Elephantine Island", "lat": 24.0856, "lng": 32.8911,
     "cat": "temple", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["precision", "machining", "hardness"],
     "desc": (
         "Island in the Nile at Aswan, the southern frontier of "
         "ancient Egypt and the ritual home of the god Khnum. The "
         "site contains a precision-cut granite box (now in fragments) "
         "and tool-mark surfaces that independent researchers cite as "
         "evidence of pre-Dynastic granite machining technology. The "
         "Elephantine box and related artifacts have been documented "
         "by UnchartedX as the 'smoking gun' for ancient machining: "
         "internal corners cut to radii inconsistent with hand "
         "chiseling, parallel inscribed lines at sub-millimeter "
         "consistency, and saw-mark patterns matching modern rotary "
         "tool signatures. Elephantine also held the famous "
         "Nilometer used for centuries to measure annual flood levels."
     ),
    },
    {"n": "Coricancha (Qorikancha)", "lat": -13.5198, "lng": -71.9764,
     "cat": "temple", "region": "South America", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "precision"],
     "desc": (
         "Most sacred Inca temple, located in central Cusco, Peru. The "
         "name means 'Golden Enclosure' in Quechua. Built atop earlier "
         "pre-Inca foundations, the structure features the highest-"
         "precision polygonal masonry in the Inca world, with massive "
         "andesite blocks fitted to sub-millimeter tolerances and "
         "curved enclosure walls of breathtaking geometric accuracy. "
         "Originally clad in solid gold sheeting, all melted down "
         "during the Spanish conquest. The Dominican church of Santo "
         "Domingo was built on top of the Inca foundations in the "
         "16th century, but the original temple walls remain visible "
         "and structurally intact, having survived multiple major "
         "earthquakes that destroyed colonial structures around them."
     ),
    },
    {"n": "Tanis (San el-Hagar)", "lat": 30.9789, "lng": 31.8800,
     "cat": "city", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["scale", "machining", "precision"],
     "desc": (
         "Ancient royal capital of the 21st and 22nd Dynasties "
         "(c. 1069-715 BCE) in the northeastern Nile Delta. Tanis "
         "served as the northern capital after Pi-Ramesses was "
         "abandoned, and many monuments at Tanis were transported "
         "wholesale from the earlier site, including obelisks, "
         "colossal statues, and inscribed blocks of Ramses II. The "
         "site contains what may be the largest stone statue ever "
         "carved in ancient Egypt: a granite colossus of Ramses II "
         "weighing approximately 1,000 tons in its original whole "
         "form. UnchartedX has documented the engineering "
         "implications of moving such a monolith from Aswan to the "
         "Delta, a distance of over 1,000 km."
     ),
    },
    {"n": "Sphinx Temple", "lat": 29.9747, "lng": 31.1372,
     "cat": "temple", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "precision"],
     "desc": (
         "Ritual structure directly east of the Great Sphinx at Giza, "
         "built from megalithic limestone core blocks subsequently "
         "cased in pink Aswan granite. The core blocks weigh up to "
         "100 tons each and are quarried from the same bedrock as the "
         "Sphinx itself, suggesting contemporaneous construction. "
         "Independent investigators (UnchartedX, Robert Schoch) "
         "note that water erosion patterns on the temple's core "
         "blocks support a pre-Dynastic origin date. Mainstream "
         "archaeology attributes the structure to Khafre (4th Dynasty), "
         "but no inscription from that era references it, and the "
         "construction technique differs significantly from "
         "contemporary 4th Dynasty work."
     ),
    },
    {"n": "Khafre Valley Temple", "lat": 29.9744, "lng": 31.1378,
     "cat": "temple", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "precision"],
     "desc": (
         "Megalithic ritual structure adjacent to the Sphinx Temple at "
         "Giza, traditionally attributed to Khafre (4th Dynasty). "
         "Construction features 100+ ton limestone core blocks faced "
         "with massive pink granite ashlars, fitted with the same "
         "polygonal precision seen in the Sphinx Temple and at "
         "Sacsayhuamán in Peru. The structure served as the eastern "
         "terminus of Khafre's pyramid causeway and was used for "
         "purification rituals before mummification. UnchartedX "
         "has documented joinery patterns inconsistent with "
         "conventional Old Kingdom masonry, suggesting the granite "
         "casing was added by Khafre over a much older megalithic "
         "core that predates the Dynastic period."
     ),
    },
    {"n": "Temple of Bastet (Bubastis)", "lat": 30.5722, "lng": 31.5089,
     "cat": "temple", "region": "Egypt", "tier": 2, "signal": "open",
     "criteria": ["precision", "scale"],
     "desc": (
         "Ancient temple complex at Tell Basta in the eastern Nile "
         "Delta, dedicated to the cat goddess Bastet. The temple was "
         "in use from the Old Kingdom through Ptolemaic times "
         "(c. 2400-30 BCE) and was famously described by Herodotus "
         "as the most beautiful in Egypt. The surviving precision-cut "
         "granite blocks, columns, and naos chambers show high-level "
         "machining tolerances that have drawn UnchartedX's attention "
         "for engineering documentation."
     ),
    },
]

# ============================================================
def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": "unchartedx", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === New sites ===
    ("Abu Sir (Pyramid Complex)", _v("qsIPLc1Auoo",
        "NEW Discoveries and Digs at Pyramid Site of Abu Sir! More Ancient Egyptian Lost Technology",
        "2024-04-10")),
    ("Abu Sir (Pyramid Complex)", _v("_JLrpiQT9cs",
        "A Megalithic Precision Box with an Inner Precision Box? The Ancient Relics of Abu Sir in Egypt!",
        "2020-02-15")),
    ("Abu Ghorab (Sun Temple of Niuserre)", _v("7_tQaDanMNE",
        "Ancient High Technology - the Machined Artifacts of Abu Ghorub - Old Kingdom Sun Temple",
        "2020-04-22")),
    ("Elephantine Island", _v("K80JebExyEY",
        "Smoking Gun Evidence for Ancient Granite Machining! Elephantine Island",
        "2023-06-08")),
    ("Coricancha (Qorikancha)", _v("dxmSz3N3HeU",
        "UnchartedX Podcast! Ollantaytambo, Coricancha and the Temple of the Moon with the Snake Bros!",
        "2021-03-18")),
    ("Tanis (San el-Hagar)", _v("LrPZM8ee690",
        "Ancient Tanis, Ramses II, and the Largest Stone Statue Ever Made",
        "2021-08-30")),
    ("Sphinx Temple", _v("gVWfLe7OTKI",
        "The Mystery of the Sphinx Temple! Evidence for Hidden Chambers, High Tech, and Secret Digs?",
        "2023-09-14")),
    ("Khafre Valley Temple", _v("pSF2fStHvKA",
        "The Valley Temple and the Sphinx - talking Egypt with Chuck from cfapps7865 channel",
        "2020-08-22")),
    ("Temple of Bastet (Bubastis)", _v("f1WKVWAsQj8",
        "Ancient Engineering at the Temple of Bastet",
        "2019-11-05")),

    # === Existing-site additions ===
    ("Pyramid of Meidum", _v("oG_Vnn8QkzQ",
        "The Unsolved Mysteries of the Broken Pyramid at Meidum, Egypt",
        "2020-07-19")),
    ("Step Pyramid of Djoser", _v("jHK2-MoR9Fs",
        "Rare Footage from Egypt - Ancient Machined Artifacts found deep beneath the Step Pyramid!",
        "2022-02-26")),
    ("Step Pyramid of Djoser", _v("iw_9He8fXxQ",
        "A Candid Look at the Amazing Artifacts Below the Step Pyramid! UnchartedX Live Walkthrough!",
        "2024-09-15")),
    ("Saqqara Necropolis", _v("7LEt8VM42PY",
        "Incredible Precision Stone Jars, and other unsolved mysteries of Saqqara!",
        "2021-04-25")),
    ("Osireion (Abydos)", _v("-TtsKKYLxPM",
        "The Megalithic Osirion of Egypt: Live Walkthrough and New Observations!",
        "2024-04-25")),
    ("Tiwanaku", _v("cyK_SMm_8LY",
        "How Old is Tiahuanaco? Is it the 'Cradle of American Man?'",
        "2023-11-20")),
    ("Puma Punku", _v("g0kf82I6ffc",
        "The Ancient Enigmas of Puma Punku and Tihuanaco",
        "2019-12-04")),
    ("Pyramid of Khafre", _v("yG-mCiTiSEE",
        "Is there an UNDISCOVERED chamber beneath the Khafre Causeway on the Giza Plateau?",
        "2022-10-15")),
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
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

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

    if isinstance(countries, dict):
        country_map = {
            'Egypt': ['Abu Sir (Pyramid Complex)',
                      'Abu Ghorab (Sun Temple of Niuserre)',
                      'Elephantine Island', 'Tanis (San el-Hagar)',
                      'Sphinx Temple', 'Khafre Valley Temple',
                      'Temple of Bastet (Bubastis)'],
            'Peru': ['Coricancha (Qorikancha)'],
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
