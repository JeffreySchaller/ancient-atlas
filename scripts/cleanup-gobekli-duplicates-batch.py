#!/usr/bin/env python3
"""
cleanup-gobekli-duplicates-batch.py — Göbekli Tepe duplicate cleanup (2026-07-09)

Context : An earlier session suppressed 3 duplicate Göbekli Tepe site entries
at RENDER time (FILTERED_SITES exclusion in public/index.html) instead of
cleaning the data. That stranded 5 unique walkthrough wires on the suppressed
"Göbekli Tepe (Potbelly Hill)" videos.json key — invisible on the live atlas.

What this does :
1. Merges the orphan wires from "Göbekli Tepe (Potbelly Hill)" into the
   primary "Göbekli Tepe" videos.json key (dedup by video id), then removes
   the orphan key. Recovers: 3× turkiyetoday, 1× megalithomania,
   1× archaiclens walkthroughs.
2. Deletes the 3 duplicate site entries from sites.json:
   "Göbekli Tepe (Potbelly Hill)", "Göbekli Tepe Visitor Center",
   "Göbekli Tepe Layer III".

DELIBERATE COUNT DECREASE : raw sites 563 → 560. This matches the count the
site has always displayed (FILTERED_SITES). The pre-flight floor moves to
560 — documented in memory/projects/ancient-atlas.md. Aux data files carry
no entries for the deleted names (verified 2026-07-09); no library refs.

The render-time exclusion in index.html becomes a harmless no-op and is left
in place as a guard against dupe reintroduction.

Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

DUPES = [
    "Göbekli Tepe (Potbelly Hill)",
    "Göbekli Tepe Visitor Center",
    "Göbekli Tepe Layer III",
]
PRIMARY = "Göbekli Tepe"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    sites = load("sites.json")
    videos = load("videos.json")
    before_sites = len(sites)
    before_wires = sum(len(v) for v in videos.values())

    if not any(s["n"] == PRIMARY for s in sites):
        sys.exit(f"ABORT: primary site {PRIMARY!r} not found")

    # 1. merge orphan wires into primary (idempotent by video id)
    merged = 0
    for dupe in DUPES:
        orphans = videos.get(dupe)
        if not orphans:
            continue
        primary_wires = videos.setdefault(PRIMARY, [])
        primary_ids = {v.get("id") for v in primary_wires}
        for v in orphans:
            if v.get("id") not in primary_ids:
                primary_wires.append(v)
                primary_ids.add(v.get("id"))
                merged += 1
                print(f"  ✓ merged wire {v.get('id')!r} ({v.get('cr','?')}) → {PRIMARY!r}")
        del videos[dupe]
        print(f"  ✓ removed orphan videos key {dupe!r}")

    # 2. delete duplicate site entries (idempotent)
    kept = [s for s in sites if s["n"] not in DUPES]
    removed = before_sites - len(kept)
    for name in DUPES:
        if any(s["n"] == name for s in sites):
            print(f"  ✓ deleted site entry {name!r}")

    save("videos.json", videos)
    save("sites.json", kept)

    after_wires = sum(len(v) for v in videos.values())
    print(f"\nsites {before_sites} → {len(kept)} (removed {removed} duplicates)")
    print(f"total wires {before_wires} → {after_wires}")
    print(f"primary {PRIMARY!r} wires: {len(videos[PRIMARY])}")

    # guards
    if len(kept) < 560:
        sys.exit("ABORT: site count fell below the documented floor of 560")
    if after_wires < before_wires:
        sys.exit("ABORT: total wire count dropped — orphan merge lost wires")

    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
