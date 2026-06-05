#!/usr/bin/env python3
"""
audit-videos.py — Audit the VIDEOS data in ancient-atlas-v6.html

Reports:
  1. Total video count across all sites
  2. Multi-site documentaries (same video ID indexed against multiple sites)
     — these are CORRECT editorially; the mobile feed handles them via badges
  3. TRUE duplicates (same site name appearing twice in VIDEOS object)
     — these are BUGS to fix immediately
  4. Distribution of multi-site coverage

Run from the project root: python3 audit-videos.py
"""
import re, sys, os
from collections import defaultdict, Counter

# Look for v6.html in current directory, then deploy/index.html
candidates = ['ancient-atlas-v6.html', 'deploy/index.html', 'index.html']
src = None
for c in candidates:
    if os.path.exists(c):
        src = c; break
if not src:
    print("Could not find ancient-atlas-v6.html or deploy/index.html in current directory.")
    sys.exit(1)

print(f"Auditing: {src}\n")

with open(src) as f:
    html = f.read()

m = re.search(r'const VIDEOS = (\{.*?\n\};)', html, re.DOTALL)
if not m:
    print("Could not find the VIDEOS object. Is this the right file?")
    sys.exit(1)
blob = m.group(1)

# Track each "Site Name": [...] block
site_pattern = re.compile(r'"([^"]+)"\s*:\s*\[(.*?)\](?=,\s*"|\s*\})', re.DOTALL)
id_pattern = re.compile(r'id:"([^"]+)".*?title:"([^"]+)"', re.DOTALL)

id_to_sites = defaultdict(list)
id_to_titles = {}
site_appearances = Counter()
total_videos = 0

for site_match in site_pattern.finditer(blob):
    site = site_match.group(1)
    site_appearances[site] += 1
    for id_m in id_pattern.finditer(site_match.group(2)):
        vid_id = id_m.group(1)
        total_videos += 1
        id_to_sites[vid_id].append(site)
        id_to_titles[vid_id] = id_m.group(2)

# 1. Real duplicates: same site name appearing twice
real_dups = {site: count for site, count in site_appearances.items() if count > 1}
print("=" * 60)
print("1. TRUE DUPLICATE site keys (BUGS — should be 0)")
print("=" * 60)
if real_dups:
    for site, count in real_dups.items():
        print(f"  BUG  {site!r} appears {count}x in VIDEOS object")
else:
    print("  No duplicate site keys found.")
print()

# 2. Multi-site documentaries
multi = {v: s for v, s in id_to_sites.items() if len(s) > 1}
print("=" * 60)
print("2. Multi-site documentaries (handled by badges)")
print("=" * 60)
print(f"  Total videos: {total_videos}")
print(f"  Multi-site docs: {len(multi)}")
print(f"  Single-site videos: {total_videos - sum(len(s) for s in multi.values())}")
print()

# 3. Distribution
counts = Counter(len(s) for s in multi.values())
print("=" * 60)
print("3. Distribution of multi-site coverage")
print("=" * 60)
for n in sorted(counts, reverse=True):
    print(f"  {n} sites covered: {counts[n]} videos")
print()

# 4. Top 10
sorted_multi = sorted(multi.items(), key=lambda x: -len(x[1]))
print("=" * 60)
print("4. Top 10 broadest documentaries")
print("=" * 60)
for vid, sites in sorted_multi[:10]:
    print(f"  [{len(sites)} sites] {id_to_titles[vid][:55]}")
    print(f"    id={vid}  →  {', '.join(sites)}")
    print()
