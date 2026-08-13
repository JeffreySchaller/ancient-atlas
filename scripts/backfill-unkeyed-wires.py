#!/usr/bin/env python3
"""
backfill-unkeyed-wires.py — credit the 45 seed videos (2026-08-13)

45 of 997 wires carried only {id, title}: no creator key, no dates. They are
the original seed videos, added before the creator system existed, and they sit
on 21 of the most-visited sites in the Atlas — Göbekli Tepe, the Great Pyramid,
Derinkuyu. Every one of them played on the site with no credit to whoever shot
it, and none of them counted toward any per-creator total.

Every id below was resolved against YouTube's public oEmbed endpoint, so the
channel names and handles are the platform's own, not guesses. Handles are
matched against the existing creators.json first — several of these turn out to
belong to channels the Atlas already credits, so this corrects their totals
rather than inventing duplicates.

One id, kBu68hzQ4HI, returns 404: the video is gone. It is left untouched and
reported, because deleting someone's curation is Jeff's call, not mine.

Idempotent. Run from repo root, then build.py.
"""
import json
import sys
import collections
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SEED_DATE = "2025-11-01"          # predates the creator system; honest placeholder

# id -> (channel name, handle) straight from youtube oembed
RESOLVED = {
    "yYCk_iEDEWU": ("Wonderliv Travel", "@Wonderliv"),
    "WZGzrBUpUps": ("Discover With Ruhi Cenet", "@RuhiCenetGlobal"),
    "0tiGV7QuSTA": ("Colorado Guide", "@coloradonativeguide"),
    "vXJc-Y3Mf5w": ("History Time", "@HistoryTime"),
    "xJU973IbG7I": ("Miniminuteman", "@miniminuteman773"),
    "CEl6P5wo6ro": ("KaimarkLifestyle", "@KaimarkLifestyle"),
    "8BHJP7uLcq4": ("Ancient Presence", "@AncientPresence"),
    "p3b8tAKFfmM": ("The Ultimate Discovery", "@ultimatediscovery"),
    "frhysD0G4mg": ("UnchartedX", "@UnchartedX"),
    "_NENyicREo8": ("Brien Foerster", "@brienfoerster"),
    "g0kf82I6ffc": ("UnchartedX", "@UnchartedX"),
    "VrPlrwuBiJk": ("Megalithomania", "@MegalithomaniaUK"),
    "qFLsvnsKc3U": ("Megalithomania", "@MegalithomaniaUK"),
    "4Tbd6g-uQWE": ("Traveling with Krushworth", "@TravelingwithKrushworth"),
    "4LCZvM6lMms": ("Secret Stops", "@SecretStopsTV"),
    "Kb1z8qQJVO0": ("Tess Agaid Smith", "@TessAgaidSmith"),
    "-xuyxSc3as8": ("Earth Unraveled", "@EarthUnraveled"),
    "6wzVMnZWpcY": ("UNESCO", "@UNESCO"),
    "FA9Mlo1Jabk": ("Odyssey", "@odyssey"),
    "C5jpbwizxBs": ("National Geographic", "@NatGeo"),
    "Qh8fZUnpKyg": ("World Wild Hearts", "@worldwildhearts"),
    "g34lDUxodZo": ("HISTORY", "@HISTORY"),
    "ljjmIPgP_Mc": ("Daily Dose Documentary", "@DailyDoseDocumentary"),
    "7w7UI08iEQs": ("FPN — History & Culture", "@Freedompressnews-Documentaries"),
    "J5YR0uqPAI8": ("National Geographic", "@NatGeo"),
    "QxNny85a23A": ("James Puente", "@JamesPuente"),
    "tg17MbVG2XI": ("HISTORY", "@HISTORY"),
    "Zdsi0qKVJO8": ("Smarthistory", "@smarthistory-art-history"),
    "KVXWZkwV0RQ": ("National Geographic", "@NatGeo"),
    "ngADMns8W78": ("RTÉ News", "@rtenews"),
    "oYqzj_C6vb0": ("Standing Stones of Ireland", "@standingstonesireland"),
    "CqO4PE4uZhc": ("Rick Steves' Europe", "@RickStevesEuropeOfficial"),
    "9_6inr3KLx0": ("Manuel Bravo", "@ManuelBravo"),
    "uWV_8IGnoOw": ("COSI", "@cosiscience"),
    "D2qoZDdg6ho": ("Rick Steves' Europe", "@RickStevesEuropeOfficial"),
    "EabKVN5pAxc": ("Manuel Bravo", "@ManuelBravo"),
    "3krqSvX8vd0": ("DarAdventures", "@daradventures"),
    "tzBmrpFNcH4": ("National Geographic", "@NatGeo"),
    "0fdreKvuqgs": ("National Geographic", "@NatGeo"),
    "Vh7Re5DdQH8": ("Rare Earth", "@RareEarthSeries"),
    "excYNB26fhs": ("60 Minutes", "@60minutes"),
    "zE5Qd26R9ek": ("The Met", "@metmuseum"),
}
DEAD = {"kBu68hzQ4HI"}            # oembed 404 — video removed from YouTube

# institutions and broadcasters rather than the independent documentarians the
# Atlas is built on; tier 3 keeps them credited without promoting them into the
# same rank as a channel that has walked 197 sites
PALETTE = ["#7E9CB8", "#A88BB8", "#8BB89C", "#B8A07E", "#9C8BB8",
           "#B88B8B", "#7EB8B0", "#B8B07E", "#8B9CB8", "#A8B87E"]


def keyify(handle, name):
    base = handle.lstrip("@").lower()
    out = "".join(c for c in base if c.isalnum())
    return out or "".join(c for c in name.lower() if c.isalnum())


def main():
    creators = json.loads((DATA / "creators.json").read_text(encoding="utf-8"))
    videos = json.loads((DATA / "videos.json").read_text(encoding="utf-8"))

    by_handle = {(v.get("handle") or "").lower().lstrip("@"): k for k, v in creators.items()}

    unkeyed = [(s, v) for s, vs in videos.items() for v in vs if not v.get("cr")]
    print(f"unkeyed wires found: {len(unkeyed)}")

    missing = [v["id"] for s, v in unkeyed if v["id"] not in RESOLVED and v["id"] not in DEAD]
    if missing:
        sys.exit(f"ABORT: {len(missing)} id(s) not in the resolved table: {missing[:6]}")

    # ---- resolve every handle to a creator key, minting only what is new
    key_for, added = {}, []
    ci = 0
    for vid, (name, handle) in RESOLVED.items():
        h = handle.lstrip("@").lower()
        if h in by_handle:
            key_for[vid] = by_handle[h]
            continue
        k = keyify(handle, name)
        if k not in creators:
            creators[k] = {
                "name": name,
                "handle": handle,
                "subs": "seed source · pre-dates the creator index",
                "color": PALETTE[ci % len(PALETTE)],
                "tier": 3,
            }
            ci += 1
            added.append((k, name, handle))
            by_handle[h] = k
        key_for[vid] = k

    # ---- backfill
    patched, skipped = 0, []
    for site, vs in videos.items():
        for v in vs:
            if v.get("cr"):
                continue
            vid = v["id"]
            if vid in DEAD:
                skipped.append((site, vid))
                continue
            v["cr"] = key_for[vid]
            v.setdefault("added", SEED_DATE)
            patched += 1

    (DATA / "creators.json").write_text(
        json.dumps(creators, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "videos.json").write_text(
        json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- report
    print(f"  ✓ wires credited : {patched}")
    print(f"  ✓ creators added : {len(added)} (creators.json now {len(creators)})")
    for k, n, h in sorted(added, key=lambda x: x[1].lower()):
        print(f"      + {k:<28} {n}  {h}")
    boosted = collections.Counter(key_for[v['id']] for s, v in unkeyed if v['id'] in key_for)
    existing = {k: c for k, c in boosted.items() if k not in {a[0] for a in added}}
    if existing:
        print("  ✓ existing creators corrected upward:")
        for k, c in sorted(existing.items(), key=lambda x: -x[1]):
            print(f"      · {k:<28} +{c}")
    if skipped:
        print(f"\n  ! {len(skipped)} left unkeyed — video no longer on YouTube:")
        for s, vid in skipped:
            print(f"      · {vid}  on  {s}")
        print("    That embed renders as 'Video unavailable'. Remove or replace it.")

    left = sum(1 for s, vs in videos.items() for v in vs if not v.get("cr"))
    print(f"\nremaining unkeyed: {left}")


if __name__ == "__main__":
    main()
