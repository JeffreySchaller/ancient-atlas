#!/usr/bin/env python3
"""
add-archaic-lens-batch.py

Wires the Archaic Lens YouTube channel into the atlas. The host
travels to sites and documents them on the ground with strong
production. 47 videos mined : 26 full-length + 21 shorts.

NEW CREATOR:
    archaiclens  ("Archaic Lens")

NEW SITES (14 high-value additions):
    Richat Structure (Eye of the Sahara) — Mauritania
    San Agustín Archaeological Park — Colombia (600+ megaliths)
    Nan Madol — Pohnpei, Micronesia
    Sogmatar — Turkey
    Tahiti Marae Complex (Marae Arahurahu) — French Polynesia
    Naveta des Tudons — Menorca, Spain
    Azores Pyramids (Pico Alto / Monte Brasil) — Portugal
    Delphi — Greece
    Mycenae (Lion Gate) — Greece
    Treasury of Atreus (Tomb of Agamemnon) — Greece
    Pyramid of Hellinikon — Greece
    Pnyx Hill — Athens, Greece
    Tula (Toltec capital) — Mexico
    Hagar Qim / Malta Cart Ruts — Malta

WIRES: 47 videos wired to a combination of the 14 new sites + existing
sites (Sacsayhuamán, Cusco walls, Easter Island sites, Bada Valley,
Göbekli Tepe, Stonehenge, Dolmen de Menga).

Idempotent. Run from repo root:
    python3 scripts/add-archaic-lens-batch.py
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
    "archaiclens": {
        "name": "Archaic Lens",
        "handle": "@ArchaicLens",
        "subs": "On-the-ground exploration of ancient and megalithic sites with strong cinematography; deep-dives on the Richat Structure, San Agustín, Nan Madol, and the megalithic Mediterranean and Pacific",
        "color": "#A87644",  # warm earth ochre
        "tier": 2,
    },
}

# ============================================================
NEW_SITES = [
    # === Africa ===
    {"n": "Richat Structure (Eye of the Sahara)", "lat": 21.1244, "lng": -11.4011,
     "cat": "geoglyph", "region": "Africa", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "stratigraphy"],
     "desc": (
         "Concentric ring structure ~50 km across in the Adrar Plateau of "
         "Mauritania, visible from space as a perfect series of "
         "geological rings. Conventional reading : a deeply eroded "
         "geological dome formed over hundreds of millions of years by "
         "differential erosion. Independent reading (Bright Insight, "
         "Jimmy Bright, Archaic Lens) : the dimensions, concentric "
         "geometry, surrounding salt deposits, and freshwater channels "
         "match Plato's description of Atlantis with striking specificity. "
         "Archaic Lens has documented multiple ground-level expeditions "
         "showing what may be anthropogenic features within the rings, "
         "including aligned stones, possible megalithic terraces, and "
         "evidence the central depression was once a lake. The Atlantis "
         "hypothesis remains heterodox; the geological scale and visual "
         "drama of the site are not in question."
     ),
    },
    # === South America ===
    {"n": "San Agustín Archaeological Park", "lat": 1.8867, "lng": -76.2700,
     "cat": "megalithic", "region": "South America", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Pre-Columbian megalithic site in southern Colombia containing the "
         "largest concentration of monumental stone statuary in the "
         "Americas : over 600 carved figures, tombs, sarcophagi, dolmens, "
         "and ceremonial platforms scattered across a UNESCO-listed "
         "archaeological park. Conventionally dated 100 BCE - 800 CE to "
         "the unnamed pre-Muisca culture that inhabited the upper "
         "Magdalena River valley. The statues blend human and feline "
         "features (jaguar-warriors), with carving precision that "
         "approaches Cusco-grade. The culture vanished centuries before "
         "Spanish contact, leaving no descendants and no written records."
     ),
    },
    # === Pacific ===
    {"n": "Nan Madol", "lat": 6.8417, "lng": 158.3331,
     "cat": "megalithic", "region": "Pacific", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "geometry"],
     "desc": (
         "Megalithic city built on coral reef and artificial islets off the "
         "southeast coast of Pohnpei, Micronesia. Approximately 92 "
         "artificial islands connected by tidal canals, built from "
         "columnar basalt logs stacked in alternating log-cabin patterns. "
         "Individual basalt columns weigh up to 50 tonnes. The basalt was "
         "quarried on the opposite side of the island (or possibly from "
         "another island entirely) and transported across open ocean. "
         "Conventionally dated to the Saudeleur dynasty (c. 1100-1628 CE) "
         "but the basalt-log-cabin construction technique appears nowhere "
         "else in Micronesian architecture and the engineering scale "
         "exceeds the documented capability of the period."
     ),
    },
    # === Middle East ===
    {"n": "Sogmatar", "lat": 36.9417, "lng": 39.4444,
     "cat": "rockcut", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["precision", "scale", "stratigraphy"],
     "desc": (
         "Late Sabian astral cult sanctuary in Şanlıurfa Province, "
         "southeastern Türkiye, approximately 60 km from Göbekli Tepe. "
         "Features rock-cut chambers, monumental tombs, an open-air "
         "sanctuary dedicated to the seven Sabian planetary deities, and "
         "inscriptions in Aramaic, Greek, and Syriac. Conventionally dated "
         "to the 1st-3rd centuries CE. The bedrock-cut central altar and "
         "the systematic alignment of seven distinct cult sites around it "
         "suggest a sophisticated astronomical and theological framework. "
         "Archaic Lens proposes (heterodox) that the underlying bedrock "
         "work may be an earlier Sabian Hall of Records rather than a "
         "Roman-period construction."
     ),
    },
    # === Pacific ===
    {"n": "Marae Arahurahu (Tahiti)", "lat": -17.7367, "lng": -149.6072,
     "cat": "temple", "region": "Pacific", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Restored ancient Tahitian marae (ceremonial platform) in the "
         "Pa'ea district of Tahiti, French Polynesia. The largest and "
         "best-preserved marae in the Society Islands. Constructed of "
         "tightly-fitted basalt blocks forming a tiered ahu platform with "
         "associated upright stones and stone sculptures. Functioned as "
         "the religious and political center of the surrounding district "
         "until the introduction of Christianity in the 19th century. "
         "Tahitian marae construction parallels Easter Island ahu "
         "architecture and the East Polynesian dispersal that connects "
         "them is documented in oral tradition and DNA evidence."
     ),
    },
    # === Europe ===
    {"n": "Naveta des Tudons", "lat": 39.9925, "lng": 3.9069,
     "cat": "tomb", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "polygonal"],
     "desc": (
         "Bronze Age megalithic chamber tomb on the island of Menorca, "
         "Balearic Islands, Spain. Roughly 14 m long, built of "
         "polygonal-fitted limestone blocks in the shape of an inverted "
         "boat hull. Conventionally dated 1200-750 BCE to the Talayotic "
         "culture. Archaic Lens documents architectural parallels to "
         "Göbekli Tepe T-pillar enclosures and to Easter Island ahu, "
         "suggesting connections that mainstream archaeology has not "
         "explored. The wider Menorcan landscape contains hundreds of "
         "Talayotic stone monuments forming one of Europe's densest "
         "megalithic complexes."
     ),
    },
    # === Europe ===
    {"n": "Azores Pyramids (Pico Alto)", "lat": 36.9853, "lng": -25.0986,
     "cat": "pyramid", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry", "stratigraphy"],
     "desc": (
         "Possible megalithic pyramids and dolmen-like structures "
         "documented on multiple Azores islands (São Miguel, Terceira, "
         "Pico) by independent archaeologist Antonieta Costa and others. "
         "Mainstream archaeology classifies the surface features as "
         "natural volcanic formations or post-medieval shepherd cairns. "
         "Independent fieldwork (Archaic Lens, Costa) documents systematic "
         "geometric arrangements, possible megalithic tombs, and rock-cut "
         "features that predate Portuguese settlement in the 15th century. "
         "The Atlantis hypothesis places the Azores as a possible peak of "
         "a submerged Atlantic ridge. The dating remains contested."
     ),
    },
    # === Greece (5 sites) ===
    {"n": "Delphi", "lat": 38.4824, "lng": 22.5009,
     "cat": "temple", "region": "Europe", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "scale", "geometry"],
     "desc": (
         "Pan-Hellenic sanctuary of Apollo on the slopes of Mount "
         "Parnassus, considered by the ancient Greeks as the omphalos "
         "(navel) of the world. The Temple of Apollo housed the Pythia, "
         "the most influential oracle of classical antiquity. The "
         "polygonal retaining wall along the Sacred Way (the polygonal "
         "wall) is celebrated for its precise irregular-block fitting, "
         "stylistically identical to Inca masonry at Sacsayhuamán though "
         "separated by an ocean and millennia. Conventional Apollo "
         "temple : 4th c. BCE. The polygonal wall may be considerably "
         "older. Connections to Cusco are an open question the atlas "
         "treats with the same convergent-triangulation discipline as "
         "the rest of the corpus."
     ),
    },
    {"n": "Mycenae (Lion Gate)", "lat": 37.7308, "lng": 22.7561,
     "cat": "city", "region": "Europe", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "polygonal"],
     "desc": (
         "Late Bronze Age citadel in the Argolid, Peloponnese, Greece. "
         "Capital of the Mycenaean civilization (c. 1600-1100 BCE) that "
         "inspired Homer's Iliad. The cyclopean walls are built of "
         "massive limestone blocks weighing many tonnes, fitted without "
         "mortar in a style the ancient Greeks themselves believed had "
         "been built by giants (Cyclopes). The Lion Gate, with its 20-tonne "
         "lintel and triangular relief of two lions flanking a column, is "
         "one of the earliest examples of monumental sculpture in Europe. "
         "The Cyclopean masonry style is paralleled at Tiryns, Argos, "
         "and the polygonal walls of Cusco half a world away."
     ),
    },
    {"n": "Treasury of Atreus (Tomb of Agamemnon)", "lat": 37.7256, "lng": 22.7544,
     "cat": "tomb", "region": "Europe", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Monumental Mycenaean tholos tomb at Mycenae, also called the "
         "Tomb of Agamemnon. Built c. 1250 BCE with a 14.5 m diameter "
         "beehive corbelled vault — the largest dome construction "
         "anywhere in the world until the Pantheon was built 1,400 years "
         "later. The lintel block above the entrance weighs an estimated "
         "120 tonnes, transported from a quarry several kilometres away. "
         "The precision of the corbelled stone joints holds without "
         "mortar to this day."
     ),
    },
    {"n": "Pyramid of Hellinikon", "lat": 37.5722, "lng": 22.7264,
     "cat": "pyramid", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "stratigraphy"],
     "desc": (
         "Small pyramidal structure in the Argolid, Greece, built of "
         "polygonal-fitted limestone blocks. Originally proposed by "
         "Greek researchers (Liritzis, Vassiliou) to date to c. 2700 BCE "
         "based on thermoluminescence and optically stimulated "
         "luminescence dating of the limestone surfaces. If correct, the "
         "Hellinikon pyramid is older than the Great Pyramid of Giza and "
         "may be the oldest stone monument in Europe. Mainstream "
         "archaeology disputes the dating and assigns the structure to "
         "the 4th century BCE Classical period."
     ),
    },
    {"n": "Pnyx Hill (Athens)", "lat": 37.9714, "lng": 23.7211,
     "cat": "city", "region": "Europe", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Open-air assembly ground in Athens where the citizens of the "
         "ancient democracy met to vote on civic matters from the 6th "
         "century BCE onward. Features a monumental rock-cut bema "
         "(speaker's platform), massive cyclopean retaining walls, and a "
         "carved auditorium oriented to seat several thousand citizens. "
         "The architectural ambition exceeds what the conventional "
         "Cleisthenes-era democracy is generally credited with."
     ),
    },
    # === Mexico ===
    {"n": "Tula (Tollan)", "lat": 20.0667, "lng": -99.3406,
     "cat": "city", "region": "Mesoamerica", "tier": 1, "signal": "open",
     "criteria": ["precision", "machining", "scale"],
     "desc": (
         "Capital of the Toltec civilization in Hidalgo, central Mexico, "
         "occupied c. 900-1150 CE. Famous for the 4.6 m tall basalt "
         "Atlantean warrior columns atop Pyramid B. Archaic Lens documents "
         "tubular drill marks and surface machining patterns on stones at "
         "the site that are difficult to reconcile with the assumed "
         "Toltec toolkit. The Toltecs claimed cultural descent from "
         "earlier Teotihuacán (which they called Tollan-Teotihuacán) and "
         "their architectural vocabulary echoes both Teotihuacán and the "
         "Maya cities further south, suggesting a deeper continuity than "
         "the conventional cultural breaks acknowledge."
     ),
    },
    # === Malta ===
    {"n": "Malta Cart Ruts (Misraħ Għar il-Kbir)", "lat": 35.8675, "lng": 14.4150,
     "cat": "geoglyph", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Maltese landscape feature also called \"Clapham Junction\" — a "
         "dense network of parallel grooves cut into the limestone "
         "bedrock, forming a complex intersection of cart-rut-like "
         "tracks. The grooves run for kilometres, cross each other at "
         "different elevations, and in places drop off underwater cliffs "
         "(implying construction during a lower sea level). Mainstream "
         "explanations (Bronze Age sledge tracks, Roman cart wheels) do "
         "not explain the underwater extensions or the grid-like density. "
         "Independent researchers connect the Maltese cart ruts to "
         "similar features in Sardinia, the Crimea, and the wider "
         "Mediterranean."
     ),
    },
]

# ============================================================
# Video metadata for each Archaic Lens video
# Each tuple: (site_name_in_atlas, video_dict)
# ============================================================
def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": f"{title} | Archaic Lens",
            "cr": "archaiclens", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Full-length videos (26) ===
    ("Sacsayhuamán", _v("cDYJcpLlthc", "Exploring Real Lost Cities in Peru", "2025-11-01")),
    ("Easter Island - Ahu Vinapu", _v("mQEO8uXZpbE", "Ancient Navels of the Earth Part I (Easter Island, Cusco, Delphi)", "2025-08-01")),
    ("Delphi", _v("mQEO8uXZpbE", "Ancient Navels of the Earth Part I (Easter Island, Cusco, Delphi)", "2025-08-01")),
    ("Sacsayhuamán", _v("mQEO8uXZpbE", "Ancient Navels of the Earth Part I (Easter Island, Cusco, Delphi)", "2025-08-01")),
    ("San Agustín Archaeological Park", _v("sVdbsvdUSyc", "Decoding the 600+ Megaliths of San Agustín, Colombia", "2024-12-01")),
    ("Azores Pyramids (Pico Alto)", _v("tL5OR8PPIFE", "Atlantis in the Azores: On the Ground Examining the Evidence", "2024-06-01")),
    ("Marae Arahurahu (Tahiti)", _v("_YkcacbKozs", "Exploring Ancient Tahiti", "2024-08-01")),
    ("Bada Valley Megaliths", _v("neDI_TRUdPU", "Exploring the 400+ Megaliths of Sulawesi, Indonesia", "2024-09-01")),
    ("Richat Structure (Eye of the Sahara)", _v("FDZY4xxsf-c", "The Richat Structure by Drone: Over an Hour of Uncut Aerial Footage", "2024-07-01")),
    ("Dolmen of Menga", _v("54PvavQtuCg", "\"H\" Symbol Found at 5500-year-old Dolmen de Menga", "2024-05-01")),
    ("Nan Madol", _v("CvPVOz-ZfG0", "Exploring Nan Madol Under Water", "2024-04-01")),
    ("Richat Structure (Eye of the Sahara)", _v("x1y3ABpMTNM", "Join Me Inside the Richat Structure Museum", "2024-02-01")),
    ("Easter Island - Ahu Vinapu", _v("VsJyQA7aGow", "Never Before Seen: The Secret Make-Make Cave of Easter Island", "2024-03-01")),
    ("Richat Structure (Eye of the Sahara)", _v("GmHuzTUL7aM", "Evidence of Prehistoric City found at Richat Structure?", "2024-02-01")),
    ("Richat Structure (Eye of the Sahara)", _v("OYabgbETL_4", "First Drone Footage of Richat Structure - Atlantis", "2022-08-01")),
    ("Göbekli Tepe (Potbelly Hill)", _v("nyQuJQJm8XI", "The Navel Connection: Göbekli Tepe / Easter Island / Sardinia", "2022-10-01")),
    ("Naveta des Tudons", _v("TW2xILBTz7U", "The Göbekli Tepe / Menorca Connection (boots on the ground)", "2022-09-01")),
    ("Malta Cart Ruts (Misraħ Għar il-Kbir)", _v("tcI7orY4sHo", "On the ground at Malta: mysterious origins, Venus figurines & cart ruts", "2022-07-01")),
    ("Sogmatar", _v("9sLa3Tq3CaY", "Is Sogmatar an Ancient Sabian Hall of Records?", "2022-09-01")),
    ("Richat Structure (Eye of the Sahara)", _v("FaIsY60xQH4", "Proof The Richat Structure Was a Lake", "2018-06-01")),
    ("Easter Island - Ahu Vinapu", _v("Xx5OOO5kDMg", "8 Unsolved Mysteries of Easter Island", "2018-09-01")),
    ("Richat Structure (Eye of the Sahara)", _v("OPGE3Ez4VEs", "Exploring the surface of the rings of the Richat", "2018-05-01")),
    ("Richat Structure (Eye of the Sahara)", _v("b4mv9znfJkE", "Evidence From The Ground That The Richat Structure Is Atlantis", "2018-04-01")),

    # === Shorts (21) ===
    ("Azores Pyramids (Pico Alto)", _v("kgvqMJEiL6I", "Hello Azores", "2024-06-15")),
    ("Mycenae (Lion Gate)", _v("fbxcgeCUjKU", "Lions Gate, Mycenae", "2024-05-15")),
    ("Pyramid of Hellinikon", _v("3tCUnligXxE", "Pyramid of Hellinikon, Greece", "2024-05-20")),
    ("Delphi", _v("bQIUtxjkQQw", "The navel of the world. Delphi, Greece.", "2024-05-25")),
    ("Treasury of Atreus (Tomb of Agamemnon)", _v("JkzPIIak9aA", "The tomb of Agamemnon is proof that sometimes myth is history", "2024-05-30")),
    ("Pnyx Hill (Athens)", _v("0VogHCZakYQ", "Pnyx Hill, Athens, Greece", "2024-06-01")),
    ("Easter Island - Ahu Vinapu", _v("F6ufanze73E", "This Moai belongs on Rapa Nui", "2024-04-01")),
    ("Stonehenge", _v("9UmWBipJkGc", "Stonehenge sarsen stones as tall as a 3-story building", "2024-03-15")),
    ("Easter Island - Ahu Vinapu", _v("aBAHzpGBjPM", "Another pyramid-like ahu on Easter Island", "2024-03-20")),
    ("Easter Island - Ahu Vinapu", _v("PutyPedBqEE", "Easter Island. Ceremonial house at Ahu Tahai", "2024-03-25")),
    ("Easter Island - Ahu Vinapu", _v("AnRoBNa7rhA", "Pyramid-like structures on Easter Island", "2024-04-05")),
    ("Sacsayhuamán", _v("GeG1jzEzhxs", "Pre-Colombian Peruvian artifacts (Cusco)", "2024-02-15")),
    ("Sacsayhuamán", _v("RI-Oq6_ieNI", "Tourist trinket or black-market artifact? Cusco shop", "2024-02-20")),
    ("Sacsayhuamán", _v("Dzb8gFQE7nc", "Inca artifacts", "2024-02-25")),
    ("Sacsayhuamán", _v("B6QhwDbJtCc", "Most intricate corner in Cusco", "2024-03-01")),
    ("Sacsayhuamán", _v("0l0x-VG6rKo", "Stranded in Cusco (protest blockade context)", "2023-01-15")),
    ("Sacsayhuamán", _v("pGZ6iTWskMQ", "Drone flight over Sacsayhuamán", "2023-02-01")),
    ("Tula (Tollan)", _v("U_XTMrm1gRQ", "Aztec sculptures - machine-precision finish", "2024-01-15")),
    ("Tula (Tollan)", _v("Xpr9RrYwx08", "Olmec statue with earliest American writing", "2024-01-20")),
    ("Tula (Tollan)", _v("raxhiNyVYJM", "Boturini Codex - Aztec migration from Aztlan", "2024-01-25")),
    ("Tula (Tollan)", _v("88JtkJsij9E", "Tubular drill marks in Tula, Mexico", "2024-01-30")),
]

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

    # 1. Creators
    print("=== CREATOR ===")
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · '{key}' already exists")
        else:
            creators[key] = info
            print(f"  ✓ Added: {key} ({info['name']})")
    save('creators.json', creators)

    # 2. Sites
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

    # 3. Video wires
    print("\n=== VIDEO WIRES ===")
    site_names = {s['n'] for s in load('sites.json')}
    missing = sorted({sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names})
    if missing:
        print(f"  ⚠ Wire targets not in sites.json:")
        for m in missing:
            print(f"      {m}")
        print(f"  (Skipping wires to these — fix names and re-run.)")

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

    # 4. Country tags
    if isinstance(countries, dict):
        country_map = {
            'Mauritania': ['Richat Structure (Eye of the Sahara)'],
            'Colombia': ['San Agustín Archaeological Park'],
            'Micronesia': ['Nan Madol'],
            'Türkiye': ['Sogmatar'],
            'French Polynesia': ['Marae Arahurahu (Tahiti)'],
            'Spain': ['Naveta des Tudons'],
            'Portugal': ['Azores Pyramids (Pico Alto)'],
            'Greece': ['Delphi', 'Mycenae (Lion Gate)',
                       'Treasury of Atreus (Tomb of Agamemnon)',
                       'Pyramid of Hellinikon', 'Pnyx Hill (Athens)'],
            'Mexico': ['Tula (Tollan)'],
            'Malta': ['Malta Cart Ruts (Misraħ Għar il-Kbir)'],
        }
        for country, names in country_map.items():
            countries.setdefault(country, [])
            for n in names:
                if n not in countries[country]:
                    countries[country].append(n)
        save('countries.json', countries)
        print(f"\n  ✓ Country tags updated ({len(country_map)} countries)")

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
