#!/usr/bin/env python3
"""
add-megaworld-asia-batch.py — MEGAWORLD ASIA cherry-pick batch (2026-07-15)

Channel: MEGAWORLD ASIA (@megaworldasia360, 640K subs) — Southeast Asia
adventure/caving channel with a strong minority of dedicated ancient-site
walkthroughs. Editorial call (Jeff-approved): NOT a full sweep — cherry-pick
only the site-dedicated ancient videos. Screened via channel search; skipped
as non-ancient: Vung Tau French gun batteries (~100 yrs), Cu Chi Tunnels
(20th c.), all caving/waterfall/loop content.

NEW CREATOR: megaworldasia (tier 2)
NEW SITE (1): Preah Vihear (Khmer clifftop temple, Dangrek Mountains,
  Cambodia; 9th–12th c., Suryavarman I & II; 800 m five-gopura axis at 625 m
  elevation; UNESCO 2008; coords per Wikipedia infobox 14.3911, 104.6803).
WIRES (10) — Vat Phou (6th, first non-Secrets-in-Stone voice), Plain of Jars
  (2nd), Koh Ker, Angkor Wat, Bayon Temple, Ta Prohm (2nd), Kbal Spean +
  Banteay Srei (one video covers both, Bedse/Barabar precedent),
  Preah Khan of Kompong Svay, Preah Vihear (new).
Wat Phou wire carries its TRUE publish date (2025-11-23) → "New to the
Atlas" badge in the hub Recent rail (debut-highlight lever).

615 → 616 sites · 65 → 66 creators · 946 → 956 wires. Floor: 616.
Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CR = "megaworldasia"
ADDED = "2026-07-15"

CREATOR = {
    "name": "MEGAWORLD ASIA",
    "handle": "@megaworldasia360",
    "subs": "640K subs · Southeast Asia off-the-beaten-track field documentaries · Khmer temples, Laos, Cambodia",
    "color": "#C77B3F",
    "tier": 2,
}

NEW_SITE = {
    "site": {
        "n": "Preah Vihear", "lat": 14.3911, "lng": 104.6803,
        "cat": "temple", "region": "Asia", "tier": 2,
        "desc": "Khmer temple perched on a 625 m clifftop in the Dangrek Mountains on the Cambodia–Thailand border, laid out along an extraordinary 800 m north–south axis of five gopuras, causeways and courtyards climbing to a sanctuary at the cliff edge. Begun in the early 9th century with most construction under Suryavarman I and Suryavarman II (11th–12th centuries), it is considered the most dramatically sited of all Khmer monuments; UNESCO-listed in 2008 and long the object of a border dispute settled at the ICJ.",
    },
    "country": "Cambodia", "era": 1050, "civ": "Khmer Empire",
}

# (site, id, title, published-or-None)
WIRES = [
    ("Vat Phou", "kZNPjP8FtRk", "WAT PHOU: Secrets of the Ancient Khmer Temple on the Mekong", "2025-11-23"),
    ("Plain of Jars", "2z73rYeHnhY", "PLAIN OF JARS: Mysterious Ancient Jars Hidden in Laos", None),
    ("Koh Ker", "_G4RzGZRl-A", "KOH KER: 36 Meters High and Completely Off the Beaten Path", None),
    ("Angkor Wat", "PdyvOXTOVOE", "Discover the Marvels of Angkor Wat: The Ultimate Temple Experience in 4K", None),
    ("Bayon Temple", "PQOLL2bclnU", "THE BAYON: Angkor's Strangest Temple — Mesmerizing Four-Faced Stupas", None),
    ("Ta Prohm", "ntLaixzCz34", "TA PROHM: Golden Hour at Ta Prohm — Photography Gold in the Jungle", None),
    ("Kbal Spean (Valley of a Thousand Lingams)", "4pWx9w8AU1A", "KBAL SPEAN & BANTEAY SREY: Hidden Angkor Temples | Off the Beaten Track", None),
    ("Banteay Srei", "4pWx9w8AU1A", "KBAL SPEAN & BANTEAY SREY: Hidden Angkor Temples | Off the Beaten Track", None),
    ("Preah Khan of Kompong Svay", "1uOd1oFYnfI", "Inside PREAH KHAN KOMPONG SVAY's Overgrown Stone City", None),
    ("Preah Vihear", "7DQRiEe8isQ", "PREAH VIHEAR TEMPLE: The Most Dangerous Temple Access in Cambodia", None),
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
    s = NEW_SITE["site"]
    if s["n"] in names:
        print(f"  · site {s['n']!r} exists")
    else:
        sites.append(s)
        names.add(s["n"])
        print(f"  ✓ site {s['n']!r}")
    countries.setdefault(s["n"], NEW_SITE["country"])
    eras.setdefault(s["n"], NEW_SITE["era"])
    civs.setdefault(s["n"], NEW_SITE["civ"])

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
    if len(sites) < 615:
        sys.exit("ABORT: below documented floor 615")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
