#!/usr/bin/env python3
"""
wire-convergence-entry.py — publish Library Entry 08 (2026-08-07)

Runs after tag-polygonal-corpus.py.

Three things :

1. Wires `library_ref` to /library/the-convergence-question.html on every site
   carrying the `polygonal` criterion (82 of them). This is the point of the
   entry: one article, 82 inbound links, and every one of those site pages
   gains a route into the argument.

2. Existing library_ref values are NOT overwritten. A handful of sites already
   point at True Monoliths (Sacsayhuaman and Ollantaytambo among them) and
   those are editorial choices, not defaults. The script reports which sites it
   skipped so the call can be made deliberately rather than by clobber.

3. Flips the Entry 08 card in public/library/index.html from its "in
   development" placeholder to a live link.

Idempotent - safe to re-run. Run from repo root, then python3 scripts/build.py
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
INDEX = REPO_ROOT / "public" / "library" / "index.html"
PAGE = REPO_ROOT / "public" / "library" / "the-convergence-question.html"

REF = {
    "url": "/library/the-convergence-question.html",
    "title": "The Convergence Question",
}

PLACEHOLDER = """      <div class="entry soon">
        <div class="entry-meta">Entry 08 · Method</div>
        <h3>The Convergence Question</h3>
        <p>Independent invention, lost predecessor, or something else? The strongest evidence for and against a shared origin behind the polygonal pattern that crosses continents.</p>
      </div>"""

LIVE = """      <a class="entry" href="the-convergence-question.html">
        <div class="entry-meta">Entry 08 · Method</div>
        <h3>The Convergence Question</h3>
        <p>Independent invention, lost predecessor, or something else? Eighty-two polygonal sites across twenty-one countries, the engineering that explains most of them, the Japanese masons we can name, and the Andean residue that survives every objection.</p>
        <div class="entry-arrow">Read entry →</div>
      </a>"""


def main():
    if not PAGE.exists():
        sys.exit(f"ABORT: {PAGE} not found - write the article first")

    # ------------------------------------------------------------ wiring
    path = DATA / "sites.json"
    sites = json.loads(path.read_text(encoding="utf-8"))
    before_count = len(sites)

    corpus = [s for s in sites if "polygonal" in (s.get("criteria") or [])]
    if not corpus:
        sys.exit("ABORT: no sites carry the polygonal criterion")

    wired, already, skipped = 0, 0, []
    for site in corpus:
        existing = site.get("library_ref")
        if existing == REF:
            already += 1
        elif existing:
            skipped.append((site["n"], existing.get("title")))
        else:
            site["library_ref"] = dict(REF)
            wired += 1

    if wired:
        path.write_text(
            json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"  ✓ wrote data/sites.json")
    print(f"  corpus {len(corpus)} · wired {wired} · already {already} · "
          f"left alone {len(skipped)}")
    for name, title in sorted(skipped):
        print(f"      · {name} keeps {title!r}")

    # ------------------------------------------------------------- index
    html = INDEX.read_text(encoding="utf-8")
    if LIVE in html:
        print("  · library index already live")
    elif PLACEHOLDER in html:
        INDEX.write_text(html.replace(PLACEHOLDER, LIVE), encoding="utf-8")
        print("  ✓ library index: Entry 08 is now a live link")
    else:
        print("  ! Entry 08 placeholder not matched in library/index.html "
              "- patch it by hand")

    # ------------------------------------------------------------ guards
    after = json.loads(path.read_text(encoding="utf-8"))
    if len(after) != before_count:
        sys.exit("ABORT: site count changed")
    pointing = [s["n"] for s in after
                if (s.get("library_ref") or {}).get("url") == REF["url"]]
    print(f"\n{len(pointing)} sites now point at Entry 08")
    print("Next step : python3 scripts/build.py")


if __name__ == "__main__":
    sys.exit(main())
