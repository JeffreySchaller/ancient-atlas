#!/usr/bin/env python3
"""
add-sorcerers-of-stone-sweep-batch.py — Sorcerers of Stone channel sweep (2026-07-09)

Full-channel curation of @sorcerersofstone (Camille Sauve, creator added in
the Naupa Huaca batch). 39 videos reviewed; 29 wired (py2A03eg-q8 already
wired to Naupa Huaca), 8 thematic videos skipped (no single site), 1 skipped
because its site (Huaca Pachacutec, Cusco) has no verifiable coordinates in
any geodata source — do not add that site until coordinates exist.

PHASE 1 — 14 wires to existing sites, including the FIRST wires for
Tambomachay and Saihuite Stone. Run cleanup-peru-duplicates-batch.py FIRST
(the Pisac wire targets the merged entry).

PHASE 2 — 10 NEW Sacred Valley / Cusco sites (all coordinates web-verified
2026-07-09 via Wikipedia/Wikidata/mapcarta; sources in the session log),
with 15 wires and countries/eras/civilizations aux entries. 557 → 567.

Editorial: signal:open only where a genuine open question is documented
(Chinchero's megalithic-course vs Inca-terrace question; Zone X's polished
cuts claim; Temple of the Moon's cave-masonry-predates-Inca claim). Other
entries stay conventional per honesty-over-completeness.

Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CR = "sorcerersofstone"
ADDED = "2026-07-09"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}

# ---------------------------------------------------------------- phase 1
PHASE1_WIRES = [
    ("Sacsayhuamán", "zl6eF77Trbg", "Cusco's Chincanas, Part 4: Sacsayhuaman"),
    ("Sacsayhuamán", "1zmwkgqyd7c", "Ancient Architects of Sacsayhuaman?"),
    ("Sacsayhuamán", "WD7vd5CSvJg", "Re-Imagining Sacsayhuaman: A Fortress or Power Plant?"),
    ("Sacsayhuamán", "pEg0Wn7rv6c", "Mystery at Sacsayhuaman's Water Temple"),
    ("Ollantaytambo", "rxXLg_-a1wY", "Deep Dive Ollantaytambo: Examining the Megalithic Mysteries"),
    ("Ollantaytambo", "Ri1VzrTlPu4", "Deep Dive Ollantaytambo, Part 2"),
    ("Qenqo", "0nvzE9nZhUg", "Cusco's Chincanas, Part 3: Qenko, the Alien-Looking Site"),
    ("Tarawasi", "1m2bn7MccCA", "Amazing New Discovery at Tarawasi!"),
    ("Tarawasi", "YED2EV7oO4k", "Hidden Messages at Tarawasi"),
    ("Machu Picchu", "jRFWrjraVpw", "Strange Machu Picchu: The Mysterious Stones on Circuit 3"),
    ("Pisac", "GWv9q7355tA", "Megalithic Pisac"),
    ("Coricancha (Qorikancha)", "KI9DXw6eqR0", "Ancient Builders of the Qoricancha?"),
    ("Tambomachay", "Auo2lFIxTXU", "Exploring Tambomachay: The Master Engineers of Ancient Peru"),
    ("Saihuite Stone", "fFW0mlKOeug", "Megalithic Sayhuite"),
]

# ---------------------------------------------------------------- phase 2
NEW_SITES = [
    {
        "site": {
            "n": "Chinchero", "lat": -13.3911, "lng": -72.0478,
            "cat": "megalithic", "region": "South America", "tier": 2,
            "signal": "open", "criteria": ["polygonal", "scale"],
            "desc": ("Royal estate of Tupac Inca Yupanqui (~1480 CE) at 3,760 m "
                     "northwest of Cusco, built over an earlier Killke occupation: "
                     "massive agricultural terraces, fine limestone palace walls "
                     "with trapezoidal niches, and carved outcrop huacas scattered "
                     "among the fields — including the ~15 m Teteqaqa stone cut "
                     "with thrones and stairways, a chincana cave, and the boulder "
                     "locals nickname the 'dinosaur stone.' Conventional "
                     "archaeology reads the whole complex as Inca over Killke; the "
                     "open question is the relationship between the heavily "
                     "weathered megalithic huacas and retaining courses and the "
                     "crisp later terracing that surrounds them."),
        },
        "country": "Peru", "era": 1480, "civ": "Inca / Killke",
        "wires": [
            ("604xXIXFl9Q", "Exploring Megalithic Chinchero with Camille Sauve and Al Magdaleno"),
            ("7LiVczDfHVM", "The Chinchero 'Dinosaur' & Ancient Stone Mysteries"),
            ("i3ySGAY7xi4", "Mystery Huacas at Chinchero: Is This a Dinosaur Carved in Ancient Stone?"),
            ("PVyJ6Za9qNU", "Mystery Huacas at Chinchero, Grand Chincana"),
            ("YqnhVfGCGJU", "Exploring Huaca Teteqaqa · Chinchero"),
        ],
    },
    {
        "site": {
            "n": "Teteqaqa (Cusco)", "lat": -13.5149, "lng": -71.9652,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Monumental sculpted limestone outcrop (~40 × 30 m, 26 m "
                     "high) above the Tullumayo valley in Cusco's San Blas "
                     "sector, now engulfed by the city. Thirty-three documented "
                     "carvings include a circular gnomon with channels, thrones, "
                     "carved basins, paccha water channels with serpent-headed "
                     "spouts, and nine high-relief serpents — many deliberately "
                     "demolished during colonial idolatry-extirpation campaigns. "
                     "Recent scholarship identifies the wak'a's original Inca "
                     "name as Chukimarka, a 'second temple of the Sun.'"),
        },
        "country": "Peru", "era": 1450, "civ": "Inca",
        "wires": [("rRwRrLpf_Zs", "Teteqaqa: A Pre-Incan Mystery")],
    },
    {
        "site": {
            "n": "Inkilltambo", "lat": -13.5019, "lng": -71.9524,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Huaca complex carved around a large limestone outcrop "
                     "northeast of Cusco within Sacsayhuamán Archaeological "
                     "Park, attributed to Inca Wiracocha with remodeling under "
                     "Pachacutec. Two narrow carved gallery passages, ceremonial "
                     "niches, rock-hewn altars, staircases and water channels "
                     "sit among fine-masonry enclosures and terraces restored in "
                     "2015-2017. Its 'Inca Cárcel' (jail) nickname misreads the "
                     "cell-like niches — archaeology reads a ceremonial "
                     "sanctuary, parts of which colonial encomenderos "
                     "deliberately destroyed."),
        },
        "country": "Peru", "era": 1420, "civ": "Inca",
        "wires": [("E3JpmGshVvE", "Other Worldly Inkilltambo")],
    },
    {
        "site": {
            "n": "Unu Urqo", "lat": -13.3215, "lng": -71.9845,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Rock sanctuary and terrace complex at the foot of "
                     "Pitusiray mountain near Calca in the Sacred Valley, with "
                     "continuous Killke-to-Inca occupation (~1000-1533 CE). The "
                     "ceremonial sector centers on a carved monolith whose hewn "
                     "water channel runs through the head of a sculpted figure "
                     "and discharges at what reads as a serpent, amphibian or "
                     "puma head — the identity is unresolved. A water-veneration "
                     "festival is still held at the site."),
        },
        "country": "Peru", "era": 1000, "civ": "Killke / Inca",
        "wires": [("64JtbCwOFkM", "Mystery Unu Urqo")],
    },
    {
        "site": {
            "n": "Rumiwasi", "lat": -13.5194, "lng": -71.9403,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("'Stone house' huaca above San Sebastián on Cusco's "
                     "outskirts, combining carved bedrock with andesite "
                     "masonry — polygonal ashlar mixed with cyclopean boulders. "
                     "Features four ritual wall niches, a ~9 m underground "
                     "passage cut through rock, carved steps and a "
                     "water-distribution canal; its alternate name Phaqchayuq "
                     "('the one with the waterfall') reflects ritual water "
                     "associations. Two doorways are reported to align with the "
                     "June and December solstices."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca",
        "wires": [("W5NTBJS4H1I", "Rumiwasi: A Happening Place!")],
    },
    {
        "site": {
            "n": "Amaru Markawasi", "lat": -13.5056, "lng": -71.9647,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Carved limestone cave shrine in the hills northeast of "
                     "Cusco near Qenqo, also known as the Temple of the Moon "
                     "(Cusco) and traditionally linked to lunar and serpent "
                     "(amaru) cults. A natural cleft forms the cave entrance, "
                     "with carved steps descending to sculpted shelves and "
                     "altar-like platforms; hilltop stairways and seats above "
                     "are heavily weathered. Attribution is contested between a "
                     "Killke-built shrine later enhanced by the Inca and a "
                     "purely Inca construction."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca / Killke (disputed)",
        "wires": [("PlTPs7Wzm-I", "Amaru Marca Wasi: The House of the Cave Snake")],
    },
    {
        "site": {
            "n": "Cusilluchayoc", "lat": -13.5084, "lng": -71.9657,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Complex of carved limestone rocks, caves and corridors "
                     "about 500 m east of Qenqo — the 'Temple of the Monkeys.' "
                     "Zoomorphic relief figures read as monkeys, serpents and "
                     "pumas accompany carved walls and stone water channels; "
                     "Spanish extirpators of idolatry chiseled the heads off "
                     "the figures, leaving the popular 'monkey' identification "
                     "an open interpretive question. Offerings are still left "
                     "at a stone locals call the heart of Pachamama."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca",
        "wires": [("7wgimhTJu8g", "Cusco's Surreal Monkey Temple")],
    },
    {
        "site": {
            "n": "Temple of the Moon (Huayna Picchu)", "lat": -13.1517, "lng": -72.5466,
            "cat": "temple", "region": "South America", "tier": 2,
            "signal": "open", "criteria": ["precision", "hardness"],
            "desc": ("Ceremonial complex of top-quality ashlar masonry set into "
                     "an open granite cave (the Great Cavern) on the far side "
                     "of Huayna Picchu, part of Pachacuti's Machu Picchu estate "
                     "and rediscovered in 1936. Inside, fine walls hold a tall "
                     "double-jamb doorway, trapezoidal niches, and a stepped "
                     "throne-like sculpture carved from the living rock. Its "
                     "function is unresolved (shrine, royal tomb, lookout), the "
                     "'Temple of the Moon' name is modern, and the contrast "
                     "between the cave's finest masonry and the surrounding "
                     "work fuels claims that the innermost construction "
                     "predates the Inca."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca",
        "wires": [("Wakzqg0Egrc", "Exploring the Moon Temple at Huayna Picchu")],
    },
    {
        "site": {
            "n": "River Intihuatana", "lat": -13.1756, "lng": -72.5574,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "desc": ("Carved granite huaca on the Urubamba river at the foot of "
                     "the Machu Picchu massif, near the hydroelectric station "
                     "and San Miguel bridge. The bedrock outcrop is sculpted "
                     "with planes, steps and gnomon-like projections, "
                     "associated with fountains, terraces and fine masonry "
                     "forming a riverside sanctuary. Archaeoastronomers "
                     "(Gullberg, Malville) read it as a solstice light-and-"
                     "shadow station ritually linked to Machu Picchu above."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca",
        "wires": [("aX6rl9vQwcs", "The River Intihuatana: An Ancient Megalithic Structure Hidden in the Jungles of Machu Picchu")],
    },
    {
        "site": {
            "n": "Zone X (Cheqtaqaqa)", "lat": -13.4966, "lng": -71.9738,
            "cat": "rock-cut", "region": "South America", "tier": 3,
            "signal": "open", "criteria": ["precision", "machining"],
            "desc": ("Cluster of large carved limestone outcrops northeast of "
                     "Sacsayhuamán — mapped as Zona X / Lanlakuyoc and "
                     "including the Cheqtaqaqa ceremonial sector — cut with "
                     "steps, seats and niches and honeycombed with roughly 15 "
                     "caves and tunnels (chincanas), several showing clear tool "
                     "enhancement. Conventional archaeology reads an Inca "
                     "quarry-and-shrine area with likely earlier Killke ritual "
                     "use; the unusually smooth, near-polished cut surfaces — "
                     "popularized as 'Zone X' by researcher Jesus Gamarra — "
                     "remain the open question. The Cheqtaqaqa sector was "
                     "damaged by graffiti vandalism in March 2026."),
        },
        "country": "Peru", "era": 1450, "civ": "Inca (pre-Inca use claimed)",
        "wires": [
            ("RFJK0o5ekjs", "Cusco's Chincanas, a Not-So-Hidden Secret, Chetaqaqa: Part 1"),
            ("qDao3yUIc9c", "Cusco's Chincanas, Part 2: Zone X"),
        ],
    },
]


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def add_wire(videos, site_name, vid, title):
    wires = videos.setdefault(site_name, [])
    if any(v.get("id") == vid for v in wires):
        print(f"  · {vid} already wired to {site_name!r}")
        return 0
    wires.append({"id": vid, "title": title, "cr": CR, "added": ADDED})
    print(f"  ✓ wired {vid} → {site_name!r}")
    return 1


def main():
    sites = load("sites.json")
    videos = load("videos.json")
    creators = load("creators.json")
    countries = load("countries.json")
    eras = load("eras.json")
    civs = load("civilizations.json")

    if CR not in creators:
        sys.exit(f"ABORT: creator {CR!r} missing — run add-sorcerers-of-stone-naupa-wire.py first")
    before_sites = len(sites)
    if before_sites != 557:
        print(f"  ! note: expected 557 sites pre-run, found {before_sites} (ok if re-run)")

    names = {s["n"] for s in sites}
    added_wires = 0

    print("— Phase 1: wires to existing sites —")
    for site_name, vid, title in PHASE1_WIRES:
        if site_name not in names:
            sys.exit(f"ABORT: existing site {site_name!r} not found (run dupes cleanup first)")
        added_wires += add_wire(videos, site_name, vid, title)

    print("— Phase 2: new sites —")
    for entry in NEW_SITES:
        site = entry["site"]
        bad = set(site.get("criteria", [])) - VALID_CRITERIA
        if bad:
            sys.exit(f"ABORT: invalid criteria {bad} on {site['n']!r}")
        if site["n"] in names:
            print(f"  · site {site['n']!r} already present")
        else:
            sites.append(site)
            names.add(site["n"])
            print(f"  ✓ added site {site['n']!r}")
        for fname, obj, val in (("countries", countries, entry["country"]),
                                ("eras", eras, entry["era"]),
                                ("civilizations", civs, entry["civ"])):
            if obj.get(site["n"]) != val:
                obj[site["n"]] = val
        for vid, title in entry["wires"]:
            added_wires += add_wire(videos, site["n"], vid, title)

    save("sites.json", sites)
    save("videos.json", videos)
    save("countries.json", countries)
    save("eras.json", eras)
    save("civilizations.json", civs)

    print(f"\nsites {before_sites} → {len(sites)} | wires added this run: {added_wires}")
    if len(sites) < before_sites:
        sys.exit("ABORT: count dropped")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
