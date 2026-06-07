#!/usr/bin/env python3
"""
add-ageless-rock-turkey-batch.py — Big batch: 23 walkthroughs from
Ageless Rock's Turkey playlist, covering Cappadocia underground cities,
rock-cut monasteries, and Mesopotamian sites along Turkey's southeast.

  New creator:
    agelessrock — Ageless Rock (2.69K subs), boots-on-ground walkthroughs
    of underground cities and rock-cut sites, focused on the "what does
    the rock actually show" question. Editorial angle: tool marks, scale,
    and design intent often inconsistent with mainstream dating.

  Existing sites (videos wired only):
    - Derinkuyu Underground City    (2 videos: 2-part series)
    - Kaymakli Underground City     (2 videos: 2-part series)
    - Gaziemir Underground City     (1 video)
    - Tatlarin Underground City     (1 video)
    - Özlüce Underground City       (1 video)
    - Özkonak Underground City      (1 video)
    - Mazi Underground City         (1 video)
    - Nevşehir Underground City     (1 video — Kayasehir is its Turkish name)

  New sites (videos + site entries):
    Gümüşler Rock-Cut Monastery, St. Mercurius Underground City,
    Kırkgöz Underground City, Ağırnas Underground City,
    Aydıntepe Underground City, Ersele Underground City,
    Dara Ancient City, Bazda Caves, Dulkadirli Underground City,
    Manazan Caves & Taşkale Granaries, Midyat (Matiate) Underground City,
    Mucur Underground City, Höyük Underground City

None of the videos qualify for NEW badge (all 6+ months old).

Idempotent. Run from the repo root:
    python3 scripts/add-ageless-rock-turkey-batch.py
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
    "agelessrock": {
        "name": "Ageless Rock",
        "handle": "@AgelessRock888",
        "subs": "boots-on-ground walkthroughs of underground cities, rock-cut "
                "monasteries, and megalithic sites; focused on tool marks, scale, "
                "and design intent that often resist mainstream chronology",
        "color": "#8C6E4F",  # cappadocian volcanic tuff
        "tier": 3,
    }
}

# ============================================================
# New sites (12) — Turkey
# ============================================================
NEW_SITES = [
    {
        "n": "Gümüşler Rock-Cut Monastery",
        "lat": 38.0083, "lng": 34.7500,
        "cat": "rockcut", "region": "Türkiye",
        "tier": 2, "signal": "open",
        "criteria": ["scale", "geometry", "precision"],
        "desc": (
            "Top-down rock-cut Byzantine monastery complex in Niğde Province, "
            "carved into a single mass of volcanic tuff. The site features a "
            "fortified main chapel with surviving frescoes, multiple chambers "
            "across vertical levels, an inner courtyard, and a hidden upper "
            "refuge accessible by ladder. Conventionally dated to the 8th-12th "
            "century Byzantine era. The site's vertical excavation strategy and "
            "the precision of its chamber alignments invite a reading consistent "
            "with much earlier rock-cutting traditions in Cappadocia."
        ),
    },
    {
        "n": "St. Mercurius Underground City",
        "lat": 38.7500, "lng": 34.7000,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground complex in the Cappadocia region associated with the "
            "early Christian veneration of St. Mercurius. Multiple levels with "
            "living chambers, storage rooms, and chapels. Like most Cappadocia "
            "underground cities, the dating rests on architectural comparison "
            "rather than direct evidence, leaving the original construction "
            "phase an open question."
        ),
    },
    {
        "n": "Kırkgöz Underground City",
        "lat": 38.7000, "lng": 35.0000,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground city in the Cappadocia region whose name (\"forty eyes\") "
            "refers to the multiple ventilation and access shafts cut through the "
            "complex. Living quarters, storage, and chapels span several levels. "
            "Part of the broader Cappadocian underground network with at least "
            "200 documented sites, most still under-investigated."
        ),
    },
    {
        "n": "Ağırnas Underground City",
        "lat": 38.8000, "lng": 35.6500,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry", "precision"],
        "desc": (
            "Multi-level underground complex in Kayseri Province, in the village "
            "of Ağırnas — the birthplace of the Ottoman master architect Mimar "
            "Sinan. The complex includes a chapel, living chambers, ventilation "
            "shafts, and storage rooms carved through volcanic tuff. Conventional "
            "dating attributes the site to the Byzantine era; independent readings "
            "point to potentially much older origins consistent with the broader "
            "Cappadocian network."
        ),
    },
    {
        "n": "Aydıntepe Underground City",
        "lat": 40.3833, "lng": 40.1333,
        "cat": "underground", "region": "Türkiye",
        "tier": 2, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground city in Bayburt Province in northeastern Turkey, "
            "geographically separated from the main Cappadocia network. Multi-level "
            "tunnels, chambers, and storage spaces carved into sedimentary rock, "
            "currently with about 1 km of excavated passageways. Conventional "
            "reading: late Roman / early Byzantine. Independent reading: the "
            "presence of this construction style this far from Cappadocia raises "
            "questions about how widely the underground-city tradition extended."
        ),
    },
    {
        "n": "Ersele Underground City",
        "lat": 38.6000, "lng": 34.7000,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground complex in the Cappadocia region with multiple chambers "
            "and connecting tunnels carved into volcanic tuff. Part of the broader "
            "Nevşehir-Kayseri underground network. Limited formal investigation."
        ),
    },
    {
        "n": "Dara Ancient City",
        "lat": 37.1764, "lng": 40.9500,
        "cat": "city", "region": "Türkiye",
        "tier": 1, "signal": "open",
        "criteria": ["scale", "polygonal", "geometry", "precision"],
        "desc": (
            "Late Roman / Byzantine frontier city in Mardin Province, southeastern "
            "Turkey, in ancient Mesopotamia. Founded by Anastasius I around 505 CE "
            "as a fortress against the Sasanian Persians. The visible complex "
            "includes massive cyclopean walls, a vast underground cistern with "
            "precise rock-cut chambers, a necropolis with elaborate tomb chambers, "
            "and an underground bridge. The Mor Mihail Monastery sits above. "
            "Independent investigators note that the rock-cut work at Dara shows "
            "tool-mark precision and chamber geometry that may predate the "
            "official Byzantine founding, with reuse and expansion in the 6th "
            "century built atop a much older substrate."
        ),
    },
    {
        "n": "Bazda Caves",
        "lat": 37.0167, "lng": 39.0167,
        "cat": "rockcut", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "precision"],
        "desc": (
            "Ancient rock-cut quarry and cave system in Şanlıurfa Province near "
            "Harran, in the cradle of early Mesopotamian civilization. The caves "
            "are documented as a Roman-era quarry that supplied stone for the "
            "city of Harran, though local tradition and the scale of the workings "
            "suggest earlier origins. The site sits in the same landscape as "
            "Göbekli Tepe (60 km away) and Karahan Tepe."
        ),
    },
    {
        "n": "Dulkadirli Underground City",
        "lat": 39.0667, "lng": 34.3833,
        "cat": "underground", "region": "Türkiye",
        "tier": 2, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground city in Kırşehir Province featuring an extensive network "
            "of tunnels, chambers, and ventilation shafts. Carved through volcanic "
            "tuff at the northwestern edge of the Cappadocian underground network. "
            "Dating remains an open question, with mainstream attribution to the "
            "Byzantine era and independent readings suggesting pre-Byzantine origin."
        ),
    },
    {
        "n": "Manazan Caves & Taşkale Granaries",
        "lat": 37.2667, "lng": 33.4500,
        "cat": "rockcut", "region": "Türkiye",
        "tier": 2, "signal": "open",
        "criteria": ["scale", "precision", "geometry"],
        "desc": (
            "Two adjacent rock-cut complexes in Karaman Province, in central "
            "southern Turkey. The Manazan Caves form a multi-level cliff-side "
            "settlement with linked chambers carved into vertical rock. The "
            "Taşkale Granaries are hundreds of precisely-cut rectangular grain "
            "storage chambers carved into a cliff face, still used by local "
            "farmers today. The granaries' precision and the scale of the cliff "
            "excavation invite comparison with similar rock-cut storage at sites "
            "across the wider Anatolian and Mesopotamian region."
        ),
    },
    {
        "n": "Matiate (Midyat) Underground City",
        "lat": 37.4167, "lng": 41.3500,
        "cat": "underground", "region": "Türkiye",
        "tier": 1, "signal": "open",
        "criteria": ["scale", "geometry", "precision"],
        "desc": (
            "Massive underground city discovered in 2020 beneath the modern town "
            "of Midyat in Mardin Province. Initial surveys describe it as one of "
            "the largest underground cities in the world, with estimates of "
            "capacity for up to 70,000 people and an estimated age of at least "
            "1,900 years. Multiple levels, chambers, places of worship, water "
            "wells, and storage facilities have been identified. Excavation is "
            "active and ongoing. Conventional reading: Roman-era refuge for "
            "early Christians and Jews. Independent reading: scale and design "
            "may indicate much older origins reused across cultures."
        ),
    },
    {
        "n": "Mucur Underground City",
        "lat": 39.0667, "lng": 34.3833,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground complex in Kırşehir Province at the edge of the broader "
            "Cappadocian underground network. Multi-level chambers, tunnels, and "
            "ventilation systems carved through volcanic tuff. Conventional and "
            "independent dating in dispute, consistent with the broader pattern "
            "of under-studied sites in the region."
        ),
    },
    {
        "n": "Höyük Underground City",
        "lat": 37.7000, "lng": 31.6000,
        "cat": "underground", "region": "Türkiye",
        "tier": 3, "signal": "open",
        "criteria": ["scale", "geometry"],
        "desc": (
            "Underground city in Konya Province, geographically distinct from the "
            "primary Cappadocian network. Multi-level chambers, storage rooms, "
            "and connecting tunnels. The site's location west of the main "
            "Cappadocian cluster broadens the geographic footprint of the "
            "Anatolian underground-city tradition."
        ),
    },
]

# ============================================================
# All 23 videos to wire
# ============================================================
VIDEOS_TO_WIRE = [
    # Derinkuyu 2-part series (3 years ago)
    ("Derinkuyu Underground City", {
        "id": "jtyIbbt7LTo",
        "title": "Derinkuyu (Part 1/2) : Underground City - Do you want to run or dig?",
        "cr": "agelessrock", "added": TODAY, "published": "2023-06-15"}),
    ("Derinkuyu Underground City", {
        "id": "FLNFTRN7SkI",
        "title": "Derinkuyu (Part 2/2) : Tool Marks + Zoroastrianism = Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2023-06-15"}),
    # Kaymakli 2-part series (3 years ago)
    ("Kaymakli Underground City", {
        "id": "qWbGNp_arS0",
        "title": "Kaymakli Underground City (Part 1/2) : Circular Stones = Stone Door?",
        "cr": "agelessrock", "added": TODAY, "published": "2023-06-22"}),
    ("Kaymakli Underground City", {
        "id": "nDYYy-3rG6I",
        "title": "Kaymakli Underground City (Part 2/2) - Narrative that doesn't make sense",
        "cr": "agelessrock", "added": TODAY, "published": "2023-06-22"}),
    # Recent series
    ("Gümüşler Rock-Cut Monastery", {
        "id": "iVdP3GDHe0w",
        "title": "The Amazing Top-Down Rock Cut Monastery of Gumusler",
        "cr": "agelessrock", "added": TODAY, "published": "2025-08-15"}),
    ("St. Mercurius Underground City", {
        "id": "xdW6AVcAoz8",
        "title": "St. Mercurius Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-08-22"}),
    ("Kırkgöz Underground City", {
        "id": "Gx9ypiw_dLo",
        "title": "Kirkgoz Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-09-08"}),
    ("Ağırnas Underground City", {
        "id": "_zAGOAJVgvI",
        "title": "Agirnas Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-09-15"}),
    ("Aydıntepe Underground City", {
        "id": "BTyiM6SFBCY",
        "title": "Aydintepe Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-09-22"}),
    ("Gaziemir Underground City", {
        "id": "TB-aKnBAgww",
        "title": "Gaziemir Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-09-29"}),
    ("Tatlarin Underground City", {
        "id": "0iDI4tXtH8A",
        "title": "Tatlarin Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-10-06"}),
    ("Özlüce Underground City", {
        "id": "nhqtFw8CJLk",
        "title": "Ozluce Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-10-13"}),
    ("Özkonak Underground City", {
        "id": "WkUUEQBvnZY",
        "title": "Ozkonak Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-10-20"}),
    ("Mazi Underground City", {
        "id": "nW9HJH9XdVo",
        "title": "Mazi Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-10-27"}),
    ("Ersele Underground City", {
        "id": "XAs8VmSD4gA",
        "title": "Ersele Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-11-03"}),
    ("Dara Ancient City", {
        "id": "GmuLXYPzH8A",
        "title": "The Mysterious Dara Ancient City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-11-10"}),
    ("Bazda Caves", {
        "id": "1ZjnsOl2OM8",
        "title": "Bazda Caves",
        "cr": "agelessrock", "added": TODAY, "published": "2025-11-17"}),
    ("Dulkadirli Underground City", {
        "id": "zDqunWbprGs",
        "title": "Dulkadilri Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-11-24"}),
    ("Nevşehir Underground City", {
        "id": "1XnVlmwiOWo",
        "title": "Kayasehir Rock City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-12-01"}),
    ("Manazan Caves & Taşkale Granaries", {
        "id": "aFMzYu1u2-U",
        "title": "Mysterious Manazan Caves and Thrilling Taskale Granaries",
        "cr": "agelessrock", "added": TODAY, "published": "2025-12-08"}),
    ("Matiate (Midyat) Underground City", {
        "id": "WxtKfaSlzNs",
        "title": "Midyat Caves or Matiate Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-12-15"}),
    ("Mucur Underground City", {
        "id": "Ca2uUIh8OYE",
        "title": "Mucur Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-12-22"}),
    ("Höyük Underground City", {
        "id": "dIRMbwH9ul8",
        "title": "Huyuk Underground City",
        "cr": "agelessrock", "added": TODAY, "published": "2025-12-29"}),
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

    # 1. Creators
    for key, info in NEW_CREATORS.items():
        if key in creators:
            print(f"  · Creator '{key}' already exists")
        else:
            creators[key] = info
            print(f"  ✓ Added creator: {key} ({info['name']})")
    save('creators.json', creators)

    # 2. Sites
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

    # 3. Videos
    creators = load('creators.json')
    videos_wired = 0
    videos_skipped = 0
    for site_name, v in VIDEOS_TO_WIRE:
        if v['cr'] not in creators:
            sys.exit(f"✗ Video {v['id']} references unknown creator '{v['cr']}'")
        videos.setdefault(site_name, [])
        existing_ids = {x['id'] for x in videos[site_name]}
        if v['id'] in existing_ids:
            videos_skipped += 1
            print(f"  · Already wired: {v['id']} → {site_name}")
        else:
            videos[site_name].append(v)
            videos_wired += 1
            print(f"  ✓ Wired: {v['id']} → {site_name}")
    if videos_wired:
        save('videos.json', videos)

    # 4. Country tag
    if isinstance(countries, dict):
        for key in ['Türkiye', 'Turkey']:
            if key in countries:
                added = 0
                for s in NEW_SITES:
                    if s['n'] not in countries[key]:
                        countries[key].append(s['n'])
                        added += 1
                if added:
                    save('countries.json', countries)
                    print(f"  ✓ {key} tagged with {added} new sites")
                break

    sites = load('sites.json')
    videos = load('videos.json')
    creators = load('creators.json')
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"\n--- summary ---")
    print(f"  Total sites:        {len(sites)}")
    print(f"  Open-question:      {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")
    print(f"  Total creators:     {len(creators)}")
    print(f"  This batch:         {videos_wired} wired, {videos_skipped} skipped, {sites_added} new sites")
    print()
    print("Now run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
