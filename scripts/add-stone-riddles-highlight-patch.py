#!/usr/bin/env python3
"""
add-stone-riddles-highlight-patch.py — Stone Riddles hub highlight (2026-07-13)

Jeff: "should Stone Riddles be highlighted anywhere? Not all the videos —
we don't want Latest overwhelmed — but maybe two of their latest?"

Mechanics of the Creator Hub Latest view:
  - Only wires WITH a `published` field enter the stream at all
    (deliberate curation lever — the other 64 SR wires stay archive-only).
  - The "Recent · NEW" rail required added<=30d AND published<=90d.
    Stone Riddles' latest uploads are ~8 months old, so real dates alone
    can't surface them — and we don't fabricate dates (editorial policy).

This patch, honestly:
  1. DATA — stamps TRUE publish dates on their 2 latest uploads:
       uCQlsruon8s  "Mysterious walls at Hyrtakina"        2025-11-03
       FxSgUJVt7gk  "The acropolis of ancient Polyrrhenia"  2025-10-31
  2. DISPLAY (public/index.html) — adds a second badge tier
     "New to the Atlas": added<=30d + published present but older than
     90d → surfaces in the Recent rail with a teal-tinted badge, sorted
     after the true-NEW cards (stream is published-desc, so this happens
     naturally). Intro text updated to explain both badges.

Idempotent — safe to re-run. Run from repo root, then build.py.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
HTML = REPO_ROOT / "public" / "index.html"

STAMPS = {  # id -> true YouTube publish date
    "uCQlsruon8s": "2025-11-03",
    "FxSgUJVt7gk": "2025-10-31",
}

# ---- display-logic edits: (old, new, must_exist_after) ----
CSS_OLD = ".video-new-badge{display:inline-block;"
CSS_ADD = (
    ".video-curated-badge{background:linear-gradient(135deg,#7FC4BA,#5A9E94);"
    "box-shadow:0 1px 5px rgba(90,158,148,.4)}\n"
)

HELPER_ANCHOR = "const SIGNAL_BADGE_SVG ="
HELPER_ADD = """// "New to the Atlas" helper — recently CURATED (added <=30d) wire whose
// upload is older than the 90-day NEW window. Surfaces channel-sweep
// highlights honestly: the badge claims curation recency, not upload recency.
function isNewlyCurated(v) {
  if (!v || typeof v !== 'object') return false;
  if (isRecentlyAdded(v)) return false;
  if (!v.added || !v.published) return false;
  const added = new Date(v.added);
  if (isNaN(added.getTime())) return false;
  const addedDays = (Date.now() - added.getTime()) / 86400000;
  return addedDays >= 0 && addedDays <= 30;
}

"""

BADGE_OLD = """      const newBadge = (typeof isRecentlyAdded === 'function' && isRecentlyAdded(v))
        ? '<span class="video-new-badge">New</span>' : '';"""
BADGE_NEW = """      const newBadge = (typeof isRecentlyAdded === 'function' && isRecentlyAdded(v))
        ? '<span class="video-new-badge">New</span>'
        : (typeof isNewlyCurated === 'function' && isNewlyCurated(v))
        ? '<span class="video-new-badge video-curated-badge">New to the Atlas</span>' : '';"""

FILTER_OLD = """    const recent = allLatest.filter(v => isNewFn(v));
    const earlier = allLatest.filter(v => !isNewFn(v));"""
FILTER_NEW = """    const isCuratedFn = (typeof isNewlyCurated === 'function') ? isNewlyCurated : (() => false);
    const recent = allLatest.filter(v => isNewFn(v) || isCuratedFn(v));
    const earlier = allLatest.filter(v => !isNewFn(v) && !isCuratedFn(v));"""

INTRO_OLD = ": `Every walkthrough sorted by <strong>publish date</strong>. <strong>Recent</strong> uploads (last 30 days) surface at the top with the <em>New</em> badge. Below: every prior walkthrough in chronological order. Click any card to jump to its site.`;"
INTRO_NEW = ": `Every walkthrough sorted by <strong>publish date</strong>. <strong>Recent</strong> uploads surface at the top with the <em>New</em> badge; <em>New to the Atlas</em> marks freshly curated walkthroughs from the archive. Below: every prior walkthrough in chronological order. Click any card to jump to its site.`;"


def main():
    # 1. data — stamp published dates
    with open(DATA / "videos.json", encoding="utf-8") as f:
        videos = json.load(f)
    hit = 0
    for wires in videos.values():
        for v in wires:
            if v.get("id") in STAMPS:
                want = STAMPS[v["id"]]
                if v.get("published") == want:
                    print(f"  · {v['id']} already stamped {want}")
                else:
                    v["published"] = want
                    print(f"  ✓ stamped {v['id']} published={want}")
                hit += 1
    if hit != len(STAMPS):
        sys.exit(f"ABORT: expected {len(STAMPS)} wires, found {hit}")
    with open(DATA / "videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # 2. display logic
    html = HTML.read_text(encoding="utf-8")
    changed = False

    if ".video-curated-badge{" not in html:
        if CSS_OLD not in html:
            sys.exit("ABORT: CSS anchor not found")
        html = html.replace(CSS_OLD, CSS_ADD + CSS_OLD, 1)
        print("  ✓ CSS: .video-curated-badge added")
        changed = True
    else:
        print("  · CSS already patched")

    if "function isNewlyCurated(" not in html:
        if HELPER_ANCHOR not in html:
            sys.exit("ABORT: helper anchor not found")
        html = html.replace(HELPER_ANCHOR, HELPER_ADD + HELPER_ANCHOR, 1)
        print("  ✓ helper isNewlyCurated() added")
        changed = True
    else:
        print("  · helper already present")

    for old, new, label in (
        (BADGE_OLD, BADGE_NEW, "badge logic"),
        (FILTER_OLD, FILTER_NEW, "recent-rail filter"),
        (INTRO_OLD, INTRO_NEW, "intro text"),
    ):
        if new in html:
            print(f"  · {label} already patched")
        elif old in html:
            html = html.replace(old, new, 1)
            print(f"  ✓ {label} patched")
            changed = True
        else:
            sys.exit(f"ABORT: {label} anchor not found")

    if changed:
        HTML.write_text(html, encoding="utf-8")
        print(f"  ✓ wrote {HTML.name}")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
