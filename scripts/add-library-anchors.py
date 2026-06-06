#!/usr/bin/env python3
"""
add-library-anchors.py — One-time edit to add anchor IDs to the 6 property rows
in public/library/megaliths.html so the badge flip-down can deep-link to them.

Adds: id="precision", id="hardness", id="scale", id="polygonal", id="stratigraphy", id="geometry"

For each row, this script finds the unique text snippet, walks backwards to the
nearest opening tag (<li>, <tr>, <div>, etc.), and inserts the id attribute.

Idempotent — won't double-patch.

Run from the repo root:
    python3 scripts/add-library-anchors.py
"""
import sys, re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HTML_PATH = REPO_ROOT / 'public' / 'library' / 'megaliths.html'

if not HTML_PATH.exists():
    sys.exit(f"Library page not found at {HTML_PATH}")

with open(HTML_PATH) as f:
    html = f.read()

# (anchor_id, distinctive_text_snippet) — text must uniquely identify the row
ANCHORS = [
    ('precision',    'tolerances tighter than a knife'),
    ('hardness',     'harder than steel'),
    ('scale',        'heavier than anything steam'),
    ('polygonal',    'polygonal interlock pattern appearing on three continents'),
    ('stratigraphy', 'Stratigraphy that runs backwards'),
    ('geometry',     'Geometry that encodes astronomy'),
]

def add_id_to_nearest_tag(html_text, snippet, anchor_id):
    """
    Find snippet in html_text. Walk backwards to the nearest opening tag.
    Insert id="anchor_id" into that tag if it doesn't already have an id.
    Returns: (new_html, status_message)
    """
    pos = html_text.find(snippet)
    if pos == -1:
        return html_text, f"NOT FOUND: '{snippet}'"

    # Walk backwards to find opening tag
    tag_pos = pos
    while tag_pos > 0:
        tag_pos -= 1
        if html_text[tag_pos] == '<' and html_text[tag_pos+1] != '/':
            # Found an opening tag. Get the tag text up to the next '>'
            tag_end = html_text.find('>', tag_pos)
            if tag_end == -1:
                return html_text, f"MALFORMED TAG near '{snippet}'"
            tag_text = html_text[tag_pos:tag_end+1]

            # Skip self-closing or non-container tags
            if tag_text.startswith(('<br', '<hr', '<img', '<svg', '<path', '<circle', '<ellipse', '<rect', '<g ')):
                continue

            # Check if it already has an id
            if re.search(r'\bid\s*=', tag_text):
                # Already has an id — check if it's our id; otherwise warn
                existing = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', tag_text)
                if existing and existing.group(1) == anchor_id:
                    return html_text, f"ALREADY HAS id='{anchor_id}'"
                # Has a different id — try the tag's parent instead
                # (skip this tag, walk further back)
                continue

            # Insert id attribute right after the tag name
            m = re.match(r'<(\w+)', tag_text)
            if not m:
                return html_text, f"COULDN'T PARSE tag near '{snippet}'"
            tag_name = m.group(1)
            new_tag = f'<{tag_name} id="{anchor_id}"' + tag_text[1+len(tag_name):]
            new_html = html_text[:tag_pos] + new_tag + html_text[tag_end+1:]
            return new_html, f"INJECTED id='{anchor_id}' into <{tag_name}>"

    return html_text, f"NO PARENT TAG FOUND for '{snippet}'"


print(f"Patching {HTML_PATH}")
print(f"File size: {len(html):,} bytes\n")
issues = 0
for anchor_id, snippet in ANCHORS:
    html, msg = add_id_to_nearest_tag(html, snippet, anchor_id)
    flag = '✓' if 'INJECTED' in msg or 'ALREADY' in msg else '✗'
    print(f"  {flag}  {anchor_id:13s}  {msg}")
    if flag == '✗':
        issues += 1

if issues > 0:
    print(f"\n⚠  {issues} anchor(s) could not be auto-injected. Either:")
    print("    a) the property row text has been edited, or")
    print("    b) the surrounding tag structure is unusual")
    print("    Inspect the library page and add the missing id(s) manually.")
    print("    The badge flip-down will still work — the deep-links will just")
    print("    land at the top of the page until the anchors are present.")
    sys.exit(1)

with open(HTML_PATH, 'w') as f:
    f.write(html)
print(f"\n✓ Anchors added.")
