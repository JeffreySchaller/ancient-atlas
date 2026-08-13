#!/usr/bin/env python3
"""
patch-editions.py — give Feel the Weight an Editions ask (2026-08-13)

The experience ended without asking for anything. Four editions* values were
computed in renderVals() and never referenced by the markup - dead code that
read, from the source alone, like a live funnel. It was not one. Nobody was
ever sent anywhere.

Worse, that dead copy sold "a measured plate of The Trilithon, archival stock,
18 x 24 in". No such product exists. The store carries the Mammoth and
Sabertooth lines and nothing else, so the copy would have been a promise the
shop could not keep.

This adds a second card to the "08 Onward" grid selling what is actually
there, and deletes the dead values so nobody re-inherits the confusion.

Idempotent. Run from repo root between extract.py and inject.py.
"""
import sys
from pathlib import Path

APP = Path(__file__).parent / "app.html"
html = APP.read_text(encoding="utf-8")

CARD = '''    <div style="background:linear-gradient(180deg,rgba(24,21,32,.72),rgba(14,12,19,.72));border:1px solid rgba(201,168,76,.22);border-radius:14px;padding:clamp(22px,3vw,30px);box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 8px 22px rgba(0,0,0,.45);display:flex;flex-direction:column;gap:13px">
      <span style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#C9A84C">Editions</span>
      <h2 style="font-size:clamp(21px,2.4vw,27px);font-weight:600;line-height:1.22;color:#F3D998;text-wrap:pretty">Keep it free.</h2>
      <p style="font-family:'JetBrains Mono',monospace;font-size:10.5px;line-height:1.85;color:#cfcbc1;letter-spacing:.02em;text-wrap:pretty">The Atlas has no ads, no tracking and no paywall, and it is going to stay that way. Editions is what pays for it — the Mammoth and the Sabertooth, printed heavyweight on good cotton, plus mugs for people who like their coffee accompanied by an extinct animal.</p>
      <div style="display:flex;flex-wrap:wrap;gap:9px;margin-top:4px">
        <a href="{{ editionsHref }}" target="_blank" rel="noopener" style="font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#241c07;padding:14px 22px;border-radius:11px;text-decoration:none;background:linear-gradient(180deg,#F0CE74,#C9A84C);border:1px solid #f0d78f">Visit Editions →</a>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:6px;border-top:1px solid rgba(201,168,76,.22);padding-top:14px">
        <a href="{{ studiesHref }}" style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#C9A84C">Creator studies →</a>
        <span style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:#807d71">Ships worldwide</span>
      </div>
    </div>
'''

ANCHOR = '''See it in your room · phase 2</span>
      </div>
    </div>
'''

# ---- 1. insert the card as the grid's second child
if 'Keep it free.' in html:
    print("  · Editions card already present")
else:
    if html.count(ANCHOR) != 1:
        sys.exit(f"ABORT: closer anchor matched {html.count(ANCHOR)} times, expected 1")
    html = html.replace(ANCHOR, ANCHOR + CARD)
    print("  ✓ Editions card added to '08 Onward'")

# ---- 2. supply the two hrefs it needs
OLDV = """      editionsBlurb: 'A measured plate of ' + s.edition + ' — the drawing, the 6-foot figure, the weight and the credit line, set the way the museum label would set it. Archival stock, 18 × 24 in.',
      editionsCta: 'Editions · ' + s.edition + ' →',
      editionsStoneHref: editionsBase + '?stone=' + s.k + '&from=immersive',
      editionsSetHref: editionsBase + '?set=feel-the-weight&from=immersive',"""
NEWV = """      /* The old editionsBlurb/Cta/StoneHref/SetHref sold "a measured plate of
         <stone>, archival stock, 18 x 24 in" and deep-linked ?stone=<key>.
         None of it was ever referenced by the markup, and no such product
         exists - the store carries the Mammoth and Sabertooth lines only. Kept
         out on purpose: do not reinstate a per-stone plate link until there is
         a per-stone plate to link to. */
      editionsHref: editionsBase + '?from=feel-the-weight',
      studiesHref: 'https://theancientatlas.com/creators/',"""
if 'editionsHref:' in html:
    print("  · renderVals already current")
elif OLDV in html:
    html = html.replace(OLDV, NEWV)
    print("  ✓ dead editions* values replaced with the two the card uses")
else:
    sys.exit("ABORT: could not find the editions* block in renderVals")

APP.write_text(html, encoding="utf-8")

# Check for the ASSIGNMENT, not the bare word - the comment above deliberately
# names these so the next reader knows why they are gone, and a substring test
# trips over its own explanation.
for tok in ('editionsBlurb', 'editionsCta', 'editionsStoneHref', 'editionsSetHref'):
    if tok + ':' in html:
        sys.exit(f"ABORT: {tok} is still being assigned")
print("  ✓ no dead editions* assignments remain")
