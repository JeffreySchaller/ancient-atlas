#!/usr/bin/env python3
"""
fix-new-badge-helper.py — Replace the isRecentlyAdded helper with a resilient
strict version that handles both calling conventions (date-string OR video
object) so the render finally shows the badge.

Why this exists:
  - add-new-video-badge.py installed a LAX helper expecting `isRecentlyAdded(dateStr)`
  - wire-new-badge-render.py wired the render to call `isRecentlyAdded(v)` with
    the whole video object
  - strict-new-badge.py was meant to upgrade the helper but couldn't find it
    in the exact format it expected, so it exited without changes

Result: caller passes an object, helper expects a string, returns false, no
badge ever renders.

This script uses a regex to locate the function regardless of exact format,
then replaces with a unified version that:
  - Accepts either a date string (legacy) or a video object (current)
  - When given an object, requires BOTH `added` ≤ 30 days AND `published` ≤ 90 days
  - When given a string, just checks `added` ≤ 30 days (backwards compat)

Idempotent. Safe to re-run.

Run from the repo root:
    python3 scripts/fix-new-badge-helper.py
"""
import re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# ============================================================
# Strict, resilient helper that handles both call signatures
# ============================================================
NEW_FN = """// NEW badge helper — true only if BOTH:
//   - added to atlas in last 30 days  (recently curated)
//   - published on YouTube in last 90 days  (actually recent upload)
// Accepts either a video object (current callers) or a date string (legacy).
function isRecentlyAdded(input) {
  // Legacy call: isRecentlyAdded(dateStr) - just check added recency
  if (typeof input === 'string') {
    const d = new Date(input);
    if (isNaN(d.getTime())) return false;
    const days = (Date.now() - d.getTime()) / 86400000;
    return days >= 0 && days <= 30;
  }
  // Modern call: isRecentlyAdded(video) - strict, both fields required
  if (!input || typeof input !== 'object') return false;
  const addedStr = input.added;
  const pubStr   = input.published;
  if (!addedStr || !pubStr) return false;
  const added = new Date(addedStr);
  const pub   = new Date(pubStr);
  if (isNaN(added.getTime()) || isNaN(pub.getTime())) return false;
  const addedDays = (Date.now() - added.getTime()) / 86400000;
  const pubDays   = (Date.now() - pub.getTime())   / 86400000;
  return addedDays >= 0 && addedDays <= 30 &&
         pubDays   >= 0 && pubDays   <= 90;
}"""

# ============================================================
# Locate and replace the existing helper using a regex
# Matches: optional comment line(s) + function isRecentlyAdded(...) { ... }
# ============================================================
# Regex strategy: find the function declaration and its body up to the
# matching closing brace. We assume the function body is short (it is).
pattern = re.compile(
    r'(?://[^\n]*\n)*'                     # optional leading comment lines
    r'function\s+isRecentlyAdded\s*\([^)]*\)\s*\{'  # function signature
    r'(?:[^{}]|\{[^{}]*\})*'               # body (handles one level of nested braces)
    r'\}',
    re.MULTILINE
)

matches = pattern.findall(html)
if not matches:
    sys.exit("Could not locate function isRecentlyAdded in public/index.html.\n"
             "Run scripts/add-new-video-badge.py first to install the base helper.")

if len(matches) > 1:
    print(f"⚠ Found {len(matches)} matches for isRecentlyAdded — only replacing the first")

# Find the leading comment-block for the function (look back from match start)
match_obj = pattern.search(html)
start = match_obj.start()
end = match_obj.end()

# Walk backwards over any consecutive comment lines that precede the function
i = start
while i > 0:
    # Find start of the previous line
    line_start = html.rfind('\n', 0, i - 1) + 1
    line = html[line_start:i].strip()
    if line.startswith('//') or line == '':
        i = line_start
    else:
        break
start = i

before = html[:start]
after = html[end:]
new_html = before + NEW_FN + after

if new_html == html:
    print("· Helper already in the resilient form — nothing to do")
    sys.exit(0)

with open(HTML_PATH, 'w') as f:
    f.write(new_html)

print(f"✓ Replaced isRecentlyAdded helper with resilient strict version")
print(f"  File: {HTML_PATH}")
print(f"  The function now accepts both date-string and video-object callers,")
print(f"  and in the modern-caller path requires both `added` ≤ 30d and `published` ≤ 90d.")
print(f"\n  Next: reload the atlas. The SOLSTICE HUNTER walkthrough on the Phnom Bok")
print(f"  detail panel should now show the New badge before its title.")
