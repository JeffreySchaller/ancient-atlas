#!/usr/bin/env python3
"""
badge-electric-flow.py — Replace scale pulse with ambient electric edge flow
and sequential dot pulse.

Removes the scale animation (was overlapping the title text). Replaces with:

  1. EDGE FLOW: two soft amber "circles of light" travel slowly around the
     pill's edge using a rotating conic gradient (6s cycle).

  2. DOT PULSE: the three dots brighten in sequence:
       Top dot      at 0s
       Bottom-left  at 2s
       Bottom-right at 4s
     Each cycle is 6s, matching the edge flow rhythm.

The result is continuous ambient motion that signals interactivity without
visual jarring. The pill stays at constant size — no overlap with title.

Idempotent.

Run from the repo root:
    python3 scripts/badge-electric-flow.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'edgeFlow' in html and 'dotPulse' in html:
    print("✓ Electric flow already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Update SIGNAL_BADGE_SVG to include classes on circles for sequential pulse
# ============================================================
old_svg = "const SIGNAL_BADGE_SVG = '<svg viewBox=\"0 0 12 12\" fill=\"currentColor\"><circle cx=\"6\" cy=\"2.5\" r=\"1.45\"/><circle cx=\"2.5\" cy=\"9.5\" r=\"1.45\"/><circle cx=\"9.5\" cy=\"9.5\" r=\"1.45\"/></svg>';"
new_svg = "const SIGNAL_BADGE_SVG = '<svg viewBox=\"0 0 12 12\" fill=\"currentColor\"><circle class=\"sd-top\" cx=\"6\" cy=\"2.5\" r=\"1.45\"/><circle class=\"sd-bl\" cx=\"2.5\" cy=\"9.5\" r=\"1.45\"/><circle class=\"sd-br\" cx=\"9.5\" cy=\"9.5\" r=\"1.45\"/></svg>';"

if old_svg not in html:
    sys.exit("Could not find SIGNAL_BADGE_SVG constant to update")
html = html.replace(old_svg, new_svg, 1)
print("✓ SVG glyph: dots now have sd-top, sd-bl, sd-br classes")

# ============================================================
# 2. Replace the detail-signal-badge CSS (with scale pulse) with the new design
# ============================================================
# Possible forms of the current CSS (depending on which prior script ran last):
existing_forms = [
    # Form from badge-with-look-closer-label.py (pill + scale pulse)
    ('.detail-signal-badge{width:auto;height:auto;padding:6px 11px 6px 8px;margin-left:12px;'
     'border:1px solid rgba(201,168,76,.28);background:rgba(201,168,76,.07);border-radius:9px;'
     'display:inline-flex;align-items:center;gap:7px;'
     'transition:background .15s,border-color .15s,transform .15s;'
     'animation:signalPulse 1.8s ease-in-out 3;cursor:pointer}'
     '.detail-signal-badge:hover{background:rgba(201,168,76,.16);border-color:rgba(201,168,76,.5);transform:translateY(-1px)}'
     '.detail-signal-badge svg{width:13px;height:13px}'
     '.signal-pill-label{font-family:var(--font-sans);font-size:11.5px;color:var(--champagne);font-weight:600;letter-spacing:.01em;white-space:nowrap;line-height:1}'
     '.detail-signal-badge:hover .signal-pill-label{color:var(--amber)}'),
]

# New CSS: ambient electric edge flow + sequential dot pulse, NO scale animation
new_css = (
    # Pill base — slightly transparent dark interior, transparent border for conic-gradient overlay
    '.detail-signal-badge{position:relative;width:auto;height:auto;padding:6px 11px 6px 8px;margin-left:12px;'
    'border-radius:9px;display:inline-flex;align-items:center;gap:7px;cursor:pointer;'
    'background:rgba(22,22,29,.55);border:1px solid rgba(201,168,76,.22);'
    'transition:background .2s,border-color .2s,transform .15s}'
    '.detail-signal-badge:hover{background:rgba(30,30,40,.7);border-color:rgba(201,168,76,.45);transform:translateY(-1px)}'
    '.detail-signal-badge svg{width:13px;height:13px;position:relative;z-index:2}'
    '.signal-pill-label{font-family:var(--font-sans);font-size:11.5px;color:var(--champagne);font-weight:600;letter-spacing:.01em;white-space:nowrap;line-height:1;position:relative;z-index:2}'
    '.detail-signal-badge:hover .signal-pill-label{color:var(--amber)}'

    # @property declaration for smooth conic angle animation
    '@property --signal-angle{syntax:"<angle>";initial-value:0deg;inherits:false}'

    # Edge flow: ::before pseudo overlays the conic gradient on top of the border
    '.detail-signal-badge::before{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;'
    'background:conic-gradient(from var(--signal-angle),'
    'transparent 0deg,'
    'rgba(232,185,96,.9) 28deg,'
    'transparent 56deg,'
    'transparent 180deg,'
    'rgba(232,185,96,.9) 208deg,'
    'transparent 236deg,'
    'transparent 360deg);'
    '-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);'
    '-webkit-mask-composite:xor;mask-composite:exclude;'
    'animation:edgeFlow 6s linear infinite;pointer-events:none;z-index:1}'
    '@keyframes edgeFlow{to{--signal-angle:360deg}}'

    # Sequential dot pulse — 6s cycle, each dot brightens for ~1s
    '.detail-signal-badge svg circle{transition:fill .25s}'
    '.detail-signal-badge svg .sd-top{animation:dotPulse 6s ease-in-out infinite 0s}'
    '.detail-signal-badge svg .sd-bl{animation:dotPulse 6s ease-in-out infinite 2s}'
    '.detail-signal-badge svg .sd-br{animation:dotPulse 6s ease-in-out infinite 4s}'
    '@keyframes dotPulse{0%,25%,100%{fill:rgba(201,168,76,.55)}10%,17%{fill:rgba(232,185,96,1)}}'
)

replaced = False
for form in existing_forms:
    if form in html:
        html = html.replace(form, new_css, 1)
        replaced = True
        print("✓ Pill CSS replaced: ambient edge flow + sequential dot pulse")
        break

if not replaced:
    sys.exit("Could not find existing detail-signal-badge CSS form to replace.\n"
             "Run badge-with-look-closer-label.py first to get the pill base in place.")

# Remove the old signalPulse keyframes (no longer needed)
old_keyframes = '@keyframes signalPulse{0%,100%{transform:scale(1);opacity:.9;filter:drop-shadow(0 0 0 rgba(201,168,76,0))}50%{transform:scale(1.35);opacity:1;filter:drop-shadow(0 0 6px rgba(201,168,76,.55))}}'
if old_keyframes in html:
    html = html.replace(old_keyframes, '', 1)
    print("✓ Removed old signalPulse keyframes (no longer needed)")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Electric flow applied to {HTML_PATH}")
print("  - Pill no longer scales (no more title overlap)")
print("  - Edge: two amber bands flow around the pill perimeter (6s cycle)")
print("  - Dots pulse sequentially: top → bottom-left → bottom-right")
