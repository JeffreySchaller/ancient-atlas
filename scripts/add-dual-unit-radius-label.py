#!/usr/bin/env python3
"""
add-dual-unit-radius-label.py — Change the Nearby Sites header from
"(within 50km)" to "(within 50km / 30mi)" so the filter radius is
self-documenting in both unit systems.

The individual distances inside the list continue to respect the
global km/mi toggle. The radius itself is the filter bound — a system
constant — so it makes sense to show both units permanently.

Idempotent.

Run from the repo root:
    python3 scripts/add-dual-unit-radius-label.py
    python3 scripts/build.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

OLD = 'Nearby Sites (within 50km)'
NEW = 'Nearby Sites (within 50km / 30mi)'

if NEW in html:
    print("· Header already dual-unit. Nothing to do.")
    sys.exit(0)

if OLD not in html:
    print(f"⚠ Could not find the exact label {OLD!r}.")
    print("  Looking for variants…")
    # Try a few near-variants
    variants = [
        'Nearby Sites (within 50 km)',
        'Nearby Sites (within 50km radius)',
        'Nearby sites (within 50km)',
    ]
    for v in variants:
        if v in html:
            html = html.replace(v, NEW, 1)
            with open(HTML_PATH, 'w') as f:
                f.write(html)
            print(f"  ✓ Replaced {v!r} with dual-unit form")
            sys.exit(0)
    sys.exit("No match found. Inspect the Nearby Sites template in showDetail.")

html = html.replace(OLD, NEW, 1)
with open(HTML_PATH, 'w') as f:
    f.write(html)
print(f"✓ Header updated to: {NEW!r}")
print(f"  File: {HTML_PATH}")
