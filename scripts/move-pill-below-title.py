#!/usr/bin/env python3
"""
move-pill-below-title.py — Move the Look-closer pill out of the title row.

Currently the pill lives inline with the h2, forcing long titles (e.g.
"Khara-Hora Shaft") to wrap. The fix: move the pill onto its own row,
right after the metadata line, just above the description.

Result:
   Khara-Hora Shaft                       ★
   📍 Asia · 🏷 Megalithic · 🎬 1 video
   [ ··· Look closer ]                       ← own row, no title interference
   A roughly 100-meter vertical shaft...

Idempotent.

Run from the repo root:
    python3 scripts/move-pill-below-title.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'signal-pill-row' in html:
    print("✓ Pill already moved below title. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Remove pill from inside h2; restore h2 to its simple form
# ============================================================
old_h2 = '<h2 style="margin:0;flex:1;display:flex;align-items:center">${site.n}${buildSignalBadgeHtml(site, true)}</h2>'
new_h2 = '<h2 style="margin:0;flex:1">${site.n}</h2>'
if old_h2 not in html:
    sys.exit("Could not find h2 with inline badge — may have a different format")
html = html.replace(old_h2, new_h2, 1)
print("✓ Pill removed from inside h2 (title no longer competes for space)")

# ============================================================
# 2. Inject pill on its own row right after the dmeta block
# ============================================================
# Anchor: closing of dmeta div followed by ddesc paragraph
old_anchor = '''      </div>
      <p class="ddesc">${site.desc}</p>'''

new_anchor = '''      </div>
      ${site.signal === 'open' ? `<div class="signal-pill-row">${buildSignalBadgeHtml(site, true)}</div>` : ''}
      <p class="ddesc">${site.desc}</p>'''

if old_anchor not in html:
    sys.exit("Could not find dmeta → ddesc transition to inject pill row.\n"
             "showDetail markup may have been customized — check manually.")
html = html.replace(old_anchor, new_anchor, 1)
print("✓ Pill row injected between metadata and description")

# ============================================================
# 3. Add CSS for the pill-row layout
# ============================================================
# Find an anchor near the detail panel CSS to insert near
css_anchor = '.detail-signal-badge{position:relative;width:auto;height:auto;padding:6px 11px 6px 8px;margin-left:12px;'
css_new_rule = (
    '.signal-pill-row{margin:14px 0 6px;display:flex}'
    '.signal-pill-row .detail-signal-badge{margin-left:0}'
)
if css_anchor in html:
    # Insert the new rule BEFORE the existing pill CSS, both stay adjacent
    html = html.replace(css_anchor, css_new_rule + css_anchor, 1)
    print("✓ .signal-pill-row CSS added; margin-left override for the pill")
else:
    sys.exit("Could not find .detail-signal-badge CSS anchor for row CSS insertion")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Pill repositioned in {HTML_PATH}")
print("  - Title now wraps naturally (no pill competing for inline space)")
print("  - Pill sits on its own row, between metadata and description")
print("  - Works for any title length, mobile and desktop")
