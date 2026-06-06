#!/usr/bin/env python3
"""
badge-stop-after-three-cycles.py — Cap badge animation at 3 cycles + respect
prefers-reduced-motion.

Changes from continuous animation:
  1. Edge flow: 3 iterations (was infinite). 6s each = 18s total.
     Plus a chained fade animation: opacity drops to 0 in the final 20%
     of the duration, so the conic gradient doesn't leave "stuck highlights"
     once it stops.
  2. Dot pulse: 3 iterations each (was infinite). Sequential offsets:
       sd-top: 0s start → ends at 18s
       sd-bl:  2s start → ends at 20s
       sd-br:  4s start → ends at 22s
     Each dot completes its 3 pulses then rests at champagne baseline.
  3. @media (prefers-reduced-motion: reduce) — disables both animations.
     Users with system accessibility preference see a static pill.

Rationale:
  - 3 cycles fits the human attention research window (orientation reflex
    catches eye in first ~3 cycles; persistent motion past that creates
    attention bleed competing with reading).
  - WCAG 2.2.2 allows >5s motion if it stops on its own; 18s of meaningful
    signaling that then ceases is well within best practice.

Idempotent.

Run from the repo root:
    python3 scripts/badge-stop-after-three-cycles.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'edgeFade' in html and 'prefers-reduced-motion' in html and 'edgeFlow 6s linear 3' in html:
    print("✓ 3-cycle stop already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Edge flow: infinite → 3 iterations + chained fade
# ============================================================
old_edge = "animation:edgeFlow 6s linear infinite;pointer-events:none;z-index:1}"
new_edge = "animation:edgeFlow 6s linear 3,edgeFade 18s linear forwards;pointer-events:none;z-index:1}"
if old_edge not in html:
    sys.exit("Could not find edge flow animation declaration to cap")
html = html.replace(old_edge, new_edge, 1)
print("✓ Edge flow: 3 iterations + chained fade-to-zero opacity")

# Add the edgeFade keyframes right after the edgeFlow keyframes
anchor = '@keyframes edgeFlow{to{--signal-angle:360deg}}'
fade_kf = '@keyframes edgeFade{0%,80%{opacity:1}100%{opacity:0}}'
if anchor not in html:
    sys.exit("Could not find edgeFlow keyframes anchor")
html = html.replace(anchor, anchor + fade_kf, 1)
print("✓ Added edgeFade keyframes (graceful fade-out in last 20% of duration)")

# ============================================================
# 2. Dot pulses: each 3 iterations (was infinite)
# ============================================================
dot_replacements = [
    ("animation:dotPulse 6s ease-in-out infinite 0s",  "animation:dotPulse 6s ease-in-out 3 0s forwards"),
    ("animation:dotPulse 6s ease-in-out infinite 2s",  "animation:dotPulse 6s ease-in-out 3 2s forwards"),
    ("animation:dotPulse 6s ease-in-out infinite 4s",  "animation:dotPulse 6s ease-in-out 3 4s forwards"),
]
for old_d, new_d in dot_replacements:
    if old_d in html:
        html = html.replace(old_d, new_d, 1)
print(f"✓ Dot pulses: 3 iterations each, forwards fill-mode (rest at champagne)")

# ============================================================
# 3. prefers-reduced-motion accessibility query
# ============================================================
prm_css = '@media (prefers-reduced-motion:reduce){.detail-signal-badge::before{animation:none;opacity:0}.detail-signal-badge svg circle{animation:none}}'

# Find a sensible insertion point — right after the dot pulse keyframes
dot_kf_anchor = '@keyframes dotPulse{0%,25%,100%{fill:rgba(201,168,76,.55)}10%,17%{fill:rgba(232,185,96,1)}}'
if dot_kf_anchor not in html:
    sys.exit("Could not find dotPulse keyframes for prefers-reduced-motion anchor")
html = html.replace(dot_kf_anchor, dot_kf_anchor + prm_css, 1)
print("✓ Added prefers-reduced-motion media query (static pill for accessibility users)")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Animation behavior tuned in {HTML_PATH}")
print("  - Edge flow: 3 cycles, then fades to zero (no stuck highlights)")
print("  - Dots: 3 pulses each, rest at champagne baseline")
print("  - prefers-reduced-motion: static pill for accessibility users")
print("  - Total animation window: ~18-22 seconds, then ambient calm")
