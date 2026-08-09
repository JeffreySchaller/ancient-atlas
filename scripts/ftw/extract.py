#!/usr/bin/env python3
"""
extract.py - pull the editable app out of the Feel the Weight bundle.

public/experiences/feel-the-weight/index.html is a self-unpacking bundle:
a base64 asset manifest plus the real page, JSON-encoded, inside a
<script type="__bundler/template"> island. Editing it in place is not
practical, so the loop is:

    extract.py  ->  app.html  ->  patch-*.py  ->  inject.py

inject.py only ever rewrites the template island, so the manifest, the
photo assets and the unpacker itself survive byte-identical.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
BUNDLE = ROOT / "public" / "experiences" / "feel-the-weight" / "index.html"
APP = Path(__file__).parent / "app.html"
PAT = re.compile(r'(<script type="__bundler/template">\s*\n)(.*?)(\n\s*</script>)', re.S)

src = BUNDLE.read_text(encoding="utf-8")
m = PAT.search(src)
if not m:
    sys.exit("ABORT: template island not found in " + str(BUNDLE))
APP.write_text(json.loads(m.group(2)), encoding="utf-8")
print("  extracted %d chars -> %s" % (APP.stat().st_size, APP.name))
