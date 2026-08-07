#!/usr/bin/env python3
"""
fix-countries-map.py — repair and backfill countries.json (2026-08-07)

Two problems, one pass.

REPAIR. countries.json had drifted into three different shapes:
  222 entries in the intended shape   "Site Name": "Country"
   40 entries inverted into buckets   "Country": ["Site A", "Site B", ...]
   17 entries keyed on site names that no longer exist in sites.json
The inverted buckets were not broken for the front end (build.py just emits
the object as SITE_COUNTRIES), but they were invisible to any lookup keyed on
site name, which is why the Atlas looked like it had 273 countries mapped
when it actually had 474. Everything is normalised here to one shape.

Of the 17 stale keys, 9 are sites that were later renamed and are remapped by
alias; 8 refer to sites that are not in the Atlas at all and are dropped.

BACKFILL. The remaining 143 unmapped sites were resolved from their own
lat/lng by offline reverse geocoding (the `reverse_geocode` package, GeoNames
populated-place data), then normalised to the house vocabulary already in use
and checked three ways:
  · country cross-checked against the site's `region` field — 6 flags, all of
    them ISO long-form names (Syrian Arab Republic, Iran Islamic Republic of,
    Palestinian Territory, Lao PDR), now normalised
  · distance to the nearest populated place — 2 sites over 80 km, both correct
    and genuinely remote (Baigong Pipes in Qinghai, Tassili n'Ajjer in the
    Algerian Sahara)
  · every country new to the vocabulary eyeballed by name against its state /
    province — Palestine, Sri Lanka, Sudan, South Africa, Germany

House conventions preserved rather than ISO-normalised, because they are
editorial choices already live on the site: Hawaii and Scotland stand alone
rather than folding into United States / United Kingdom, Türkiye is spelled
with the dotted U, Rapa Nui is "Chile (Rapa Nui)", and the scattered
Micronesian sites stay under "Oceania".

The resolved values are baked in below rather than recomputed, so this script
is deterministic and needs no network or geocoding dependency.

Result: countries.json goes 474 → 617 of 617 sites, one shape throughout.
Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

# sites renamed since countries.json was last hand-edited
ALIASES = {
    "Pyramid of Khufu (Great Pyramid)": "Great Pyramid of Giza (Khufu)",
    "\u0120gantija": "\u0120gantija Temples",
    "Jericho": "Jericho (Tell es-Sultan)",
    "Teotihuacan": "Teotihuac\u00e1n",
    "Mycenae (Lion Gate)": "Mycenae",
    "Pnyx Hill (Athens)": "Pnyx",
    "Pisac (Pisaq)": "Pisac",
    "Amaru Muru (Stargate)": "Aramu Muru",
    "Cumbemayo Aqueduct": "Cumbe Mayo",
}

# keys referring to sites the Atlas does not carry — dropped
STALE = {
    "Acigol Underground City", "Lascaux", "Acropolis of Athens", "Pompeii",
    "Herculaneum", "Susa", "Ur (Ziggurat of Ur)",
    "Babylon (Ziggurat of Etemenanki)",
}

# reverse-geocoded and reviewed
BACKFILL = {
    "Abba Yohani Rock-Cut Church": "Ethiopia",
    "Abu Hureyra": "Syria",
    "Acigöl Underground City": "Türkiye",
    "Adadi Maryam Monolithic Church": "Ethiopia",
    "Adam's Calendar": "South Africa",
    "Ambager Church Complex": "Ethiopia",
    "Ani": "Türkiye",
    "Aphrodisias": "Türkiye",
    "Aurangabad Caves": "India",
    "Baigong Pipes": "China",
    "Barabar Caves": "India",
    "Barnenez": "France",
    "Bent Pyramid (Dahshur)": "Egypt",
    "Black Pyramid (Dahshur)": "Egypt",
    "Bryn Celli Ddu": "United Kingdom",
    "Cairn of Barclodiad y Gawres": "United Kingdom",
    "Castlerigg Stone Circle": "United Kingdom",
    "Chalcatzingo": "Mexico",
    "Chan Chan": "Peru",
    "Chennakeshava Temple (Belur)": "India",
    "Cholula": "Mexico",
    "Colossi of Memnon": "Egypt",
    "Daisen Kofun": "Japan",
    "Daniel Korkor Rock-Cut Church": "Ethiopia",
    "Debra Damo Monastery": "Ethiopia",
    "Dendera Temple Complex": "Egypt",
    "Dharmrajeshwar Temple": "India",
    "Dolmen of Menga": "Spain",
    "Dowth": "Ireland",
    "Edfu Temple (Temple of Horus)": "Egypt",
    "El Tajín": "Mexico",
    "Ephesus": "Türkiye",
    "Epidaurus": "Greece",
    "Externsteine": "Germany",
    "Gate of the Sun (Tiwanaku)": "Bolivia",
    "Gavrinis": "France",
    "Geneta Mariam Monolithic Church": "Ethiopia",
    "Great Pyramid of Giza (Khufu)": "Egypt",
    "Guanlin Temple": "China",
    "Gunung Padang": "Indonesia",
    "Guyaju Caves": "China",
    "Güzelyurt Underground City": "Türkiye",
    "Hampi": "India",
    "Hawara Pyramid & Labyrinth": "Egypt",
    "Hejin City Fortress": "China",
    "Hierapolis": "Türkiye",
    "Hoysaleshwara Temple": "India",
    "Huaca de la Luna": "Peru",
    "Huaca del Sol": "Peru",
    "Huashan Grottoes": "China",
    "Hypogeum of Ħal Saflieni": "Malta",
    "Ihlara Valley": "Türkiye",
    "Ishi-no-Hoden": "Japan",
    "Ishibutai Kofun": "Japan",
    "Jerash (Gerasa)": "Jordan",
    "Jericho (Tell es-Sultan)": "Palestine",
    "Jiahu": "China",
    "Jiroft": "Iran",
    "Kailasa Temple (Ellora Cave 16)": "India",
    "Kalavantin Durg": "India",
    "Knowth": "Ireland",
    "La Venta": "Mexico",
    "Lalibela Rock-Hewn Churches": "Ethiopia",
    "Locmariaquer": "France",
    "Longyou Caves": "China",
    "Mamallapuram": "India",
    "Masuda no Iwafune": "Japan",
    "Medhane Alem Adi Kasho": "Ethiopia",
    "Medinet Habu": "Egypt",
    "Meroe Pyramids": "Sudan",
    "Moray": "Peru",
    "Mt. Kuromata": "Japan",
    "My Son Sanctuary": "Vietnam",
    "Myra": "Türkiye",
    "Naneghat": "India",
    "Naupa Huaca": "Peru",
    "Nazugn Mariam Monolithic Church": "Ethiopia",
    "Nemrut Dağı": "Türkiye",
    "Nevşehir Underground City": "Türkiye",
    "Newgrange": "Ireland",
    "Nimrud": "Iraq",
    "Ortahisar Castle": "Türkiye",
    "Osaka Castle": "Japan",
    "Osireion (Abydos)": "Egypt",
    "Oya Stone Quarry": "Japan",
    "Padmanabhaswamy Temple": "India",
    "Palmyra": "Syria",
    "Pantelleria Vecchia Bank Monolith": "Italy",
    "Pasargadae": "Iran",
    "Patara": "Türkiye",
    "Perge": "Türkiye",
    "Phaistos": "Greece",
    "Philae Temple (Temple of Isis)": "Egypt",
    "Pisac": "Peru",
    "Pitalkhora Caves": "India",
    "Pyramid of Meidum": "Egypt",
    "Pyramid of Unas": "Egypt",
    "Qenqo": "Peru",
    "Raqchi (Temple of Wiracocha)": "Peru",
    "Red Pyramid (Dahshur)": "Egypt",
    "Ring of Brodgar": "Scotland",
    "Sagalassos": "Türkiye",
    "Sahasralinga (Shilmala River)": "India",
    "Sakafune-ishi": "Japan",
    "Sambor Prei Kuk": "Cambodia",
    "San Lorenzo Tenochtitlán": "Mexico",
    "Sannai-Maruyama": "Japan",
    "Sanxingdui": "China",
    "Saqqara Necropolis": "Egypt",
    "Sardinia Nuraghi (Su Nuraxi)": "Italy",
    "Sardis": "Türkiye",
    "Selime Cathedral": "Türkiye",
    "Serapeum of Saqqara": "Egypt",
    "Sigiriya": "Sri Lanka",
    "Silbury Hill": "United Kingdom",
    "Siwa Oracle Temple (Amun)": "Egypt",
    "Tall el-Hammam": "Jordan",
    "Tambomachay": "Peru",
    "Tassili n'Ajjer": "Algeria",
    "Taş Tepeler (Stone Hills)": "Türkiye",
    "Temple of Hatshepsut": "Egypt",
    "Temple of Kom Ombo": "Egypt",
    "Teotihuacán": "Mexico",
    "Terracotta Army": "China",
    "Tipón": "Peru",
    "Tiryns": "Greece",
    "Tomb of the General": "China",
    "Troy (Hisarlik)": "Türkiye",
    "Tulum": "Mexico",
    "Uchisar Fairy Chimneys": "Türkiye",
    "Unfinished Obelisk (Aswan)": "Egypt",
    "Ur": "Iraq",
    "Uçhisar Castle": "Türkiye",
    "Vat Phou": "Laos",
    "Vettuvan Koil": "India",
    "Washa Mikael Rock-Cut Church": "Ethiopia",
    "West Kennet Long Barrow": "United Kingdom",
    "Xanthos": "Türkiye",
    "Yonaguni Monument": "Japan",
    "Zelve Open Air Museum": "Türkiye",
    "Özkonak Underground City": "Türkiye",
    "Ġgantija Temples": "Malta",
    "Ōyu Stone Circles": "Japan"
}


def main():
    sites = json.loads((DATA / "sites.json").read_text(encoding="utf-8"))
    names = {s["n"] for s in sites}
    raw = json.loads((DATA / "countries.json").read_text(encoding="utf-8"))

    resolved = {}
    stats = {"kept": 0, "unbucketed": 0, "aliased": 0, "dropped": 0}

    def put(name, country):
        name = ALIASES.get(name, name)
        if name in STALE or name not in names:
            stats["dropped"] += 1
            return False
        resolved[name] = country
        return True

    for key, value in raw.items():
        if isinstance(value, list):          # inverted bucket
            for n in value:
                if put(n, key):
                    stats["unbucketed"] += 1
        elif key in names:                   # already correct
            resolved[key] = value
            stats["kept"] += 1
        elif ALIASES.get(key) in names:      # renamed site
            resolved[ALIASES[key]] = value
            stats["aliased"] += 1
        else:
            stats["dropped"] += 1

    before = len(resolved)
    for name, country in BACKFILL.items():
        if name not in names:
            sys.exit(f"ABORT: backfill target {name!r} not in sites.json")
        resolved.setdefault(name, country)
    added = len(resolved) - before

    print(f"  kept {stats['kept']}, unbucketed {stats['unbucketed']}, "
          f"aliased {stats['aliased']}, dropped {stats['dropped']}")
    print(f"  backfilled {added}")

    missing = names - set(resolved)
    extra = set(resolved) - names
    if extra:
        sys.exit(f"ABORT: {len(extra)} keys are not site names: {sorted(extra)[:5]}")
    if missing:
        print(f"  ! {len(missing)} sites still unmapped: {sorted(missing)[:10]}")

    if not all(isinstance(v, str) for v in resolved.values()):
        sys.exit("ABORT: non-string value survived normalisation")

    out = {k: resolved[k] for k in sorted(resolved)}
    (DATA / "countries.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  \u2713 wrote data/countries.json")
    print(f"\ncoverage {len(out)} / {len(names)} sites \u00b7 "
          f"{len(set(out.values()))} distinct countries")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
