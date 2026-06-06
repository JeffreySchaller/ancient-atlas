#!/usr/bin/env python3
"""
fix-hover-card-click.py — Fix the click-through bug on the sticky hover card.

Bug: clicking the hover card called signalHoverCardClick → openSignalCard,
which opens the criteria card. But the document-level click listener then
fires (event bubbling), sees the click was inside .signal-hover-card (not
.signal-card or .signal-badge), and calls closeSignalCard() — closing the
just-opened criteria card on the same tick.

Fix:
  1. Add .signal-hover-card to the document click listener's exclusion list
  2. Pass event to signalHoverCardClick and stopPropagation as belt-and-suspenders

Idempotent.

Run from the repo root:
    python3 scripts/fix-hover-card-click.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if "!e.target.closest('.signal-hover-card')" in html:
    print("✓ Click-through fix already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Update document click listener to also exclude .signal-hover-card
# ============================================================
old_listener = "document.addEventListener('click', e => {\n  if (!e.target.closest('.signal-card') && !e.target.closest('.signal-badge')) {\n    closeSignalCard();\n  }\n});"
new_listener = "document.addEventListener('click', e => {\n  if (!e.target.closest('.signal-card') && !e.target.closest('.signal-badge') && !e.target.closest('.signal-hover-card')) {\n    closeSignalCard();\n  }\n});"

if old_listener not in html:
    sys.exit("Could not find document click listener to patch (might already be patched in a different way)")
html = html.replace(old_listener, new_listener, 1)
print("✓ Document click listener now ignores .signal-hover-card clicks")

# ============================================================
# 2. Pass event to signalHoverCardClick + stopPropagation
# ============================================================
# Update the inline onclick attribute
old_onclick = 'onclick="signalHoverCardClick()"'
new_onclick = 'onclick="signalHoverCardClick(event)"'
if old_onclick in html:
    html = html.replace(old_onclick, new_onclick, 1)
    print("✓ Hover card onclick now passes event")

# Update the function to accept and stop the event
old_fn = """function signalHoverCardClick() {
  const siteName = _signalHoverSiteName;
  if (!siteName) return;
  _signalHoverPin = false;
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
  openSignalCard({currentTarget: hc}, siteName);
}"""

new_fn = """function signalHoverCardClick(evt) {
  if (evt) evt.stopPropagation();
  const siteName = _signalHoverSiteName;
  if (!siteName) return;
  _signalHoverPin = false;
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
  openSignalCard({currentTarget: hc}, siteName);
}"""

if old_fn in html:
    html = html.replace(old_fn, new_fn, 1)
    print("✓ signalHoverCardClick now stops event propagation")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Click-through bug fixed in {HTML_PATH}")
print("  Clicking the hover card now opens the criteria card cleanly.")
