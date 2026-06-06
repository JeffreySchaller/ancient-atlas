#!/usr/bin/env python3
"""
tune-badge-language.py — Two language refinements.

1. SCALE LABEL: factually tightened.
   Before: "Stones heavier than modern cranes can lift"  (false — modern
   gantry cranes top out around 3,000-5,000 tons, more than any known
   megalithic block).
   After:  "Stones heavier than the period's tools could lift"  (period-
   specific, which is the actual engineering anomaly).

2. EDUCATIONAL CTA: invitation, not challenge.
   Before: "More than one reading of this site is in play. The signals
   above frame what's worth looking at. Look for yourself."
   ("Look for yourself" reads as a dare.)

   After:  "This site has more than one reading. The signals above
   are lenses to explore it."
   ("Lenses to explore" is engineering metaphor + invitation. Two
   crisp sentences. Inviting, not confrontational.)

Idempotent. Safe to re-run.

Run from the repo root:
    python3 scripts/tune-badge-language.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# Idempotency
if "lenses to explore" in html:
    print("✓ Language already tuned. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Scale label: modern cranes → period's tools
# ============================================================
old_scale = "label: 'Stones heavier than modern cranes can lift'"
new_scale = "label: 'Stones heavier than the period\\'s tools could lift'"
if old_scale not in html:
    sys.exit("Could not find scale label to retighten")
html = html.replace(old_scale, new_scale, 1)
print("✓ Scale label tightened: refers to period's tools, not modern cranes")

# ============================================================
# 2. Educational CTA: invitation via lenses metaphor
# ============================================================
old_edu = "More than one reading of this site is in play. The signals above frame what's worth looking at. Look for yourself."
new_edu = "This site has more than one reading. The signals above are lenses to explore it."
if old_edu not in html:
    sys.exit("Could not find educational CTA to soften")
html = html.replace(old_edu, new_edu, 1)
print("✓ Educational CTA reframed: invitation via lenses metaphor")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Language tuned in {HTML_PATH}")
print("  - Scale: 'Stones heavier than the period\\'s tools could lift'")
print("  - Edu:   'This site has more than one reading.")
print("           The signals above are lenses to explore it.'")
