#!/usr/bin/env python3
"""
tag-polygonal-corpus.py — complete the polygonal criterion (2026-08-07)

Groundwork for Library Entry 08, The Convergence Question.

The entry's whole method is that a pattern claim has to be tested against the
whole corpus rather than a curated four-panel montage. That only works if the
corpus is actually tagged. It was not: 29 sites describe polygonal or cyclopean
masonry in their own descriptions while carrying no `polygonal` criterion, so
they were invisible to the filter the entry sends readers to. Alatri, the type
site for Italian polygonal masonry, was one of them. So was Sacsayhuaman.

Every one of the 29 was checked by reading the sentence in its own desc that
mentions the masonry; all 29 are genuine, no false positives from phrasing like
"unlike polygonal work". The list is explicit below rather than regex-derived,
so re-running cannot sweep in new sites by accident.

Only `criteria` is touched. `signal` is deliberately left alone: the Look Closer
badge renders on signal == "open" AND criteria, so tagging a site that is not
flagged open adds it to the filter without putting a badge on it. The one
visible change is Sacsayhuaman, already signal:open, whose badge text gains the
polygonal clause it should always have had.

Corpus: 53 -> 82 sites carrying the polygonal criterion.
No site count change (617). Idempotent - safe to re-run.
Run from repo root, then python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

VALID_CRITERIA = {"precision", "polygonal", "scale", "hardness",
                  "stratigraphy", "geometry", "machining"}

# Verified one by one against the masonry sentence in each site's own desc.
TARGETS = [
    "Sacsayhuamán",
    "Tiryns",
    "Koh Ker",
    "Abu Rawash",
    "Alatri Acropolis",
    "Alba Fucens",
    "Segni (Signia)",
    "Cosa",
    "Daorson",
    "Arcadian Gate (Messene)",
    "Pnyx",
    "Hosn Suleiman",
    "Pyramid of Hellinikon",
    "Rumiwasi",
    "Hyrtakina",
    "Aptera",
    "Lato",
    "Eleutherai Fortress",
    "Dodona",
    "Cassope",
    "Oiniades",
    "Agios Adrianos Fort",
    "Asine",
    "Midea",
    "Heraion of Argos",
    "Protonuraghe Bruncu Madugui",
    "Nuraghe Corbos",
    "Sacred Well Is Pirois",
    "Monte Pallano",
]


def main():
    path = DATA / "sites.json"
    sites = json.loads(path.read_text(encoding="utf-8"))
    before_count = len(sites)
    by_name = {s["n"]: s for s in sites}

    unknown = [n for n in TARGETS if n not in by_name]
    if unknown:
        sys.exit(f"ABORT: not in sites.json: {unknown}")

    added, already = 0, 0
    for name in TARGETS:
        site = by_name[name]
        crit = site.get("criteria") or []
        if "polygonal" in crit:
            already += 1
            continue
        crit = list(crit) + ["polygonal"]
        bad = set(crit) - VALID_CRITERIA
        if bad:
            sys.exit(f"ABORT: {name} would carry invalid criteria {bad}")
        site["criteria"] = crit
        added += 1

    if added:
        path.write_text(
            json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"  ✓ wrote data/sites.json")
    print(f"  tagged {added}, already tagged {already}")

    # ------------------------------------------------------------- guards
    after = json.loads(path.read_text(encoding="utf-8"))
    if len(after) != before_count:
        sys.exit("ABORT: site count changed")
    corpus = [s for s in after if "polygonal" in (s.get("criteria") or [])]
    badge_gained = [s["n"] for s in after
                    if s["n"] in TARGETS and s.get("signal") == "open"]
    print(f"\npolygonal corpus : {len(corpus)} sites")
    print(f"of the newly tagged, already signal:open (badge text changes) : "
          f"{sorted(badge_gained)}")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
