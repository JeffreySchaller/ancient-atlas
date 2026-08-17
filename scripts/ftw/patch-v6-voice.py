#!/usr/bin/env python3
# Feel the Weight: the v6 voice and composition.
#
# Runs AFTER patch-gradient.py, on the same app.html.
#
# Three things change, and they are the three Jeff reacted to:
#
#   1. The headline stops naming the stone and starts saying what it is like.
#      "Longer than a bus, and lifted into a wall." One word of it is italic
#      and champagne, which is the only decoration on the page.
#   2. Band one stacks. The stage runs full width, the sentence sits under it.
#      A 13.6 m stone wants a wide frame, not a column beside a column.
#   3. The simile that lands the weight moves BELOW the field of trucks.
#      You see the wall of vehicles first, then you are told what it means.
#
# Idempotent. Assertions read the finished file.

import re, sys
from pathlib import Path

APP = Path(__file__).resolve().parent / "app.html"
src = APP.read_text()
orig = len(src)

SQ = chr(39)
MONO = "font-family:" + SQ + "JetBrains Mono" + SQ + ",monospace;"

if "const GRADIENT = {" not in src:
    sys.exit("ABORT: run patch-gradient.py first")

def cut_element(s, start_marker, tag="div"):
    i = s.find(start_marker)
    if i == -1:
        return s, None
    open_re = re.compile("<" + tag + r"\b")
    close = "</" + tag + ">"
    depth, j = 0, i
    while True:
        m_open = open_re.search(s, j)
        m_close = s.find(close, j)
        if m_close == -1:
            sys.exit("ABORT: unbalanced <%s>" % tag)
        if m_open and m_open.start() < m_close:
            depth += 1; j = m_open.end(); continue
        depth -= 1; j = m_close + len(close)
        if depth == 0:
            return s[:i] + s[j:], s[i:j]

# ------------------------------------------------------- 1. the v6 copy
def L(js): return js          # these lines are JS, not python source

GRAD = "\n".join([
L("/* The headline is split in three because the middle word is set in italic"),
L("   champagne, and the templating layer escapes markup. Same trick as the"),
L("   Giza-block line further down the page, which already worked. */"),
L("const GRADIENT = {"),
L("  giza: {"),
L("    name:'Giza block',"),
L("    glyph:'M4 8 L12 4 L20 8 L20 17 L12 21 L4 17 Z M4 8 L12 12 L20 8 M12 12 L12 21',"),
L("    h1:'One block. And then ', h2:'two million', h3:' more.',"),
L("    said:'The average stone in the Great Pyramid. Nothing unusual about this one, which is the unsettling part.',"),
L("    matter:'Local limestone',"),
L("    v1:'About what you could park ', v2:'on your driveway', v3:'.',"),
L("    cards:["),
L("      { t:'The pile', b:'Stacked one on another, this block and its two million siblings reach higher than any building would for the next four thousand years.' },"),
L("      { t:'The fit', b:'The casing stones at the top were set close enough that a blade will not pass between them.' },"),
L("      { t:'The catch', b:'Nothing about a single block is impressive. Everything about two million of them is.' }"),
L("    ] },"),
L("  ollan: {"),
L("    name:'Ollantaytambo',"),
L("    glyph:'M3 20 L3 14 L9 14 L9 9 L15 9 L15 5 L21 5 M3 20 L21 20 L21 5',"),
L("    h1:'Carried up a ', h2:'mountain', h3:'.',"),
L("    said:'Quarried across a river and a valley, then brought uphill to a terrace nobody has explained.',"),
L("    matter:'Rhyolite, from the far side of a valley',"),
L("    v1:'A row of them nose to tail, ', v2:'the length of a street', v3:'.',"),
L("    cards:["),
L("      { t:'The route', b:'The quarry is on the opposite mountainside. Whatever moved these went down, across a river, and then up.' },"),
L("      { t:'The strays', b:'Some never arrived. They are still lying on the slope, dressed and abandoned, which is how the route is known at all.' },"),
L("      { t:'The joint', b:'Where they did arrive, the faces meet without mortar and have held through earthquakes that flattened the colonial town below.' }"),
L("    ] },"),
L("  temple: {"),
L("    name:'The Western Stone',"),
L("    glyph:'M2.5 9 H21.5 V15 H2.5 Z M8 9 V15 M15 9 V15',"),
L("    h1:'Longer than a ', h2:'bus', h3:', and lifted into a wall.',"),
L("    said:'The largest cut stone in the Temple Mount. It sits in a course above ground level, and today you can only see it underground.',"),
L("    matter:'Meleke limestone',"),
L("    v1:'Enough to fill ', v2:'a supermarket car park', v3:', twice over.',"),
L("    cards:["),
L("      { t:'Not on the ground', b:'This is the part people miss. It was not dragged into place and left. It was raised, and set into a course with stones above it.' },"),
L("      { t:'The company it keeps', b:'It is not alone. The same course carries several others of comparable size, cut to sit against it.' },"),
L("      { t:'The method', b:'No proposed technique for placing it has been demonstrated at this scale. That is not a mystery claim, it is the state of the literature.' }"),
L("    ] },"),
L("  trilithon: {"),
L("    name:'The Trilithon',"),
L("    glyph:'M3 21 V7 H7 V21 M10 21 V7 H14 V21 M17 21 V7 H21 V21 M2 5.5 H22',"),
L("    h1:'Three of these, ', h2:'side by side', h3:', twenty feet up.',"),
L("    said:'Baalbek. Not laid on the ground but raised into a wall, fitted so closely the joints still hold.',"),
L("    matter:'Limestone, from a quarry under the modern town',"),
L("    v1:'A queue that would ', v2:'run out of the town', v3:'.',"),
L("    cards:["),
L("      { t:'Three, not one', b:'The Trilithon is a set. Three stones of this size, in the same course, touching.' },"),
L("      { t:'The height', b:'They are not at ground level. They sit on a foundation course already several metres high.' },"),
L("      { t:'Downhill, at least', b:'The quarry is uphill of the site, which is the one mercy in the whole arrangement.' }"),
L("    ] },"),
L("  pregnant: {"),
L("    name:'Stone of the Pregnant Woman',"),
L("    glyph:'M2.5 18 L14 8.5 L21.5 12.5 L10 21.5 Z M2.5 18 L2.5 15 L14 5.5 L21.5 9.5 L21.5 12.5',"),
L("    h1:'Still lying where it was ', h2:'cut', h3:'.',"),
L("    said:'Dressed on every face and left in the quarry at an angle, as though the job stopped mid-sentence.',"),
L("    matter:'Limestone, still attached at one corner',"),
L("    v1:'More than ', v2:'everyone on your street owns', v3:', combined.',"),
L("    cards:["),
L("      { t:'Finished, and abandoned', b:'It is not a rough blank. The faces are dressed. Somebody completed the hard part and then walked away.' },"),
L("      { t:'The angle', b:'It lies tilted because one corner was never separated from the bedrock. You can put your hand on the join.' },"),
L("      { t:'The neighbours', b:'A second, heavier stone was found beside it in the same quarry, which suggests this one was not the ambition, only the survivor.' }"),
L("    ] },"),
L("  forgotten: {"),
L("    name:'The Forgotten Stone',"),
L("    glyph:'M2 14 L12 8 L22 14 M2 14 V19 H22 V14 M2 19 H22',"),
L("    h1:'Nobody has ever ', h2:'moved', h3:' this one.',"),
L("    said:'The heaviest worked stone we know of. It is still in the ground, and it has never been anywhere else.',"),
L("    matter:'Limestone, partly still buried',"),
L("    v1:'It will not ', v2:'fit on your screen', v3:'.',"),
L("    cards:["),
L("      { t:'Found late', b:'It was uncovered in the same quarry in the 1990s, under the one everybody already knew about.' },"),
L("      { t:'Still down there', b:'Only the top is exposed. The dimensions come from where the cut faces run into the ground.' },"),
L("      { t:'The question it asks', b:'Somebody cut this deliberately, to size, for a purpose. The interesting question is not how they would have moved it. It is what they thought they were going to do with it.' }"),
L("    ] }"),
L("};"),
])

i = src.index("const GRADIENT = {")
j = src.index("\n};", i) + len("\n};")
src = src[:i] + GRAD + src[j:]

# ------------------------------------------- 2. band one stacks and widens
# A 13.6 m stone wants a wide frame. The sentence goes underneath it, where a
# caption goes, and the pills go under that.

if 'data-screen-label="D01 Specimen"' in src and "class=\"v6-say\"" not in src:
    i = src.index('data-screen-label="D01 Specimen"')
    a = src.rindex("<section", 0, i)
    b = src.index("</section>", i) + len("</section>")
    old_d01 = src[a:b]

    rest, stage = cut_element(old_d01, '<div data-quake=""')
    if stage is None:
        sys.exit("ABORT: the stage block could not be lifted out of band one")

    # full width, and a touch shorter so the trucks are one clean scroll away
    stage = stage.replace(
        'style="grid-column:1;grid-row:1 / span 3;align-self:stretch;position:relative;width:100%;'
        'min-height:min(56vh,440px);',
        'style="position:relative;width:100%;height:clamp(300px,42vh,420px);', 1)
    if "grid-column:1" in stage:
        sys.exit("ABORT: the stage kept its grid placement")

    # the top-right door and the bottom-left instruction chip both go; v6 puts
    # two quiet labels in the corners instead
    stage, _door = cut_element(stage, '<a href="#fw-weight"', "a")
    stage = stage.replace(
        'background:rgba(9,9,13,.74);border:1px solid rgba(201,168,76,.2);border-radius:8px;'
        'padding:5px 9px;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);white-space:nowrap"'
        '>{{ hintSpin }}',
        'color:#6f6b60;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap">Drag to turn it')
    stage = stage.replace(
        '<div style="position:absolute;top:13px;left:16px;right:16px;display:flex;flex-wrap:wrap;'
        'align-items:baseline;justify-content:space-between;gap:6px 14px;pointer-events:none">',
        '<span style="position:absolute;right:16px;bottom:18px;' + MONO + 'font-size:9.5px;'
        'letter-spacing:.16em;text-transform:uppercase;color:#6f6b60;pointer-events:none">'
        'Figure at six feet</span>'
        '<div style="position:absolute;top:13px;left:16px;right:16px;display:flex;flex-wrap:wrap;'
        'align-items:baseline;justify-content:space-between;gap:6px 14px;pointer-events:none">')

    PILL = "".join([
    '<button sc-camel-on-click="{{ s.pick }}" class="{{ s.cls }}" style="', MONO,
    'font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;padding:9px 15px 9px 11px;',
    'border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:9px;',
    'transition:background .15s,color .15s,border-color .15s,transform .15s;',
    'border:1px solid {{ s.border }};background:{{ s.bg }};color:{{ s.fg }};font-weight:{{ s.weight }};',
    'transform:{{ s.lift }}" style-hover="border-color:rgba(232,185,96,.6);color:#F3D998">',
    '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" ',
    'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ',
    'style="display:block;flex:none;opacity:.85"><path d="{{ s.glyph }}"/></svg>',
    '<span>{{ s.short }}</span></button>'])

    D01 = "".join([
    '<section data-screen-label="D01 Specimen" style="max-width:1180px;margin:0 auto;',
    'padding:calc(47px + clamp(12px,2.4vh,30px)) clamp(20px,4vw,40px) 0;',
    'display:flex;flex-direction:column;gap:clamp(18px,2.6vw,30px)">',
      stage,
      '<div class="v6-say" style="display:flex;flex-direction:column">',
        '<h1 style="font-size:clamp(29px,4.2vw,52px);font-weight:600;line-height:1.02;',
        'letter-spacing:-.022em;color:#F0EEE9;margin:0;max-width:24ch;text-wrap:pretty">',
        '{{ headLead }}<em style="font-style:italic;color:#C9A84C">{{ headEm }}</em>{{ headTail }}</h1>',
        '<p style="font-size:clamp(15.5px,1.5vw,19px);line-height:1.5;color:#C5C5D0;',
        'max-width:46ch;margin:15px 0 0;text-wrap:pretty">{{ said }}</p>',
        '<p style="', MONO, 'font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;',
        'color:#C9A84C;margin:17px 0 0">{{ matter }}</p>',
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:clamp(18px,2.4vw,26px)">',
          '<sc-for list="{{ stones }}" as="s" hint-placeholder-count="6">', PILL, '</sc-for>',
        '</div>',
      '</div>',
    '</section>'])

    src = src[:a] + D01 + src[b:]

# --------------------------------- 2b. the phone gets the same sentence
# Same split headline, same serif deck, same quiet corner label. The phone
# has no room for a chip that repeats what a finger already knows.
src = src.replace(
    '>{{ head }}</h1>',
    '>{{ headLead }}<em style="font-style:italic;color:#C9A84C">{{ headEm }}</em>{{ headTail }}</h1>')
src = src.replace(
    '<p style="' + MONO + 'font-size:13.5px;line-height:1.7;color:#9a9689;letter-spacing:.02em;'
    'text-wrap:pretty">{{ said }}</p>',
    '<p style="font-size:16px;line-height:1.5;color:#C5C5D0;text-wrap:pretty">{{ said }}</p>')
src = src.replace(
    'background:rgba(9,9,13,.74);border:1px solid rgba(201,168,76,.2);border-radius:8px;'
    'padding:5px 9px;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);'
    'white-space:normal">{{ hintSpin }}',
    'color:#6f6b60;letter-spacing:.16em;text-transform:uppercase;white-space:normal">Drag to turn it')

# ---------------------------------- 3. the simile lands after the trucks
# Seeing the wall of vehicles and then being told what it means is a better
# order than being told and then shown.
OLD_HEAD = ('<p style="font-size:clamp(21px,2.7vw,32px);font-weight:500;line-height:1.26;'
            'color:#EDE7D8;max-width:30ch;margin:0;text-wrap:pretty">{{ truckHead }}</p>')
if OLD_HEAD in src:
    src = src.replace(OLD_HEAD, "")

VERDICT = "".join([
'<p style="font-size:clamp(19px,2.4vw,30px);font-weight:500;line-height:1.24;color:#F0EEE9;',
'max-width:30ch;margin:clamp(14px,1.8vw,20px) 0 0;text-wrap:pretty">',
'{{ verdictLead }}<b style="color:#E8B960;font-weight:600">{{ verdictEm }}</b>{{ verdictTail }}</p>'])

CAP = ('<p style="' + MONO + 'font-size:11px;color:#8A8779;line-height:1.8;letter-spacing:.02em;'
       'max-width:62ch;text-wrap:pretty">{{ truckCap }}</p>')
if "{{ verdictLead }}" not in src:
    if CAP not in src:
        sys.exit("ABORT: the truck caption moved, cannot place the verdict")
    src = src.replace(CAP, VERDICT + CAP, 1)

# ------------------------------------------- 3b. a wide stage needs more room
# The framing pad was tuned for a stage roughly as tall as it is wide. Run the
# same subject through a 3.5:1 frame and the camera sits close enough that the
# far end of a 13.6 m stone falls off the left edge, because the target is
# offset right to make room for the figure. Pad harder as the frame widens.
OLD_FIT = ("this.camDist = Math.max((subjH / 2) / t, (W / 2) / (t * this.camera.aspect)) * 1.2;")
NEW_FIT = ("const need = Math.max((subjH / 2) / t, (W / 2) / (t * this.camera.aspect));\n"
           "    this.camDist = need * (this.camera.aspect > 2.2 ? 1.46 : 1.2);")
if OLD_FIT in src:
    src = src.replace(OLD_FIT, NEW_FIT)
elif "this.camera.aspect > 2.2 ? 1.46" not in src:
    sys.exit("ABORT: the framing pad moved")

# the two corner labels sit over a lit stone, so they need the same shadow the
# other stage type already carries
src = src.replace("color:#6f6b60;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap\">Drag to turn it",
  "color:#8d8879;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap;"
  "text-shadow:0 0 10px rgba(10,10,14,.98),0 0 22px rgba(10,10,14,.9)\">Drag to turn it")
src = src.replace("color:#6f6b60;letter-spacing:.16em;text-transform:uppercase;white-space:normal\">Drag to turn it",
  "color:#8d8879;letter-spacing:.16em;text-transform:uppercase;white-space:normal;"
  "text-shadow:0 0 10px rgba(10,10,14,.98),0 0 22px rgba(10,10,14,.9)\">Drag to turn it")
src = src.replace("text-transform:uppercase;color:#6f6b60;pointer-events:none\">Figure at six feet",
  "text-transform:uppercase;color:#8d8879;pointer-events:none;"
  "text-shadow:0 0 10px rgba(10,10,14,.98),0 0 22px rgba(10,10,14,.9)\">Figure at six feet")

# --------------------------------------------------------- 4. the wiring
src = src.replace(
    "      head: g.head, said: g.said, matter: g.matter, cards: g.cards,",
    "      headLead: g.h1, headEm: g.h2, headTail: g.h3,\n"
    "      said: g.said, matter: g.matter, cards: g.cards,")

src = src.replace("      truckHead: g.simile,",
                  "      verdictLead: g.v1, verdictEm: g.v2, verdictTail: g.v3,")

src = src.replace("          label: (GRADIENT[x.k] || {}).head || x.label,",
                  "          label: (GRADIENT[x.k] || {}).name || x.label,")

# the kicker over band one named a gesture that is no longer the point
src = src.replace(">Put your hands on it<", ">The stone<")

# ---------------------------------------------------------- 5. assertions
fails = []
def want(cond, msg):
    if not cond: fails.append(msg)

want("{{ headLead }}" in src and "{{ headEm }}" in src and "{{ headTail }}" in src,
     "the headline is not split for its italic word")
want("{{ head }}" not in src, "the old name-the-stone headline survives")
want("{{ truckHead }}" not in src, "the simile is still being asked for above the trucks")
want("{{ verdictLead }}" in src and "{{ verdictEm }}" in src,
     "the simile did not land below the trucks")
want(src.count('class="v6-say"') == 1, "band one did not restack")
want("grid-column:1;grid-row:1 / span 3" not in src, "the stage kept its column")
want('href="#fw-weight"' not in src, "a door survives that v6 does not have")
want("Figure at six feet" in src, "the scale label is missing from the stage")
want("this.camera.aspect > 2.2 ? 1.46" in src, "the wide stage will crop the stone")
want(src.count("text-shadow:0 0 10px rgba(10,10,14,.98)") == 3,
     "a stage corner label is unreadable over the stone")
want("Drag to turn it" in src, "the turn instruction is missing from the stage")
want("{{ hintSpin }}" not in src, "the old instruction chip survives")
want("h2:'bus'" in src, "the v6 copy did not land")
want(src.count("{{ s.glyph }}") == 2, "a pill row lost its glyph")
want("Six stones &#183; pick another" not in src and "Six stones \u00b7 pick another" not in src,
     "the pill row still counts itself")

# the field of trucks, the spin, the person and the photograph all survive
for keep in ['data-trucks=""', 'data-swatch=""', 'data-stage=""', "toggleSpin",
             "{{ t.d }}", "{{ c.t }}", "data-photo=\"\""]:
    want(keep in src, "%s went missing" % keep)

# order is still the argument
def at(label):
    k = src.find('data-screen-label="%s"' % label)
    return -1 if k == -1 else src.rindex("<section", 0, k)
o = [at(x) for x in ["D01 Specimen", "05 What it weighs", "06 If you keep looking",
                     "06 Closer", "08 The real stone"]]
want(-1 not in o, "a band went missing")
want(o == sorted(o), "the gradient is out of order: %r" % o)

if fails:
    for f in fails:
        print("  FAIL " + f)
    sys.exit("ABORT: %d check(s) failed, nothing written" % len(fails))

APP.write_text(src)
print("app.html %d -> %d chars" % (orig, len(src)))
print("band one stacked, headline split, verdict moved below the field")
