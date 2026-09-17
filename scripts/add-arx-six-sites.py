#!/usr/bin/env python3
"""
add-arx-six-sites.py — the rest of the ARX Project sweep (2026-09-17)

Follows add-iglesia-vieja-arxproject.py (creator + Iglesia Vieja) and
add-pijijiapan-and-arx-sweep.py (Pijijiapan + wires to Mitla and La Venta).

What this adds :
- 6 new sites : Izapa, Piedras Negras, Río Bec, San Miguel Ixtapan,
                Teotitlán del Valle, Valle de Bravo Petroglyphs
- 17 wires    : all The ARX Project
- aux maps    : country, civilization, era and tags for each

TWO OF THE NINE CANDIDATES ARE HELD, NOT DROPPED. Both fail on the pin,
not on the merit, and the research is recorded here so they drop straight
in when a coordinate turns up:

  GUIRÚN, Oaxaca (EwDaRPB2zQY). A cruciform megalithic chamber, 10 m
  east-west by 8.7 m north-south, walls 2.5 m high, built of 52 blocks,
  the largest about 3.8 x 1.0 x 0.9 m and an estimated 10 tons, unroofed,
  with geometric patterns cut into the interior faces. Documented by
  Marshall Saville in a 1909 report and surveyed without excavation by
  Feinman and Nicholas in 2004. The best location available is "a hilltop
  about 5 km northeast of Xaagá" from a secondary source. Xaagá geocodes
  to 16.90306/-96.32778, but an SRTM sweep of the 4-6 km arc northeast of
  it returns a broad ridge running 2166-2385 m with no single summit to
  choose - candidate points within 200 m of each other in height spread
  over 2 km of ground. That is an inference on an inference, and one
  inferred pin (Pijijiapan) is already one more than this atlas should
  carry. ARX filmed there and would know the coordinate.

  CERRO TEPERUEDA, Juan N. Méndez, Puebla (91EUnpBsTfk). Reported in
  August 2023 after heavy rain exposed four rectangular spaces read as
  ballcourts, mounds to 5 m, and a possible pyramid; registered with INAH
  and watched by municipal forest rangers. Held for two reasons. The hill
  is not geocodable - only the municipal seat is, at 18.54063/-97.74876,
  which is a town and not the site. And the identification is unsettled:
  the press called it the earliest Olmec ceremonial centre in the region,
  and ARX's own title asks whether it is really an Olmec stone pyramid.
  A site whose name, position and culture are all provisional is not one
  this atlas should assert.

NOTES ON THE SIX THAT ARE GOING IN

  Río Bec is in CAMPECHE, Mexico. The video title places it in "the
  jungle of Peten"; its own description says Campeche, and so does every
  source. The desc says Campeche.

  San Miguel Ixtapan absorbs San Francisco Los Nopales (B1p9tMy4wTU,
  n44ZsraXwF8, fEZzw2p4pxc) and the upper Aquiagua canyon survey
  (F3M9DtHJpx0), per Jeff. One slab corpus, one region, one INAH
  director; two records would make both look thinner than the story is.

  Categories follow what each site IS, except where the megalithic
  character is the defining feature. Izapa, Piedras Negras and Río Bec
  are cities. San Miguel Ixtapan is megalithic - the carved slabs are why
  anyone is looking. Teotitlán del Valle is a settlement. Valle de Bravo
  is monolithic; there is no petroglyph category and the carvings are
  worked stone, not ground figures.

  Where a claim belongs to the film rather than the literature the desc
  attributes it. The Tiwanaku comparison at San Miguel Ixtapan is ARX's
  and rests on visual similarity. The Book of Mormon reading of Izapa
  Stela 5 is Jakeman's from the 1950s and is not accepted by Mesoamerican
  archaeology. Valle de Bravo's Teotihuacan-era dating is proposed, not
  established. None of the three is stated as fact.

  Teotitlán del Valle is live work with no published result. It earns a
  record because the question is open, not because it is answered.

Coordinates, each cross-checked against a second source:
  Izapa                 14.9234  -92.1798   es.wiki; en.wiki agrees to 30 m
  Piedras Negras        17.1684  -91.2618   OSM + Nominatim; es.wiki 200 m
  Río Bec               18.3793  -89.3585   Nominatim; en.wiki 700 m
  San Miguel Ixtapan    18.8075 -100.1553   es.wiki zona arqueológica page
  Teotitlán del Valle   17.0292  -96.5200   Wikidata Q7701202 municipal seat
  Valle de Bravo        19.1961 -100.1558   Nominatim, Presa Valle de Bravo

Sites count : 623 → 629.

This script is idempotent — safe to re-run. Run from repo root, then
python3 scripts/build.py
"""
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}
VALID_SIGNAL = {"open", "convergent", None}
CR = "arxproject"

SITES = [
 {"n": "Izapa", "lat": 14.9234, "lng": -92.1798, "cat": "city",
  "region": "Central America", "tier": 2, "criteria": ["scale", "geometry"],
  "desc": (
    "Large Formative centre in the Soconusco of Chiapas, at the foot of "
    "Volcán Tacaná, running about 1.5 km north to south with 161 mapped "
    "mounds, six major plazas and roughly 250,000 cubic metres of "
    "architecture. The whole layout is set 21 degrees east of true north. "
    "Occupied from about 1500 BCE by Mixe-Zoquean groups — the same "
    "language family as the builders of Iglesia Vieja up the coast, and "
    "the family most often connected to the Olmec — with its apogee "
    "between roughly 500 BCE and 100 CE and occupation continuing to "
    "about 1200 CE. Its carved stelae are dense enough that they named a "
    "tradition : the Izapan style turns up along the Pacific piedmont and "
    "into the highlands at Takalik Abaj and Kaminaljuyu, and sits "
    "chronologically and iconographically between Olmec and Maya. Stela 5, "
    "the so-called Tree of Life stone, carries a crowded scene that has "
    "been argued over for seventy years; a 1950s reading by M. Wells "
    "Jakeman took it as a depiction of a Book of Mormon narrative, which "
    "Mesoamerican archaeology has not accepted, while the stone itself "
    "remains genuinely difficult and genuinely important."),
  "aux": {"countries.json": "Mexico",
          "civilizations.json": "Mixe-Zoquean, later Maya",
          "eras.json": -850,
          "tags.json": "mexico chiapas soconusco izapa tuxtla chico stelae izapan "
                       "style mixe-zoque olmec maya tree of life stela 5 tacana"}},

 {"n": "Piedras Negras", "lat": 17.1684, "lng": -91.2618, "cat": "city",
  "region": "Central America", "tier": 2, "criteria": ["scale"],
  "desc": (
    "Yo'k'ib', the great entrance : the largest Maya city of the "
    "Usumacinta basin, on the river's bank inside what is now the Sierra "
    "del Lacandón national park in Petén. Ceramics put occupation from "
    "about 700 BCE, and the city reached its extent and its power between "
    "450 and 810 CE, with a long documented rivalry across the river with "
    "Yaxchilán. Its importance to the field is out of proportion even to "
    "its size. Piedras Negras produced an unusually large body of dated "
    "sculpture, and it was on those stelae that Tatiana Proskouriakoff "
    "showed the inscriptions were recording the births, accessions and "
    "deaths of actual rulers — the step that turned Maya writing from "
    "ornament and calendar into history, and the foundation everything "
    "since has been built on. The site is remote enough that it has stayed "
    "largely unrestored."),
  "aux": {"countries.json": "Guatemala",
          "civilizations.json": "Classic Maya",
          "eras.json": 450,
          "tags.json": "guatemala peten usumacinta piedras negras yokib maya "
                       "stelae proskouriakoff yaxchilan sierra del lacandon"}},

 {"n": "Río Bec", "lat": 18.3793, "lng": -89.3585, "cat": "city",
  "region": "Central America", "tier": 3, "criteria": ["geometry"],
  "desc": (
    "Maya site in southern Campeche — not Petén, despite how it is often "
    "billed — that gave its name to an entire architectural style. The Río "
    "Bec façade is architecture built as illusion. Two solid masonry "
    "towers flank a long range building; the stairways up their faces are "
    "a motif rather than stairs, too steep to climb and leading nowhere; "
    "the temples on top are solid masses with no rooms inside; the "
    "doorways are niches cut to look like doors. The towers narrow as they "
    "rise to fake greater height. The style appears in the 7th century and "
    "runs into the early 12th, spreading to neighbouring sites and sitting "
    "close to the Chenes style to its northwest. Teoberto Maler mentioned "
    "the place at the end of the 19th century without ever going there; "
    "Maurice de Périgny was the first European to reach and report it, and "
    "it was effectively lost again until 1912. A CNRS team under Dominique "
    "Michelet has been mapping and excavating the groups since the 2000s. "
    "Much of it remains unrestored, which is most of its appeal."),
  "aux": {"countries.json": "Mexico",
          "civilizations.json": "Classic Maya (Río Bec style)",
          "eras.json": 700,
          "tags.json": "mexico campeche rio bec maya towers false stairs chenes "
                       "calakmul perigny maler michelet cnrs unrestored"}},

 {"n": "San Miguel Ixtapan", "lat": 18.8075, "lng": -100.1553, "cat": "megalithic",
  "region": "Central America", "tier": 3, "criteria": ["precision", "geometry"],
  "desc": (
    "Ceremonial centre in the Tierra Caliente of the State of México, in "
    "the municipality of Tejupilco, in a part of the country that has "
    "barely been surveyed. Four occupation stages are recognised : Late "
    "Classic 500-700 CE, an Epiclassic apogee 750-900 during Teotihuacán's "
    "decline, Early Postclassic reuse and modification 900-1200, then "
    "abandonment and a Mexica return. The ball court is a double-T, about "
    "50 m by 7.5 m, with a great many richly furnished burials along its "
    "south side, and a carved stone maquette of the site was found here in "
    "1958 — excavation did not begin until 1985. The name is Nahuatl for "
    "the place of salt, and the salt is still worked : hundreds of "
    "monolithic evaporation pans are cut straight into the banks of the "
    "Aquiagua and San Felipe rivers and remain in use. What draws "
    "attention now is a corpus of carved megalithic slabs recovered from "
    "ranches around the village and at San Francisco Los Nopales a few "
    "kilometres away, more than a dozen documented so far, one of them "
    "three tons and one sitting on what appears to be a buried pyramidal "
    "structure. The films argue the precision of their geometric carving "
    "has no Mesoamerican parallel and resembles Tiwanaku work in Bolivia. "
    "That comparison is theirs and rests on visual similarity; no contact "
    "is established. The slabs themselves are real, unexplained in style, "
    "and being rescued one at a time from farmland."),
  "aux": {"countries.json": "Mexico",
          "civilizations.json": "Epiclassic central Mexican (Matlatzinca-related)",
          "eras.json": 750,
          "tags.json": "mexico estado de mexico tejupilco san miguel ixtapan salt "
                       "salinas aquiagua san francisco los nopales megalithic slabs "
                       "carved epiclassic matlatzinca tiwanaku comparison"}},

 {"n": "Teotitlán del Valle", "lat": 17.0292, "lng": -96.5200, "cat": "settlement",
  "region": "Central America", "tier": 3,
  "desc": (
    "Zapotec town in the Tlacolula valley, 31 km from Oaxaca at the foot "
    "of the Sierra Juárez, known in Zapotec as Xaguixe, the place at the "
    "foot of the mountain, and known to everyone else for the wool rugs "
    "woven here on hand looms. It is one of the earliest Zapotec "
    "foundations in the valley and has kept its language. The reason it is "
    "in the atlas is that nobody yet knows what is underneath it. From "
    "2025 a UNAM geophysics team working under INAH has been running "
    "ground-penetrating radar and electrical resistivity tomography across "
    "the municipal square, the churchyard and the nave of the church "
    "itself, looking for the subterranean layout of the Zapotec centre the "
    "living town sits on. This is open work with nothing published. The "
    "record is here for the question, not for an answer."),
  "aux": {"countries.json": "Mexico",
          "civilizations.json": "Zapotec",
          "tags.json": "mexico oaxaca tlacolula teotitlan del valle zapotec xaguixe "
                       "gpr ground penetrating radar resistivity unam inah rugs"}},

 {"n": "Valle de Bravo Petroglyphs", "lat": 19.1961, "lng": -100.1558, "cat": "monolithic",
  "region": "Central America", "tier": 3,
  "desc": (
    "Carvings in the bed of the Presa Miguel Alemán in the State of "
    "México, a reservoir that drowned the valley in 1947. After months of "
    "drought in early 2024 the water fell far enough to expose dozens of "
    "them for the first time in decades : scale models of pyramids and "
    "ceremonial staircases cut into the rock, along with what have been "
    "read as astronomical markers, abstract symbols and figures. A "
    "Teotihuacán-era date, somewhere in the range 200 BCE to 700 CE, has "
    "been proposed for them; it is a proposal rather than a finding. The "
    "site's difficulty is its own : it is only visible when the reservoir "
    "drops, which is exactly why so little work has been done on it, and "
    "why an ordinary drought year is also the only research window."),
  "aux": {"countries.json": "Mexico",
          "civilizations.json": "Central Mexican (Teotihuacán-era, proposed)",
          "tags.json": "mexico estado de mexico valle de bravo presa miguel aleman "
                       "petroglyphs pyramid models reservoir drought carvings"}},
]

WIRES = [
 ("Izapa", "btur88glOys", "Izapa: Mormon Archaeology, Trans-Oceanic Contact, and the Origins of Maya Civilization", "2025-04-26"),
 ("Piedras Negras", "Y7xp7fwxHdI", "Expedition Piedras Negras: Quest for the Hall of Records", "2026-08-23"),
 ("Río Bec", "ICp3zHZW6H4", "We explored a LOST MAYA CITY in the jungle of Peten | Ruins of Rio Bec", "2024-12-23"),
 ("San Miguel Ixtapan", "NouJ2vj4Kbg", "Mysterious Tiwanaku-style Megaliths of Ancient Mexico | ¿Antiguos Contactos entre México y Peru?", "2024-04-13"),
 ("San Miguel Ixtapan", "NipA7ELzeuI", "Ancient MONOLITHIC Salt Evaporation Ponds | Salinas prehispánicas de San Miguel Ixtapan", "2024-11-06"),
 ("San Miguel Ixtapan", "fEZzw2p4pxc", "EXCLUSIVE: New Megalithic finds from San Miguel Ixtapan", "2023-06-18"),
 ("San Miguel Ixtapan", "F3M9DtHJpx0", "We found a lost world in Central Mexico | Vestigios de una civilización desconocida", "2024-07-15"),
 ("San Miguel Ixtapan", "B1p9tMy4wTU", "San Francisco Los Nopales | ARX Project", "2023-02-27"),
 ("San Miguel Ixtapan", "n44ZsraXwF8", "Stone Slab Rescue, Mission 2 — San Francisco Los Nopales, 2023", "2023-05-17"),
 ("San Miguel Ixtapan", "ZECv7ig6JX0", "Stone Slab Rescue, Mission 1 — San Miguel Ixtapan, 2021", "2022-01-06"),
 ("San Miguel Ixtapan", "J1D82Xl-LnE", "San Miguel Ixtapan — ARX Project [ENG]", "2021-10-27"),
 ("Teotitlán del Valle", "NvYlTPpBIxI", "Teotitlan del Valle — Revealing the Cradle of Zapotec Civilization", "2025-07-10"),
 ("Teotitlán del Valle", "gLmNdpgoHDc", "Scanning for LOST ZAPOTEC RUINS | Nuevas investigaciones en Teotitlán del Valle, Oaxaca", "2025-08-07"),
 ("Teotitlán del Valle", "Y-VL5dJQ7ns", "Empieza investigación arqueológica en Teotitlán del Valle, Oaxaca", "2025-07-04"),
 ("Teotitlán del Valle", "yl3ovK5Q1tY", "New Underground Research Project | Teotitlan, the Place of the Gods", "2025-04-20"),
 ("Valle de Bravo Petroglyphs", "XPR6o4kFXcw", "Hallazgo milenario en Valle de Bravo | Pyramids beneath a Mexican Lake", "2024-03-08"),
]
# WtXoE_RX36s is the Spanish cut of J1D82Xl-LnE; not wired, same reason as the
# two Mitla trailers in the previous batch.

def load(n): return json.loads((DATA / n).read_text(encoding="utf-8"))
def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  ✓ wrote data/{n}")

def main():
    cats = load("categories.json")
    ck = set(cats.keys()) if isinstance(cats, dict) else {c.get("key") for c in cats}
    creators = load("creators.json")
    if CR not in creators:
        sys.exit(f"ABORT: creator {CR!r} missing")
    sites = load("sites.json")
    before = len(sites)
    regions = {s["region"] for s in sites}
    names = {s["n"] for s in sites}

    for spec in SITES:
        rec = {k: v for k, v in spec.items() if k != "aux"}
        bad = set(rec.get("criteria", [])) - VALID_CRITERIA
        if bad: sys.exit(f"ABORT: {rec['n']}: invalid criteria {bad}")
        if rec.get("signal") not in VALID_SIGNAL: sys.exit(f"ABORT: {rec['n']}: bad signal")
        if rec["cat"] not in ck: sys.exit(f"ABORT: {rec['n']}: category {rec['cat']!r} undefined")
        if rec["region"] not in regions: sys.exit(f"ABORT: {rec['n']}: region {rec['region']!r} unused elsewhere")
        for s in sites:
            if s["n"] == rec["n"]: continue
            d = math.hypot((s["lat"]-rec["lat"])*111.0,
                           (s["lng"]-rec["lng"])*111.0*math.cos(math.radians(rec["lat"])))
            if d < 1.0: sys.exit(f"ABORT: {rec['n']} lands {d:.2f} km from {s['n']!r}")
        if rec["n"] in names:
            print(f"  · {rec['n']!r} already present.")
        else:
            sites.append(rec); names.add(rec["n"])
            print(f"  ✓ Added {rec['n']!r} ({rec['cat']}, tier {rec['tier']}).")
    save("sites.json", sites)

    for spec in SITES:
        for filename, value in spec["aux"].items():
            m = load(filename)
            if m.get(spec["n"]) == value: continue
            m[spec["n"]] = value
            save(filename, m)

    sites_now = {s["n"] for s in load("sites.json")}
    videos = load("videos.json")
    seen = {v.get("id") for rows in videos.values() for v in rows}
    changed = False
    for target, vid, title, pub in WIRES:
        if target not in sites_now: sys.exit(f"ABORT: target {target!r} missing")
        rows = videos.setdefault(target, [])
        if any(v.get("id") == vid for v in rows):
            print(f"  · {vid} already wired to {target!r}.")
        elif vid in seen:
            sys.exit(f"ABORT: {vid} already wired elsewhere")
        else:
            rows.append({"id": vid, "title": title, "cr": CR,
                         "added": "2026-09-17", "published": pub})
            seen.add(vid); changed = True
            print(f"  ✓ Wired {vid} → {target!r}.")
    if changed: save("videos.json", videos)

    after = len(load("sites.json"))
    print(f"\nsites {before} → {after}")
    if after < before: sys.exit("ABORT: site count dropped")
    print("Next step : python3 scripts/build.py")

if __name__ == "__main__":
    sys.exit(main())
