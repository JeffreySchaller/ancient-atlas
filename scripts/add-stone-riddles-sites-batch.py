#!/usr/bin/env python3
"""
add-stone-riddles-sites-batch.py — Stone Riddles sweep, part 2 (2026-07-11)

47 NEW sites + 50 wires from the @StoneRiddles catalog, in four researched
clusters (all coordinates web-verified 2026-07-11 via Wikipedia/Wikidata/
mapcarta/topostext/nurnet; research agents' sources in session log):
Crete (7) · Central Greece (6) · NW Greece + Argolid (11) · Sardinia (17) ·
Italy (6). 565 → 612.

Editorial skips (documented): Giant's grave of Uore + its disputed 'holy
well' (NO verifiable coordinates); 'Black Pyramid' of Poggio Conte (natural
rock formation below a 13th-c. hermitage — not an ancient monument);
Meteora (natural pillars); 4 thematic/documentary videos.

Notable: the 'ruins of Ogas' video resolved to Acropolis Oga on Methana —
an unexcavated fortress unnamed in ancient sources; flagged signal:open.
signal:open applied with restraint per editorial bar + the Mohs≥6 hardness
rule (Santu Antine's basalt ashlar; S'Ena e Thomes' 7-ton shaped granite
stele). Run AFTER add-stone-riddles-quickwins-batch.py. Idempotent.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CR = "stoneriddles"
ADDED = "2026-07-11"
VALID = {"precision", "polygonal", "scale", "hardness", "stratigraphy", "geometry", "machining"}


def S(n, lat, lng, cat, tier, desc, signal=None, criteria=None):
    d = {"n": n, "lat": lat, "lng": lng, "cat": cat, "region": "Europe", "tier": tier, "desc": desc}
    if signal:
        d["signal"] = signal
        d["criteria"] = criteria
    return d


NEW = [
    # ---------------- CRETE ----------------
    dict(site=S("Hyrtakina", 35.2797, 23.7515, "megalithic", 3,
        "Remote Dorian city on Kastri hill in southwest Crete, defended by polygonal masonry walls roughly half a mile long forming two 'cyclopic' circuits, with gate passages protected by projecting flanking walls. A temple of Pan stood on the acropolis; the east and south sides rely on sheer terrain."),
        country="Greece", era=-300, civ="Dorian Cretan",
        wires=[("uCQlsruon8s", "Mysterious Walls at Hyrtakina")]),
    dict(site=S("Polyrrhenia", 35.4580, 23.6556, "city", 3,
        "Amphitheatre-like acropolis city above Kissamos in northwest Crete, its fortification walls still standing 3-5.5 m high in a mix of Hellenistic coursed work and later rebuilds over older masonry. Rock-cut chambers and cisterns honeycomb the hill, with a temple of Dictynna and a Hadrianic aqueduct."),
        country="Greece", era=-600, civ="Dorian Cretan",
        wires=[("FxSgUJVt7gk", "The Acropolis of Ancient Polyrrhenia")]),
    dict(site=S("Falasarna", 35.5103, 23.5675, "city", 2,
        "The best-preserved ancient closed war harbour in Crete: an artificial basin ringed by cut-stone quays with mooring bollards still bearing rope marks, linked to the sea by chain-closable channels and guarded by dressed-stone towers. Tectonic uplift of ~6.5 m — most scholars blame the great AD 365 earthquake — left the entire harbour stranded 100 m inland, a stone throne possibly of Astarte beside it."),
        country="Greece", era=-500, civ="Greek (Cretan maritime city-state)",
        wires=[("RT4VQAa1b6U", "The Closed Harbour of Falasarna")]),
    dict(site=S("Aptera", 35.4626, 24.1415, "city", 2,
        "Large city-state on a plateau commanding Souda Bay, attested as A-pa-ta-wa in Linear B and enclosed by a fortification circuit of which about 4 km survives in fine polygonal and coursed Hellenistic masonry. Inside are Doric temples, a theatre, huge three-vaulted Roman cisterns and baths; the city was famed for its mercenary archers."),
        country="Greece", era=-700, civ="Dorian Cretan (Minoan/Mycenaean antecedents)",
        wires=[("_LPW4WiEuLg", "4 km of Polygonal Walls at Aptera!")]),
    dict(site=S("Lato", 35.1778, 25.6536, "city", 2,
        "One of Crete's best-preserved Classical stone cities, saddled between twin acropolis peaks above Mirabello Bay. Its stepped agora, prytaneion, temple and terraced houses are built of large roughly dressed limestone blocks in massive polygonal-to-trapezoidal drystone style on cyclopean-looking terrace walls; the settlement is thought to predate the Dorian arrival."),
        country="Greece", era=-500, civ="Dorian Cretan",
        wires=[("jEbUvHHZWBA", "The Stone City of Lato")]),
    dict(site=S("Stylos Tholos Tomb", 35.4495, 24.1272, "tomb", 3,
        "Monumental corbel-vaulted tholos tomb of a Late Minoan III ruler on Azoires hill south of Aptera, approached by an exceptionally long stone-built dromos of 20.8 m with a Mycenaean-style relieving triangle above the entrance. Hellenistic cups found in the triangle show ceremonies continued at the looted tomb a millennium after construction."),
        country="Greece", era=-1300, civ="Minoan (Late Minoan III)",
        wires=[("OwWF4lpCCdA", "The Vaulted Tomb of Stylos")]),
    dict(site=S("Kamilari Tholos Tomb", 35.0454, 24.7869, "tomb", 3,
        "The best-preserved Mesara-type circular tholos tomb, its drystone wall of large roughly shaped stones still standing about 2 m high around a chamber 7.6 m across, with five annex chambers and an offering area that yielded some 500 inverted vessels. Three famous clay models — circle dancers, offering bearers, a banquet with horns of consecration — came from the tomb."),
        country="Greece", era=-1900, civ="Minoan (Mesara tholos tradition)",
        wires=[("uHNtyaIc51Q", "The Tholos Tomb of Kamilari")]),
    # ---------------- CENTRAL GREECE ----------------
    dict(site=S("Eleutherai Fortress", 38.1794, 23.3758, "megalithic", 2,
        "One of the best-preserved fortresses of ancient Greece, guarding the Kaza pass between Attica and Boeotia: an 860 m circuit of superb coursed trapezoidal ashlar averaging 2.6 m thick, with six towers still standing 4-6 m high along the north side. Excavation identified an earlier polygonal-masonry phase beneath the Classical walls, and whether Athens or Boeotia built the fort is still argued."),
        country="Greece", era=-370, civ="Classical Greek (Attic-Boeotian frontier)",
        wires=[("VIpMXqxD50Q", "Exquisitely Preserved Walls at Eleutherai")]),
    dict(site=S("Siphai (Tipha)", 38.1900, 23.0529, "megalithic", 3,
        "Fortified harbour town of the Boeotian coast — mythical home of Tiphys, pilot of the Argo — whose late-4th-century BC ashlar circuit follows a rocky spine down into the Corinthian Gulf, leaving wall footings and a monumental building partly submerged. Two gates flanked by artillery towers survive, and traces of a protective sea mole lie in the anchorage; the underwater works have never been investigated."),
        country="Greece", era=-350, civ="Boeotian Greek",
        wires=[("R-OZrCgyRuU", "Walls in the Sea at Siphai")]),
    dict(site=S("Panopeus", 38.4950, 22.7950, "megalithic", 3,
        "Acropolis above Agios Vlasios celebrated since the 19th century as a textbook example of fine polygonal masonry, with curtains standing 5-6 m high and one tower reaching 9 m. Pausanias noted the town had no agora or theatre — its fame rested on the walls and the clay 'of which Prometheus moulded men.' The polygonal work looks archaic, yet the standing circuit is conventionally dated after the 346 BCE destruction, leaving the relationship between older polygonal sections and the rebuild an open question.",
        signal="open", criteria=["polygonal", "stratigraphy"]),
        country="Greece", era=-400, civ="Phocian Greek",
        wires=[("8MfM9WVc77A", "Polygonal and Megalithic Stones at Panopeus")]),
    dict(site=S("Orchomenos (Boeotia)", 38.4931, 22.9747, "city", 2,
        "Minyan and Mycenaean centre that rivalled Thebes, anchored by the Treasury of Minyas — a monumental tholos tomb rivalling the Treasury of Atreus, with a ~6 m monolithic inner lintel and a side chamber whose ceiling slab is carved with spirals and floral relief. Above rise 4th-century BC fortification walls on Mt. Akontion; Mycenaean Orchomenos also engineered the draining of Lake Copais, the largest lake in Greece."),
        country="Greece", era=-1250, civ="Minyan / Mycenaean",
        wires=[("a91ukD2vy3s", "The Wonders of Orchomenos"), ("cVlboPnBbm0", "The Majestic Treasury of Minyas")]),
    dict(site=S("Lilaia", 38.6260, 22.5060, "megalithic", 3,
        "Towered acropolis above the springs of the Cephissus river in Phocis, its 4th-century BC circuit built in trapezoidal masonry with rectangular towers still standing to substantial height, commanding the entire upper valley. Traces of earlier fortification survive at the summit; Pausanias saw temples of Apollo and Artemis with Pentelic-marble statues of Athenian workmanship."),
        country="Greece", era=-350, civ="Phocian Greek",
        wires=[("dZ7SHYP8Td0", "The Towers of Lilaia")]),
    dict(site=S("Proerna", 39.2435, 22.2731, "megalithic", 3,
        "Fortified acropolis at Neo Monastiri in Achaean Phthiotis, its Hellenistic circuit built as two faces of firmly jointed trapezoidal grey limestone with headers between sets of stretchers, the south flank surviving eight courses (~4.2 m) high. Open drains through the outer face manage rainwater — systematic Hellenistic military engineering; the sanctuary of Demeter Proernia lies below."),
        country="Greece", era=-350, civ="Thessalian / Achaean Phthiotis Greek",
        wires=[("1Eihw8GtnEk", "The Walls at the Acropolis of Proerna")]),
    # ---------------- NW GREECE + ARGOLID ----------------
    dict(site=S("Dodona", 39.5464, 20.7878, "temple", 2,
        "Reputedly the oldest Hellenic oracle, centred on the sacred oak of Zeus below Mt. Tomaros, with cult activity from the Late Bronze Age and over 4,200 inscribed oracular lead tablets recovered. The great Hellenistic theatre built under Pyrrhus (~17,000 seats) is among the largest in Greece; a fortified acropolis of coursed trapezoidal-polygonal limestone crowns the sanctuary. How the divination actually worked — rustling oak leaves, resonating bronze cauldrons, or doves and priestesses — is still debated."),
        country="Greece", era=-800, civ="Epirote Greek",
        wires=[("sU8YyTARPuQ", "The Ancient Oracle of Dodona")]),
    dict(site=S("Cassope", 39.1451, 20.6733, "city", 2,
        "A complete Hippodamian grid city on a high terrace under the Zalongo cliffs overlooking the Ambracian Gulf, founded in the mid-4th century BC as capital of the Kassopaians. Its fortifications and terrace works are laid in polygonal and trapezoidal grey limestone; the theatre, odeion, prytaneion and a 180-room hostel survive. Abandoned in 31 BC when Rome moved the population to Nikopolis."),
        country="Greece", era=-360, civ="Epirote Greek (Kassopaians)",
        wires=[("WhXLtIJmvRg", "The Polygonal City of Cassope")]),
    dict(site=S("Oiniades", 38.4118, 21.1948, "city", 2,
        "Marsh-girt hill city on the lower Acheloos with a 5.5 km circuit regarded as one of the finest displays of polygonal masonry in Greece — tightly jointed curvilinear limestone following the crag line, its gates roofed with corbelled and true voussoir arches, among the earliest Greek arch construction. The naval installation preserves rock-cut shipsheds with colonnaded slipways rising from the silted ancient harbour."),
        country="Greece", era=-450, civ="Acarnanian Greek",
        wires=[("0Bp4pCUIxFw", "Unique Polygonal Vaulted Arch at Oiniades")]),
    dict(site=S("New Pleuron", 38.4144, 21.4097, "city", 2,
        "Superbly preserved Hellenistic city on Mt. Arakynthos above Missolonghi, founded c. 230 BCE after Macedon destroyed Old Pleuron: a 2.4 km rectangular circuit with 31 towers and 7 gates in large drafted limestone blocks, standing in places to full curtain height. Inside are a theatre built against the city wall, a 62 m stoa, and a monumental five-basin communal cistern."),
        country="Greece", era=-230, civ="Aetolian Greek",
        wires=[("4vxuZMiKyik", "Massive Walls and Unusual Constructions at New Pleuron")]),
    dict(site=S("Methana Acropolis (Palaiokastro)", 37.5867, 23.3494, "megalithic", 3,
        "Small fortified acropolis on a coastal lava dome of the volcanic Methana peninsula, its walls built of local andesite and dacite in rough megalithic style, first raised in Mycenaean times and rebuilt into the Byzantine era. The ancient town of Methana spreads around its foot, with the sanctuaries of Isis and Hermes recorded by Pausanias nearby."),
        country="Greece", era=-1300, civ="Mycenaean, then Classical Greek",
        wires=[("0YucYn8-6F8", "The Acropolis of Methana")]),
    dict(site=S("Kazarma Acropolis", 37.5969, 22.9427, "megalithic", 3,
        "Steep fortress hill on the ancient Argos-Epidaurus road, its circuit walls 2.5 m thick and up to 5.2 m high in huge tightly fitted polygonal/cyclopean blocks with four round towers. Directly below runs the Mycenaean highway with the Arkadiko bridge — the best-preserved Cyclopean corbel-arch bridge in the world, still in use after ~3,300 years. How much walling is genuinely Mycenaean versus 4th-century BC Argive polygonal rebuild is still discussed, and the site's ancient name is unresolved.",
        signal="open", criteria=["polygonal", "stratigraphy"]),
        country="Greece", era=-1300, civ="Mycenaean / Classical Argive",
        wires=[("p-fGEVNiMbk", "Little Known Polygonal Walls at Kazarma")]),
    dict(site=S("Agios Adrianos Fort", 37.5999, 22.8453, "megalithic", 3,
        "Compact Hellenistic fort on the Palaiokastro hill east of Agios Adrianos village in the Argolid, built of grey limestone in fine polygonal masonry: a 50 × 26 m enclosure with a square keep surviving three storeys high, entered through a gate with a 2.1 m monolithic lintel. It guarded the Argos-Epidaurus route and remains essentially unexcavated since trial digs in 1890."),
        country="Greece", era=-320, civ="Hellenistic Greek (Argive)",
        wires=[("2Dust-UkG9M", "Beautiful Polygonal Walls at Agios Adrianos")]),
    dict(site=S("Asine", 37.5280, 22.8745, "megalithic", 3,
        "Triangular rocky headland rising straight from the sea beside Tolo, ringed by fortification walls of cyclopean character heavily rebuilt around 300 BCE — massive roughly polygonal limestone with a large landward bastion. Swedish excavations from 1922 revealed Early Helladic houses, Mycenaean remains and a Geometric town; attributing individual wall stretches between the Bronze Age circuit and the Hellenistic refortification remains difficult."),
        country="Greece", era=-1300, civ="Mycenaean / Hellenistic Greek",
        wires=[("82mjHuq-A_U", "The Seaside Polygonal Walls of Asine")]),
    dict(site=S("Midea", 37.6499, 22.8417, "megalithic", 2,
        "The third great cyclopean citadel of the Argolid after Mycenae and Tiryns, crowning a 268 m conical hill: its circuit of enormous unworked and hammer-dressed conglomerate boulders runs ~450 m with walls 5-7 m thick and two gates. Terraces inside carried megaron-type buildings that yielded Linear B; the rich Dendra cemetery (source of the Dendra panoply) was its necropolis. Whether earthquake or attack destroyed it c. 1200 BCE is debated."),
        country="Greece", era=-1300, civ="Mycenaean",
        wires=[("q8MVH0-EosY", "The Cyclopean Walls of Midea")]),
    dict(site=S("Heraion of Argos", 37.6919, 22.7747, "temple", 2,
        "Grand terraced sanctuary of Hera stepping down a spur of Mt. Euboea above the Argive plain, its uppermost Old Temple terrace retained by a monumental wall of huge unmortared conglomerate blocks in 'cyclopean' style — larger even than true Mycenaean work. Long mistaken for genuine Bronze Age construction, the terrace is argued to be an Iron Age/Archaic imitation consciously evoking the Mycenaean past — a documented open question of archaizing masonry.",
        signal="open", criteria=["scale", "stratigraphy"]),
        country="Greece", era=-700, civ="Archaic-Classical Greek (Argive)",
        wires=[("mBfZCWeqvyE", "The Heraion Sanctuary Near Argos")]),
    dict(site=S("Acropolis Oga (Methana)", 37.6172, 23.4118, "megalithic", 3,
        "Flat-topped volcanic height on the northern Methana peninsula preserving stretches of ancient fortification in large roughly fitted volcanic stone, a tower stump and a cistern. Mentioned by no ancient author and never excavated, it is dated only by the broadly Classical-Hellenistic look of the walls; an inscription from the site names a sanctuary of Poseidon Phytalios. Virtually everything about it — date, name, function — remains open.",
        signal="open", criteria=["stratigraphy"]),
        country="Greece", era=None, civ="Ancient Greek (unattributed)",
        wires=[("d9sLt8szPGU", "The Mysterious Ruins of Ogas")]),
    # ---------------- SARDINIA ----------------
    dict(site=S("Nuraghe Santu Antine", 40.4865, 8.7698, "megalithic", 2,
        "The finest of Sardinia's nuraghi: a basalt keep 15.5 m across, preserved to 17.5 m (originally ~23 m), with three superimposed corbel-vaulted tholos chambers linked by a helical stone staircase, enclosed in a triangular bastion with corner towers and loopholed corridors. Whether the great nuraghi were fortresses, chiefly residences or ceremonial centres is still debated, and claimed solstitial alignments remain contested — the hardness and regularity of the basalt coursework stands out either way.",
        signal="open", criteria=["precision", "hardness"]),
        country="Italy", era=-1500, civ="Nuragic",
        wires=[("fPXkyRFkvew", "Nuraghe Santu Antine")]),
    dict(site=S("Giants' Grave S'Ena e Thomes", 40.3790, 9.5154, "tomb", 2,
        "One of the best-preserved giants' tombs in Sardinia, built entirely of local granite: a semicircular exedra of knife-edge orthostats fronts an 11 m dolmenic corridor, centred on an arched monolithic stele ~4 m tall and around 7 tons, its borders smoothed and a small carved portal at its base symbolizing passage to the afterlife. Its unusual southern orientation and inconsistently reported dating are discussed in the literature.",
        signal="open", criteria=["scale", "hardness"]),
        country="Italy", era=-1700, civ="Nuragic (Bonnanaro origins)",
        wires=[("7ucq1eHx58U", "Giant's Grave S'Ena e Thomes")]),
    dict(site=S("Sacred Well of Sa Testa", 40.9346, 9.5459, "temple", 3,
        "Nuragic water sanctuary near Olbia built of worked schist and granite: a paved circular courtyard leads through a trapezoidal vestibule down 17 corbel-roofed steps to a spring chamber under a tholos vault up to 6.8 m high. Finds include a juniper-wood female statuette in Greek-Oriental style; proposed lunar alignments are unverifiable since the tholos top is incomplete."),
        country="Italy", era=-1100, civ="Nuragic",
        wires=[("4XylNHgkWNg", "Holy Well Sa Testa")]),
    dict(site=S("Nuraghe Su Mulinu", 39.6344, 8.9942, "megalithic", 3,
        "Marlstone complex combining an early corridor protonuraghe with later tholos towers and a four-tower antemural. One tower's ritual room preserves the only known Nuragic altar of the Early Iron Age — a sandstone model of a nuraghe fortress with lustral basin and drainage, once adorned with bronze swords — central evidence in the debate over the 'sacralization' of nuragic architecture."),
        country="Italy", era=-1500, civ="Nuragic",
        wires=[("dV4rrVRh3s0", "Nuraghe Su Mulinu")]),
    dict(site=S("Hypogeum of Sas Puntas", 40.6831, 8.5612, "tomb", 3,
        "Rock-cut hypogeum at Tissi whose sculpted facade translates a giants'-tomb front entirely into living limestone: a 9.5 m exedra, a 3.25 m arched stele with lunette, benches, baetyl holes and cup marks, leading to an oval burial chamber. Scholars debate whether such 'tombe a prospetto' imitate megalithic giants' tombs or continue the older domus de janas tradition; Roman-era wine presses were later cut into it."),
        country="Italy", era=-1500, civ="Nuragic (pre-Nuragic rock-cut tradition)",
        wires=[("DQUKBXqSNqQ", "Hypogeic Structure Sas Puntas")]),
    dict(site=S("Nuraghe Santa Barbara (Bauladu)", 40.0078, 8.6759, "megalithic", 3,
        "Quadrilobate basalt nuraghe with an intact ground-floor tholos chamber and three collapsed lateral towers, surrounded by an extensive village of circular and courtyard huts including a large 'meeting house.' UCLA excavations (1986-89) found a foundry area with bronze figurines and mould fragments attesting on-site metallurgy."),
        country="Italy", era=-1400, civ="Nuragic",
        wires=[("KL_iGB5TvCo", "Nuraghe Santa Barbara Bauladu")]),
    dict(site=S("Iloi Complex (Sedilo)", 40.1600, 8.8984, "megalithic", 3,
        "Basalt plateau complex above Lake Omodeo: a trilobate nuraghe with a ~10 m central tower and an intact tholos vault, a Bronze-to-Iron Age village, two giants' tombs in isodomic masonry, and the adjacent Ispiluncas necropolis of at least 33 rock-cut domus de janas with carved imitations of roof beams and traces of red ochre — four millennia of funerary and settlement architecture in one place."),
        country="Italy", era=-1400, civ="Nuragic (necropolis pre-Nuragic Ozieri)",
        wires=[("op6kl9oSIFE", "Nuraghe Iloi"), ("eblUVqvytvc", "Giants' Graves of Iloi"), ("SRsHL77f0cY", "Domus de Janas Iloi")]),
    dict(site=S("Protonuraghe Bruncu Madugui", 39.7309, 8.9978, "megalithic", 3,
        "Corridor-type protonuraghe of cyclopean basalt on the Giara di Gesturi, an ellipsoidal mass ~28 × 16.5 m long regarded as a prototype of the corridor nuraghi, with entrance passage, corbelled stairway and pseudo-vaulted rooms instead of a single tholos. Its chronology is contested — Lilliu's Early Bronze dating versus recent Middle Bronze arguments — a debate central to whether protonuraghi predate the classic tholos towers."),
        country="Italy", era=-1800, civ="Early Nuragic",
        wires=[("r8uvqh0FlZg", "Protonuraghe Bruncu Madugui")]),
    dict(site=S("Nuraghe Serbissi", 39.8453, 9.4611, "megalithic", 3,
        "Limestone complex nuraghe perched at ~950 m on the dolomitic Taccu di Osini: a central tower with well-preserved tholos, three secondary towers around a small courtyard, and a village of eight huts. A natural karst cave about 206 m long runs directly beneath the complex, used by the inhabitants, probably for storage."),
        country="Italy", era=-1600, civ="Nuragic",
        wires=[("BB2aD_Iy25s", "Nuraghe Serbissi")]),
    dict(site=S("Nuraghe Piscu", 39.5897, 9.1307, "megalithic", 3,
        "Complex nuraghe dominating the Trexenta plain: a central tholos tower ~11 m across and 9 m high in regular courses of worked marl-limestone, enclosed by a lobed bastion and an outer antemural with village huts and a rainwater cistern. Whether the bastion is trilobate or quadrilobate is genuinely unclear — an 'unusual floor plan' noted in the literature."),
        country="Italy", era=-1400, civ="Nuragic",
        wires=[("fUKJ4B6fu2M", "Nuraghe Piscu")]),
    dict(site=S("Nuraghe Corbos", 40.2567, 8.9435, "megalithic", 3,
        "Well-preserved single-tower basalt nuraghe near Silanus, ~11 m across and nearly 12 m tall with a markedly truncated-conical profile — polygonal lower courses, sub-square upper ones. The 9 m tholos chamber has three cross-set niches and a helicoidal stair to an upper cell; regular square holes in the outer masonry are of debated function, possibly beam housings."),
        country="Italy", era=-1000, civ="Nuragic",
        wires=[("J2VMdsME5Tw", "Nuraghe Corbos")]),
    dict(site=S("Nuraghe Piricu", 40.1080, 8.6804, "megalithic", 3,
        "Complex basalt nuraghe in the Montiferru district of Santu Lussurgiu: the central tower preserves about twenty courses for ~12 m of height, its ground-floor tholos rising 8 m to an ogival closure with three niches, flanked by remains of four peripheral towers."),
        country="Italy", era=-1400, civ="Nuragic",
        wires=[("wDngCen-mDg", "Nuraghe Piricu")]),
    dict(site=S("Giants' Grave of Imbertighe", 40.2081, 8.8067, "tomb", 3,
        "Giants' tomb outside Borore famed for its intact monolithic arched stele, 3.65 m tall with a relief cornice and a small portal at its base — Pinza called it the facade of the most beautiful giants' tomb known in Sardinia. The exedra wings survive in unusually regular basalt ashlar; the 9 m funerary corridor is known only from 19th-century records."),
        country="Italy", era=-1500, civ="Nuragic",
        wires=[("sxjQaWCPwFs", "Giant's Grave of Imbertighe")]),
    dict(site=S("Giants' Grave Mura Cuada", 40.0396, 8.7175, "tomb", 3,
        "Isolated coursed-masonry giants' tomb on the Abbasanta basalt plateau, of the stele-less type: a concave exedra of well-dressed basalt courses fronts an architraved entrance and a funerary chamber 4.5 m long with orthostatic walls under corbelled courses. It stands flush against the active Cagliari-Macomer railway line."),
        country="Italy", era=-1500, civ="Nuragic",
        wires=[("8a8ScKzwvjk", "Giant's Grave Mura Cuada")]),
    dict(site=S("Domus de Janas of Corongiu (Pimentel)", 39.4978, 9.0591, "tomb", 3,
        "Rock-cut tomb group in sandstone near Pimentel, its main chamber entered by a vertical shaft and carrying incised and red-painted symbolic decoration — a double spiral, a 'boat' motif with spiral ends, and zigzag bands — among the best-known painted domus decoration in the Trexenta. Late Neolithic Ozieri work, reused for millennia."),
        country="Italy", era=-3200, civ="Pre-Nuragic (Ozieri)",
        wires=[("KHnZUUOYGdM", "Domus de Janas Pimentel")]),
    dict(site=S("Giants' Grave Su Mont'e s'Abe", 40.8757, 9.4840, "tomb", 3,
        "One of Sardinia's largest giants' tombs, in granite near Olbia: a mound 28 m long enclosing a 13 m funerary corridor whose orthostatic walls — an Early Bronze Age gallery grave — were crowned with coursed blocks and a 21.5 m exedra when the monument was rebuilt as a giants' tomb. Its two-phase biography is the standard case study for the debated evolution from allée couverte to giants' tomb."),
        country="Italy", era=-1700, civ="Nuragic (over Bonnanaro gallery grave)",
        wires=[("Td0WzA0B084", "Giant's Grave Su Monte 'e S'Abe")]),
    dict(site=S("Sacred Well Is Pirois", 39.5648, 9.5928, "temple", 3,
        "Sacred well in the Rio Quirra valley built of green-blue schist in two masonry styles — polygonal blocks outside, thin slabs within: eight steps descend under an inverted-staircase ceiling to a still-flowing spring shaft capped by an intact corbelled tholos with apical oculus. A sealed upper chamber accessible only through the oculus — ritual room, mini-nuraghe, or structural device — is a documented open question."),
        country="Italy", era=-1100, civ="Nuragic",
        wires=[("-lfnWb9nmik", "Holy Well Is Pirois")]),
    # ---------------- ITALY ----------------
    dict(site=S("Messapian Walls of Castro", 40.0070, 18.4257, "city", 3,
        "Stretches of the massive mid-4th-century BC Messapian circuit in large dry-laid limestone blocks survive beneath Castro's historic centre, alongside an intramural sanctuary of Athena with a Hellenistic Doric temple and a colossal limestone cult statue restored in 2023. Whether this is Virgil's Castrum Minervae — the landing place of Aeneas — is an ongoing scholarly debate."),
        country="Italy", era=-350, civ="Messapian",
        wires=[("6hx-B9RLTeE", "The Messapic Walls of Castro · Puglia")]),
    dict(site=S("Via Cava di San Sebastiano", 42.6551, 11.6375, "rock-cut", 3,
        "One of the deepest of the Etruscan vie cave of the Sorano-Pitigliano tuff plateau: a narrow sunken road hand-cut into volcanic tuff with sheer walls rising 20-25 m above the roadbed, running beside a rock-cut necropolis. The function of the hollow ways — transport, drainage, defense, or processional — remains genuinely debated."),
        country="Italy", era=-500, civ="Etruscan",
        wires=[("TvZERmkhybU", "Via Cava (Hollow Way) of S. Sebastiano")]),
    dict(site=S("Bisenzio (Visentium)", 42.5742, 11.8749, "city", 3,
        "Protohistoric and Etruscan centre on a promontory above Lake Bolsena whose Iron Age settlement covered up to 100 hectares, famed for Villanovan bronze work. The most visible remain is the cliff-cut 'colombario' with some 900 niches over the lake; the site's abrupt decline after 500 BCE is the focus of the international Bisenzio Project."),
        country="Italy", era=-800, civ="Etruscan (Villanovan origins)",
        wires=[("--X_JHRRXZY", "The Protostoric Site of Mount Bisenzio")]),
    dict(site=S("Etruscan Necropolis of Puntone", 42.6739, 11.4907, "tomb", 3,
        "Small rural necropolis in oak woodland near Saturnia: tumuli on rectangular bases built entirely of large dry-laid travertine slabs, with dromos corridors leading to chambers roofed by pitched monolithic slabs — heavy slab construction of markedly megalithic character."),
        country="Italy", era=-600, civ="Etruscan",
        wires=[("Hl3aDTQu1xY", "Etruscan Necropolis of Puntone")]),
    dict(site=S("Juvanum", 41.9979, 14.2498, "city", 3,
        "Samnite sanctuary and Roman municipium on an Abruzzo plateau: two temple podia of dry-laid limestone stand beside a Hellenistic theatre whose cavea is partly carved directly into the rock outcrop, above the paved forum and basilica of the Roman town."),
        country="Italy", era=-300, civ="Samnite (Carricini), then Roman",
        wires=[("DEmecP35nhY", "The Archaeological Area of Juvanum · Abruzzo")]),
    dict(site=S("Monte Pallano", 42.0394, 14.3891, "megalithic", 2,
        "On a 1,020 m ridge in Abruzzo, a ~160 m stretch survives of a cyclopean dry-stone circuit originally at least 4 km long enclosing 35 hectares — identified with ancient Pallanum. The wall stands over 5 m high in huge irregular limestone blocks, pierced by gates with massive monolithic architraves. Dating and attribution are genuinely unsettled, with proposals spanning the 6th to 3rd centuries BCE and different Italic groups.",
        signal="open", criteria=["scale"]),
        country="Italy", era=-450, civ="Italic / Samnite (attribution debated)",
        wires=[("BzccSfaChPI", "The Megalithic Wall of Monte Pallano")]),
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

    if CR not in creators:
        sys.exit("ABORT: run add-stone-riddles-quickwins-batch.py first")
    before = len(sites)
    names = {s["n"] for s in sites}
    added_sites = added_wires = 0

    for entry in NEW:
        site = entry["site"]
        if set(site.get("criteria", [])) - VALID:
            sys.exit(f"ABORT: bad criteria on {site['n']!r}")
        if site["n"] in names:
            print(f"  · site {site['n']!r} exists")
        else:
            sites.append(site)
            names.add(site["n"])
            added_sites += 1
            print(f"  ✓ site {site['n']!r}")
        countries[site["n"]] = entry["country"]
        if entry.get("era") is not None:
            eras[site["n"]] = entry["era"]
        civs[site["n"]] = entry["civ"]
        for vid, title in entry["wires"]:
            wires = videos.setdefault(site["n"], [])
            if any(v.get("id") == vid for v in wires):
                print(f"    · {vid} already wired")
            else:
                wires.append({"id": vid, "title": title, "cr": CR, "added": ADDED})
                added_wires += 1

    save("sites.json", sites)
    save("videos.json", videos)
    save("countries.json", countries)
    save("eras.json", eras)
    save("civilizations.json", civs)

    print(f"\nsites {before} → {len(sites)} (+{added_sites}) | wires added: {added_wires}")
    if len(sites) < before:
        sys.exit("ABORT: count dropped")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
