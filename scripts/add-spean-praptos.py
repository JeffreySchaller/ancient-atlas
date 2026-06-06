#!/usr/bin/env python3
"""
add-spean-praptos.py — Add Spean Praptos (Kampong Kdei Bridge) to the atlas.

12th-century corbel-arch bridge in Cambodia. Tier 2. signal: "open" with
criteria scale + geometry + precision based on the Praveen Mohan transcript
engineering observations.

Wires Praveen Mohan's "They Destroyed Every Face On This Ancient Bridge"
walkthrough (u8Q_mrWMDuY).

Idempotent.

Run from the repo root:
    python3 scripts/add-spean-praptos.py
"""
import json, sys, subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'

SITE = {
    "n": "Spean Praptos (Kampong Kdei Bridge)",
    "lat": 13.0989,
    "lng": 104.8053,
    "cat": "megalithic",
    "region": "Asia",
    "tier": 2,
    "signal": "open",
    "criteria": ["scale", "geometry", "precision"],
    "desc": "12th-century corbel-arch bridge spanning the Chikreng River in Cambodia's Siem Reap Province, roughly 65 km east of Angkor. 87 meters long, 30 feet wide, supported by 21 piers spaced to slow floodwater while restricting passage of large boats — embedded military chokepoint. Laterite structural core with a sandstone facade : the same composite logic modern engineers use with rebar in concrete, executed 900 years before reinforced concrete. Pier height engineered to 23 feet, three times the historical maximum flood level. A T-54 tank (36 tons) crossed during the Khmer Rouge era without structural failure. Featured on Cambodia's 5,000 riel banknote, still in daily local use. The carved human figures on the naga balustrades have had their faces deliberately removed : selectively, by intent, with bodies and poses left intact."
}

VIDEO = {
    "id": "u8Q_mrWMDuY",
    "title": "They Destroyed Every Face On This Ancient Bridge. What Were They Hiding?",
    "cr": "praveenmohan"
}

VALID_CRITERIA = {"precision", "hardness", "scale", "polygonal", "stratigraphy", "geometry"}

def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)

def save_json(name, obj):
    with open(DATA_DIR / name, 'w') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def main():
    if not DATA_DIR.exists():
        sys.exit(f"data/ not found at {DATA_DIR}")

    # Validate criteria
    invalid = [c for c in SITE.get('criteria', []) if c not in VALID_CRITERIA]
    if invalid:
        sys.exit(f"✗ Invalid criteria: {invalid}")

    # Load
    sites = load_json('sites.json')
    videos = load_json('videos.json')
    creators = load_json('creators.json')
    countries = load_json('countries.json')

    # Idempotency: skip if already added
    site_names = {s['n'] for s in sites}
    if SITE['n'] in site_names:
        print(f"✓ {SITE['n']} already in atlas. Nothing to do.")
        sys.exit(0)

    # Verify creator exists
    if VIDEO['cr'] not in creators:
        # Try fuzzy match
        guesses = [k for k in creators if 'praveen' in k.lower()]
        if guesses:
            actual = guesses[0]
            print(f"  ⚠ Creator key '{VIDEO['cr']}' not found — using closest match '{actual}'")
            VIDEO['cr'] = actual
        else:
            sys.exit(f"✗ Creator key '{VIDEO['cr']}' not in creators.json and no close match found")
    else:
        print(f"  ✓ Creator '{VIDEO['cr']}' verified ({creators[VIDEO['cr']].get('name', '?')})")

    # 1. Append site
    sites.append(SITE)
    save_json('sites.json', sites)
    print(f"  ✓ Site added: {SITE['n']}")
    print(f"     signal: {SITE['signal']}, criteria: {SITE['criteria']}")

    # 2. Wire video
    videos.setdefault(SITE['n'], [])
    existing_ids = {v['id'] for v in videos[SITE['n']]}
    if VIDEO['id'] not in existing_ids:
        videos[SITE['n']].append(VIDEO)
        save_json('videos.json', videos)
        print(f"  ✓ Video wired: {VIDEO['id']} - {VIDEO['title'][:60]}…")
    else:
        print(f"  · Video already wired")

    # 3. Add to Cambodia country tag
    if isinstance(countries, dict):
        if 'Cambodia' not in countries:
            countries['Cambodia'] = []
        if SITE['n'] not in countries['Cambodia']:
            countries['Cambodia'].append(SITE['n'])
            save_json('countries.json', countries)
            print(f"  ✓ Tagged under Cambodia (now {len(countries['Cambodia'])} sites)")
        else:
            print(f"  · Already tagged under Cambodia")

    # Summary
    print(f"\n--- summary ---")
    total_open = sum(1 for s in sites if s.get('signal') == 'open')
    print(f"  Total sites: {len(sites)}")
    print(f"  Open-question sites: {total_open}")
    print(f"  Total walkthroughs: {sum(len(v) for v in videos.values())}")

    # Run build
    print("\nRunning build.py to refresh public/index.html + public/data/…")
    build_script = REPO_ROOT / 'scripts' / 'build.py'
    if build_script.exists():
        r = subprocess.run(['python3', str(build_script)], capture_output=True, text=True)
        print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
        if r.returncode != 0:
            print("BUILD FAILED:", r.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
