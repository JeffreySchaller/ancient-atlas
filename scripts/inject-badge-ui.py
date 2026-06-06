#!/usr/bin/env python3
"""
inject-badge-ui.py — One-time UI patch to add the open-question badge to public/index.html.

Adds:
  1. CSS rules for the badge glyph + flip-down card + criterion icons
  2. JS constants: SIGNAL_CRITERIA (6 criteria, label + inline SVG icon) and SIGNAL_BADGE_SVG
  3. Helper functions: buildSignalBadgeHtml, openSignalCard, closeSignalCard
  4. Click-outside / Esc listeners
  5. A hidden <div id="signal-card"> appended to body
  6. Patches buildSiteCardHtml() to render the badge after the site name
  7. Patches showDetail() to render the badge next to the h2 title

Idempotent — safe to run more than once. Won't double-patch.

Run from the repo root:
    python3 scripts/inject-badge-ui.py
"""
import sys, re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# ============================================================
# Idempotency check
# ============================================================
if 'SIGNAL_CRITERIA' in html:
    print("✓ Badge UI already injected. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. CSS block — inject before </style>
# ============================================================
CSS = """
/* ===== Open-question badge (signal: open) ===== */
.signal-badge{display:inline-flex;width:12px;height:12px;margin-left:4px;cursor:pointer;color:var(--champagne);opacity:.55;transition:opacity .15s,transform .15s;vertical-align:middle;flex-shrink:0;align-self:center}
.signal-badge:hover{opacity:1;transform:scale(1.18)}
.signal-badge svg{width:100%;height:100%;display:block}
.detail-signal-badge{width:18px;height:18px;margin-left:10px}

/* ===== Signal flip-down card ===== */
.signal-card{position:fixed;width:300px;background:rgba(13,13,18,.97);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(201,168,76,.28);border-radius:12px;padding:14px 16px 10px;box-shadow:0 16px 48px rgba(0,0,0,.65);z-index:10000;opacity:0;transform:translateY(-6px);pointer-events:none;transition:opacity .18s ease,transform .18s ease;font-family:var(--font-sans);color:var(--cloud)}
.signal-card.open{opacity:1;transform:translateY(0);pointer-events:auto}
.signal-card-title{font-family:var(--font-mono);font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--champagne);font-weight:700;margin-bottom:10px}
.signal-card-row{display:flex;align-items:flex-start;gap:11px;padding:9px 0;color:var(--cloud);font-size:12px;line-height:1.45;text-decoration:none;border-bottom:1px solid rgba(42,42,53,.4);transition:color .12s}
.signal-card-row:last-of-type{border-bottom:none}
.signal-card-row:hover{color:var(--ivory)}
.signal-card-row:hover .criterion-icon{color:var(--amber)}
.criterion-icon{width:18px;height:18px;flex-shrink:0;color:var(--champagne);margin-top:1px;transition:color .12s}
.criterion-icon svg{width:100%;height:100%;display:block}
.signal-card-foot{margin-top:8px;padding-top:10px;border-top:1px solid rgba(42,42,53,.5);text-align:right}
.signal-card-foot a{color:var(--champagne);text-decoration:none;font-family:var(--font-mono);font-size:10px;text-transform:uppercase;letter-spacing:.12em}
.signal-card-foot a:hover{color:var(--amber)}
"""

if '</style>' not in html:
    sys.exit("Could not find </style> in index.html")
html = html.replace('</style>', CSS + '\n</style>', 1)
print("✓ Injected CSS")

# ============================================================
# 2. <div id="signal-card"> injection — before </body>
# ============================================================
CARD_DIV = '<div id="signal-card" class="signal-card" role="dialog" aria-label="Engineering signature"></div>\n'
if '</body>' not in html:
    sys.exit("Could not find </body> in index.html")
html = html.replace('</body>', CARD_DIV + '</body>', 1)
print("✓ Injected #signal-card div")

# ============================================================
# 3. JS block — constants + helpers
# ============================================================
# Inject AFTER the const PATRONS line so it sits near other static data
JS_BLOCK = r'''

// ============================================================
// SIGNAL: open-question badge taxonomy
// Closed set of 6 criteria, matched 1:1 to /library/megaliths.html
// Icons are inline SVG to match the library's line-icon style.
// ============================================================
const SIGNAL_BADGE_SVG = '<svg viewBox="0 0 12 12" fill="currentColor"><circle cx="6" cy="2.5" r="1.45"/><circle cx="2.5" cy="9.5" r="1.45"/><circle cx="9.5" cy="9.5" r="1.45"/></svg>';

const SIGNAL_CRITERIA = {
  precision: {
    label: 'Mortarless joinery, sub-millimeter tolerance',
    anchor: 'precision',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><rect x="4" y="5" width="16" height="14" rx="1"/><path d="M4 11h16M4 15h16"/></svg>',
  },
  hardness: {
    label: 'Stone harder than period tools',
    anchor: 'hardness',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M12 3l4 5-4 13-4-13z"/><path d="M8 8h8"/></svg>',
  },
  scale: {
    label: 'Block scale exceeds documented lift capability',
    anchor: 'scale',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/></svg>',
  },
  polygonal: {
    label: 'Polygonal interlock pattern across continents',
    anchor: 'polygonal',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="7" r="2.5"/><circle cx="6.5" cy="16" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/></svg>',
  },
  stratigraphy: {
    label: 'Stratigraphy that runs backwards',
    anchor: 'stratigraphy',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M3 7h18M3 12h18M3 17h18"/></svg>',
  },
  geometry: {
    label: 'Geometry encoding astronomy, Earth, human form',
    anchor: 'geometry',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><ellipse cx="9" cy="12" rx="5.5" ry="8.5"/><ellipse cx="15" cy="12" rx="5.5" ry="8.5"/></svg>',
  },
};

function buildSignalBadgeHtml(site, large) {
  if (!site || site.signal !== 'open') return '';
  const cls = large ? 'signal-badge detail-signal-badge' : 'signal-badge';
  const escName = (site.n || '').replace(/'/g, "\\'");
  return `<span class="${cls}" onclick="event.stopPropagation();openSignalCard(event, '${escName}')" title="Open question — signals don't yet converge" role="button" aria-label="Open engineering signature panel">${SIGNAL_BADGE_SVG}</span>`;
}

function openSignalCard(evt, siteName) {
  const site = SITES.find(s => s.n === siteName);
  if (!site || site.signal !== 'open') return;
  const card = document.getElementById('signal-card');
  if (!card) return;
  const criteria = site.criteria || [];

  const rowsHtml = criteria.map(key => {
    const c = SIGNAL_CRITERIA[key];
    if (!c) return '';
    return `<a class="signal-card-row" href="/library/megaliths.html#${c.anchor}" target="_blank" rel="noopener">
      <span class="criterion-icon">${c.icon}</span>
      <span>${c.label}</span>
    </a>`;
  }).join('');

  card.innerHTML = `
    <div class="signal-card-title">Engineering signature · ${site.n}</div>
    ${rowsHtml}
    <div class="signal-card-foot"><a href="/library/megaliths.html" target="_blank" rel="noopener">Read the reference →</a></div>
  `;

  // Position card relative to the clicked badge, keep inside viewport
  const rect = evt.currentTarget.getBoundingClientRect();
  const cardW = 300;
  const cardH = Math.min(280, 80 + criteria.length * 48);
  let left = rect.left + (rect.width / 2) - (cardW / 2);
  let top = rect.bottom + 8;
  left = Math.max(8, Math.min(window.innerWidth - cardW - 8, left));
  if (top + cardH > window.innerHeight - 8) {
    top = Math.max(8, rect.top - cardH - 8);
  }
  card.style.left = left + 'px';
  card.style.top = top + 'px';
  card.classList.add('open');
}

function closeSignalCard() {
  const card = document.getElementById('signal-card');
  if (card) card.classList.remove('open');
}

document.addEventListener('click', e => {
  if (!e.target.closest('.signal-card') && !e.target.closest('.signal-badge')) {
    closeSignalCard();
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeSignalCard();
});
window.addEventListener('scroll', closeSignalCard, true);
'''

# Inject the JS block after `const PATRONS = [];`
patron_anchor = 'const PATRONS = [];'
if patron_anchor not in html:
    sys.exit(f"Could not find '{patron_anchor}' in index.html — bailing rather than guess location.")
html = html.replace(patron_anchor, patron_anchor + JS_BLOCK, 1)
print("✓ Injected JS constants + handlers")

# ============================================================
# 4. Patch buildSiteCardHtml — render badge after .nm span
# ============================================================
before_site = '<span class="nm">${site.n}</span>'
after_site = '<span class="nm">${site.n}</span>${buildSignalBadgeHtml(site, false)}'
if before_site not in html:
    sys.exit("Could not find site name span in buildSiteCardHtml — schema may have changed.")
html = html.replace(before_site, after_site, 1)
print("✓ Patched buildSiteCardHtml")

# ============================================================
# 5. Patch showDetail — render badge next to h2 title
# ============================================================
before_detail = '<h2 style="margin:0;flex:1">${site.n}</h2>'
after_detail = '<h2 style="margin:0;flex:1;display:flex;align-items:center">${site.n}${buildSignalBadgeHtml(site, true)}</h2>'
if before_detail not in html:
    sys.exit("Could not find detail h2 in showDetail — schema may have changed.")
html = html.replace(before_detail, after_detail, 1)
print("✓ Patched showDetail")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Badge UI injected into {HTML_PATH}")
print("  Open the file in a browser to verify.")
print("  Re-running this script is safe — it detects existing injection and skips.")
