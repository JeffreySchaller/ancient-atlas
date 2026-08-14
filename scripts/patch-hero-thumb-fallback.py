#!/usr/bin/env python3
"""Fix the grey placeholder heroes on the creator study page.

The four feature heroes request maxresdefault.jpg. Most YouTube uploads have
no maxres rendition, and YouTube answers those with HTTP 404 whose *body is a
valid 120x90 grey placeholder JPEG*. The browser decodes it fine and fires
`load`, not `error` - so the existing onerror-only fallback never ran and the
hero rendered as a grey box. Measured on the four current heroes:

  nC92mpGoV74  maxres 404/120x90   sd 200/640x480   <- grey
  JSLlvWKdtrs  maxres 404/120x90   sd 200/640x480   <- grey
  UZJVXxoFMoo  maxres 200/1280x720                  <- the one that worked
  k_6sk8u6R3E  maxres 404/120x90   sd 200/640x480   <- grey

So the test has to be the decoded size, not the error event. ytFallback()
walks maxres -> sd -> hq -> mq and stops at the first rendition wider than the
placeholder. sddefault is 4:3 but .fart img is object-fit:cover at 16/9, so it
crops to an effective 640x360 - sharp at the ~580px the hero renders.

Idempotent.
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build-creator-feature.py"

src = BUILDER.read_text()

OLD_FALLBACK = '''FALLBACK = ("this.onerror=null;this.src='https://i.ytimg.com/vi/'"
            "+this.dataset.vid+'/mqdefault.jpg'")


def thumb(vid, big=False):
    q = "maxresdefault" if big else "mqdefault"
    return (f'<img src="https://i.ytimg.com/vi/{e(vid["id"])}/{q}.jpg" '
            f'data-vid="{e(vid["id"])}" onerror="{FALLBACK}" alt="" '
            f'loading="lazy" decoding="async">')'''

NEW_FALLBACK = '''def thumb(vid, big=False):
    """A YouTube still.

    Big (feature hero): ask for maxresdefault and let ytFallback() walk down
    to whatever actually exists. YouTube serves a missing rendition as a 404
    carrying a valid 120x90 grey JPEG, which browsers treat as a successful
    load - so the fallback triggers on decoded width, not on the error event.

    Small (strip and deck cards): mqdefault always exists for a live video and
    at ~165px on screen there is nothing to gain from a larger fetch, which
    matters when the deck holds a few hundred of them.
    """
    v = e(vid["id"])
    if not big:
        return (f'<img src="https://i.ytimg.com/vi/{v}/mqdefault.jpg" '
                f'alt="" loading="lazy" decoding="async">')
    return (f'<img src="https://i.ytimg.com/vi/{v}/maxresdefault.jpg" '
            f'data-vid="{v}" data-q="0" '
            f'onload="ytFallback(this)" onerror="ytFallback(this)" '
            f'alt="" loading="lazy" decoding="async">')'''

HELPER = '''SCRIPT = """
// A missing YouTube thumbnail comes back as a 404 whose body is a valid
// 120x90 grey placeholder, so the image "loads" and onerror never fires.
// Step down the rendition ladder until something wider than the placeholder
// arrives. Global on purpose - the hero imgs call it from onload/onerror.
function ytFallback(img){
  var q = ['maxresdefault','sddefault','hqdefault','mqdefault'];
  var i = +(img.dataset.q || 0);
  if (img.naturalWidth > 120 || i >= q.length - 1) return;
  img.dataset.q = ++i;
  img.src = 'https://i.ytimg.com/vi/' + img.dataset.vid + '/' + q[i] + '.jpg';
}
'''

edits = 0
if "def ytFallback" not in src and "ytFallback(this)" not in src:
    if src.count(OLD_FALLBACK) != 1:
        sys.exit("ABORT: the FALLBACK/thumb block is not in the shape this "
                 "patch expects - inspect build-creator-feature.py by hand")
    src = src.replace(OLD_FALLBACK, NEW_FALLBACK, 1)
    edits += 1

if "function ytFallback" not in src:
    if src.count('SCRIPT = """\n') != 1:
        sys.exit(f'ABORT: expected 1 SCRIPT block, found {src.count(chr(83)+"CRIPT = " + chr(34)*3)}')
    src = src.replace('SCRIPT = """\n', HELPER, 1)
    edits += 1

assert src.count("function ytFallback") == 1, "helper duplicated"
assert src.count("def thumb(") == 1, "thumb duplicated"
assert "FALLBACK = (" not in src, "the dead FALLBACK constant survived"
assert "%d" in src, "the SCRIPT percent-format placeholder was lost"

if edits:
    BUILDER.write_text(src)
    compile(src, str(BUILDER), "exec")

print(f"{edits} edit(s) applied to scripts/build-creator-feature.py")
if not edits:
    print("Already patched - nothing to do.")
