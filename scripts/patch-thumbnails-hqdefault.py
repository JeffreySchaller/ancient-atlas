#!/usr/bin/env python3
"""
patch-thumbnails-hqdefault.py — CDN robustness fix.

YouTube's mqdefault.jpg (320x180) sometimes returns a 120x90 grey
placeholder for newly-uploaded videos while hqdefault.jpg (480x360)
already works. Same for default.jpg (120x90), which can return the
grey placeholder during early CDN propagation.

We saw this for bnslsxXi3RY (Ancient Atlas Derinkuyu walkthrough)
on 2026-06-09: hqdefault returned a real 480x360 frame, but mqdefault
returned the 120x90 placeholder. The atlas rendered the placeholder
as a broken-looking thumbnail in the Derinkuyu site card.

Fix: every thumbnail render switches to hqdefault.jpg, which is
universally available for any live YouTube video. Slightly larger
file but the aspect ratio is identical and the visual lift is real.

Touches:
    public/index.html       — main atlas (8 mqdefault, 1 default)
    public/contribute.html  — contribute page (any mqdefault refs)

Idempotent. Run from repo root:
    python3 scripts/patch-thumbnails-hqdefault.py
    python3 scripts/build.py    # (no-op for this patch but standard)
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TARGETS = [
    REPO_ROOT / 'public' / 'index.html',
    REPO_ROOT / 'public' / 'contribute.html',
]

# These are the YouTube thumbnail size variants. We're collapsing
# everything to hqdefault since it's the smallest universally-available
# variant. mqdefault and default both have CDN-propagation gaps.
REPLACEMENTS = [
    ('/mqdefault.jpg', '/hqdefault.jpg'),
    ('/default.jpg',   '/hqdefault.jpg'),
]

def main():
    total_changes = 0
    for path in TARGETS:
        if not path.exists():
            print(f"  · Skipping (not found): {path.name}")
            continue
        text = path.read_text(encoding='utf-8')
        changes = 0
        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count:
                # Only count YouTube thumbnail URLs, not unrelated paths
                # by anchoring to the i.ytimg.com host
                # We rely on the fact that these substrings only appear
                # in the i.ytimg.com URL patterns in our codebase.
                text = text.replace(old, new)
                changes += count
                print(f"  ✓ {path.name}: {old} → {new}  ({count}x)")
        if changes:
            path.write_text(text, encoding='utf-8')
            total_changes += changes
        else:
            print(f"  · {path.name}: no changes (already hqdefault)")

    print(f"\n--- summary ---")
    print(f"  Total replacements: {total_changes}")
    if total_changes:
        print("\nNow run: python3 scripts/build.py")

if __name__ == '__main__':
    main()
