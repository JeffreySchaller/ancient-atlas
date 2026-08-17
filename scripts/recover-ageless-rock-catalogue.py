#!/usr/bin/env python3
"""Rescue the catalogue this page is built from, and stop keeping it in Downloads.

build-creator-feature.py reads its episode list from ~/Downloads. That file is
gone. The builder has been unrunnable for some unknown length of time and nobody
found out until it was needed, which is the failure mode of every dependency that
lives in a folder people clear out.

The built page still carries every episode, so the catalogue is recovered from
it, written into data/ where the rest of the Atlas keeps its inputs, and the
builder is pointed there with Downloads left as a fallback so an existing local
copy still wins.

Refuses to write a catalogue smaller than the page it came from.
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PAGE = REPO / "public" / "creators" / "ageless-rock.html"
OUT = REPO / "data" / "ageless-rock-catalogue.md"
BUILDER = REPO / "scripts" / "build-creator-feature.py"

if not PAGE.exists():
    sys.exit("ABORT: no built page to recover from")

html = PAGE.read_text(encoding="utf-8")

# Every episode appears as a watch link with its title in the cell markup.
pairs = []
seen = set()
for m in re.finditer(
        r'href="https://www\.youtube\.com/watch\?v=([\w-]{11})"[^>]*>(.*?)</a>', html, re.S):
    vid = m.group(1)
    blob = m.group(2)
    t = re.search(r'class="t"[^>]*>(.*?)<', blob, re.S)
    if not t:
        continue
    title = re.sub(r"\s+", " ", t.group(1)).strip()
    title = (title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                  .replace("&quot;", '"').replace("&#x27;", "'").replace("&#39;", "'"))
    if vid in seen or not title:
        continue
    seen.add(vid)
    pairs.append((title, vid))

if len(pairs) < 200:
    sys.exit(f"ABORT: only recovered {len(pairs)} episodes, refusing to write a partial catalogue")

lines = [f"{i}. [{t}](https://www.youtube.com/watch?v={v})" for i, (t, v) in enumerate(pairs, 1)]
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- the builder
src = BUILDER.read_text()
OLD = 'CATALOGUE = Path.home() / "Downloads" / "ageless-rock-videos.md"'
NEW = ('# The catalogue used to live in ~/Downloads, which is not a place a build\n'
       '# input can live: it vanished, and the builder was unrunnable until the\n'
       '# episode list was recovered out of the page it had already produced. The\n'
       '# repo copy is now the source of truth; a local Downloads copy still wins if\n'
       '# one exists, so an in-progress update is not silently ignored.\n'
       '_LOCAL = Path.home() / "Downloads" / "ageless-rock-videos.md"\n'
       'CATALOGUE = _LOCAL if _LOCAL.exists() else (\n'
       '    Path(__file__).resolve().parent.parent / "data" / "ageless-rock-catalogue.md")')
if "_LOCAL = Path.home()" not in src:
    if OLD not in src:
        sys.exit("ABORT: the CATALOGUE line is not what this patch expects")
    BUILDER.write_text(src.replace(OLD, NEW))

print(f"Recovered {len(pairs)} episodes to {OUT.relative_to(REPO)}")
print("Builder now reads the repo copy, with ~/Downloads as an override.")
