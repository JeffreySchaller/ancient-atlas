#!/usr/bin/env python3
"""
inject.py - put app.html back into the Feel the Weight bundle.

Rewrites ONLY the <script type="__bundler/template"> island. The asset
manifest, the external-resource map and the unpacker are untouched.

THE ESCAPING RULE - read this before changing anything
------------------------------------------------------
The template is a JSON string living INSIDE a <script> element, and the
app it encodes contains </script> tags of its own. A plain json.dumps()
therefore emits a literal "</script>" that closes the island early, and
the page dies at load with

    Error unpacking: Unterminated string in JSON at position 198

which is exactly what happened the first time. The original bundler
sidesteps this by escaping the solidus as \\u002F, so </script> ships as
<\\u002Fscript>. \\u002F is legal JSON and decodes straight back to "/",
so escaping every "</" is both sufficient and lossless. The round-trip
assertion below is what actually guarantees it - keep it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
BUNDLE = ROOT / "public" / "experiences" / "feel-the-weight" / "index.html"
APP = Path(__file__).parent / "app.html"
PAT = re.compile(r'(<script type="__bundler/template">\s*\n)(.*?)(\n\s*</script>)', re.S)


def island(src, name):
    m = re.search(r'<script type="__bundler/' + name + r'">\s*\n(.*?)\n\s*</script>', src, re.S)
    if not m:
        sys.exit("ABORT: missing __bundler/" + name + " island")
    return json.loads(m.group(1))


def main():
    src = BUNDLE.read_text(encoding="utf-8")
    m = PAT.search(src)
    if not m:
        sys.exit("ABORT: template island not found")
    app = APP.read_text(encoding="utf-8")

    manifest = island(src, "manifest")
    ext = island(src, "ext_resources")
    before = json.loads(m.group(2))

    # Every uuid the unpacker substitutes must still be referenced, or an
    # asset silently resolves to an empty blob and a photo renders blank.
    lost = [u for u in manifest if u in before and u not in app]
    if lost:
        sys.exit("ABORT: %d asset uuid(s) dropped from the template: %s"
                 % (len(lost), lost[:4]))

    # The bundle carries its OWN <title> in the outer shell, shown for the
    # second or so before the unpacker swaps the document. Left alone it keeps
    # flashing the previous copy in the tab strip, so keep the two in step.
    inner = re.search(r"<title>(.*?)</title>", app, re.S)
    if inner:
        src = re.sub(r"<title>.*?</title>", "<title>" + inner.group(1) + "</title>",
                     src, count=1, flags=re.S)
        m = PAT.search(src)
        print("  outer title synced: " + inner.group(1))

    encoded = json.dumps(app).replace("</", "<\\u002F")
    if "</script>" in encoded or "</" in encoded:
        sys.exit("ABORT: unescaped close tag survived encoding")
    if json.loads(encoded) != app:
        sys.exit("ABORT: encoded island does not round-trip to the source")

    out = src[:m.start(2)] + encoded + src[m.end(2):]
    BUNDLE.write_text(out, encoding="utf-8")

    # Re-read from disk and decode, the same way the browser will.
    check = BUNDLE.read_text(encoding="utf-8")
    if json.loads(PAT.search(check).group(2)) != app:
        sys.exit("ABORT: written bundle does not decode back to app.html")
    for name in ("manifest", "ext_resources", "page_order"):
        island(check, name)

    print("  injected %d chars; %d manifest assets, %d ext resources intact"
          % (len(app), len(manifest), len(ext)))
    print("  round-trip verified from disk")


if __name__ == "__main__":
    main()
