#!/usr/bin/env python3
"""
fix-drawer-iframe-flash.py — Eliminate scroll flashing in the library drawer.

Cause: the drawer has `backdrop-filter: blur(20px)` applied to a fixed-
position element. The iframe inside is OPAQUE (it has its own background),
so the backdrop blur is computing the underlying atlas content unnecessarily.
During fast scrolls inside the iframe, the browser compositor struggles —
repaints flash.

Fixes:
  1. Remove backdrop-filter from .library-drawer (the iframe is opaque,
     blur is wasted work)
  2. Make .library-drawer background fully opaque (no transparency means
     no need to composite with anything underneath)
  3. Add `transform: translateZ(0)` + `will-change: transform` to the
     iframe to force a dedicated GPU compositing layer
  4. Add `contain: layout style paint` to iframe wrapper — performance hint
     telling the browser this subtree is independent

Idempotent.

Run from the repo root:
    python3 scripts/fix-drawer-iframe-flash.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

if "/* DRAWER_FLASH_FIX_APPLIED */" in html:
    print("✓ Drawer flash fix already applied. Nothing to do.")
    sys.exit(0)

# ============================================================
# 1. Update .library-drawer: opaque background, no backdrop-filter
# ============================================================
old_drawer_css = ".library-drawer{position:fixed;top:0;right:0;width:540px;max-width:100vw;height:100vh;background:rgba(13,13,18,.98);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-left:1px solid rgba(201,168,76,.22);box-shadow:-16px 0 48px rgba(0,0,0,.6);z-index:20000;transform:translateX(100%);transition:transform .3s cubic-bezier(.32,.72,0,1);display:flex;flex-direction:column;font-family:var(--font-sans)}"
new_drawer_css = "/* DRAWER_FLASH_FIX_APPLIED */ .library-drawer{position:fixed;top:0;right:0;width:540px;max-width:100vw;height:100vh;background:#0D0D12;border-left:1px solid rgba(201,168,76,.22);box-shadow:-16px 0 48px rgba(0,0,0,.6);z-index:20000;transform:translateX(100%);transition:transform .3s cubic-bezier(.32,.72,0,1);display:flex;flex-direction:column;font-family:var(--font-sans);contain:layout style;will-change:transform}"

if old_drawer_css not in html:
    sys.exit("Could not find .library-drawer CSS to replace")

html = html.replace(old_drawer_css, new_drawer_css, 1)
print("✓ Drawer: opaque background + removed backdrop-filter + GPU layer hints")

# ============================================================
# 2. Iframe wrap: contain hint for paint isolation
# ============================================================
old_wrap_css = ".library-drawer-iframe-wrap{flex:1;position:relative;overflow:hidden;background:var(--obsidian)}"
new_wrap_css = ".library-drawer-iframe-wrap{flex:1;position:relative;overflow:hidden;background:var(--obsidian);contain:layout style paint;isolation:isolate}"
if old_wrap_css in html:
    html = html.replace(old_wrap_css, new_wrap_css, 1)
    print("✓ Iframe wrap: paint containment + stacking context isolation")

# ============================================================
# 3. Iframe: force its own compositing layer
# ============================================================
old_iframe_css = ".library-drawer-iframe{width:100%;height:100%;border:none;background:var(--obsidian)}"
new_iframe_css = ".library-drawer-iframe{width:100%;height:100%;border:none;background:var(--obsidian);transform:translateZ(0);will-change:transform;-webkit-transform:translateZ(0)}"
if old_iframe_css in html:
    html = html.replace(old_iframe_css, new_iframe_css, 1)
    print("✓ Iframe: forced GPU compositing layer (translateZ + will-change)")

# ============================================================
# 4. Backdrop: also remove its backdrop-filter for consistency
# ============================================================
old_backdrop_css = ".library-drawer-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:19999;opacity:0;transition:opacity .25s ease;pointer-events:none;backdrop-filter:blur(2px)}"
new_backdrop_css = ".library-drawer-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.62);z-index:19999;opacity:0;transition:opacity .25s ease;pointer-events:none}"
if old_backdrop_css in html:
    html = html.replace(old_backdrop_css, new_backdrop_css, 1)
    print("✓ Backdrop: removed blur (was repaint-heavy), slightly darker for compensation")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Scroll flashing fix applied to {HTML_PATH}")
print("  Drawer is opaque, iframe gets its own GPU layer.")
print("  Try fast-scrolling the library — should be silky now.")
