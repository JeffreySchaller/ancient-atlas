#!/usr/bin/env python3
"""
library-drawer-no-flash.py — Fix landing position + flash on drawer open.

Two issues to address:
  1. Iframe lands somewhere mid-page (browser is restoring scroll from
     previous navigation with #precision)
  2. Brief white flash visible during the about:blank → real URL transition

Fixes:
  1. Drop the about:blank reset
  2. Append cache-busting query (?_=Date.now()) so browser sees a fresh URL
     and doesn't restore scroll position
  3. Force scrollTo(0,0) on iframe content after onload — belt-and-suspenders
  4. Add z-index to loading overlay so it sits on top of the iframe (covers
     any momentary content gap with the dark obsidian background)

Idempotent.

Run from the repo root:
    python3 scripts/library-drawer-no-flash.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if "// NO_FLASH_APPLIED" in html:
    print("✓ No-flash fix already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Replace the URL-load block (drop about:blank, add cache-bust + scrollTo)
# ============================================================
old_url_block = """  // LAND_AT_TOP_APPLIED — every click lands at the intro so the user
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

new_url_block = """  // NO_FLASH_APPLIED — eliminate about:blank flash + force scroll-to-top
  const crit = SIGNAL_CRITERIA[criterionKey];
  const fullUrl = '/library/megaliths.html';
  const sectionUrl = '/library/megaliths.html#' + (crit ? crit.anchor : criterionKey);

  if (titleEl) titleEl.textContent = crit ? crit.label : 'Engineering reference';

  // Show loading overlay BEFORE swapping src so dark background covers transition
  if (loading) loading.classList.remove('hidden');

  const scrollIframeTop = () => {
    try {
      if (iframe.contentWindow) iframe.contentWindow.scrollTo(0, 0);
      if (iframe.contentDocument) {
        const de = iframe.contentDocument.documentElement;
        const bd = iframe.contentDocument.body;
        if (de) de.scrollTop = 0;
        if (bd) bd.scrollTop = 0;
      }
    } catch(e) { /* sandbox or cross-origin */ }
  };

  iframe.onload = () => {
    // Force scroll to top even if browser tried to restore
    scrollIframeTop();
    requestAnimationFrame(scrollIframeTop);
    setTimeout(scrollIframeTop, 80);
    // Hide loading overlay after content is visibly at top
    setTimeout(() => { if (loading) loading.classList.add('hidden'); }, 120);
  };
  iframe.onerror = () => {
    window.open(fullUrl, '_blank', 'noopener');
    closeLibraryDrawer();
  };

  // Cache-busting query — browser sees a fresh URL each click → no scroll
  // restoration from previous navigation
  iframe.src = fullUrl + '?_=' + Date.now();"""

if old_url_block not in html:
    sys.exit("Could not find LAND_AT_TOP block to replace.\n"
             "Did library-drawer-land-at-top.py run first?")

html = html.replace(old_url_block, new_url_block, 1)
print("✓ URL load logic rewritten: cache-busting + scrollTo + delayed loading hide")

# ============================================================
# 2. Add z-index to loading overlay so it covers the iframe properly
# ============================================================
old_loading_css = ".library-drawer-loading{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--mist);font-size:12px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.12em;background:var(--obsidian);transition:opacity .2s}"
new_loading_css = ".library-drawer-loading{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--mist);font-size:12px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.12em;background:var(--obsidian);transition:opacity .2s;z-index:2}"

if old_loading_css not in html:
    sys.exit("Could not find loading overlay CSS to update z-index on")

html = html.replace(old_loading_css, new_loading_css, 1)
print("✓ Loading overlay z-index added — now covers iframe during transition")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ No-flash + reliable scroll-to-top applied in {HTML_PATH}")
print("  - No more about:blank flash")
print("  - Cache-busting URL prevents scroll restoration")
print("  - scrollTo fires after onload + rAF + 80ms timeout (belt + suspenders + braces)")
print("  - Loading overlay covers iframe during the brief load window")
