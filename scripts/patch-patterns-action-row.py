#!/usr/bin/env python3
"""Give the verb its own row.

Measuring caught what reading would not: at a 264px card the metrics and the
verb do not fit on one line, so "23 SITES · 10 COUNTRIES" wrapped and left the
word COUNTRIES stranded under a right-aligned arrow. Ragged, and it made the one
line that states the job the hardest line to read.

So the verb becomes a full-width action row under a hairline, with the arrow
pushed to the far edge. It now looks like the bottom of a button rather than a
caption, which is the correct signal: this whole card is a door.

Idempotent: running twice is a no-op.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-patterns.py"

src = BUILDER.read_text()
orig = src

M_OLD = ("""            f'<p class="pfoot"><span class="pm">{len(carriers)} sites · {len(cs)} countries</span>'
            f'<span class="pgo">{go}</span></p>'""")
M_NEW = ("""            f'<p class="pm">{len(carriers)} sites · {len(cs)} countries</p>'
            f'<p class="pgo">{go}</p>'""")
if M_NEW not in src:
    if M_OLD not in src:
        sys.exit("ABORT: the card footer markup is not what this patch expects")
    src = src.replace(M_OLD, M_NEW)

# the verb carries the arrow to the far edge itself now
G_OLD = 'go = (f\'Watch {nvid} studies <i>→</i>\' if nvid else "Not yet written")'
G_NEW = ('go = (f\'<span>Watch {nvid} studies</span><i>→</i>\' if nvid\n'
         '              else \'<span>Not yet written</span>\')')
if G_NEW not in src:
    if G_OLD not in src:
        sys.exit("ABORT: the verb builder is not what this patch expects")
    src = src.replace(G_OLD, G_NEW)

C_OLD = """.pfoot{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:0}}
.pm{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);margin:0}}
.pgo{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
color:var(--champagne);white-space:nowrap}}
.pgo i{{font-style:normal;display:inline-block;transition:transform .16s}}
.pcard:hover .pgo{{color:var(--amber)}}
.pcard:hover .pgo i{{transform:translateX(3px)}}"""
C_NEW = """.pm{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);margin:0 0 8px}}
/* A full-width row under a hairline reads as the bottom of a button. Side by
   side with the counts it did not fit at 264px and wrapped, which buried the
   one line on the card that states the job. */
.pgo{{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0;
border-top:1px solid var(--stone);padding-top:9px;
font-family:var(--font-mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
color:var(--champagne);transition:border-color .18s,color .18s}}
.pgo i{{font-style:normal;display:inline-block;transition:transform .16s}}
.pcard:hover .pgo{{color:var(--amber);border-top-color:rgba(201,168,76,.32)}}
.pcard:hover .pgo i{{transform:translateX(3px)}}"""
if ".pgo{{display:flex" not in src:
    if C_OLD not in src:
        sys.exit("ABORT: the footer CSS is not what this patch expects")
    src = src.replace(C_OLD, C_NEW)

# claw back the row's extra height so 1280x720 keeps all seven in view
for old, new in (
        ("border-radius:12px;padding:14px 15px 12px;background:var(--charcoal);transition:.18s}}",
         "border-radius:12px;padding:13px 15px 11px;background:var(--charcoal);transition:.18s}}"),
        (".pb{{font-size:12.5px;line-height:1.45;color:var(--cloud);margin:0 0 10px;",
         ".pb{{font-size:12.5px;line-height:1.45;color:var(--cloud);margin:0 0 9px;")):
    if new in src:
        continue
    if old not in src:
        sys.exit(f"ABORT: anchor drifted: {old[:50]!r}")
    src = src.replace(old, new)

if src != orig:
    BUILDER.write_text(src)

assert ".pfoot" not in src, "stale .pfoot rule or markup left behind"
assert ".pgo{{display:flex" in src and 'class="pgo"' in src, "action row missing"
assert "-webkit-line-clamp:2" in src, "clamp lost"
assert "{glyph(k, 34)}" in src, "card glyph size lost"

print("Verb has its own row." if src != orig else "Already current.")
