#!/usr/bin/env python3
"""
add-ageless-rock-theme-6-pacific-peru-ersele.py — Theme 6.

  Hawaii (12 walkthroughs, all to new sites):
    - 6 new sites: Necker Island, Menehune Fishpond, Menehune Ditch,
      Wailua River Heiaus, Healing Stones of Kapaemahu, Hawaiian Heiaus

  Oceania (11 walkthroughs):
    - 2 wired to existing Nan Madol (Temwen Island 1+2)
    - 8 new sites: Latte Stones of Guam, Latte Stones of Tinian, Rota
      Quarry, Yap Rai Stones, Palau Megalithic Site, Kosrae Leluh
      Island, Marquesas Islands

  Peru (8 walkthroughs):
    - 3 wired to existing Machu Picchu (3-part series)
    - 5 wired to existing Ollantaytambo

  Ersele Underground City upgrade:
    - Update description: 2.5 km² spread, 5 levels deep, 7 entrances,
      22 preservation pits, water channels, cheese + wine production
      rooms — much larger than original description suggested
    - Update coordinates to actual Ozancık village location
    - Add: Ozancık Höyük (Bronze Age mound, ~100m diameter, first
      identified by archaeologist David French)

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-6-pacific-peru-ersele.py
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

creators = load('creators.json')
if 'agelessrock' not in creators:
    sys.exit("agelessrock creator not found")

# ============================================================
NEW_SITES = [
    # === Hawaii (6 new) ===
    {"n": "Necker Island Megalithic Site", "lat": 23.5750, "lng": -164.7000,
     "cat": "megalithic", "region": "Pacific", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Small remote island in the Northwest Hawaiian Islands, 250 km from Kauai, with 33 documented stone shrines (heiau) on its ridge — far more per square kilometer than anywhere in the main Hawaiian chain. The island has no fresh water and minimal soil; the question of who built and used these structures, and why, remains an open archaeological puzzle. Some readings invoke a pre-Polynesian (Menehune or other) substrate, with later Polynesian use built atop."},
    {"n": "Menehune Fishpond (Alekoko)", "lat": 21.9569, "lng": -159.3786,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Massive ancient fishpond near Lihue on Kauai, with a 270-meter-long curved stone wall enclosing 200,000 m² of water. Local tradition holds that the wall was built in a single night by the Menehune — a legendary race of small, skilled stone-workers said to predate the Polynesian Hawaiians. Construction date and method remain unresolved."},
    {"n": "Menehune Ditch (Kīkīaola)", "lat": 21.9678, "lng": -159.6889,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision", "geometry"],
     "desc": "Ancient stone-lined irrigation channel on Kauai with precisely fitted, cut-and-dressed basalt blocks resembling polygonal masonry traditions in Peru and Türkiye. The visible section is about 60 meters long. Local tradition again attributes the work to the Menehune. The precision of the stone-fitting is unique within Polynesian construction, which typically uses uncut stones. Mainstream archaeology dates the work to pre-contact Hawaii; independent investigators question the chronology and the cultural attribution."},
    {"n": "Wailua River Heiaus (Kauai)", "lat": 22.0481, "lng": -159.3372,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Cluster of seven major heiaus (sacred stone temples) along the Wailua River on Kauai, traditionally the seat of Kauai royalty. Includes Hikinaakala (sunrise temple), Holoholoku, Malae, and Poliahu. Several show astronomical alignments to solstices and equinoxes."},
    {"n": "Healing Stones of Kapaemahu (Oahu)", "lat": 21.2828, "lng": -157.8292,
     "cat": "megalithic", "region": "Pacific", "tier": 3, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Four massive boulders on Waikiki Beach, Oahu, traditionally said to embody the mana (spiritual power) of four mahu (third-gender) healers from Tahiti who arrived in Hawaii in the 15th-16th century. The stones weigh several tons each and were moved to their current location by ritual."},
    {"n": "Hawaiian Heiaus", "lat": 19.5000, "lng": -155.5000,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Stone temple platforms (heiau) found across all the Hawaiian Islands. Used for religious ceremonies, agricultural rites, navigation training, and royal lineage rituals. Multi-level stepped platforms with precisely fitted stones, often oriented to astronomical events. Dating ranges from early Polynesian settlement (~400-800 CE) through the kapu period."},

    # === Oceania (7 new) ===
    {"n": "Latte Stones of Guam", "lat": 13.3833, "lng": 144.7000,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Distinctive pillar-and-capstone stone supports (latte) erected across the Mariana Islands by the ancient Chamorro people. Each latte is a coral or limestone column topped with a hemispherical capstone (tasa). Functioned as foundations for elevated wooden houses. The House of Taga on Tinian and the Latte Stone Park in Hagåtña on Guam preserve the most monumental examples (up to 5 m tall). Date range: ~800-1700 CE."},
    {"n": "Latte Stones of Tinian", "lat": 14.9569, "lng": 145.6333,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "House of Taga site on Tinian preserves the largest standing latte stones in the Mariana Islands — pillars up to 5 m tall, paired with hemispherical capstones weighing several tons each. Quarried from coral limestone at Rota and transported to Tinian over open ocean. Construction techniques remain partially debated."},
    {"n": "Rota Quarry (As Nieves)", "lat": 14.1311, "lng": 145.1742,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Ancient quarry on Rota (Northern Mariana Islands) where the largest unfinished latte stones in the world remain in situ. The largest abandoned pillar would have stood 6.4 m tall and weighed 30+ tons. The quarrying technique and the reason for the abandonment of these stones remain open questions."},
    {"n": "Yap Rai Stones", "lat": 9.5167, "lng": 138.1167,
     "cat": "megalithic", "region": "Pacific", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Massive limestone discs (rai) used as currency on Yap Island, Federated States of Micronesia. The largest disc is 3.6 m in diameter and weighs 4 tons. Quarried not on Yap but on Palau, 400 km away, and transported by canoe across open ocean. Each stone retains its monetary identity even when transferred or lost — including a stone that fell into the sea but is still owned and traded."},
    {"n": "Palau Megalithic Site", "lat": 7.4750, "lng": 134.5717,
     "cat": "megalithic", "region": "Pacific", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Cluster of monolithic stones and earthwork terraces in the Republic of Palau, particularly the Badrulchau Stone Monoliths in northern Babeldaob — 37 standing basalt columns arranged in two rows, with some showing carved faces. Local tradition attributes them to gods. Construction date and purpose unconfirmed."},
    {"n": "Kosrae Leluh Island", "lat": 5.3033, "lng": 162.9881,
     "cat": "megalithic", "region": "Pacific", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "polygonal", "geometry"],
     "desc": "Ancient walled city on Leluh Island just off Kosrae, Federated States of Micronesia. Massive basalt walls (some over 8 m tall) enclose tomb compounds and royal residences. Construction style closely parallels Nan Madol (300 km away on Pohnpei) — both use natural basalt prisms laid in alternating directions. Active ~1250-1850 CE."},
    {"n": "Marquesas Islands", "lat": -9.0000, "lng": -139.5000,
     "cat": "megalithic", "region": "Pacific", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "French Polynesian archipelago with extensive megalithic stone platforms (paepae and tohua), tiki statues, and ceremonial complexes (me'ae). Includes the largest tiki statues in Polynesia (some over 2.5 m tall) and elaborate stone-paved plazas. Marquesan navigators are believed to have founded Hawaii and influenced early Easter Island culture."},

    # === Turkey — Ozancık Höyük (new) ===
    {"n": "Ozancık Höyük", "lat": 38.7280, "lng": 34.2100,
     "cat": "tomb", "region": "Türkiye", "tier": 3, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Bronze Age earthen mound approximately 100 m in diameter located adjacent to the Ersele Underground City complex near Ozancık village, Ortaköy district, Aksaray Province. First identified by British archaeologist David French. The mound was first mentioned in an 11th-century Turkish-Arabic dictionary. The name 'höyük' derives from old Turkish root meaning 'to rise.' Function and exact construction date unconfirmed; widely classified as Bronze Age construction but no formal excavation has been carried out. Sits in the same landscape as the 2.5 km² underground city below — the relationship between the mound above and the labyrinth below remains an unresolved archaeological question."},
]

# Update existing Ersele description (idempotent via marker check)
ERSELE_UPDATE = {
    "n": "Ersele Underground City",
    "lat": 38.7280,
    "lng": 34.2100,
    "desc": (
        "Massive underground complex near Ozancık village in Ortaköy district, "
        "Aksaray Province, also referred to locally as Ozancık Underground City. "
        "The complex spans approximately 2.5 km² with seven separate entrances "
        "and is documented as five levels deep. Includes 22 preservation pits, "
        "water channels, wells, and dedicated rooms for cheese and wine "
        "production. Significantly larger than most published references suggest "
        "and remains under-investigated relative to its scale. A Bronze Age mound "
        "(Ozancık Höyük, ~100 m diameter) sits adjacent on the surface above. "
        "Conventional reading : Byzantine-era defensive refuge consistent with the "
        "broader Cappadocian underground-city tradition. Independent reading : the "
        "tool-mark patterns, the chamber design (welcoming entrances inconsistent "
        "with a hiding place), and the relationship between the underground "
        "complex and the surface mound point to a much older substrate predating "
        "the regional defensive-refuge interpretation."
    ),
}

# ============================================================
VIDEOS_TO_WIRE = [
    # === Hawaii (12) ===
    ("Hawaiian Heiaus", {"id": "vtYn9wJaC4g", "title": "Ancient Fishpond and Fishtrap", "cr": "agelessrock", "added": TODAY, "published": "2024-12-01"}),
    ("Hawaiian Heiaus", {"id": "71H0fyHpB2s", "title": "Energies of Ancient Temples", "cr": "agelessrock", "added": TODAY, "published": "2024-12-08"}),
    ("Hawaiian Heiaus", {"id": "ywRHXRbADMs", "title": "Healing Heiaus of Hawaii", "cr": "agelessrock", "added": TODAY, "published": "2024-12-15"}),
    ("Healing Stones of Kapaemahu (Oahu)", {"id": "-Ze9JcGD6Ts", "title": "Healing Stones of Oahu", "cr": "agelessrock", "added": TODAY, "published": "2024-12-22"}),
    ("Necker Island Megalithic Site", {"id": "NqJY9gJK5pg", "title": "Megalithic Culture @ Necker Island", "cr": "agelessrock", "added": TODAY, "published": "2024-12-29"}),
    ("Menehune Fishpond (Alekoko)", {"id": "9lOgKCRTYLI", "title": "Mysterious Menehune Fishpond", "cr": "agelessrock", "added": TODAY, "published": "2025-01-05"}),
    ("Menehune Ditch (Kīkīaola)", {"id": "i7MelPWI5Ms", "title": "Mysterious Megalithic Menehune Ditch", "cr": "agelessrock", "added": TODAY, "published": "2025-01-12"}),
    ("Hawaiian Heiaus", {"id": "knPtO2v4U1E", "title": "Heiaus of Hawaii : Ancient Temple and Ancient Ponds", "cr": "agelessrock", "added": TODAY, "published": "2025-01-19"}),
    ("Hawaiian Heiaus", {"id": "0AS2SVcXYj4", "title": "Heiaus of Hawaii : Intriguing Hawaiian Terraces", "cr": "agelessrock", "added": TODAY, "published": "2025-01-26"}),
    ("Wailua River Heiaus (Kauai)", {"id": "0v6lAJf_Qe8", "title": "Heiaus of Hawaii : Wonders of Wailua", "cr": "agelessrock", "added": TODAY, "published": "2025-02-02"}),
    ("Hawaiian Heiaus", {"id": "4jNkHMbNSnE", "title": "Heiaus of Hawaii : Astronomical Megalithic Platforms", "cr": "agelessrock", "added": TODAY, "published": "2025-02-09"}),
    ("Hawaiian Heiaus", {"id": "QFRy-wesnk0", "title": "Heiaus of Hawaii : Mysterious Megalithic Platforms", "cr": "agelessrock", "added": TODAY, "published": "2025-02-16"}),

    # === Oceania (11) ===
    ("Latte Stones of Guam", {"id": "HWqycLvzXTU", "title": "Megalithic Latte Stones of Guam", "cr": "agelessrock", "added": TODAY, "published": "2025-02-23"}),
    ("Latte Stones of Tinian", {"id": "raeuYv9mP0w", "title": "Latte Stones in Tiny Tinian", "cr": "agelessrock", "added": TODAY, "published": "2025-03-02"}),
    ("Rota Quarry (As Nieves)", {"id": "vzsfqVKlYz4", "title": "Can you solve the mystery at Rota Quarry?", "cr": "agelessrock", "added": TODAY, "published": "2025-03-09"}),
    ("Yap Rai Stones", {"id": "WpLN2WB6Pyw", "title": "Yap Island 1: Money! Money! Money!", "cr": "agelessrock", "added": TODAY, "published": "2025-03-16"}),
    ("Yap Rai Stones", {"id": "fhVtZ_0NM9U", "title": "Yap Island 2: Rai Stone + Fei Stone = Limestone", "cr": "agelessrock", "added": TODAY, "published": "2025-03-23"}),
    ("Palau Megalithic Site", {"id": "Ieg9F3YQljQ", "title": "Palau Island 1 : Island of Monolithic Mysteries", "cr": "agelessrock", "added": TODAY, "published": "2025-03-30"}),
    ("Palau Megalithic Site", {"id": "oSSpTjmHNMg", "title": "Palau Island 2 : Rai Stone & Earthwork Terraces", "cr": "agelessrock", "added": TODAY, "published": "2025-04-06"}),
    ("Nan Madol", {"id": "4nPk4n7K0Mc", "title": "Temwen Island 1 : Megalithic City of Nan Madol", "cr": "agelessrock", "added": TODAY, "published": "2025-04-13"}),
    ("Nan Madol", {"id": "z8qRrFvZ1qQ", "title": "Temwen Island 2 : Magnetized City of Nan Madol", "cr": "agelessrock", "added": TODAY, "published": "2025-04-20"}),
    ("Kosrae Leluh Island", {"id": "p6bjaujVnqE", "title": "Kosrae Island : Megaliths of Leluh Island", "cr": "agelessrock", "added": TODAY, "published": "2025-04-27"}),
    ("Marquesas Islands", {"id": "MXmPInmNZNU", "title": "Mysterious and Marvelous Marquesas", "cr": "agelessrock", "added": TODAY, "published": "2025-05-04"}),

    # === Peru (8) — all to existing sites ===
    ("Machu Picchu", {"id": "1AWZs3hwqWg", "title": "Machu Picchu (1/3) : What happened here?", "cr": "agelessrock", "added": TODAY, "published": "2023-09-01"}),
    ("Machu Picchu", {"id": "2mjf6UI3VHQ", "title": "Machu Picchu (2/3) : Step Pyramid on Top?", "cr": "agelessrock", "added": TODAY, "published": "2023-09-08"}),
    ("Machu Picchu", {"id": "WckJe9zddB0", "title": "Machu Picchu (3/3) : Mysterious Temple of the Sun and Temple Mount", "cr": "agelessrock", "added": TODAY, "published": "2023-09-15"}),
    ("Ollantaytambo", {"id": "Osu8NEjk2rI", "title": "Ollantaytambo - Aqueducts of Unknown Origin", "cr": "agelessrock", "added": TODAY, "published": "2023-09-22"}),
    ("Ollantaytambo", {"id": "n5rhXvUKmmI", "title": "Ollantaytambo - Bedrock Terrace for Farming?", "cr": "agelessrock", "added": TODAY, "published": "2023-09-29"}),
    ("Ollantaytambo", {"id": "i3Yw5TODKlk", "title": "Ollantaytambo - Land of the Giants?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-06"}),
    ("Ollantaytambo", {"id": "9VQHhu3DRrg", "title": "Ollantaytambo - What is the story @ Wall of 6 Monoliths?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-13"}),
    ("Ollantaytambo", {"id": "JSLlvWKdtrs", "title": "Ollantaytambo : Endless mysteries", "cr": "agelessrock", "added": TODAY, "published": "2023-10-20"}),
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

    # 1. Update Ersele if present
    ersele_updated = False
    for s in sites:
        if s['n'] == 'Ersele Underground City':
            if s.get('desc') != ERSELE_UPDATE['desc']:
                s['lat'] = ERSELE_UPDATE['lat']
                s['lng'] = ERSELE_UPDATE['lng']
                s['desc'] = ERSELE_UPDATE['desc']
                ersele_updated = True
                print(f"  ✓ Updated Ersele Underground City description + coords")
            else:
                print(f"  · Ersele Underground City already up to date")
            break
    else:
        print(f"  ⚠ Ersele Underground City not found in sites.json — skipping update")

    # 2. Add new sites
    site_names = {s['n'] for s in sites}
    sites_added = 0
    for s in NEW_SITES:
        if s['n'] in site_names:
            print(f"  · Site already exists: {s['n']}")
        else:
            sites.append(s)
            sites_added += 1
            print(f"  ✓ Added site: {s['n']}")
    if sites_added or ersele_updated:
        save('sites.json', sites)

    site_names = {s['n'] for s in load('sites.json')}
    missing = [sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names]
    if missing:
        sys.exit(f"✗ Wire targets not in sites.json: {missing}")

    # 3. Wire videos
    videos_wired = 0
    new_badges = 0
    for site_name, v in VIDEOS_TO_WIRE:
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
            print(f"  ✓ Wired: {v['id']} → {site_name}  ({pub_days}d){new_tag}")
    if videos_wired:
        save('videos.json', videos)

    if isinstance(countries, dict):
        countries.setdefault('Hawaii', [])
        countries.setdefault('Oceania', [])
        countries.setdefault('Türkiye', [])
        hawaii_new = [s['n'] for s in NEW_SITES if s['n'] in
                      ['Necker Island Megalithic Site', 'Menehune Fishpond (Alekoko)',
                       'Menehune Ditch (Kīkīaola)', 'Wailua River Heiaus (Kauai)',
                       'Healing Stones of Kapaemahu (Oahu)', 'Hawaiian Heiaus']]
        oceania_new = [s['n'] for s in NEW_SITES if s['n'] in
                       ['Latte Stones of Guam', 'Latte Stones of Tinian',
                        'Rota Quarry (As Nieves)', 'Yap Rai Stones',
                        'Palau Megalithic Site', 'Kosrae Leluh Island', 'Marquesas Islands']]
        for c, names in [('Hawaii', hawaii_new), ('Oceania', oceania_new),
                         ('Türkiye', ['Ozancık Höyük'])]:
            for n in names:
                if n not in countries[c]:
                    countries[c].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, Ersele updated: {ersele_updated}, {new_badges} videos fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
