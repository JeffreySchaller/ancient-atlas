#!/usr/bin/env python3
"""
wire-agelessrock-unplaced.py — close the Ageless Rock wiring gap (2026-08-07)

Building the creator study surfaced this: 53 of Bernie Ong's 296 walkthroughs
had no wire in videos.json, and the great majority were not unknown places at
all. They were sites the Atlas already carries that had simply never been
linked — Ellora, Kailasa, Lalibela, Barabar, Ajanta, Aurangabad, Pitalkhora,
the Tigray rock churches, Plain of Jars, Hoysaleshwara, Chennakeshava,
Padmanabhaswamy, Naneghat, Dharmrajeshwar, Sahasralinga, the Azores.

That gap was load-bearing. The study's strongest argument is the subtractive
tradition — cultures that cut downward into bedrock instead of building upward
— and Lalibela, Kailasa and Barabar are its three best cases. The build script
refuses to render a theme whose sites have no footage, so it aborted rather
than quietly dropping them. Correct behaviour, and the reason this pass exists.

Every mapping below is explicit, and every target is checked against
sites.json before anything is written. Titles that are genuinely general
(round-ups, quizzes, comparison essays, a millstone) are deliberately left
unwired; they belong to no single site.

No new sites, no changed sites. videos.json only.
Idempotent — safe to re-run. Run from repo root, then build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CREATOR = "agelessrock"
ADDED = "2026-08-07"

# video id -> (site name, title)
WIRES = {
    # --- India, the top-down rock-cut corpus -------------------------------
    "rZUvCU6aLRs": ("Ellora Caves", "Ellora Caves 1 to 10 : Intriguing India"),
    "zyg8sG5W1mI": ("Ellora Caves", "Ellora Caves 11 to 15 : Insane India"),
    "AJohwLrSRrc": ("Kailasa Temple (Ellora Cave 16)", "Ellora cave 16 (surrounding) : Impossible India"),
    "0XZt9sT600w": ("Ellora Caves", "Ellora Caves 17 to 21 : Imposing India"),
    "OTmBxbBdxCs": ("Ellora Caves", "Ellora Caves 22 to 24 : Incredible India"),
    "B8sc0JG9Hqw": ("Ellora Caves", "Ellora Caves 25 to 28 : Incomprehensible India"),
    "GMiNzaskpP0": ("Ellora Caves", "Ellora Cave 29 : Improbable India"),
    "-26jmwmSVls": ("Ellora Caves", "Ellora Caves 30 to 31 : Illustrious India"),
    "CVvoxiE3OGg": ("Ellora Caves", "Ellora Caves 32 to 34 : Inconceivable India"),
    "dSRNkksXZ1o": ("Kailasa Temple (Ellora Cave 16)", "Who Built Kailasa Temple?"),
    "IrnsAWcPLqM": ("Barabar Caves", "Who Created Barabar Caves in India?"),
    "yTWX9Nnyfy4": ("Ajanta Caves", "Amazing Ajanta and some Crazy Calculations."),
    "z53Z4YQjLbI": ("Aurangabad Caves", "Aurangabad Caves - Western Group (1/2)"),
    "noCNgUwi8BE": ("Aurangabad Caves", "Aurangabad Caves - Western Group (2/2)"),
    "HcO2Gsg9-Bc": ("Aurangabad Caves", "Aurangabad Caves - Eastern Group"),
    "bZT0zUREisk": ("Pitalkhora Caves", "Did Buddhist monks create Pitalkhora Caves site?"),
    "0RKIciQL54s": ("Dharmrajeshwar Temple", "Dharmrajeshwar Temple ... a monolithic top-down rock cut bedrock of mystery"),
    "AV2S-_osfas": ("Naneghat", "Mysterious giant jar in Naneghat no one is talking about."),
    "18lEAXbeGhw": ("Hoysaleshwara Temple", "The Mysteries at Hoysaleshwara Temple"),
    "YL3lltYne3U": ("Chennakeshava Temple (Belur)", "The mysteries of Chennakeshava Temple in Belur, India"),
    "lJBDgRqMpWI": ("Padmanabhaswamy Temple", "Padmanabhaswamy Temple (Part 2/2) : The Richest Megalithic Temple"),
    "LFTcDkDnMjQ": ("Padmanabhaswamy Temple", "Padmanabhaswamy Temple (Part 1/2)"),
    "dTW47WWxxoo": ("Sahasralinga (Shilmala River)", "The Mysterious Shilmala River - Sahasralinga"),

    # --- Ethiopia, rock-hewn and monolithic churches -----------------------
    "ivW_t6bo0es": ("Lalibela Rock-Hewn Churches", "Lalibela Churches (Part 1/3)"),
    "nC92mpGoV74": ("Lalibela Rock-Hewn Churches", "Lalibela Churches (Part 2/3) : Northern Group"),
    "YojKBBuJdjE": ("Lalibela Rock-Hewn Churches", "Lalibela Churches (Part 3/3) : Eastern Group"),
    "r5H5oFQvcYY": ("Abba Yohani Rock-Cut Church", "Abba Yohani Rock Cut Church"),
    "d12SDZsPWqs": ("Daniel Korkor Rock-Cut Church", "Daniel Korkor Rock Cut Church"),
    "2AddrT9bApM": ("Medhane Alem Adi Kasho", "Rock Cave Cut Church of Medhane Alem Adi Kasho"),
    "sI9wknFPjfk": ("Debra Damo Monastery", "Debra Damo Monastery of Ethiopia"),
    "qU321I6o61c": ("Adadi Maryam Monolithic Church", "Adadi Maryam Monolithic Church"),
    "v-M13a2B0Y8": ("Nazugn Mariam Monolithic Church", "Monolithic Church of Nazugn Mariam"),
    "eW1L7uDH2Zc": ("Geneta Mariam Monolithic Church", "Monolithic Church of Geneta Mariam"),
    "IcUfttZ1XR8": ("Washa Mikael Rock-Cut Church", "Washa Mikael Rock Cut Church"),
    "qafmKW7gQDA": ("Ambager Church Complex", "Ambager Church Complex of Amhara, Ethiopia"),

    # --- elsewhere ---------------------------------------------------------
    "Zz02DiKqHBo": ("Plain of Jars", "Who Made Over 2,000 Giant Jars in Laos?"),
    "DO1OTMfOCtg": ("Azores Pyramids (Pico Alto)", "Megalith of Azores"),
    "OH1QxxJDSyI": ("Azores Pyramids (Pico Alto)", "Was Azores once part of Atlantis?"),
}

# Left unwired on purpose: they belong to no single site.
#   IKScQCLj2F4 Mysterious Circular Stones Around the World
#   2XQNNf1LlYE Mills and Stones @ Millstones of Stanage
#   kun5oIBqGTo Mysterious Striations at megalithic sites
#   zbEEa9bkdb8 Compare Cave Dwellings
#   b7vGMD0vWK0 Quiz : Mysterious Megalithic Culture Gear Tracks
#   q5Z_NNNORzs Mysteries of China
#   V0wTRWFqh-8 Pyramids of Mesoamerica (already wired to Cholula)
#   plus five Portuguese monuments with no Atlas record yet


def main():
    sites = {s["n"] for s in json.loads((DATA / "sites.json").read_text(encoding="utf-8"))}
    path = DATA / "videos.json"
    videos = json.loads(path.read_text(encoding="utf-8"))

    unknown = sorted({s for s, _ in WIRES.values() if s not in sites})
    if unknown:
        print("ABORT: these targets are not in sites.json:")
        for u in unknown:
            print("   ·", u)
        sys.exit(1)

    existing = {v["id"] for lst in videos.values() for v in lst}
    added, already = 0, 0
    for vid, (site, title) in sorted(WIRES.items(), key=lambda kv: kv[1][0]):
        lst = videos.setdefault(site, [])
        if any(v.get("id") == vid for v in lst):
            already += 1
            continue
        lst.append({"id": vid, "title": title, "cr": CREATOR,
                    "added": ADDED, "published": ADDED})
        added += 1

    if added:
        path.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print(f"  ✓ wrote data/videos.json")
    print(f"  wired {added}, already present {already}, "
          f"{len(WIRES) - added - already} skipped")

    after = json.loads(path.read_text(encoding="utf-8"))
    mine = sum(1 for lst in after.values() for v in lst if v.get("cr") == CREATOR)
    total = sum(len(l) for l in after.values())
    print(f"\nAgeless Rock wires : {mine} · walkthroughs overall : {total}")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
