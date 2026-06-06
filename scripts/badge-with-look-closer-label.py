#!/usr/bin/env python3
"""
badge-with-look-closer-label.py — Add labeled pill to the detail-panel badge.

The hover card was elegant but required discovery. A professional UX designer
would just label the click target. So:

  Before: ···                    (bare dots, ambiguous affordance)
  After:  [ ··· Look closer ]    (labeled pill, unambiguous)

The pill keeps:
  - Three-dot triangulation glyph (unique visual identifier)
  - Pulse animation on appearance (attention)
  - Click opens criteria card (existing)

The hover card is removed (now redundant — label does the educational job).
Sidebar dots stay compact (no label, space-constrained).

Idempotent.

Run from the repo root:
    python3 scripts/badge-with-look-closer-label.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'Look closer' in html:
    print("✓ 'Look closer' label already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Pill CSS for the detail-panel badge
# ============================================================
# Find the current detail-signal-badge CSS and replace
# Could be in two forms — the pulse-only version OR our earlier pill version
forms = [
    # Current form (after refine: pulse-only, bare dots)
    '.detail-signal-badge{width:18px;height:18px;margin-left:10px;animation:signalPulse 1.8s ease-in-out 3}',
    # If somehow earlier polish-style pill is still there
    '.detail-signal-badge{width:18px;height:18px;margin-left:10px;animation:signalPulse 1.4s ease-in-out 2}',
]

pill_css = (
    # Labeled pill, animated on first appearance
    '.detail-signal-badge{width:auto;height:auto;padding:6px 11px 6px 8px;margin-left:12px;'
    'border:1px solid rgba(201,168,76,.28);background:rgba(201,168,76,.07);border-radius:9px;'
    'display:inline-flex;align-items:center;gap:7px;'
    'transition:background .15s,border-color .15s,transform .15s;'
    'animation:signalPulse 1.8s ease-in-out 3;cursor:pointer}'
    '.detail-signal-badge:hover{background:rgba(201,168,76,.16);border-color:rgba(201,168,76,.5);transform:translateY(-1px)}'
    '.detail-signal-badge svg{width:13px;height:13px}'
    # Label inside pill
    '.signal-pill-label{font-family:var(--font-sans);font-size:11.5px;color:var(--champagne);font-weight:600;letter-spacing:.01em;white-space:nowrap;line-height:1}'
    '.detail-signal-badge:hover .signal-pill-label{color:var(--amber)}'
)

replaced = False
for form in forms:
    if form in html:
        html = html.replace(form, pill_css, 1)
        replaced = True
        print(f"✓ Pill CSS applied (replaced existing form)")
        break

if not replaced:
    sys.exit("Could not find existing detail-signal-badge CSS form to replace — manual check needed")

# Adjust signalPulse keyframes to also account for new pill (slight glow rather than scale-only)
# The existing keyframes are fine — pill scales just like dots did, looks natural

# ============================================================
# 2. Update buildSignalBadgeHtml to include the label
# ============================================================
# It may currently be the sticky-hover version (with onmouseenter handlers)
# OR a simpler version. Find and replace.

forms_js = [
    # Sticky hover version (most likely current)
    ('''function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  return `<span class="${cls}" onmouseenter="signalHover(event, '${escName}')" onmouseleave="signalHoverEnd()" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question · click to learn more" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`;
}'''),
    # Simpler version (without hover handlers)
    ('''function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  return `<span class="${cls}" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question · click to learn more" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`;
}'''),
]

new_js = '''function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  const label = large ? '<span class="signal-pill-label">Look closer</span>' : '';
  return `<span class="${cls}" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question · click for engineering signatures" role="button" aria-label="View engineering signature">${SIGNAL_BADGE_SVG}${label}</span>`;
}'''

js_replaced = False
for form in forms_js:
    if form in html:
        html = html.replace(form, new_js, 1)
        js_replaced = True
        print(f"✓ buildSignalBadgeHtml updated — pill includes 'Look closer' label")
        break

if not js_replaced:
    print("⚠ Could not find buildSignalBadgeHtml in known form — please verify manually")

# ============================================================
# 3. Hover card is now redundant — disable it
# ============================================================
# The hover card behavior was: hover → educational card → click → criteria
# Now the label handles "learn more" affordance directly, so we don't need the
# hover step. Make the signalHover function a no-op.

old_hover_top = "function signalHover(evt, siteName) {\n  if (SIGNAL_IS_TOUCH) return;\n  const criteriaCard = document.getElementById('signal-card');\n  if (criteriaCard && criteriaCard.classList.contains('open')) return;\n\n  clearTimeout(_signalHoverTimer);"

# We'll keep the hover handlers as no-ops to preserve idempotency of older patches
# Simplest: just add an early return at the top
disable_marker = "// DISABLED: hover card replaced by labeled pill\n  return;\n  "
new_hover_top = "function signalHover(evt, siteName) {\n  " + disable_marker + "if (SIGNAL_IS_TOUCH) return;\n  const criteriaCard = document.getElementById('signal-card');\n  if (criteriaCard && criteriaCard.classList.contains('open')) return;\n\n  clearTimeout(_signalHoverTimer);"

if old_hover_top in html:
    html = html.replace(old_hover_top, new_hover_top, 1)
    print("✓ Hover card behavior disabled (replaced by labeled pill)")
else:
    # might already be disabled, or signature differs slightly
    print("· Hover top not in expected form — skipping (may already be addressed)")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Labeled badge applied to {HTML_PATH}")
print("  Detail-panel badge now reads:  [ ··· Look closer ]")
print("  Pulse still runs on appearance. Click opens criteria card.")
print("  Hover card disabled — the pill teaches what the dots couldn't.")
