#!/usr/bin/env python3
"""
add-new-video-badge.py — Add "NEW" badge to recently-added walkthroughs.

Schema addition: optional "added" ISO date field on video entries.
Behavior:
  - Videos with `added` within the last 30 days → render small "NEW" pill
  - Videos without the field → render nothing extra (backwards-compatible)
  - Auto-disappears after 30 days (no manual cleanup)

Touches:
  1. CSS: .video-new-badge style (champagne pill, top-right of thumbnail)
  2. JS: helper isRecentlyAdded(dateStr) → boolean
  3. JS: detail-panel video card render — adds <span class="video-new-badge">NEW</span>
     before video title when isRecentlyAdded
  4. JS: mobile feed video card render — same treatment
  5. Backfill: tag recent Russia + Spean Praptos walkthroughs with today's date
     so they show NEW immediately

Idempotent.

Run from the repo root:
    python3 scripts/add-new-video-badge.py
"""
import sys, json, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'
DATA_DIR = REPO_ROOT / 'data'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")
if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}")

with open(HTML_PATH) as f:
    html = f.read()

# ============================================================
# A. HTML/CSS/JS patches (idempotent on this marker)
# ============================================================
if 'video-new-badge' in html:
    print("· UI already injected — skipping HTML/CSS/JS portion")
    html_changed = False
else:
    html_changed = True

    # 1. CSS for the NEW badge
    NEW_CSS = (
        '.video-new-badge{display:inline-block;font-family:var(--font-mono);'
        'font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;'
        'color:#0D0D12;background:linear-gradient(135deg,#E8B960,#C9A84C);'
        'padding:3px 7px;border-radius:5px;line-height:1;'
        'box-shadow:0 1px 5px rgba(232,185,96,.4);vertical-align:middle;'
        'margin-right:7px;flex-shrink:0}'
    )
    if '</style>' not in html:
        sys.exit("Could not find </style>")
    html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
    print("✓ Injected .video-new-badge CSS")

    # 2. JS helper: isRecentlyAdded(dateStr)
    HELPER_JS = """

// NEW badge helper — true if the video was added in the last 30 days
function isRecentlyAdded(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') return false;
  const added = new Date(dateStr);
  if (isNaN(added.getTime())) return false;
  const days = (Date.now() - added.getTime()) / 86400000;
  return days >= 0 && days <= 30;
}
"""
    # Inject after SIGNAL_CRITERIA definition (a clean stable spot)
    anchor = "const SIGNAL_BADGE_SVG"
    if anchor in html:
        html = html.replace(anchor, HELPER_JS + '\n' + anchor, 1)
        print("✓ Injected isRecentlyAdded helper")
    else:
        # Fallback — put it near const PATRONS
        anchor = "const PATRONS = [];"
        if anchor in html:
            html = html.replace(anchor, anchor + HELPER_JS, 1)
            print("✓ Injected isRecentlyAdded helper (alt anchor)")
        else:
            sys.exit("Could not find anchor for helper injection")

    # 3. Detail panel video card render — find the title <h3> and prepend NEW pill
    old_video_html = '<h3 style="margin:0 0 4px;font-size:13px;line-height:1.35">${v.title}</h3>'
    new_video_html = '<h3 style="margin:0 0 4px;font-size:13px;line-height:1.35">${isRecentlyAdded(v.added) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</h3>'
    if old_video_html in html:
        html = html.replace(old_video_html, new_video_html, 1)
        print("✓ Detail-panel video card now shows NEW badge")
    else:
        print("⚠ Could not find detail-panel video card title — schema may differ. Skipping (UI will work for sites without recent videos but pill won't render).")

    # 4. Mobile feed video card render — same pattern
    # The mobile feed renders videos with .mf-video-title or similar
    # Look for the rendering function
    mf_variations = [
        # Common pattern in mobile feed
        ('<div class="mf-video-title">${v.title}</div>',
         '<div class="mf-video-title">${isRecentlyAdded(v.added) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</div>'),
        # Alternative
        ('<div class="mf-vid-title">${v.title}</div>',
         '<div class="mf-vid-title">${isRecentlyAdded(v.added) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</div>'),
    ]
    for old_mf, new_mf in mf_variations:
        if old_mf in html:
            html = html.replace(old_mf, new_mf, 1)
            print(f"✓ Mobile feed video card now shows NEW badge")
            break
    else:
        print("· Mobile feed video card pattern not found (may not exist in this build, no harm done)")

    # Write HTML changes
    with open(HTML_PATH, 'w') as f:
        f.write(html)

# ============================================================
# B. Backfill `added` for recent batches (Russia + Spean Praptos)
# ============================================================
RECENT_VIDEO_IDS = {
    # Russia batch
    "qBin7G3n4eE",  # Caucasus dolmens (UIY)
    "85cDo54GFlo",  # Arkaim (UIY)
    "NvzxNm3Mxcs",  # Remote Wilderness (UIY broad survey)
    "J1QDP-Oqcr0",  # Khara-Hora Shaft (UIY)
    "n-at6AZIsoI",  # ANOTHER Pre-Historic (Chusovo Wall, UIY)
    "aPyw-yiKTMY",  # Hyperborean (UIY → Chusovo Wall)
    # Spean Praptos
    "u8Q_mrWMDuY",  # Praveen Mohan
}

today = datetime.date.today().isoformat()

videos_path = DATA_DIR / 'videos.json'
with open(videos_path) as f:
    videos = json.load(f)

tagged = 0
for site, vlist in videos.items():
    for v in vlist:
        if v.get('id') in RECENT_VIDEO_IDS and not v.get('added'):
            v['added'] = today
            tagged += 1

if tagged:
    with open(videos_path, 'w') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Backfilled `added: {today}` on {tagged} recent video entries")
else:
    print("\n· No recent videos needed backfilling")

# ============================================================
# C. Run build.py so public/index.html + public/data/ pick up changes
# ============================================================
if html_changed or tagged:
    print("\nRunning build.py to refresh public/index.html + public/data/…")
    import subprocess
    build_script = REPO_ROOT / 'scripts' / 'build.py'
    if build_script.exists():
        r = subprocess.run(['python3', str(build_script)], capture_output=True, text=True)
        print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
        if r.returncode != 0:
            print("BUILD FAILED:", r.stderr)
            sys.exit(1)

print(f"\n✓ NEW badge installed")
print("  Future add-* scripts should set added: <today> on video entries")
print("  Badge auto-disappears 30 days after the `added` date")
