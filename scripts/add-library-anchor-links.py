#!/usr/bin/env python3
"""
add-library-anchor-links.py — Wire 'Featured in the Library' link onto the
four anchor sites of Library Entry 03 (Mini Megaliths).

What this does:

1. Adds a `library_ref` field to four sites in sites.json:
     - Osireion
     - Coricancha (Qorikancha)
     - Ahu Vinapu
     - Phnom Bok

   Each gets:
     "library_ref": {
       "url": "/library/mini-megaliths.html",
       "title": "Mini Megaliths"
     }

2. Patches public/index.html so the detail panel renders a small
   "Featured in the Library : Mini Megaliths →" link below the description
   whenever the active site has a library_ref.

Idempotent. Safe to re-run. Reports gracefully if site names don't match
(in which case it prints close matches you can correct manually).

Run from the repo root:
    python3 scripts/add-library-anchor-links.py
"""
import sys, json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not DATA_DIR.exists():
    sys.exit(f"data/ not found at {DATA_DIR}. Run this from the repo root.")
if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}.")

# ============================================================
# Anchor sites and the article they all point at
# ============================================================
ARTICLE = {
    "url": "/library/mini-megaliths.html",
    "title": "Mini Megaliths",
}

# Site names as they appear in sites.json (the "n" field)
# If a name doesn't match, the script will print close matches.
ANCHOR_SITES = [
    "Osireion",
    "Coricancha (Qorikancha)",
    "Ahu Vinapu",
    "Phnom Bok",
]

# ============================================================
# Step 1: sites.json
# ============================================================
sites_path = DATA_DIR / 'sites.json'
with open(sites_path) as f:
    sites = json.load(f)

if not isinstance(sites, list):
    sys.exit("sites.json is not a list — schema mismatch")

site_names = [s.get('n', '') for s in sites]
sites_updated = 0
sites_already_set = 0
sites_missing = []

for target in ANCHOR_SITES:
    found = False
    for site in sites:
        if site.get('n') == target:
            found = True
            if site.get('library_ref') == ARTICLE:
                sites_already_set += 1
                print(f"  · {target}: library_ref already set")
            else:
                site['library_ref'] = ARTICLE
                sites_updated += 1
                print(f"  ✓ {target}: library_ref added")
            break
    if not found:
        sites_missing.append(target)

# Report any missing with close matches
if sites_missing:
    print(f"\n  ⚠ {len(sites_missing)} site name(s) not found in sites.json:")
    for missing in sites_missing:
        key = missing.split('(')[0].strip().lower()
        candidates = [n for n in site_names if key and key in n.lower()]
        print(f"    · {missing!r}")
        for c in candidates[:5]:
            print(f"        candidate: {c!r}")
    print("  Edit ANCHOR_SITES in this script to match exact names, then re-run.")

if sites_updated:
    with open(sites_path, 'w') as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)
    print(f"\n  ✓ sites.json updated ({sites_updated} new, {sites_already_set} already set)")
else:
    print(f"\n  · sites.json unchanged ({sites_already_set} already set)")

# ============================================================
# Step 2: public/index.html
# ============================================================
with open(HTML_PATH) as f:
    html = f.read()

# Marker we use to detect prior installation
INSTALL_MARKER = "library-ref-card"

if INSTALL_MARKER in html:
    print("\n  · library_ref render already wired in public/index.html")
    print("\n✓ Done. Run scripts/build.py to regenerate the atlas.")
    sys.exit(0)

# ----------- 2a. CSS for the library link card -----------
LIBRARY_CSS = (
    '.library-ref-card{display:flex;align-items:center;gap:10px;'
    'margin:18px 0 6px;padding:12px 14px;'
    'border:1px solid rgba(201,168,76,.28);border-radius:8px;'
    'background:rgba(201,168,76,.05);'
    'text-decoration:none;color:var(--ivory);'
    'transition:all .15s}'
    '.library-ref-card:hover{border-color:rgba(201,168,76,.55);'
    'background:rgba(201,168,76,.10)}'
    '.library-ref-card .lr-icon{flex-shrink:0;width:22px;height:22px;'
    'color:var(--champagne);opacity:.9}'
    '.library-ref-card .lr-text{display:flex;flex-direction:column;'
    'flex:1;min-width:0;line-height:1.3}'
    '.library-ref-card .lr-eyebrow{font-family:var(--font-mono);'
    'font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;'
    'color:var(--champagne);opacity:.85;margin-bottom:2px}'
    '.library-ref-card .lr-title{font-family:var(--font-serif);'
    'font-size:14.5px;font-weight:600;font-variation-settings:"opsz" 24;'
    'color:var(--ivory)}'
    '.library-ref-card .lr-arrow{flex-shrink:0;color:var(--champagne);'
    'opacity:.7;transition:transform .15s}'
    '.library-ref-card:hover .lr-arrow{transform:translateX(3px);opacity:1}'
)

if '</style>' not in html:
    sys.exit("Could not find </style> in public/index.html")
html = html.replace('</style>', LIBRARY_CSS + '\n</style>', 1)
print("\n  ✓ Injected .library-ref-card CSS")

# ----------- 2b. Render helper (template literal builder) -----------
HELPER_JS = """

// Library reference card — renders a contextual link to a Library entry
// when the active site declares { library_ref: { url, title } }.
function renderLibraryRef(site) {
  if (!site || !site.library_ref) return '';
  const ref = site.library_ref;
  if (!ref.url || !ref.title) return '';
  const eyebrow = ref.eyebrow || 'Featured in the Library';
  return `<a class="library-ref-card" href="${ref.url}">
    <svg class="lr-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/>
      <path d="M20 4h-7a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h8z"/>
    </svg>
    <span class="lr-text">
      <span class="lr-eyebrow">${eyebrow}</span>
      <span class="lr-title">${ref.title}</span>
    </span>
    <svg class="lr-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M5 12h14M13 5l7 7-7 7"/>
    </svg>
  </a>`;
}
"""

# Inject the helper near other render helpers
helper_anchors = [
    "function renderSignalBadge",
    "function showDetail",
    "const SIGNAL_BADGE_SVG",
    "const PATRONS = [];",
]
helper_injected = False
for anchor in helper_anchors:
    if anchor in html:
        html = html.replace(anchor, HELPER_JS + '\n' + anchor, 1)
        print(f"  ✓ Injected renderLibraryRef helper (anchor: {anchor!r})")
        helper_injected = True
        break

if not helper_injected:
    sys.exit("Could not find an anchor to inject renderLibraryRef helper.\n"
             "Look for renderSignalBadge or showDetail in public/index.html.")

# ----------- 2c. Render call site (detail panel description) -----------
# Try multiple patterns the description block might use
render_patterns = [
    # Pattern: description ends, then coordinates render
    ('${site.desc}</div>',
     '${site.desc}${renderLibraryRef(site)}</div>'),
    ('${s.desc}</div>',
     '${s.desc}${renderLibraryRef(s)}</div>'),
    # Pattern: description in <p>
    ('${site.desc}</p>',
     '${site.desc}</p>${renderLibraryRef(site)}'),
    ('${s.desc}</p>',
     '${s.desc}</p>${renderLibraryRef(s)}'),
    # Pattern: directly templated
    ('<div class="site-desc">${site.desc}</div>',
     '<div class="site-desc">${site.desc}</div>${renderLibraryRef(site)}'),
    ('<div class="site-desc">${s.desc}</div>',
     '<div class="site-desc">${s.desc}</div>${renderLibraryRef(s)}'),
]

render_wired = False
for old, new in render_patterns:
    if old in html:
        html = html.replace(old, new, 1)
        print(f"  ✓ Wired renderLibraryRef into detail panel ({old[:50]!r}…)")
        render_wired = True
        break

if not render_wired:
    print("  ⚠ Could not find a description anchor to wire the render call.")
    print("    The CSS and helper are installed but the link won't appear")
    print("    until you manually add ${renderLibraryRef(site)} after the desc")
    print("    in the detail panel template (look for `site.desc` in index.html).")

# Write
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n  ✓ public/index.html updated")
print("\n✓ Done. Now run scripts/build.py to regenerate the atlas:")
print("    python3 scripts/build.py")
