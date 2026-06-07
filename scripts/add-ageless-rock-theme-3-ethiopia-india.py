#!/usr/bin/env python3
"""
add-ageless-rock-theme-3-ethiopia-india.py — Theme 3 batch.

  Ethiopia (17 walkthroughs):
    - 9 wired to existing sites: Lalibela (3-part), Wukro Cherkos,
      Abuna Yemata Guh, Maryam Korkor, Mikael Imba, Abreha we Atsbeha
    - 9 new sites: Debra Damo Monastery, Daniel Korkor, Abba Yohani,
      Geneta Mariam, Nazugn Mariam, Adadi Maryam, Washa Mikael,
      Ambager Church Complex, Medhane Alem Adi Kasho

  India (23 walkthroughs):
    - 11 wired to existing sites: Ellora Caves (8 parts), Barabar Caves,
      Ajanta Caves
    - 9 new sites: Kailasa Temple, Padmanabhaswamy Temple, Aurangabad
      Caves, Hoysaleshwara Temple, Chennakeshava Temple, Sahasralinga
      (Shilmala River), Pitalkhora Caves, Naneghat, Dharmrajeshwar Temple

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-3-ethiopia-india.py
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
    # === Ethiopia (9 new) ===
    {"n": "Debra Damo Monastery", "lat": 14.3633, "lng": 39.2944,
     "cat": "rockcut", "region": "Africa", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "6th-century Aksumite-era monastery on a sheer-sided plateau (amba) in northern Tigray. Access is only by a 15-meter leather rope hauled up by monks. The plateau preserves Ethiopia's oldest extant church building, a wood-and-stone basilica with intricately carved wooden panels."},
    {"n": "Daniel Korkor Rock-Cut Church", "lat": 13.9522, "lng": 39.1639,
     "cat": "rockcut", "region": "Africa", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Rock-hewn church carved high into the Gheralta cliffs of Tigray, adjacent to Maryam Korkor. Requires a difficult climb. Believed to have been carved by hand from a single sandstone mass, with crosses, frescoes, and column capitals shaped into the bedrock."},
    {"n": "Abba Yohani Rock-Cut Church", "lat": 13.9667, "lng": 38.8500,
     "cat": "rockcut", "region": "Africa", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Cliff-face rock-hewn church in Tembien district of Tigray. Multiple chambers carved into the sandstone cliff. Frescoes still visible on the interior walls."},
    {"n": "Geneta Mariam Monolithic Church", "lat": 12.0017, "lng": 39.0750,
     "cat": "rockcut", "region": "Africa", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "13th-century monolithic rock-cut church in Lasta, Amhara region, attributed to King Yekuno Amlak. Free-standing church carved from a single block of red volcanic tuff, similar in technique to the churches of Lalibela 25 km away. The church preserves elaborate frescoes."},
    {"n": "Nazugn Mariam Monolithic Church", "lat": 11.9833, "lng": 39.0500,
     "cat": "rockcut", "region": "Africa", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Monolithic rock-hewn church in the Amhara region, related stylistically to the Lalibela complex. Carved from a single mass of volcanic tuff. Continued in use by the Ethiopian Orthodox Church today."},
    {"n": "Adadi Maryam Monolithic Church", "lat": 8.7333, "lng": 38.4500,
     "cat": "rockcut", "region": "Africa", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Rock-hewn church 60 km south of Addis Ababa, the southernmost monolithic church in Ethiopia. Carved from a horizontal rock outcrop into a cruciform plan. Locally attributed to King Lalibela's expansion of the rock-church tradition."},
    {"n": "Washa Mikael Rock-Cut Church", "lat": 9.1167, "lng": 38.7833,
     "cat": "rockcut", "region": "Africa", "tier": 3, "signal": "open",
     "criteria": ["scale"],
     "desc": "Cave church carved into a rock outcrop on Yeka Mountain on the edge of Addis Ababa. Original date and builder uncertain; conventionally attributed to the medieval Ethiopian period but possibly older."},
    {"n": "Ambager Church Complex", "lat": 12.0500, "lng": 39.0500,
     "cat": "rockcut", "region": "Africa", "tier": 3, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Cluster of rock-cut churches in the Amhara region near the Lalibela tradition. Multiple separate church structures carved into a single rock plateau. Less documented than Lalibela but architecturally related."},
    {"n": "Medhane Alem Adi Kasho", "lat": 13.9500, "lng": 39.1500,
     "cat": "rockcut", "region": "Africa", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Rock-hewn church at Adi Kasho in Tigray's Gheralta cluster (distinct from the famous Bete Medhane Alem at Lalibela). Carved into the cliff face with frescoed interiors. Part of the broader northern-Ethiopian rock-church corpus that long predates Lalibela in some scholarship."},

    # === India (9 new) ===
    {"n": "Kailasa Temple (Ellora Cave 16)", "lat": 20.0264, "lng": 75.1796,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry", "hardness"],
     "desc": "The largest monolithic rock-cut structure in the world, carved top-down from a single mass of basalt at Ellora. Approximately 200,000 tons of rock removed to create a full Hindu temple complex with multi-story sanctum, courtyards, pillared halls, and bas-reliefs. Conventionally attributed to King Krishna I of the Rashtrakuta dynasty in the 8th century. Independent reading: the engineering — including the top-down carve sequence, the precision of the proportions, and the absence of construction-era inscriptions describing the work — invites a much older substrate."},
    {"n": "Padmanabhaswamy Temple", "lat": 8.4825, "lng": 76.9433,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Massive Hindu temple in Thiruvananthapuram (Kerala) dedicated to Vishnu in his reclining form. Built of granite and laterite, with a 30 m gopuram (gateway tower). Famous for the immense treasure (estimated to exceed $20 billion) found in its vaults in 2011. Independent investigators draw architectural connections to Angkor Thom in Cambodia."},
    {"n": "Aurangabad Caves", "lat": 19.9000, "lng": 75.3458,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Cluster of 12 Buddhist rock-cut caves on a hillside in Maharashtra, near Aurangabad city. Western and Eastern groups separated by a kilometer. Conventional dating: 6th-8th century CE. Independent reading: tool-mark patterns and chamber geometry invite older construction. Independent investigators note design similarities with Andean rock-cutting."},
    {"n": "Hoysaleshwara Temple", "lat": 13.2127, "lng": 76.0922,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "scale", "geometry"],
     "desc": "12th-century Shiva temple at Halebidu, Karnataka, built by the Hoysala Empire. Constructed of soapstone with thousands of carved figures across exterior walls — possibly the most densely carved temple in India. Twin sanctuaries on a star-shaped platform."},
    {"n": "Chennakeshava Temple (Belur)", "lat": 13.1622, "lng": 75.8597,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "scale", "geometry"],
     "desc": "12th-century Hoysala temple at Belur, Karnataka, dedicated to Vishnu. Took 103 years to complete. Famed for the intricate soapstone carvings: bracket figures, musicians, dancers, and narrative friezes of unprecedented fineness."},
    {"n": "Sahasralinga (Shilmala River)", "lat": 14.8531, "lng": 74.7956,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["precision", "scale", "geometry"],
     "desc": "Site on the Shalmala riverbed in Sirsi, Karnataka, where over a thousand Shiva lingas and yonis are carved directly into the bedrock. The lingas emerge during dry season and become submerged with seasonal river flow. Conventional dating: 17th century Sonda dynasty. Parallels exist at Kbal Spean in Cambodia (Phnom Kulen), already in the atlas."},
    {"n": "Pitalkhora Caves", "lat": 20.5667, "lng": 75.0167,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "14 rock-cut Buddhist caves in Maharashtra, predating the Ajanta Caves. Carved from basalt cliffs around the 2nd-1st century BCE. Notable for the elephant guardian statues and the chaitya hall with stupa."},
    {"n": "Naneghat", "lat": 19.2972, "lng": 73.6694,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Ancient mountain pass cut through the Western Ghats in Maharashtra, used as a trade route by the Satavahanas (~200 BCE). Notable for a giant carved stone jar of disputed function, plus an inscription on the cave wall documenting royal grants."},
    {"n": "Dharmrajeshwar Temple", "lat": 24.3000, "lng": 75.4500,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Top-down rock-cut monolithic temple in Mandsaur district, Madhya Pradesh, carved from a single rock outcrop in a manner directly comparable to Kailasa Temple at Ellora and the Lalibela churches in Ethiopia. Much less famous than either, but the technique connects three continents."},
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === Ethiopia ===
    ("Lalibela", {"id": "ivW_t6bo0es", "title": "Lalibela Churches (Part 1/3) : Is the Church of St. George in Lalibela carved by Ethiopians?", "cr": "agelessrock", "added": TODAY, "published": "2024-08-01"}),
    ("Lalibela", {"id": "nC92mpGoV74", "title": "Lalibela Churches (Part 2/3) : Mysterious Rock-Cut Monolithic Churches of Lalibela - Northern Group", "cr": "agelessrock", "added": TODAY, "published": "2024-08-08"}),
    ("Lalibela", {"id": "YojKBBuJdjE", "title": "Lalibela Churches (Part 3/3) : Largest Monolithic Bedrock Church in the World - Eastern Group", "cr": "agelessrock", "added": TODAY, "published": "2024-08-15"}),
    ("Ambager Church Complex", {"id": "qafmKW7gQDA", "title": "Ambager Church Complex of Amhara, Ethiopia", "cr": "agelessrock", "added": TODAY, "published": "2024-08-22"}),
    ("Washa Mikael Rock-Cut Church", {"id": "IcUfttZ1XR8", "title": "Washa Mikael Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-08-29"}),
    ("Geneta Mariam Monolithic Church", {"id": "eW1L7uDH2Zc", "title": "Monolithic Church of Geneta Mariam", "cr": "agelessrock", "added": TODAY, "published": "2024-09-05"}),
    ("Nazugn Mariam Monolithic Church", {"id": "v-M13a2B0Y8", "title": "Monolithic Church of Nazugn Mariam", "cr": "agelessrock", "added": TODAY, "published": "2024-09-12"}),
    ("Adadi Maryam Monolithic Church", {"id": "qU321I6o61c", "title": "Adadi Maryam Monolithic Church", "cr": "agelessrock", "added": TODAY, "published": "2024-09-19"}),
    ("Debra Damo Monastery", {"id": "sI9wknFPjfk", "title": "Debra Damo Monastery of Ethiopia", "cr": "agelessrock", "added": TODAY, "published": "2024-09-26"}),
    ("Abreha we Atsbeha", {"id": "5ktd7APveuM", "title": "Abreha & Atsbeha Rock Cut Cave Church", "cr": "agelessrock", "added": TODAY, "published": "2024-10-03"}),
    ("Mikael Imba", {"id": "grgL5S2ADkc", "title": "Mikael Imba Rock Cut Cave Church", "cr": "agelessrock", "added": TODAY, "published": "2024-10-10"}),
    ("Medhane Alem Adi Kasho", {"id": "2AddrT9bApM", "title": "Rock Cave Cut Church of Medhane Alem Adi Kasho", "cr": "agelessrock", "added": TODAY, "published": "2024-10-17"}),
    ("Wukro Cherkos", {"id": "J8Fww-MU5qw", "title": "Wukro Cherkos Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-10-24"}),
    ("Abuna Yemata Guh", {"id": "IWhBeOlEEZw", "title": "Abuna Yemata Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-10-31"}),
    ("Maryam Korkor", {"id": "NZFdNMSSR0Y", "title": "Maryam Korkor Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-11-07"}),
    ("Daniel Korkor Rock-Cut Church", {"id": "d12SDZsPWqs", "title": "Daniel Korkor Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-11-14"}),
    ("Abba Yohani Rock-Cut Church", {"id": "r5H5oFQvcYY", "title": "Abba Yohani Rock Cut Church", "cr": "agelessrock", "added": TODAY, "published": "2024-11-21"}),

    # === India ===
    ("Barabar Caves", {"id": "IrnsAWcPLqM", "title": "Who Created Barabar Caves in India?", "cr": "agelessrock", "added": TODAY, "published": "2024-03-01"}),
    ("Hoysaleshwara Temple", {"id": "18lEAXbeGhw", "title": "The Mysteries at Hoysaleshwara Temple", "cr": "agelessrock", "added": TODAY, "published": "2024-03-08"}),
    ("Chennakeshava Temple (Belur)", {"id": "YL3lltYne3U", "title": "The mysteries of Chennakeshava Temple in Belur, India", "cr": "agelessrock", "added": TODAY, "published": "2024-03-15"}),
    ("Sahasralinga (Shilmala River)", {"id": "dTW47WWxxoo", "title": "The Mysterious Shilmala River - Sahasralinga", "cr": "agelessrock", "added": TODAY, "published": "2024-03-22"}),
    ("Kailasa Temple (Ellora Cave 16)", {"id": "dSRNkksXZ1o", "title": "Who Built Kailasa Temple?", "cr": "agelessrock", "added": TODAY, "published": "2024-03-29"}),
    ("Ajanta Caves", {"id": "yTWX9Nnyfy4", "title": "Amazing Ajanta and some Crazy Calculations.", "cr": "agelessrock", "added": TODAY, "published": "2024-04-05"}),
    ("Pitalkhora Caves", {"id": "bZT0zUREisk", "title": "Did Buddhist monks create Pitalkhora Caves site?", "cr": "agelessrock", "added": TODAY, "published": "2024-04-12"}),
    ("Naneghat", {"id": "AV2S-_osfas", "title": "Mysterious giant jar in Naneghat no one is talking about.", "cr": "agelessrock", "added": TODAY, "published": "2024-04-19"}),
    ("Padmanabhaswamy Temple", {"id": "lJBDgRqMpWI", "title": "Padmanabhaswamy Temple (Part 2/2) : The Richest Megalithic Temple", "cr": "agelessrock", "added": TODAY, "published": "2024-04-26"}),
    ("Padmanabhaswamy Temple", {"id": "LFTcDkDnMjQ", "title": "Padmanabhaswamy Temple (Part 1/2) - Is there any connection with Angkor Thom?", "cr": "agelessrock", "added": TODAY, "published": "2024-05-03"}),
    ("Dharmrajeshwar Temple", {"id": "0RKIciQL54s", "title": "Dharmrajeshwar Temple ... a monolithic top-down rock cut bedrock of mystery", "cr": "agelessrock", "added": TODAY, "published": "2024-05-10"}),
    ("Aurangabad Caves", {"id": "z53Z4YQjLbI", "title": "Aurangabad Caves - Western Group (1/2) : Cave Temples so old, no one knows anything for sure", "cr": "agelessrock", "added": TODAY, "published": "2024-05-17"}),
    ("Aurangabad Caves", {"id": "noCNgUwi8BE", "title": "Aurangabad Caves - Western Group (2/2) : Indians and Peruvians had same idea?", "cr": "agelessrock", "added": TODAY, "published": "2024-05-24"}),
    ("Aurangabad Caves", {"id": "HcO2Gsg9-Bc", "title": "Aurangabad Caves - Eastern Group : More Indian caves with Peruvian similarity.", "cr": "agelessrock", "added": TODAY, "published": "2024-05-31"}),
    ("Ellora Caves", {"id": "rZUvCU6aLRs", "title": "Ellora Caves 1 to 10 : Intriguing India", "cr": "agelessrock", "added": TODAY, "published": "2024-06-07"}),
    ("Ellora Caves", {"id": "zyg8sG5W1mI", "title": "Ellora Caves 11 to 15 : Insane India", "cr": "agelessrock", "added": TODAY, "published": "2024-06-14"}),
    ("Ellora Caves", {"id": "AJohwLrSRrc", "title": "Ellora cave 16 (surrounding) : Impossible India", "cr": "agelessrock", "added": TODAY, "published": "2024-06-21"}),
    ("Ellora Caves", {"id": "0XZt9sT600w", "title": "Ellora Caves 17 to 21 : Imposing India", "cr": "agelessrock", "added": TODAY, "published": "2024-06-28"}),
    ("Ellora Caves", {"id": "OTmBxbBdxCs", "title": "Ellora Caves 22 to 24 : Incredible India", "cr": "agelessrock", "added": TODAY, "published": "2024-07-05"}),
    ("Ellora Caves", {"id": "B8sc0JG9Hqw", "title": "Ellora Caves 25 to 28 : Incomprehensible India", "cr": "agelessrock", "added": TODAY, "published": "2024-07-12"}),
    ("Ellora Caves", {"id": "GMiNzaskpP0", "title": "Ellora Cave 29 : Improbable India", "cr": "agelessrock", "added": TODAY, "published": "2024-07-19"}),
    ("Ellora Caves", {"id": "-26jmwmSVls", "title": "Ellora Caves 30 to 31 : Illustrious India", "cr": "agelessrock", "added": TODAY, "published": "2024-07-26"}),
    ("Ellora Caves", {"id": "CVvoxiE3OGg", "title": "Ellora Caves 32 to 34 : Inconceivable India", "cr": "agelessrock", "added": TODAY, "published": "2024-08-02"}),
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
        eth_sites = [s['n'] for s in NEW_SITES if s['region'] == 'Africa']
        ind_sites = [s['n'] for s in NEW_SITES if s['region'] == 'Asia']
        for c, names in [('Ethiopia', eth_sites), ('India', ind_sites)]:
            countries.setdefault(c, [])
            for n in names:
                if n not in countries[c]:
                    countries[c].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (Ethiopia, India)")

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
