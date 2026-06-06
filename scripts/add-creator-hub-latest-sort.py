#!/usr/bin/env python3
"""
add-creator-hub-latest-sort.py — Add a 4th sort tab "Latest" to the Creator
Hub modal. Sorts all videos by published date desc, shows the publish date
on each card, and surfaces NEW-qualifying videos in a "Recent" section at
the top. Existing NEW badge renders automatically on qualifying cards.

What this adds:

  1. CSS for date pill + recent section header
  2. JS helper formatRelativeDate(isoStr) → "5d ago", "3w ago", "May 26, 2026"
  3. Latest sort button in the .cr-sort row
  4. New 'latest' branch in the hubSortMode if/else chain
  5. introText case for 'latest'

Idempotent. Safe to re-run.

Run from the repo root:
    python3 scripts/add-creator-hub-latest-sort.py
    python3 scripts/build.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'index.html'

if not HTML_PATH.exists():
    sys.exit(f"public/index.html not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

MARKER = "hubSortMode === 'latest'"
if MARKER in html:
    print("· Latest sort already wired. Nothing to do.")
    sys.exit(0)

changes = 0

# ============================================================
# 1. CSS — date pill + recent header
# ============================================================
LATEST_CSS = (
    '.cr-vdate{font-family:var(--font-mono),"JetBrains Mono",monospace;'
    'font-size:10px;letter-spacing:.08em;color:var(--mist,#8A8A9A);'
    'margin-top:3px;text-transform:uppercase;font-weight:500}'
    '.cr-vcard:hover .cr-vdate{color:var(--cloud,#C5C5D0)}'
    '.cr-recent-divider{margin:24px 0 16px;padding:10px 14px;'
    'border-top:1px solid rgba(201,168,76,.18);'
    'font-family:var(--font-mono),"JetBrains Mono",monospace;'
    'font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;'
    'color:var(--champagne,#C9A84C);opacity:.85;font-weight:600}'
)
if '</style>' not in html:
    sys.exit("Could not find </style>")
html = html.replace('</style>', LATEST_CSS + '\n</style>', 1)
print("  ✓ Injected .cr-vdate + .cr-recent-divider CSS")
changes += 1

# ============================================================
# 2. formatRelativeDate helper — inject before showCreators or near it
# ============================================================
HELPER_JS = """

// Humanize an ISO date into a short relative phrase, falling back to date string
function formatRelativeDate(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  if (isNaN(d.getTime())) return '';
  const days = Math.floor((Date.now() - d.getTime()) / 86400000);
  if (days < 0)   return 'upcoming';
  if (days === 0) return 'today';
  if (days === 1) return '1d ago';
  if (days < 7)   return days + 'd ago';
  if (days < 30)  return Math.floor(days/7) + 'w ago';
  if (days < 365) return Math.floor(days/30) + 'mo ago';
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
}
"""
helper_anchors = [
    "let hubSortMode",
    "function setHubSortMode",
    "function showCreators",
]
helper_done = False
for anchor in helper_anchors:
    if anchor in html:
        html = html.replace(anchor, HELPER_JS + '\n' + anchor, 1)
        print(f"  ✓ Injected formatRelativeDate helper (before `{anchor}`)")
        helper_done = True
        break
if not helper_done:
    sys.exit("Could not find an anchor for formatRelativeDate helper.")
changes += 1

# ============================================================
# 3. Add the Latest sort button
# ============================================================
old_buttons = (
    '<button class="${hubSortMode === \'bysite\' ? \'on\' : \'\'}" '
    'onclick="setHubSortMode(\'bysite\')">By Site</button>'
)
new_buttons = (
    '<button class="${hubSortMode === \'bysite\' ? \'on\' : \'\'}" '
    'onclick="setHubSortMode(\'bysite\')">By Site</button>\n'
    '      <button class="${hubSortMode === \'latest\' ? \'on\' : \'\'}" '
    'onclick="setHubSortMode(\'latest\')">Latest</button>'
)
if old_buttons not in html:
    sys.exit("Could not find the 'By Site' button to insert Latest after.")
html = html.replace(old_buttons, new_buttons, 1)
print("  ✓ Added Latest sort button after 'By Site'")
changes += 1

# ============================================================
# 4. Render branch for 'latest' mode
# ============================================================
# Find the end of the bysite branch — the line `  }` that closes the
# `else if (hubSortMode === 'bysite') {` block. We anchor on the literal
# code that comes right before it.
LATEST_BRANCH = """ else if (hubSortMode === 'latest') {
    // Flatten all videos with site context, filter for published date, sort desc
    const allLatest = [];
    Object.entries(VIDEOS).forEach(([siteName, vids]) => {
      vids.forEach(v => { if (v.published) allLatest.push({ ...v, _siteName: siteName }); });
    });
    allLatest.sort((a, b) => new Date(b.published) - new Date(a.published));

    function renderLatestCard(v) {
      const creator = v.cr && CREATORS[v.cr] ? CREATORS[v.cr] : null;
      const safeTitle = v.title.replace(/"/g, '&quot;');
      const escSite = (v._siteName || '').replace(/'/g, "\\\\'");
      const dateLabel = formatRelativeDate(v.published);
      const newBadge = (typeof isRecentlyAdded === 'function' && isRecentlyAdded(v))
        ? '<span class="video-new-badge">New</span>' : '';
      const credit = creator
        ? '<div class="cr-vsite" style="color:' + creator.color + '"><span class="cr-vsite-dot" style="background:' + creator.color + '"></span>' + creator.name + ' · <em style="font-style:normal;opacity:.7">' + v._siteName + '</em></div>'
        : '<div class="cr-vsite cr-vsite-yt"><span class="cr-vsite-yt-icon">\\u25B6</span>YouTube · <em style="font-style:normal;opacity:.7">' + v._siteName + '</em></div>';
      return '<button class="cr-vcard" onclick="closeCreators();selectSiteByName(\\'' + escSite + '\\')" title="' + safeTitle + '">' +
        '<div class="cr-vthumb" style="background-image:url(https://i.ytimg.com/vi/' + v.id + '/mqdefault.jpg)"></div>' +
        '<div class="cr-vbody">' +
          '<div class="cr-vtitle">' + newBadge + v.title + '</div>' +
          credit +
          (dateLabel ? '<div class="cr-vdate">' + dateLabel + '</div>' : '') +
        '</div>' +
      '</button>';
    }

    // Split: NEW-qualifying at top, the rest below
    const isNewFn = (typeof isRecentlyAdded === 'function') ? isRecentlyAdded : (() => false);
    const recent = allLatest.filter(v => isNewFn(v));
    const earlier = allLatest.filter(v => !isNewFn(v));

    bodyContent = (recent.length
      ? '<div class="cr-recent-divider">Recent · last 30 days</div><div class="cr-section-videos">' +
        recent.map(renderLatestCard).join('') + '</div>'
      : ''
    ) +
    '<div class="cr-recent-divider">Earlier walkthroughs</div><div class="cr-section-videos">' +
      earlier.map(renderLatestCard).join('') + '</div>';
  }"""

# Anchor: find the end of the bysite branch.
# It ends with `;\n  }` after the bodyContent template literal closes.
# Use the unique tail pattern from the bysite branch.
BYSITE_TAIL = "${rest.map(([n, v]) => renderSiteSection(n, v)).join('')}\n      </div>\n    `;\n  }"
if BYSITE_TAIL not in html:
    print("  ⚠ Could not find the exact bysite branch tail. Trying simpler anchor…")
    BYSITE_TAIL_ALT = "${rest.map(([n, v]) => renderSiteSection(n, v)).join('')}"
    if BYSITE_TAIL_ALT not in html:
        sys.exit("Could not locate the bysite branch in the html.")
    # Find the next `  }` after this anchor — that closes the bysite branch
    idx = html.find(BYSITE_TAIL_ALT)
    # Walk forward to find the closing `  }` of the bysite branch
    close_idx = html.find('\n  }', idx)
    if close_idx < 0:
        sys.exit("Could not find close of bysite branch.")
    # Insert latest branch right after that close
    insert_at = close_idx + len('\n  }')
    html = html[:insert_at] + LATEST_BRANCH + html[insert_at:]
else:
    html = html.replace(BYSITE_TAIL, BYSITE_TAIL + LATEST_BRANCH, 1)
print("  ✓ Inserted 'latest' render branch after 'bysite'")
changes += 1

# ============================================================
# 5. introText — add 'latest' case
# ============================================================
old_intro_tail = (
    "    : `Browse by <strong>site</strong> instead of by creator. "
    "The 10 most-documented sites surface at the top — places where "
    "multiple creators have converged. Below: every other site with "
    "walkthroughs, alphabetical. Click any thumbnail to jump to the site.`;"
)
new_intro_tail = (
    "    : hubSortMode === 'bysite'\n"
    "    ? `Browse by <strong>site</strong> instead of by creator. "
    "The 10 most-documented sites surface at the top — places where "
    "multiple creators have converged. Below: every other site with "
    "walkthroughs, alphabetical. Click any thumbnail to jump to the site.`\n"
    "    : `Every walkthrough sorted by <strong>publish date</strong>. "
    "<strong>Recent</strong> uploads (last 30 days) surface at the top with "
    "the <em>New</em> badge. Below: every prior walkthrough in chronological order. "
    "Click any card to jump to its site.`;"
)
if old_intro_tail in html:
    html = html.replace(old_intro_tail, new_intro_tail, 1)
    print("  ✓ Added 'latest' case to introText")
    changes += 1
else:
    print("  ⚠ Could not find exact introText tail to extend.")
    print("    The Latest sort will work but the intro text won't show for that mode.")
    print("    Look for the introText ternary near `hubSortMode === 'alphabetical'`.")

# ============================================================
# Write
# ============================================================
with open(HTML_PATH, 'w') as f:
    f.write(html)

print(f"\n✓ Done. {changes} edit(s) applied to public/index.html.")
print(f"  Run scripts/build.py and reload the atlas, then open Creator Hub.")
print(f"  You should see a 4th sort tab: Latest.")
