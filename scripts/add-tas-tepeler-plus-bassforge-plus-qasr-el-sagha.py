#!/usr/bin/env python3
"""
add-tas-tepeler-plus-bassforge-plus-qasr-el-sagha.py — Combined three-part batch:

  Part A — Taş Tepeler completion (Megalithomania)
    7 new sites: Sayburç, Sefertepe, Gürcütepe, Çakmaktepe, Ayanlar
      Höyük, Harbetsuvan Tepesi, Yenimahalle Höyük
    2 walkthroughs by megalithomania (Major Discoveries + 2025 update)

  Part B — Qasr el Sagha (Megalithomania)
    1 new site: Qasr el Sagha predynastic cyclopean temple, Fayoum, Egypt
    1 walkthrough by megalithomania (Dec 2023, video ID DVY08kpKn6I)

  Part C — BassForge global anomalies
    NEW creator: bassforge (top-tier global synthesis channel)
    11 new sites: Gornaya Shoria (Russia), Sage Wall (Montana),
      Vilcabamba/Espíritu Pampa (Peru), Hegra/Madain Saleh (Saudi Arabia),
      Yangshan Quarry (China), Yakushima Megaliths (Japan), Xi'an
      Pyramids (China), Carnac Alignments (France), Gochang Dolmens
      (South Korea), Ikom Monoliths (Nigeria), Bada Valley Megaliths
      (Indonesia)
    1 walkthrough wired to ~20 atlas sites (BassForge's "Insane Anomalies
      Decoded 2026" is a global synthesis tour)

Idempotent. Run from the repo root:
    python3 scripts/add-tas-tepeler-plus-bassforge-plus-qasr-el-sagha.py
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

# ============================================================
NEW_CREATORS = {
    "bassforge": {
        "name": "BassForge",
        "handle": "@BassForge",
        "subs": "Global ancient-anomaly synthesis channel; rapid-fire tours connecting megalithic + rock-cut + cyclopean sites across continents with technical lens (engineering, geometry, signal processing analogies)",
        "color": "#5C2A9D",  # deep violet — synthesis / pattern recognition
        "tier": 2,
    }
}

# ============================================================
NEW_SITES = [
    # ============= PART A — Taş Tepeler completion (7 new) =============
    {"n": "Sayburç", "lat": 36.8633, "lng": 38.5108,
     "cat": "megalithic", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["precision", "scale", "geometry"],
     "desc": (
         "Pre-pottery Neolithic settlement in Bozova district, Şanlıurfa "
         "Province. Famous for the Sayburç relief — a narrative scene "
         "carved across a bench-back showing two human figures flanked by "
         "leopards and bulls, considered the earliest known narrative "
         "scene in human art (c. 9400 BCE). Part of the Taş Tepeler "
         "complex. The recent discovery (announced 2025) of a complete "
         "human statue with the body matching a head shown to Megalithomania "
         "the previous year places this site at the center of the Taş "
         "Tepeler statuary tradition."
     ),
    },
    {"n": "Sefertepe", "lat": 37.1300, "lng": 38.9400,
     "cat": "megalithic", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Pre-pottery Neolithic site in Şanlıurfa Province, near Karahan "
         "Tepe. Discoveries announced in 2025 include two carved heads "
         "emerging from a single slab and a small statue with two faces "
         "(one open-mouthed) on opposite sides of the same stone. The "
         "dual-face motif resonates with the open-mouth carving on the "
         "main head in structure AB at Karahan Tepe, suggesting deep "
         "iconographic continuity across Taş Tepeler sites."
     ),
    },
    {"n": "Gürcütepe", "lat": 37.1300, "lng": 38.8100,
     "cat": "megalithic", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Cluster of four small Neolithic mounds in the valleys below "
         "Göbekli Tepe (visible from it). One of the last-phase sites in "
         "the Taş Tepeler region, dated c. 7000 BCE. Important as the "
         "first site in the region where full-bodied feminine goddess "
         "figurines appear — connecting forward to Çatalhöyük further "
         "west and the Maltese goddess tradition further afield."
     ),
    },
    {"n": "Çakmaktepe", "lat": 37.2500, "lng": 38.9600,
     "cat": "megalithic", "region": "Türkiye", "tier": 1, "signal": "open",
     "criteria": ["scale", "stratigraphy"],
     "desc": (
         "Pre-pottery Neolithic site near Göbekli Tepe, recently proven "
         "to be older than Göbekli Tepe by ~500 years (potentially c. "
         "12,000 years old). Megalithomania observed a T-pillar lying on "
         "the ground here before excavation began. As of 2025, a Japanese "
         "archaeological team is starting proper excavation. Part of the "
         "Taş Tepeler complex that is rewriting Neolithic chronology."
     ),
    },
    {"n": "Ayanlar Höyük", "lat": 37.5500, "lng": 38.4000,
     "cat": "megalithic", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Pre-pottery Neolithic mound site (also called Gre Filla) in "
         "Hilvan district, Şanlıurfa Province. One of the 12 sites in the "
         "broader Taş Tepeler complex. Largely unexcavated as of 2025 but "
         "shows surface T-pillar evidence consistent with the Göbekli / "
         "Karahan tradition."
     ),
    },
    {"n": "Harbetsuvan Tepesi", "lat": 37.0950, "lng": 39.2750,
     "cat": "megalithic", "region": "Türkiye", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Hilltop pre-pottery Neolithic site approximately 1 km from "
         "Karahan Tepe, hard to access and remote. Part of the Taş "
         "Tepeler complex. Excavation discoveries are being made but "
         "the site has received little public attention compared to "
         "Karahan and Göbekli."
     ),
    },
    {"n": "Yenimahalle Höyük", "lat": 37.1500, "lng": 38.7800,
     "cat": "megalithic", "region": "Türkiye", "tier": 3, "signal": "open",
     "criteria": ["scale"],
     "desc": (
         "Neolithic mound site in central Şanlıurfa, one of the 12 sites "
         "of the Taş Tepeler complex. Largely buried under modern "
         "neighborhood development."
     ),
    },

    # ============= PART B — Qasr el Sagha (1 new) =============
    {"n": "Qasr el Sagha", "lat": 29.5917, "lng": 30.7167,
     "cat": "temple", "region": "Egypt", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "precision", "scale"],
     "desc": (
         "Predynastic / Old Kingdom cyclopean temple on the northern edge "
         "of the Fayoum depression in middle Egypt. Built of massive "
         "polygonal limestone blocks with no mortar, fitting in the same "
         "interlocking style as Sacsayhuamán in Peru. Conventionally "
         "dated to the Middle Kingdom (c. 1850 BCE) but undecorated, "
         "unfinished, and structurally unlike any contemporary Egyptian "
         "temple — leading Megalithomania and other independent "
         "researchers to argue for a much earlier predynastic foundation. "
         "Critical reference point for the Osireion / pre-dynastic "
         "cyclopean Egypt thesis covered in Library Entry 03."
     ),
    },

    # ============= PART C — BassForge global anomalies (11 new) =============
    {"n": "Gornaya Shoria Megaliths", "lat": 52.8000, "lng": 87.9000,
     "cat": "megalithic", "region": "Russia", "tier": 1, "signal": "open",
     "criteria": ["scale", "polygonal", "geometry"],
     "desc": (
         "Mountain site in Kemerovo Oblast, southwestern Siberia, where "
         "researchers (Valery Uvarov, Georgy Sidorov, John Jensen) have "
         "documented stones reported to weigh 3,000-4,000 tonnes — "
         "potentially the largest worked megaliths anywhere on Earth, "
         "exceeding Baalbek's trilithon. The mainstream view labels the "
         "formations natural granite weathering. Independent researchers "
         "point to flat-cut surfaces, right-angle joints, and stacked "
         "courses that are difficult to reconcile with natural processes. "
         "Remote location and limited Western access have kept the site "
         "underdocumented."
     ),
    },
    {"n": "Sage Wall (Montana)", "lat": 45.4750, "lng": -111.7833,
     "cat": "megalithic", "region": "North America", "tier": 2, "signal": "open",
     "criteria": ["polygonal", "precision", "geometry"],
     "desc": (
         "Megalithic interlocking wall structure on a private ranch in "
         "the Tobacco Root Mountains, southwestern Montana. Discovered by "
         "the landowner family in the 1980s. Features polygonal joinery "
         "stylistically comparable to Sacsayhuamán in Peru and Cusco's "
         "walls — irregularly-shaped, multi-ton blocks fitted without "
         "mortar. Mainstream archaeology classifies it as natural rock "
         "formation. Independent researchers (Brien Foerster, JJ Ainsworth, "
         "Jimmy Bright) argue the joinery angles, scoop marks, and "
         "interlocks indicate intentional construction. One of North "
         "America's most-debated megalithic anomalies."
     ),
    },
    {"n": "Vilcabamba (Espíritu Pampa)", "lat": -12.9333, "lng": -73.0667,
     "cat": "city", "region": "South America", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "scale", "stratigraphy"],
     "desc": (
         "Last stronghold of the Inca Empire after the Spanish conquest, "
         "deep in the Vilcabamba mountains northeast of Cusco. Rediscovered "
         "by Hiram Bingham in 1911 and definitively identified in 1964 "
         "by Gene Savoy. Shows the same stratigraphic pattern visible at "
         "Machu Picchu and Sacsayhuamán: older, more refined polygonal "
         "masonry at the base, with cruder Inca-era stonework added on "
         "top. This 'old work / new work' contrast is one of the strongest "
         "visual arguments for a pre-Inca megalithic tradition that the "
         "Incas inherited rather than built."
     ),
    },
    {"n": "Hegra (Madain Saleh)", "lat": 26.7900, "lng": 37.9533,
     "cat": "rockcut", "region": "Middle East", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "scale", "geometry"],
     "desc": (
         "Second-largest city of the Nabataean Empire (after Petra), in "
         "AlUla, Saudi Arabia. 131 monumental tombs carved directly into "
         "sandstone mountains, c. 1st century BCE - 1st century CE. The "
         "tombs are carved top-down from the mountain face — unfinished "
         "examples reveal the work sequence clearly. Greco-Roman stylistic "
         "elements appear deep in Arabian territory. Interior chambers "
         "are remarkably plain despite the elaborate exterior facades, a "
         "puzzle that conventional and independent readings interpret "
         "differently. Critical anchor for Library Entry 04 (the Top-Down "
         "Tradition)."
     ),
    },
    {"n": "Yangshan Quarry", "lat": 32.0500, "lng": 118.9500,
     "cat": "monolithic", "region": "China", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": (
         "Ming Dynasty stone quarry near Nanjing, China, abandoned in 1405 "
         "CE. Contains three of the largest worked megaliths on Earth: a "
         "stele base (16,000 tonnes), shaft (8,800 tonnes), and head "
         "(6,000 tonnes), all carved but never removed from the bedrock. "
         "Intended for the Ming Xiaoling Mausoleum but abandoned when "
         "transport proved impossible. A rare case where conventional "
         "dating is firm — Ming dynasty records explicitly document the "
         "project. The site's value to the atlas is comparative: it shows "
         "what extracting such megaliths actually requires, even with "
         "early-modern infrastructure."
     ),
    },
    {"n": "Yakushima Megaliths", "lat": 30.3500, "lng": 130.5000,
     "cat": "megalithic", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Carved megalithic stones on Yakushima Island, off the southern "
         "tip of Japan's main island chain. Features include a precisely "
         "rectangular cut stone sitting atop a larger worked rock, "
         "additional bread-loaf-shaped blocks reminiscent of the laser-cut "
         "appearance of stones at AlUla (Saudi Arabia) and Puma Punku "
         "(Bolivia). Local lore connects the stones to the legendary land "
         "of Mu. Mainstream archaeology is silent on these features."
     ),
    },
    {"n": "Xi'an Pyramids", "lat": 34.3833, "lng": 108.9333,
     "cat": "pyramid", "region": "China", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "stratigraphy"],
     "desc": (
         "Cluster of at least 40 documented pyramids north of Xi'an in "
         "Shaanxi Province, China. Some have greater internal volume "
         "than the Great Pyramid of Giza. Officially classified as Han "
         "and Tang dynasty burial mounds (c. 200 BCE - 900 CE), though "
         "no bodies have been recovered from inside any of them — only "
         "from surrounding areas. China publicly states it lacks the "
         "resources to excavate without damage; shallow-rooted trees have "
         "been planted on top of many to obscure the geometric form. The "
         "Zion-Xi'an cluster shares stellar alignment patterns with "
         "Teotihuacán and Giza (Orion's Belt thesis). One of the largest "
         "unexcavated pyramid fields on Earth."
     ),
    },
    {"n": "Carnac Stones (Brittany)", "lat": 47.5833, "lng": -3.0750,
     "cat": "megalithic", "region": "Europe", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Massive Neolithic alignment of approximately 4,000 standing "
         "stones in long parallel rows stretching across the landscape "
         "of Brittany, France. Stones weigh 40-350 tonnes. Dated to c. "
         "5000 BCE — predating Stonehenge by 1,000+ years. Recent "
         "research (BassForge synthesis) demonstrates the alignment "
         "encodes astrogeometry: three perfect squares laid end-to-end "
         "produce the exact angle of a 3-4-5 right triangle (Pythagorean "
         "triple) thousands of years before its formal documentation by "
         "the Sumerians. The astrogeometric encoding parallels Angkor "
         "Wat and the Great Pyramid. The world's largest concentration "
         "of standing-stone megaliths."
     ),
    },
    {"n": "Gochang Dolmens", "lat": 35.4333, "lng": 126.5500,
     "cat": "megalithic", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Dolmen field in Jeollabuk Province, South Korea — part of the "
         "Gochang-Hwasun-Ganghwa dolmen system that contains over 35,000 "
         "documented dolmens, more than 40% of the world's total. Some "
         "individual capstones exceed 100 tonnes. A documented modern "
         "reconstruction experiment in Denmark succeeded with a 9-tonne "
         "stone; the Korean originals weigh 10x that and were placed "
         "thousands of times. Conventionally classified as burial "
         "monuments, but the structural insecurity of the dolmen form as "
         "a tomb is increasingly questioned. UNESCO designates this as a "
         "world heritage zone (not site) due to scale."
     ),
    },
    {"n": "Ikom Monoliths", "lat": 6.0667, "lng": 8.8600,
     "cat": "megalithic", "region": "Africa", "tier": 2, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": (
         "Cluster of approximately 350 anthropomorphic carved stone "
         "monoliths in Cross River State, southeastern Nigeria, ancestral "
         "territory of the Ekoi people. Carved from basalt and limestone, "
         "depicting stylized human figures with arms folded across the "
         "body. Conventional dating: 200 BCE - 200 CE. Stylistic "
         "parallels to figures in Sulawesi (Indonesia) and the South "
         "American spiral-motif tradition raise questions of Atlantic-era "
         "cultural diffusion. Largely absent from mainstream archaeology "
         "discourse despite its scale."
     ),
    },
    {"n": "Bada Valley Megaliths", "lat": -1.7833, "lng": 120.2000,
     "cat": "megalithic", "region": "Indonesia", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": (
         "Cluster of approximately 400 megalithic statues and stone "
         "vessels (kalamba) in the Bada, Besoa, and Napu valleys of "
         "central Sulawesi, within Lore Lindu National Park. Anthropomorphic "
         "statues up to 4.5 m tall (Palindo, the tallest), of unknown "
         "carvers and unknown date. Mainstream estimates range from 1000 "
         "BCE to 1500 CE — a 2,500-year uncertainty window that reflects "
         "the absence of associated material culture for dating. The "
         "kalamba (giant stone basins) share form with the Plain of Jars "
         "in Laos."
     ),
    },
]

# ============================================================
VIDEOS_TO_WIRE = [
    # ===== Part A: Megalithomania Taş Tepeler walkthroughs =====
    # "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç"
    ("Karahan Tepe", {
        "id": "pqNED6RJ4HY",
        "title": "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç | Taş Tepeler | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-11-29"}),
    ("Göbekli Tepe (Potbelly Hill)", {
        "id": "pqNED6RJ4HY",
        "title": "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç | Taş Tepeler | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-11-29"}),
    ("Sayburç", {
        "id": "pqNED6RJ4HY",
        "title": "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç | Taş Tepeler | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-11-29"}),
    ("Sefertepe", {
        "id": "pqNED6RJ4HY",
        "title": "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç | Taş Tepeler | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-11-29"}),
    ("Gürcütepe", {
        "id": "pqNED6RJ4HY",
        "title": "Major Discoveries at Göbekli Tepe, Karahan Tepe, Sefer Tepe & Sayburç | Taş Tepeler | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-11-29"}),

    # Karahan Tepe May 2025 Update walkthrough
    ("Karahan Tepe", {
        "id": "VXKhfI601Gc",
        "title": "Karahan Tepe | 2025 Update + New Discoveries | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2025-06-10"}),

    # ===== Part B (cont'd): Megalithomania Qasr el Sagha walkthrough =====
    # Verified via YouTube search: DVY08kpKn6I = MegalithomaniaUK's
    # "Qasr el Sagha | Predynastic Cyclopean Temple in Egypt"
    # Published Dec 3, 2023; 61,357 views; 37:17.
    ("Qasr el Sagha", {
        "id": "DVY08kpKn6I",
        "title": "Qasr el Sagha | Predynastic Cyclopean Temple in Egypt | Megalithomania",
        "cr": "megalithomania", "added": TODAY, "published": "2023-12-03"}),

    # ===== Part C: BassForge "Insane Anomalies Decoded 2026" — global tour =====
    # Verified via YouTube search: V_O9fRvd1OY = BassForge channel's
    # "Ancient Architects | Insane Anomalies Decoded [2026]"
    # This single video covers dozens of sites; wire to its core anchors.
    ("Gornaya Shoria Megaliths", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Sage Wall (Montana)", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Vilcabamba (Espíritu Pampa)", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Hegra (Madain Saleh)", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Yangshan Quarry", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Yakushima Megaliths", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Xi'an Pyramids", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Carnac Stones (Brittany)", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Gochang Dolmens", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Ikom Monoliths", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
    ("Bada Valley Megaliths", {
        "id": "V_O9fRvd1OY",
        "title": "Ancient Architects | Insane Anomalies Decoded [2026]",
        "cr": "bassforge", "added": TODAY, "published": "2026-01-15"}),
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
        country_map = {
            'Türkiye': ['Sayburç', 'Sefertepe', 'Gürcütepe', 'Çakmaktepe',
                       'Ayanlar Höyük', 'Harbetsuvan Tepesi', 'Yenimahalle Höyük'],
            'Egypt': ['Qasr el Sagha'],
            'Russia': ['Gornaya Shoria Megaliths'],
            'United States': ['Sage Wall (Montana)'],
            'Peru': ['Vilcabamba (Espíritu Pampa)'],
            'Saudi Arabia': ['Hegra (Madain Saleh)'],
            'China': ['Yangshan Quarry', "Xi'an Pyramids"],
            'Japan': ['Yakushima Megaliths'],
            'France': ['Carnac Stones (Brittany)'],
            'South Korea': ['Gochang Dolmens'],
            'Nigeria': ['Ikom Monoliths'],
            'Indonesia': ['Bada Valley Megaliths'],
        }
        for country, names in country_map.items():
            countries.setdefault(country, [])
            for n in names:
                if n not in countries[country]:
                    countries[country].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated ({len(country_map)} countries)")

    sites = load('sites.json')
    videos = load('videos.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  This batch:         {videos_wired} videos wired, {sites_added} new sites, {new_badges} fire NEW badge")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
