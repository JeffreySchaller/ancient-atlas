#!/usr/bin/env python3
"""
patch-entry08-counts.py — keep Library Entry 08 in step with the corpus (2026-08-07)

Adding Cutimbo and giving Sillustani the polygonal criterion moved the corpus
from 82 to 84, and Peru from 12 to 14. Entry 08's whole method is that it counts
from the Atlas rather than from a montage, so a stale count in the prose is not
cosmetic, it undercuts the argument the entry makes about itself.

This patches the counts and the Peru row. Idempotent, and it refuses to write
if a replacement target is missing so it cannot half-apply.

Run from repo root. No build step needed - library pages are hand-authored -
but run scripts/build-seo-pages.py if the sitemap needs refreshing.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAGE = REPO_ROOT / "public" / "library" / "the-convergence-question.html"

OLD_PERU_ROW = (
    '<div class="dist-row"><div class="dist-n">12</div><div class="dist-c">'
    '<b>Peru</b><span>Sacsayhuamán, Ollantaytambo, Coricancha, Chinchero, '
    'Pisac, Rumiwasi, Tarawasi, Killarumiyoq, Vilcashuaman, Vilcabamba, '
    'Chucuito, Wari</span></div></div>'
)
NEW_PERU_ROW = (
    '<div class="dist-row"><div class="dist-n">14</div><div class="dist-c">'
    '<b>Peru</b><span>Sacsayhuamán, Ollantaytambo, Coricancha, Chinchero, '
    'Pisac, Rumiwasi, Tarawasi, Killarumiyoq, Vilcashuaman, Vilcabamba, '
    'Chucuito, Wari, and the Titicaca chullpa pair Sillustani and '
    'Cutimbo</span></div></div>'
)

REPLACEMENTS = [
    ("Eighty-two sites in twenty-one countries",
     "Eighty-four sites in twenty-one countries"),
    ("Eighty-two polygonal sites across twenty-one countries",
     "Eighty-four polygonal sites across twenty-one countries"),
    ("carries <strong>82 sites</strong> flagged",
     "carries <strong>84 sites</strong> flagged"),
    (OLD_PERU_ROW, NEW_PERU_ROW),
    ("82 sites · 21 countries · five continents",
     "84 sites · 21 countries · five continents"),
    ("alone account for 51 of the 82.",
     "alone account for 53 of the 84."),
    ("covers more of the 82 than most people expect",
     "covers more of the 84 than most people expect"),
    ("Most of the 82 need no exotic explanation.",
     "Most of the 84 need no exotic explanation."),
    ("has been done at very few of the 82",
     "has been done at very few of the 84"),
    ("Eighty-two sites, twenty-one countries. Counted from the Atlas",
     "Eighty-four sites, twenty-one countries. Counted from the Atlas"),
]


def main():
    if not PAGE.exists():
        sys.exit(f"ABORT: {PAGE} not found")
    html = PAGE.read_text(encoding="utf-8")

    applied, already, missing = 0, 0, []
    out = html
    for old, new in REPLACEMENTS:
        if old in out:
            out = out.replace(old, new)
            applied += 1
        elif new in out:
            already += 1
        else:
            missing.append(old[:60])

    if missing:
        print("ABORT: these targets matched neither old nor new text:")
        for m in missing:
            print(f"    {m!r}")
        sys.exit(1)

    if applied:
        PAGE.write_text(out, encoding="utf-8")
        print(f"  ✓ patched {applied} passages ({already} already current)")
    else:
        print(f"  · already current ({already} passages)")

    stale = [n for n in ("Eighty-two", "82 sites", "of the 82") if n in out]
    if stale:
        sys.exit(f"ABORT: stale counts survive: {stale}")
    print("  ✓ no stale counts remain")


if __name__ == "__main__":
    sys.exit(main())
