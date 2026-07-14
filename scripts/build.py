#!/usr/bin/env python3
"""
build.py — Phase 2 build script.

Reads data/*.json files and surgically replaces the corresponding
`const NAME = ...` blocks inside public/index.html. The HTML structure,
CSS, and JavaScript logic are preserved exactly — only the data blocks
are regenerated from the JSON source of truth.

Run from the repo root:
    python3 scripts/build.py

Output: public/index.html is rewritten with the latest data from data/.

Pre-flight validations:
    - Every JSON file exists and parses cleanly
    - SITES is a list, all other data files are dicts
    - Every video creator key maps to a known creator
    - No duplicate site keys in any map
"""
import re, json, sys, os, shutil
from pathlib import Path

# In the GitHub repo structure: scripts/build.py is at repo root + scripts/
# data/ and public/ are siblings. So go up one level from scripts/.
REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
SRC_HTML = REPO_ROOT / 'public' / 'index.html'
PUBLIC_DATA_DIR = REPO_ROOT / 'public' / 'data'

# ============================================================
# Mapping: data file → const NAME inside HTML
# ============================================================
BLOCKS = [
    # (json filename, const name, JSON type)
    ('sites.json',          'SITES',          list),
    ('creators.json',       'CREATORS',       dict),
    ('tours.json',          'TOURS',          dict),
    ('videos.json',         'VIDEOS',         dict),
    ('categories.json',     'CATS',           dict),
    ('eras.json',           'SITE_YEARS',     dict),
    ('countries.json',      'SITE_COUNTRIES', dict),
    ('civilizations.json',  'SITE_CULTURES',  dict),
    ('tags.json',           'SITE_TAGS',      dict),
    ('search-aliases.json', 'SEARCH_ALIASES', dict),
]

# ============================================================
# 1. Load + validate all data files
# ============================================================
def load_and_validate():
    if not DATA_DIR.exists():
        sys.exit(f"data/ not found at {DATA_DIR}")
    if not SRC_HTML.exists():
        sys.exit(f"public/index.html not found at {SRC_HTML}")

    data = {}
    for filename, const_name, expected_type in BLOCKS:
        path = DATA_DIR / filename
        if not path.exists():
            sys.exit(f"Missing data file: {path}")
        try:
            with open(path) as f:
                obj = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"JSON parse error in {filename}: {e}")
        if not isinstance(obj, expected_type):
            sys.exit(f"{filename}: expected {expected_type.__name__}, got {type(obj).__name__}")
        data[const_name] = obj
    return data

# ============================================================
# 2. Cross-validation: catch the bugs CI will eventually catch automatically
# ============================================================
def cross_validate(data):
    errors = []
    warnings = []

    # 2a. Sites: no duplicate names
    sites = data['SITES']
    names = [s.get('n', '') for s in sites]
    dups = {n for n in names if names.count(n) > 1}
    if dups:
        errors.append(f"sites.json: duplicate names: {sorted(dups)}")

    # 2b. Sites: all entries have required fields
    required_site_fields = {'n', 'lat', 'lng', 'cat', 'region', 'tier', 'desc'}
    for i, s in enumerate(sites):
        missing = required_site_fields - set(s.keys())
        if missing:
            errors.append(f"sites.json[{i}] ({s.get('n','?')}): missing fields {missing}")

    # 2c. Videos: every creator key in videos maps to a known creator
    creators = data['CREATORS']
    videos = data['VIDEOS']
    unknown_crs = set()
    for site_name, vid_list in videos.items():
        for v in vid_list:
            cr = v.get('cr')
            if cr and cr not in creators:
                unknown_crs.add(cr)
    if unknown_crs:
        warnings.append(f"videos.json: creator keys not in creators.json: {sorted(unknown_crs)}")

    # 2d. Videos: site keys in videos should exist in sites (warn only — videos may use synonyms)
    site_names = {s['n'] for s in sites}
    video_keys = set(videos.keys())
    orphan_video_keys = video_keys - site_names
    if orphan_video_keys:
        warnings.append(f"videos.json: site keys not in sites.json ({len(orphan_video_keys)} entries): {sorted(orphan_video_keys)[:5]}...")

    return errors, warnings

# ============================================================
# 2e. Walkthrough ranking — quality floor + freshness lift
# ============================================================
# Display order per site card (data/videos.json keeps insertion order
# as the audit ledger; ranking is computed at build time):
#   score = creator tier weight + NEW-window boost
#     tier 1 → 3.0, tier 2 → 2.0, tier 3 / no creator entry → 1.0
#     added within NEW_WINDOW_DAYS → +1.5
#   so: NEW tier-1 (4.5) > established tier-1 (3.0) > NEW tier-3 (2.5)
#       > established tier-2 (2.0). New creators debut above mid-tier
#       backlog, never above proven anchors. Boost expires with the NEW
#       badge — the card self-heals to pure quality order.
# Tie-breaks: published date (newer first), then title.

NEW_WINDOW_DAYS = 90
TIER_WEIGHT = {1: 3.0, 2: 2.0, 3: 1.0}

def rank_walkthroughs(data):
    import datetime
    today = datetime.date.today()
    creators = data['CREATORS']

    def score(v):
        cr = creators.get(v.get('cr') or '', {})
        s = TIER_WEIGHT.get(cr.get('tier', 3), 1.0)
        try:
            added = datetime.date.fromisoformat(v.get('added', '1970-01-01'))
            if (today - added).days <= NEW_WINDOW_DAYS:
                s += 1.5
        except ValueError:
            pass
        return s

    for vid_list in data['VIDEOS'].values():
        # stable two-pass: newest published first, then by score —
        # equal scores keep newest-first order
        vid_list.sort(key=lambda v: v.get('published', '0000-00-00'),
                      reverse=True)
        vid_list.sort(key=score, reverse=True)

# ============================================================
# 3. Render each data block as JS literal (pretty-printed but valid JS)
# ============================================================
def js_dump(obj):
    """
    Render a Python object as a valid JS literal.

    We use json.dumps with compact-ish formatting to keep diffs readable.
    The output is valid JSON, which is a strict subset of JS object literals.
    """
    return json.dumps(obj, ensure_ascii=False, indent=2)

# ============================================================
# 4. Surgical replacement of `const NAME = ...` block
# ============================================================
def replace_block(html, const_name, new_value_str):
    """
    Find `const NAME = ` followed by a balanced { } or [ ] block,
    then replace just the value (preserving const declaration + trailing semicolon).
    """
    # Find start
    pattern = re.compile(r'(const\s+' + re.escape(const_name) + r'\s*=\s*)([\{\[])')
    m = pattern.search(html)
    if not m:
        raise RuntimeError(f"Could not find: const {const_name} = ...")

    open_pos = m.start(2)
    open_ch = m.group(2)
    close_ch = '}' if open_ch == '{' else ']'

    # Walk forward to balanced close
    depth = 0
    i = open_pos
    n = len(html)
    in_str = False
    str_ch = None
    while i < n:
        c = html[i]
        if in_str:
            if c == '\\' and i + 1 < n:
                i += 2
                continue
            if c == str_ch:
                in_str = False
                str_ch = None
            i += 1
            continue
        if c in '"\'':
            in_str = True
            str_ch = c
            i += 1
            continue
        if c == '/' and i + 1 < n:
            if html[i+1] == '/':
                j = html.find('\n', i)
                if j == -1: break
                i = j + 1
                continue
            if html[i+1] == '*':
                j = html.find('*/', i+2)
                if j == -1: break
                i = j + 2
                continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                # Replace html[open_pos : i+1] with new_value_str
                return html[:open_pos] + new_value_str + html[i+1:]
        i += 1
    raise RuntimeError(f"Unbalanced {open_ch}/{close_ch} for {const_name}")

# ============================================================
# Main
# ============================================================
def main():
    print(f"Reading: {SRC_HTML}")
    print(f"Data:    {DATA_DIR}\n")

    data = load_and_validate()
    errors, warnings = cross_validate(data)
    rank_walkthroughs(data)
    if errors:
        print("✗ Validation errors (build aborted):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    if warnings:
        print("⚠ Warnings (build continuing):")
        for w in warnings:
            print(f"  - {w}")
        print()

    # Read current HTML
    with open(SRC_HTML) as f:
        html = f.read()

    # Replace each block
    for filename, const_name, _ in BLOCKS:
        try:
            new_block = js_dump(data[const_name])
            html = replace_block(html, const_name, new_block)
            print(f"  ✓ {const_name}")
        except Exception as e:
            sys.exit(f"  ✗ {const_name}: {e}")

    # Write rebuilt HTML
    with open(SRC_HTML, 'w') as f:
        f.write(html)

    # Mirror data/ → public/data/ so deployed pages (contribute.html, future
    # client-side tools) can fetch them at runtime. Netlify only publishes
    # public/, so files outside it are unreachable from the deployed site.
    PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    mirrored = 0
    for filename, const_name, _ in BLOCKS:
        if const_name == 'VIDEOS':
            # mirror the ranked order (data/videos.json stays the
            # insertion-order ledger; the served mirror matches display)
            with open(PUBLIC_DATA_DIR / filename, 'w') as f:
                json.dump(data['VIDEOS'], f, indent=2, ensure_ascii=False)
        else:
            shutil.copy2(DATA_DIR / filename, PUBLIC_DATA_DIR / filename)
        mirrored += 1

    # Print summary
    sz = os.path.getsize(SRC_HTML)
    print(f"\n✓ Built: {SRC_HTML} ({sz:,} bytes)")
    print(f"✓ Mirrored: {mirrored} JSON files → public/data/")
    print(f"  Sites:       {len(data['SITES'])}")
    print(f"  Creators:    {len(data['CREATORS'])}")
    print(f"  Walkthroughs: {sum(len(v) for v in data['VIDEOS'].values())}")

    # SEO layer — regenerate static per-site pages + sitemap (added 2026-07-13)
    __import__('subprocess').run(
        ['python3', __import__('os').path.join(__import__('os').path.dirname(__file__), 'build-seo-pages.py')],
        check=True)

if __name__ == '__main__':
    main()
