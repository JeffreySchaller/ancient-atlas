#!/usr/bin/env python3
"""
library-drawer-land-at-top.py — Land at the library intro, not the section.

Currently: clicking a criterion opens the library drawer scrolled to
the specific section (e.g. /library/megaliths.html#scale). The user
loses the framing intro that explains the six properties together.

After: every criterion click opens the library drawer at the top of
the page, where the intro paragraphs + six-icon overview live. The
user gets the full framework and can navigate to the specific section
from there if they want.

Also forces iframe to fully reload (via about:blank cycle) so the
scroll position is always top on each criterion click.

Idempotent.

Run from the repo root:
    python3 scripts/library-drawer-land-at-top.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# Idempotency marker
if "// LAND_AT_TOP_APPLIED" in html:
    print("✓ Land-at-top already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Update openLibraryDrawer to drop the anchor + force fresh load
# ============================================================
old_url_block = """  const crit = SIGNAL_CRITERIA[criterionKey];
  const anchor = crit ? crit.anchor : criterionKey;
  const url = '/library/megaliths.html#' + anchor;

  // Update title from the criterion label
  if (titleEl) titleEl.textContent = crit ? crit.label : 'Engineering reference';

  // Set iframe src — load fresh each time so the anchor scroll triggers
  if (loading) loading.classList.remove('hidden');
  iframe.onload = () => { if (loading) loading.classList.add('hidden'); };
  iframe.onerror = () => {
    // Fallback: open in new tab if iframe fails to load
    window.open(url, '_blank', 'noopener');
    closeLibraryDrawer();
  };
  iframe.src = url;"""

new_url_block = """  // LAND_AT_TOP_APPLIED — every click lands at the intro so the user
  // sees the framing + the six-icon overview, not just one section.
  const crit = SIGNAL_CRITERIA[criterionKey];
  const fullUrl = '/library/megaliths.html';
  const sectionUrl = '/library/megaliths.html#' + (crit ? crit.anchor : criterionKey);

  // Drawer title still reflects what the user clicked — gives context
  if (titleEl) titleEl.textContent = crit ? crit.label : 'Engineering reference';

  // Force iframe to reload from scratch so scroll position is always top
  if (loading) loading.classList.remove('hidden');
  iframe.onload = () => { if (loading) loading.classList.add('hidden'); };
  iframe.onerror = () => {
    // Fallback: open in new tab if iframe fails to load
    window.open(fullUrl, '_blank', 'noopener');
    closeLibraryDrawer();
  };
  // Clear → set forces the iframe to navigate fresh and reset scroll
  iframe.src = 'about:blank';
  setTimeout(() => { iframe.src = fullUrl; }, 20);"""

if old_url_block not in html:
    sys.exit("Could not find openLibraryDrawer URL block to update.\n"
             "Did the drawer script run first?")

html = html.replace(old_url_block, new_url_block, 1)
print("✓ Drawer now lands at library top (intro + six icons) on every click")
print("  Iframe resets to about:blank then loads fresh — scroll always starts at top")

# ============================================================
# 2. Footer link also points to the full library (no anchor)
# ============================================================
old_footer = "if (footerA) footerA.href = url;"
new_footer = "if (footerA) footerA.href = sectionUrl;  // footer still deep-links so new-tab gives direct section"
if old_footer in html:
    html = html.replace(old_footer, new_footer, 1)
    print("✓ Footer 'Open in new tab' still deep-links to the section (user chose to open externally → likely wants direct)")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Land-at-top behavior applied in {HTML_PATH}")
print("  - Drawer click → library top (intro + six-icon overview)")
print("  - Footer 'Open in new tab' → deep-link to section (external context preserved)")
print("  - User builds full framework each visit; can navigate to detail from the icons")
