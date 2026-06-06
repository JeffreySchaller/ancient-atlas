#!/usr/bin/env python3
"""
refine-progressive-badge.py — Three refinements to the progressive badge.

1. PULSE : 3 iterations × 1.8s instead of 2 × 1.4s.
   Slower, more breathing-like. Longer attention window.

2. HOVER CARD : minimal click-encouraging CTA.
   Before: 3-sentence educational copy
   After : eyebrow "Open Question" + line "Click to learn more →"

3. CLICK CARD : adds educational section at bottom.
   The "Open Question" explanation moves from hover to here, where it sits
   alongside the site-specific engineering signatures. One surface, full context.

Idempotent. Safe to run more than once.

Run from the repo root:
    python3 scripts/refine-progressive-badge.py
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
if 'signal-card-edu' in html:
    print("✓ Refinement already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Pulse: 2 iterations × 1.4s → 3 iterations × 1.8s
# ============================================================
old_pulse = '.detail-signal-badge{width:18px;height:18px;margin-left:10px;animation:signalPulse 1.4s ease-in-out 2}'
new_pulse = '.detail-signal-badge{width:18px;height:18px;margin-left:10px;animation:signalPulse 1.8s ease-in-out 3}'
if old_pulse not in html:
    sys.exit("Could not find pulse CSS to retime")
html = html.replace(old_pulse, new_pulse, 1)
print("✓ Pulse retimed: 3 iterations × 1.8s (5.4s total)")

# ============================================================
# 2. Hover card content → minimal CTA
# ============================================================
old_hover_content = '''hc.innerHTML = `
      <div class="signal-hover-eyebrow">Open question</div>
      <div class="signal-hover-body">Mainstream and independent readings of this site don't yet converge. The atlas marks the question rather than picking the verdict.</div>
      <div class="signal-hover-cta">Click for engineering signatures →</div>
    `;'''

new_hover_content = '''hc.innerHTML = `
      <div class="signal-hover-eyebrow">Open question</div>
      <div class="signal-hover-cta-primary">Click to learn more →</div>
    `;'''

if old_hover_content not in html:
    sys.exit("Could not find hover card innerHTML to refine")
html = html.replace(old_hover_content, new_hover_content, 1)
print("✓ Hover card simplified to click-encouraging CTA")

# Adjust hover-card height calculation since content shrunk
# (originally accounted for ~140px; now closer to 80px)
# We'll add a slimmer style for it
old_hover_card_css = '.signal-hover-card{position:fixed;width:260px;background:rgba(13,13,18,.97);'
new_hover_card_css = '.signal-hover-card{position:fixed;width:240px;background:rgba(13,13,18,.97);'
html = html.replace(old_hover_card_css, new_hover_card_css, 1)

# Add a CSS rule for the new primary CTA (larger, more prominent than the old subtle cta)
anchor_for_new_css = '.signal-hover-cta{margin-top:8px;font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--champagne)}'
new_cta_css = (
    anchor_for_new_css +
    '.signal-hover-cta-primary{margin-top:6px;font-family:var(--font-sans);font-size:13px;color:var(--champagne);font-weight:600;letter-spacing:.01em}'
)
html = html.replace(anchor_for_new_css, new_cta_css, 1)
print("✓ Hover card CTA styled for prominence")

# ============================================================
# 3. Click card: add educational section at bottom
# ============================================================
# CSS for the new educational block
anchor_card_foot = '.signal-card-foot{margin-top:8px;padding-top:10px;border-top:1px solid rgba(42,42,53,.5);text-align:right}'
new_edu_css = (
    '.signal-card-edu{margin-top:12px;padding-top:11px;border-top:1px solid rgba(42,42,53,.5)}'
    '.signal-card-edu-eyebrow{font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--champagne);font-weight:700;margin-bottom:5px}'
    '.signal-card-edu-body{font-size:11.5px;line-height:1.55;color:var(--cloud)}'
    # Adjust the foot to no longer carry the top border (the edu section now does)
    '.signal-card-foot{margin-top:10px;padding-top:8px;border-top:none;text-align:right}'
)
# Replace just the .signal-card-foot rule with the new edu CSS + adjusted foot
html = html.replace(anchor_card_foot, new_edu_css, 1)
print("✓ Educational section CSS added; card-foot top-border removed")

# Patch the click card innerHTML to include the educational section
old_card_innerHTML = '''  card.innerHTML = `
    <button class="signal-card-x" onclick="closeSignalCard()" aria-label="Close engineering signature panel">×</button>
    <div class="signal-card-title">Engineering signature · ${site.n}</div>
    ${rowsHtml}
    <div class="signal-card-foot"><a href="/library/megaliths.html" target="_blank" rel="noopener">Read the reference →</a></div>
  `;'''

new_card_innerHTML = '''  card.innerHTML = `
    <button class="signal-card-x" onclick="closeSignalCard()" aria-label="Close engineering signature panel">×</button>
    <div class="signal-card-title">Engineering signature · ${site.n}</div>
    ${rowsHtml}
    <div class="signal-card-edu">
      <div class="signal-card-edu-eyebrow">Open question</div>
      <div class="signal-card-edu-body">Mainstream and independent readings of this site don't yet converge. The atlas marks the question rather than picking the verdict.</div>
    </div>
    <div class="signal-card-foot"><a href="/library/megaliths.html" target="_blank" rel="noopener">Read the reference →</a></div>
  `;'''

if old_card_innerHTML not in html:
    sys.exit("Could not find click card innerHTML to extend")
html = html.replace(old_card_innerHTML, new_card_innerHTML, 1)
print("✓ Click card now includes educational section at bottom")

# Adjust the card height calculation (added ~70px for edu section)
old_height_calc = 'const cardH = Math.min(280, 80 + criteria.length * 48);'
new_height_calc = 'const cardH = Math.min(420, 150 + criteria.length * 48);'
if old_height_calc in html:
    html = html.replace(old_height_calc, new_height_calc, 1)
    print("✓ Card height calc adjusted for new edu section")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Progressive badge refined in {HTML_PATH}")
print("  - Pulse: 3 × 1.8s (was 2 × 1.4s)")
print("  - Hover: 'Open Question / Click to learn more →' (minimal CTA)")
print("  - Click: icons + educational section at bottom + Read the reference")
