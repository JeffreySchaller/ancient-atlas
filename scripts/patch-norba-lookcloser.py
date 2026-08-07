#!/usr/bin/env python3
"""
patch-norba-lookcloser.py — Norba reclassification (2026-08-07)

Follow-up to add-norba-stoneriddles-batch.py. Jeff's call after seeing the
record live :

1. cat  "city" → "megalithic". Norba's claim on the Atlas is the polygonal
   circuit itself, not the town plan inside it. Filing it under City/Ruins
   buried it under the Type filter alongside Roman colonies whose interest
   is urban rather than lithic.

2. signal "convergent" → "open", which earns the Look Closer badge
   (front-end renders on signal === 'open' AND criteria; see
   scripts/build-seo-pages.py L199). The open question at Norba is real and
   narrow : the 1901 excavations assigned the visible fabric to the Roman
   period, while the polygonal courses carry the same masonry vocabulary as
   circuits elsewhere in Italy that are argued to be far older. Norba is
   still the dated control case; a control with a contested lower course is
   exactly what deserves the badge.

3. One sentence of desc retuned so the record does not open by waving the
   question away, now that it carries a Look Closer.

criteria unchanged : polygonal, scale, geometry.
No site count change (617). Idempotent — safe to re-run.
Run from repo root, then python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

SITE_NAME = "Norba"

NEW_CAT = "megalithic"
NEW_SIGNAL = "open"
REQUIRED_CRITERIA = ["polygonal", "scale", "geometry"]

OLD_SENTENCE = (
    "Norba's value to the polygonal question is its date rather than its "
    "mystery : besieged in the civil war between Marius and Sulla, the "
    "inhabitants burned the town and killed themselves rather than "
    "surrender at the end of 82 BCE, and the site was never reoccupied."
)
NEW_SENTENCE = (
    "What makes Norba unusual is that it is dated : besieged in the civil "
    "war between Marius and Sulla, the inhabitants burned the town and "
    "killed themselves rather than surrender at the end of 82 BCE, and the "
    "site was never reoccupied."
)


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  ✓ wrote data/{name}")


def main():
    sites = load("sites.json")
    before = len(sites)

    hits = [s for s in sites if s["n"] == SITE_NAME]
    if len(hits) != 1:
        sys.exit(f"ABORT: expected exactly 1 {SITE_NAME!r} record, found {len(hits)}")
    site = hits[0]

    changed = False

    if site.get("cat") != NEW_CAT:
        print(f"  ✓ cat {site.get('cat')!r} → {NEW_CAT!r}")
        site["cat"] = NEW_CAT
        changed = True
    else:
        print(f"  · cat already {NEW_CAT!r}")

    if site.get("signal") != NEW_SIGNAL:
        print(f"  ✓ signal {site.get('signal')!r} → {NEW_SIGNAL!r}")
        site["signal"] = NEW_SIGNAL
        changed = True
    else:
        print(f"  · signal already {NEW_SIGNAL!r}")

    if site.get("criteria") != REQUIRED_CRITERIA:
        print(f"  ✓ criteria → {REQUIRED_CRITERIA}")
        site["criteria"] = list(REQUIRED_CRITERIA)
        changed = True
    else:
        print(f"  · criteria already {REQUIRED_CRITERIA}")

    if OLD_SENTENCE in site.get("desc", ""):
        site["desc"] = site["desc"].replace(OLD_SENTENCE, NEW_SENTENCE)
        print("  ✓ desc sentence retuned")
        changed = True
    elif NEW_SENTENCE in site.get("desc", ""):
        print("  · desc already retuned")
    else:
        print("  ! desc sentence not matched — left untouched, check by hand")

    if changed:
        save("sites.json", sites)

    # ------------------------------------------------------------ guards
    after_sites = load("sites.json")
    if len(after_sites) != before:
        sys.exit("ABORT: site count changed")
    final = [s for s in after_sites if s["n"] == SITE_NAME][0]
    assert final["cat"] == NEW_CAT
    assert final["signal"] == NEW_SIGNAL
    assert final["criteria"] == REQUIRED_CRITERIA
    badge = final.get("signal") == "open" and bool(final.get("criteria"))
    print(f"\nsites {before} (unchanged) · Look Closer badge : {badge}")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
