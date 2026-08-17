#!/usr/bin/env python3
"""
build-creators-hub.py — the /creators/ index (2026-08-13)

Both Ageless Rock pages were orphans: nothing on the site linked to them and
the sitemap never saw them, because build-seo-pages.py only globbed library/.
This builds the index that gives them a home, gives the YouTube channel a
durable URL to point at, and scales to Creator Study No. 02 and beyond.

Every number on the page is counted from data/ at build time. Nothing is
hand-typed, so the page cannot drift away from the Atlas.

Interview state lives in data/feature.json. An empty id renders the "coming"
state rather than a broken embed — see scripts/set-interview.py.

Run from repo root, after build.py.
"""
import json
import sys
import collections
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
OUT = ROOT / "public" / "creators" / "index.html"
BASE = "https://theancientatlas.com"

def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))

creators = load("creators.json")
videos = load("videos.json")
feature = load("feature.json")
iv = feature.get("interview", {})
IV_ID = (iv.get("id") or "").strip()

# ---------------------------------------------------------------- counts
wires = collections.Counter()
sites = collections.defaultdict(set)
for site, vs in videos.items():
    for v in vs:
        k = v.get("cr")
        if not k:
            continue
        wires[k] += 1
        sites[k].add(site)

if "agelessrock" not in wires:
    sys.exit("ABORT: no agelessrock wires found — refusing to build a feature page about nothing")

AR_V, AR_S = wires["agelessrock"], len(sites["agelessrock"])
runner_up = wires.most_common(2)[1]
TOTAL_V = sum(wires.values())
TOTAL_SITES = len({s for v in sites.values() for s in v})

STUDY = {
    "no": "01", "slug": "ageless-rock", "name": "Ageless Rock", "person": "Bernie Ong",
    "handle": "@AgelessRock888",
    "line": "Four ways of working stone, traced across a body of work built in the edit room rather than on the road.",
}

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------------------------------------------------------------- interview block
if IV_ID:
    interview = f'''      <div class="iv">
        <div class="iv-frame"><iframe src="https://www.youtube-nocookie.com/embed/{IV_ID}"
          title="{esc(iv.get('title',''))}" loading="lazy" allowfullscreen
          allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"></iframe></div>
        <div class="iv-meta"><span class="tag tag-live">The interview</span>
          <p>{esc(iv.get("title",""))}</p>
          <a class="btn btn-ghost" href="https://youtu.be/{IV_ID}" rel="noopener">Watch on the channel ↗</a></div>
      </div>'''
else:
    interview = '''      <div class="iv iv-soon">
        <div class="iv-frame iv-placeholder"><span>Conversation forthcoming</span></div>
        <div class="iv-meta"><span class="tag">The interview</span>
          <p>A conversation with Bernie Ong is being cut now, and lands on the Ancient Atlas
             channel shortly. The study below stands on its own until it does.</p>
          <a class="btn btn-ghost" href="https://www.youtube.com/@AncientAtlasMap" rel="noopener">The Atlas channel ↗</a></div>
      </div>'''

# ---------------------------------------------------------------- contributor table
rows = []
top_n = wires.most_common(1)[0][1]
for k, n in wires.most_common(14):
    m = creators.get(k, {})
    nm = esc(m.get("name") or k)
    handle = esc(m.get("handle") or "")
    col = m.get("color") or "#C9A84C"
    lead = ' class="lead"' if k == "agelessrock" else ""
    rows.append(
        f'<tr{lead}><td><i style="background:{col}"></i>{nm}</td>'
        f'<td class="hnd">{handle}</td>'
        f'<td class="bar"><i style="width:{max(4, round(n / top_n * 100))}%;'
        f'background:linear-gradient(90deg,{col},rgba(232,185,96,.85))"></i></td></tr>')
rows = "\n".join(rows)

share = AR_V / TOTAL_V * 100

html = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Creator Studies | The Ancient Atlas</title>
<meta name="description" content="Close readings of the channels documenting the ancient world. A site page shows you a place. A body of work shows you a habit of mind.">
<link rel="canonical" href="{BASE}/creators/">
<meta property="og:title" content="Creator Studies · The Ancient Atlas">
<meta property="og:description" content="Study No. 01: Ageless Rock. Four ways of working stone, traced across one body of work.">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:url" content="{BASE}/creators/">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--obsidian:#0B0B0F;--charcoal:#14141A;--slate:#1C1C24;--stone:#2A2A35;
--champagne:#C9A84C;--amber:#E8B960;--ivory:#F0EEE9;--cloud:#C5C5D0;--mist:#8A8A9A;
--sans:'Inter',system-ui,sans-serif;--serif:'Fraunces',Georgia,serif;--mono:'JetBrains Mono',monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--obsidian);color:var(--ivory);font-family:var(--sans);line-height:1.6;
-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 clamp(20px,4vw,48px)}}
nav{{display:flex;gap:26px;align-items:center;padding:22px 0;border-bottom:1px solid rgba(201,168,76,.16);
font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;flex-wrap:wrap}}
nav a{{color:var(--mist);text-decoration:none;transition:color .18s}} nav a:hover{{color:var(--amber)}}
nav a.here{{color:var(--champagne)}}
nav .brand{{color:var(--champagne);font-weight:600;letter-spacing:.2em;margin-right:auto}}
header{{padding:clamp(56px,9vw,110px) 0 clamp(30px,5vw,54px)}}
.kicker{{font-family:var(--mono);font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--champagne)}}
h1{{font-family:var(--serif);font-weight:600;font-size:clamp(40px,7vw,78px);line-height:1.04;
letter-spacing:-.02em;margin:18px 0 20px}}
.deck{{font-size:clamp(16px,2vw,19px);color:var(--cloud);max-width:60ch}}
.deck + .deck{{margin-top:15px}}
.deck b{{color:var(--ivory);font-weight:500}}
section{{padding:clamp(34px,5vw,60px) 0;border-top:1px solid rgba(201,168,76,.14)}}
h2{{font-family:var(--mono);font-size:11px;letter-spacing:.26em;text-transform:uppercase;
color:var(--champagne);margin-bottom:26px}}
.study{{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(24px,4vw,52px);align-items:start}}
@media(max-width:860px){{.study{{grid-template-columns:1fr}}}}
/* An index against an entry, not a headline of its own. Baseline-aligned with
   the name so the pair reads as one object. */
.hd{{display:flex;align-items:baseline;gap:clamp(12px,1.6vw,20px);flex-wrap:wrap}}
.no{{font-family:var(--serif);font-size:clamp(38px,5.4vw,62px);line-height:.9;color:var(--stone);font-weight:600;flex:none}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}}
.study h3{{font-family:var(--serif);font-size:clamp(30px,4.4vw,46px);font-weight:600;line-height:1.08;
margin:10px 0 12px;letter-spacing:-.01em}}
.study .who{{font-family:var(--mono);font-size:12px;letter-spacing:.1em;color:var(--mist);margin-bottom:18px}}
.study p.body{{color:var(--cloud);margin-bottom:22px;max-width:52ch}}
.stats{{display:flex;gap:30px;flex-wrap:wrap;margin:24px 0 28px;padding:20px 0;
border-top:1px solid rgba(201,168,76,.14);border-bottom:1px solid rgba(201,168,76,.14)}}
.stat b{{display:block;font-family:var(--serif);font-size:34px;font-weight:600;color:var(--amber);line-height:1}}
.stat span{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist)}}
/* Three analogs where three counts used to be. A digital quantity is invisible,
   so it gets rendered at a scale a body understands, and unlike a figure it does
   not go stale as the archive grows. */
.facts{{display:flex;flex-direction:column;gap:0;margin:24px 0 28px;
border-top:1px solid rgba(201,168,76,.16);border-bottom:1px solid rgba(201,168,76,.16)}}
.fact{{display:flex;align-items:baseline;gap:18px;padding:13px 2px}}
.fact + .fact{{border-top:1px solid rgba(201,168,76,.09)}}
.fact span{{font-family:var(--mono);font-size:9.5px;letter-spacing:.17em;text-transform:uppercase;
color:var(--amber);flex:none;width:74px}}
.fact p{{margin:0;font-size:14.5px;line-height:1.5;color:var(--cloud)}}
/* The bar IS the analog. It says "one channel carries most of this" faster than
   a number, and it cannot go stale. */
th.barh{{text-align:left;width:44%}}
td.bar{{padding:11px 10px}}
td.bar i{{display:block;height:5px;border-radius:4px;min-width:6px;
box-shadow:0 0 10px rgba(232,185,96,.16)}}
@media(max-width:640px){{.fact{{flex-direction:column;gap:5px}}.fact span{{width:auto}}}}
.btns{{display:flex;gap:12px;flex-wrap:wrap}}
/* Two doors, not two pills. Identical buttons say the choice does not matter;
   the choice is the point. Each names what is behind it. */
.doors-lede{{font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;
text-transform:uppercase;color:var(--amber);margin:30px 0 11px}}
.doors{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.door{{display:block;text-decoration:none;border:1px solid rgba(201,168,76,.22);
border-radius:12px;padding:15px 16px 14px;background:rgba(201,168,76,.035);
transition:border-color .16s,background .16s,transform .16s}}
.door:hover{{border-color:rgba(201,168,76,.55);background:rgba(201,168,76,.08);
transform:translateY(-2px)}}
.door b{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
color:var(--amber);font-weight:500;line-height:1.35}}
.door b i{{font-style:normal;flex:none;transition:transform .16s}}
.door:hover b i{{transform:translateX(4px)}}
.door p{{margin:9px 0 0;font-size:13.5px;line-height:1.5;color:var(--cloud)}}
@media(max-width:860px){{.doors{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{.door,.door b i{{transition:none}}
.door:hover{{transform:none}}.door:hover b i{{transform:none}}}}
.btn{{display:inline-block;font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
padding:14px 22px;border-radius:10px;text-decoration:none;transition:.2s;font-weight:500}}
.btn-solid{{background:linear-gradient(180deg,var(--amber),var(--champagne));color:#241c07;font-weight:600}}
.btn-solid:hover{{filter:brightness(1.08)}}
.btn-ghost{{border:1px solid rgba(232,185,96,.5);color:var(--amber)}}
.btn-ghost:hover{{background:rgba(232,185,96,.12)}}
.iv{{border:1px solid rgba(201,168,76,.2);border-radius:16px;overflow:hidden;background:var(--charcoal)}}
.iv-frame{{aspect-ratio:16/9;background:#000}}
.iv-frame iframe{{width:100%;height:100%;border:0;display:block}}
.iv-placeholder{{display:flex;align-items:center;justify-content:center;
background:radial-gradient(circle at 50% 40%,rgba(201,168,76,.10),rgba(11,11,15,0) 70%),var(--slate)}}
.iv-placeholder span{{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mist)}}
.iv-meta{{padding:20px 22px 22px}}
.iv-meta p{{color:var(--cloud);font-size:14.5px;margin:12px 0 16px}}
.tag{{display:inline-block;font-family:var(--mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
color:var(--mist);border:1px solid rgba(201,168,76,.3);border-radius:999px;padding:4px 11px}}
.tag-live{{color:#241c07;background:var(--amber);border-color:var(--amber);font-weight:600}}
table{{width:100%;border-collapse:collapse;font-size:14.5px}}
th{{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mist);
text-align:left;padding:0 10px 12px;font-weight:500}}
th.num,td.num{{text-align:right}}
td{{padding:11px 10px;border-top:1px solid rgba(201,168,76,.1);color:var(--cloud)}}
td i{{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:11px;vertical-align:middle}}
tr.lead td{{color:var(--ivory);font-weight:600;background:rgba(201,168,76,.06)}}
td.hnd{{font-family:var(--mono);font-size:11.5px;color:var(--mist)}}
td.num{{font-family:var(--mono);color:var(--ivory)}}
.note{{font-size:13.5px;color:var(--mist);margin-top:18px;max-width:64ch}}
.shop{{display:flex;gap:22px;align-items:center;flex-wrap:wrap;justify-content:space-between;
border:1px solid rgba(201,168,76,.22);border-radius:16px;padding:26px 28px;background:var(--charcoal)}}
.shop p{{color:var(--cloud);max-width:52ch;font-size:14.5px;margin-top:8px}}
footer{{padding:44px 0 70px;border-top:1px solid rgba(201,168,76,.14);
font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--mist)}}
footer a{{color:var(--mist);text-decoration:none}} footer a:hover{{color:var(--amber)}}
</style></head><body>
<div class="wrap">
<nav>
  <a class="brand" href="/">THE ANCIENT ATLAS</a>
  <a href="/">Map</a><a href="/sites/">Sites</a><a href="/library/">Library</a>
  <a class="here" href="/creators/">Creator Studies</a>
  <a href="/experiences/feel-the-weight/">Feel the Weight</a>
  <a href="https://editions.theancientatlas.com" rel="noopener">Editions ↗</a>
</nav>

<header>
  <div class="kicker">Creator Studies</div>
  <h1>The people who<br>actually went looking</h1>
  <p class="deck">Everything on this map that you can actually watch exists because somebody carried a
  camera up a hill and pressed record. Nobody commissioned it. They went, and then they came back
  and showed the rest of us.</p>
  <p class="deck">A Creator Study is a close reading of one of those bodies of work. What it covers,
  what it keeps circling back to, and what only comes into focus when you see the whole of it at
  once. That last part is the reason to be here. A site page shows you a place. A body of work shows
  you a habit of mind.</p>
</header>

<section>
  <h2 class="sr-only">Study No. {STUDY["no"]}: {STUDY["name"]}</h2>
  <div class="study">
    <div>
      <div class="hd"><span class="no">{STUDY["no"]}</span><h3>{STUDY["name"]}</h3></div>
      <div class="who">{STUDY["person"]} · {STUDY["handle"]}</div>
      <p class="body">{STUDY["line"]} Not a travel channel. Each episode is assembled and narrated rather than shot on
      location, and that is precisely why the pattern shows through it. A traveller is bound by an
      itinerary. A researcher can set Ethiopia beside Peru on the same screen and let you look at
      both at once.</p>
      <div class="facts">
        <div class="fact"><span>Reach</span><p>More of this map than any other single channel.</p></div>
        <div class="fact"><span>Method</span><p>Assembled from research, so the argument is not bound by a flight path.</p></div>
        <div class="fact"><span>Depth</span><p>Weeks of evenings, if you started tonight.</p></div>
      </div>
      <p class="doors-lede">Two ways in</p>
      <div class="doors">
        <a class="door" href="/creators/ageless-rock.html">
          <b>Follow the argument <i>&rarr;</i></b>
          <p>What repeats when you stop sorting these places by where they are. Four answers,
          each with the footage that makes its case.</p></a>
        <a class="door" href="/creators/ageless-rock-by-place.html">
          <b>Start where you already care <i>&rarr;</i></b>
          <p>Every episode filed by the place it studies rather than the day it was posted.
          Begin with a country you know and let it lead you outward.</p></a>
      </div>
    </div>
{interview}
  </div>
</section>

<section>
  <h2>Where the footage comes from</h2>
  <table>
    <thead><tr><th>Channel</th><th>Handle</th><th class="barh">Share of the Atlas</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <p class="note">Measured by what is wired into this map, not by subscriber count. The bars are
  relative to each other: one channel carries more of the Atlas than any other, by a margin you can
  see without being told the figure.</p>
</section>

<section>
  <div class="shop">
    <div>
      <div class="kicker">Editions</div>
      <p>The Atlas is free and always will be. Editions is what keeps it that way: prints and
      pieces for people who would rather look at this every day than scroll past it.</p>
    </div>
    <a class="btn btn-solid" href="https://editions.theancientatlas.com?from=creators" rel="noopener">Visit Editions →</a>
  </div>
</section>

<footer>
  <a href="/">The Ancient Atlas</a>, a hand-curated map of the deep past ·
  <a href="/sites/">All sites</a> · <a href="/library/">Library</a> ·
  <a href="/contribute.html">Contribute</a> · <a href="/contact.html">Contact</a>
</footer>
</div></body></html>
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"  ✓ {OUT.relative_to(ROOT)}")
print(f"    Ageless Rock: {AR_V} wires / {AR_S} sites ({share:.1f}% of {TOTAL_V})")
print(f"    interview   : {'LIVE ' + IV_ID if IV_ID else 'not yet released (placeholder state)'}")
