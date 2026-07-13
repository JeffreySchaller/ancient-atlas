#!/usr/bin/env python3
"""
add-stone-riddles-quickwins-batch.py — Stone Riddles sweep, part 1 (2026-07-11)

Full-channel curation of @StoneRiddles (73 long-form videos; Mediterranean
polygonal-masonry field surveys: Greece, Sardinia, Italy). Part 1 ships the
zero-research work:

1. DUPE CLEANUP (Pisac/Göbekli pattern):
   - "Pnyx" + "Pnyx Hill (Athens)"     → "Pnyx" (keeps the richer Hill
     content: tier 2, signal:convergent, criteria, cyclopean desc)
   - "Mycenae" + "Mycenae (Lion Gate)" → "Mycenae" (keeps Lion Gate's
     richer content: tier 1, signal:convergent, criteria)
   Wires merged; none lost. 567 → 565 (deliberate, documented).

2. NEW CREATOR: stoneriddles (Stone Riddles, @StoneRiddles, tier 3 —
   small channel, exceptional field coverage).

3. 16 WIRES to 11 existing sites (Phaistos, Pnyx, Delphi, Nekromanteion of
   Acheron, Arcadian Gate (Messene) ×3, Epidaurus, Tiryns ×2, Mycenae ×2,
   Pyramid of Hellinikon, Sardinia Nuraghi (Su Nuraxi) ← the full Sardinia
   documentary, Cosa ×2).

Part 2 (companion script) adds the ~47 researched new sites.
Idempotent — safe to re-run. Run from repo root, then build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
CR = "stoneriddles"
ADDED = "2026-07-11"

MERGES = [  # (keep, remove) — keeper adopts remover's content below
    ("Pnyx", "Pnyx Hill (Athens)"),
    ("Mycenae", "Mycenae (Lion Gate)"),
]

CREATOR = {
    "name": "Stone Riddles",
    "handle": "@StoneRiddles",
    "subs": "Mediterranean polygonal-masonry field surveys · Greece, Sardinia, Italy documentaries",
    "color": "#5A9E94",
    "tier": 3,
}

WIRES = [
    ("Phaistos", "SwDngsk1SBo", "Large Blocks at Phaistos"),
    ("Pnyx", "anKyo0ISMtw", "The Cyclopean Stone Blocks of Pnyx"),
    ("Delphi", "lX1FndaE63o", "Polygonal Walls Everywhere!! In Delphi"),
    ("Nekromanteion of Acheron", "betc2ZPMeQY", "The Enigmatic Necromanteion"),
    ("Arcadian Gate (Messene)", "SrBzJlzIjdw", "Mixture of Architectural Styles at the City of Messene"),
    ("Arcadian Gate (Messene)", "EWTuv1WUk6M", "Colossal Walls at Messene"),
    ("Arcadian Gate (Messene)", "b7hG-LASJIU", "Was the Messene Wall Really Built in 85 Days??"),
    ("Epidaurus", "KirEaArhQKE", "Polygonal Masonry, Megalithism and Precision Stone Cuts at Epidaurus"),
    ("Tiryns", "JN29fgkckrk", "The Treasury of Tiryns"),
    ("Tiryns", "SjgkEj_ynKc", "Massive Blocks at Tiryns"),
    ("Mycenae", "roVE1FS6B2g", "The Gigantic Treasuries of Mycenae"),
    ("Mycenae", "DjsNO-KtSGY", "Huge Polygonal Walls at Mycenae"),
    ("Pyramid of Hellinikon", "z6yUigPi1nw", "The Polygonal Pyramid of Hellinikon"),
    ("Sardinia Nuraghi (Su Nuraxi)", "q0YNkMIt3BY", "Documentary Stone Riddles II — Archaeological Treasures of Sardinia"),
    ("Cosa", "SargCH8f2aY", "The Polygonal Walls of Cosa — Tuscany"),
    ("Cosa", "sIFCCZ6Obwo", "Polygonal Site of Cosa in Tuscany from Drone"),
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
    before_sites = len(sites)
    before_wires = sum(len(v) for v in videos.values())

    # 1. dupes — keeper adopts remover's content (name preserved)
    by_name = {s["n"]: s for s in sites}
    for keep, remove in MERGES:
        if remove in by_name and keep in by_name:
            keeper, remover = by_name[keep], by_name[remove]
            for k, v in remover.items():
                if k != "n":
                    keeper[k] = v
            sites = [s for s in sites if s["n"] != remove]
            by_name = {s["n"]: s for s in sites}
            print(f"  ✓ merged {remove!r} content into {keep!r}, deleted dupe")
        if remove in videos:
            kw = videos.setdefault(keep, [])
            ids = {v.get("id") for v in kw}
            for v in videos[remove]:
                if v.get("id") not in ids:
                    kw.append(v)
                    ids.add(v.get("id"))
                    print(f"  ✓ moved wire {v.get('id')!r} → {keep!r}")
            del videos[remove]

    # 2. creator
    if CR in creators:
        print(f"  · creator {CR!r} exists")
    else:
        creators[CR] = CREATOR
        print(f"  ✓ added creator {CR!r}")

    # 3. wires
    names = {s["n"] for s in sites}
    for site_name, vid, title in WIRES:
        if site_name not in names:
            sys.exit(f"ABORT: site {site_name!r} not found")
        wires = videos.setdefault(site_name, [])
        if any(v.get("id") == vid for v in wires):
            print(f"  · {vid} already wired to {site_name!r}")
        else:
            wires.append({"id": vid, "title": title, "cr": CR, "added": ADDED})
            print(f"  ✓ wired {vid} → {site_name!r}")

    save("sites.json", sites)
    save("creators.json", creators)
    save("videos.json", videos)

    after_wires = sum(len(v) for v in videos.values())
    print(f"\nsites {before_sites} → {len(sites)} | wires {before_wires} → {after_wires}")
    if after_wires < before_wires:
        sys.exit("ABORT: wires lost")
    if len(sites) < 565:
        sys.exit("ABORT: below documented floor 565")
    print("Next: part-2 new-sites batch, then build.py")


if __name__ == "__main__":
    sys.exit(main())
