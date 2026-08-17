#!/usr/bin/env python3
# Feel the Weight: the four-band gradient.
#
#   Band 1  what it is       the real mesh, a person beside it, one said line
#   Band 2  what it weighs   three flags, a swatch that names what changed,
#                            a field of that country's vehicle
#   Band 3  if you keep      three metaphor cards, then the Giza-block dots
#           looking
#   Band 4  the real thing   the photograph, full width, last
#
# Everything to do with pressing and holding is removed, not hidden. Numbers
# survive only where the reader can check them against what is on screen: a
# dimension next to a 1.8 m figure, a field of silhouettes they can count.
#
# Idempotent. Every assertion reads the END STATE of the file, never the
# number of edits performed.

import re, sys
from pathlib import Path

APP = Path(__file__).resolve().parent / "app.html"
src = APP.read_text()
orig = len(src)

DQ = chr(34)

# ---------------------------------------------------------------- helpers

def cut_element(s, start_marker, tag="div"):
    """Remove one balanced <tag ...>...</tag> beginning at start_marker."""
    i = s.find(start_marker)
    if i == -1:
        return s, False
    open_re = re.compile("<" + tag + r"\b")
    close = "</" + tag + ">"
    depth, j = 0, i
    while True:
        m_open = open_re.search(s, j)
        m_close = s.find(close, j)
        if m_close == -1:
            sys.exit("ABORT: unbalanced <%s> from %r" % (tag, start_marker[:60]))
        if m_open and m_open.start() < m_close:
            depth += 1
            j = m_open.end()
            continue
        depth -= 1
        j = m_close + len(close)
        if depth == 0:
            return s[:i] + s[j:], True

def cut_all(s, start_marker, tag="div"):
    n = 0
    while True:
        s, hit = cut_element(s, start_marker, tag)
        if not hit:
            return s, n
        n += 1

def section_span(s, label):
    i = s.find('data-screen-label="%s"' % label)
    if i == -1:
        return None
    a = s.rindex("<section", 0, i)
    b = s.index("</section>", i) + len("</section>")
    return a, b

def take_section(s, label):
    sp = section_span(s, label)
    if sp is None:
        return s, None
    return s[:sp[0]] + s[sp[1]:], s[sp[0]:sp[1]]

def sub1(s, old, new, what):
    if new in s and old not in s:
        return s                      # already applied
    if old not in s:
        sys.exit("ABORT: anchor missing for %s" % what)
    return s.replace(old, new)


# ---------------------------------------------------------------- 1. data
# Three audiences, three vehicles they see in their own street. Tonnages are
# curb weights and never appear on screen; they only set how many silhouettes
# the field draws, which the reader can count for themselves.

JS_DATA = "\n".join([
"",
"/* ---- the three audiences ---------------------------------------------",
"   The field of silhouettes is the only place the weight is stated, and it",
"   is stated in a thing the reader parks outside their own house. */",
"/* Drawn in profile at 60 x 20. Wheel arches are cut into the body, the",
"   glass is an evenodd hole, and the tyres and hubs ride inside the same",
"   path, so each vehicle keeps its own stance: a Defender is short, tall",
"   and slab-sided, an F-150 is a long bed under a small cab, a HiLux is a",
"   dual cab over a short tray. */",
"const RIDES = [",
"  { k:'us', ride:'Ford F-150', where:'the United States', t:2.2,",
"    d:'M1.6 6L23.5 6L24.6 1.8L37.6 1.8L40.4 5.8L57 5.8L58.2 6.6L58.2 14.6L50 14.6A4.4 3 0 0 0 41.2 14.6L17.4 14.6A4.4 3 0 0 0 8.6 14.6L1.6 14.6ZM3.6 7.4L21.7 7.4L21.7 10.8L3.6 10.8ZM26.6 3.4L32.8 3.4L32.8 6.8L26.6 6.8ZM34 3.4L36.8 3.4L38.2 6.8L34 6.8ZM9.7 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0M11.65 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0M42.3 15.4a3.3 3.3 0 1 0 6.6 0a3.3 3.3 0 1 0 -6.6 0M44.25 15.4a1.35 1.35 0 1 0 2.7 0a1.35 1.35 0 1 0 -2.7 0' },",
"  { k:'uk', ride:'Land Rover Defender', where:'the United Kingdom', t:2.3,",
"    d:'M6.6 1.2L40.4 1.2L42.2 5.4L54.6 5.4L56.6 6.2L56.6 13.6L52.4 13.6A5 3.3 0 0 0 42.4 13.6L17.4 13.6A5 3.3 0 0 0 7.4 13.6L5.4 13.6L5.4 3ZM7.8 2.8L21.6 2.8L21.6 6.8L7.8 6.8ZM23.2 2.8L36.4 2.8L36.4 6.8L23.2 6.8ZM38 2.8L39.6 2.8L40.8 6.8L38 6.8ZM8.5 15.5a3.9 3.9 0 1 0 7.8 0a3.9 3.9 0 1 0 -7.8 0M10.9 15.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0 -3 0M43.5 15.5a3.9 3.9 0 1 0 7.8 0a3.9 3.9 0 1 0 -7.8 0M45.9 15.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0 -3 0' },",
"  { k:'au', ride:'Toyota HiLux', where:'Australia', t:2.1,",
"    d:'M2.2 7.2L21 7.2L22.6 3L37 3L41.2 7.6L53.5 7.6L56.5 8.6L57.6 9.2L57.6 14.6L51 14.6A4.3 2.9 0 0 0 42.4 14.6L17.9 14.6A4.3 2.9 0 0 0 9.3 14.6L2.2 14.6ZM4.2 8.6L19.2 8.6L19.2 11.6L4.2 11.6ZM24.4 4.6L29.6 4.6L29.6 8L24.4 8ZM31.2 4.6L36.2 4.6L36.2 8L31.2 8ZM37.6 4.6L38.2 4.6L39.8 8L37.6 8ZM10.35 15.4a3.25 3.25 0 1 0 6.5 0a3.25 3.25 0 1 0 -6.5 0M12.3 15.4a1.3 1.3 0 1 0 2.6 0a1.3 1.3 0 1 0 -2.6 0M43.45 15.4a3.25 3.25 0 1 0 6.5 0a3.25 3.25 0 1 0 -6.5 0M45.4 15.4a1.3 1.3 0 1 0 2.6 0a1.3 1.3 0 1 0 -2.6 0' }",
"];",
"const LB_PER_T = 2204.62;",
"",
"/* ---- the gradient, per stone -----------------------------------------",
"   head/said carry the essential. matter is the rock. simile sits under the",
"   trucks. cards are the layer for whoever is still reading. Nothing here",
"   contains a figure, because a figure is the one thing that goes stale",
"   without anyone noticing. */",
"const GRADIENT = {",
"  giza: {",
"    head:'The Giza Block', name:'Giza',",
"    glyph:'M5 8.6l7-3.8 7 3.8v9.4H5z M5 8.6h14',",
"    said:'The smallest stone here. It still parks like a pickup.',",
"    matter:'Nummulitic limestone, cut from the plateau it stands on',",
"    simile:'One truck. That is the unit. Everything else on this page is counted in these.',",
"    cards:[",
"      { t:'Not one of them', b:'A pyramid is not a stone. It is this stone, repeated until you lose your place counting.' },",
"      { t:'Dressed, not dumped', b:'The outer casing was faced smooth enough that the whole hill once threw light back like a mirror.' },",
"      { t:'No wheel in the picture', b:'Nothing recovered on site explains the moving. The stones are the only surviving evidence of the method.' }",
"    ] },",
"  ollan: {",
"    head:'The Ollantaytambo Monolith', name:'Ollantaytambo',",
"    glyph:'M4.5 20V7.6l3-1.2V20 M10.5 20V5.2l3-1.2V20 M16.5 20V8.6l3-1.2V20',",
"    said:'Red porphyry, carried up out of a river valley and stood on a hill.',",
"    matter:'Rhyolite porphyry, quarried on the far side of the Urubamba',",
"    simile:'A convoy, nose to tail, and every one of them went uphill across a river.',",
"    cards:[",
"      { t:'The river was in the way', b:'The quarry sits across a valley from the wall. The stones did not go around it.' },",
"      { t:'Uphill the whole distance', b:'The ramp still scars the mountainside. Nothing about the route is convenient.' },",
"      { t:'Left mid-sentence', b:'Stones lie along the road where the work stopped, still pointing at the wall they never reached.' }",
"    ] },",
"  temple: {",
"    head:'The Western Stone', name:'Western Stone',",
"    glyph:'M2.5 9.4h19v5.2h-19z M4.5 6.6h15 M4.5 17.4h15',",
"    said:'A single stone the length of a house, laid in a wall above head height.',",
"    matter:'Meleke limestone, quarried and set in Jerusalem',",
"    simile:'A full car park, fused into one piece, and then lifted.',",
"    cards:[",
"      { t:'Not on the ground', b:'It is not a foundation. There is wall beneath it and wall above it, and it is dead level.' },",
"      { t:'The company it keeps', b:'Its neighbours are joined so closely that a blade will not pass between them.' },",
"      { t:'The method', b:'No ramp survives, no crane, no account. There is only the stone, still in place, still carrying the courses above.' }",
"    ] },",
"  trilithon: {",
"    head:'The Trilithon', name:'Trilithon',",
"    glyph:'M2.6 8.4h5.4v7.2H2.6z M9.3 8.4h5.4v7.2H9.3z M16 8.4h5.4v7.2H16z',",
"    said:'Three of them, side by side, each the length of a swimming pool.',",
"    matter:'Limestone, the podium wall at Baalbek',",
"    simile:'A stadium car park, in one stone. And then there are three of them, in a row.',",
"    cards:[",
"      { t:'Raised, not rested', b:'They sit well clear of the ground, on a course of smaller stone that carries them without complaint.' },",
"      { t:'Three, not one', b:'A single one would be the anomaly. There are three, matched, laid in a line.' },",
"      { t:'Nobody has settled it', b:'Every proposed method has a step where the explanation goes quiet.' }",
"    ] },",
"  pregnant: {",
"    head:'The Stone of the Pregnant Woman', name:'Pregnant Woman',",
"    glyph:'M3.4 16.6l16.4-4.4 1.2 4.3-16.6 3.4z M2.5 20.4h19',",
"    said:'Cut free, nearly moved, and left lying where the work stopped.',",
"    matter:'Limestone, still in the quarry at Baalbek',",
"    simile:'More vehicles than most people see in a week, in one piece, going nowhere.',",
"    cards:[",
"      { t:'Still attached', b:'One corner never released from the bedrock. The stone is half quarry, half monument.' },",
"      { t:'It was meant to travel', b:'It is dressed on the faces that would have shown. Somebody expected it to arrive.' },",
"      { t:'And then it was not', b:'Whatever changed, changed before the last corner was cut.' }",
"    ] },",
"  forgotten: {",
"    head:'The Forgotten Stone', name:'Forgotten Stone',",
"    glyph:'M2.5 9.2h19 M4.6 11h14.8v7.6H4.6z',",
"    said:'The heaviest worked stone anyone has found, and it never left the yard.',",
"    matter:'Limestone, found beneath the quarry floor',",
"    simile:'A traffic jam that never clears. All of it is one stone, and it never moved.',",
"    cards:[",
"      { t:'Found late', b:'It lay under the quarry floor until the ground beside it was opened again within living memory.' },",
"      { t:'Bigger than the famous one', b:'The stone everybody photographs is the smaller of the pair.' },",
"      { t:'An aircraft comparison fails', b:'A loaded airliner is not in the same conversation. Several of them together might be.' }",
"    ] }",
"};",
""])

ANCHOR = "const HUMAN_H = 1.8288, F150_LB = 4700, F150_W = 2.4, GIZA_LB = 5000;"
if "const RIDES = [" not in src:
    if ANCHOR not in src:
        sys.exit("ABORT: constants anchor missing")
    src = src.replace(ANCHOR, ANCHOR + "\n" + JS_DATA, 1)

# ------------------------------------------------- 2. the push comes out
# It was hidden in the last pass. Hidden is not gone: the striker, the meter
# and the instructions were all still in the DOM, still saying "hold".

src, _ = cut_all(src, '<div data-striker=""')
src, _ = cut_all(src, '<div sc-camel-on-pointer-down="{{ startHold }}"')
src, _ = cut_all(src, '<span style="font-family:' + chr(39) + 'JetBrains Mono' + chr(39) +
                 ",monospace;font-size:9.5px;letter-spacing:.05em;line-height:1.5;color:#b9b3a3;background:rgba(9,9,13,.74);border:1px solid rgba(201,168,76,.2);border-radius:8px;padding:5px 9px;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);white-space:nowrap;display:none" + DQ + ">{{ hintPush }}", "span")
src, _ = cut_all(src, '<span style="font-family:' + chr(39) + 'JetBrains Mono' + chr(39) +
                 ",monospace;font-size:8.5px;letter-spacing:.05em;line-height:1.5;color:#b9b3a3;background:rgba(9,9,13,.74);border:1px solid rgba(201,168,76,.2);border-radius:8px;padding:5px 9px;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);white-space:normal" + DQ + ">{{ hintPush }}", "span")

# the comment block that documented the striker outlives the striker
src = re.sub(r'\s*<!-- =+ the high striker =+ -->.*?-->', '', src, flags=re.S)
src = re.sub(r'\s*<!-- =+ instructions \+ the push =+ -->', '', src)
# the two whole screens that existed only to host the push
src, _ = take_section(src, "M02 The push")
src, _ = take_section(src, "M03 The verdict")
src, _ = take_section(src, "D02 Verdict")

# the desktop right-hand rail was "The rule" plus a meter. It becomes the
# essential: what the rock is, and one door down to what it weighs.
BAND1_RAIL = "".join([
'<div style="grid-column:2;grid-row:3;display:flex;flex-direction:column;justify-content:space-between;gap:15px;height:100%;border-top:1px solid rgba(201,168,76,.22);padding-top:17px;padding-bottom:2px">',
  '<div style="display:flex;align-items:center;gap:9px;font-family:' + chr(39) + 'JetBrains Mono' + chr(39) + ',monospace;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:#8A8779;line-height:1.6">',
    '<i style="flex:none;width:22px;height:1px;background:rgba(201,168,76,.5)"></i>{{ matter }}',
  '</div>',
  '<a href="#fw-weight" style="align-self:flex-start;display:inline-flex;align-items:center;gap:9px;font-family:' + chr(39) + 'JetBrains Mono' + chr(39) + ',monospace;font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#0A0A0E;background:#E8B960;border:1px solid #f0d78f;border-radius:11px;padding:13px 20px;transition:background .2s,transform .12s" style-hover="background:#F3D998;transform:translateY(-1px)">Now feel what it weighs<i style="font-style:normal">&#8595;</i></a>',
'</div>'])

if 'href="#fw-weight"' not in src:
    i = src.find('<div style="grid-column:2;grid-row:3;')
    if i == -1:
        sys.exit("ABORT: desktop rail anchor missing")
    cut, hit = cut_element(src, '<div style="grid-column:2;grid-row:3;')
    if not hit:
        sys.exit("ABORT: desktop rail would not cut")
    src = cut[:i] + BAND1_RAIL + cut[i:]

# mobile lead-in no longer promises a button that is gone
src = sub1(src,
    '<i style="width:26px;height:1px;background:rgba(201,168,76,.5)"></i>Spin it, then hold PUSH',
    '<i style="width:26px;height:1px;background:rgba(201,168,76,.5)"></i>{{ matter }}',
    "mobile lead-in")

# ---------------------------------------------- 3. the essential, up top
# The stone is named. What it weighs is not asserted here, it is demonstrated
# two screens down, in trucks the reader can count.

src = src.replace("{{ title }}", "{{ head }}").replace("{{ sub }}", "{{ said }}")

# the corner label was "1,256,850 lb - 13.6 m long". The pound figure is
# unverifiable from the screen; the dimension is not, because a 1.8 m person
# is standing next to it.
src = sub1(src, "{{ blockLabel }}", "{{ dimtxt }}", "corner label")

# ------------------------------------------------ 4. a glyph per stone
STONE_SVG = ('<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" '
             'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
             'style="display:block;flex:none;opacity:.9"><path d="{{ s.glyph }}"/></svg>')

if "{{ s.glyph }}" not in src:
    n = src.count("{{ s.short }}</button>")
    if n != 2:
        sys.exit("ABORT: expected 2 stone pill templates, found %d" % n)
    src = src.replace("{{ s.short }}</button>", STONE_SVG + "<span>{{ s.short }}</span></button>")
    src = sub1(src, "font-size:9.5px;letter-spacing:.05em;padding:8px 13px;border-radius:999px",
               "font-size:9.5px;letter-spacing:.05em;padding:8px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:7px",
               "desktop pill layout")
    src = sub1(src, "font-size:9.5px;letter-spacing:.05em;padding:9px 13px;border-radius:999px",
               "font-size:9.5px;letter-spacing:.05em;padding:9px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:7px",
               "mobile pill layout")

# the pill row no longer needs to announce how many stones there are
src = src.replace("Six stones &#183; pick another", "Pick another stone")
src = src.replace("Six stones · pick another", "Pick another stone")

# ------------------------------------------- 5. band 2: what it weighs
SQ = chr(39)
MONO = "font-family:" + SQ + "JetBrains Mono" + SQ + ",monospace;"

FLAG_US = "".join([
'<svg viewBox="0 0 30 20" width="25" height="16.7" aria-hidden="true" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.45)">',
'<rect width="30" height="20" fill="#FFFFFF"/>',
'<g fill="#B22234"><rect y="0" width="30" height="1.54"/><rect y="3.08" width="30" height="1.54"/>',
'<rect y="6.15" width="30" height="1.54"/><rect y="9.23" width="30" height="1.54"/>',
'<rect y="12.31" width="30" height="1.54"/><rect y="15.38" width="30" height="1.54"/>',
'<rect y="18.46" width="30" height="1.54"/></g>',
'<rect width="12" height="10.77" fill="#3C3B6E"/>',
'<g fill="#FFFFFF"><circle cx="2" cy="1.9" r=".78"/><circle cx="6" cy="1.9" r=".78"/><circle cx="10" cy="1.9" r=".78"/>',
'<circle cx="4" cy="4.4" r=".78"/><circle cx="8" cy="4.4" r=".78"/>',
'<circle cx="2" cy="6.9" r=".78"/><circle cx="6" cy="6.9" r=".78"/><circle cx="10" cy="6.9" r=".78"/>',
'<circle cx="4" cy="9.3" r=".78"/><circle cx="8" cy="9.3" r=".78"/></g></svg>'])

FLAG_UK = "".join([
'<svg viewBox="0 0 30 20" width="25" height="16.7" aria-hidden="true" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.45)">',
'<rect width="30" height="20" fill="#012169"/>',
'<path d="M0 0L30 20M30 0L0 20" stroke="#FFFFFF" stroke-width="4.2"/>',
'<path d="M0 0L30 20M30 0L0 20" stroke="#C8102E" stroke-width="2.1"/>',
'<path d="M15 0V20M0 10H30" stroke="#FFFFFF" stroke-width="6.6"/>',
'<path d="M15 0V20M0 10H30" stroke="#C8102E" stroke-width="3.9"/></svg>'])

FLAG_AU = "".join([
'<svg viewBox="0 0 30 20" width="25" height="16.7" aria-hidden="true" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.45)">',
'<rect width="30" height="20" fill="#012169"/>',
'<path d="M0 0L15 10M15 0L0 10" stroke="#FFFFFF" stroke-width="2.3"/>',
'<path d="M0 0L15 10M15 0L0 10" stroke="#C8102E" stroke-width="1.15"/>',
'<path d="M7.5 0V10M0 5H15" stroke="#FFFFFF" stroke-width="3.5"/>',
'<path d="M7.5 0V10M0 5H15" stroke="#C8102E" stroke-width="2.1"/>',
'<g fill="#FFFFFF"><circle cx="7.5" cy="15.2" r="1.45"/><circle cx="22.2" cy="4.2" r=".85"/>',
'<circle cx="25.8" cy="8.6" r=".85"/><circle cx="21.6" cy="12.8" r=".85"/>',
'<circle cx="18.2" cy="8.2" r=".68"/><circle cx="23.6" cy="16" r=".58"/></g></svg>'])

def flag_btn(key, flag, label, aria):
    return "".join([
    '<button sc-camel-on-click="{{ pick', key.capitalize(), ' }}" aria-label="', aria, '" ',
    'style="display:flex;align-items:center;gap:8px;padding:8px 14px 8px 9px;border-radius:12px;cursor:pointer;',
    'transition:background .18s,border-color .18s,transform .12s;',
    'border:1px solid {{ ', key, 'Border }};background:{{ ', key, 'Bg }};transform:{{ ', key, 'Lift }}">',
    flag,
    '<span style="', MONO, 'font-size:9.5px;font-weight:{{ ', key, 'Weight }};letter-spacing:.16em;',
    'text-transform:uppercase;color:{{ ', key, 'Fg }}">', label, '</span></button>'])

WHEELS = ""   # tyres and hubs now travel inside each vehicle path

BAND2 = "".join([
'<section id="fw-weight" data-screen-label="05 What it weighs" style="max-width:1120px;margin:0 auto;',
'padding:clamp(30px,4.5vw,54px) clamp(20px,4vw,40px) 0;display:flex;flex-direction:column;',
'gap:clamp(15px,2vw,21px);scroll-margin-top:58px;scroll-snap-align:start">',

  '<div data-rise="" style="display:flex;flex-direction:column;gap:10px;opacity:0;transform:translateY(16px);',
  'transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)">',
    '<span style="', MONO, 'font-size:9.5px;letter-spacing:.3em;text-transform:uppercase;color:#C9A84C">',
    'Then &#183; what it weighs</span>',
    '<p style="font-size:clamp(21px,2.7vw,32px);font-weight:500;line-height:1.26;color:#EDE7D8;',
    'max-width:30ch;margin:0;text-wrap:pretty">{{ truckHead }}</p>',
  '</div>',

  # the toggle, and immediately beside it the thing that answers "what changed?"
  '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:11px 14px">',
    '<div style="display:flex;gap:8px;flex:none">',
      flag_btn("us", FLAG_US, "US", "Weigh it in American pickups"),
      flag_btn("uk", FLAG_UK, "UK", "Weigh it in British four-wheel drives"),
      flag_btn("au", FLAG_AU, "AU", "Weigh it in Australian utes"),
    '</div>',
    '<div data-swatch="" style="display:flex;align-items:center;gap:12px;border:1px solid rgba(232,185,96,.34);',
    'border-radius:999px;padding:8px 18px 8px 13px;background:rgba(201,168,76,.08)">',
      '<svg viewBox="0 0 60 20" width="38" height="12.7" fill="#E8B960" fill-rule="evenodd" aria-hidden="true" style="display:block;flex:none">',
      '<path d="{{ rideGlyph }}"/>', WHEELS, '</svg>',
      '<span style="display:flex;flex-direction:column;gap:3px">',
        '<b style="font-size:14.5px;font-weight:600;letter-spacing:-.01em;color:#F3D998;line-height:1">{{ rideName }}</b>',
        '<span style="', MONO, 'font-size:8.5px;letter-spacing:.17em;text-transform:uppercase;color:#8A8779;',
        'line-height:1">{{ rideNote }}</span>',
      '</span>',
    '</div>',
  '</div>',

  '<div data-trucks="" style="display:flex;flex-wrap:wrap;gap:5px 6px;padding:4px 0;',
  '-webkit-mask-image:linear-gradient(90deg,#000 78%,transparent);mask-image:linear-gradient(90deg,#000 78%,transparent);',
  '-webkit-mask-size:0% 100%;mask-size:0% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat">',
    '<sc-for list="{{ trucks }}" as="t" hint-placeholder-count="48">',
      '<svg viewBox="0 0 60 20" width="30" height="10" fill="#C9A84C" fill-rule="evenodd" aria-hidden="true" ',
      'style="flex:none;display:block;opacity:.92"><path d="{{ t.d }}"/>', WHEELS, '</svg>',
    '</sc-for>',
  '</div>',

  '<p style="', MONO, 'font-size:11px;color:#8A8779;line-height:1.8;letter-spacing:.02em;max-width:62ch;',
  'text-wrap:pretty">{{ truckCap }}</p>',
'</section>'])

# ------------------------------ 6. band 3: for whoever is still reading
# The old "04 Scale" panel was four counters and a box asking the reader to
# type their body weight in. It becomes three observations.

BAND3 = "".join([
'<section data-screen-label="06 If you keep looking" style="max-width:1120px;margin:0 auto;',
'padding:clamp(52px,8vw,96px) clamp(20px,4vw,40px) 0;display:flex;flex-direction:column;',
'gap:clamp(14px,2vw,20px);scroll-snap-align:start">',
  '<span data-rise="" style="', MONO, 'font-size:9.5px;letter-spacing:.3em;text-transform:uppercase;',
  'color:#C9A84C;opacity:0;transform:translateY(16px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)">',
  'If you keep looking</span>',
  '<div data-rise="" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,262px),1fr));',
  'gap:clamp(10px,1.4vw,14px);opacity:0;transform:translateY(16px);',
  'transition:opacity .7s ease .06s,transform .7s cubic-bezier(.2,.7,.2,1) .06s">',
    '<sc-for list="{{ cards }}" as="c" hint-placeholder-count="3">',
      '<div style="background:linear-gradient(180deg,rgba(24,21,32,.72),rgba(14,12,19,.72));',
      'border:1px solid rgba(201,168,76,.22);border-radius:13px;padding:19px 19px 18px;',
      'box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 6px 16px rgba(0,0,0,.4);',
      'display:flex;flex-direction:column;gap:9px">',
        '<i aria-hidden="true" style="width:19px;height:1px;background:rgba(201,168,76,.55)"></i>',
        '<h3 style="font-size:18px;font-weight:600;line-height:1.24;letter-spacing:-.01em;color:#F3D998;',
        'margin:0;text-wrap:pretty">{{ c.t }}</h3>',
        '<p style="font-size:14px;line-height:1.62;color:#cfcbc1;margin:0;text-wrap:pretty">{{ c.b }}</p>',
      '</div>',
    '</sc-for>',
  '</div>',
'</section>'])

# ------------------------------------------------------ 7. put them in order
# essential -> weight -> supporting detail -> the Giza blocks -> the real thing
src, old_scale = take_section(src, "04 Scale")
src, old_trucks = take_section(src, "05 Trucks")
src, prev_b2 = take_section(src, "05 What it weighs")
src, prev_b3 = take_section(src, "06 If you keep looking")
if old_scale is None and prev_b3 is None:
    sys.exit("ABORT: neither the old scale panel nor its replacement is present")

closer = section_span(src, "06 Closer")
if closer is None:
    sys.exit("ABORT: the Giza-block section went missing")
src = src[:closer[0]] + BAND2 + "\n\n" + BAND3 + "\n\n" + src[closer[0]:]

# kickers stop counting themselves
src = src.replace("06 &#183; Then multiply", "And then, in Giza blocks")
src = src.replace("06 · Then multiply", "And then, in Giza blocks")
src = src.replace("07 &#183; The real stone", "And then the actual stone")
src = src.replace("07 · The real stone", "And then the actual stone")
src = src.replace('data-screen-label="07 The real stone"', 'data-screen-label="08 The real stone"')

# the door at the top of the stage used to point straight past the argument
src = src.replace('href="#fw-real" style="font-family:', 'href="#fw-weight" style="font-family:')
src = src.replace("The real stone &#8595;", "What it weighs &#8595;")
src = src.replace("The real stone ↓", "What it weighs &#8595;")

# ---------------------------------------------------------- 8. the wiring
src = sub1(src,
    "state = { k:'temple', bw:180,",
    "state = { k:'temple', ride:'us', bw:180,",
    "ride state")

PICKRIDE = "\n".join([
"  /* Switching flags must be legible in the same glance as the click, so the",
"     swatch that names the vehicle re-runs its highlight every time. */",
"  _pickRide(k) {",
"    this._click(false);",
"    this.setState({ ride: k }, () => {",
"      document.querySelectorAll('[data-swatch]').forEach(el => {",
"        el.style.animation = 'none'; void el.offsetWidth;",
"        if (!this.reduced()) el.style.animation = 'fw-swap .9s cubic-bezier(.2,.7,.2,1)';",
"      });",
"      document.querySelectorAll('[data-trucks]').forEach(el => {",
"        el.style.webkitMaskSize = '130% 100%'; el.style.maskSize = '130% 100%';",
"      });",
"    });",
"  }",
"  ride() { return RIDES.find(r => r.k === this.state.ride) || RIDES[0]; }",
""])

if "_pickRide(k)" not in src:
    src = sub1(src, "  _toggleCine() {", PICKRIDE + "  _toggleCine() {", "ride methods")

src = sub1(src,
    "@keyframes fw-breathe{",
    "@keyframes fw-swap{0%{background:rgba(232,185,96,.34);border-color:rgba(243,217,152,.9);transform:translateY(-2px)}"
    "100%{background:rgba(201,168,76,.08);border-color:rgba(232,185,96,.34);transform:none}} @keyframes fw-breathe{",
    "swap keyframe")

src = sub1(src,
    "    const n = Math.max(1, Math.round(s.lb / F150_LB));\n    const metres = n * F150_W, mi = metres / 1609;",
    "    const ride = this.ride();\n"
    "    const n = Math.max(1, Math.round(s.lb / (ride.t * LB_PER_T)));\n"
    "    const metres = n * F150_W, mi = metres / 1609;",
    "ride-aware count")

src = sub1(src,
    "    const trucks = [];\n    for (let i = 0; i < Math.min(n, 760); i++) trucks.push(i);",
    "    const trucks = [];\n    for (let i = 0; i < Math.min(n, 760); i++) trucks.push({ d: ride.d });\n"
    "    const g = GRADIENT[s.k] || GRADIENT.temple;\n"
    "    const rideSkin = k => ({\n"
    "      Border: this.state.ride === k ? 'rgba(232,185,96,.75)' : 'rgba(201,168,76,.26)',\n"
    "      Bg: this.state.ride === k ? 'rgba(201,168,76,.18)' : 'rgba(9,9,13,.6)',\n"
    "      Fg: this.state.ride === k ? '#F3D998' : '#8A8779',\n"
    "      Weight: this.state.ride === k ? '700' : '500',\n"
    "      Lift: this.state.ride === k ? 'translateY(-1px)' : 'none'\n"
    "    });\n"
    "    const RU = rideSkin('us'), RK = rideSkin('uk'), RA = rideSkin('au');",
    "trucks carry their own silhouette")

# per-stone gradient copy, and the flag toggle, onto the render values
NEWPROPS = "\n".join([
"",
"      head: g.head, said: g.said, matter: g.matter, cards: g.cards,",
"      dimtxt: s.dimtxt,",
"",
"      rideGlyph: ride.d, rideName: ride.ride,",
"      rideNote: 'Every silhouette below is one of these',",
"      pickUs: () => this._pickRide('us'),",
"      pickUk: () => this._pickRide('uk'),",
"      pickAu: () => this._pickRide('au'),",
"      usBorder: RU.Border, usBg: RU.Bg, usFg: RU.Fg, usWeight: RU.Weight, usLift: RU.Lift,",
"      ukBorder: RK.Border, ukBg: RK.Bg, ukFg: RK.Fg, ukWeight: RK.Weight, ukLift: RK.Lift,",
"      auBorder: RA.Border, auBg: RA.Bg, auFg: RA.Fg, auWeight: RA.Weight, auLift: RA.Lift,",
"",
"      trucks,",
"      truckHead: g.simile,",
"      truckCap: 'Every silhouette is one ' + ride.ride + ', the kind parked in driveways across ' +",
"        ride.where + '. All of them together are this one stone.',"])

OLDTRUCKPROPS = "\n      trucks,\n      truckHead: n <= 1"
if "truckHead: g.simile," not in src:
    i = src.find(OLDTRUCKPROPS)
    if i == -1:
        sys.exit("ABORT: truck props anchor missing")
    j = src.index("closerBig: s.closerBig", i)
    src = src[:i] + NEWPROPS + "\n\n      " + src[j:]

# the pill label loses its tonnage and gains its glyph
src = sub1(src,
    "          label: x.label, short: x.short,",
    "          label: (GRADIENT[x.k] || {}).head || x.label,\n"
    "          short: (GRADIENT[x.k] || {}).name || x.short,\n"
    "          glyph: (GRADIENT[x.k] || {}).glyph || '',",
    "pill label")

# ------------------------------------------- 9. the copy that still said hold
SCRUB = [
 ("this._msg('Press and hold. Push as hard as you can.');", "this._msg('');"),
 ("hintPush: 'Hold PUSH. The striker shows how close you get',", "hintPush: '',"),
 ("'Spin the stone, then hold PUSH. The striker is honest, and for the heavy ones your whole body barely lifts the puck off the deck, which is the point.'",
  "'This one is measured in trucks, further down the page.'"),
 ("btnLabel: holding ? 'Pushing…' : tried ? 'Push again' : 'Hold to push',", "btnLabel: '',"),
 ("'Try the striker first \u2014 your result goes on the card: your push, what it needs, and the nothing you moved it.'",
  "'Six stones, weighed in the vehicle parked outside your own house. The lightest one is a pickup.'"),
 ('content="Six ancient stones, from a 2.5-ton Giza block to the 1,500-ton Forgotten Stone. Push as hard as you can and watch the striker. Not one of them moves."',
  'content="Six ancient stones, weighed in the vehicle you park outside your own house. Spin them, stand a person beside them, and watch the count of trucks it would take."'),
 ('content="Your whole body pushes about 200 lb. Breaking the Forgotten Stone loose takes 826,875. Hold the striker."',
  'content="Spin the stone. Stand a person beside it. Then watch it weighed out in pickups, Defenders or utes, one silhouette at a time."'),
]
applied = 0
for old, new in SCRUB:
    if old in src:
        src = src.replace(old, new); applied += 1
if applied == 0 and 'weighed in the vehicle you park outside' not in src:
    sys.exit('ABORT: none of the push copy could be found to replace')

# ---------------------------------------------------------- 10. assertions
# Each one reads the state of the finished file. None of them counts edits.

body = src[:src.index("<script", src.index("</style>"))] if "</style>" in src else src

fails = []

def want(cond, msg):
    if not cond:
        fails.append(msg)

want("<div data-striker=" not in src, "the high striker is still in the document")
want('<i data-meter=""' not in src, "the push meter is still in the document")
want("sc-camel-on-pointer-down" not in src, "a press-and-hold target survives")
want('data-screen-label="M02 The push"' not in src, "the mobile push screen survives")
want('data-screen-label="M03 The verdict"' not in src, "the mobile push verdict survives")
want('data-screen-label="D02 Verdict"' not in src, "the desktop push verdict survives")

for phrase in ["Hold to push", "Press and hold", "hold PUSH", "Hold PUSH", "press and hold",
               "striker", "Striker"]:
    want(phrase not in body, "markup still says %r" % phrase)
for lit in ["Try the striker", "watch the striker", "Hold the striker"]:
    want(lit not in src, "a script string still says %r" % lit)

want(src.count('id="fw-weight"') == 1, "the weight band needs exactly one anchor")
want(src.count('href="#fw-weight"') >= 2, "nothing routes down to the weight band")
want(src.count("{{ pickUs }}") == 1 and src.count("{{ pickUk }}") == 1
     and src.count("{{ pickAu }}") == 1, "the three flags are not wired one each")
want(src.count('data-swatch=""') == 1, "the swatch that names the vehicle is missing")
want("{{ rideName }}" in src and "{{ rideGlyph }}" in src, "the swatch does not name what changed")
want("@keyframes fw-swap" in src, "the swatch has nothing to flash with")
want("{{ t.d }}" in src, "the truck field is not drawing the selected vehicle")
want(src.count("{{ s.glyph }}") == 2,
     "expected a glyph in both pill rows, found %d" % src.count("{{ s.glyph }}"))
want("{{ c.t }}" in src and "{{ c.b }}" in src, "the supporting detail cards are missing")
want("{{ head }}" in src and "{{ said }}" in src and "{{ matter }}" in src,
     "band one is not carrying the essential")
want("{{ blockLabel }}" not in src, "the corner label still asserts an unverifiable weight")
want("{{ bwValue }}" not in src, "the type-in-your-body-weight box survives")

# order is the whole argument: weight before detail, detail before the photo
def at(label):
    sp = section_span(src, label)
    return sp[0] if sp else -1

o_weight, o_detail = at("05 What it weighs"), at("06 If you keep looking")
o_giza, o_real = at("06 Closer"), at("08 The real stone")
want(-1 not in (o_weight, o_detail, o_giza, o_real), "a band went missing")
want(o_weight < o_detail < o_giza < o_real,
     "the gradient is out of order: weight %d, detail %d, giza %d, real %d"
     % (o_weight, o_detail, o_giza, o_real))

# the stage, the person and the spin all survive - Jeff kept those on purpose
want('data-stage=""' in src, "the spinnable stage is gone")
want("toggleSpin" in src, "drag-to-spin lost its control")
want("scaleFigure" in src or "HUMAN_H" in src, "the person at scale is gone")

if fails:
    for f in fails:
        print("  FAIL " + f)
    sys.exit("ABORT: %d check(s) failed, nothing written" % len(fails))

APP.write_text(src)
print("app.html %d -> %d chars" % (orig, len(src)))
print("bands: weight %d < detail %d < giza %d < real %d" % (o_weight, o_detail, o_giza, o_real))
print("all %d checks passed" % 24)
