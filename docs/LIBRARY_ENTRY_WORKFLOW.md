# Library entry workflow

Every Library entry — from Entry 01 today to Entry 05 next and onward — ships
through the same six-step process. This doc is the standard. Follow it and the
new entry will deploy frictionlessly.

## Terminology

- **OG card** (Open Graph card) is the proper term for the image that link
  preview clients render — Apple Messages, Slack, Discord, X, LinkedIn,
  Facebook all read the same `og:*` meta tags. Stop saying "iMessage card."
- **Library entry** is the prose article at `/library/<slug>.html`.
- **Hero photo** is the article's anchor image, also used as the OG card
  background.
- **JTBD subtitle** is the Open Graph card's `og:description` — see Step 4.

## The six steps

### 1. Author the article HTML

Create `public/library/<slug>.html`. Copy the structure of `true-monoliths.html`
or `mini-megaliths.html` (the most current pattern). Key invariants :

- Header has `<button class="share-btn">` and `<a class="back-btn">` inside
  `<div class="header-actions">`.
- The `shareArticle()` JS at the bottom must match the latest version (touch-
  detect for mobile, plain clipboard write on desktop, top-positioned toast
  with the Look Closer edge-flow). See any of Entries 01-04 for the exact
  block.
- `<figure class="photo">` CSS block must be in the `<style>` head (already
  the case if you copied from an existing entry).

### 2. Save the hero photo

Put it at `public/library/photos/<slug>/01-<descriptive-name>.jpg`. The
photo will be cover-cropped to 1200x630 for the OG card and rendered
full-bleed in the article body. High resolution is fine — 1600+ on the
short side gives the OG generator something to work with.

### 3. Register the entry in the OG generator

Open `scripts/generate-library-og-images.py` and add a new dict to the
`CARDS` list :

```python
dict(
    slug='<slug>',
    mode='photo',
    entry=5,
    title='Your Entry Title',
    subtitle="A JTBD question.",  # see Step 4
    photo=PHOTOS_DIR / '<slug>' / '01-<descriptive-name>.jpg',
),
```

That's the entire config. The CARDS list is the **single source of truth** —
the script handles cropping, gradient overlay, brand chrome, the entry pill,
the title block, and the subtitle. No other code change is needed to
generate the new OG image.

### 4. Write the JTBD subtitle

The subtitle is **not** the article's tagline. It is the **Jobs-To-Be-Done
question** that the visitor would hire this Library entry to answer. It must
be a question, it must be distinct from the title, and it must enhance
expectation rather than restate.

| Title says | Subtitle asks |
|---|---|
| What the entry **is** | What you'll **walk away knowing** |

Calibration examples from the existing entries :

| Entry | Title | JTBD subtitle |
|---|---|---|
| 01 | *What is a Megalith?* | *When does a stone stop being a rock and start being engineering?* |
| 02 | *Stone Circles* | *What were they keeping time of, two thousand years before Pythagoras?* |
| 03 | *Mini Megaliths* | *Why does a hundred-ton wall need a hand-sized stone?* |
| 04 | *True Monoliths* | *What kind of tool turns a mountain into a working city?* |

**Length target :** 6-14 words, 50-80 characters. Long enough to land the
provocation, short enough to read at iMessage's downscaled thumbnail size.
The subtitle font is 56px which means roughly two lines on the card.

**Voice :** Curiosity, not authority. The question opens a loop the reader
wants closed. "Why" / "What" / "When" / "How" beats "Discover," "Learn,"
"Understand."

### 5. Wire the head metadata

Add the standard `og:*` + `twitter:*` block to `<head>`. Use the
true-monoliths.html block as the template — change the URL slug, title,
description (= JTBD subtitle), and image filename. Leave the structural
fields (`og:type=article`, `og:site_name`, image dimensions, twitter:card)
unchanged.

```html
<link rel="canonical" href="https://theancientatlas.com/library/<slug>" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="The Ancient Atlas" />
<meta property="og:title" content="Entry Title — The Ancient Atlas Library" />
<meta property="og:description" content="The same JTBD question." />
<meta property="og:url" content="https://theancientatlas.com/library/<slug>" />
<meta property="og:image" content="https://theancientatlas.com/library/og/<slug>.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Entry Title — Ancient Atlas Library Entry N. The JTBD question." />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Entry Title — The Ancient Atlas Library" />
<meta name="twitter:description" content="The same JTBD question." />
<meta name="twitter:image" content="https://theancientatlas.com/library/og/<slug>.png" />
```

### 6. Generate, link, deploy

```bash
cd ~/Documents/GitHub/ancient-atlas
python3 scripts/generate-library-og-images.py    # produces public/library/og/<slug>.png
# Add the new entry to the Library hub list in public/library/index.html
# (drop a card under <main class="entries"> matching the existing pattern)
git add public/library/<slug>.html \
        public/library/photos/<slug>/ \
        public/library/og/<slug>.png \
        public/library/index.html \
        scripts/generate-library-og-images.py
git commit -m "Library Entry N: <slug> — <one-line summary>"
git push origin main
```

That's it. Netlify deploys in 30-90 seconds, the OG card is live, the article
is in the Library, and the share button works.

## Pre-flight checks for any new entry

Run these before pushing :

1. The OG card script ran without errors and produced
   `public/library/og/<slug>.png`.
2. The article HTML parses cleanly :
   ```bash
   python3 -c "from html.parser import HTMLParser
   p = HTMLParser(); p.feed(open('public/library/<slug>.html').read())"
   ```
3. The og:url, canonical, og:image, and twitter:image all reference
   `<slug>` with no `.html` suffix on the URL and `.png` on the image.
4. The Library hub at `/library/` lists the new entry.

## Visual reference for v4 OG card design

These are the locked-in sizing decisions from v4 :

| Element | Source size | Reason |
|---|---|---|
| Title (long) | 86px bold serif | Magazine-cover heft |
| Title (short, <18 chars) | 104px bold serif | Single-word punch |
| JTBD subtitle | 56px italic serif + 1px stroke | Doubled from v3 for prominence; carries the question |
| Brand wordmark "Ancient Atlas" | 48px bold serif + 2px stroke | Thickened, not enlarged |
| Brand subtitle "Library" | 32px italic + 1px stroke | Companion to wordmark |
| Compass mark radius | 38px, weight 4 | Heavy enough to read at thumbnail size |
| ENTRY tag pill text | 38px mono | Doubled per Jeff's v4 |
| ENTRY tag pill padding | 30px × 18px | Proportional to text |
| ENTRY tag pill border | 4px | Thick enough to read at downscale |
| URL stamp | **removed** | Redundant — the link client shows the URL underneath the card |

The photo is darkened to 0.68 brightness with a top + bottom gradient
overlay so the brand chrome and title block both read clearly against
any background. No URL stamp competes with the JTBD question for
attention at the bottom.

## Adding a Library entry that does NOT use a photo

If no hero photo exists yet, use `mode='vector'` instead of `mode='photo'`
and supply a `mark` function that draws the entry's decorative element.
See the `mark_stone_circle` example in the generator. The vector card
follows the same v4 sizing rules.

## Adding a Library hub-only card variant

The hub itself uses `mode='hub'` which composes from the global atlas
og-image. The hub's subtitle is set inside `compose_hub_card()` rather
than the CARDS dict, since it relates to the whole Library rather than
any single entry.
