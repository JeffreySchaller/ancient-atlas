#!/usr/bin/env python3
"""
add-leshan-wanderingwolf.py — Wandering Wolf at Leshan (2026-08-07)

Adds : jMhbbpTXOp8  "Leshan Giant Buddha and Oriental Park - China"
       Wandering Wolf (@wanderingwolf), 14:17

Wired to Leshan Giant Buddha and deliberately placed FIRST in that site's
list, ahead of the existing Ageless Rock entry, per Jeff's call on ordering.

Also : Leshan Giant Buddha moves cat "rock-cut" -> "megalithic".

Idempotent — safe to re-run. Run from repo root, then python3 scripts/build.py
(and the two creator page builders, which read videos.json).
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"

SITE = "Leshan Giant Buddha"
NEW_CAT = "megalithic"
CREATOR_KEY = "wanderingwolf"

VIDEO = {
    "id": "jMhbbpTXOp8",
    "title": "Leshan Giant Buddha and Oriental Park - China",
    "cr": CREATOR_KEY,
    "added": "2026-08-07",
    "published": "2026-08-07",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print(f"  ✓ wrote data/{name}")


def main():
    creators = load("creators.json")
    if CREATOR_KEY not in creators:
        sys.exit(f"ABORT: creator {CREATOR_KEY!r} not in creators.json")

    # ------------------------------------------------------------ the site
    sites = load("sites.json")
    before = len(sites)
    hit = [s for s in sites if s["n"] == SITE]
    if len(hit) != 1:
        sys.exit(f"ABORT: expected exactly one {SITE!r}, found {len(hit)}")
    site = hit[0]
    if site.get("cat") != NEW_CAT:
        print(f"  ✓ cat {site.get('cat')!r} → {NEW_CAT!r}")
        site["cat"] = NEW_CAT
        save("sites.json", sites)
    else:
        print(f"  · cat already {NEW_CAT!r}")

    # ------------------------------------------------------------ the wire
    videos = load("videos.json")
    lst = videos.setdefault(SITE, [])
    if any(v.get("id") == VIDEO["id"] for v in lst):
        # already there — make sure it is still first
        if lst[0].get("id") != VIDEO["id"]:
            lst.sort(key=lambda v: v.get("id") != VIDEO["id"])
            save("videos.json", videos)
            print(f"  ✓ moved {VIDEO['id']!r} back to first position")
        else:
            print(f"  · {VIDEO['id']!r} already wired, already first")
    else:
        lst.insert(0, dict(VIDEO))
        save("videos.json", videos)
        print(f"  ✓ wired {VIDEO['id']!r} → {SITE!r} (first in list)")

    # ----------------------------------------------------------- guards
    after_sites = load("sites.json")
    if len(after_sites) != before:
        sys.exit("ABORT: site count changed")
    final = [s for s in after_sites if s["n"] == SITE][0]
    order = [(v["id"], v["cr"]) for v in load("videos.json")[SITE]]
    print(f"\n{SITE}: cat={final['cat']} tier={final.get('tier')}")
    print("order :")
    for i, (vid, cr) in enumerate(order, 1):
        print(f"  {i}. {vid}  {cr}")
    if order[0][0] != VIDEO["id"]:
        sys.exit("ABORT: the new entry is not first")
    print("\nNext : python3 scripts/build.py && "
          "python3 scripts/build-creator-page.py && "
          "python3 scripts/build-creator-feature.py")


if __name__ == "__main__":
    sys.exit(main())
