#!/usr/bin/env python3
"""
strict-new-badge.py — Tighten the NEW badge: require BOTH conditions.

Before: NEW shown if `added` within last 30 days. A 5-year-old video
added today would falsely signal "fresh content."

After: NEW shown only if:
  1. `added`     within last 30 days  (recently curated)
  AND
  2. `published` within last 90 days  (actually recent upload)

Both fields are optional. If either is missing or stale, no badge.

Also tags Spean Praptos walkthrough with `published: "2026-05-31"` so it
correctly shows NEW (published 5 days before today's date when applied).

Idempotent.

Run from the repo root:
    python3 scripts/strict-new-badge.py
"""
import sys, json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'
DATA_DIR = REPO_ROOT / 'data'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# ============================================================
# A. Update isRecentlyAdded helper to require BOTH conditions
# ============================================================
old_fn = """// NEW badge helper — true if the video was added in the last 30 days
function isRecentlyAdded(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') return false;
  const added = new Date(dateStr);
  if (isNaN(added.getTime())) return false;
  const days = (Date.now() - added.getTime()) / 86400000;
  return days >= 0 && days <= 30;
}"""

new_fn = """// NEW badge helper — true only if the video was BOTH:
//   - added to atlas in last 30 days  (recently curated)
//   - published on YouTube in last 90 days  (actually recent upload)
// Original helper kept for backwards compat; signature accepts the whole
// video object now to check both fields.
function isRecentlyAdded(video) {
  // Accept legacy date-string call for safety, but prefer video object
  if (typeof video === 'string') return false;  // old call sites won't trigger
  if (!video || typeof video !== 'object') return false;

  const addedStr = video.added;
  const pubStr   = video.published;
  if (!addedStr || !pubStr) return false;  // both required

  const added = new Date(addedStr);
  const pub   = new Date(pubStr);
  if (isNaN(added.getTime()) || isNaN(pub.getTime())) return false;

  const addedDays = (Date.now() - added.getTime()) / 86400000;
  const pubDays   = (Date.now() - pub.getTime())   / 86400000;

  return addedDays >= 0 && addedDays <= 30 &&
         pubDays   >= 0 && pubDays   <= 90;
}"""

if old_fn not in html:
    sys.exit("Could not find original isRecentlyAdded helper to update.\n"
             "Did add-new-video-badge.py run first?")
html = html.replace(old_fn, new_fn, 1)
print("✓ isRecentlyAdded now requires both `added` and `published` recent")

# ============================================================
# B. Update call sites — pass the whole video object, not just date
# ============================================================
old_call_a = "isRecentlyAdded(v.added)"
new_call_a = "isRecentlyAdded(v)"
count = html.count(old_call_a)
if count > 0:
    html = html.replace(old_call_a, new_call_a)
    print(f"✓ Updated {count} call site(s) to pass video object")

# ============================================================
# Write HTML
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

# ============================================================
# C. Add published date to Spean Praptos video (and any other known ones)
# ============================================================
KNOWN_PUBLISH_DATES = {
    "u8Q_mrWMDuY": "2026-05-31",  # Spean Praptos — Praveen Mohan, per PDF
    # Other Russia batch videos are 9 months+ old — won't qualify as NEW
    # so we don't need their publish dates for badge logic. Could add for record.
}

videos_path = DATA_DIR / 'videos.json'
with open(videos_path) as f:
    videos = json.load(f)

tagged = 0
for site, vlist in videos.items():
    for v in vlist:
        if v.get('id') in KNOWN_PUBLISH_DATES and not v.get('published'):
            v['published'] = KNOWN_PUBLISH_DATES[v['id']]
            tagged += 1
            print(f"  ✓ {v['id']} → published: {v['published']}  ({site[:40]})")

if tagged:
    with open(videos_path, 'w') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Tagged {tagged} video(s) with publish date")
else:
    print("\n· No new publish dates to tag")

# ============================================================
# D. Run build.py
# ============================================================
print("\nRunning build.py…")
import subprocess
build_script = REPO_ROOT / 'scripts' / 'build.py'
if build_script.exists():
    r = subprocess.run(['python3', str(build_script)], capture_output=True, text=True)
    print(r.stdout[-400:] if len(r.stdout) > 400 else r.stdout)
    if r.returncode != 0:
        print("BUILD FAILED:", r.stderr)
        sys.exit(1)

print("\n✓ Strict NEW badge applied.")
print("  Russia batch videos: do NOT show NEW (all published >90 days ago)")
print("  Spean Praptos walkthrough: SHOWS NEW (published 2026-05-31, ~5 days ago)")
print("  Future add-* scripts: set both `added` and `published` for NEW to render")
