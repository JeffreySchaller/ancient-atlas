#!/usr/bin/env python3
"""
finalize-badge-language.py — Bring the badge to its final intended state from
ANY starting point. Replaces polish-badge-copy-and-hover.py + tune-badge-language.py.

Detects current state of each piece and applies whatever's needed:
  1. Criteria labels → plain engineering voice (matching library)
  2. Scale label → period-specific (not "modern cranes")
  3. Educational copy → "lenses to explore" invitation (drops "mainstream")
  4. Hover card → sticky + clickable
  5. Title tooltips → consistent with hover CTA

Idempotent. Safe to run from ANY state — original, partially-polished, or
fully-polished. Just gets you to the final state.

Run from the repo root:
    python3 scripts/finalize-badge-language.py
"""
import sys, re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

print(f"Inspecting {HTML_PATH}")
print(f"File size: {len(html):,} bytes\n")

# ============================================================
# 1. Criteria labels — apply ANY → final state
# ============================================================
# Final state targets:
FINAL_LABELS = {
    'precision':    "Stones fitted without mortar, almost no gap",
    'hardness':     "Stone harder than steel",
    'scale':        "Stones heavier than the period\\'s tools could lift",
    'polygonal':    "Same interlock pattern on three continents",
    'stratigraphy': "Older layers, more advanced work",
    'geometry':     "Geometry that encodes astronomy, Earth, and the human form",
}

# Possible source forms for each label (multiple starting states)
LABEL_VARIANTS = {
    'precision': [
        "Mortarless joinery, sub-millimeter tolerance",
        "Stones fitted without mortar, almost no gap",
    ],
    'hardness': [
        "Stone harder than period tools",
        "Stone harder than steel",
    ],
    'scale': [
        "Block scale exceeds documented lift capability",
        "Stones heavier than modern cranes can lift",
        "Stones heavier than the period's tools could lift",  # already final
    ],
    'polygonal': [
        "Polygonal interlock pattern across continents",
        "Same interlock pattern on three continents",
    ],
    'stratigraphy': [
        "Stratigraphy that runs backwards",
        "Older layers, more advanced work",
    ],
    'geometry': [
        "Geometry encoding astronomy, Earth, human form",
        "Geometry that encodes astronomy, Earth, and the human form",
    ],
}

label_changes = 0
for key, variants in LABEL_VARIANTS.items():
    final = FINAL_LABELS[key]
    for variant in variants:
        # JS string literal form
        old_str = f"label: '{variant}'"
        new_str = f"label: '{final}'"
        if old_str in html and old_str != new_str:
            html = html.replace(old_str, new_str, 1)
            print(f"  ✓ {key:13s}  '{variant[:50]}' → '{final[:50]}'")
            label_changes += 1
            break
    else:
        # If we got here without break, check whether the final form is already present
        if f"label: '{final}'" in html:
            print(f"  · {key:13s}  already at final state")
        else:
            print(f"  ⚠  {key:13s}  no known form found — manual check needed")

print(f"\n→ {label_changes} criteria label(s) updated")

# ============================================================
# 2. Educational copy — apply ANY → "lenses to explore"
# ============================================================
final_edu = "This site has more than one reading. The signals above are lenses to explore it."
edu_variants = [
    "Mainstream and independent readings of this site don't yet converge. The atlas marks the question rather than picking the verdict.",
    "More than one reading of this site is in play. The signals above frame what's worth looking at. Look for yourself.",
    "This site has more than one reading. The signals above are lenses to explore it.",  # already final
]

edu_changed = False
for variant in edu_variants:
    if variant in html and variant != final_edu:
        html = html.replace(variant, final_edu, 1)
        print(f"\n✓ Educational copy reframed to: '{final_edu[:60]}...'")
        edu_changed = True
        break

if not edu_changed:
    if final_edu in html:
        print(f"\n· Educational copy already at final state")
    else:
        print(f"\n⚠  Educational copy not found in any known form — manual check needed")

# ============================================================
# 3. Title tooltip — consistent CTA
# ============================================================
old_titles = [
    'title="Open question — signals don\'t yet converge"',
]
new_title = 'title="Open question · click to learn more"'
title_changes = 0
for ot in old_titles:
    if ot in html:
        # there may be 2 occurrences (sidebar + detail)
        n = html.count(ot)
        html = html.replace(ot, new_title)
        title_changes += n
if title_changes:
    print(f"\n✓ {title_changes} title tooltip(s) updated to '{new_title}'")
elif new_title in html:
    print(f"\n· Title tooltip already consistent")

# ============================================================
# 4. Hover card sticky behavior — only if not already applied
# ============================================================
if 'signalHoverCardEnter' not in html:
    print("\nApplying sticky hover card behavior...")

    # 4a. CSS: pointer-events auto when shown + hover state
    old_css_pe = "z-index:9999;opacity:0;transform:translateY(-4px);pointer-events:none;transition:opacity .18s ease,transform .18s ease;font-family:var(--font-sans);color:var(--cloud)}"
    new_css_pe = "z-index:9999;opacity:0;transform:translateY(-4px);pointer-events:none;transition:opacity .18s ease,transform .18s ease,background .15s,border-color .15s;font-family:var(--font-sans);color:var(--cloud);cursor:pointer}.signal-hover-card.show{pointer-events:auto}.signal-hover-card.show:hover{background:rgba(18,18,26,.99);border-color:rgba(201,168,76,.45)}.signal-hover-card.show:hover .signal-hover-cta-primary{color:var(--amber)}"
    if old_css_pe in html:
        html = html.replace(old_css_pe, new_css_pe, 1)
        print("  ✓ Hover card CSS upgraded — pointer-events on when shown + hover affordance")

    # 4b. Wire mouse handlers onto the div
    old_div = '<div id="signal-hover-card" class="signal-hover-card" aria-hidden="true"></div>'
    new_div = '<div id="signal-hover-card" class="signal-hover-card" aria-hidden="true" onmouseenter="signalHoverCardEnter()" onmouseleave="signalHoverCardLeave()" onclick="signalHoverCardClick()"></div>'
    if old_div in html:
        html = html.replace(old_div, new_div, 1)
        print("  ✓ Hover card div has enter/leave/click handlers")

    # 4c. Add sticky JS helpers
    old_handlers_start = "let _signalHoverTimer = null;\nfunction signalHover(evt, siteName) {"
    new_handlers_start = """let _signalHoverTimer = null;
let _signalHoverPin = false;
let _signalHoverSiteName = null;

function signalHoverCardEnter() {
  _signalHoverPin = true;
}

function signalHoverCardLeave() {
  _signalHoverPin = false;
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
}

function signalHoverCardClick() {
  const siteName = _signalHoverSiteName;
  if (!siteName) return;
  _signalHoverPin = false;
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
  openSignalCard({currentTarget: hc}, siteName);
}

function signalHover(evt, siteName) {"""
    if old_handlers_start in html:
        html = html.replace(old_handlers_start, new_handlers_start, 1)
        print("  ✓ Sticky JS helpers added")

    # 4d. Track siteName in hover state
    old_inner = """    const hc = document.getElementById('signal-hover-card');
    if (!hc) return;"""
    new_inner = """    const hc = document.getElementById('signal-hover-card');
    if (!hc) return;
    _signalHoverSiteName = siteName;"""
    if old_inner in html:
        html = html.replace(old_inner, new_inner, 1)
        print("  ✓ siteName now tracked for sticky card click")

    # 4e. signalHoverEnd with 200ms grace period
    old_hover_end = """function signalHoverEnd() {
  clearTimeout(_signalHoverTimer);
  const hc = document.getElementById('signal-hover-card');
  if (hc) hc.classList.remove('show');
}"""
    new_hover_end = """function signalHoverEnd() {
  clearTimeout(_signalHoverTimer);
  setTimeout(() => {
    if (!_signalHoverPin) {
      const hc = document.getElementById('signal-hover-card');
      if (hc) hc.classList.remove('show');
    }
  }, 200);
}"""
    if old_hover_end in html:
        html = html.replace(old_hover_end, new_hover_end, 1)
        print("  ✓ signalHoverEnd now has 200ms grace period")
else:
    print("\n· Sticky hover behavior already applied")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Badge finalized in {HTML_PATH}")
print(f"  Reload to see the final state.")
