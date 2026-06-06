#!/usr/bin/env python3
"""
audit-videos.py — Phase 2 version.

Reads data/videos.json directly (no more HTML parsing) and reports:
  1. Multi-site documentaries (handled by mobile feed badges)
  2. Duplicate video IDs in the same site (bugs)
  3. Distribution of multi-site coverage
  4. Unknown creator references (warning)

Run from the repo root:
    python3 scripts/audit-videos.py

Exits with non-zero status on validation errors so CI can use it as a gate.
"""
import json, sys, os
from pathlib import Path
from collections import defaultdict, Counter

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}")

# Load
with open(DATA_DIR / 'videos.json') as f:
    videos = json.load(f)
with open(DATA_DIR / 'creators.json') as f:
    creators = json.load(f)
with open(DATA_DIR / 'sites.json') as f:
    sites = json.load(f)
site_names = {s['n'] for s in sites}
known_creators = set(creators.keys())

# Tally
id_to_sites = defaultdict(list)
total_videos = 0
duplicates_in_site = []
unknown_creators_used = defaultdict(set)
orphan_site_keys = set()

for site_name, vid_list in videos.items():
    if site_name not in site_names:
        orphan_site_keys.add(site_name)
    seen_ids_in_site = set()
    for v in vid_list:
        vid = v.get('id')
        cr = v.get('cr')
        if not vid:
            continue
        if vid in seen_ids_in_site:
            duplicates_in_site.append((site_name, vid))
        seen_ids_in_site.add(vid)
        id_to_sites[vid].append(site_name)
        if cr and cr not in known_creators:
            unknown_creators_used[cr].add(site_name)
        total_videos += 1

multi = {v: s for v, s in id_to_sites.items() if len(s) > 1}
single = total_videos - sum(len(s) for s in multi.values())

# ============================================================
# Report
# ============================================================
exit_code = 0

print("=" * 60)
print("1. DUPLICATE VIDEO IDs WITHIN A SITE (BUGS — should be 0)")
print("=" * 60)
if duplicates_in_site:
    exit_code = 1
    for site, vid in duplicates_in_site:
        print(f"  BUG  Site {site!r} has video ID {vid!r} listed twice")
else:
    print("  No duplicates within sites.")
print()

print("=" * 60)
print("2. ORPHAN SITE KEYS (videos.json keys not in sites.json)")
print("=" * 60)
if orphan_site_keys:
    for k in sorted(orphan_site_keys):
        print(f"  ⚠  videos['{k}'] but no matching site in sites.json")
    print("  (These videos won't render — site card not in catalog.)")
else:
    print("  All video keys map to known sites.")
print()

print("=" * 60)
print("3. UNKNOWN CREATOR REFERENCES")
print("=" * 60)
if unknown_creators_used:
    for cr, where in unknown_creators_used.items():
        print(f"  ⚠  Creator key {cr!r} used in {len(where)} site(s) but not in creators.json")
        for site in sorted(where)[:3]:
            print(f"       • {site}")
else:
    print("  All creator references resolve.")
print()

print("=" * 60)
print("4. MULTI-SITE DOCUMENTARIES (handled by mobile feed badges)")
print("=" * 60)
print(f"  Total walkthroughs: {total_videos}")
print(f"  Unique video IDs: {len(id_to_sites)}")
print(f"  Multi-site documentaries: {len(multi)}")
print(f"  Single-site videos: {single}")
print()

counts = Counter(len(s) for s in multi.values())
if counts:
    print("  Distribution:")
    for n in sorted(counts, reverse=True):
        print(f"    {n} sites covered: {counts[n]} videos")
print()

print("=" * 60)
print("5. TOP 10 BROADEST DOCUMENTARIES")
print("=" * 60)
sorted_multi = sorted(multi.items(), key=lambda x: -len(x[1]))
for vid, all_sites in sorted_multi[:10]:
    # Find title from first occurrence
    title = '?'
    for site_name in all_sites:
        for v in videos.get(site_name, []):
            if v.get('id') == vid:
                title = v.get('title', '?')[:55]
                break
        if title != '?':
            break
    print(f"  [{len(all_sites)} sites] {title}")
    print(f"    id={vid}  →  {', '.join(all_sites)}")
    print()

sys.exit(exit_code)
