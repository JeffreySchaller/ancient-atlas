#!/usr/bin/env python3
"""
fix-video-stop-on-toggle.py — Fix the bug where toggling Network or km/mi
destroys the YouTube iframe in the right-side detail card and stops the
playing video.

Three changes:

1. Annotate each <span class="nearby-dist"> with data-km="<value>" so the
   underlying distance is recoverable without re-rendering.

2. Add updateNearbyDistances() helper that surgically rewrites the text
   content of all .nearby-dist nodes using fmtDist() against the current
   useMetric state. No iframe touch, no innerHTML wipe.

3. Replace the km/mi onclick to call updateNearbyDistances() instead of
   showDetail(selectedSite). Video keeps playing.

4. Bonus: add a subtle pulse to the km/mi button the first time Network
   is enabled in a session, so the toggle's affordance is discoverable.

Idempotent.

Run from the repo root:
    python3 scripts/fix-video-stop-on-toggle.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

MARKER = "function updateNearbyDistances"
if MARKER in html:
    print("· updateNearbyDistances already installed. Nothing to do.")
    sys.exit(0)

changes = 0

# ============================================================
# 1. Annotate .nearby-dist spans with data-km so distance survives DOM
# ============================================================
old_nearby = '<span class="nearby-dist">${fmtDist(n.dist)}</span>'
new_nearby = '<span class="nearby-dist" data-km="${n.dist}">${fmtDist(n.dist)}</span>'
if old_nearby not in html:
    sys.exit("Could not find .nearby-dist span to annotate.")
html = html.replace(old_nearby, new_nearby, 1)
print("  ✓ Annotated .nearby-dist with data-km attribute")
changes += 1

# ============================================================
# 2. Inject the surgical updater helper
# ============================================================
HELPER = """

// Surgically update nearby distances in-place when useMetric flips.
// This avoids re-running showDetail(), which would wipe the right card's
// innerHTML and kill the playing YouTube iframe.
function updateNearbyDistances() {
  document.querySelectorAll('.nearby-dist[data-km]').forEach(el => {
    const km = parseFloat(el.dataset.km);
    if (!isNaN(km)) el.textContent = fmtDist(km);
  });
}

// Subtle one-shot pulse on the km/mi toggle the first time Network is
// activated in a session, so the affordance is discoverable.
let _unitPulseShown = false;
function pulseUnitToggleOnce() {
  if (_unitPulseShown) return;
  _unitPulseShown = true;
  const btn = document.querySelector('.unit-toggle');
  if (!btn) return;
  btn.classList.add('unit-attention');
  setTimeout(() => btn.classList.remove('unit-attention'), 2400);
}
"""

# Inject before toggleNetwork or function fmtDist
helper_anchors = ["function fmtDist", "function toggleNetwork", "function renderNetwork"]
helper_done = False
for anchor in helper_anchors:
    if anchor in html:
        html = html.replace(anchor, HELPER + '\n' + anchor, 1)
        print(f"  ✓ Injected updateNearbyDistances helper before `{anchor}`")
        helper_done = True
        break
if not helper_done:
    sys.exit("Could not anchor the helper injection.")
changes += 1

# ============================================================
# 3. Replace the km/mi click handler to be surgical
# ============================================================
old_unit = "unitBtn.onclick = () => { useMetric = !useMetric; renderFilters(); renderNetwork(); if (selectedSite) showDetail(selectedSite); };"
new_unit = "unitBtn.onclick = () => { useMetric = !useMetric; renderFilters(); renderNetwork(); updateNearbyDistances(); };"
if old_unit not in html:
    print("  ⚠ Could not find the exact km/mi click handler.")
    print("    Look for `unitBtn.onclick = () =>` near the km/mi toggle definition.")
else:
    html = html.replace(old_unit, new_unit, 1)
    print("  ✓ km/mi onclick now updates distances in place, no full re-render")
    changes += 1

# ============================================================
# 4. Trigger the one-shot pulse when Network is enabled
# ============================================================
old_toggle = """function toggleNetwork() {
  showNetwork = !showNetwork;
  renderFilters();
  renderNetwork();
  renderBroadcastControls();
}"""
new_toggle = """function toggleNetwork() {
  showNetwork = !showNetwork;
  renderFilters();
  renderNetwork();
  renderBroadcastControls();
  if (showNetwork) {
    // Defer to next frame so the freshly-rendered button is present in the DOM
    requestAnimationFrame(pulseUnitToggleOnce);
  }
}"""
if old_toggle in html:
    html = html.replace(old_toggle, new_toggle, 1)
    print("  ✓ toggleNetwork now triggers one-shot pulse on km/mi button")
    changes += 1
else:
    print("  ⚠ Could not find toggleNetwork to add pulse trigger (non-critical)")

# ============================================================
# 5. Add the pulse CSS
# ============================================================
PULSE_CSS = (
    '.unit-toggle.unit-attention{'
    'animation:unitPulse 1.2s ease-out 2;'
    'box-shadow:0 0 0 0 rgba(201,168,76,.55)}'
    '@keyframes unitPulse{'
    '0%{box-shadow:0 0 0 0 rgba(201,168,76,.55)}'
    '60%{box-shadow:0 0 0 12px rgba(201,168,76,0)}'
    '100%{box-shadow:0 0 0 0 rgba(201,168,76,0)}}'
)
if PULSE_CSS not in html and '</style>' in html:
    html = html.replace('</style>', PULSE_CSS + '\n</style>', 1)
    print("  ✓ Injected unit-attention pulse CSS")
    changes += 1

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Done. {changes} edit(s) applied to public/index.html.")
print(f"  Run scripts/build.py and reload, then test on a site with video:")
print(f"  1. Click a site, play its walkthrough")
print(f"  2. Click Network (video should KEEP playing, km/mi pulses once)")
print(f"  3. Click km/mi (video should KEEP playing, distances flip in place)")
