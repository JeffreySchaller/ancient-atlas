#!/usr/bin/env python3
"""A hover card for every tile in the header.

Editions and Experiences already had one, and they are the two tiles people
actually click. That is not a coincidence: a card answers "what is behind this
number" before you spend a navigation on finding out. The other nine tiles were
bare numbers with an arrow, which asks the reader to gamble.

So this generalises the two bespoke blooms into one `.hb` system and hangs nine
new cards off it. The existing `.ed-*` and `.fw-*` blooms are left alone: they
carry real artwork and a gag animation, they work, and rewriting working code to
satisfy a taxonomy is how you break a header at 11pm.

Every number on every card comes out of the data files at build time. Nothing is
typed twice, so nothing can drift.

Two things this had to get right:

  Specificity. `.stats > div, .stats > a` at (0,1,1) styles the tiles today.
  Wrapping a tile in `.hb-wrap` moves it out of that selector's reach, so each
  wrapped tile needs its padding restored at a specificity that does not then
  collide with the scoped rules Studies and Patterns already carry. The plain
  tiles get an explicit `.hb-tile` class rather than a `:not()` dodge, because
  `:not()` would have added an element term and quietly outranked them.

  The header is hidden below 950px in portrait, so these are desktop-only by
  construction and need no separate suppression.

Idempotent: running twice is a no-op.
"""
import ast
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"
DATA = REPO / "data"

sites = json.loads((DATA / "sites.json").read_text())
videos = json.loads((DATA / "videos.json").read_text())
creators = json.loads((DATA / "creators.json").read_text())
feature = json.loads((DATA / "feature.json").read_text())
patterns = {k: v for k, v in json.loads((DATA / "patterns.json").read_text()).items()
            if not k.startswith("_")}

GLYPHS = None
for node in ast.walk(ast.parse((REPO / "scripts" / "build-patterns.py").read_text())):
    if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "GLYPHS" for t in node.targets):
        GLYPHS = ast.literal_eval(node.value)
if not GLYPHS:
    sys.exit("ABORT: could not read GLYPHS out of build-patterns.py")

n_sites = len(sites)
n_vid = len({k for k, v in videos.items() if v})
n_wires = sum(len(v) for v in videos.values())
regions = collections.Counter(s.get("region", "?") for s in sites)
n_regions = len(regions)
per_creator = collections.Counter()
for lst in videos.values():
    for w in lst:
        if w.get("cr"):
            per_creator[w["cr"]] += 1
n_creators = len(creators)
top5 = per_creator.most_common(5)

# feature.json stores a SLUG ("ageless-rock"); creators.json is keyed by a
# squashed handle ("agelessrock"). A plain dict lookup silently returns nothing,
# which rendered "ageless-rock, 0 walkthroughs" on the first run. Resolve it
# properly and refuse to build rather than ship a zero.
def _slug(x):
    return "".join(ch for ch in x.lower() if ch.isalnum())


_want = _slug(feature.get("featured_study", ""))
featured_key = next((k for k in creators
                     if _slug(k) == _want or _slug(creators[k].get("name", "")) == _want), "")
if not featured_key:
    sys.exit(f"ABORT: feature.json names {feature.get('featured_study')!r} and nothing in "
             "creators.json resolves to it")
featured_name = creators[featured_key].get("name", featured_key)
featured_n = per_creator.get(featured_key, 0)
if featured_n < 1:
    sys.exit(f"ABORT: {featured_name} resolves but carries 0 wires; that is not a feature")

ARTICLES = [
    ("What is a megalith?", "megaliths.html"),
    ("Stone Circles", "stone-circles.html"),
    ("Mini Megaliths", "mini-megaliths.html"),
    ("True Monoliths", "true-monoliths.html"),
    ("Finding North", "finding-north.html"),
    ("The View From Above", "the-view-from-above.html"),
    ("The Convergence Question", "the-convergence-question.html"),
]
for _, href in ARTICLES:
    if not (REPO / "public" / "library" / href).exists():
        sys.exit(f"ABORT: library/{href} is listed here but not on disk")
n_articles = len(ARTICLES)

src = INDEX.read_text()
orig = src

# ---------------------------------------------------------------------- pieces


def rows(pairs):
    return ('<div class="hb-rows">'
            + "".join(f'<div class="hb-row"><span>{a}</span><b>{b}</b></div>' for a, b in pairs)
            + "</div>")


def bars(pairs, top):
    """Bars without labels. The shape carries the point, that the spread is
    lopsided, and a shape stays true as the data grows in a way a printed
    figure does not."""
    out = []
    for name, n in pairs:
        pct = max(8, round(n / top * 100))
        out.append('<div class="hb-brow"><span>' + name + '</span>'
                   '<i class="hb-bar" style="width:' + str(pct) + '%"></i></div>')
    return '<div class="hb-rows">' + ''.join(out) + '</div>'


def glyph_row():
    order = sorted(patterns, key=lambda k: patterns[k]["index"])
    svgs = "".join(
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" '
        f'stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">{GLYPHS[k]}</svg>'
        for k in order)
    return f'<div class="hb-glyphs">{svgs}</div>'


def card(kicker, title, sub="", body="", cta=None, side=""):
    cta_html = ""
    if cta:
        label, attrs = cta
        cta_html = f'<a class="hb-cta" {attrs}>{label}</a>'
    return (f'<div class="hb{side}" aria-hidden="true">'
            f'<p class="hb-k">{kicker}</p>'
            f'{body if body and "hb-glyphs" in body else ""}'
            f'<p class="hb-t">{title}</p>'
            + (f'<p class="hb-s">{sub}</p>' if sub else "")
            + (body if body and "hb-glyphs" not in body else "")
            + cta_html + "</div>")


# Story, not inventory. Two reasons, both of them right.
#
# A printed count is a liability. It is correct for exactly as long as nobody
# adds a site, and when it drifts nobody notices, so the reader quietly concludes
# the Atlas cannot count its own rows. The live tile beside each card already
# carries that number and is wired to the data. The card must not repeat it.
#
# And a figure is a poor way into a story. "618 sites" is a fact about a
# database. "Every stone here, someone stood next to" is a reason to click. The
# tile is the ledger; the card is the invitation. Two different jobs, and the
# card was doing the tile's.
#
# The region bars are the one survivor, and they keep their shape while losing
# their labels: the point is that the distribution is lopsided, and a bar stays
# true as the data grows in a way a printed number does not.
CARDS = {
    "sites": card(
        "The Atlas",
        "Every stone here, someone stood next to.",
        "Placed by hand and checked against the ground, not scraped from a list.",
        "", ("Browse the index &rarr;", 'href="sites/"')),
    "video": card(
        "Walkthroughs",
        "You do not have to take anyone's word.",
        "Most of this map comes with someone walking you through it, camera in hand.",
        "", ("See the creators &rarr;", 'href="creators/"')),
    "regions": card(
        "Where",
        "The deep past is not evenly spread.",
        "Some coastlines are crowded. Whole continents are nearly empty. Both are worth a look.",
        bars(regions.most_common(4), regions.most_common(1)[0][1]),
        ("Browse by region &rarr;", 'href="sites/"')),
    "studies": card(
        "Creator Studies &middot; No. 01",
        "One channel's life's work, laid back over the map.",
        "A study takes a single creator and shows you everywhere they have actually been.",
        "", ("Open the studies &rarr;", 'href="creators/"')),
    # "The Atlas filmed none of this" was written to make a point about credit
    # and overshot into a false claim: Ancient Atlas is a creator too, listed in
    # the sidebar with everyone else, and now carries its own fieldwork. Same
    # point, made true.
    "creators": card(
        "Creators",
        "Built with the people who went there.",
        "Most of the footage is theirs, some of it is ours, and every clip is credited and links back.",
        "", ("Meet them &rarr;", 'href="creators/"')),
    "articles": card(
        "The Library",
        "How to read a site before anyone tells you what it means.",
        "The vocabulary: what counts as a megalith, what a joint can prove, what the ground remembers.",
        rows([(t, "") for t, _ in ARTICLES[:4]] + [("and more", "")]),
        ("Open the Library &rarr;", 'href="library/index.html"')),
    "patterns": card(
        "Patterns",
        "The same idea, in places that never met.",
        "Sort by method instead of by map and the coincidences stop looking like coincidences.",
        glyph_row(), ("See the patterns &rarr;", 'href="patterns/"')),
    "support": card(
        "Support", "Free, and staying free.",
        "No ads, no paywall, nothing tracked beyond a page count.",
        "", ("How to help &rarr;", 'href="#" onclick="openSupport();return false;"'), side=" hb--r"),
    "contact": card(
        "Contact", "Found something wrong?",
        "Corrections and new sites land in the same inbox, and both get read.",
        "", ("Get in touch &rarr;", 'href="contact.html"'), side=" hb--r"),
}

# ------------------------------------------------------------------- the tiles
# (anchor in the file, replacement) — each wraps one tile and drops its card in.
TILES = [
    ('<div><div class="stat-val" id="stat-sites">0</div><div class="stat-lbl">Sites</div></div>',
     '<div class="hb-wrap"><div class="hb-tile"><div class="stat-val" id="stat-sites">0</div>'
     '<div class="stat-lbl">Sites</div></div>{card}</div>', "sites"),
    ('<div><div class="stat-val" id="stat-vids">0</div><div class="stat-lbl">With Video</div></div>',
     '<div class="hb-wrap"><div class="hb-tile"><div class="stat-val" id="stat-vids">0</div>'
     '<div class="stat-lbl">With Video</div></div>{card}</div>', "video"),
    ('<div><div class="stat-val" id="stat-regions">0</div><div class="stat-lbl">Regions</div></div>',
     '<div class="hb-wrap"><div class="hb-tile"><div class="stat-val" id="stat-regions">0</div>'
     '<div class="stat-lbl">Regions</div></div>{card}</div>', "regions"),
    ('<a class="stat-action stat-experiences" href="creators/" title="Creator Studies — No. 01: '
     'Ageless Rock, 285 walkthroughs across 197 sites"><div class="stat-val stat-exp-glyph">✦</div>'
     '<div class="stat-lbl">Studies ↗</div></a>',
     '<div class="hb-wrap"><a class="stat-action stat-experiences" href="creators/" '
     'title="Creator Studies, No. 01"><div class="stat-val stat-exp-glyph">✦</div>'
     '<div class="stat-lbl">Studies ↗</div></a>{card}</div>', "studies"),
    ('<div class="stat-action" onclick="openCreators()" title="View all creators">'
     '<div class="stat-val" id="stat-creators">0</div><div class="stat-lbl">Creators ↗</div></div>',
     '<div class="hb-wrap"><div class="stat-action hb-tile" onclick="openCreators()" '
     'title="View all creators"><div class="stat-val" id="stat-creators">0</div>'
     '<div class="stat-lbl">Creators ↗</div></div>{card}</div>', "creators"),
    ('<a class="stat-action" href="library/index.html" title="Open the Library — 6 articles on '
     'reading deep history">\n      <div class="stat-val" id="stat-articles">6</div>\n'
     '      <div class="stat-lbl">Articles ↗</div>\n    </a>',
     '<div class="hb-wrap"><a class="stat-action hb-tile" href="library/index.html" '
     'title="Open the Library">'
     '<div class="stat-val" id="stat-articles">{n_articles}</div>'
     '<div class="stat-lbl">Articles ↗</div></a>{card}</div>', "articles"),
    ('<a class="stat-action stat-patterns" href="patterns/" title="Patterns: the same engineering '
     'signatures across sites that never met">\n      <div class="stat-val">7</div>\n'
     '      <div class="stat-lbl">Patterns ↗</div>\n    </a>',
     '<div class="hb-wrap"><a class="stat-action stat-patterns" href="patterns/" '
     'title="Patterns: the same engineering signatures across sites that never met">'
     '<div class="stat-val">7</div><div class="stat-lbl">Patterns ↗</div></a>{card}</div>',
     "patterns"),
    ('<div class="stat-support" onclick="openSupport()" title="Support the Atlas">'
     '<div class="stat-val stat-support-glyph">♥</div><div class="stat-lbl">Support ↗</div></div>',
     '<div class="hb-wrap"><div class="stat-support hb-tile" onclick="openSupport()" '
     'title="Support the Atlas"><div class="stat-val stat-support-glyph">♥</div>'
     '<div class="stat-lbl">Support ↗</div></div>{card}</div>', "support"),
    ('<a class="stat-contact" href="contact.html" title="Report an error or suggest a site">'
     '<div class="stat-val stat-contact-glyph">✉</div><div class="stat-lbl">Contact ↗</div></a>',
     '<div class="hb-wrap"><a class="stat-contact hb-tile" href="contact.html" '
     'title="Report an error or suggest a site"><div class="stat-val stat-contact-glyph">✉</div>'
     '<div class="stat-lbl">Contact ↗</div></a>{card}</div>', "contact"),
]

if 'class="hb-wrap"' not in src:
    for old, new, key in TILES:
        if src.count(old) != 1:
            sys.exit(f"ABORT: tile {key!r} anchor matched {src.count(old)} times, expected 1")
        src = src.replace(old, new.replace("{card}", CARDS[key])
                                   .replace("{n_articles}", str(n_articles)))

# -------------------------------------------------------------------- the CSS
CSS_ANCHOR = ".stats > .stat-experiences,.fw-wrap > .stat-experiences{padding:7px 15px}"
CSS_FIXED = (".stats > .stat-experiences,.fw-wrap > .stat-experiences,"
             ".hb-wrap > .stat-experiences{padding:7px 15px}")
if ".hb-wrap > .stat-experiences" not in src:
    if CSS_ANCHOR not in src:
        sys.exit("ABORT: the Studies padding rule is gone")
    src = src.replace(CSS_ANCHOR, CSS_FIXED)

PAT_ANCHOR = ".stats > .stat-patterns{padding:6px 15px;margin:-2px -8px}"
PAT_FIXED = ".stats > .stat-patterns,.hb-wrap > .stat-patterns{padding:6px 15px;margin:-2px -8px}"
if ".hb-wrap > .stat-patterns" not in src:
    if PAT_ANCHOR not in src:
        sys.exit("ABORT: the Patterns padding rule is gone")
    src = src.replace(PAT_ANCHOR, PAT_FIXED)

BLOOM_CSS = """
/* ===== Header hover cards =====================================================
   One generic bloom, nine tiles. Deliberately NOT a rewrite of .ed-bloom or
   .fw-bloom: those two carry artwork and an animation, they work, and merging
   them into this would be refactoring for tidiness at the cost of a working
   header. Visual parameters are copied so all eleven read as one system.

   `.stats > div, .stats > a` (0,1,1) no longer reaches a wrapped tile, so the
   plain ones carry an explicit .hb-tile class. A `:not(.hb)` dodge would have
   added an element term and silently outranked the scoped Studies and Patterns
   rules above. */
.hb-wrap{position:relative}
.hb-wrap > .hb-tile{padding:4px 0}
.hb-wrap > .hb{position:absolute;top:calc(100% + 12px);left:-12px;
transform:translateY(-6px) scale(.98);width:278px;
background:linear-gradient(160deg,rgba(26,26,34,.98),rgba(13,13,18,.98));
border:1px solid rgba(201,168,76,.30);border-radius:14px;padding:14px;
box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 0 1px rgba(201,168,76,.06);
opacity:0;pointer-events:none;text-align:left;
transition:opacity .22s ease,transform .22s cubic-bezier(.2,.8,.2,1);z-index:1200}
.hb-wrap > .hb.hb--r{left:auto;right:-12px}
.hb::before{content:"";position:absolute;top:-7px;left:26px;width:12px;height:12px;
background:rgba(26,26,34,.98);border-left:1px solid rgba(201,168,76,.30);
border-top:1px solid rgba(201,168,76,.30);transform:rotate(45deg)}
.hb.hb--r::before{left:auto;right:26px}
/* invisible bridge across the 12px gap, so a slow cursor does not lose the card */
.hb::after{content:"";position:absolute;top:-16px;left:0;right:0;height:16px}
.hb-wrap:hover > .hb{opacity:1;pointer-events:auto;transform:translateY(0) scale(1)}
.hb-k{font-family:var(--font-mono);font-size:8.5px;letter-spacing:.19em;text-transform:uppercase;
color:var(--champagne);margin:0 0 9px}
.hb-t{font-family:var(--font-serif);font-size:17.5px;font-weight:600;color:var(--ivory);
line-height:1.16;margin:0}
.hb-s{font-size:12px;line-height:1.5;color:var(--mist);margin:5px 0 0}
.hb-rows{margin:11px 0 0;display:flex;flex-direction:column;gap:6px}
.hb-row{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
font-family:var(--font-mono);font-size:10px;letter-spacing:.02em;color:var(--cloud)}
.hb-row b{color:var(--champagne);font-weight:500;flex:none}
.hb-brow{display:flex;align-items:center;gap:8px;font-family:var(--font-mono);font-size:10px;
color:var(--cloud)}
.hb-brow span{width:88px;flex:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hb-brow b{color:var(--champagne);font-weight:500;flex:none;width:26px;text-align:right}
.hb-bar{height:3px;border-radius:3px;background:linear-gradient(90deg,#C9A84C,#E8B960);
flex:0 1 auto;min-width:6px}
.hb-glyphs{display:flex;align-items:center;gap:8px;color:var(--champagne);margin:0 0 11px}
.hb-glyphs svg{width:22px;height:22px;flex:none}
.hb-cta{display:flex;align-items:center;justify-content:center;gap:7px;width:100%;
font-family:var(--font-sans);font-size:13px;font-weight:600;color:var(--obsidian);
background:linear-gradient(180deg,#F3D998,#E8B960);padding:9px 14px;border-radius:9px;
text-decoration:none;box-shadow:0 6px 16px rgba(201,168,76,.22);margin-top:12px}
@media (prefers-reduced-motion:reduce){.hb-wrap > .hb{transition:opacity .01s}}"""

if ".hb-wrap > .hb{position:absolute" not in src:
    src = src.replace(PAT_FIXED, PAT_FIXED + BLOOM_CSS)

if src != orig:
    INDEX.write_text(src)

n_wrap = src.count('class="hb-wrap"')
assert n_wrap == 9, "expected 9 wrappers, got %d" % n_wrap
assert src.count('class="hb-cta"') == 9, "expected 9 CTAs"
assert src.count("hb-glyphs") >= 2, "pattern glyph row missing"
assert ".hb-wrap > .stat-experiences" in src and ".hb-wrap > .stat-patterns" in src, \
    "scoped padding not extended to wrapped tiles"
assert 'id="stat-articles">7<' in src, "articles tile not corrected to 7"
assert src.count("fw-bloom") > 0 and src.count("ed-bloom") > 0, "existing blooms damaged"

# The previous run passed every assertion above while a card read
# "ageless-rock, 0 walkthroughs", because nothing asserted on what the cards
# actually SAY. These do. A digit anywhere in a headline or body is now a build
# failure, which enforces the no-stale-counts rule structurally rather than by
# remembering to.
import re as _re

titles = _re.findall(r'<p class="hb-t">(.*?)</p>', src)
bodies = _re.findall(r'<p class="hb-s">(.*?)</p>', src)
assert len(titles) == 9, "expected 9 card headlines, got %d" % len(titles)
for t in titles + bodies:
    if _re.search(r"[0-9]", t):
        sys.exit("ABORT: card copy carries a figure that will go stale: %r" % t)
for must in ("Every stone here, someone stood next to.",
             "Built with the people who went there.",
             "One channel's life's work, laid back over the map."):
    assert must in src, "missing headline: %s" % must

_own = sum(1 for lst in videos.values() for w in lst if w.get("cr") == "ancientatlas")
if _own < 1:
    sys.exit("ABORT: the Creators card says some of the footage is ours; "
             "videos.json carries no ancientatlas wires to back that")

print("9 header cards wired. Story-led, no printed counts.")
print("Creators card claim checked: %d Ancient Atlas wires in videos.json." % _own)
print("Integrity: feature.json resolves to %s (%d wires). %d sites, %d regions, %d articles."
      % (featured_name, featured_n, n_sites, n_regions, n_articles))
print("Region bars keep their shape and lost their labels.")
