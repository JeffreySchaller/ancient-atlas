#!/usr/bin/env python3
"""
check-title-drift.py — does a stored title still match YouTube's?

Why this exists: on 2026-09-07 the Ageless Rock conversation was found stored
under its original question-form title while YouTube served a retitled version.
Nothing caught it, because the oEmbed step in .github/workflows/ci.yml has been
commented out since Phase 1 waiting on a scripts/verify-pr.py that was never
written. A retitle is invisible until someone happens to look at both.

Scope: first-party rows only (cr == 'ancientatlas' in videos.json, plus every
entry and reply in conversations.json). Those are the titles we control and
therefore the ones that drift. Checking all 911 wires would take minutes and
rate-limit; check-dead-wires.py already covers the whole corpus on demand.

Exit codes:
    0  no drift, or drift found while running as a warning (the CI default)
    1  drift found AND --strict was passed

    python3 scripts/check-title-drift.py            # warn, never blocks CI
    python3 scripts/check-title-drift.py --strict   # fail the build on drift
    python3 scripts/check-title-drift.py --selftest # prove it discriminates
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST_KEY = "ancientatlas"
OEMBED = "https://www.youtube.com/oembed?url={}&format=json"


def fetch_title(vid):
    """Live title from YouTube, or None if the video is gone or unreachable."""
    url = OEMBED.format(urllib.parse.quote(
        f"https://www.youtube.com/watch?v={vid}", safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "ancient-atlas-ci"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r).get("title")


def first_party_rows():
    """[(id, stored_title, where)] for everything we publish ourselves."""
    rows = []
    videos = json.loads((ROOT / "data/videos.json").read_text())
    for site, wires in videos.items():
        for w in wires:
            if w.get("cr") == HOST_KEY:
                rows.append((w["id"], w.get("title", ""), f"videos.json · {site}"))
    convs = json.loads((ROOT / "data/conversations.json").read_text())
    for e in convs.get("conversations", []):
        ep = e.get("episode", "?")
        if e.get("id"):
            rows.append((e["id"], e.get("title", ""), f"conversations.json · {ep}"))
        reply = e.get("reply") or {}
        if reply.get("id"):
            rows.append((reply["id"], reply.get("title", ""),
                         f"conversations.json · {ep} reply"))
    # one row per id; a conversation is site-keyed nowhere, a video may be many-keyed
    seen, unique = set(), []
    for vid, title, where in rows:
        if vid in seen:
            continue
        seen.add(vid)
        unique.append((vid, title, where))
    return unique


def compare(rows, fetch=fetch_title):
    drift, gone = [], []
    for vid, stored, where in rows:
        try:
            live = fetch(vid)
        except Exception as exc:
            gone.append((vid, where, str(exc)[:60]))
            continue
        if live is None:
            gone.append((vid, where, "no title in oEmbed response"))
        elif live != stored:
            drift.append((vid, where, stored, live))
    return drift, gone


def selftest():
    """The verifier's job is to reject the bad case, not bless the good one."""
    good = [("aaaaaaaaaaa", "Exactly Right", "fixture")]
    bad = [("bbbbbbbbbbb", "The Old Title", "fixture")]
    titles = {"aaaaaaaaaaa": "Exactly Right", "bbbbbbbbbbb": "The New Title"}
    d, _ = compare(good, fetch=lambda v: titles[v])
    assert d == [], f"clean case should not drift, got {d}"
    d, _ = compare(bad, fetch=lambda v: titles[v])
    assert len(d) == 1 and d[0][2] == "The Old Title" and d[0][3] == "The New Title", d
    d, g = compare([("ccccccccccc", "x", "fixture")],
                   fetch=lambda v: (_ for _ in ()).throw(OSError("404")))
    assert len(g) == 1 and not d, (d, g)
    print("selftest: clean passes, drift is caught, unreachable is reported  OK")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    strict = "--strict" in sys.argv
    rows = first_party_rows()
    print(f"checking {len(rows)} first-party titles against YouTube oEmbed\n")
    drift, gone = compare(rows)
    for vid, where, stored, live in drift:
        print(f"DRIFT  {vid}  ({where})")
        print(f"       stored: {stored}")
        print(f"       live:   {live}")
    for vid, where, why in gone:
        print(f"UNREACHABLE  {vid}  ({where})  {why}")
    if not drift and not gone:
        print("no drift")
    print(f"\n{len(drift)} drifted, {len(gone)} unreachable, "
          f"{len(rows) - len(drift) - len(gone)} matched")
    if drift and strict:
        print("\nFAIL: --strict and titles have drifted.")
        return 1
    if drift:
        print("\nWarning only. Re-run with --strict to make this block the build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
