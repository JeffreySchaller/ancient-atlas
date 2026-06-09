# Batch authoring workflow

The Ancient Atlas data lives in two synchronized directories within this
repo :

| Path | Role |
|---|---|
| `data/*.json` | Source of truth for content. Batch scripts read and write here. |
| `public/data/*.json` | Mirrored copy that Netlify serves directly. `scripts/build.py` syncs this from `data/` and bakes the same data into `public/index.html`. |

**Both directories must always be in sync.** `scripts/build.py` enforces
this — it reads `data/`, writes `public/data/` and `public/index.html`.

## Authoring a new content batch

```bash
cd ~/Documents/GitHub/ancient-atlas
# 1. Write your batch script under scripts/
#    Pattern: scripts/add-<creator-or-topic>-batch.py
#    The script must read from data/, validate, and write back to data/.
#    It must be idempotent (safe to re-run).

# 2. Run the batch
python3 scripts/add-<topic>-batch.py

# 3. Rebuild public/index.html and mirror public/data/
python3 scripts/build.py

# 4. Regenerate OG image if site count or walkthrough count changed
python3 scripts/regenerate-og-image.py

# 5. Commit and push
git add data/ public/data/ public/index.html public/og-image.png scripts/
git commit -m "<topic> batch: +N sites, +M wires"
git push origin main
```

Netlify auto-deploys from `main`. Live in ~ 30-90 seconds.

## What NOT to do

- **Never run a batch script from outside this repo.** Old iCloud-based
  scripts at `~/Library/Mobile Documents/com~apple~CloudDocs/Projects/ancient-atlas/phase-2-output/`
  are deprecated and will write stale data over the canonical state.
  That directory is now marked `_DEPRECATED/` with a STOP README.

- **Never copy data files from iCloud into this repo.** The iCloud
  Phase 2 working copy has been stale since early 2026. The June 2026
  Secrets in Stone push briefly downgraded the live atlas from 499 to
  300 sites because it was authored against the stale iCloud source.
  See git log for the recovery commit.

- **Never bypass `scripts/build.py`.** If you hand-edit `data/sites.json`
  but skip the rebuild, `public/data/` and `public/index.html` will drift
  out of sync and Netlify will serve an inconsistent state.

## Pre-flight check (recommended)

Before any content batch ships, run :

```bash
python3 -c "
import json
s = json.load(open('data/sites.json'))
c = json.load(open('data/creators.json'))
v = json.load(open('data/videos.json'))
print(f'PRE-FLIGHT: {len(s)} sites, {len(c)} creators, {sum(len(x) for x in v.values())} walkthroughs')
print('  ↪ If sites or creators is LOWER than the previous deploy, ABORT.')
"
```

If the pre-flight count is lower than what's currently live at
theancientatlas.com, something is wrong. **Abort the batch.**

## Schema reference

`data/sites.json` is a list of site objects :

```json
{
  "n":   "Site name (canonical, used as key in videos.json)",
  "lat": 13.4445,
  "lng": 103.9461,
  "cat": "temple | pyramid | underground | rock-cut | tomb | megalithic | city | settlement | geoglyph",
  "region": "Africa | Asia | Europe | Middle East | South America | etc.",
  "tier": 1,
  "signal": "open",
  "criteria": ["precision", "polygonal", "scale", "hardness",
               "stratigraphy", "geometry", "machining"],
  "desc": "..."
}
```

`data/videos.json` is a dict keyed by site name, each value a list of
video objects :

```json
{
  "id": "11-char-YouTube-ID",
  "title": "Video title | Creator name",
  "cr": "praveenmohan",
  "added": "2026-06-08",
  "published": "2025-07-15"
}
```

`data/creators.json` is a dict keyed by short slug :

```json
{
  "praveenmohan": {
    "name": "Praveen Mohan",
    "handle": "@RealPraveenMohan",
    "subs": "Short tagline",
    "color": "#DB6A6B",
    "tier": 1
  }
}
```

Valid criteria values : `precision`, `polygonal`, `scale`, `hardness`,
`stratigraphy`, `geometry`, `machining`. Anything else will fail
pre-flight validation in batch scripts.

## Backup recovery (if a stale push happens again)

The canonical data is mirrored across :

1. `data/*.json` (read by batches)
2. `public/data/*.json` (mirrored by build.py)
3. The embedded SITES/CREATORS/VIDEOS constants in `public/index.html`

If any one of these gets corrupted, the others usually survive. To
restore :

```bash
# Restore data/ from public/data/ (if data/ got stunted)
cp public/data/*.json data/
# Or restore from HEAD before the bad commit
git show HEAD~1:public/data/sites.json > data/sites.json
# Then rebuild
python3 scripts/build.py
```

The June 2026 recovery used pattern #1 because the bad batch wrote to
`data/` and `public/index.html` but not `public/data/`.
