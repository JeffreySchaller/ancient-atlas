#!/usr/bin/env python3
"""Ask YouTube's oEmbed endpoint about every wire in data/videos.json.

A 404 means the video is gone (deleted, private, or taken down) and the embed
on that site page renders as "Video unavailable". A 401 means embedding is
disabled. Anything else is live.

Needs network, so it runs on the Mac, not in the container.
Writes a TSV report; makes no changes to any data file.
"""
import json
import pathlib
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
VIDEOS = REPO / "data" / "videos.json"
OUT = pathlib.Path.home() / "Downloads" / "atlas-wire-check.tsv"

videos = json.loads(VIDEOS.read_text())
wires = {}
for site, lst in videos.items():
    for w in lst:
        wires.setdefault(w["id"], {"sites": [], "title": w.get("title", ""),
                                   "cr": w.get("cr", "")})["sites"].append(site)

ids = sorted(wires)
print(f"checking {len(ids)} unique ids across {len(videos)} sites", flush=True)


def check(vid):
    url = ("https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com"
           f"%2Fwatch%3Fv%3D{vid}&format=json")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                body = json.loads(r.read())
                return vid, r.status, body.get("author_name", "")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 2:
                continue
            return vid, e.code, ""
        except Exception as e:
            if attempt < 2:
                continue
            return vid, -1, type(e).__name__
    return vid, -1, "retries exhausted"


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, ids))

rows = []
for vid, code, author in results:
    w = wires[vid]
    rows.append((code, vid, w["cr"], author, w["title"], "; ".join(w["sites"])))
rows.sort(key=lambda r: (r[0] == 200, r[0]))

with OUT.open("w") as f:
    f.write("status\tid\tcredited_key\toembed_author\ttitle\tsites\n")
    for r in rows:
        f.write("\t".join(str(x) for x in r) + "\n")

bad = [r for r in rows if r[0] != 200]
print(f"{len(rows) - len(bad)} live, {len(bad)} not returning 200", flush=True)
for r in bad:
    print(f"  {r[0]}  {r[1]}  {r[5]}  {r[4][:60]}", flush=True)
print(f"report: {OUT}", flush=True)
