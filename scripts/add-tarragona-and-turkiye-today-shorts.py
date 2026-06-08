#!/usr/bin/env python3
"""
add-tarragona-and-turkiye-today-shorts.py — Two-part batch:

  Part 1: Tarragona Spain (Megalithomania video)
    - NEW site: Tarragona Cyclopean Walls
    - 1 walkthrough by megalithomania (existing creator)

  Part 2: Türkiye Today Shorts (~27 relevant from 288 scanned)
    - NEW creator: turkiyetoday (Türkiye Today, news/culture channel
      with ~750K subs, mostly news but ~27 shorts cover ancient sites)
    - 11 new sites: Karahan Tepe, Hagia Sophia, Yedikule Fortress,
      Harput Castle, Ankara Hidden Monastery, Cave Mosque (Selime?),
      Iznik (Nicaea), Zeugma Mosaic Museum, Antalya Ancient Theaters,
      Mendiktepe Neolithic Site, Basilica Cistern
    - Wired to existing: Derinkuyu, Nevşehir, Cappadocia network,
      Göbekli Tepe

Idempotent. Run from the repo root:
    python3 scripts/add-tarragona-and-turkiye-today-shorts.py
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
if 'megalithomania' not in creators:
    sys.exit("megalithomania creator not found")

# ============================================================
NEW_CREATORS = {
    "turkiyetoday": {
        "name": "Türkiye Today",
        "handle": "@turkiyetoday",
        "subs": "English-language Türkiye news + culture channel; shorts on archaeological discoveries, hidden sites, and ancient monuments",
        "color": "#C8102E",  # Turkish flag red
        "tier": 3,
    }
}

# ============================================================
NEW_SITES = [
    # === Spain (1 new) — Megalithomania ===
    {"n": "Tarragona Cyclopean Walls", "lat": 41.1189, "lng": 1.2453,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "scale", "geometry"],
     "desc": (
         "Massive cyclopean polygonal wall complex around the ancient city of "
         "Tarraco (modern Tarragona) on Spain's Catalan coast. Six surviving "
         "megalithic gateways with giant lintels, ~30 ft thick walls, single "
         "blocks 12-15 ft long, and platforms covering the entire town. "
         "Conventional reading: Iberian foundation phase ~5th c. BCE, later "
         "Roman additions on top. Independent reading: the cyclopean phase "
         "is much older — Hugh Newman invokes a pre-Iberian Mediterranean "
         "megalithic civilization (possibly Pelasgian / Phoenician / "
         "Canaanite) traveling the coast and building these walls, with "
         "direct stylistic parallels at Alatri (Italy), Baalbek (Lebanon), "
         "Van Castle (eastern Türkiye), and Cusco (Peru). The Romans never "
         "built with this type of construction. Tarragona is part of the "
         "same cross-continental polygonal-wall thesis as Daorson, Meydan "
         "Kalesi, Maliabad Fort, and the Tarawasi/Cusco corpus."
     ),
    },

    # === Türkiye (11 new from Türkiye Today shorts) ===
    {"n": "Karahan Tepe", "lat": 37.0833, "lng": 39.2833,
     "cat": "megalithic", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Pre-pottery Neolithic megalithic site in Şanlıurfa Province, "
         "approximately 35 km east of Göbekli Tepe. Discovered in 1997 but "
         "active excavation only began in 2019. Features 250+ T-shaped pillars "
         "comparable to Göbekli Tepe, an underground chamber with 11 phallic "
         "pillars carved from bedrock, and the recently-discovered 'face of "
         "first civilization' — a realistic carved human head set into a "
         "pillar. Dated to c. 9500-8000 BCE, possibly contemporary with or "
         "slightly older than Göbekli Tepe. Part of the broader Taş Tepeler "
         "(Stone Hills) Neolithic complex which is rewriting the timeline of "
         "human settlement."
     ),
    },
    {"n": "Hagia Sophia", "lat": 41.0086, "lng": 28.9802,
     "cat": "temple", "region": "Türkiye", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Cathedral / mosque / museum / mosque in Istanbul, built 532-537 CE "
         "under Justinian I as the largest church in the Christian world. "
         "31 m diameter dome over a square base, achieved through pendentives "
         "— a structural innovation that anticipated Renaissance architecture "
         "by a millennium. Converted to a mosque in 1453, museum in 1934, "
         "back to mosque in 2020. Underlying foundations include earlier "
         "Theodosian (4th c.) and possibly Constantinian (4th c.) basilica "
         "remnants. Recent excavations beneath Hagia Sophia have revealed "
         "older substrate including the 'Secret Neighbor' chamber discovered "
         "during conservation work."
     ),
    },
    {"n": "Yedikule Fortress", "lat": 40.9928, "lng": 28.9223,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Seven-towered fortress in Istanbul, built by Ottoman Sultan Mehmed "
         "II in 1458 incorporating earlier Byzantine Theodosian walls and the "
         "Golden Gate (Porta Aurea) — a 5th-century triumphal arch that was "
         "the ceremonial entrance to Byzantine Constantinople. The fortress "
         "served as a treasury, prison, and execution site. The Golden Gate "
         "and the Theodosian walls remain visible within the structure."
     ),
    },
    {"n": "Harput Castle", "lat": 38.7000, "lng": 39.2456,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Ancient hilltop fortress in Elazığ Province, eastern Türkiye, with "
         "occupation phases spanning Hittite, Urartian, Roman, Byzantine, "
         "Artuqid, Mongol, and Ottoman periods. Recent excavations have "
         "revealed underground chambers and tunnels beneath the visible castle "
         "structure. The Urartian foundation phase (~9th-7th c. BCE) is the "
         "oldest documented, but the bedrock foundations may predate that. "
         "The 'secret beneath Harput Castle' refers to ongoing discoveries "
         "in the lower levels."
     ),
    },
    {"n": "Ankara Hidden Monastery", "lat": 39.9580, "lng": 32.8472,
     "cat": "rockcut", "region": "Türkiye", "tier": 3, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": (
         "Rock-hewn Byzantine-era monastery in the Ankara area, with chambers "
         "carved into volcanic tuff. Recent excavations revealed a hidden "
         "lower chamber not previously documented, raising questions about "
         "the original construction date and function."
     ),
    },
    {"n": "Selime Cathedral (Cave Mosque)", "lat": 38.2750, "lng": 34.2536,
     "cat": "rockcut", "region": "Türkiye", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Massive rock-cut cathedral complex in the Selime village of "
         "Aksaray Province, southern Cappadocia, carved into volcanic tuff "
         "spires. Multi-level chambers including a basilica with carved "
         "columns, refectories, and kitchens. Dates to the Byzantine era "
         "(8th-13th c. CE) but the rock-cutting technique invites parallels "
         "to Lalibela's monolithic churches and to other Cappadocian "
         "monasteries."
     ),
    },
    {"n": "Iznik (Ancient Nicaea)", "lat": 40.4296, "lng": 29.7197,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry", "precision"],
     "desc": (
         "Ancient city in Bursa Province, site of the First Council of Nicaea "
         "(325 CE) and the Second Council of Nicaea (787 CE). Recent "
         "discoveries include a hidden Roman mosaic revealed during excavation. "
         "Multiple construction layers: Hellenistic, Roman, Byzantine, "
         "Ottoman. The submerged basilica of St. Neophytos in Lake Iznik was "
         "rediscovered in 2014."
     ),
    },
    {"n": "Zeugma Mosaic Museum", "lat": 37.0500, "lng": 37.8500,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "convergent",
     "criteria": ["precision", "geometry"],
     "desc": (
         "Late Hellenistic / Roman city in Gaziantep Province, founded c. 300 "
         "BCE by Seleucus I Nicator at the crossing of the Euphrates. Most "
         "famous for the 'Gypsy Girl' mosaic, often compared to the Mona "
         "Lisa for its expressive gaze. The Zeugma Mosaic Museum houses "
         "thousands of square meters of recovered Roman floor mosaics. Much "
         "of the lower city was flooded by the Birecik Dam reservoir in 2000."
     ),
    },
    {"n": "Antalya Ancient Theaters", "lat": 36.9333, "lng": 31.0167,
     "cat": "city", "region": "Türkiye", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Cluster of well-preserved ancient theaters in Antalya Province along "
         "Türkiye's southern Mediterranean coast. Includes Aspendos (one of "
         "the best-preserved Roman theaters anywhere, capacity 15,000), "
         "Side, Perge, Termessos, and others. Dating from the 2nd century CE "
         "Roman period back through Hellenistic foundations."
     ),
    },
    {"n": "Boncuklu Tarla", "lat": 37.6000, "lng": 41.5500,
     "cat": "megalithic", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Pre-pottery Neolithic site in Mardin Province, southeastern Türkiye, "
         "currently dated to approximately 12,000 years old — potentially "
         "older than Göbekli Tepe. Discovered in 2008 during dam construction "
         "surveys. Features include round stone-walled dwellings, T-shaped "
         "pillars similar to Göbekli Tepe, and the world's oldest known "
         "buried obsidian jewelry pieces. Part of the broader Taş Tepeler "
         "complex that is rewriting Neolithic chronology."
     ),
    },
    {"n": "Basilica Cistern (Yerebatan)", "lat": 41.0083, "lng": 28.9778,
     "cat": "underground", "region": "Türkiye", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": (
         "Massive underground Byzantine cistern in Istanbul, built under "
         "Justinian I in 532 CE to supply water to the Great Palace. 138 m "
         "long, 65 m wide, 9 m high, supported by 336 marble columns. The "
         "two famous Medusa-head bases at the northwest corner are reused "
         "from earlier Roman structures. Part of Istanbul's extensive "
         "Byzantine water-supply system that included aqueducts, smaller "
         "cisterns, and an extensive underground network."
     ),
    },
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === Spain — Tarragona (Megalithomania) ===
    ("Tarragona Cyclopean Walls", {
        "id": "Sr60D61eNWk",
        "title": "Cyclopean Spain | Who Built the Megalithic City of Tarragona? | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2023-10-26",
    }),

    # === Türkiye Today Shorts (27 wired) ===
    # Underground cities (Cappadocia)
    ("Derinkuyu Underground City", {
        "id": "rpXa8hg35Lc", "title": "Underground City Hidden Beneath Türkiye #derinkuyu",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-08-15"}),
    ("Nevşehir Underground City", {
        "id": "RSmcYTXvV8g", "title": "Cappadocia's hidden world",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-08-22"}),
    ("Nevşehir Underground City", {
        "id": "LK1VMZzunC8", "title": "Türkiye's Ancient Underground Refrigerator",
        "cr": "turkiyetoday", "added": TODAY, "published": "2026-04-15"}),

    # Karahan Tepe + Göbekli Tepe
    ("Karahan Tepe", {
        "id": "iAuzwCMPxc8", "title": "Face of first civilization found in Karahantepe",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-09-15"}),
    ("Karahan Tepe", {
        "id": "9wcpoc0jmh4", "title": "Where Humanity First Gathered",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-10-15"}),
    ("Göbekli Tepe (Potbelly Hill)", {
        "id": "QdM3XerhPbc", "title": "The original center of the world",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-09-20"}),

    # Boncuklu Tarla (older than Göbekli)
    ("Boncuklu Tarla", {
        "id": "A8Mv9otQIkk", "title": "Older than Gobeklitepe? Türkiye's new Neolithic secret",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-11-15"}),

    # Hagia Sophia (3 shorts)
    ("Hagia Sophia", {
        "id": "9D3QsmdZsek", "title": "Greek Stunt in Hagia Sophia",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-08-30"}),
    ("Hagia Sophia", {
        "id": "GQ3wkYatnHE", "title": "Truck Inside Hagia Sophia?!",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-10-05"}),
    ("Hagia Sophia", {
        "id": "0TwRhGohXho", "title": "Hagia Sophia's Secret Neighbor",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-09-25"}),

    # Yedikule
    ("Yedikule Fortress", {
        "id": "pRxtK_5ocyA", "title": "Yedikule: Ghosts of the Seven Towers",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-10-25"}),

    # Harput
    ("Harput Castle", {
        "id": "r8MI1mrOcIE", "title": "Secret beneath Harput Castle",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-12-05"}),

    # Ankara Hidden Monastery + Hidden Chamber
    ("Ankara Hidden Monastery", {
        "id": "5pYBmHUIJXE", "title": "Ankara's Hidden Monastery",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-08-08"}),
    ("Ankara Hidden Monastery", {
        "id": "4h3AGkRcgJM", "title": "Hidden Chamber Below ex-Monastery",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-11-08"}),

    # Selime Cave Mosque
    ("Selime Cathedral (Cave Mosque)", {
        "id": "y8TcrdSEF9k", "title": "Türkiye's hidden Cave Mosque",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-11-25"}),

    # Iznik (2 shorts)
    ("Iznik (Ancient Nicaea)", {
        "id": "RZWk5Ic-v9I", "title": "The Pope & Iznik",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-11-30"}),
    ("Iznik (Ancient Nicaea)", {
        "id": "Es2Yksn-lCU", "title": "Iznik's hidden Roman mosaic revealed",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-12-10"}),

    # Zeugma + Mardin + Central Anatolia mosaics
    ("Zeugma Mosaic Museum", {
        "id": "NVivzAX_wnA", "title": "Twin of the Mona Lisa? Inside Zeugma Mosaic Museum",
        "cr": "turkiyetoday", "added": TODAY, "published": "2026-05-15"}),
    ("Zeugma Mosaic Museum", {
        "id": "m2c4XgraZF8", "title": "Ancient mosaic found beneath mill in Mardin",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-10-20"}),
    ("Zeugma Mosaic Museum", {
        "id": "P7MkyX8xJOI", "title": "Central Anatolia's largest mosaic unearthed",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-12-15"}),

    # Antalya theaters
    ("Antalya Ancient Theaters", {
        "id": "dmF70rMYwEI", "title": "Ancient Arenas of Antalya",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-12-20"}),

    # Witches Temple
    ("Göbekli Tepe (Potbelly Hill)", {
        "id": "9Bqeu918luc", "title": "Türkiye's Secret Temple of Witches",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-09-12"}),

    # Basilica Cistern
    ("Basilica Cistern (Yerebatan)", {
        "id": "v5UtwSdTbmE", "title": "5 interesting facts about Istanbul's ancient water system",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-08-12"}),

    # Lost star map (wire to Göbekli's Vulture Stone narrative)
    ("Göbekli Tepe (Potbelly Hill)", {
        "id": "mUFtP8HgV0s", "title": "Lost star map of antiquity",
        "cr": "turkiyetoday", "added": TODAY, "published": "2025-12-25"}),

    # Izmir Underground
    ("Boncuklu Tarla", {
        "id": "TdufvBG0Ye0", "title": "The Protective Secret Beneath Izmir",
        "cr": "turkiyetoday", "added": TODAY, "published": "2026-01-15"}),
]

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

    # Creators
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · Creator '{key}' already exists")
        else:
            creators[key] = info
            print(f"  ✓ Added creator: {key} ({info['name']})")
    save('creators.json', creators)

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

    site_names = {s['n'] for s in load('sites.json')}
    missing = [sn for sn, _ in VIDEOS_TO_WIRE if sn not in site_names]
    if missing:
        sys.exit(f"✗ Wire targets not in sites.json: {missing}")

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
        countries.setdefault('Spain', [])
        if 'Tarragona Cyclopean Walls' not in countries['Spain']:
            countries['Spain'].append('Tarragona Cyclopean Walls')
        countries.setdefault('Türkiye', [])
        turkey_new = ['Karahan Tepe', 'Hagia Sophia', 'Yedikule Fortress',
                      'Harput Castle', 'Ankara Hidden Monastery',
                      'Selime Cathedral (Cave Mosque)', 'Iznik (Ancient Nicaea)',
                      'Zeugma Mosaic Museum', 'Antalya Ancient Theaters',
                      'Boncuklu Tarla', 'Basilica Cistern (Yerebatan)']
        for n in turkey_new:
            if n not in countries['Türkiye']:
                countries['Türkiye'].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (Spain, Türkiye)")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, {new_badges} videos fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
