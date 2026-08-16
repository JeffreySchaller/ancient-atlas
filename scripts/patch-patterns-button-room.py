#!/usr/bin/env python3
"""Give the header's Patterns tile room to breathe.

Same trap as the Studies tile: `.stats > div, .stats > a` is (0,1,1) and beats
`.stat-action` at (0,1,0), so the tile's designed `padding:6px 10px` is flattened
to `4px 0` and the hover pill hugs the text with zero side padding. The fix is a
selector at (0,2,0) scoped to this one tile.

Negative horizontal margin absorbs most of the new padding back out of the
layout, so the pill gets 15px of internal air while the header only grows 7px
per side. The header clips at high browser zoom; that budget is not free.

Idempotent: running twice is a no-op.
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "public" / "index.html"

src = INDEX.read_text()
orig = src

# 1. tag the tile so it can be addressed without an attribute selector
OLD_A = ('<a class="stat-action" href="patterns/" title="Patterns '
         '— the same engineering signatures across sites that never met">')
NEW_A = ('<a class="stat-action stat-patterns" href="patterns/" title="Patterns: the same '
         'engineering signatures across sites that never met">')

if NEW_A not in src:
    if OLD_A not in src:
        sys.exit("ABORT: the Patterns anchor in public/index.html is not what this patch expects")
    src = src.replace(OLD_A, NEW_A)

# 2. the scoped rule, parked next to the Studies fix it mirrors
ANCHOR = ".stats > .stat-experiences,.fw-wrap > .stat-experiences{padding:7px 15px}"
RULE = ("\n/* Same (0,1,1) trap as above. Patterns carries no border of its own, so the\n"
        "   padding only shows on hover — which is exactly when it is needed. The\n"
        "   negative margin keeps most of it out of the header's width budget. */\n"
        ".stats > .stat-patterns{padding:6px 15px;margin:-2px -8px}")

if RULE.strip() not in src:
    if ANCHOR not in src:
        sys.exit("ABORT: the Studies padding rule is gone; the CSS has been reorganised")
    src = src.replace(ANCHOR, ANCHOR + RULE)

if src != orig:
    INDEX.write_text(src)

assert src.count('class="stat-action stat-patterns"') == 1, "tile class not unique"
assert ".stats > .stat-patterns{padding:6px 15px" in src, "scoped rule missing"
assert src.count('href="patterns/"') == 2, "expected desktop tile + mobile mini-nav link"

# The rule must win. Compute specificity the same way the cascade does.
def spec(sel):
    return (sel.count("#"), sel.count(".") + sel.count("["), len(re.findall(r"(?:^|[\s>+~])([a-z]+)", sel)))

loser = spec(".stats > a")
winner = spec(".stats > .stat-patterns")
if winner <= loser:
    sys.exit(f"ABORT: {winner} does not beat {loser}; the padding would be flattened again")

print(f"Patterns tile: padding 6px 15px, specificity {winner} beats {loser}.")
print("Wrote public/index.html." if src != orig else "Already current.")
