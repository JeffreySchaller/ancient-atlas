#!/usr/bin/env python3
"""One shape for the whole nav, and numbers only where numbers belong.

The header had grown three different kinds of object wearing the same clothes: a
passive count, a bordered feature tile, and a plain link, all rendered as
"big thing on top, small word underneath". Nothing lined up because nothing was
actually the same: Studies and Experiences carried 7px/15px of padding and a
border, everything else 4px/0 and none, and the glyphs were emoji, which arrive
at whatever weight and baseline the OS feels like. Emoji were a real cause of the
misalignment, not just a style choice.

The rule now: NUMBERS LIVE IN THE LEDGER, GLYPHS LIVE IN THE NAV.

  Ledger, left, four counts:  Sites · With Video · Regions · Creators
  Nav, right, seven identical tiles: Studies, Experiences, Patterns, Articles,
  Editions, Support, Contact

Creators moves left into the ledger, because Jeff likes that number and it is a
count like the others. Articles, Patterns and Editions lose theirs: those were
inventory that changes, printed where nobody would notice it going stale, which
is the same argument that took the counts off the hover cards.

Every nav tile is now the same box, the same width, the same padding. The glyph
comes up to roughly the size the numbers were and the label drops to 8.5px, so
the mark leads and the word supports. Featured state (Studies, Experiences,
Editions) is border and background only, so it no longer changes the geometry.
Two of the three dividers go: one break, between the ledger and the nav, which is
the only distinction that means anything.

All seven glyphs are drawn as SVG in the same line language as the pattern marks:
24 viewBox, round joins, one stroke weight. No emoji anywhere in the row.

The hover cards are untouched. This rewrites tile innards inside the existing
wrappers rather than around them.

Idempotent: running twice is a no-op.
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"

GLYPH = {
    "studies": '<path d="M12 2.2 L13.7 10.3 L21.8 12 L13.7 13.7 L12 21.8 L10.3 13.7 '
               'L2.2 12 L10.3 10.3 Z"/>',
    "experiences": '<path d="M12 6.4 V19.2"/><path d="M7.6 19.2 H16.4"/>'
                   '<path d="M4.4 9.2 H19.6"/><circle cx="12" cy="4.8" r="1.3"/>'
                   '<path d="M4.4 9.2 L2.1 14.4 H6.7 Z"/>'
                   '<path d="M19.6 9.2 L17.3 14.4 H21.9 Z"/>',
    "patterns": '<circle cx="5.2" cy="7.6" r="1.7"/><circle cx="18.8" cy="6.8" r="1.7"/>'
                '<circle cx="12" cy="17.2" r="1.7"/>'
                '<path d="M6.9 7.4 L17.1 6.9"/><path d="M6.2 9.1 L11 15.7"/>'
                '<path d="M13.1 15.8 L17.9 8.4"/>',
    "articles": '<path d="M12 7.1 C10.1 5.4 7 4.9 4.1 5.3 V17.9 C7 17.5 10.1 18 12 19.7"/>'
                '<path d="M12 7.1 C13.9 5.4 17 4.9 19.9 5.3 V17.9 C17 17.5 13.9 18 12 19.7"/>'
                '<path d="M12 7.1 V19.7"/>',
    "editions": '<path d="M4.6 8.9 L19.4 8.9 L18.6 20.6 L5.4 20.6 Z"/>'
                '<path d="M8.4 8.9 L8.4 6 C8.4 4.5 9.9 3.1 12 3.1 C14.1 3.1 15.6 4.5 15.6 6 '
                'L15.6 8.9"/>',
    "support": '<path d="M12 20.1 C12 20.1 3.7 15.2 3.7 9.7 C3.7 7.1 5.6 5.4 7.9 5.4 '
               'C9.6 5.4 11.1 6.4 12 7.8 C12.9 6.4 14.4 5.4 16.1 5.4 C18.4 5.4 20.3 7.1 '
               '20.3 9.7 C20.3 15.2 12 20.1 12 20.1 Z"/>',
    "contact": '<path d="M3.3 6.4 H20.7 V17.6 H3.3 Z"/><path d="M3.3 7.1 L12 13.1 L20.7 7.1"/>',
}


def g(key):
    return ('<svg class="nav-glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.35" stroke-linejoin="round" stroke-linecap="round" '
            'aria-hidden="true">' + GLYPH[key] + "</svg>")


def tile(tag, attrs, key, label, featured=False, new=False):
    cls = "nav-tile" + (" is-featured" if featured else "") + (" is-new" if new else "")
    return (f'<{tag} class="{cls}" {attrs}>{g(key)}'
            f'<span class="nav-lbl">{label}</span></{tag}>')


src = INDEX.read_text()
orig = src

if 'class="nav-tile' not in src:
    # ---------------------------------------------------------- the seven tiles
    SWAPS = [
        # Studies
        ('<a class="stat-action stat-experiences" href="creators/" title="Creator Studies, No. 01">'
         '<div class="stat-val stat-exp-glyph">✦</div><div class="stat-lbl">Studies ↗</div></a>',
         tile("a", 'href="creators/" title="Creator Studies"', "studies", "Studies",
              featured=True, new=True)),
        # Experiences
        ('<a class="stat-action stat-experiences" href="experiences/feel-the-weight/" '
         'title="Experiences — six stones, 2.5 to 1,500 tons">'
         '<div class="stat-val stat-exp-glyph">⚖</div><div class="stat-lbl">Experiences ↗</div></a>',
         tile("a", 'href="experiences/feel-the-weight/" title="Experiences"', "experiences",
              "Experiences", featured=True, new=True)),
        # Patterns
        ('<a class="stat-action stat-patterns" href="patterns/" title="Patterns: the same '
         'engineering signatures across sites that never met"><div class="stat-val">7</div>'
         '<div class="stat-lbl">Patterns ↗</div></a>',
         tile("a", 'href="patterns/" title="Patterns"', "patterns", "Patterns")),
        # Articles
        ('<a class="stat-action hb-tile" href="library/index.html" title="Open the Library">'
         '<div class="stat-val" id="stat-articles">7</div><div class="stat-lbl">Articles ↗</div></a>',
         tile("a", 'href="library/index.html" title="The Library"', "articles", "Articles")),
        # Support
        ('<div class="stat-support hb-tile" onclick="openSupport()" title="Support the Atlas">'
         '<div class="stat-val stat-support-glyph">♥</div><div class="stat-lbl">Support ↗</div></div>',
         tile("div", 'onclick="openSupport()" title="Support the Atlas"', "support", "Support")),
        # Contact
        ('<a class="stat-contact hb-tile" href="contact.html" '
         'title="Report an error or suggest a site">'
         '<div class="stat-val stat-contact-glyph">✉</div><div class="stat-lbl">Contact ↗</div></a>',
         tile("a", 'href="contact.html" title="Contact"', "contact", "Contact")),
    ]
    for old, new in SWAPS:
        if src.count(old) != 1:
            sys.exit(f"ABORT: tile anchor matched {src.count(old)} times: {old[:80]!r}")
        src = src.replace(old, new)

    # Editions is multi-line in the source
    ed_old = re.search(
        r'<a class="stat-action ed-featured".*?</a>\n', src, re.S)
    if not ed_old:
        sys.exit("ABORT: could not find the Editions tile")
    src = src.replace(ed_old.group(0), tile(
        "a", 'href="https://editions.theancientatlas.com" target="_blank" rel="noopener" '
             'title="Editions"', "editions", "Editions", featured=True) + "\n")

    # ------------------------------------------------- Creators joins the ledger
    # Line-based, because each wrapper occupies exactly one line and a regex over
    # nested divs is how you lose a hover card without noticing.
    lines = src.split("\n")
    cre = [k for k, ln in enumerate(lines) if "openCreators()" in ln and "hb-wrap" in ln]
    reg = [k for k, ln in enumerate(lines) if 'id="stat-regions"' in ln]
    if len(cre) != 1 or len(reg) != 1:
        sys.exit(f"ABORT: found {len(cre)} Creators lines and {len(reg)} Regions lines, "
                 "expected 1 of each")
    block = lines.pop(cre[0]).replace('<div class="stat-lbl">Creators \u2197</div>',
                                      '<div class="stat-lbl">Creators</div>')
    reg = [k for k, ln in enumerate(lines) if 'id="stat-regions"' in ln][0]
    lines.insert(reg + 1, block)

    # ---------------------------------------------- one divider, not three
    div = '<div class="stat-divider" aria-hidden="true"></div>'
    lines = [ln for ln in lines if div not in ln]
    cre = [k for k, ln in enumerate(lines) if "openCreators()" in ln][0]
    lines.insert(cre + 1, "    " + div)
    src = "\n".join(lines)

# ------------------------------------------------------------------------ CSS
CSS = """
/* ===== Standardised nav tiles ================================================
   One box for all seven, so they line up because they ARE the same, not because
   three separate rules happen to agree. Numbers live in the ledger on the left;
   the nav is glyphs. Every mark is SVG in the same line language as the pattern
   glyphs: emoji arrive at whatever weight and baseline the OS chooses, which was
   a real cause of the old misalignment and not merely a style preference. */
.nav-tile{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
gap:7px;min-width:88px;padding:7px 8px;border-radius:9px;border:1px solid transparent;
position:relative;text-decoration:none;color:inherit;cursor:pointer;
transition:background .15s,border-color .15s,transform .15s}
.nav-tile:hover{background:rgba(201,168,76,.07);border-color:rgba(201,168,76,.22);
transform:translateY(-1px)}
.nav-glyph{width:21px;height:21px;flex:none;color:var(--champagne);
filter:drop-shadow(0 0 7px rgba(232,185,96,.26));transition:color .15s,transform .2s}
.nav-tile:hover .nav-glyph{color:#F3D998;transform:scale(1.07)}
.nav-lbl{font-family:var(--font-mono);font-size:8.5px;letter-spacing:.14em;
text-transform:uppercase;color:var(--cloud);white-space:nowrap;line-height:1}
.nav-tile:hover .nav-lbl{color:var(--ivory)}
/* Featured is skin, not geometry: it may not change the box. */
.nav-tile.is-featured{border-color:rgba(201,168,76,.20);background:rgba(201,168,76,.05)}
.nav-tile.is-featured:hover{background:rgba(201,168,76,.10)}
.nav-tile.is-new::after{content:"NEW";position:absolute;top:-5px;right:-5px;
font-family:var(--font-mono);font-size:6.5px;letter-spacing:.1em;color:#0A0A0E;
background:var(--amber);padding:1px 3px;border-radius:5px;font-weight:700;line-height:1.1}
@media (prefers-reduced-motion:reduce){.nav-tile,.nav-glyph{transition:none}
.nav-tile:hover{transform:none}.nav-tile:hover .nav-glyph{transform:none}}"""

if ".nav-tile{display:flex" not in src:
    anchor = ".stats > .stat-patterns,.hb-wrap > .stat-patterns{padding:6px 15px;margin:-2px -8px}"
    if anchor not in src:
        sys.exit("ABORT: CSS anchor missing")
    src = src.replace(anchor, anchor + CSS)

src = src.replace(".stats{display:flex;gap:18px;align-items:flex-start}",
                  ".stats{display:flex;gap:9px;align-items:flex-start}")

# Measuring the render caught two leftovers that reading would not have. The
# tiles were all 88x53 and still not aligned: .fw-wrap and .ed-wrap carried
# margin-top:-6px from when Experiences and Editions were taller than their
# neighbours, so those two sat 6px high. And Creators kept .stat-action, whose
# margin:-2px lifted it 2px above the other three ledger counts.
for wrap in (".fw-wrap{position:relative;margin-top:-6px}",
             ".ed-wrap{position:relative;margin-top:-6px}"):
    if wrap in src:
        src = src.replace(wrap, wrap.replace(";margin-top:-6px", ""))
src = src.replace('<div class="stat-action hb-tile" onclick="openCreators()"',
                  '<div class="hb-tile" onclick="openCreators()"')

if src != orig:
    INDEX.write_text(src)

n = src.count('class="nav-tile')
assert n == 7, "expected 7 nav tiles, got %d" % n
n_div = src.count('<div class="stat-divider"')
assert n_div == 1, "expected exactly 1 divider, got %d" % n_div
for e in ("✦", "⚖", "♥", "✉"):
    assert e not in src.split("</header>")[0], "emoji %s survives in the header" % e
head = src.split("</header>")[0]
# Four counts left in the row: Sites, With Video, Regions, Creators. The assert
# double-counted the id-bearing one on the first pass, which is a reminder that a
# check you have not seen fail is not a check yet.
n_num = head.count('<div class="stat-val"')
assert n_num == 4, "expected 4 ledger numbers in the header, got %d" % n_num
assert 'id="stat-creators"' in head, "Creators lost"
n_wrap = src.count('class="hb-wrap"')
assert n_wrap == 9, "a hover card wrapper was lost: %d of 9" % n_wrap
assert src.count("ed-bloom") > 0 and src.count("fw-bloom") > 0, "existing blooms damaged"

print("7 nav tiles standardised. Numbers now only in the ledger.")
print("Glyphs: " + ", ".join(sorted(GLYPH)))
