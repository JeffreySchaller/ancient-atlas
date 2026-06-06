#!/usr/bin/env python3
"""
wire-new-badge-render.py — Actually wire the NEW badge into the video card render.

add-new-video-badge.py looked for `<h3>` in the video card markup but the
actual element is `<div class="vtitle">`. The helper function and CSS got
installed correctly, but the call site never fired — so no NEW pill ever
rendered.

Fix: patch the .vtitle div to call isRecentlyAdded and conditionally render
the pill before the title text.

Idempotent.

Run from the repo root:
    python3 scripts/wire-new-badge-render.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'isRecentlyAdded(v) ?' in html:
    print("✓ NEW badge render already wired. Nothing to do.")
    sys.exit(0)

# ============================================================
# Patch the .vtitle div in showDetail's video card render
# ============================================================
old_vtitle = '<div class="vtitle">${v.title}</div>'
new_vtitle = '<div class="vtitle">${isRecentlyAdded(v) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</div>'

if old_vtitle not in html:
    sys.exit("Could not find .vtitle div in detail panel video card render")

html = html.replace(old_vtitle, new_vtitle, 1)
print("✓ Detail-panel .vtitle now conditionally renders NEW badge")

# ============================================================
# Also try patching the mobile feed if present (.mf-video-title or similar)
# ============================================================
mf_variants = [
    ('<div class="mf-vtitle">${v.title}</div>',
     '<div class="mf-vtitle">${isRecentlyAdded(v) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</div>'),
    ('<div class="mf-video-title">${v.title}</div>',
     '<div class="mf-video-title">${isRecentlyAdded(v) ? \'<span class="video-new-badge">New</span>\' : \'\'}${v.title}</div>'),
]
for old, new in mf_variants:
    if old in html:
        html = html.replace(old, new, 1)
        print(f"✓ Mobile feed video title also wired")
        break

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ NEW badge render wired in {HTML_PATH}")
print("  Open a site with a recently-published-and-added video.")
print("  Spean Praptos (Kampong Kdei Bridge) is the test case.")
