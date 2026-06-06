#!/usr/bin/env python3
"""
fix-marker-hover-title-wrap.py — Wrap long titles in map marker hover cards.

The .hp-name class (title in the hover card that appears over a map marker)
had no overflow handling. Long titles like "Thracian Megaliths (Buzovgrad)"
got truncated mid-word by the card's overflow:hidden with no ellipsis.

Fix:
  - Allow word wrap (break-word)
  - Cap at 2 lines with -webkit-line-clamp + ellipsis as fallback
  - Visible result: title wraps naturally to 2 lines, ellipsis if even
    that overflows

Also patches .hp-mini-name (cluster grid mini cards) which already had
white-space:nowrap + ellipsis — those stay as-is since they're tighter.

Idempotent.

Run from the repo root:
    python3 scripts/fix-marker-hover-title-wrap.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# Idempotency — look for our line-clamp marker
if '.hp-name{font-family:\'Fraunces\',serif;font-size:16px;font-weight:600;color:#F0EEE9;line-height:1.2;margin-bottom:3px;letter-spacing:-0.01em;word-wrap' in html:
    print("✓ Hover card title wrap already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# Replace .hp-name CSS with wrap-aware version
# ============================================================
old_rule = ".hp-name{font-family:'Fraunces',serif;font-size:16px;font-weight:600;color:#F0EEE9;line-height:1.2;margin-bottom:3px;letter-spacing:-0.01em}"
new_rule = ".hp-name{font-family:'Fraunces',serif;font-size:16px;font-weight:600;color:#F0EEE9;line-height:1.2;margin-bottom:3px;letter-spacing:-0.01em;word-wrap:break-word;overflow-wrap:break-word;display:-webkit-box;-webkit-line-clamp:2;line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}"

if old_rule not in html:
    sys.exit("Could not find .hp-name CSS rule to patch — has it been hand-edited?")

html = html.replace(old_rule, new_rule, 1)
print("✓ .hp-name now wraps to 2 lines with ellipsis fallback")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Map marker hover card titles fixed in {HTML_PATH}")
print("  Long titles like 'Thracian Megaliths (Buzovgrad)' now wrap cleanly.")
