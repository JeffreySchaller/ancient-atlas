#!/usr/bin/env python3
"""
add-hugh-newman-triple-batch.py — Hugh Newman triple gap-fill:
    Mesoamerica + UK Cornwall/Oxfordshire + Ireland.

This is the follow-up to add-hugh-newman-batch.py. Same editorial
discipline: only sites Hugh has direct dedicated coverage of, never
guessing.

EDITORIAL HONESTY NOTE — substitutions from the original ask:

    Asked                       Why substituted                Shipped instead
    -------------------------   ----------------------------   --------------------------------
    Copán (Honduras)            Hugh has no direct video       Cuicuilco
    Monte Albán                 Hugh has no direct video       Xochicalco
    El Tajín                    Hugh has no direct video       Comalcalco
    Sayil / Kabah               Hugh has no direct video       Aké + Izamal + Chaltun Ha
    Marlborough Mound           Hugh has no direct video       (skipped, atlas already has Silbury)
    Hill of Tara                Hugh has no direct video       Loughcrew
    Poulnabrone                 Hugh has no direct video       Carrowmore Megalithic Cemetery
    Knockmany                   Hugh has no video at all       Giant's Ring (Northern Ireland)

The substitutions are Hugh's actual coverage in those territories.
Tara / Poulnabrone / Marlborough Mound can come back for a future
batch with a different anchor creator.

NEW SITES (12):

    Mesoamerica (6):
        Cuicuilco                       — Mexico City, Mexico
        Xochicalco                      — Morelos, Mexico
        Comalcalco                      — Tabasco, Mexico
        Aké                             — Yucatán, Mexico
        Izamal Satellite Pyramids       — Yucatán, Mexico
        Chaltun Ha                      — Yucatán, Mexico

    UK (3):
        Rollright Stones                — Oxfordshire, England
        Mên-an-Tol                      — Cornwall, England
        Merry Maidens                   — Cornwall, England

    Ireland (3):
        Loughcrew                       — Co. Meath, Ireland
        Carrowmore Megalithic Cemetery  — Co. Sligo, Ireland
        Giant's Ring                    — Co. Down, Northern Ireland

NEW WIRES (~14):
    12 anchoring the new sites (one video covers both Izamal & Chaltun Ha)
    + 2 Newgrange fill (Anthony Murphy / Hugh Ireland interviews)

Idempotent. Run from repo root:
    python3 scripts/add-hugh-newman-triple-batch.py
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

NEW_SITES = [
    # === Mesoamerica ===
    {"n": "Cuicuilco", "lat": 19.3019, "lng": -99.1797,
     "cat": "pyramid", "region": "Americas", "tier": 1, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Circular stepped pyramid buried under volcanic lava on the "
         "southern edge of Mexico City. Cuicuilco is one of the oldest "
         "Mesoamerican pyramids — conventional dating places its main "
         "construction phase c. 800-200 BCE, but the Xitle volcano "
         "eruption that buried the city is geologically dated c. 245 "
         "BCE to as late as 1670 CE depending on which stratigraphic "
         "model is applied. The base diameter approaches 135 m. The "
         "circular footprint is anomalous in a region where rectangular "
         "stepped pyramids dominate, and Hugh Newman has explored "
         "alternative timelines that place an original pre-Xitle phase "
         "substantially earlier than the orthodox sequence."
     ),
    },
    {"n": "Xochicalco", "lat": 18.8047, "lng": -99.2967,
     "cat": "pyramid", "region": "Americas", "tier": 1, "signal": "open",
     "criteria": ["precision", "geometry"],
     "desc": (
         "Fortified pre-Columbian city on a hilltop in Morelos, Mexico, "
         "dominated by the Pyramid of the Plumed Serpent — covered on "
         "all four sides with precision-cut bas-relief Quetzalcoatl "
         "iconography in the same iconographic tradition that runs "
         "from Teotihuacan to Chichén Itzá. Xochicalco also preserves "
         "an underground observatory with a vertical light shaft that "
         "tracks the sun's zenith passages on May 14/15 and July 28/29. "
         "Conventional dating c. 650-900 CE, but the precision of the "
         "stonework and the astronomical engineering are consistent "
         "with the broader Mesoamerican megalithic tradition Hugh "
         "Newman documents across the region."
     ),
    },
    {"n": "Comalcalco", "lat": 18.2667, "lng": -93.2025,
     "cat": "pyramid", "region": "Americas", "tier": 2, "signal": "open",
     "criteria": ["machining", "stratigraphy"],
     "desc": (
         "Mayan city in the western lowlands of Tabasco, Mexico — the "
         "only major Mayan site built primarily of fired clay brick "
         "rather than the limestone block used everywhere else in the "
         "Maya world. Conventional dating places the city c. 250-1000 "
         "CE. What makes Comalcalco anomalous is the bricks themselves: "
         "many bear inscriptions and pictographic marks that include "
         "Old World script forms — Phoenician, Libyan, Iberian — "
         "documented since the 19th century and revisited in the "
         "diffusionist literature. Hugh Newman has filmed on-site and "
         "presents the brick inscription corpus as a working puzzle."
     ),
    },
    {"n": "Aké", "lat": 20.9300, "lng": -89.3033,
     "cat": "pyramid", "region": "Americas", "tier": 2, "signal": "open",
     "criteria": ["scale"],
     "desc": (
         "Ancient Mayan city in Yucatán, Mexico, distinguished by the "
         "massive flat-topped Pyramid of the Pillars — a stepped "
         "platform crowned with thirty-six cylindrical limestone "
         "columns up to 4 m tall arranged in a 6×6 grid. The Spanish "
         "built the Church of San Lorenzo directly on top of the "
         "pyramid in the colonial period, a literal layering visible "
         "today. Conventional dating places the megalithic phase in "
         "the Late Preclassic to Early Classic (c. 250 BCE - 600 CE). "
         "Hugh Newman covers Aké as a strong example of the "
         "Mesoamerican pattern of churches built directly atop "
         "pre-existing pyramid platforms."
     ),
    },
    {"n": "Izamal Satellite Pyramids", "lat": 20.9333, "lng": -89.0167,
     "cat": "pyramid", "region": "Americas", "tier": 2, "signal": "open",
     "criteria": ["scale"],
     "desc": (
         "Cluster of massive Mayan pyramids in and around the town of "
         "Izamal, Yucatán, Mexico, including Kinich Kak Moo — the "
         "largest pyramid in Yucatán by base area (200×180 m, 34 m "
         "tall) — and a constellation of satellite pyramids spread "
         "across the surrounding landscape. Conventional dating places "
         "the main construction in the Early Classic period (c. 250-600 "
         "CE). The Convento de San Antonio de Padua, one of the oldest "
         "monasteries in the Americas, was built in 1549 on top of one "
         "of the original pyramid platforms. Hugh Newman filmed the "
         "satellite cluster on a Mexico expedition."
     ),
    },
    {"n": "Chaltun Ha", "lat": 20.7050, "lng": -88.9500,
     "cat": "pyramid", "region": "Americas", "tier": 3, "signal": "open",
     "criteria": ["scale"],
     "desc": (
         "Little-documented Mayan pyramid site in Yucatán, Mexico, "
         "rediscovered in recent years and largely overlooked by "
         "mainstream archaeology. The site preserves a substantial "
         "stepped pyramid and platform group obscured by jungle "
         "regrowth. Conventional dating treats it as part of the "
         "broader Yucatán Maya tradition (Late Preclassic through "
         "Classic). Hugh Newman filmed an exploratory visit, treating "
         "Chaltun Ha as one of the many lesser-known pyramid sites "
         "that fill the gaps between the famous tourist centers."
     ),
    },

    # === UK (Cornwall + Oxfordshire) ===
    {"n": "Rollright Stones", "lat": 51.9756, "lng": -1.5708,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["geometry", "scale"],
     "desc": (
         "Complex of three Neolithic and Bronze Age megalithic "
         "monuments straddling the Oxfordshire-Warwickshire border "
         "in England: the King's Men stone circle (c. 2500-2000 BCE, "
         "33 m diameter, ~77 limestone stones), the King Stone single "
         "monolith, and the Whispering Knights portal dolmen "
         "(c. 3800-3500 BCE — substantially older than the circle). "
         "The three monuments span roughly two millennia of continuous "
         "ritual use. Maria Wheatley and Hugh Newman have documented "
         "geomantic landscape geometry connecting all three. Folk "
         "tradition holds the stones cannot be counted twice to the "
         "same total — a memetic remnant of the geometric anomalies."
     ),
    },
    {"n": "Mên-an-Tol", "lat": 50.1572, "lng": -5.6047,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["geometry"],
     "desc": (
         "Small but iconic megalithic monument on the moorland of "
         "West Penwith in Cornwall, England — a holed stone roughly "
         "1.3 m tall flanked by two upright menhirs, plus additional "
         "stones nearby that may once have formed a stone circle. "
         "Conventional dating places the monument in the Late Neolithic "
         "to Early Bronze Age (c. 3500-1500 BCE). The holed stone is "
         "the focus of long-standing folk-healing tradition — children "
         "and adults are passed through the hole for healing. "
         "Archaeoastronomers have proposed solar and lunar alignments "
         "through the aperture. Hugh Newman covers the site in his "
         "Cornwall megalithic surveys."
     ),
    },
    {"n": "Merry Maidens", "lat": 50.0658, "lng": -5.5908,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["geometry"],
     "desc": (
         "Late Neolithic stone circle in the West Penwith peninsula "
         "of Cornwall, England — nineteen granite stones forming a "
         "near-perfect circle 24 m in diameter, conventionally dated "
         "c. 2500-1500 BCE. The associated outliers The Pipers (two "
         "tall menhirs 400 m to the northeast) and the Tregiffian "
         "burial chamber make this a small ritual complex. Folk "
         "tradition holds the maidens were petrified for dancing on "
         "the Sabbath — a Christianized echo of an older animating "
         "myth. Hugh Newman films Merry Maidens in his Cornish "
         "megalithic series alongside Mên-an-Tol and the Hurlers."
     ),
    },

    # === Ireland ===
    {"n": "Loughcrew", "lat": 53.7444, "lng": -7.1119,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["geometry", "precision"],
     "desc": (
         "Complex of approximately thirty passage tombs spread across "
         "the Loughcrew hills (Slieve na Calliagh — 'mountain of the "
         "hag') in County Meath, Ireland. The cairns are conventionally "
         "dated c. 3300 BCE, contemporary with Newgrange and Knowth. "
         "Cairn T preserves the most spectacular megalithic art in "
         "Ireland: deeply carved concentric circles, sunburst motifs, "
         "and abstract symbols on multiple chamber stones. The cairn's "
         "passage is aligned on sunrise at the spring and autumn "
         "equinoxes — the rising sun illuminates the rear chamber and "
         "specific carvings in sequence. Hugh Newman documents the "
         "alignments and the Winnemucca petroglyph correspondence."
     ),
    },
    {"n": "Carrowmore Megalithic Cemetery", "lat": 54.2522, "lng": -8.5181,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["stratigraphy", "scale"],
     "desc": (
         "One of the oldest and largest megalithic cemeteries in "
         "Ireland and Europe — over thirty surviving dolmens and "
         "passage tombs across a 1 km² area of the Cúil Irra peninsula "
         "in County Sligo. Radiocarbon dates from Carrowmore Tomb 4 "
         "have returned ages as early as 5,400 BP (c. 4400 BCE), "
         "making the earliest tombs at Carrowmore older than Newgrange "
         "and contemporary with the oldest megalithic activity anywhere "
         "in western Europe. The central cairn Listoghil is aligned "
         "with the Halloween (Samhain) sunrise over Knocknarea. Hugh "
         "Newman covers Carrowmore as a key reference for the "
         "western-Atlantic megalithic chronology."
     ),
    },
    {"n": "Giant's Ring", "lat": 54.5436, "lng": -5.9558,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Massive late-Neolithic henge enclosing a small passage "
         "dolmen, located at Ballynahatty just south of Belfast in "
         "County Down, Northern Ireland. The henge bank is "
         "approximately 200 m in diameter and 4 m tall, conventionally "
         "dated c. 2700 BCE. At its geometric center stands a five-stone "
         "portal dolmen — the proportions of the ring to the dolmen "
         "are anomalous compared to other Irish henges. Recent "
         "geophysical survey revealed a substantial timber circle "
         "predating the stone phase, plus a separate timber palisaded "
         "enclosure adjacent to the henge. Hugh Newman covers the "
         "Giant's Ring as a critical Northern Ireland henge."
     ),
    },
]

def _v(vid, title, published="2024-01-01"):
    return {"id": vid, "title": title,
            "cr": "megalithomania", "added": TODAY, "published": published}

VIDEOS_TO_WIRE = [
    # === Mesoamerica new sites ===
    ("Cuicuilco", _v("DI69-81Ck9s",
        "Cuicuilco: Is A Mysterious Circular Pyramid in Mexico City 7,000 Years Old?",
        "2024-05-14")),
    ("Xochicalco", _v("X1pbhrpaobg",
        "Exploring the Mayan Temple of Quetzalcoatl | Xochicalco Pyramids & Observatory | Megalithomania",
        "2024-02-08")),
    ("Comalcalco", _v("Q09GQH9f9PU",
        "Comalcalco | Mysterious Inscriptions from Around the World in Ancient Mexico | Megalithomania",
        "2024-03-22")),
    ("Aké", _v("zav5PIVHqiI",
        "Hidden Ruins of the Maya | Churches Built on Pyramids & Megaliths in the Town of Aké, Mexico pt.2",
        "2024-04-18")),
    # Same video wired to two adjacent Yucatán sites — Hugh covers both in one film.
    ("Izamal Satellite Pyramids", _v("JJ-ZKBejuA8",
        "The Lost Pyramid of Chaltun Ha and the Satellite Pyramids of Izamal, Mexico | Megalithomania",
        "2024-05-02")),
    ("Chaltun Ha", _v("JJ-ZKBejuA8",
        "The Lost Pyramid of Chaltun Ha and the Satellite Pyramids of Izamal, Mexico | Megalithomania",
        "2024-05-02")),

    # === UK new sites ===
    ("Rollright Stones", _v("ysaNL0j37Ag",
        "The Rollright Stones Mystery | A New View of Stone Circles | Maria Wheatley | Megalithomania",
        "2024-07-08")),
    ("Mên-an-Tol", _v("9CdyQL4Cmwo",
        "Mên-an-Tol | Megalithic Anomalies and Giant Lore in Ancient Cornwall | Megalithomania",
        "2024-09-12")),
    ("Merry Maidens", _v("RxF2-dR6Y9s",
        "Merry Maidens & The Pipers | Exploring a Stunning Stone Circle in Ancient Cornwall | Megalithomania",
        "2024-08-30")),

    # === Ireland new sites ===
    ("Loughcrew", _v("xut5gv1kXlA",
        "Loughcrew | Megalithic Art in Ancient Ireland & The Winnemucca Connection | Megalithomania",
        "2024-10-08")),
    ("Carrowmore Megalithic Cemetery", _v("IDfs7uO_dhE",
        "The 7,000 Year Old Carrowmore Megalithic Cemetery in Ancient Ireland",
        "2024-06-10")),
    ("Giant's Ring", _v("_VQ8_LWEgNI",
        "The Giant's Ring | Neolithic Henge & Dolmen in Northern Ireland | Megalithomania",
        "2024-11-04")),

    # === Existing-site fill: Newgrange Ireland coverage ===
    ("Newgrange", _v("-R91cWmQGRE",
        "Anthony Murphy | The Discovery of Dronehenge near Newgrange in Ireland | Megalithomania",
        "2023-09-15")),
    ("Newgrange", _v("515ecDeMpqY",
        "Newgrange: Cygnus, Venus & Secret Alignments - Anthony Murphy & Hugh Newman",
        "2023-12-21")),
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

    print("=== NEW SITES ===")
    site_names = {s['n'] for s in sites}
    added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Already exists: {s['n']}")
        else:
            sites.append(s)
            added += 1
            print(f"  ✓ Added: {s['n']}")
    save('sites.json', sites)

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
        country_map = {
            'Mexico': ['Cuicuilco', 'Xochicalco', 'Comalcalco',
                       'Aké', 'Izamal Satellite Pyramids', 'Chaltun Ha'],
            'United Kingdom': ['Rollright Stones', 'Mên-an-Tol', 'Merry Maidens',
                                "Giant's Ring"],
            'Ireland': ['Loughcrew', 'Carrowmore Megalithic Cemetery'],
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
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {added} new sites, {wired} wires, {new_badges} fire NEW badge")
    print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
