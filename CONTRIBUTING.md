# Contributing to the Ancient Atlas

Thank you for wanting to add to the atlas. This guide will get you contributing in 10 minutes.

The atlas is editorially curated. Not every YouTube video about an ancient site belongs here. We aim for **walkthroughs** that show the site itself — preferably with the creator on the ground — and that bring something more than what a Wikipedia article would give a reader.

---

## What we accept

**Yes :**

- On-site walkthroughs (creator visits the place with a camera)
- Field reports from researchers and creators with established credibility (Hugh Newman, Brien Foerster, UnchartedX, Cosmic Summit, Secrets in Stone, etc.)
- Long-form documentaries about specific sites
- Drone or first-person footage of architecture, masonry, or alignments
- Original-source academic content (lectures, conference talks, recorded interviews)
- Multi-site documentaries that cover atlas-cataloged places (these get auto-badged with the "Also covers" treatment)

**No :**

- Pure clickbait ("ANCIENT ALIENS DESTROYED THE TRUTH!!" titles)
- Reaction videos / commentary on someone else's footage
- AI-generated narration of stock footage
- Videos that misidentify the site
- Hate speech, racism, or content that mocks the cultures being shown
- Content where the site is incidental (e.g., a travel vlog where Stonehenge appears for 30 seconds)

When in doubt, **ask in the PR description** and a maintainer will weigh in.

---

## How to add a single walkthrough

### Option A : The friction-free way (recommended)

1. Visit **[theancientatlas.com/contribute](https://theancientatlas.com/contribute)**
2. Paste the YouTube URL
3. The page auto-fetches the video's title and creator via the YouTube oEmbed API
4. Pick the site from the searchable dropdown
5. Click "Submit"
6. The form opens a pre-filled pull request in GitHub — you click "Propose change"
7. A maintainer reviews and merges within 48 hours

### Option B : Direct GitHub edit

1. Open [`data/videos.json`](data/videos.json) in this repo
2. Click the pencil icon (edit this file)
3. Find the site name as a JSON key
4. Add an entry like :

```json
"Dolmen of Menga": [
  {"id": "WZo6sw2y-4k", "title": "The Fabulous Construction of the Dolmen de Menga", "cr": "prehistoryguys"}
]
```

Where :
- `id` = the YouTube video ID (the part after `v=`)
- `title` = the actual video title from YouTube (the CI will verify this matches)
- `cr` = the creator key (see [`data/creators.json`](data/creators.json) for the list of registered creators)

5. Commit and open a pull request
6. CI runs automatic checks (oEmbed verification, duplicate detection, schema validation) — your PR will show ✓ or ✗ on each
7. A maintainer reviews and merges

---

## How to add multiple walkthroughs at once

The atlas contribute page has a **bulk mode** at [theancientatlas.com/contribute?mode=bulk](https://theancientatlas.com/contribute?mode=bulk).

Paste up to 25 YouTube URLs (one per line). The page :

- Validates each URL via oEmbed in parallel
- Lets you assign each to a site from the dropdown
- Opens a single pull request with all entries at once

Bulk mode is the right path when you've just returned from a research session with a long list of new videos.

---

## How to add a new site (not yet in the catalog)

New sites require more editorial review than new walkthroughs. The process :

1. Open an **issue** first using the "New site proposal" template
2. The issue should include : site name, country, coordinates (lat/lng), category (megalithic / pyramid / temple / etc.), era, civilization, and a brief description
3. A maintainer responds with feedback within 48 hours
4. If approved, the maintainer either adds the site directly or asks you to submit a PR with the entry in `data/sites.json`

We're rigorous about new sites because every entry on the map represents an editorial claim about the catalog's scope. We aim for : significant, well-documented, ancient, and visitable.

---

## How to register a new creator

If you want to add a walkthrough from a creator who isn't yet in `data/creators.json` :

1. In your PR, add the creator to `data/creators.json` with :

```json
"creatorkey": {
  "name": "Channel Name as It Appears on YouTube",
  "handle": "@ChannelHandle",
  "subs": "Brief editorial note about what they cover",
  "color": "#XXXXXX",
  "tier": 2
}
```

Tier guidance :
- **Tier 1** = primary editorial voices the atlas explicitly champions. Reserved for the most credible, original-research creators.
- **Tier 2** = significant contributors with consistent quality.
- **Tier 3** = useful niche or emerging voices.

2. Then reference the new creator key in your video entry's `cr` field.

3. The maintainer will adjust the tier in review if needed.

---

## What the CI checks do

When you open a PR, GitHub Actions runs three automatic checks. All three must pass before merge :

| Check | What it does |
|---|---|
| **oEmbed verification** | Fetches the YouTube oEmbed for each new video ID and confirms (a) the video exists, (b) the `cr` field matches the actual channel, (c) the title is sensible. This catches misattributions at PR time, not after deploy. |
| **Duplicate detection** | Runs `audit-videos.py` and blocks if the PR introduces a duplicate site key or a same-ID-in-same-site collision. |
| **Schema validation** | Confirms every entry has the required fields and they're the right types. |

If a check fails, you'll see what went wrong directly in the PR. Fix it, push again, and CI re-runs automatically.

---

## Editorial style notes

The atlas writes with a particular voice. You don't need to nail it for a video entry, but if your contribution involves description text :

- No em dashes (telltale AI signal — we use periods, commas, colons, semicolons instead)
- No "genuinely," "delve," or "straightforward"
- Future-forward language; contrast through specificity not negation
- Concise expert tone; doesn't need to prove credibility

See [`docs/EDITORIAL_GUIDELINES.md`](docs/EDITORIAL_GUIDELINES.md) for the full editorial standard.

---

## Recognition

Contributors who consistently add high-quality entries become part of the atlas's editorial team. We track contribution counts and tenure :

- **5 merged PRs** → self-merge privileges for additions to existing sites
- **20 merged PRs** → ability to propose new sites
- **50 merged PRs** → invited to the editorial team

We also tag contributor-driven walkthroughs as "Filmed for the Atlas" when applicable, giving the contributor and creator visible attribution on the site.

---

## Questions?

- Open an issue on GitHub
- Email [hello@theancientatlas.com](mailto:hello@theancientatlas.com)
- Use the [contact form](https://theancientatlas.com/contact)

The atlas grows by what readers and contributors notice. Thanks for caring enough to add to it.
