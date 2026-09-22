#!/usr/bin/env python3
"""
add-luzhouabo-approximate.py — 泸州阿波 / Luzhou Abo (2026-09-22)

What this adds :
- 1 new creator : luzhouabo (泸州阿波 Luzhou Abo, @luzhouabo)
- 3 new sites   : Eastern Han Cliff Tombs (Sichuan)
                  Sichuan Cave Fortress (999 AD)
                  Hubei Cliff Dwelling
- 3 wires       : one each
- aux maps      : country, civilization, era, tags

*** READ THIS BEFORE TRUSTING THESE THREE COORDINATES ***

All three pins are APPROXIMATE and every one of them may be wrong by
hundreds of kilometres. This is a deliberate decision by Jeff on
2026-09-22, taken with the error bars in front of him, so that these
subjects are visible in the atlas rather than absent. They are NOT
research-grade positions and must not be treated as such.

The reason is the creator's method. 泸州阿波 films places that are
deliberately unidentified - one of his own titles says outright that no
information about the site can be found online. Full descriptions,
keywords, video location metadata and top comments were all checked for
all three. None gives anything below province level, and Sichuan is
800 km across.

So each pin uses the best prior available and says so in its own desc,
in the first sentence, where a reader will see it:

  Eastern Han Cliff Tombs (Sichuan)  28.8200, 105.9849
      Pinned on the Hejiang cliff-tomb group in LUZHOU - the creator's
      home prefecture, which his channel name states - a documented
      Eastern Han cliff-tomb complex of 13 locations across 13
      townships, national protected unit since 2013. Same period, same
      class, right prefecture. Not the same claim as "this is it".

  Sichuan Cave Fortress (999 AD)     28.8710, 105.4420
      No prior at all beyond "Sichuan". Pinned on Luzhou itself, the
      creator's base. A separate Chinese channel covers what appears to
      be the same site - same 999 date, same hand-pushed stone door -
      and calls it 青龙寨 (Qinglong Zhai), but no authoritative source
      or coordinate was found for that name, so it is not asserted here.

  Hubei Cliff Dwelling               30.2951, 109.4796
      Pinned on Enshi. Hubei's cliff dwellings are an Enshi phenomenon:
      恩施崖居, documented by National Geographic China as "fossil
      specimens in the history of vernacular dwelling". Regional, not
      site-level.

HOW TO FIX ONE. Replace lat/lng, delete the first sentence of the desc,
and drop "approximate location" from its tags.json entry. The tag is
there so `grep "approximate location" data/tags.json` finds every
provisional pin in the atlas. Right now it finds exactly these three.

Not affected: Pijijiapan's pin is an inference too, but from a measured
offset in a published source, and is good to about 1 km. These are a
different order of uncertainty and are marked differently.

Sites count : 629 → 632.

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
CR = "luzhouabo"
CREATOR = {
    "name": "Luzhou Abo",
    "handle": "@luzhouabo",
    "subs": "泸州阿波 · Sichuan-based · unmapped cliff dwellings, cave forts and stone villages across China",
    "color": "#7E8CA8",   # vestigial; toneCreators() recomputes at runtime
    "tier": 3,
}

APPROX = "approximate location"

SITES = [
 {"n": "Eastern Han Cliff Tombs (Sichuan)", "lat": 28.8200, "lng": 105.9849,
  "cat": "tomb", "region": "Asia", "tier": 3, "criteria": ["scale"],
  "desc": (
    "Location approximate. The film does not say where this is, so the "
    "pin sits on the Hejiang cliff-tomb group in Luzhou — the creator's "
    "home prefecture — which is a documented Eastern Han complex of the "
    "same kind; the actual group may be elsewhere in Sichuan. What the "
    "film shows is a cliff-tomb cemetery cut some 1,800 years ago into "
    "the rock of a Sichuan mountainside, the chambers finished not as "
    "burial slots but as complete domestic interiors — rooms laid out "
    "like a house for the living. That much is ordinary for the "
    "tradition : Sichuan's Eastern Han cliff tombs run to thousands of "
    "chambers along the Min, Yangtze, Chishui and Xishui valleys, and "
    "the best-studied groups at Jiangkou and Mahao carry carved "
    "furniture, painted stone coffins and, at Mahao, some of the "
    "earliest Buddhist images known in China. The film's own question is "
    "narrower and better : where did the spoil go. Cutting chambers of "
    "that size out of a cliff produces an enormous volume of broken "
    "rock, and there is no talus, no spoil heap, nothing below the cliff "
    "face. Somebody carried it away."),
  "aux": {"countries.json": "China", "civilizations.json": "Eastern Han",
          "eras.json": 100,
          "tags.json": "china sichuan cliff tombs yamu eastern han rock-cut "
                       "burial chambers luzhou hejiang spoil " + APPROX}},

 {"n": "Sichuan Cave Fortress (999 AD)", "lat": 28.8710, "lng": 105.4420,
  "cat": "rock-cut", "region": "Asia", "tier": 3, "criteria": ["scale"],
  "desc": (
    "Location approximate. The film gives only the province, so the pin "
    "sits on Luzhou, the creator's base; the site may be anywhere in "
    "Sichuan. A three-storey fortress cut into solid rock, entered "
    "through a single stone door of about 400 kg that still swings by "
    "hand, opening onto interconnected chambers, concealed passages and "
    "enough of them to get lost in. The date given on film is precise — "
    "carved in 999 AD, which puts it in the early Northern Song — and "
    "the local guide's account is the only source for it. The walls "
    "inside are black with soot, which the film reads as evidence of a "
    "fire attack, a siege rather than a hearth. Another Chinese channel "
    "appears to cover the same fortress, giving the same 999 date and "
    "the same hand-pushed stone door, and calls it 青龙寨, Qinglong "
    "Zhai; no authoritative source or coordinate was found under that "
    "name, so the atlas does not assert it."),
  "aux": {"countries.json": "China", "civilizations.json": "Northern Song (reported)",
          "eras.json": 999,
          "tags.json": "china sichuan cave fortress dongzhai rock-cut stone door "
                       "northern song 999 qinglongzhai luzhou " + APPROX}},

 {"n": "Hubei Cliff Dwelling", "lat": 30.2951, "lng": 109.4796,
  "cat": "rock-cut", "region": "Asia", "tier": 3, "criteria": ["scale"],
  "desc": (
    "Location approximate. The film names only Hubei, so the pin sits on "
    "Enshi, where Hubei's cliff dwellings are concentrated — 恩施崖居, "
    "described by National Geographic China as fossil specimens in the "
    "history of vernacular dwelling — but the site may be elsewhere in "
    "the province. An entire mountainside hollowed out by hand into "
    "dozens of stone rooms, fitted out to be lived in rather than "
    "sheltered in, reached across a cliff face. The labour is the point "
    "and so is the question behind it : this is not a cave anyone "
    "improved, it is a building excavated rather than built, and the "
    "reason people chose to make a home this way — war, most likely, as "
    "at the other Chinese cliff settlements — is not recorded anywhere "
    "on the site."),
  "aux": {"countries.json": "China", "civilizations.json": "Not established",
          "tags.json": "china hubei enshi cliff dwelling yaju rock-cut stone houses "
                       "hollowed mountain " + APPROX}},
]

WIRES = [
 ("Eastern Han Cliff Tombs (Sichuan)", "sJ4Iw4U2m2k",
  "China's eeriest Han cliff tombs: 1,800-year-old homes. Giant stones vanished mysteriously", "2026-09-09"),
 ("Sichuan Cave Fortress (999 AD)", "4edw4Jt9980",
  "999 AD Carved: Sichuan's Thousand-Year-Old Mysterious Palace", "2026-09-17"),
 ("Hubei Cliff Dwelling", "blJo5t7Ory4",
  "A thousand-year-old cliff dwelling in Hubei: an entire mountain hollowed out", "2026-08-00"),
]

def load(n): return json.loads((DATA / n).read_text(encoding="utf-8"))
def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  ✓ wrote data/{n}")

def main():
    cats = load("categories.json")
    ck = set(cats.keys()) if isinstance(cats, dict) else {c.get("key") for c in cats}
    creators = load("creators.json")
    if CR in creators:
        print(f"  · creator {CR!r} already present.")
    else:
        creators[CR] = dict(CREATOR); save("creators.json", creators)
        print(f"  ✓ added creator {CR!r}.")
    creators = load("creators.json")

    sites = load("sites.json"); before = len(sites)
    regions = {s["region"] for s in sites}; names = {s["n"] for s in sites}
    for spec in SITES:
        rec = {k: v for k, v in spec.items() if k != "aux"}
        bad = set(rec.get("criteria", [])) - VALID_CRITERIA
        if bad: sys.exit(f"ABORT: {rec['n']}: bad criteria {bad}")
        if rec["cat"] not in ck: sys.exit(f"ABORT: {rec['n']}: category undefined")
        if rec["region"] not in regions: sys.exit(f"ABORT: {rec['n']}: unused region")
        # the desc MUST lead with the caveat - that is the whole deal here
        if not rec["desc"].startswith("Location approximate."):
            sys.exit(f"ABORT: {rec['n']}: desc must open with the location caveat")
        if APPROX not in spec["aux"]["tags.json"]:
            sys.exit(f"ABORT: {rec['n']}: tags must carry the {APPROX!r} marker")
        for s in sites:
            if s["n"] == rec["n"]: continue
            d = math.hypot((s["lat"]-rec["lat"])*111.0,
                           (s["lng"]-rec["lng"])*111.0*math.cos(math.radians(rec["lat"])))
            if d < 1.0: sys.exit(f"ABORT: {rec['n']} lands {d:.2f} km from {s['n']!r}")
        if rec["n"] in names:
            print(f"  · {rec['n']!r} already present.")
        else:
            sites.append(rec); names.add(rec["n"])
            print(f"  ✓ added {rec['n']!r} ({rec['cat']}) — APPROXIMATE pin")
    save("sites.json", sites)

    for spec in SITES:
        for filename, value in spec["aux"].items():
            m = load(filename)
            if m.get(spec["n"]) == value: continue
            m[spec["n"]] = value; save(filename, m)

    sites_now = {s["n"] for s in load("sites.json")}
    videos = load("videos.json")
    seen = {v.get("id") for rows in videos.values() for v in rows}
    changed = False
    for target, vid, title, pub in WIRES:
        if target not in sites_now: sys.exit(f"ABORT: {target!r} missing")
        rows = videos.setdefault(target, [])
        if any(v.get("id") == vid for v in rows):
            print(f"  · {vid} already wired."); continue
        if vid in seen: sys.exit(f"ABORT: {vid} wired elsewhere")
        rows.append({"id": vid, "title": title, "cr": CR,
                     "added": "2026-09-22", "published": pub})
        seen.add(vid); changed = True
        print(f"  ✓ wired {vid} → {target!r}.")
    if changed: save("videos.json", videos)

    after = len(load("sites.json"))
    print(f"\nsites {before} → {after}")
    if after < before: sys.exit("ABORT: site count dropped")
    print("\nPROVISIONAL PINS IN THE ATLAS:")
    t = load("tags.json")
    for k, v in t.items():
        if APPROX in v: print("   ", k)
    print("\nNext step : python3 scripts/build.py")

if __name__ == "__main__":
    sys.exit(main())
