#!/usr/bin/env python3
# Two things Bernie did that the Atlas had not caught up with.
#
# 1. Panoias Sanctuary has been on the map since before he filmed it, and his
#    walkthrough went up in June. The site sat there with an empty video list.
#
# 2. On 17 Aug he published "Comparing 4 religions", which is not a site
#    walkthrough at all - the thumbnail is our map and the description is an
#    invitation to come and talk to us, linking the site and our joint
#    interview. It has no home in videos.json because it is not about a place.
#    It belongs beside the interview it answers.
#
# Idempotent. Assertions read the finished files.

import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HUB = ROOT / "scripts" / "build-creators-hub.py"

PANOIAS_SITE = "Panoias Sanctuary"
PANOIAS_VID = {
    "id": "O1bIu4FFbEQ",
    "title": "Panoias Sanctuary of Vale de Nogueiras Village",
    "cr": "agelessrock",
    "added": "2026-08-20",
    "published": "2026-06-25",
}
REPLY = {
    "id": "CB9d9SRtmOs",
    "title": "Comparing 4 religions",
    "published": "2026-08-17",
    "note": "Bernie's answer to the interview: he opens the Atlas on screen and "
            "invites his audience to come and talk to us. Not a site walkthrough, "
            "so it lives here rather than in videos.json.",
}

# ------------------------------------------------------------ 1. the walkthrough
vp = DATA / "videos.json"
videos = json.loads(vp.read_text(encoding="utf-8"))

# videos.json is keyed only by sites that already have footage, so a site with
# none has no key at all. sites.json is the authority on whether the place
# exists; a key created here must match its name exactly or the video dangles.
sites = json.loads((DATA / "sites.json").read_text(encoding="utf-8"))
if not any(s["n"] == PANOIAS_SITE for s in sites):
    sys.exit("ABORT: %r is not a site in sites.json, so the video would dangle" % PANOIAS_SITE)
videos.setdefault(PANOIAS_SITE, [])

seen = {v["id"] for vs in videos.values() for v in vs}
if PANOIAS_VID["id"] not in seen:
    videos[PANOIAS_SITE].append(PANOIAS_VID)
    vp.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ------------------------------------------------------------ 2. the reply
fp = DATA / "feature.json"
feature = json.loads(fp.read_text(encoding="utf-8"))
if feature.get("reply", {}).get("id") != REPLY["id"]:
    feature["reply"] = REPLY
    fp.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# -------------------------------------------------- 3. render it beside the interview
hub = HUB.read_text(encoding="utf-8")
orig_hub = len(hub)

READ = 'iv = feature.get("interview", {})\nIV_ID = (iv.get("id") or "").strip()'
READ_NEW = (READ + '\nrp = feature.get("reply", {})\nRP_ID = (rp.get("id") or "").strip()')
if "RP_ID" not in hub:
    if READ not in hub:
        sys.exit("ABORT: the feature block in build-creators-hub.py moved")
    hub = hub.replace(READ, READ_NEW, 1)

BLOCK = '''
# ---------------------------------------------------------------- the reply
# A creator pointing back at us is worth more than anything we can say about
# ourselves, so it sits inside the interview card rather than below the fold.
if RP_ID:
    reply = (f'<p class="iv-reply">And his answer: '
             f'<a href="https://youtu.be/{RP_ID}" rel="noopener">'
             f'{esc(rp.get("title",""))} \\u2197</a></p>')
else:
    reply = ""

'''
ANCHOR = "# ---------------------------------------------------------------- interview block"
if "iv-reply" not in hub:
    if ANCHOR not in hub:
        sys.exit("ABORT: the interview block anchor moved")
    hub = hub.replace(ANCHOR, BLOCK.lstrip("\n") + ANCHOR, 1)

OLD_CTA = ('          <a class="btn btn-ghost" href="https://youtu.be/{IV_ID}" rel="noopener">'
           'Watch on the channel \u2197</a></div>')
NEW_CTA = ('          <a class="btn btn-ghost" href="https://youtu.be/{IV_ID}" rel="noopener">'
           'Watch on the channel \u2197</a>{reply}</div>')
if "{reply}</div>" not in hub:
    if OLD_CTA not in hub:
        sys.exit("ABORT: the interview call to action moved")
    hub = hub.replace(OLD_CTA, NEW_CTA, 1)

CSS_ANCHOR = ".iv-meta"   # matched as ".iv-meta{" below
if ".iv-reply{" not in hub:
    i = hub.find(CSS_ANCHOR + "{")
    if i == -1:
        sys.exit("ABORT: no .iv-meta rule to hang the reply styling off")
    # every rule in this template closes with "}}", so seeking the first "}"
    # lands BETWEEN the pair and splits it, which is how the builder stopped
    # parsing the first time round
    j = hub.index("}}", i) + 2
    css = ("\n.iv-reply{{margin-top:11px;font-size:12.5px;line-height:1.6;color:var(--mist)}}"
           "\n.iv-reply a{{color:var(--champagne);text-decoration:none;"
           "border-bottom:1px solid rgba(201,168,76,.35)}}"
           "\n.iv-reply a:hover{{color:var(--amber)}}")
    hub = hub[:j] + css + hub[j:]

if len(hub) != orig_hub:
    HUB.write_text(hub, encoding="utf-8")

# ------------------------------------------------------------------ assertions
fails = []
def want(c, m):
    if not c: fails.append(m)

videos = json.loads(vp.read_text(encoding="utf-8"))
pan = videos[PANOIAS_SITE]
want(sum(1 for v in pan if v["id"] == PANOIAS_VID["id"]) == 1,
     "the Panoias walkthrough is missing or duplicated")
for site, vs in videos.items():
    ids = [v["id"] for v in vs]
    if len(ids) != len(set(ids)):
        fails.append("%s lists the same video twice" % site)

feature = json.loads(fp.read_text(encoding="utf-8"))
want(feature.get("reply", {}).get("id") == REPLY["id"], "the reply did not land in feature.json")
want(feature.get("interview", {}).get("id") == "2OSddPnrShw",
     "the interview entry was disturbed")

hub = HUB.read_text(encoding="utf-8")
for token in ["RP_ID", "iv-reply", "{reply}</div>", ".iv-reply{"]:
    want(token in hub, "builder is missing %r" % token)
want(hub.count("{reply}</div>") == 1, "the reply is rendered more than once")
import ast
try:
    ast.parse(hub)
except SyntaxError as e:
    fails.append("the builder no longer parses: %s" % e)

if fails:
    for f in fails:
        print("  FAIL " + f)
    sys.exit("ABORT: %d check(s) failed" % len(fails))

print("Panoias Sanctuary: %d video(s) -> %s" % (len(pan), ", ".join(v["id"] for v in pan)))
print("feature.json reply: %s (%s)" % (REPLY["id"], REPLY["published"]))
print("builder wired to render the reply inside the interview card")
