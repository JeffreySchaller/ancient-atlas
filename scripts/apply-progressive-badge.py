#!/usr/bin/env python3
"""
apply-progressive-badge.py — Progressive disclosure badge design.

Replaces the "OPEN QUESTION" text label approach with three layered surfaces:

  1. PULSE on appearance — detail-panel badge pulses 2 times when site opens.
     Attention moment. Catches the eye. Then settles to passive rest state.

  2. HOVER (desktop only) — educational card explaining the open-question
     concept. Two sentences, one CTA. Fades in on mouseenter, out on mouseleave.
     Suppressed on touch devices.

  3. CLICK — the criteria flip-down (unchanged), revealing engineering
     signatures present at THIS site.

Removes:
  - Pill-with-label styling from tune-badge-discoverability.py (if previously applied)
  - "Open question" inline label from buildSignalBadgeHtml

Idempotent. Safe to run multiple times.

Run from the repo root:
    python3 scripts/apply-progressive-badge.py
"""
import sys, re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# ============================================================
# Idempotency check
# ============================================================
if 'signal-hover-card' in html:
    print("✓ Progressive badge already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. REVERT: Remove the inline "Open Question" label from buildSignalBadgeHtml
#    (only if tune-badge-discoverability.py was previously run)
# ============================================================
label_with_label = """function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  const label = large ? '<span class="signal-badge-label">Open question</span>' : '';
  return `<span class="${cls}" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question — signals don't yet converge" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}${label}</span>`;
}"""

label_without_label = """function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  return `<span class="${cls}" onmouseenter="signalHover(event, '${escName}')" onmouseleave="signalHoverEnd()" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question — signals don't yet converge" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`"""

original_js = """function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  return `<span class="${cls}" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question — signals don't yet converge" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`;
}"""

new_js = """function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\\\'");
  return `<span class="${cls}" onmouseenter="signalHover(event, '${escName}')" onmouseleave="signalHoverEnd()" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question — signals don't yet converge" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`;
}"""

replaced = False
if label_with_label in html:
    html = html.replace(label_with_label, new_js, 1)
    print("✓ Reverted pill+label (from earlier tune script) and added hover handlers")
    replaced = True
elif original_js in html:
    html = html.replace(original_js, new_js, 1)
    print("✓ Added hover handlers to buildSignalBadgeHtml")
    replaced = True
else:
    sys.exit("Could not find buildSignalBadgeHtml in known form. Manual edit needed.")

# ============================================================
# 2. Revert pill-style detail badge CSS (if present), restore clean dot style + add pulse
# ============================================================
pill_detail_css = ('.detail-signal-badge{width:auto;height:auto;padding:5px 10px 5px 7px;margin-left:12px;'
    'border:1px solid rgba(201,168,76,.22);background:rgba(201,168,76,.06);border-radius:8px;'
    'display:inline-flex;align-items:center;gap:7px;opacity:.9;transition:background .15s,border-color .15s,opacity .15s,transform .15s}'
    '.detail-signal-badge:hover{background:rgba(201,168,76,.14);border-color:rgba(201,168,76,.42);opacity:1;transform:none}'
    '.detail-signal-badge svg{width:13px;height:13px}'
    '.signal-badge-label{font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.14em;font-weight:600;color:var(--champagne);white-space:nowrap;transition:color .15s}'
    '.detail-signal-badge:hover .signal-badge-label{color:var(--amber)}')

original_detail_css = '.detail-signal-badge{width:18px;height:18px;margin-left:10px}'

new_detail_css = (
    '.detail-signal-badge{width:18px;height:18px;margin-left:10px;animation:signalPulse 1.4s ease-in-out 2}'
    '@keyframes signalPulse{0%,100%{transform:scale(1);opacity:.9;filter:drop-shadow(0 0 0 rgba(201,168,76,0))}50%{transform:scale(1.35);opacity:1;filter:drop-shadow(0 0 6px rgba(201,168,76,.55))}}'
    # Hover educational card (desktop only)
    '.signal-hover-card{position:fixed;width:260px;background:rgba(13,13,18,.97);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(201,168,76,.28);border-radius:11px;padding:13px 15px 12px;box-shadow:0 12px 36px rgba(0,0,0,.55);z-index:9999;opacity:0;transform:translateY(-4px);pointer-events:none;transition:opacity .18s ease,transform .18s ease;font-family:var(--font-sans);color:var(--cloud)}'
    '.signal-hover-card.show{opacity:1;transform:translateY(0)}'
    '.signal-hover-eyebrow{font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.16em;color:var(--champagne);font-weight:700;margin-bottom:6px}'
    '.signal-hover-body{font-size:12px;line-height:1.55;color:var(--cloud)}'
    '.signal-hover-cta{margin-top:8px;font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--champagne)}'
)

if pill_detail_css in html:
    html = html.replace(pill_detail_css, new_detail_css, 1)
    print("✓ Reverted pill CSS, applied pulse + hover-card styles")
elif original_detail_css in html:
    html = html.replace(original_detail_css, new_detail_css, 1)
    print("✓ Added pulse animation + hover-card styles")
else:
    sys.exit("Could not find .detail-signal-badge CSS. Manual edit needed.")

# ============================================================
# 3. Inject hover card div before </body>
# ============================================================
hover_div = '<div id="signal-hover-card" class="signal-hover-card" aria-hidden="true"></div>\n'
html = html.replace('</body>', hover_div + '</body>', 1)
print("✓ Injected #signal-hover-card div")

# ============================================================
# 4. Inject JS handlers (signalHover, signalHoverEnd)
# ============================================================
new_handlers = r'''

// Touch device detection — suppresses hover cards on tablets/phones
const SIGNAL_IS_TOUCH = ('ontouchstart' in window || navigator.maxTouchPoints > 0);

let _signalHoverTimer = null;
function signalHover(evt, siteName) {
  if (SIGNAL_IS_TOUCH) return;
  // Don't show hover card if criteria card is already open (avoid stacking)
  const criteriaCard = document.getElementById('signal-card');
  if (criteriaCard && criteriaCard.classList.contains('open')) return;

  clearTimeout(_signalHoverTimer);
  _signalHoverTimer = setTimeout(() => {
    const hc = document.getElementById('signal-hover-card');
    if (!hc) return;
    hc.innerHTML = `
      <div class="signal-hover-eyebrow">Open question</div>
      <div class="signal-hover-body">Mainstream and independent readings of this site don't yet converge. The atlas marks the question rather than picking the verdict.</div>
      <div class="signal-hover-cta">Click for engineering signatures →</div>
    `;
    const rect = evt.target.closest('.signal-badge').getBoundingClientRect();
    const cardW = 260;
    let left = rect.left + (rect.width / 2) - (cardW / 2);
    let top = rect.bottom + 8;
    left = Math.max(8, Math.min(window.innerWidth - cardW - 8, left));
    if (top + 140 > window.innerHeight - 8) {
      top = Math.max(8, rect.top - 140 - 8);
    }
    hc.style.left = left + 'px';
    hc.style.top = top + 'px';
    hc.classList.add('show');
  }, 180);  // small delay so brief mouse-overs don't trigger it
}

function signalHoverEnd() {
  clearTimeout(_signalHoverTimer);
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
}
'''

# Find the existing SIGNAL block to attach to (right after closeSignalCard function)
anchor = 'window.addEventListener(\'scroll\', closeSignalCard, true);'
if anchor not in html:
    sys.exit(f"Could not find anchor '{anchor}' for handler injection")
html = html.replace(anchor, anchor + new_handlers, 1)
print("✓ Injected signalHover + signalHoverEnd handlers")

# ============================================================
# 5. Make sure openSignalCard closes the hover card too (so they don't stack)
# ============================================================
old_open = "function openSignalCard(evt, siteName) {"
new_open = "function openSignalCard(evt, siteName) {\n  signalHoverEnd();  // close educational card if open"
if old_open not in html:
    sys.exit("Could not find openSignalCard")
html = html.replace(old_open, new_open, 1)
print("✓ Patched openSignalCard to dismiss hover card")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Progressive badge applied to {HTML_PATH}")
print("  Reload and click an open-question site.")
print("  - Badge pulses twice when detail panel opens")
print("  - Hovering the badge shows a small educational card (desktop)")
print("  - Clicking opens the criteria card (existing)")
print("  - Touch devices skip the hover layer; pulse + click only")
