#!/usr/bin/env python3
"""
add-ageless-rock-theme-5-mesoamerica-alatri.py — Theme 5.

  Mexico (22 walkthroughs):
    - 3 wired to existing: Calakmul, Palenque, Cholula
    - 7 new sites: Teotihuacan: Pyramid of the Sun, Pyramid of the Moon,
      Pyramid of the Feathered Serpent + Chichen Itza, Coba,
      Chacchoben, Dzibanche

  Guatemala (16 walkthroughs):
    - 2 wired to existing: Tikal (8 videos), El Mirador (2 videos)
    - 5 new sites: Uaxactun, Yaxha, Nakum, Naranjo, Zaculeu

  Belize (4 walkthroughs):
    - 3 new sites: Caracol, Lamanai, Xunantunich

  Italy bonus (1 walkthrough):
    - Alatri (existing) — Megalithomania video, Hugh Newman explores
      the Pelasgian/Titan polygonal walls compared to Peru

  Note: "Pyramids of Mesoamerica" (V0wTRWFqh-8) appears in Mexico,
  Guatemala, and Belize playlists. Wired once to Cholula Pyramid as
  the regional overview anchor.

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-5-mesoamerica-alatri.py
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
for cr in ['agelessrock', 'megalithomania']:
    if cr not in creators:
        sys.exit(f"Creator {cr!r} not found")

# ============================================================
NEW_SITES = [
    # === Mexico (7 new) ===
    {"n": "Pyramid of the Sun (Teotihuacan)", "lat": 19.6925, "lng": -98.8438,
     "cat": "pyramid", "region": "Central America", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "The third-largest pyramid in the world by base area, at the heart of Teotihuacan, Mexico. 65 m tall, 220 m base, oriented to the setting sun on the day the sun passes its zenith at Teotihuacan's latitude. Built c. 200 CE. The Teotihuacanos who built it left no decipherable written language; the city was already in ruins when the Aztecs encountered it and named it 'Place Where the Gods Were Born.'"},
    {"n": "Pyramid of the Moon (Teotihuacan)", "lat": 19.6981, "lng": -98.8439,
     "cat": "pyramid", "region": "Central America", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Second-largest pyramid at Teotihuacan, aligned with the symmetry axis of the city and the contour of the sacred Mount Tlaloc behind it. 43 m tall. Built in seven construction phases between 100 BCE and 350 CE. Recent excavations have revealed elaborate offerings and burials beneath the pyramid."},
    {"n": "Pyramid of the Feathered Serpent (Teotihuacan)", "lat": 19.6862, "lng": -98.8408,
     "cat": "pyramid", "region": "Central America", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "scale", "geometry"],
     "desc": "Pyramid at the south of the Ciudadela complex at Teotihuacan, decorated with massive sculpted stone serpent heads and rain god (Tlaloc) panels. Tunnel discovered beneath the pyramid in 2003 has revealed extensive ritual offerings including liquid mercury and over 100,000 artifacts. Construction phase: 150-250 CE."},
    {"n": "Chichen Itza", "lat": 20.6843, "lng": -88.5678,
     "cat": "city", "region": "Central America", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Maya-Toltec city in Yucatán with multiple iconic structures: the Pyramid of Kukulkan (El Castillo), the Great Ball Court, the Temple of the Warriors, the Observatory (El Caracol), the Sacred Cenote, and the Ossuary Pyramid. Known for stunning acoustic effects: a clap at the base of Kukulkan produces a chirp identical to the quetzal bird call. Founded c. 6th century CE, peak occupation 800-1100 CE."},
    {"n": "Coba", "lat": 20.4914, "lng": -87.7333,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya city in the Yucatán jungle with the tallest pyramid in the northern Maya lowlands (Nohoch Mul, 42 m). Connected to other Maya cities by an extensive network of raised limestone causeways (sacbeob), some 100+ km long. Active 200-1100 CE."},
    {"n": "Chacchoben", "lat": 18.7167, "lng": -88.1500,
     "cat": "city", "region": "Central America", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya ceremonial center in southern Quintana Roo, Mexico. Multiple pyramids and monuments in the Petén style. Active c. 200 BCE to 700 CE. Less well-known than Tulum or Chichen Itza, with intact pyramids still surrounded by jungle."},
    {"n": "Dzibanche", "lat": 18.7333, "lng": -88.7500,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Important Maya city in southern Quintana Roo, capital of the Kaan dynasty during the Early Classic period. The Temple of the Owl, Temple of the Cormorant, and Temple of the Lintels are among the major structures. Famous for the wooden lintels preserved over a thousand years, with carved hieroglyphic inscriptions."},

    # === Guatemala (5 new) ===
    {"n": "Uaxactun", "lat": 17.3897, "lng": -89.6311,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya ceremonial center in the Petén jungle of Guatemala, 23 km north of Tikal. Features the E-Group astronomical complex used to mark solstices and equinoxes via the rising sun's position viewed from the main observation platform. Founded c. 1000 BCE."},
    {"n": "Yaxha", "lat": 17.0708, "lng": -89.4083,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya city on the shore of Lake Yaxha in Guatemala's Petén region. Featured astronomical alignments with both the cardinal directions and solstice sunrises. Multiple plazas, ball courts, and a network of causeways. Active from the Late Preclassic through Terminal Classic periods."},
    {"n": "Nakum", "lat": 17.1833, "lng": -89.3833,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "open",
     "criteria": ["scale"],
     "desc": "Large Maya city in Guatemala's Petén region, less studied than its neighbors. Recent investigations have revealed monumental architecture, including pyramids and acropolis complexes. Function and timeline remain partially open."},
    {"n": "Naranjo", "lat": 17.1306, "lng": -89.2369,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Major Maya city in Petén, Guatemala. Wealthy in carved stelae and elaborate hieroglyphic stairways. Engaged in rivalries and alliances with Tikal and Calakmul during the Classic period. Several large pyramids surrounding the central plaza."},
    {"n": "Zaculeu", "lat": 15.3433, "lng": -91.4900,
     "cat": "city", "region": "Central America", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Late Postclassic Maya city in the western highlands of Guatemala, capital of the Mam Maya kingdom. Stuccoed pyramids on multiple platforms. Conquered by Spanish forces in 1525 after a six-month siege. Modern restoration in the 1940s preserved the white-plastered appearance."},

    # === Belize (3 new) ===
    {"n": "Caracol", "lat": 16.7642, "lng": -88.9856,
     "cat": "city", "region": "Central America", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Largest Maya archaeological site in Belize. Caana ('sky-house') pyramid is the tallest man-made structure in Belize at 43 m. Caracol defeated Tikal in a Late Classic war (562 CE). At its peak the urban area covered 200 km² with an estimated population of 150,000. Extensive system of agricultural terraces and reservoirs."},
    {"n": "Lamanai", "lat": 17.7572, "lng": -88.6539,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya city in northern Belize on the New River Lagoon, with one of the longest continuous occupations of any Maya site — from c. 1500 BCE to the 19th century. The High Temple is 33 m tall. Notable for the Mask Temple with massive limestone face sculptures."},
    {"n": "Xunantunich", "lat": 17.0892, "lng": -89.1408,
     "cat": "city", "region": "Central America", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Maya city in western Belize. El Castillo pyramid is 40 m tall, with elaborate stucco friezes wrapping the upper levels depicting the Maya cosmos. Active Late Classic period (600-900 CE). Local folklore associates the site with a 'stone maiden' ghost — 'Xunantunich' means 'Stone Maiden' in Yucatec Maya."},
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === Mexico — Teotihuacan (3 years ago each) ===
    ("Pyramid of the Sun (Teotihuacan)", {"id": "BcH0PjNCfWg", "title": "Clueless @ Pyramids of the Sun at Teotihuacan", "cr": "agelessrock", "added": TODAY, "published": "2023-02-15"}),
    ("Pyramid of the Moon (Teotihuacan)", {"id": "jyn1dC7fgNE", "title": "Did giants built Pyramid of the Moon in Teotihuacan?", "cr": "agelessrock", "added": TODAY, "published": "2023-02-22"}),
    ("Pyramid of the Feathered Serpent (Teotihuacan)", {"id": "mxz6ktrGCRw", "title": "Pyramid / Temple of the Feathered Serpent @ Teotihuacan", "cr": "agelessrock", "added": TODAY, "published": "2023-03-01"}),

    # === Mexico — Chacchoben (6 months ago) ===
    ("Chacchoben", {"id": "EEShawZwoFQ", "title": "Chacchoben Ruins : Pyramid 1", "cr": "agelessrock", "added": TODAY, "published": "2025-12-15"}),
    ("Chacchoben", {"id": "pGAQOQzRjTA", "title": "Chacchoben Ruins : Pyramids and Monuments", "cr": "agelessrock", "added": TODAY, "published": "2026-01-08"}),

    # === Mexico — Coba (5 months ago) ===
    ("Coba", {"id": "nNuOW1JUrT0", "title": "Pyramids at Coba", "cr": "agelessrock", "added": TODAY, "published": "2026-01-15"}),

    # === Mexico — Chichen Itza (5 months to 3 months ago, 9 videos) ===
    ("Chichen Itza", {"id": "uFv2PoBdvj4", "title": "Chichen Itza : Astronomical Pyramid of Kukulkan", "cr": "agelessrock", "added": TODAY, "published": "2026-01-29"}),
    ("Chichen Itza", {"id": "cTzxU3nYSkA", "title": "Chichen Itza : Astounding Acoustic at Pyramid of Kukulkan", "cr": "agelessrock", "added": TODAY, "published": "2026-01-22"}),
    ("Chichen Itza", {"id": "h2YFnGc8RdA", "title": "Chichen Itza clap echo effect", "cr": "agelessrock", "added": TODAY, "published": "2026-01-15"}),
    ("Chichen Itza", {"id": "DbPSuRt32V4", "title": "Chichen Itza : The Great Ball Court", "cr": "agelessrock", "added": TODAY, "published": "2026-02-08"}),
    ("Chichen Itza", {"id": "4vj6HPtGqi4", "title": "Chichen Itza : Amazing Acoustics @ Temple of The Warriors", "cr": "agelessrock", "added": TODAY, "published": "2026-02-15"}),
    ("Chichen Itza", {"id": "K3G54tBHhtQ", "title": "Chichen Itza : Observatory Tower", "cr": "agelessrock", "added": TODAY, "published": "2026-02-22"}),
    ("Chichen Itza", {"id": "Mm-Vath0XHk", "title": "Chichen Itza : Ossuary Pyramid", "cr": "agelessrock", "added": TODAY, "published": "2026-03-01"}),
    ("Chichen Itza", {"id": "JD8uBRvSDO8", "title": "Chichen Itza : Sacred Cenote", "cr": "agelessrock", "added": TODAY, "published": "2026-03-15"}),
    ("Chichen Itza", {"id": "rTAOCwaDqgA", "title": "Chichen Itza : Lesser Known Structures of an Ancient City", "cr": "agelessrock", "added": TODAY, "published": "2026-03-08"}),

    # === Mexico — Dzibanche (3 months / 2 months ago) ===
    ("Dzibanche", {"id": "TRJ4nBL_LdE", "title": "Dzibanche : Temple of the Owl", "cr": "agelessrock", "added": TODAY, "published": "2026-03-22"}),
    ("Dzibanche", {"id": "WIad3TXcX3A", "title": "Dzibanche : Temple of the Cormorant", "cr": "agelessrock", "added": TODAY, "published": "2026-03-15"}),
    ("Dzibanche", {"id": "BlYHXSV9uxo", "title": "Dzibanche : Temple of the Lintels and others", "cr": "agelessrock", "added": TODAY, "published": "2026-04-01"}),

    # === Mexico — Palenque, Cholula, Calakmul (2 months ago) ===
    ("Palenque", {"id": "ZjSTfRmEqU4", "title": "Ruins of Palenque", "cr": "agelessrock", "added": TODAY, "published": "2026-04-08"}),
    ("Cholula", {"id": "JSUSZEDVHj4", "title": "Cholula Pyramid", "cr": "agelessrock", "added": TODAY, "published": "2026-04-15"}),
    ("Calakmul", {"id": "Z32PamswaU0", "title": "A Millennium of Calakmul", "cr": "agelessrock", "added": TODAY, "published": "2026-04-22"}),

    # === Mexico — Regional overview (1 month ago) — wire to Cholula ===
    ("Cholula", {"id": "V0wTRWFqh-8", "title": "Pyramids of Mesoamerica", "cr": "agelessrock", "added": TODAY, "published": "2026-05-07"}),

    # === Guatemala — Tikal (11 months ago for series) ===
    ("Tikal", {"id": "2ofM2HBkEao", "title": "Tikal : Pyramid I - Temple of Jaguar", "cr": "agelessrock", "added": TODAY, "published": "2025-06-07"}),
    ("Tikal", {"id": "IqgLI8h9Ce8", "title": "Tikal : Pyramid II - Temple of The Masks", "cr": "agelessrock", "added": TODAY, "published": "2025-06-14"}),
    ("Tikal", {"id": "E7USr3aIlmA", "title": "Tikal : Pyramid III - Temple of Jaguar Priest", "cr": "agelessrock", "added": TODAY, "published": "2025-06-21"}),
    ("Tikal", {"id": "s0zzmLAhmwY", "title": "Tikal : Pyramid IV - Temple of Twin Headed Serpent", "cr": "agelessrock", "added": TODAY, "published": "2025-06-28"}),
    ("Tikal", {"id": "apBUt97t8kg", "title": "Tikal : Pyramid V - A Titan Among Giants", "cr": "agelessrock", "added": TODAY, "published": "2025-07-05"}),
    ("Tikal", {"id": "JMk7ojsArNE", "title": "Tikal : Pyramid VI - Temple of Inscriptions", "cr": "agelessrock", "added": TODAY, "published": "2025-07-12"}),
    ("Tikal", {"id": "vo65N-ExKJw", "title": "Tikal : Lost World Pyramid (Mundo Perdido)", "cr": "agelessrock", "added": TODAY, "published": "2025-07-19"}),
    ("Tikal", {"id": "eh9WIsuWuQ8", "title": "Tikal : Chambers of Temples and Palaces", "cr": "agelessrock", "added": TODAY, "published": "2025-07-26"}),

    # === Guatemala — Petén cluster ===
    ("Naranjo", {"id": "7bAPadYWISI", "title": "Naranjo : Land of Pyramids", "cr": "agelessrock", "added": TODAY, "published": "2025-07-30"}),
    ("Yaxha", {"id": "_Lws9iEiE-s", "title": "Yaxha : City of Astronomical Alignments", "cr": "agelessrock", "added": TODAY, "published": "2025-08-06"}),
    ("Nakum", {"id": "SNHgrHRFem8", "title": "Nakum : Large City with Little Information", "cr": "agelessrock", "added": TODAY, "published": "2025-08-13"}),
    ("Uaxactun", {"id": "sJk29ra2qgc", "title": "Uaxactun : Astronomical Ancient Achievement", "cr": "agelessrock", "added": TODAY, "published": "2025-08-20"}),

    # === Guatemala — El Mirador + Zaculeu (3 years ago for older ones) ===
    ("El Mirador", {"id": "6OvZxQshNVE", "title": "Tiger Pyramid + Snake Kings + Orion Constellation = Maya Civilization at El Mirador", "cr": "agelessrock", "added": TODAY, "published": "2023-04-15"}),
    ("El Mirador", {"id": "Aop4aDWydYI", "title": "Is La Danta Pyramid larger than Khufu's Pyramid?", "cr": "agelessrock", "added": TODAY, "published": "2023-04-22"}),
    ("Zaculeu", {"id": "8DwN_N5jxpc", "title": "Zaculeu Pyramids in Guatemala... Tomb? Palace? Temple?", "cr": "agelessrock", "added": TODAY, "published": "2023-05-01"}),

    # === Belize (3 years ago) ===
    ("Xunantunich", {"id": "q3PpYNjS6kg", "title": "White Ghost in Xunantunich Pyramid in Belize", "cr": "agelessrock", "added": TODAY, "published": "2023-03-15"}),
    ("Caracol", {"id": "1xEUxYIh_VQ", "title": "Caracol Pyramids of Belize are more mysterious than you think.", "cr": "agelessrock", "added": TODAY, "published": "2023-03-22"}),
    ("Lamanai", {"id": "nvgxmcA8qnU", "title": "Lamanai Pyramids of Belize - Few Temples but No Palace?", "cr": "agelessrock", "added": TODAY, "published": "2023-03-29"}),

    # === Italy bonus — Alatri (existing, Megalithomania video) ===
    ("Alatri Acropolis", {"id": "a-QbC_vZr88", "title": "Polygonal Walls of the Giants in Ancient Italy | Alatri Megalithic Acropolis | Megalithomania", "cr": "megalithomania", "added": TODAY, "published": "2019-04-15"}),
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
        mex_new = ['Pyramid of the Sun (Teotihuacan)', 'Pyramid of the Moon (Teotihuacan)',
                   'Pyramid of the Feathered Serpent (Teotihuacan)', 'Chichen Itza', 'Coba',
                   'Chacchoben', 'Dzibanche']
        guat_new = ['Uaxactun', 'Yaxha', 'Nakum', 'Naranjo', 'Zaculeu']
        belize_new = ['Caracol', 'Lamanai', 'Xunantunich']
        for c, names in [('Mexico', mex_new), ('Guatemala', guat_new), ('Belize', belize_new)]:
            countries.setdefault(c, [])
            for n in names:
                if n not in countries[c]:
                    countries[c].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (Mexico, Guatemala, Belize)")

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
