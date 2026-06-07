#!/usr/bin/env python3
"""
add-ageless-rock-theme-2-cambodia-indonesia.py — Theme 2 batch.

  Cambodia (35 walkthroughs from Ageless Rock):
    - Wire to existing sites: Angkor Wat, Angkor Thom, Beng Mealea (2),
      Banteay Srei, Preah Khan of Kompong Svay (5), Sambor Prei Kuk wired
      elsewhere, Koh Ker wired elsewhere, Ta Prohm wired elsewhere
    - 17 new sites: Bayon, Banteay Chhmar, Banteay Kdei, Banteay Prei,
      Banteay Toap, Banteay Prei Nokor, Preah Khan (of Angkor),
      Phnom Chisor, Srah Srang, Neak Poan + Jayatataka Baray,
      West Baray, East Baray, West Mebon, East Mebon, Bat Chum,
      Veal Phtei, Kravan, Chaw Srei Vibol, Neam Rup

  Indonesia (37 walkthroughs from Ageless Rock):
    - Wire to existing: Borobudur (4), Prambanan (1), Bada Valley Megaliths (2)
    - 21 new sites: Ratu Boko, Sambisari, Sewu, Plaosan, Kalasan, Mendut,
      Pawon, Ijo, Sojiwan, Banyunibo, Barong, Bubrah, Lumbung, Sari,
      Kedulan, Tampaksiring (Gunung Kawi), Pura Besakih, Lempuyang Luhur,
      Sumba, Sumbawa, Toraja, Nias

  Bonus: Maliabad Fort, India (Megalithomania, MegalithomaniaUK)
    - 1 new site, 1 walkthrough
    - Megalithomania (Hugh Newman) channel already exists in atlas

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-2-cambodia-indonesia.py
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

# Verify creators exist
creators = load('creators.json')
for cr in ['agelessrock', 'megalithomania']:
    if cr not in creators:
        sys.exit(f"Creator {cr!r} not found")

# ============================================================
NEW_SITES = [
    # === Cambodia (18 new sites) ===
    {"n": "Bayon Temple", "lat": 13.4413, "lng": 103.8593,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Buddhist temple at the center of Angkor Thom, built by Jayavarman VII in the late 12th/early 13th century. Famous for the 216 serene stone faces carved into 54 towers. Bas-reliefs depict everyday Khmer life with extraordinary detail."},
    {"n": "Preah Khan (Angkor)", "lat": 13.4621, "lng": 103.8731,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Major late-12th-century Buddhist temple complex at Angkor, built by Jayavarman VII as a monastery and university. Name means 'Sacred Sword.' The outer enclosure walls form a near-square 800m × 700m. Distinct from Preah Khan of Kompong Svay (a separate remote site)."},
    {"n": "Srah Srang", "lat": 13.4337, "lng": 103.9006,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale"],
     "desc": "Royal bathing pool 700m × 350m at Angkor, dating to mid-10th century with later modifications under Jayavarman VII. Sandstone landing stage with naga balustrades on the western side. Functioned alongside the adjacent Banteay Kdei temple."},
    {"n": "Banteay Kdei", "lat": 13.4360, "lng": 103.8995,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "Buddhist temple at Angkor built in the late 12th to early 13th century under Jayavarman VII. Adjacent to Srah Srang. Multiple concentric enclosures with sandstone galleries and face-towers similar to Ta Prohm and Bayon."},
    {"n": "West Baray", "lat": 13.4326, "lng": 103.8042,
     "cat": "underground", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Massive Angkor-era reservoir, approximately 8 km × 2.1 km, the largest hydraulic structure of the ancient world. Built in the 11th century under Suryavarman I. Still partially water-filled. Contains the West Mebon temple on a central island."},
    {"n": "West Mebon", "lat": 13.4317, "lng": 103.7958,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Hindu temple on an artificial island at the center of the West Baray. Mid-11th century under Udayadityavarman II. Famous bronze reclining Vishnu statue recovered from the central well in 1936."},
    {"n": "East Baray", "lat": 13.4502, "lng": 103.9170,
     "cat": "underground", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Now-dry Angkor-era reservoir approximately 7.5 km × 1.8 km, constructed in the late 9th century by Yasovarman I. The East Mebon temple sits on the former central island."},
    {"n": "East Mebon", "lat": 13.4499, "lng": 103.9098,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "10th-century Hindu temple dedicated to Shiva, built by Rajendravarman II in 952 CE on what was then an island in the East Baray. Three-tier sandstone and laterite pyramid with elephant statues at each corner."},
    {"n": "Neak Poan (Jayatataka Baray)", "lat": 13.4669, "lng": 103.8930,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["geometry", "scale"],
     "desc": "Buddhist temple on an artificial island in the center of the Jayatataka Baray at Angkor, built by Jayavarman VII in the late 12th century. Designed to mimic the sacred Anavatapta lake of Buddhist cosmology, with four connected pools radiating from a central circular pond."},
    {"n": "Bat Chum", "lat": 13.4233, "lng": 103.8869,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Small mid-10th-century Buddhist temple at Angkor with three brick shrines on a common platform. Built by a Brahmin during the reign of Rajendravarman II. Adjacent to a small baray."},
    {"n": "Banteay Srei", "lat": 13.5988, "lng": 103.9622,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "geometry"],
     "desc": "10th-century Hindu temple ('Citadel of Women') 25 km north-east of Angkor, dedicated to Shiva. Built in red sandstone with exquisite high-relief carvings unmatched in Angkor for fineness. Consecrated 967 CE."},
    {"n": "Veal Phtei", "lat": 13.4500, "lng": 103.9100,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale"],
     "desc": "Small Angkor-era temple of which little official scholarship remains. Modest sandstone structure in the broader Angkor archaeological area. Function and exact dating remain open questions."},
    {"n": "Kravan", "lat": 13.4318, "lng": 103.8868,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Prasat Kravan: five-shrine brick temple at Angkor, completed 921 CE. Notable for the bas-relief brick carvings of Vishnu and Lakshmi inside the central shrine, rare in Khmer brick-temple tradition."},
    {"n": "Chaw Srei Vibol", "lat": 13.4683, "lng": 104.0017,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["geometry", "scale"],
     "desc": "Hilltop temple complex 30 km east of Angkor on the Wat Trak hill, with three terraced enclosures climbing the slope. The site sits on what some investigators describe as a notable ley-line alignment. Little formal documentation."},
    {"n": "Banteay Prei (Angkor)", "lat": 13.4774, "lng": 103.8784,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Small Bayon-style temple at Angkor, late 12th century. Distinct from Banteay Prei Nokor in eastern Cambodia. Heavily forested and minimally restored."},
    {"n": "Neam Rup (Pleasant Temple)", "lat": 13.4400, "lng": 103.9050,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["geometry"],
     "desc": "Tiny temple at Angkor whose astronomical alignments and proportions seem to require disproportionate effort relative to its modest size. Function and dating remain open."},
    {"n": "Phnom Chisor", "lat": 11.0833, "lng": 104.9333,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "11th-century hilltop Hindu temple in Takeo Province, southern Cambodia, dedicated to Shiva. Built by Suryavarman I. Unique east-facing layout with an elaborate processional staircase. 503 steps lead to the summit."},
    {"n": "Banteay Chhmar", "lat": 14.0667, "lng": 102.9833,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Massive late-12th-century Buddhist temple complex in remote north-west Cambodia, built by Jayavarman VII. One of the largest temples of the Khmer empire, with an enclosure measuring 1.9 km × 1.7 km. Famous for face-towers and the bas-relief of Avalokiteshvara with multiple arms."},
    {"n": "Banteay Toap", "lat": 13.6167, "lng": 102.9000,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale"],
     "desc": "Khmer-era fortified temple in north-west Cambodia, traditionally associated with Banteay Chhmar's military function. Multiple enclosure walls."},
    {"n": "Banteay Prei Nokor", "lat": 11.4167, "lng": 105.8667,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Black-sandstone temple complex in Tboung Khmum Province, eastern Cambodia. Date and origin uncertain — possibly 8th-9th century, pre-Angkor era. The black sandstone is distinctive."},

    # === Indonesia (21 new sites) ===
    {"n": "Ratu Boko", "lat": -7.7700, "lng": 110.4900,
     "cat": "city", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Hilltop archaeological complex south of Prambanan in Central Java, dating to roughly the 8th century. The site mixes Buddhist and Hindu features in a layout that doesn't match standard temple or palace conventions. Stone gates, terraces, pools, and a meditation cave. The function is debated: royal residence, monastery, or ceremonial complex."},
    {"n": "Sambisari", "lat": -7.7656, "lng": 110.4458,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["geometry"],
     "desc": "9th-century Hindu temple in Yogyakarta sitting 6.5 metres below the surrounding ground level. Discovered 1966 by a farmer plowing his field. The 6.5m of stratigraphy over the temple is consistent with volcanic ash burial from Mount Merapi but raises questions about exactly when."},
    {"n": "Sewu Temple", "lat": -7.7400, "lng": 110.4933,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "geometry"],
     "desc": "8th-century Mahayana Buddhist temple complex in Central Java, the second-largest in Indonesia after Borobudur. 249 temples arranged in a mandala. Built by the Shailendra dynasty."},
    {"n": "Plaosan", "lat": -7.7400, "lng": 110.5033,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Twin Mahayana Buddhist temples near Prambanan, 9th century, possibly commissioned by King Rakai Pikatan and Queen Pramodawardhani as symbols of religious harmony between their families' Hindu and Buddhist traditions."},
    {"n": "Kalasan", "lat": -7.7669, "lng": 110.4719,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "9th-century Buddhist temple in Central Java dedicated to the goddess Tara, the oldest Buddhist temple on the Prambanan plain. Notable for the precision of its proportions and the use of vajralepa stucco coating."},
    {"n": "Mendut", "lat": -7.6053, "lng": 110.2300,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["geometry", "precision"],
     "desc": "Late-8th- to early-9th-century Buddhist temple near Borobudur. Houses a large stone Buddha statue flanked by Avalokitesvara and Vajrapani. Aligned axially with Pawon and Borobudur on what some investigators interpret as a ley line."},
    {"n": "Pawon", "lat": -7.6064, "lng": 110.2233,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Small Buddhist temple between Borobudur and Mendut, completing the three-temple axial alignment. Function debated: relic shrine, tomb, or ritual stop on a pilgrimage route."},
    {"n": "Ijo", "lat": -7.7903, "lng": 110.5097,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "9th-century Hindu temple at the highest elevation in the Prambanan plain region. Terraced layout with main shrine at the top of three platforms."},
    {"n": "Sojiwan", "lat": -7.7558, "lng": 110.4925,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "9th-century Buddhist temple near Prambanan, recently restored. Notable for the carved animal-fable reliefs around its base."},
    {"n": "Banyunibo", "lat": -7.7619, "lng": 110.5028,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "9th-century Buddhist temple with distinctive single-chamber design and elaborate antefix decoration. The name means 'falling water.'"},
    {"n": "Barong", "lat": -7.7833, "lng": 110.5000,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["geometry"],
     "desc": "Hilltop temple south of Prambanan. Three shrines originally, only two remain — the third is presumed to have been destroyed or removed. Distinctive layout."},
    {"n": "Bubrah", "lat": -7.7411, "lng": 110.4933,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "Small Buddhist temple in the Prambanan plain, possibly serving as a satellite to Sewu. Recently restored from a heavily-ruined state."},
    {"n": "Lumbung", "lat": -7.7414, "lng": 110.4925,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["geometry"],
     "desc": "Buddhist temple named 'rice barn' due to local interpretation. No surviving inscriptions or texts describing its original function. Cluster of small shrines around a central temple."},
    {"n": "Sari", "lat": -7.7669, "lng": 110.4783,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["geometry"],
     "desc": "9th-century Buddhist monastery near Kalasan. Two-story structure with monastic cells on the upper level. Believed to have housed monks attending services at Kalasan."},
    {"n": "Kedulan", "lat": -7.7458, "lng": 110.4753,
     "cat": "temple", "region": "Asia", "tier": 3, "signal": "open",
     "criteria": ["geometry"],
     "desc": "Hindu temple in Yogyakarta found buried under approximately 7m of volcanic ash. Discovered in 1993 during sand mining. Excavation ongoing. Trinity of shrines for Trimurti deities."},
    {"n": "Tampaksiring (Gunung Kawi)", "lat": -8.4283, "lng": 115.3128,
     "cat": "megalithic", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "11th-century rock-cut temple complex in Bali, with 10 large candi (shrine niches) carved directly into the cliffs of the Pakerisan river valley. Associated with the burial of King Anak Wungsu and his consorts. Massive monolithic excavation."},
    {"n": "Pura Besakih", "lat": -8.3739, "lng": 115.4514,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "The 'Mother Temple' of Bali, on the slopes of Mount Agung. Largest Hindu temple complex in Bali, with 23 separate temples in a unified architectural layout. Origins debated — possibly pre-Hindu Megalithic substrate."},
    {"n": "Pura Lempuyang Luhur", "lat": -8.3958, "lng": 115.6322,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Sacred Hindu temple in eastern Bali, one of the six holiest in Bali. Sits on Mount Lempuyang. Famous for the 'Gates of Heaven' (Gateway to Heaven) framing Mount Agung in the distance."},
    {"n": "Sumba Megalithic Tombs", "lat": -9.6667, "lng": 119.4000,
     "cat": "megalithic", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale"],
     "desc": "Living megalithic tradition on Sumba island in eastern Indonesia. Massive stone slab tombs (some weighing 70 tons) are still constructed today using traditional methods. The continuity of the practice from at least the late Neolithic into the 21st century is anthropologically unique."},
    {"n": "Sumbawa Megaliths", "lat": -8.7500, "lng": 117.7500,
     "cat": "megalithic", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Multiple megalithic sites on Sumbawa island including Ai Renung (the 'Phantom Five' carved sarcophagi-like blocks) and Raboran. Form, function, and dating largely unestablished by formal archaeology."},
    {"n": "Toraja Rock-Cut Burials", "lat": -3.0167, "lng": 119.8167,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale"],
     "desc": "Living rock-cut burial tradition in the Toraja highlands of South Sulawesi. Cliff-face tombs with wooden tau-tau effigies of the deceased standing in carved balconies. Practice continues today."},
    {"n": "Nias Island Megaliths", "lat": 1.0833, "lng": 97.7333,
     "cat": "megalithic", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Monolithic stone tables, seats, and tall standing stones in traditional Nias villages in western Sumatra. Some pieces weigh over a ton. Pre-modern villagers transported and erected them using ritualized communal effort recorded in oral tradition."},

    # === India (1 new site) ===
    {"n": "Maliabad Fort", "lat": 16.2167, "lng": 77.3667,
     "cat": "megalithic", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["polygonal", "scale", "geometry"],
     "desc": "Massive fortified complex in the Karnataka region of central India near Raichur, with cyclopean polygonal walls that stretch approximately 5 km / 3.5 miles. The walls show bent corners, multi-sided polygonal blocks (including a 12-sided stone similar to the one in Cusco), nubs identical to those at Sacsayhuamán, and granite stonework directly compared by Hugh Newman to Egypt's Valley Temple, Puma Punku in Bolivia, and the megalithic Andean tradition. Includes a Shiva Temple with two life-size white granite elephants and a Shiva Lingam. Conventional dating: 13th century CE. Independent reading: the polygonal cyclopean phase is much older, with the medieval fort built atop a much earlier megalithic substrate."},
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === Cambodia ===
    ("Angkor Wat", {"id": "t5yrTx7udT4", "title": "Angkor Archaeological Park is insanely huge. So how can the history vanish?", "cr": "agelessrock", "added": TODAY, "published": "2023-01-15"}),
    ("Angkor Wat", {"id": "Rda15KOGr6o", "title": "7 Reasons Angkor Wat Cannot Be Built by Human", "cr": "agelessrock", "added": TODAY, "published": "2023-01-22"}),
    ("Bayon Temple", {"id": "SIJm3OYQP-g", "title": "Who built the mysterious Bayon Temple in Angkor Thom?", "cr": "agelessrock", "added": TODAY, "published": "2023-01-29"}),
    ("West Baray", {"id": "k_6sk8u6R3E", "title": "West Baray of an Angkorian City", "cr": "agelessrock", "added": TODAY, "published": "2023-02-05"}),
    ("West Mebon", {"id": "lLvDAm02Gxg", "title": "West Mebon is a temple in a moat", "cr": "agelessrock", "added": TODAY, "published": "2023-02-12"}),
    ("East Baray", {"id": "hrAFQ2tPujs", "title": "East Baray and Mebon is a temple in a moat", "cr": "agelessrock", "added": TODAY, "published": "2023-02-19"}),
    ("Neak Poan (Jayatataka Baray)", {"id": "x5NHxYAFyvM", "title": "Jayatataka Baray & Neak Poan Temple in the Mebon", "cr": "agelessrock", "added": TODAY, "published": "2023-02-26"}),
    ("Neak Poan (Jayatataka Baray)", {"id": "-_2Q5f6CrbU", "title": "Neak Poan Temple & Jayatataka Baray : Anavatapta Lake Connection", "cr": "agelessrock", "added": TODAY, "published": "2023-03-05"}),
    ("Neak Poan (Jayatataka Baray)", {"id": "5wi-4YE3hj0", "title": "Jayatataka Baray + Neak Poan Temple = Healthy", "cr": "agelessrock", "added": TODAY, "published": "2023-03-12"}),
    ("Preah Khan (Angkor)", {"id": "57r9TKVHAbw", "title": "Preah Khan Temple (1/3) : Yin & Yang of Outer Structure", "cr": "agelessrock", "added": TODAY, "published": "2023-03-19"}),
    ("Preah Khan (Angkor)", {"id": "mScLJsNZWck", "title": "Preah Khan Temple (2/3) : Preah Khan Reach = The Sacred Sword", "cr": "agelessrock", "added": TODAY, "published": "2023-03-26"}),
    ("Preah Khan (Angkor)", {"id": "PFKtlgzqrx0", "title": "Preah Khan Temple (3/3) : A Lost Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-04-02"}),
    ("Srah Srang", {"id": "LF1VmkbCYTs", "title": "Srah Srang - Lost Underwater Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-04-09"}),
    ("Banteay Kdei", {"id": "LWRbFWJPRJo", "title": "Banteay Kdei Temple : A Piquant Prasat linked to Srah Srang", "cr": "agelessrock", "added": TODAY, "published": "2023-04-16"}),
    ("Preah Khan of Kompong Svay", {"id": "eJkYv4H6D50", "title": "Preah Khan Temple of Kampong Svay (1/5) : The Moat", "cr": "agelessrock", "added": TODAY, "published": "2023-04-23"}),
    ("Preah Khan of Kompong Svay", {"id": "vcLjTumN2Bc", "title": "Preah Khan Temple of Kampong Svay (2/5) : The Baray", "cr": "agelessrock", "added": TODAY, "published": "2023-04-30"}),
    ("Preah Khan of Kompong Svay", {"id": "9VFs7ERqmVQ", "title": "Preah Khan Temple of Kampong Svay (3/5) : The Temples Inside", "cr": "agelessrock", "added": TODAY, "published": "2023-05-07"}),
    ("Preah Khan of Kompong Svay", {"id": "Ae9bCWgrGxk", "title": "Preah Khan Temple of Kampong Svay (4/5) : The Water Tanks Inside", "cr": "agelessrock", "added": TODAY, "published": "2023-05-14"}),
    ("Preah Khan of Kompong Svay", {"id": "BDsXbbQO2S4", "title": "Preah Khan Temple of Kampong Svay (5/5) : Sacred Temple of the Far East", "cr": "agelessrock", "added": TODAY, "published": "2023-05-21"}),
    ("Banteay Chhmar", {"id": "Qy2hWsf_dnA", "title": "Banteay Chhmar (1/3) : Layout of an Advance Civilization", "cr": "agelessrock", "added": TODAY, "published": "2023-05-28"}),
    ("Banteay Chhmar", {"id": "YiEgi42zUt4", "title": "Banteay Chhmar (2/3) : Baray with a Snaky Mebon", "cr": "agelessrock", "added": TODAY, "published": "2023-06-04"}),
    ("Banteay Chhmar", {"id": "FQNxobvdgKY", "title": "Banteay Chhmar (3/3) : Fortress of Cats with Satellite Temples", "cr": "agelessrock", "added": TODAY, "published": "2023-06-11"}),
    ("Banteay Toap", {"id": "Q956NTYeLMg", "title": "Banteay Toap : Mysterious Fortress of the Army", "cr": "agelessrock", "added": TODAY, "published": "2023-06-18"}),
    ("Banteay Prei Nokor", {"id": "8XsaxhoeOo8", "title": "Banteay Prei Nokor Temple : The Black Sandstone Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-06-25"}),
    ("Chaw Srei Vibol", {"id": "P3zld0Ms99g", "title": "Chaw Srei Vibol Temple (1/2) : A Temple with Intelligent Design", "cr": "agelessrock", "added": TODAY, "published": "2023-07-02"}),
    ("Chaw Srei Vibol", {"id": "j2d5REgnT8E", "title": "Chaw Srei Vibol Temple (2/2) : The Mysterious Ley Line", "cr": "agelessrock", "added": TODAY, "published": "2023-07-09"}),
    ("Banteay Prei (Angkor)", {"id": "Mmr4jWW_mok", "title": "Banteay Prei Temple : Fortress of the Jungle", "cr": "agelessrock", "added": TODAY, "published": "2023-07-16"}),
    ("Neam Rup (Pleasant Temple)", {"id": "T5XA5spGcMo", "title": "Neam Rup Temple : Astronomical Effort for a Tiny Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-07-23"}),
    ("Phnom Chisor", {"id": "jKxR3s8tXqU", "title": "Phnom Chisor : A Temple With Unique Design", "cr": "agelessrock", "added": TODAY, "published": "2023-07-30"}),
    ("Banteay Srei", {"id": "qIOd9Qt8Rvc", "title": "Banteay Srei Temple : Citadel of Women", "cr": "agelessrock", "added": TODAY, "published": "2023-08-06"}),
    ("Bat Chum", {"id": "rugyshug2Hw", "title": "Bat Chum Temple : Three Shrines and a Baray", "cr": "agelessrock", "added": TODAY, "published": "2023-08-13"}),
    ("Veal Phtei", {"id": "jDekkDT73GM", "title": "Veal Phtei : A Temple Too Tiny", "cr": "agelessrock", "added": TODAY, "published": "2023-08-20"}),
    ("Beng Mealea", {"id": "5MEuk-zSSJo", "title": "Beng Mealea (1/2) : An Advance Temple Layout", "cr": "agelessrock", "added": TODAY, "published": "2023-08-27"}),
    ("Beng Mealea", {"id": "AvU2_ZYgFIc", "title": "Beng Mealea (2/2) : So big but yet so lost", "cr": "agelessrock", "added": TODAY, "published": "2023-09-03"}),
    ("Kravan", {"id": "PxvnrVm1ebk", "title": "Kravan - A Five Structure Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-09-10"}),

    # === Indonesia ===
    ("Kedulan", {"id": "oXweT9vwq24", "title": "Kedulan Temple 2 : A Trinity Mystery", "cr": "agelessrock", "added": TODAY, "published": "2024-02-04"}),
    ("Kedulan", {"id": "qDduNWHpPB8", "title": "Kedulan Temple 1 : A Sunken Treasure", "cr": "agelessrock", "added": TODAY, "published": "2024-01-28"}),
    ("Sari", {"id": "PR_IBAO6dNg", "title": "Sari Temple : Once a Glittering Golden Temple", "cr": "agelessrock", "added": TODAY, "published": "2024-01-21"}),
    ("Lumbung", {"id": "nvvPSTFRGCE", "title": "Lumbung Temple : Rice Barn Temple with no history and no rice", "cr": "agelessrock", "added": TODAY, "published": "2024-01-14"}),
    ("Bubrah", {"id": "VVuEZUycuoo", "title": "Bubrah Temple : Restored Temple with Damaged History", "cr": "agelessrock", "added": TODAY, "published": "2024-01-07"}),
    ("Barong", {"id": "4aCkVXA9Vok", "title": "Barong Temple : 3 minus 1 = Confuse", "cr": "agelessrock", "added": TODAY, "published": "2023-12-31"}),
    ("Banyunibo", {"id": "6uOG_3yOlEQ", "title": "Banyunibo Temple : A Temple with Sacred Layout", "cr": "agelessrock", "added": TODAY, "published": "2023-12-24"}),
    ("Sumbawa Megaliths", {"id": "QPshss9J9oE", "title": "Sumbawa : An Island of Megalithic Mysteries", "cr": "agelessrock", "added": TODAY, "published": "2023-12-17"}),
    ("Sumbawa Megaliths", {"id": "CKIDugjXb6M", "title": "Sumbawa : Megaliths of Ai Renung - The Phantom Five", "cr": "agelessrock", "added": TODAY, "published": "2023-12-10"}),
    ("Sumbawa Megaliths", {"id": "6nnKGlyel54", "title": "Sumbawa : Megaliths of Raboran - Sarcophagi or something else?", "cr": "agelessrock", "added": TODAY, "published": "2023-12-03"}),
    ("Sumba Megalithic Tombs", {"id": "pOJRzSf1aZ0", "title": "Sumba : Mysterious Megalithic Tombs", "cr": "agelessrock", "added": TODAY, "published": "2023-11-26"}),
    ("Pura Besakih", {"id": "n2Ke5kyDXjs", "title": "Pura Agung Besakih : A Temple Too Grand To Be Unheard Off", "cr": "agelessrock", "added": TODAY, "published": "2023-11-19"}),
    ("Pura Lempuyang Luhur", {"id": "sUoWWFHMYM8", "title": "Penataran Agung Lempuyang Luhur : A World Class Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-11-12"}),
    ("Tampaksiring (Gunung Kawi)", {"id": "rU6PvkJHGDg", "title": "Megalith of Tampaksiring at Gunung Kawi", "cr": "agelessrock", "added": TODAY, "published": "2023-11-05"}),
    ("Borobudur", {"id": "7ZEm8hS2ppw", "title": "Borobudur (Part 4/4) : Borobudur was built when stones were soft like clay", "cr": "agelessrock", "added": TODAY, "published": "2023-10-29"}),
    ("Borobudur", {"id": "jDWx0u48eHc", "title": "Borobudur (3/4) : In the beginning there was Wisdom and Wisdom was Buddha", "cr": "agelessrock", "added": TODAY, "published": "2023-10-22"}),
    ("Borobudur", {"id": "lJSGbQXuBr8", "title": "Borobudur (Part 2/4) : A monument we barely know", "cr": "agelessrock", "added": TODAY, "published": "2023-10-15"}),
    ("Borobudur", {"id": "X49i3_PNWsA", "title": "Borobudur (Part 1/4) : A huge stepped pyramid?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-08"}),
    ("Pawon", {"id": "OO7aBMneVR4", "title": "Is Petite Pawon Temple for Worship?", "cr": "agelessrock", "added": TODAY, "published": "2023-10-01"}),
    ("Mendut", {"id": "syjj8Xww7Fs", "title": "Mysterious Mendut Temple on Ley Line", "cr": "agelessrock", "added": TODAY, "published": "2023-09-24"}),
    ("Ijo", {"id": "uU2vxLPhAdA", "title": "Ijo Temple on Ijo Hill is very mojo", "cr": "agelessrock", "added": TODAY, "published": "2023-09-17"}),
    ("Sojiwan", {"id": "ysfRtduVV4Q", "title": "Stupendous Sojiwan Temple with a taste of mystery", "cr": "agelessrock", "added": TODAY, "published": "2023-09-10"}),
    ("Ratu Boko", {"id": "vLX686DLnrc", "title": "Ratu Boko (4/4) : Is this a palace in another dimension?", "cr": "agelessrock", "added": TODAY, "published": "2023-09-03"}),
    ("Ratu Boko", {"id": "XPpYzLHr3gQ", "title": "Ratu Boko (3/4) : How can we not know anything about this site?", "cr": "agelessrock", "added": TODAY, "published": "2023-08-27"}),
    ("Ratu Boko", {"id": "RLZm5_5b3sw", "title": "Ratu Boko (2/4) : Lots of platforms but still no clue", "cr": "agelessrock", "added": TODAY, "published": "2023-08-20"}),
    ("Ratu Boko", {"id": "XnQG4mYzAFQ", "title": "Ratu Boko (1/4) : Who built Ratu Boko Palace?", "cr": "agelessrock", "added": TODAY, "published": "2023-08-13"}),
    ("Sambisari", {"id": "6Gk8UVc-SCo", "title": "Sambisari Temple (2/2) : Is it related to Pyramid of The Feathered Serpent in Mexico?", "cr": "agelessrock", "added": TODAY, "published": "2023-08-06"}),
    ("Sambisari", {"id": "LeWQrudrMZg", "title": "Sambisari Temple (1/2) : A stupendous temple 6.5m below ground level.", "cr": "agelessrock", "added": TODAY, "published": "2023-07-30"}),
    ("Sewu Temple", {"id": "eonkC5jh-ns", "title": "Sewu Temple (2/2) : Blueprints of builders found in Cambodia, Mexico and Iran?", "cr": "agelessrock", "added": TODAY, "published": "2023-07-23"}),
    ("Sewu Temple", {"id": "K0YK_LvtETE", "title": "Sewu Temple (1/2) : Head Spinning Sewu Temple of Klaten in Java", "cr": "agelessrock", "added": TODAY, "published": "2023-07-16"}),
    ("Kalasan", {"id": "RJDSJvg50E4", "title": "Is Kalasan Temple in Indonesia related to Chichen Itza Temple in Mexico?", "cr": "agelessrock", "added": TODAY, "published": "2023-07-09"}),
    ("Plaosan", {"id": "Pi1GSU0tyPM", "title": "Phenomenal Plaosan of Prambanan in Java, Indonesia", "cr": "agelessrock", "added": TODAY, "published": "2023-07-02"}),
    ("Prambanan", {"id": "GP0gKHEXWzA", "title": "Phenomenal Perturbing Prambanan Temple", "cr": "agelessrock", "added": TODAY, "published": "2023-06-25"}),
    ("Toraja Rock-Cut Burials", {"id": "Zwxp5Yw8HmE", "title": "Gigantic Monoliths and Mysterious Rock Cut Burials of Toraja, Indonesia", "cr": "agelessrock", "added": TODAY, "published": "2023-06-18"}),
    ("Nias Island Megaliths", {"id": "Wii86ebnCn8", "title": "Who made monoliths and stone tables in Nias Island of Indonesia?", "cr": "agelessrock", "added": TODAY, "published": "2023-06-11"}),
    ("Bada Valley Megaliths", {"id": "oHrkACXQ3Kg", "title": "Balang Gergasi di Situs Megalitik Lembah Bada", "cr": "agelessrock", "added": TODAY, "published": "2023-06-04"}),
    ("Bada Valley Megaliths", {"id": "CVRIfc21tbc", "title": "Mysterious Giant Stone Jars of Bada Valley in Sulawesi", "cr": "agelessrock", "added": TODAY, "published": "2023-05-28"}),

    # === India (Megalithomania) ===
    ("Maliabad Fort", {"id": "BglGyCgVE0U", "title": "Who Built the Polygonal & Cyclopean Walls of Maliabad Fort in India? | Megalithomania", "cr": "megalithomania", "added": TODAY, "published": "2025-06-15"}),
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

    # Country tagging
    if isinstance(countries, dict):
        cam_sites = ['Bayon Temple', 'Preah Khan (Angkor)', 'Srah Srang', 'Banteay Kdei',
                     'West Baray', 'West Mebon', 'East Baray', 'East Mebon',
                     'Neak Poan (Jayatataka Baray)', 'Bat Chum', 'Banteay Srei',
                     'Veal Phtei', 'Kravan', 'Chaw Srei Vibol', 'Banteay Prei (Angkor)',
                     'Neam Rup (Pleasant Temple)', 'Phnom Chisor', 'Banteay Chhmar',
                     'Banteay Toap', 'Banteay Prei Nokor']
        ind_sites = ['Ratu Boko', 'Sambisari', 'Sewu Temple', 'Plaosan', 'Kalasan',
                     'Mendut', 'Pawon', 'Ijo', 'Sojiwan', 'Banyunibo', 'Barong', 'Bubrah',
                     'Lumbung', 'Sari', 'Kedulan', 'Tampaksiring (Gunung Kawi)',
                     'Pura Besakih', 'Pura Lempuyang Luhur', 'Sumba Megalithic Tombs',
                     'Sumbawa Megaliths', 'Toraja Rock-Cut Burials', 'Nias Island Megaliths']
        for c, names in [('Cambodia', cam_sites), ('Indonesia', ind_sites), ('India', ['Maliabad Fort'])]:
            countries.setdefault(c, [])
            for n in names:
                if n not in countries[c]:
                    countries[c].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (Cambodia, Indonesia, India)")

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
