#!/usr/bin/env python3
"""
add-share-button-to-library.py — Add a brand-aligned Share button to all
three Library entry articles in public/library/.

Behavior:
  - Native share sheet on mobile via navigator.share()
  - Clipboard copy + champagne toast on desktop fallback
  - Sits immediately before the existing back-link/back-btn in the article header
  - "Share" text label on desktop, icon-only on mobile (<700px)

Articles patched:
  - public/library/megaliths.html        (Entry 01 — uses .back-link)
  - public/library/stone-circles.html    (Entry 02 — uses .back-link)
  - public/library/mini-megaliths.html   (Entry 03 — uses .back-btn)

Idempotent.

Run from the repo root:
    python3 scripts/add-share-button-to-library.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LIB_DIR = REPO_ROOT / 'public' / 'library'

ARTICLES = [
    LIB_DIR / 'megaliths.html',
    LIB_DIR / 'stone-circles.html',
    LIB_DIR / 'mini-megaliths.html',
]

# ============================================================
# Patch pieces
# ============================================================
SHARE_CSS = (
    '.share-btn{font-family:var(--font-mono),"JetBrains Mono",monospace;'
    'font-size:11px;letter-spacing:.12em;text-transform:uppercase;'
    'color:var(--cloud,#C5C5D0);text-decoration:none;padding:8px 12px;'
    'border:1px solid rgba(201,168,76,.3);border-radius:8px;font-weight:600;'
    'transition:all .15s;background:rgba(201,168,76,.04);cursor:pointer;'
    'display:inline-flex;align-items:center;gap:7px;margin-right:8px;'
    'font-family:inherit}'
    '.share-btn:hover{color:var(--champagne,#C9A84C);'
    'border-color:rgba(201,168,76,.55);background:rgba(201,168,76,.1)}'
    '.share-btn svg{width:13px;height:13px;flex-shrink:0}'
    '@media(max-width:700px){.share-btn span{display:none}'
    '.share-btn{padding:7px 9px;margin-right:6px}}'
    '.share-toast{position:fixed;bottom:32px;left:50%;'
    'transform:translateX(-50%) translateY(20px);background:#0D0D12;'
    'border:1px solid #C9A84C;color:#F0EEE9;padding:11px 22px;'
    'border-radius:8px;font-family:"JetBrains Mono",monospace;'
    'font-size:11px;letter-spacing:.14em;text-transform:uppercase;'
    'z-index:9999;opacity:0;pointer-events:none;'
    'transition:all .25s ease-out;'
    'box-shadow:0 4px 24px rgba(201,168,76,.25)}'
    '.share-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}'
)

SHARE_BUTTON_HTML = (
    '<button class="share-btn" onclick="shareArticle()" '
    'aria-label="Share this article" type="button">'
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true">'
    '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>'
    '</svg>'
    '<span>Share</span>'
    '</button>'
)

SHARE_TOAST_HTML = '<div class="share-toast" id="shareToast">Link copied</div>'

SHARE_SCRIPT = """
<script>
async function shareArticle() {
  const url = window.location.href;
  const title = document.title;
  const text = (document.querySelector('meta[name="description"]') || {}).content || '';
  if (navigator.share) {
    try {
      await navigator.share({ title, text, url });
      return;
    } catch (e) {
      if (e && e.name === 'AbortError') return;
    }
  }
  try {
    await navigator.clipboard.writeText(url);
  } catch (e) {
    const tmp = document.createElement('input');
    tmp.value = url;
    document.body.appendChild(tmp);
    tmp.select();
    try { document.execCommand('copy'); } catch (e2) {}
    document.body.removeChild(tmp);
  }
  const toast = document.getElementById('shareToast');
  if (toast) {
    toast.classList.add('show');
    setTimeout(function(){ toast.classList.remove('show'); }, 2200);
  }
}
</script>
"""

# ============================================================
# Per-file patch
# ============================================================
def patch(path):
    if not path.exists():
        print(f"  ⚠ {path.name}: not found, skipping")
        return False

    with open(path) as f:
        html = f.read()

    if 'share-btn' in html and 'shareArticle' in html:
        print(f"  · {path.name}: already has share button, skipping")
        return False

    changes = 0

    # 1. CSS — inject before </style>
    if SHARE_CSS not in html:
        if '</style>' not in html:
            print(f"  ⚠ {path.name}: no </style> tag, cannot inject CSS")
            return False
        html = html.replace('</style>', SHARE_CSS + '\n</style>', 1)
        changes += 1

    # 2. Button — insert before the back link in the header
    button_inserted = False
    back_patterns = [
        ('<a href="/library/" class="back-btn">',
         SHARE_BUTTON_HTML + '<a href="/library/" class="back-btn">'),
        ('<a class="back-btn" href="/library/">',
         SHARE_BUTTON_HTML + '<a class="back-btn" href="/library/">'),
        ('<a href="index.html" class="back-link">',
         SHARE_BUTTON_HTML + '<a href="index.html" class="back-link">'),
        ('<a class="back-link" href="index.html">',
         SHARE_BUTTON_HTML + '<a class="back-link" href="index.html">'),
    ]
    for old, new in back_patterns:
        if old in html:
            html = html.replace(old, new, 1)
            button_inserted = True
            changes += 1
            break

    if not button_inserted:
        print(f"  ⚠ {path.name}: could not find back-link/back-btn anchor")
        return False

    # 3. Toast + script — append just before </body>
    if '</body>' not in html:
        print(f"  ⚠ {path.name}: no </body> tag")
        return False
    html = html.replace('</body>',
                        SHARE_TOAST_HTML + SHARE_SCRIPT + '</body>', 1)
    changes += 1

    with open(path, 'w') as f:
        f.write(html)
    print(f"  ✓ {path.name}: share button + toast + script injected ({changes} edits)")
    return True

# ============================================================
def main():
    if not LIB_DIR.exists():
        sys.exit(f"public/library/ not found at {LIB_DIR}. Run this from the repo root.")
    print(f"Patching {len(ARTICLES)} library article(s):\n")
    patched = sum(1 for a in ARTICLES if patch(a))
    print(f"\n  Total files patched: {patched} / {len(ARTICLES)}")
    if patched:
        print("\n✓ Done. Reload any library article and try the Share button.")
        print("  Desktop: copies URL + flashes 'Link copied' toast.")
        print("  Mobile: opens the native share sheet.")

if __name__ == '__main__':
    main()
