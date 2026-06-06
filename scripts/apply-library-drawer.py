#!/usr/bin/env python3
"""
apply-library-drawer.py — In-atlas library drawer for criterion deep-links.

Currently: clicking a criterion in the criteria card opens
/library/megaliths.html#scale in a new tab. Fragments attention.

After: clicking a criterion slides a drawer in from the right showing
the library section, anchored via iframe to the matching #id. Close the
drawer → user is back on the criteria card → back on the same site.

  Atlas →  Detail panel →  Criteria card →  Library drawer (iframe to section)
                              ↑                       ↓ (X / Esc / backdrop)
                              ←──────────────────────

Mobile: drawer becomes full-screen overlay, same dismissal mechanics.

Iframe loads the live library page anchored to #id, so library updates
flow through automatically without rebuild work. A footer link offers
"Open in new tab" as an escape hatch.

Idempotent.

Run from the repo root:
    python3 scripts/apply-library-drawer.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if 'openLibraryDrawer' in html:
    print("✓ Library drawer already installed. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. CSS for the drawer + backdrop
# ============================================================
DRAWER_CSS = """
/* ===== Library reference drawer (in-atlas mini-window) ===== */
.library-drawer-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:19999;opacity:0;transition:opacity .25s ease;pointer-events:none;backdrop-filter:blur(2px)}
.library-drawer-backdrop.show{opacity:1;pointer-events:auto}
.library-drawer{position:fixed;top:0;right:0;width:540px;max-width:100vw;height:100vh;background:rgba(13,13,18,.98);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-left:1px solid rgba(201,168,76,.22);box-shadow:-16px 0 48px rgba(0,0,0,.6);z-index:20000;transform:translateX(100%);transition:transform .3s cubic-bezier(.32,.72,0,1);display:flex;flex-direction:column;font-family:var(--font-sans)}
.library-drawer.open{transform:translateX(0)}
.library-drawer-header{padding:16px 20px;border-bottom:1px solid rgba(42,42,53,.4);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-shrink:0;background:rgba(13,13,18,.96)}
.library-drawer-eyebrow{font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.16em;color:var(--champagne);font-weight:700;margin-bottom:3px}
.library-drawer-title{font-family:var(--font-serif);font-size:17px;color:var(--ivory);font-weight:600;line-height:1.25;font-variation-settings:"opsz" 24}
.library-drawer-close{width:32px;height:32px;background:transparent;border:none;color:var(--mist);font-size:22px;cursor:pointer;border-radius:7px;display:flex;align-items:center;justify-content:center;line-height:1;font-weight:300;transition:color .15s,background .15s;flex-shrink:0}
.library-drawer-close:hover{background:rgba(201,168,76,.1);color:var(--ivory)}
.library-drawer-iframe-wrap{flex:1;position:relative;overflow:hidden;background:var(--obsidian)}
.library-drawer-iframe{width:100%;height:100%;border:none;background:var(--obsidian)}
.library-drawer-loading{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--mist);font-size:12px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.12em;background:var(--obsidian);transition:opacity .2s}
.library-drawer-loading.hidden{opacity:0;pointer-events:none}
.library-drawer-footer{padding:12px 20px;border-top:1px solid rgba(42,42,53,.4);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-shrink:0;background:rgba(13,13,18,.96)}
.library-drawer-footer-hint{font-family:var(--font-sans);font-size:11px;color:var(--mist)}
.library-drawer-footer a{color:var(--champagne);font-family:var(--font-mono);font-size:10px;text-transform:uppercase;letter-spacing:.14em;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:5px;padding:5px 9px;border-radius:7px;border:1px solid rgba(201,168,76,.25);transition:all .15s}
.library-drawer-footer a:hover{background:rgba(201,168,76,.1);border-color:rgba(201,168,76,.45);color:var(--amber)}

@media (max-width:600px){.library-drawer{width:100vw;border-left:none}.library-drawer-header{padding:14px 16px}.library-drawer-footer{padding:10px 16px}}
"""

if '</style>' not in html:
    sys.exit("Could not find </style>")
html = html.replace('</style>', DRAWER_CSS + '\n</style>', 1)
print("✓ Injected drawer CSS")

# ============================================================
# 2. Drawer HTML — inject before </body>
# ============================================================
DRAWER_HTML = """
<div id="library-drawer-backdrop" class="library-drawer-backdrop" onclick="closeLibraryDrawer()" aria-hidden="true"></div>
<aside id="library-drawer" class="library-drawer" role="dialog" aria-label="Library reference" aria-hidden="true">
  <header class="library-drawer-header">
    <div style="min-width:0;flex:1">
      <div class="library-drawer-eyebrow">Library reference</div>
      <div class="library-drawer-title" id="library-drawer-title">Engineering reference</div>
    </div>
    <button class="library-drawer-close" onclick="closeLibraryDrawer()" aria-label="Close library reference">×</button>
  </header>
  <div class="library-drawer-iframe-wrap">
    <div class="library-drawer-loading" id="library-drawer-loading">Loading…</div>
    <iframe class="library-drawer-iframe" id="library-drawer-iframe" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox" loading="lazy"></iframe>
  </div>
  <footer class="library-drawer-footer">
    <span class="library-drawer-footer-hint">Esc to close</span>
    <a href="/library/megaliths.html" target="_blank" rel="noopener" id="library-drawer-footer-link">Open in new tab →</a>
  </footer>
</aside>
"""

html = html.replace('</body>', DRAWER_HTML + '</body>', 1)
print("✓ Injected drawer HTML structure")

# ============================================================
# 3. JS: open/close drawer + Esc handler + criterion handler patching
# ============================================================
DRAWER_JS = r"""

// ============================================================
// Library drawer — opens criteria deep-links in a slide-in panel
// instead of a new tab, preserving the user's atlas context
// ============================================================
function openLibraryDrawer(criterionKey) {
  const drawer    = document.getElementById('library-drawer');
  const backdrop  = document.getElementById('library-drawer-backdrop');
  const iframe    = document.getElementById('library-drawer-iframe');
  const titleEl   = document.getElementById('library-drawer-title');
  const loading   = document.getElementById('library-drawer-loading');
  const footerA   = document.getElementById('library-drawer-footer-link');
  if (!drawer || !iframe) return;

  const crit = SIGNAL_CRITERIA[criterionKey];
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
  iframe.src = url;

  if (footerA) footerA.href = url;

  drawer.classList.add('open');
  drawer.setAttribute('aria-hidden', 'false');
  if (backdrop) backdrop.classList.add('show');
  // Prevent background scroll on mobile
  document.body.style.overflow = 'hidden';
}

function closeLibraryDrawer() {
  const drawer   = document.getElementById('library-drawer');
  const backdrop = document.getElementById('library-drawer-backdrop');
  const iframe   = document.getElementById('library-drawer-iframe');
  if (drawer) {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
  }
  if (backdrop) backdrop.classList.remove('show');
  document.body.style.overflow = '';
  // Optional: clear iframe src on close to save memory and ensure fresh load next time
  // Wait for the slide-out animation to complete first
  setTimeout(() => {
    if (iframe && drawer && !drawer.classList.contains('open')) {
      iframe.src = 'about:blank';
    }
  }, 350);
}

// Esc closes the drawer
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    const drawer = document.getElementById('library-drawer');
    if (drawer && drawer.classList.contains('open')) {
      closeLibraryDrawer();
    }
  }
});
"""

# Inject JS — anchor on the closeSignalCard function (already exists)
anchor = "function closeSignalCard() {"
if anchor not in html:
    sys.exit(f"Could not find anchor '{anchor}' for JS injection")
html = html.replace(anchor, DRAWER_JS + '\n' + anchor, 1)
print("✓ Injected drawer JS (open/close + Esc handler)")

# ============================================================
# 4. Patch openSignalCard rendering: criterion rows now use the drawer
# ============================================================
old_row_template = '''return `<a class="signal-card-row" href="/library/megaliths.html#${c.anchor}" target="_blank" rel="noopener">
      <span class="criterion-icon">${c.icon}</span>
      <span>${c.label}</span>
    </a>`;'''

new_row_template = '''return `<a class="signal-card-row" href="/library/megaliths.html#${c.anchor}" onclick="event.preventDefault();event.stopPropagation();openLibraryDrawer('${key}')" target="_blank" rel="noopener">
      <span class="criterion-icon">${c.icon}</span>
      <span>${c.label}</span>
    </a>`;'''

if old_row_template not in html:
    sys.exit("Could not find criterion row template to patch for drawer")
html = html.replace(old_row_template, new_row_template, 1)
print("✓ Criterion rows now open in drawer (with fallback to new-tab href)")

# ============================================================
# 5. Also patch the "Read the reference" footer link
# ============================================================
old_foot = '<div class="signal-card-foot"><a href="/library/megaliths.html" target="_blank" rel="noopener">Read the reference →</a></div>'
new_foot = '<div class="signal-card-foot"><a href="/library/megaliths.html" onclick="event.preventDefault();event.stopPropagation();openLibraryDrawer(\'precision\')" target="_blank" rel="noopener">Read the reference →</a></div>'
if old_foot in html:
    html = html.replace(old_foot, new_foot, 1)
    print("✓ 'Read the reference' link also opens drawer (defaults to first section)")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Library drawer installed in {HTML_PATH}")
print("  Click any criterion → drawer slides in showing the library section")
print("  Close via X, Esc, or backdrop click — returns to criteria card")
print("  Right-click any criterion → still works to open in new tab")
