#!/usr/bin/env python3
"""
add-goatcounter-analytics.py — privacy-first visitor analytics (2026-07-15)

WHY: Netlify logs only retain 7 days and can't dedupe visitors; the Reddit
post + SEO ramp need durable daily-uniques + referrer history. GoatCounter:
free, no cookies (no consent banner needed), ~3KB script, GDPR-friendly.

Site code: **ancientatlas** → dashboard at https://ancientatlas.goatcounter.com
NOTE: Jeff must register that exact code at https://www.goatcounter.com/signup
(2 minutes, free). Until then the beacon 404s silently — harmless; data starts
flowing the moment the account exists. The map's ?site=NAME deep links are
recorded as distinct query strings, so per-site interest inside the SPA is
visible too.

DOES (idempotent):
  1. Inserts the GoatCounter snippet before </head> in:
     public/index.html, contact.html, contribute.html, library/*.html
  2. Patches scripts/build-seo-pages.py page_shell so all 616+ generated
     site pages carry it (takes effect on next build.py run).
  3. favicon fix: copies favicon-32.png → favicon.ico (browsers request
     /favicon.ico automatically; it was 404ing ~90% of the time).

Run from repo root, then python3 scripts/build.py.
"""
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PUB = REPO_ROOT / "public"

SNIPPET = (
    '<script data-goatcounter="https://ancientatlas.goatcounter.com/count" '
    'async src="//gc.zgo.at/count.js"></script>\n</head>'
)
MARK = "ancientatlas.goatcounter.com"


def patch_html(path):
    html = path.read_text(encoding="utf-8")
    if MARK in html:
        print(f"  · {path.relative_to(REPO_ROOT)} already patched")
        return
    if "</head>" not in html:
        sys.exit(f"ABORT: no </head> in {path}")
    html = html.replace("</head>", SNIPPET, 1)
    path.write_text(html, encoding="utf-8")
    print(f"  ✓ {path.relative_to(REPO_ROOT)}")


def main():
    # 1. static pages
    targets = [PUB / "index.html", PUB / "contact.html", PUB / "contribute.html"]
    targets += sorted((PUB / "library").glob("*.html"))
    for t in targets:
        patch_html(t)

    # 2. SEO page generator template
    gen = REPO_ROOT / "scripts" / "build-seo-pages.py"
    src = gen.read_text(encoding="utf-8")
    if MARK in src:
        print("  · build-seo-pages.py already patched")
    else:
        anchor = "<style>{CSS}</style>"
        if anchor not in src:
            sys.exit("ABORT: generator anchor not found")
        src = src.replace(
            anchor,
            anchor + '\n<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>',
            1,
        )
        gen.write_text(src, encoding="utf-8")
        print("  ✓ build-seo-pages.py template patched (site pages get it on next build)")

    # 3. favicon.ico
    ico = PUB / "favicon.ico"
    if ico.exists():
        print("  · favicon.ico exists")
    else:
        shutil.copy2(PUB / "favicon-32.png", ico)
        print("  ✓ favicon.ico created from favicon-32.png")

    print("\nNext step : python3 scripts/build.py")
    print("Jeff step : register code 'ancientatlas' at https://www.goatcounter.com/signup")


if __name__ == "__main__":
    sys.exit(main())
