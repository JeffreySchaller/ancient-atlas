#!/usr/bin/env python3
"""
add-criteria-card-x.py — Add an X close button to the criteria flip-down card.

Improves mobile dismissal UX (click-outside isn't always obvious on touch).
Click-outside and Esc still work.

Idempotent. Safe to run more than once.

Run from the repo root:
    python3 scripts/add-criteria-card-x.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# Idempotency check
if 'signal-card-x' in html:
    print("✓ X close button already present. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Inject X button CSS into the signal-card block
# ============================================================
anchor_css = '.signal-card{position:fixed;width:300px;'
new_css = (
    # X button
    '.signal-card-x{position:absolute;top:6px;right:8px;width:22px;height:22px;background:transparent;border:none;'
    'color:var(--mist);font-size:18px;cursor:pointer;border-radius:6px;display:flex;align-items:center;justify-content:center;'
    'line-height:1;padding:0;transition:color .15s,background .15s;font-family:var(--font-sans);font-weight:300}'
    '.signal-card-x:hover{color:var(--ivory);background:rgba(201,168,76,.1)}'
    # Title needs right padding so it doesn't collide with X
    '.signal-card-title{padding-right:24px}'
)
if anchor_css not in html:
    sys.exit("Could not find .signal-card CSS anchor")
html = html.replace(anchor_css, new_css + anchor_css, 1)
print("✓ Injected X button CSS")

# ============================================================
# 2. Patch the openSignalCard innerHTML to include the X
# ============================================================
old_inner = '''  card.innerHTML = `
    <div class="signal-card-title">Engineering signature · ${site.n}</div>
    ${rowsHtml}'''
new_inner = '''  card.innerHTML = `
    <button class="signal-card-x" onclick="closeSignalCard()" aria-label="Close engineering signature panel">×</button>
    <div class="signal-card-title">Engineering signature · ${site.n}</div>
    ${rowsHtml}'''

if old_inner not in html:
    sys.exit("Could not find openSignalCard innerHTML to patch")
html = html.replace(old_inner, new_inner, 1)
print("✓ Added X button to card markup")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ X close button added to criteria card in {HTML_PATH}")
print("  Click-outside and Esc still work — X is the additional discoverable path.")
