#!/usr/bin/env python3
"""
add-mythical-ireland-batch.py — Anthony Murphy / Boyne Valley batch (2026-07-14)

Closes the long-standing backlog item ("Anthony Murphy / Boyne Valley batch").
Anchor creator: Anthony Murphy (Mythical Ireland, @mythicalireland, 26.4K subs)
— author, archaeoastronomy researcher, co-discoverer of the 2018 "Dronehenge"
henge at Newgrange, and 1999 co-discoverer of the Baltray solstice alignment.

EDITORIAL HONESTY NOTE (continues add-hugh-newman-triple-batch.py ledger):
    Asked (parked 2026-06)   Status now
    ----------------------   -----------------------------------------------
    Hill of Tara             ADDED — Murphy has a dedicated dawn walkthrough
    Poulnabrone              STILL PARKED — Murphy has no field video (only a
                             myth episode mentioning Sheelah); needs another anchor
    Knockmany                STILL PARKED — Murphy coverage is a myth lecture,
                             not field footage; needs another anchor
    Marlborough Mound        STILL PARKED — England, outside Murphy's territory

NEW CREATOR: anthonymurphy (tier 2)
NEW SITES (3, coords web-verified 2026-07-14 vs megalithic.co.uk /
megalithicireland.com / knowth.com / Wikipedia):
    Hill of Tara             53.5775, -6.6119   tomb  tier 2
    Fourknocks Passage Tomb  53.5966, -6.3265   tomb  tier 2
    Baltray Standing Stones  53.7408, -6.2658   megalithic  tier 3
WIRES (14): Newgrange×2, Knowth×2, Dowth×2, Loughcrew×2 (existing) +
    Hill of Tara×2, Fourknocks×3, Baltray×1 (new).
Two wires carry TRUE publish dates → they surface in the Creator Hub Recent
rail with the "New to the Atlas" badge (curation lever, see
add-stone-riddles-highlight-patch.py).

612 → 615 sites · 64 → 65 creators · 932 → 946 wires. Pre-flight floor: 615.
Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CR = "anthonymurphy"
ADDED = "2026-07-14"

CREATOR = {
    "name": "Anthony Murphy / Mythical Ireland",
    "handle": "@mythicalireland",
    "subs": "Boyne Valley archaeoastronomy · author · Dronehenge co-discoverer · Irish myth + megaliths",
    "color": "#4E9B47",
    "tier": 2,
}

NEW_SITES = [
    {
        "site": {
            "n": "Hill of Tara", "lat": 53.5775, "lng": -6.6119,
            "cat": "tomb", "region": "Europe", "tier": 2,
            "desc": "Ancient royal ceremonial complex in Co. Meath, traditionally the inauguration place and seat of the High Kings of Ireland, with earthworks spanning the Neolithic to the Iron Age. Its oldest visible monument is the Mound of the Hostages, a passage tomb built around 3200 BCE, and the Lia Fáil (Stone of Destiny) standing stone atop the Forradh was said to roar when touched by the rightful king.",
        },
        "country": "Ireland", "era": -3200, "civ": "Neolithic to Iron Age Ireland (Gaelic royal site)",
    },
    {
        "site": {
            "n": "Fourknocks Passage Tomb", "lat": 53.5966, "lng": -6.3265,
            "cat": "tomb", "region": "Europe", "tier": 2,
            "desc": "Decorated Neolithic passage tomb near the Meath–Dublin border, built around 3000 BCE, with a short passage opening into an unusually wide pear-shaped cruciform chamber with three recesses. Excavations in 1950–52 found some 65 burials, and among its dozen decorated stones is a stylized carving regarded as possibly the earliest depiction of a human face in Ireland; the chamber is now protected by a concrete dome.",
        },
        "country": "Ireland", "era": -3000, "civ": "Neolithic Ireland (passage tomb builders)",
    },
    {
        "site": {
            "n": "Baltray Standing Stones", "lat": 53.7408, "lng": -6.2658,
            "cat": "megalithic", "region": "Europe", "tier": 3,
            "desc": "A pair of standing stones (about 3 m and 2 m tall, 9 m apart, originally likely three) near the Boyne estuary in Co. Louth, probably erected in the Bronze Age. The flat face of the larger stone points toward Rockabill island offshore, marking the winter solstice sunrise — an alignment discovered and documented in 1999 by Anthony Murphy, Richard Moore and Michael Byrne.",
        },
        "country": "Ireland", "era": -1000, "civ": "Bronze Age Ireland",
    },
]

# (site, id, title, published-or-None)
WIRES = [
    ("Newgrange", "smBYtvhILDw", "Do the myths about Newgrange offer an insight into its function or purpose?", None),
    ("Newgrange", "R0s74JgOMf8", "Fascinating alignment of Newgrange and other ancient sites", None),
    ("Knowth", "ZiXceFW1pqU", "Knowth: one of the great treasures of Ireland", None),
    ("Knowth", "64jj111a9mo", "Knowth Calendar Stone — 5,300-year-old lunar calculations on Irish stone", None),
    ("Dowth", "AoaREltkFyg", "Midwinter sun shines into Dowth's southern chamber", None),
    ("Dowth", "TEA87IoIN-A", "Dowth Stone of the Seven Suns Projection Mapping", None),
    ("Loughcrew", "ZNrigPnGhOk", "Loughcrew: myths, history and astronomy of a Neolithic cemetery in Ireland", None),
    ("Loughcrew", "8z57ZIP-CeA", "The Hill of the Witch — the Cairns of Loughcrew, a quick guide", None),
    ("Hill of Tara", "U01nSNBjuwg", "Hill of Tara at dawn: a sunrise tour of the ancient monuments", "2020-03-16"),
    ("Hill of Tara", "L4BWDYh8tjw", "The First Kings of Tara", None),
    ("Fourknocks Passage Tomb", "OLnhZwkXBJQ", "Welcome to Fourknocks, a 5,000-year-old megalithic site in Meath", "2016-10-08"),
    ("Fourknocks Passage Tomb", "tGI8FWWTbTU", "Inside Fourknocks: megalithic art and astronomical alignment", None),
    ("Fourknocks Passage Tomb", "9WdAYLtcDMQ", "Fourknocks: a shimmering beam of the sun illuminates megalithic art", None),
    ("Baltray Standing Stones", "AaYSq7H6iuM", "Baltray standing stones midwinter sunrise", None),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    sites = load("sites.json")
    creators = load("creators.json")
    videos = load("videos.json")
    countries = load("countries.json")
    eras = load("eras.json")
    civs = load("civilizations.json")
    before_sites, before_wires = len(sites), sum(len(v) for v in videos.values())

    if CR in creators:
        print(f"  · creator {CR!r} exists")
    else:
        creators[CR] = CREATOR
        print(f"  ✓ added creator {CR!r} (tier 2)")

    names = {s["n"] for s in sites}
    for entry in NEW_SITES:
        s = entry["site"]
        if s["n"] in names:
            print(f"  · site {s['n']!r} exists")
        else:
            sites.append(s)
            names.add(s["n"])
            print(f"  ✓ site {s['n']!r}")
        countries.setdefault(s["n"], entry["country"])
        eras.setdefault(s["n"], entry["era"])
        civs.setdefault(s["n"], entry["civ"])

    for site_name, vid, title, pub in WIRES:
        if site_name not in names:
            sys.exit(f"ABORT: site {site_name!r} not found")
        wires = videos.setdefault(site_name, [])
        if any(v.get("id") == vid for v in wires):
            print(f"  · {vid} already wired to {site_name!r}")
        else:
            w = {"id": vid, "title": title, "cr": CR, "added": ADDED}
            if pub:
                w["published"] = pub
            wires.append(w)
            print(f"  ✓ wired {vid} → {site_name!r}" + (" (badge-eligible)" if pub else ""))

    save("sites.json", sites)
    save("creators.json", creators)
    save("videos.json", videos)
    save("countries.json", countries)
    save("eras.json", eras)
    save("civilizations.json", civs)

    after_wires = sum(len(v) for v in videos.values())
    print(f"\nsites {before_sites} → {len(sites)} | wires {before_wires} → {after_wires} | creators {len(creators)}")
    if after_wires < before_wires:
        sys.exit("ABORT: wires lost")
    if len(sites) < 612:
        sys.exit("ABORT: below documented floor 612")
    print("Next step : python3 scripts/build.py  (SEO pages regenerate automatically)")


if __name__ == "__main__":
    sys.exit(main())
