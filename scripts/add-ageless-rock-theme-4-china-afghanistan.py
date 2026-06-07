#!/usr/bin/env python3
"""
add-ageless-rock-theme-4-china-afghanistan.py — Theme 4.

  China (26 walkthroughs):
    - 4 wired to existing: Leshan, Longyou Caves, Yangshan Quarry, Huashan
    - 22 new sites: Mogao, Longmen, Yungang, Bingling, Maijishan, Dazu,
      Qin Shi Huang Mausoleum, Maoling Mausoleum, Xuankong (Hanging Temple),
      Tianlong Shan, Xumishan, Mengshan Giant Buddha, Tiantishan,
      Matisi, Wushan, Shaohao Mausoleum, Elephant Mountain, Yuji Mountain,
      Rongxian Giant Buddha, Keyan Big Buddha, Goguryeo Tombs (Jilin),
      Zhangye Dafo Temple

  Afghanistan (2 walkthroughs, both new sites):
    - Bamiyan, Takht-e Rustam (top-down rock-cut bedrock stupa)

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-theme-4-china-afghanistan.py
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
    # === China (22 new) ===
    {"n": "Mogao Grottoes", "lat": 40.0467, "lng": 94.7997,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "UNESCO-listed Buddhist cave complex near Dunhuang, Gansu. 735 caves carved into a 1.6 km cliff face along the Silk Road, with murals covering 45,000 square meters of wall surface and over 2,400 painted clay sculptures. Active 4th-14th centuries CE."},
    {"n": "Longmen Grottoes", "lat": 34.5566, "lng": 112.4744,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Cliff-face Buddhist cave complex outside Luoyang, Henan, carved into limestone over the Yi River. Over 2,300 caves containing 100,000+ Buddha statues and 60+ stupas. Active 5th-10th centuries CE under the Northern Wei and Tang dynasties. UNESCO World Heritage."},
    {"n": "Yungang Grottoes", "lat": 40.1100, "lng": 113.1300,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Buddhist cave complex outside Datong, Shanxi, with 252 caves carved into sandstone cliffs during the Northern Wei dynasty (5th-6th c. CE). Contains over 51,000 statues, including monumental Buddhas exceeding 17 meters in height."},
    {"n": "Bingling Temple Grottoes", "lat": 35.7989, "lng": 103.0000,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex in Gansu, accessible only by boat across the Liujiaxia Reservoir. 183 caves and 694 statues across multiple cliffs. The 27-meter seated Maitreya is the centerpiece. Carved between the 4th and 16th centuries."},
    {"n": "Maijishan Grottoes", "lat": 34.3567, "lng": 105.8939,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex on a mountain shaped like a wheat-stack in Tianshui, Gansu. 194 caves with 7,200+ sculptures. Caves accessible via a vertical maze of plank walkways and bridges clinging to the cliff face. Active 5th-13th centuries."},
    {"n": "Dazu Rock Carvings", "lat": 29.7028, "lng": 105.7000,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Cliff-face Buddhist, Taoist, and Confucian carvings outside Chongqing. 50,000+ statues across 75 sites, mostly carved 9th-13th centuries CE under the Song dynasty. UNESCO World Heritage."},
    {"n": "Qin Shi Huang Mausoleum", "lat": 34.3833, "lng": 109.2500,
     "cat": "tomb", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Tomb complex of China's first emperor, Qin Shi Huang (210 BCE), near Xi'an. The central mound (over 50m tall) remains unexcavated. Surrounded by the famous Terracotta Army of 8,000+ life-size warriors, plus chariots and horses. The interior chamber is described in Sima Qian's records as containing mercury rivers and a celestial mural."},
    {"n": "Maoling Mausoleum (Great White Pyramid)", "lat": 34.3597, "lng": 108.5728,
     "cat": "tomb", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "geometry"],
     "desc": "Tomb of Emperor Wu of Han (139-87 BCE) near Xianyang, Shaanxi. A massive pyramidal mound, the largest of the Han imperial pyramids in the area. Sometimes called the 'Great White Pyramid' for its size and visibility. Unexcavated."},
    {"n": "Xuankong Temple (Hanging Temple)", "lat": 39.6649, "lng": 113.7079,
     "cat": "temple", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["precision", "geometry"],
     "desc": "Buddhist-Taoist-Confucian temple built into a cliff face in Shanxi, 75 meters above the ground. The temple is supported by oak crossbeam pegs inserted into the cliff and appears to defy gravity. Original construction in the late Northern Wei (5th-6th c. CE)."},
    {"n": "Tianlong Shan Grottoes", "lat": 37.7500, "lng": 112.4500,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex in Taiyuan, Shanxi. 25 caves carved during the Eastern Wei, Northern Qi, Sui, and Tang dynasties (6th-8th c. CE). Many sculptures were removed in the early 20th century — recent reunification projects have begun returning them digitally."},
    {"n": "Xumishan Grottoes", "lat": 36.4000, "lng": 106.2167,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex in Guyuan, Ningxia, with 162 caves carved into red sandstone. The largest Buddha is 20.6 meters tall. Active 5th-9th c. CE."},
    {"n": "Mengshan Giant Buddha", "lat": 37.7833, "lng": 112.4789,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Massive seated Buddha statue carved into Mount Meng outside Taiyuan, Shanxi. Originally 63 meters tall (officially the world's tallest seated stone Buddha when built in 551 CE under the Northern Qi). Mostly buried by landslides until 20th-century rediscovery."},
    {"n": "Tiantishan Grottoes", "lat": 37.6644, "lng": 102.9075,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex on Heavenly Stairs Mountain (Tiantishan) near Wuwei, Gansu. The central Buddha statue is 28 meters tall. Caves carved between the 5th and 7th centuries."},
    {"n": "Matisi Grottoes", "lat": 38.6500, "lng": 100.5000,
     "cat": "rockcut", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Multi-level Buddhist cave complex in Zhangye, Gansu, carved into a red sandstone mountain. Caves connected by tunnels and stairs cut through the rock. Active 4th c. CE through Yuan dynasty."},
    {"n": "Wushan Grottoes (Lashao Temple)", "lat": 34.7167, "lng": 104.6833,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex in Wushan County, Gansu. Distinct from Maijishan. Contains a 40-meter-tall standing Buddha carved into the cliff face (one of the largest standing stone Buddhas in China)."},
    {"n": "Shaohao Mausoleum", "lat": 35.7333, "lng": 117.0167,
     "cat": "tomb", "region": "Asia", "tier": 2, "signal": "open",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Pyramidal mausoleum near Qufu, Shandong, attributed to the mythological emperor Shaohao (c. 2600 BCE in traditional chronology). Step-pyramid construction in stone, similar in form to Mesoamerican pyramids. Open questions about the chronology."},
    {"n": "Elephant Mountain Grottoes", "lat": 29.3667, "lng": 105.1167,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist cave complex on Elephant Mountain in Sichuan. Centerpiece is a 36-meter-tall seated Buddha carved into the cliff. Tang dynasty (7th-9th c. CE)."},
    {"n": "Yuji Mountain Buddha", "lat": 34.5500, "lng": 109.2167,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Giant seated Buddha statue carved into Yuji Mountain in Shaanxi. Less well-known than Leshan, but of substantial scale. Tang-era carving."},
    {"n": "Rongxian Giant Buddha", "lat": 29.4789, "lng": 104.0167,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "36-meter-tall seated Buddha statue carved into a cliff face in Rongxian, Sichuan. Tang dynasty (early 9th c. CE)."},
    {"n": "Keyan Big Buddha", "lat": 30.0167, "lng": 120.5833,
     "cat": "rockcut", "region": "Asia", "tier": 3, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Stone Buddha carved into a granite cliff at Keyan, Shaoxing, Zhejiang. The site doubles as a former quarry that produced stone for the broader Shaoxing region. The Buddha statue is approximately 10.6 m tall."},
    {"n": "Goguryeo Tombs (Jilin)", "lat": 41.1167, "lng": 126.1833,
     "cat": "tomb", "region": "Asia", "tier": 1, "signal": "convergent",
     "criteria": ["scale", "geometry", "precision"],
     "desc": "Goguryeo Kingdom royal tombs in Ji'an, Jilin Province, near the North Korean border. Step-pyramid tombs of the Goguryeo kings (c. 37 BCE - 668 CE), constructed of precisely-fitted stone blocks. The General's Tomb is 31 m wide and 13 m high. Distinct stone-pyramid tradition that parallels Maya step-pyramid construction."},
    {"n": "Zhangye Dafo Temple", "lat": 38.9333, "lng": 100.4500,
     "cat": "temple", "region": "Asia", "tier": 2, "signal": "convergent",
     "criteria": ["scale", "precision"],
     "desc": "Buddhist temple in Zhangye, Gansu, founded 1098 CE. Houses the largest indoor reclining Buddha in China — 35 meters long, made of clay over a wooden frame. Active monastery along the Silk Road."},

    # === Afghanistan (2 new) ===
    {"n": "Bamiyan", "lat": 34.8326, "lng": 67.8264,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision"],
     "desc": "Sandstone cliffs in central Afghanistan holding the niches of two monumental standing Buddhas (35m and 53m) carved into the cliff in the 6th century CE. Destroyed by the Taliban in 2001. The surrounding cliff complex contains hundreds of meditation caves with painted frescoes still visible. UNESCO World Heritage as a cultural landscape since 2003."},
    {"n": "Takht-e Rustam (Afghanistan)", "lat": 36.7000, "lng": 67.1167,
     "cat": "rockcut", "region": "Asia", "tier": 1, "signal": "open",
     "criteria": ["scale", "precision", "geometry"],
     "desc": "Top-down rock-cut Buddhist stupa carved from a single bedrock outcrop in Samangan Province, northern Afghanistan. The stupa is excavated into the surrounding rock rather than built up — the entire complex (stupa, surrounding monastery cells, courtyard) was sculpted by removing material. Same top-down technique visible at Kailasa (India), Dharmrajeshwar (India), and the Lalibela churches (Ethiopia)."},
]

# ============================================================
VIDEOS_TO_WIRE = [
    # === China ===
    ("Huashan Grottoes", {"id": "tvin563SMCo", "title": "Mysteries of Huashan Grottoes in China", "cr": "agelessrock", "added": TODAY, "published": "2022-12-01"}),
    ("Longyou Caves", {"id": "9WqTASklAWY", "title": "The Mysterious Longyou Caves in China", "cr": "agelessrock", "added": TODAY, "published": "2022-12-08"}),
    ("Yangshan Quarry", {"id": "UZJVXxoFMoo", "title": "Mysterious Yangshan Monument", "cr": "agelessrock", "added": TODAY, "published": "2022-12-15"}),
    ("Goguryeo Tombs (Jilin)", {"id": "FpL5c3xRlEs", "title": "The Mysterious Goguryeo Tombs in China", "cr": "agelessrock", "added": TODAY, "published": "2022-12-29"}),
    ("Shaohao Mausoleum", {"id": "A7Ewz9Mjfq4", "title": "The Mysterious Shaohao Tomb / Mausoleum in China", "cr": "agelessrock", "added": TODAY, "published": "2022-12-22"}),
    ("Maoling Mausoleum (Great White Pyramid)", {"id": "gt_6fP9GMgs", "title": "The Mysterious Great White Pyramid / Maoling Mausoleum in China", "cr": "agelessrock", "added": TODAY, "published": "2023-01-05"}),
    ("Qin Shi Huang Mausoleum", {"id": "jwgL_gXRces", "title": "The Mysterious Qin Shi Huang Mausoleum in China", "cr": "agelessrock", "added": TODAY, "published": "2023-01-12"}),
    ("Leshan Giant Buddha", {"id": "NkLghqHyUWM", "title": "The Mysterious Leshan Giant Buddha in China", "cr": "agelessrock", "added": TODAY, "published": "2023-01-19"}),
    ("Wushan Grottoes (Lashao Temple)", {"id": "St9OQDq2PGc", "title": "Mysterious Wushan Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2023-01-26"}),
    ("Longmen Grottoes", {"id": "sPAkmkyje8A", "title": "Mysterious Longmen Grottoes in Henan, China", "cr": "agelessrock", "added": TODAY, "published": "2023-02-02"}),
    ("Maijishan Grottoes", {"id": "gnbmvsPWuHY", "title": "The Mysterious Maijishan Grottoes in China", "cr": "agelessrock", "added": TODAY, "published": "2023-02-09"}),
    ("Zhangye Dafo Temple", {"id": "SEPNAIhGZtA", "title": "Dafo (Great Buddha) Temple in China", "cr": "agelessrock", "added": TODAY, "published": "2023-02-16"}),
    ("Matisi Grottoes", {"id": "ieYxHh-tMDA", "title": "Mysterious Magnificent Matisi Grottoes in China", "cr": "agelessrock", "added": TODAY, "published": "2023-02-23"}),
    ("Dazu Rock Carvings", {"id": "giJoaNJmgPw", "title": "The Mysterious Dazu Rock Carving and Grottoes in China.", "cr": "agelessrock", "added": TODAY, "published": "2023-03-02"}),
    ("Mogao Grottoes", {"id": "4ogImPDlsSk", "title": "Mysterious Mogao Grottoes in Gansu, China", "cr": "agelessrock", "added": TODAY, "published": "2023-03-09"}),
    ("Xuankong Temple (Hanging Temple)", {"id": "WB_pqZjeK80", "title": "Amazing Xuankong Temple (Hanging Temple) of Shanxi, China", "cr": "agelessrock", "added": TODAY, "published": "2023-03-16"}),
    ("Mengshan Giant Buddha", {"id": "CcYact99C0U", "title": "Magnificent Mengshan Giant Buddha of China", "cr": "agelessrock", "added": TODAY, "published": "2023-03-23"}),
    ("Tiantishan Grottoes", {"id": "fPDY_011IOk", "title": "Amazing Giant Buddha of Tiantishan (Heavenly Stairs Mountain) Grottoes in China", "cr": "agelessrock", "added": TODAY, "published": "2023-03-30"}),
    ("Yungang Grottoes", {"id": "LkyC_0lg57M", "title": "Giant Buddhas of Yungang Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2024-08-06"}),
    ("Xumishan Grottoes", {"id": "YCb_rI3zlkY", "title": "Giant Buddha of Xumishan Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2024-08-13"}),
    ("Bingling Temple Grottoes", {"id": "XZEiRg1RGng", "title": "Giant Buddha of Bingling Temple Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2024-08-20"}),
    ("Elephant Mountain Grottoes", {"id": "dOLrT9nuzPU", "title": "Giant Buddha of Elephant Mountain Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2024-08-27"}),
    ("Tianlong Shan Grottoes", {"id": "H4VN1ay68Bg", "title": "Giant Buddha of Tianlong Shan Grottoes", "cr": "agelessrock", "added": TODAY, "published": "2024-09-03"}),
    ("Yuji Mountain Buddha", {"id": "pyeAf6_f8dI", "title": "Giant Buddha of Yuji Mountain", "cr": "agelessrock", "added": TODAY, "published": "2024-09-10"}),
    ("Rongxian Giant Buddha", {"id": "S3PqiO2QTh8", "title": "Giant Buddha of Rongxian", "cr": "agelessrock", "added": TODAY, "published": "2024-09-17"}),
    ("Keyan Big Buddha", {"id": "83zjOOhP_Lg", "title": "Keyan Big Buddha", "cr": "agelessrock", "added": TODAY, "published": "2024-09-24"}),

    # === Afghanistan ===
    ("Takht-e Rustam (Afghanistan)", {"id": "F3MjnNYCSRA", "title": "Top-Down Rock-Cut Bedrock Stupa of Takht-e Rustam", "cr": "agelessrock", "added": TODAY, "published": "2022-11-15"}),
    ("Bamiyan", {"id": "GiPd3BzwP2U", "title": "Giant Buddha of Bamiyan", "cr": "agelessrock", "added": TODAY, "published": "2024-12-01"}),
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
        china_sites = [s['n'] for s in NEW_SITES if 'Afghanistan' not in s['n'] and s['n'] != 'Bamiyan']
        afgh_sites = ['Bamiyan', 'Takht-e Rustam (Afghanistan)']
        for c, names in [('China', china_sites), ('Afghanistan', afgh_sites)]:
            countries.setdefault(c, [])
            for n in names:
                if n not in countries[c]:
                    countries[c].append(n)
        save('countries.json', countries)
        print(f"  ✓ Country tags updated (China, Afghanistan)")

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
