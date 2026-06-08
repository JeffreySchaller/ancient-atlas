#!/usr/bin/env python3
"""
add-ageless-rock-theme-7-egypt-israel-japan-scotland-portugal.py — Theme 7,
final theme of the Ageless Rock mining series.

  Egypt (9 walkthroughs, all to existing sites):
    Wired to: Khufu, Khafre, Menkaure, Djoser, Meidum, Bent, Red, Black

  Israel (12 walkthroughs):
    - 6 new sites: Zedekiah's Cave, Temple Mount (megaliths),
      Hezekiah's Tunnel, Jerusalem Archaeological Park, Horvat,
      Kidron Valley Tombs (7 sub-tombs consolidated into one site)

  Japan (5 walkthroughs):
    - 4 new sites: Hodota, Sakitama, Saitobaru, Koichi
    - 1 wired to existing Daisen Kofun

  Scotland (3 walkthroughs):
    - 2 new sites: Gilmerton Cove (2-part), Rosslyn Chapel + Castle

  Portugal (5 walkthroughs):
    - 5 new sites: Fornos de Algodres, Forcadas + Cortiço Dolmen,
      Necropolis of Sao Gens, Sao Miguel, Moreira de Rei

  Some of the Portugal videos qualify for NEW badge (recent uploads).

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-7-egypt-israel-japan-scotland-portugal.py
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
    # === Israel (6 new) ===
    {"n": "Zedekiah's Cave", "lat": 31.7833, "lng": 35.2306,
     "cat": "underground", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Massive man-made limestone cave system beneath the Muslim Quarter of the Old City of Jerusalem, extending 230 m into the bedrock under the Temple Mount. Traditionally attributed to King Solomon's quarries (1000 BCE). Local legend holds it was the escape route used by King Zedekiah when fleeing Babylonian siege in 587 BCE. Tool-mark analysis and the precision of the chamber walls invite older or alternative readings."},
    {"n": "Temple Mount Megaliths", "lat": 31.7780, "lng": 35.2354,
     "cat": "megalithic", "region": "Middle East", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "polygonal"],
     "desc": "Massive stone blocks at the western and southern retaining walls of the Temple Mount (Har HaBayit) in Jerusalem. The 'Western Stone' is the largest cut stone in the wall — 13.6 m long, 4.6 m high, 3 m deep, estimated to weigh 570 tons. Conventional reading: Herodian (1st century BCE - 1st century CE). Independent reading: the largest stones at the base may predate the Herodian retaining wall construction by centuries, with later building atop a much older substrate."},
    {"n": "Hezekiah's Tunnel", "lat": 31.7733, "lng": 35.2367,
     "cat": "underground", "region": "Middle East", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "533-meter rock-cut water tunnel in the City of David, Jerusalem, carved through solid bedrock to bring water from the Gihon Spring to the Pool of Siloam within the city walls. Dated by inscription to the reign of King Hezekiah (8th century BCE). The tunnel was excavated from both ends simultaneously — two teams of workers met in the middle, the meeting point still visible. The Siloam Inscription describing this is one of the oldest extant Hebrew inscriptions."},
    {"n": "Jerusalem Archaeological Park", "lat": 31.7766, "lng": 35.2371,
     "cat": "city", "region": "Middle East", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Open-air archaeological zone at the southwest corner of the Temple Mount in Jerusalem (the Davidson Center). Includes Robinson's Arch fragments, the Herodian street, the southern stairs, monumental ashlar walls, ritual baths, and multiple construction phases visible in stratigraphy from First Temple (8th c. BCE) through Islamic-period reconstruction."},
    {"n": "Horvat Midras", "lat": 31.6347, "lng": 34.9667,
     "cat": "underground", "region": "Middle East", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Roman-era ruined city in the Judean Foothills with extensive underground cave system, a small step-pyramid, and unique carved stone wheels of unknown function. Surface ruins date to Second Temple Period (516 BCE - 70 CE). The pyramid and the underground complex invite questions about earlier substrate construction and the function of the stone wheels."},
    {"n": "Kidron Valley Tombs", "lat": 31.7758, "lng": 35.2392,
     "cat": "tomb", "region": "Middle East", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Cluster of monumental rock-cut tombs in the Kidron Valley between Jerusalem's Old City and the Mount of Olives. Includes the Tomb of Absalom (1st c. CE, conical roof on a square base), the Tomb of Zechariah (free-standing pyramidal monolith carved from the cliff), the Tomb of the Sons of Hezir (Second Temple priestly family), the Tomb of Pharaoh's Daughter (Iron Age), and tombs traditionally attributed to Jehoshaphat, the Prophets, and King David. The precision rock-cutting and the freestanding nature of several monuments (carved from the cliff into freestanding forms) make this cluster unique among ancient tomb traditions."},

    # === Japan (4 new) ===
    {"n": "Hodota Kofun Cluster", "lat": 36.2833, "lng": 138.9000,
     "cat": "tomb", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Cluster of keyhole-shaped burial mounds (kofun) in Gunma Prefecture, Japan. Dates to the Kofun period (3rd-7th c. CE). The Hodota cluster includes multiple haniwa (clay figure) burial complexes whose function and design specifications still raise questions."},
    {"n": "Sakitama Kofun Cluster", "lat": 36.1300, "lng": 139.4789,
     "cat": "tomb", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Cluster of nine keyhole-shaped kofun in Saitama Prefecture, Japan, dating to the late 5th-6th c. CE. The Inariyama Kofun within the cluster yielded the famous gold-inlaid iron sword (Inariyama Sword) inscribed with one of the oldest extant Japanese-language inscriptions. Modern aerial views reveal striking geometric precision in the keyhole layouts."},
    {"n": "Saitobaru Kofun Cluster", "lat": 32.0833, "lng": 131.4167,
     "cat": "tomb", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Vast cluster of 311+ kofun in Miyazaki Prefecture, southern Japan. The largest single cluster of kofun in the country, spanning 4th-7th c. CE. The Osahozuka kofun is one of the largest. Sacred mountain setting associated with the mythological founding of Japan in the Nihon Shoki."},
    {"n": "Koichi Kofun Cluster", "lat": 34.5000, "lng": 135.5000,
     "cat": "tomb", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Lesser-documented kofun cluster in Japan whose size and proportions Ageless Rock investigates for parallels to the Mesoamerican and other monumental burial-mound traditions."},

    # === Scotland (2 new) ===
    {"n": "Gilmerton Cove", "lat": 55.8967, "lng": -3.1294,
     "cat": "underground", "region": "Europe", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Underground complex of chambers, tunnels, and stone-carved tables and benches in Edinburgh, Scotland. First officially recorded in 1724 when blacksmith George Paterson claimed to have spent five years digging it out as his dwelling — though the precision of the chamber finishing and the scale of the work invite skepticism of his account. Multiple theories: medieval drinking den, Knights Templar refuge, Druidic temple, Hellfire Club meeting place, or much older pre-Christian construction."},
    {"n": "Rosslyn Chapel & Castle", "lat": 55.8553, "lng": -3.1622,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "geometry"],
     "desc": "15th-century chapel near Edinburgh built by William Sinclair, with adjacent ruined castle. Famous for the Apprentice Pillar and extensive cryptic carvings interpreted variously as Templar, Masonic, or Rosicrucian symbolism. The chapel sits atop a foundation that some independent investigators read as much older — possibly a Picto-Celtic megalithic site that was later Christianized."},

    # === Portugal (5 new) ===
    {"n": "Tombs and Dolmens of Fornos de Algodres", "lat": 40.6300, "lng": -7.5400,
     "cat": "megalithic", "region": "Europe", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Megalithic tomb and dolmen cluster in the Fornos de Algodres municipality of central Portugal. Multiple Neolithic burial monuments dating to 4000-3000 BCE, including the Anta da Pera do Moço and surrounding dolmens. Part of the broader Iberian megalithic corpus that includes the Antequera dolmens to the south in Spain."},
    {"n": "Forcadas Tombs & Cortiço Dolmen", "lat": 40.6500, "lng": -7.5500,
     "cat": "megalithic", "region": "Europe", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Megalithic tomb cluster and dolmen in central Portugal near Cortiço da Serra. Neolithic construction (4000-3000 BCE), part of the wider Beira Alta megalithic landscape. The Cortiço Dolmen preserves carved decorative motifs on some stones."},
    {"n": "Necropolis of Sao Gens", "lat": 40.5800, "lng": -7.4500,
     "cat": "tomb", "region": "Europe", "tier": 3, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Medieval rock-cut tomb cluster (necropolis) in central Portugal. Anthropomorphic tombs cut directly into outcrop bedrock, typical of the Visigothic-to-medieval transitional period in Iberia (6th-12th centuries CE)."},
    {"n": "Necropolis of Saint Michael (Sao Miguel)", "lat": 40.5500, "lng": -7.4800,
     "cat": "tomb", "region": "Europe", "tier": 3, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Rock-cut tomb cluster (necropolis) in central Portugal, with anthropomorphic graves carved into bedrock. Medieval period attribution; part of the broader Iberian rock-cut burial tradition."},
    {"n": "Necropolis of Moreira de Rei", "lat": 40.4769, "lng": -7.1839,
     "cat": "tomb", "region": "Europe", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Rock-cut necropolis in Trancoso municipality, central Portugal. Anthropomorphic graves carved into the local granite bedrock outcrops, plus associated medieval church and castle structures atop the site. Active 6th-13th centuries CE."},
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === Egypt (9) — all to existing sites ===
    ("Great Pyramid of Giza (Khufu)", {"id": "b-kk-FyPhtE", "title": "Khufu's Pyramid - Simple Impossible Calculation", "cr": "agelessrock", "added": TODAY, "published": "2022-06-01"}),
    ("Pyramid of Khafre", {"id": "1-xPbEOaPCE", "title": "Is Khafre's Pyramid a man-made structure?", "cr": "agelessrock", "added": TODAY, "published": "2022-06-08"}),
    ("Pyramid of Menkaure", {"id": "56LYtSvC7BA", "title": "Menkaure gave us a clue how pyramid was made.", "cr": "agelessrock", "added": TODAY, "published": "2023-04-01"}),
    ("Step Pyramid of Djoser", {"id": "uERtkstQuxw", "title": "Pyramid of Djoser = Pyramid of Joseph?", "cr": "agelessrock", "added": TODAY, "published": "2023-04-08"}),
    ("Pyramid of Meidum", {"id": "DaAs-bMKOF0", "title": "Mysteries at Meidum are more mysterious than you think...", "cr": "agelessrock", "added": TODAY, "published": "2023-04-15"}),
    ("Bent Pyramid (Dahshur)", {"id": "9tEsueLITPw", "title": "Mind Bending Bent Pyramid of Egypt", "cr": "agelessrock", "added": TODAY, "published": "2023-04-22"}),
    ("Great Pyramid of Giza (Khufu)", {"id": "7F7hBRrovVE", "title": "7 Wonders of Ancient Pyramids in Egypt", "cr": "agelessrock", "added": TODAY, "published": "2023-04-29"}),
    ("Red Pyramid (Dahshur)", {"id": "6aqRoGIdVb8", "title": "Red Pyramid is highly unlikely a tomb.", "cr": "agelessrock", "added": TODAY, "published": "2023-05-06"}),
    ("Black Pyramid (Dahshur)", {"id": "mb9EdRZHNgU", "title": "The Black Pyramid of Amenemhat III in Dahshur, Egypt", "cr": "agelessrock", "added": TODAY, "published": "2023-05-13"}),

    # === Israel (12) ===
    ("Zedekiah's Cave", {"id": "n9Z_g9DcJXM", "title": "The Mysterious Zedekiah's Cave in Israel", "cr": "agelessrock", "added": TODAY, "published": "2022-08-01"}),
    ("Temple Mount Megaliths", {"id": "2s-ZHU8nQMU", "title": "Megaliths at Temple Mount in Israel?", "cr": "agelessrock", "added": TODAY, "published": "2022-08-08"}),
    ("Hezekiah's Tunnel", {"id": "3PhxvzpHXJ8", "title": "The Mysterious Hezekiah's Tunnel", "cr": "agelessrock", "added": TODAY, "published": "2022-08-15"}),
    ("Jerusalem Archaeological Park", {"id": "aflyBTMSA9g", "title": "Who Built The Jerusalem Archaeological Park in Israel?", "cr": "agelessrock", "added": TODAY, "published": "2022-08-22"}),
    ("Horvat Midras", {"id": "42-TXfjLNcE", "title": "Mysterious Caves + Pyramid + Stone Wheels = Horvat", "cr": "agelessrock", "added": TODAY, "published": "2022-09-01"}),
    ("Kidron Valley Tombs", {"id": "vhzH8rqsrFI", "title": "Kidron Valley of Tombs : Where is Zechariah's Tomb?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-01"}),
    ("Kidron Valley Tombs", {"id": "w-2wiRWTTDU", "title": "Kidron Valley of Tombs : Where is Absalom's Tomb?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-08"}),
    ("Kidron Valley Tombs", {"id": "5tJr2SR9Jtk", "title": "Kidron Valley of Tombs : Where is Pharaoh's Daughter Tomb?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-15"}),
    ("Kidron Valley Tombs", {"id": "JI_GONchbbA", "title": "Kidron Valley of Tombs : Sons of Hezir's Tomb", "cr": "agelessrock", "added": TODAY, "published": "2023-10-22"}),
    ("Kidron Valley Tombs", {"id": "LuT3lfx0lHQ", "title": "Kidron Valley of Tombs : Tomb of Jehoshaphat", "cr": "agelessrock", "added": TODAY, "published": "2023-10-29"}),
    ("Kidron Valley Tombs", {"id": "mggFDhg2Blc", "title": "Kidron Valley of Tombs : Tomb of the Prophets", "cr": "agelessrock", "added": TODAY, "published": "2023-11-05"}),
    ("Kidron Valley Tombs", {"id": "JsBqssFs7KY", "title": "Kidron Valley of Tombs : Tomb of King David", "cr": "agelessrock", "added": TODAY, "published": "2023-11-12"}),

    # === Japan (5) ===
    ("Daisen Kofun", {"id": "7PtSa57GKHs", "title": "Daisen Kofun in Mozu Cluster - Largest Tomb in the World", "cr": "agelessrock", "added": TODAY, "published": "2023-01-01"}),
    ("Hodota Kofun Cluster", {"id": "scQeyaB6Kvs", "title": "Hodota Kofun Cluster remains a mystery....", "cr": "agelessrock", "added": TODAY, "published": "2023-01-08"}),
    ("Sakitama Kofun Cluster", {"id": "PdMY7oDI_lU", "title": "Megalithic and futuristic kofuns of Sakitama", "cr": "agelessrock", "added": TODAY, "published": "2023-01-15"}),
    ("Saitobaru Kofun Cluster", {"id": "2kNvKb0VM2g", "title": "Mysterious Cluster of Kofuns in Saitobaru.", "cr": "agelessrock", "added": TODAY, "published": "2023-01-22"}),
    ("Koichi Kofun Cluster", {"id": "3lsp77wh6tU", "title": "Does Koichi Kofun Cluster in Japan have something to do with giants?", "cr": "agelessrock", "added": TODAY, "published": "2023-01-29"}),

    # === Scotland (3) ===
    ("Gilmerton Cove", {"id": "aF5PEPtZWUc", "title": "Gilmerton Cove (1/2) : Creepy Underground of Scotland", "cr": "agelessrock", "added": TODAY, "published": "2022-10-01"}),
    ("Gilmerton Cove", {"id": "m1EOoFpn_cg", "title": "Gilmerton Cove (2/2) : Jacob's Pillow = Coronation Stone?", "cr": "agelessrock", "added": TODAY, "published": "2022-10-08"}),
    ("Rosslyn Chapel & Castle", {"id": "COCcbw4vii8", "title": "Rosslyn Chapel + Rosslyn Castle = Megalithic Site?!?!", "cr": "agelessrock", "added": TODAY, "published": "2022-10-15"}),

    # === Portugal (5) — fresh uploads, some fire NEW badge ===
    ("Tombs and Dolmens of Fornos de Algodres", {"id": "GQOLob9ZK7E", "title": "Tombs and Dolmens of Fornos de Algodres", "cr": "agelessrock", "added": TODAY, "published": "2026-06-05"}),
    ("Forcadas Tombs & Cortiço Dolmen", {"id": "96gC9A1jmQg", "title": "Forcadas Tombs & Cortiço Dolmen", "cr": "agelessrock", "added": TODAY, "published": "2026-05-27"}),
    ("Necropolis of Sao Gens", {"id": "QfrIiH0qF18", "title": "Necropolis of Sao Gens", "cr": "agelessrock", "added": TODAY, "published": "2026-05-17"}),
    ("Necropolis of Saint Michael (Sao Miguel)", {"id": "qnH9XNBhrBQ", "title": "Necropolis of Saint Michael (Sao Miguel)", "cr": "agelessrock", "added": TODAY, "published": "2026-05-07"}),
    ("Necropolis of Moreira de Rei", {"id": "A4cG95SYO_M", "title": "Necropolis of Moreira de Rei", "cr": "agelessrock", "added": TODAY, "published": "2026-05-07"}),
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
        israel_new = ['Zedekiah\'s Cave', 'Temple Mount Megaliths', "Hezekiah's Tunnel",
                      'Jerusalem Archaeological Park', 'Horvat Midras', 'Kidron Valley Tombs']
        japan_new = ['Hodota Kofun Cluster', 'Sakitama Kofun Cluster',
                     'Saitobaru Kofun Cluster', 'Koichi Kofun Cluster']
        scotland_new = ['Gilmerton Cove', 'Rosslyn Chapel & Castle']
        portugal_new = ['Tombs and Dolmens of Fornos de Algodres',
                        'Forcadas Tombs & Cortiço Dolmen',
                        'Necropolis of Sao Gens',
                        'Necropolis of Saint Michael (Sao Miguel)',
                        'Necropolis of Moreira de Rei']
        for c, names in [('Israel', israel_new), ('Japan', japan_new),
                         ('Scotland', scotland_new), ('Portugal', portugal_new)]:
            countries.setdefault(c, [])
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
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, {new_badges} videos fire NEW badge")
    print()
    print("=" * 60)
    print("  AGELESS ROCK MINING COMPLETE — 7 THEMES SHIPPED")
    print("=" * 60)
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
