#!/usr/bin/env python3
"""Four refinements to the Patterns shelf, in one pass.

1. Bigger glyphs. They were drawn as logos and rendered as bullets: 30px on the
   page kicker, 26px on the index cards. Raised to 40 / 34 so the mark reads as
   the pattern's identity rather than as decoration next to the label.

2. Two-line clamp on the index card blurbs. Each card now shows the opening of
   the claim and stops, with a native ellipsis. The full sentence is the first
   thing on the pattern page, so the card opens a loop the page closes. This is
   the Zeigarnik effect used honestly: nothing is hidden that the click does not
   immediately deliver, and no text is invented to be truncated.

3. Em dashes cleared from every string the site renders. Video titles are left
   exactly as their creators published them: those are citations, not our copy.

4. Claims rewritten so the cut lands somewhere useful. Concrete nouns first, the
   payoff last, second person where it fits. "Softer does not cut harder" is now
   below the fold on the hardness card by design.

Idempotent: running twice is a no-op. Aborts if any anchor has drifted.
"""
import json
import ast
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PJSON = REPO / "data" / "patterns.json"
BUILDER = REPO / "scripts" / "build-patterns.py"

EMDASH = "—"

# ---------------------------------------------------------------- patterns.json

CLAIMS = {
    "machining": "Striations, bore holes, saw kerfs and flat-planed faces that look mechanical. "
                 "Four continents, no contact between them, and stone their documented toolkits "
                 "were not supposed to cut.",
    "precision": "Joints you cannot slide paper into. Surfaces flat to a fraction of a millimetre, "
                 "corners cut square in granite, and the tolerance holds across whole buildings "
                 "rather than one showpiece block.",
    "polygonal": "Many-sided stones cut to fit each other rather than to a standard. No vertical "
                 "joint runs the height of the wall, so when the ground moves the wall flexes "
                 "instead of failing.",
    "geometry": "Circles, spirals, cup-and-ring marks, precise alignments and repeated proportions. "
                "Every inhabited continent carries some of them, in cultures with no route between "
                "them.",
    "scale": "Blocks from 50 to 1,500 tons, quarried, dressed, and in most cases carried somewhere "
             "else, by people whose documented toolkit was rope, timber and muscle.",
    "hardness": "Granite, diorite, basalt and andesite, 6 to 7 on Mohs, worked to a finish by "
                "cultures whose surviving tools are copper and stone. Softer does not cut harder.",
    "stratigraphy": "Weathering, sediment and buried courses that read older than the date on the "
                    "sign. The one criterion where the evidence sits under the building rather "
                    "than in it.",
}

# (json path, old fragment, new fragment) — fragments, so an unrelated edit
# elsewhere in the same paragraph does not silently break the patch.
PROSE = [
    ("machining", "essay", 1, "different processes " + EMDASH + " appearance",
                              "different processes; appearance"),
    ("machining", "videos_note", None, "site walkthroughs " + EMDASH + " which is why",
                                       "site walkthroughs, which is why"),
    ("geometry", "essay", 0, "constructions recur " + EMDASH + " the same alignment",
                             "constructions recur: the same alignment"),
    ("scale", "essay", 0, "is people " + EMDASH + " 2,205 of them",
                          "is people: 2,205 of them"),
    ("hardness", "essay", 0,
     "is abrasion " + EMDASH + " sand, dolerite pounders, time " + EMDASH + " and for rough",
     "is abrasion, meaning sand, dolerite pounders and time, and for rough"),
    ("stratigraphy", "essay", 0, "a dispute exists " + EMDASH + " not that it",
                                 "a dispute exists, not that it"),
]

NOTE_FIX = ("machining", 2, "Türkiye " + EMDASH + " the reference surface",
                            "Türkiye · the reference surface")

data = json.loads(PJSON.read_text())
keys = [k for k in data if not k.startswith("_")]
missing = set(CLAIMS) - set(keys)
if missing:
    sys.exit(f"ABORT: patterns.json is missing {sorted(missing)}")

claims_changed = 0
for k, new in CLAIMS.items():
    if data[k]["claim"] != new:
        data[k]["claim"] = new
        claims_changed += 1

prose_changed = 0
for key, field, idx, old, new in PROSE:
    holder = data[key]
    cur = holder[field][idx] if idx is not None else holder[field]
    if new in cur:
        continue
    if old not in cur:
        sys.exit(f"ABORT: anchor drifted at {key}.{field}[{idx}]: {old!r} not found")
    cur = cur.replace(old, new)
    if idx is not None:
        holder[field][idx] = cur
    else:
        holder[field] = cur
    prose_changed += 1

key, vidx, old, new = NOTE_FIX
note = data[key]["videos"][vidx].get("note", "")
if new not in note:
    if old not in note:
        sys.exit(f"ABORT: anchor drifted at {key}.videos[{vidx}].note: {old!r} not found")
    data[key]["videos"][vidx]["note"] = note.replace(old, new)
    prose_changed += 1

# Every rendered string must now be clean. Video titles are exempt: they are the
# creators' own titles, quoted verbatim, and editing them would be a citation error.
leftovers = []


def sweep(node, path, exempt=False):
    if isinstance(node, dict):
        for kk, vv in node.items():
            sweep(vv, f"{path}.{kk}", exempt or kk == "title")
    elif isinstance(node, list):
        for i, vv in enumerate(node):
            sweep(vv, f"{path}[{i}]", exempt)
    elif isinstance(node, str) and not exempt and EMDASH in node:
        leftovers.append((path, node))


sweep(data, "")
if leftovers:
    for p, s in leftovers:
        print(f"  LEFT {p}: {s}")
    sys.exit(f"ABORT: {len(leftovers)} em dashes still in rendered copy")

PJSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# ------------------------------------------------------------- build-patterns.py

src = BUILDER.read_text()
orig = src

BUILDER_EDITS = [
    # 1. glyph sizes
    ("{glyph(key, 30)}", "{glyph(key, 40)}"),
    ("{glyph(k, 26)}", "{glyph(k, 34)}"),
    # a larger mark needs a little more air beside the label
    ("color:var(--champagne);margin:0 0 14px;display:flex;align-items:center;gap:11px}",
     "color:var(--champagne);margin:0 0 16px;display:flex;align-items:center;gap:14px}"),
    ("color:var(--champagne);margin:0 0 11px;display:flex;align-items:center;gap:10px}}",
     "color:var(--champagne);margin:0 0 12px;display:flex;align-items:center;gap:13px}}"),
    # 2. two-line clamp with ellipsis on the card blurb
    (".pb{{font-size:13.5px;color:var(--cloud);margin:0 0 12px}}",
     ".pb{{font-size:13.5px;line-height:1.5;color:var(--cloud);margin:0 0 12px;\n"
     "display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;\n"
     "overflow:hidden;text-overflow:ellipsis}}"),
    # 3. em dashes out of every rendered string
    ('title = f\'{spec["name"]} ' + EMDASH + ' a pattern across',
     'title = f\'{spec["name"]}: a pattern across'),
    ("content=\"{e(spec['name'])} " + EMDASH + " The Ancient Atlas\"",
     "content=\"{e(spec['name'])} · The Ancient Atlas\""),
    ("<h2>Watch the comparison " + EMDASH + " {len(vids)} studies</h2>",
     "<h2>Watch the comparison · {len(vids)} studies</h2>"),
    ("what it is not " + EMDASH + " the argument in full",
     "what it is not: the argument in full"),
    ("<h2>Every site in the Atlas that carries it " + EMDASH + " {len(carriers)}",
     "<h2>Every site in the Atlas that carries it · {len(carriers)}"),
    ('cs = {countries.get(x["n"], "' + EMDASH + '") for x in carriers}',
     'cs = {countries.get(x["n"], "?") for x in carriers}'),
    ('f\'{spec["name"]} ' + EMDASH + ' not yet written\'',
     'f\'{spec["name"]}: not yet written\''),
    ("<title>Patterns " + EMDASH + " the same idea, in places that never met",
     "<title>Patterns: the same idea, in places that never met"),
    ('content="Patterns ' + EMDASH + ' The Ancient Atlas"',
     'content="Patterns · The Ancient Atlas"'),
    ("were made " + EMDASH + " seven engineering signatures tracked across 618 sites, each with "
     "the comparative studies\nthat argue it. Sort by country and these never appear together. "
     "Sort by method and they are obviously\none idea.",
     "were made: seven engineering signatures tracked across 618 sites, each with the studies "
     "that\nargue it. Sort by country and these never appear together. Sort by method and you are "
     "looking\nat one idea."),
]

for old, new in BUILDER_EDITS:
    if new in src and old not in src:
        continue
    if old not in src:
        sys.exit(f"ABORT: builder anchor drifted: {old[:70]!r}")
    src = src.replace(old, new)

# footer line appears twice (pattern page + index); both are rendered copy
foot_old = "The Ancient Atlas " + EMDASH + " a hand-curated map of the deep past."
foot_new = "The Ancient Atlas, a hand-curated map of the deep past."
if foot_old in src:
    src = src.replace(foot_old, foot_new)
if src.count(foot_new) != 2:
    sys.exit(f"ABORT: expected 2 footers, found {src.count(foot_new)}")

# Comments, docstrings and developer-facing sys.exit strings are allowed to keep
# their dashes; they are never rendered. Assert only on string literals that can
# reach the browser, found by parsing rather than by scanning lines.
tree = ast.parse(src)
docstrings = set()
for node in ast.walk(tree):
    if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        body = getattr(node, "body", [])
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                and isinstance(body[0].value.value, str):
            docstrings.add(id(body[0].value))
exempt = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and getattr(getattr(node, "func", None), "attr", "") == "exit":
        for sub in ast.walk(node):
            exempt.add(id(sub))
bad = []
for node in ast.walk(tree):
    if isinstance(node, ast.Constant) and isinstance(node.value, str) \
            and EMDASH in node.value and id(node) not in docstrings and id(node) not in exempt:
        bad.append((node.lineno, node.value))
if bad:
    for ln, v in bad:
        print(f"  LEFT line {ln}: {v.strip()[:110]}")
    sys.exit(f"ABORT: {len(bad)} em dashes left in builder output strings")

assert "{glyph(key, 40)}" in src and "{glyph(k, 34)}" in src, "glyph sizes not raised"
assert "-webkit-line-clamp:2" in src, "clamp not applied"
assert 'href="#landmass"' in src, "shared landmass defs lost"
assert "vw = float(window)" in src, "regional minimap window lost"
assert 'k.startswith("_")' in src, "_note guard lost"

if src != orig:
    BUILDER.write_text(src)

print(f"patterns.json: {claims_changed} claims rewritten, {prose_changed} prose fixes.")
print(f"build-patterns.py: {'patched' if src != orig else 'already current'}.")
for k in keys:
    print(f"  {k:<13} claim {len(data[k]['claim']):>3} chars")
