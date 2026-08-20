#!/usr/bin/env python3
"""
build-creator-page.py — Ageless Rock creator page (2026-08-07)

Builds public/creators/ageless-rock.html : Bernie Ong's whole channel, 296
videos, arranged by place instead of by upload date.

Why this exists. YouTube can sort a channel by newest, oldest or most viewed.
It cannot tell you that Bernie covers 194 sites across 22 countries, or
put his eleven Chichen Itza videos next to each other, or let you jump from a
walkthrough straight into the site record. The Atlas already holds that
structure : 247 of his 296 videos are wired to sites with countries,
categories and tiers. This page is that structure made visible.

Sources
  data/videos.json        wires  (cr == "agelessrock")
  data/sites.json         cat, tier, region
  data/countries.json     country per site
  ~/Downloads/ageless-rock-videos.md   the full 296, in channel order

The 49 videos with no Atlas wire are NOT hidden. They get their own section at
the foot of the page, which doubles as a work queue : each one is a candidate
site record the Atlas does not yet carry.

Thumbnails are hotlinked from i.ytimg.com and lazy-loaded. No view counts or
publish dates are shown, because this build does not have them and inventing
them would be the exact kind of decoration the page is arguing against.

Run from repo root :  python3 scripts/build-creator-page.py
Then                  python3 scripts/build-seo-pages.py   (sitemap)
"""
import json
import html
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
OUT_DIR = REPO_ROOT / "public" / "creators"
OUT = OUT_DIR / "ageless-rock-by-place.html"
# The catalogue used to live in ~/Downloads, which is not a place a build
# can depend on: the file went missing once and this builder became
# unrunnable. Its sibling build-creator-feature.py was given the repo copy
# as a fallback at the time and this one was missed. Same fix.
_LOCAL = Path.home() / "Downloads" / "ageless-rock-videos.md"
CATALOGUE = _LOCAL if _LOCAL.exists() else (
    Path(__file__).resolve().parent.parent / "data" / "ageless-rock-catalogue.md")

CREATOR_KEY = "agelessrock"
HANDLE = "@AgelessRock888"
CHANNEL_URL = "https://www.youtube.com/@AgelessRock888"

# Narrative order, not alphabetical: start where the record is thickest.
REGION_ORDER = [
    "Asia", "Central America", "North America", "Middle East",
    "Türkiye", "Europe", "Africa", "Egypt", "South America",
    "Peru", "Greece", "Italy", "Pacific",
]

CAT_LABEL = {
    "megalithic": "Megalithic", "city": "City / Ruins", "temple": "Temple",
    "rock-cut": "Rock-Cut", "rockcut": "Rock-Cut", "tomb": "Tomb / Burial",
    "underground": "Underground", "pyramid": "Pyramid",
    "settlement": "Settlement", "geoglyph": "Geoglyph",
    "monolithic": "Monolithic",
}


def slugify(name):
    """Byte-for-byte the same rule as scripts/build-seo-pages.py.

    Do not "simplify" this. Dropping the transliteration step silently breaks
    every link to a site whose name carries a diacritic, and there are a lot of
    those: Ozkonak, Gumusler, Kirkgoz, Manazan Caves & Taskale, Aydintepe,
    Hoyuk, Ozluce, Menehune Ditch (Kikiaola). They 404 rather than erroring, so
    nothing catches it except a link check.
    """
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("ı", "i").replace("ħ", "h").replace("ø", "o").replace("ß", "ss")
    s = re.sub(r"[''']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "site"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def parse_catalogue():
    if not CATALOGUE.exists():
        sys.exit(f"ABORT: catalogue not found at {CATALOGUE}")
    rows = []
    pat = re.compile(r"^(\d+)\.\s+\[(.+?)\]\((https://www\.youtube\.com/watch\?v=([\w-]+))\)\s*$")
    for line in CATALOGUE.read_text(encoding="utf-8").splitlines():
        m = pat.match(line.strip())
        if m:
            rows.append({"n": int(m.group(1)), "title": m.group(2),
                         "url": m.group(3), "id": m.group(4)})
    if not rows:
        sys.exit("ABORT: parsed zero videos from the catalogue")
    return rows


def build_model():
    videos = load("videos.json")
    sites = {s["n"]: s for s in load("sites.json")}
    countries = load("countries.json")

    # video id -> list of site names (primary = first wire encountered)
    wire = {}
    for site_name, lst in videos.items():
        for v in lst:
            if v.get("cr") != CREATOR_KEY:
                continue
            wire.setdefault(v["id"], []).append(site_name)

    catalogue = parse_catalogue()

    # region -> country -> site -> [videos]
    tree, unplaced = {}, []
    for vid in catalogue:
        targets = wire.get(vid["id"])
        if not targets:
            unplaced.append(vid)
            continue
        primary = targets[0]
        site = sites.get(primary)
        if site is None:
            unplaced.append(vid)
            continue
        region = site.get("region") or "Unsorted"
        country = countries.get(primary, region)
        node = tree.setdefault(region, {}).setdefault(country, {}).setdefault(
            primary, {"site": site, "videos": [], "also": []})
        node["videos"].append(vid)
        if len(targets) > 1:
            node["also"] = targets[1:]

    stats = {
        "videos": len(catalogue),
        "placed": len(catalogue) - len(unplaced),
        "unplaced": len(unplaced),
        "sites": sum(len(c) for r in tree.values() for c in r.values()),
        "countries": len({c for r in tree.values() for c in r}),
        "regions": len(tree),
    }
    return tree, unplaced, stats


def region_sort_key(name):
    return (REGION_ORDER.index(name) if name in REGION_ORDER else 99, name)


def e(s):
    return html.escape(str(s), quote=True)


def render_video(v):
    return f"""<a class="vid" href="{e(v['url'])}" target="_blank" rel="noopener">
  <div class="thumb"><img src="https://i.ytimg.com/vi/{e(v['id'])}/mqdefault.jpg" alt="" loading="lazy" decoding="async" width="320" height="180"><span class="play" aria-hidden="true"></span></div>
  <div class="vtitle">{e(v['title'])}</div>
</a>"""


def render_site(name, node):
    site = node["site"]
    cat = CAT_LABEL.get(site.get("cat"), (site.get("cat") or "").title())
    tier = site.get("tier")
    open_q = site.get("signal") == "open" and site.get("criteria")
    vids = "".join(render_video(v) for v in node["videos"])
    badge = '<span class="pill open">Look Closer</span>' if open_q else ""
    also = ""
    if node["also"]:
        also = ('<span class="also">also covers '
                + ", ".join(e(a) for a in node["also"]) + "</span>")
    return f"""<section class="site" data-site="{e(name.lower())}">
  <header class="site-head">
    <h4><a href="/sites/{slugify(name)}">{e(name)}</a></h4>
    <div class="meta"><span class="pill">{e(cat)}</span><span class="pill tier">Tier {e(tier)}</span>{badge}
      <span class="count">{len(node['videos'])} episode{"s" if len(node['videos']) != 1 else ""}</span>{also}</div>
  </header>
  <div class="grid">{vids}</div>
</section>"""


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --obsidian:#0D0D12;--charcoal:#16161D;--slate:#1E1E28;--stone:#2A2A35;
  --mist:#8A8A9A;--cloud:#C5C5D0;--ivory:#F0EEE9;--champagne:#C9A84C;
  --amber:#E8B960;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  --serif:'Fraunces',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
}
html{scroll-behavior:smooth;scroll-padding-top:132px}
body{font-family:var(--sans);background:var(--obsidian);color:var(--ivory);-webkit-font-smoothing:antialiased}
body::before{content:'';position:fixed;inset:0;opacity:.03;pointer-events:none;z-index:9999;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
::selection{background:var(--champagne);color:var(--obsidian)}
a{color:inherit}

/* ---------- masthead ---------- */
header.site{position:sticky;top:0;z-index:100;background:linear-gradient(180deg,rgba(13,13,18,.98),rgba(13,13,18,.92));backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(42,42,53,.5);padding:13px 26px;display:flex;align-items:center;gap:20px}
.brand{display:flex;align-items:center;gap:13px;text-decoration:none}
.brand svg{width:32px;height:32px;filter:drop-shadow(0 2px 8px rgba(201,168,76,.2))}
.brand b{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:-.4px}
.brand i{font-family:var(--serif);font-style:italic;font-size:12px;color:var(--champagne);opacity:.85;display:block;margin-top:1px}
.spacer{flex:1}
.toplinks{display:flex;gap:22px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.toplinks a{color:var(--cloud);text-decoration:none;transition:color .15s}
.toplinks a:hover,.toplinks a.active{color:var(--champagne)}

/* ---------- hero ---------- */
.hero{max-width:1280px;margin:0 auto;padding:72px 26px 40px;position:relative}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(900px 420px at 8% 0%,rgba(201,168,76,.10),transparent 62%);pointer-events:none;z-index:-1}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--champagne);font-weight:700;margin-bottom:20px}
h1{font-family:var(--serif);font-size:clamp(46px,7vw,86px);font-weight:600;line-height:.98;letter-spacing:-.025em;font-variation-settings:"opsz" 144}
.sub{font-family:var(--serif);font-style:italic;font-size:clamp(18px,2.1vw,24px);color:var(--cloud);margin-top:16px;max-width:62ch;line-height:1.45}
.byline{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist);margin-top:22px}
.byline a{color:var(--champagne);text-decoration:none;border-bottom:1px solid rgba(201,168,76,.4)}
.stats{display:flex;flex-wrap:wrap;gap:44px;margin-top:44px;padding-top:32px;border-top:1px solid rgba(42,42,53,.7)}
.stat b{font-family:var(--serif);font-variation-settings:"opsz" 144;font-size:44px;font-weight:600;color:var(--amber);display:block;line-height:1}
.stat span{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mist);display:block;margin-top:9px}

/* ---------- index bar ---------- */
.indexbar{position:sticky;top:59px;z-index:90;background:rgba(13,13,18,.95);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid rgba(42,42,53,.5);padding:12px 26px}
.indexinner{max-width:1280px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.jump{display:flex;gap:7px;flex-wrap:wrap;flex:1;min-width:260px}
.jump a{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--cloud);text-decoration:none;padding:5px 11px;border:1px solid rgba(42,42,53,.9);border-radius:7px;transition:all .15s;white-space:nowrap}
.jump a:hover{color:var(--champagne);border-color:rgba(201,168,76,.5);background:rgba(201,168,76,.07)}
.jump a em{font-style:normal;color:var(--mist);margin-left:5px}
#q{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--ivory);background:rgba(30,30,40,.85);border:1px solid rgba(42,42,53,1);border-radius:8px;padding:9px 13px;width:236px;outline:none;transition:border-color .15s}
#q::placeholder{color:var(--mist)}
#q:focus{border-color:rgba(201,168,76,.6)}
#hits{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mist);min-width:96px}

/* ---------- regions ---------- */
main{max-width:1280px;margin:0 auto;padding:8px 26px 110px}
.region{padding-top:64px}
.region-head{display:flex;align-items:baseline;gap:18px;margin-bottom:6px}
.region h2{font-family:var(--serif);font-size:clamp(30px,4vw,44px);font-weight:600;letter-spacing:-.02em;font-variation-settings:"opsz" 96}
.region-head .n{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--champagne)}
.region>.rule{height:1px;background:linear-gradient(90deg,rgba(201,168,76,.45),rgba(201,168,76,.04));margin:14px 0 4px}
.country{padding-top:38px}
.country h3{font-family:var(--mono);font-size:11.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--cloud);font-weight:600;padding-bottom:10px;border-bottom:1px solid rgba(42,42,53,.6)}
.country h3 em{font-style:normal;color:var(--mist);margin-left:8px;letter-spacing:.12em}

/* ---------- site block ---------- */
.site{padding:26px 0 6px}
.site-head{margin-bottom:15px}
.site-head h4{font-family:var(--serif);font-size:23px;font-weight:600;letter-spacing:-.012em;font-variation-settings:"opsz" 48;line-height:1.2}
.site-head h4 a{text-decoration:none;transition:color .15s}
.site-head h4 a:hover{color:var(--champagne)}
.meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-top:8px}
.pill{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--cloud);border:1px solid rgba(42,42,53,1);border-radius:99px;padding:3px 10px}
.pill.tier{color:var(--mist)}
.pill.open{color:var(--amber);border-color:rgba(232,185,96,.45);background:rgba(232,185,96,.07)}
.count,.also{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mist)}
.also::before{content:'·';margin-right:9px;color:var(--stone)}

/* ---------- video grid ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:20px}
.vid{text-decoration:none;display:block;group:card}
.thumb{position:relative;aspect-ratio:16/9;border-radius:9px;overflow:hidden;background:var(--charcoal);border:1px solid rgba(42,42,53,.9);transition:transform .22s cubic-bezier(.2,.7,.3,1),border-color .22s,box-shadow .22s}
.thumb img{width:100%;height:100%;object-fit:cover;display:block;opacity:.88;transition:opacity .22s,transform .5s cubic-bezier(.2,.7,.3,1)}
.play{position:absolute;left:50%;top:50%;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:rgba(13,13,18,.62);backdrop-filter:blur(3px);border:1px solid rgba(240,238,233,.28);opacity:0;transition:opacity .22s,transform .22s}
.play::after{content:'';position:absolute;left:17px;top:13px;border-left:15px solid var(--ivory);border-top:9px solid transparent;border-bottom:9px solid transparent}
.vid:hover .thumb{transform:translateY(-3px);border-color:rgba(201,168,76,.55);box-shadow:0 16px 34px rgba(0,0,0,.5)}
.vid:hover .thumb img{opacity:1;transform:scale(1.045)}
.vid:hover .play{opacity:1}
.vtitle{font-size:13.5px;line-height:1.45;color:var(--cloud);margin-top:11px;transition:color .15s}
.vid:hover .vtitle{color:var(--ivory)}

/* ---------- unplaced ---------- */
.unplaced{margin-top:96px;padding:34px 30px;border:1px solid rgba(201,168,76,.2);border-radius:14px;background:rgba(201,168,76,.03)}
.unplaced h2{font-family:var(--serif);font-size:30px;font-weight:600;letter-spacing:-.015em}
.unplaced p{font-size:15.5px;line-height:1.65;color:var(--cloud);margin-top:12px;max-width:74ch}
.unplaced .grid{margin-top:26px}
.hidden{display:none !important}
.empty{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist);padding:60px 0;text-align:center}

footer.site{border-top:1px solid rgba(42,42,53,.6);padding:34px 26px;text-align:center;font-size:13px;color:var(--mist)}
footer.site a{color:var(--champagne);text-decoration:none}

@media(max-width:720px){
  header.site{padding:11px 16px;gap:12px}
  .toplinks{gap:13px;font-size:10px}
  .brand i{display:none}
  .hero{padding:48px 18px 30px}
  .stats{gap:28px}
  .stat b{font-size:34px}
  .indexbar{top:55px;padding:10px 16px}
  #q{width:100%}
  main{padding:8px 18px 80px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
  .vtitle{font-size:12.5px}
}
@media(prefers-reduced-motion:reduce){*{transition:none !important;animation:none !important}html{scroll-behavior:auto}}
"""


LOGO_SVG = ('<svg viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<defs><linearGradient id="g" x1="50%" y1="0%" x2="50%" y2="100%">'
            '<stop offset="0%" stop-color="#F5DCA0"/><stop offset="100%" stop-color="#8E7234"/>'
            '</linearGradient></defs><polygon points="-36.71,-36.71 -12.28,-29.64 0,-84 12.28,-29.64 '
            '36.71,-36.71 29.64,-12.28 84,0 29.64,12.28 36.71,36.71 12.28,29.64 0,84 -12.28,29.64 '
            '-36.71,36.71 -29.64,12.28 -84,0 -29.64,-12.28" fill="url(#g)"/>'
            '<circle cx="0" cy="0" r="6" fill="#F5DCA0"/></svg>')

SCRIPT = """
(function(){
  var q=document.getElementById('q'), hits=document.getElementById('hits');
  var sites=[].slice.call(document.querySelectorAll('.site'));
  var vids=[].slice.call(document.querySelectorAll('.vid'));
  var groups=[].slice.call(document.querySelectorAll('.country,.region,.unplaced'));
  var total=vids.length;
  vids.forEach(function(v){ v.dataset.t=(v.textContent||'').toLowerCase(); });
  sites.forEach(function(s){ s.dataset.t=(s.textContent||'').toLowerCase(); });
  function reset(){
    vids.forEach(function(v){v.classList.remove('hidden')});
    sites.forEach(function(s){s.classList.remove('hidden')});
    groups.forEach(function(g){g.classList.remove('hidden')});
    hits.textContent=total+' episodes';
    var e=document.getElementById('noresults'); if(e) e.classList.add('hidden');
  }
  function run(){
    var term=q.value.trim().toLowerCase();
    if(!term){ reset(); return; }
    var shown=0;
    sites.forEach(function(s){
      var siteMatch=s.dataset.t.indexOf(term)>-1;
      var any=false;
      [].slice.call(s.querySelectorAll('.vid')).forEach(function(v){
        var ok=siteMatch||v.dataset.t.indexOf(term)>-1;
        v.classList.toggle('hidden',!ok); if(ok){any=true;shown++;}
      });
      s.classList.toggle('hidden',!any);
    });
    groups.forEach(function(g){
      var any=[].slice.call(g.querySelectorAll('.vid')).some(function(v){return !v.classList.contains('hidden')});
      g.classList.toggle('hidden',!any);
    });
    hits.textContent=shown+(shown===1?' episode':' episodes');
    var e=document.getElementById('noresults'); if(e) e.classList.toggle('hidden',shown>0);
  }
  q.addEventListener('input',run);
  q.addEventListener('keydown',function(ev){ if(ev.key==='Escape'){q.value='';run();q.blur();} });
  document.addEventListener('keydown',function(ev){
    if(ev.key==='/' && document.activeElement!==q){ ev.preventDefault(); q.focus(); }
  });
  reset();
})();
"""


def render_page(tree, unplaced, stats):
    regions = sorted(tree, key=region_sort_key)

    jump = "".join(
        f'<a href="#r-{slugify(r)}">{e(r)}<em>{sum(len(s["videos"]) for c in tree[r].values() for s in c.values())}</em></a>'
        for r in regions)
    if unplaced:
        jump += f'<a href="#unplaced">Not yet mapped<em>{len(unplaced)}</em></a>'

    body = []
    for r in regions:
        countries = sorted(tree[r], key=lambda c: (-sum(len(s["videos"]) for s in tree[r][c].values()), c))
        n_v = sum(len(s["videos"]) for c in tree[r].values() for s in c.values())
        n_s = sum(len(c) for c in tree[r].values())
        blocks = []
        for c in countries:
            site_items = sorted(tree[r][c].items(), key=lambda kv: (-len(kv[1]["videos"]), kv[0]))
            cv = sum(len(s["videos"]) for s in tree[r][c].values())
            blocks.append(
                f'<div class="country"><h3>{e(c)}<em>{cv} video{"s" if cv != 1 else ""} · '
                f'{len(site_items)} site{"s" if len(site_items) != 1 else ""}</em></h3>'
                + "".join(render_site(n, node) for n, node in site_items) + "</div>")
        body.append(
            f'<section class="region" id="r-{slugify(r)}">'
            f'<div class="region-head"><h2>{e(r)}</h2>'
            f'<span class="n">{n_v} episodes · {n_s} sites</span></div>'
            f'<div class="rule"></div>' + "".join(blocks) + "</section>")

    unplaced_html = ""
    if unplaced:
        unplaced_html = f"""<section class="unplaced" id="unplaced">
  <h2>Not yet on the map</h2>
  <p>{len(unplaced)} of Bernie's {stats['videos']} episodes have no site record in the Atlas yet. They are shown here rather than hidden, because this page is only as honest as the gaps it admits. Each one is a candidate: a site the Atlas does not carry, or an episode that has not been wired to a record it belongs to.</p>
  <div class="grid">{''.join(render_video(v) for v in unplaced)}</div>
</section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Ageless Rock — every episode, by place | The Ancient Atlas</title>
<meta name="description" content="Bernie Ong's Ageless Rock channel, {stats['videos']} narrated studies arranged by region, country and site instead of by upload date. {stats['sites']} sites across {stats['countries']} countries." />
<meta name="theme-color" content="#0D0D12" />
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png" />
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png" />
<link rel="canonical" href="https://theancientatlas.com/creators/ageless-rock" />
<meta property="og:type" content="profile" />
<meta property="og:site_name" content="The Ancient Atlas" />
<meta property="og:title" content="Ageless Rock : every episode, by place" />
<meta property="og:description" content="{stats['videos']} episodes across {stats['sites']} sites and {stats['countries']} countries, filed by place instead of by upload date." />
<meta property="og:url" content="https://theancientatlas.com/creators/ageless-rock" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preconnect" href="https://i.ytimg.com" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>{CSS}</style>
<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>

<header class="site">
  <a class="brand" href="/">{LOGO_SVG}<span><b>Ancient Atlas</b><i>A map of the deep past</i></span></a>
  <div class="spacer"></div>
  <nav class="toplinks"><a href="/">Atlas</a><a href="/library/">Library</a><a href="/creators/ageless-rock" class="active">Creator</a><a href="/contact.html">Contact</a></nav>
</header>

<div class="hero">
  <div class="eyebrow">Creator Index · 01</div>
  <h1>Ageless Rock</h1>
  <p class="sub">Every episode of <b>Ageless Rock</b>, filed by the place it studies rather than the day it was posted.</p>
  <p class="byline">{e(HANDLE)} · <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">Subscribe on YouTube ↗</a></p>
  <div class="stats">
    <div class="stat"><b>{stats['videos']}</b><span>Episodes</span></div>
    <div class="stat"><b>{stats['sites']}</b><span>Sites</span></div>
    <div class="stat"><b>{stats['countries']}</b><span>Countries</span></div>
    <div class="stat"><b>{stats['regions']}</b><span>Regions</span></div>
  </div>
</div>

<div class="indexbar">
  <div class="indexinner">
    <div class="jump">{jump}</div>
    <input id="q" type="search" placeholder="Search  ·  press /" autocomplete="off" spellcheck="false" aria-label="Search episodes" />
    <div id="hits"></div>
  </div>
</div>

<main>
{''.join(body)}
<div id="noresults" class="empty hidden">Nothing matches that.</div>
{unplaced_html}
</main>

<footer class="site">
  Episodes belong to <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">Ageless Rock</a>. Arranged by <a href="/">The Ancient Atlas</a>, hand-curated and ad-free.
</footer>

<script>{SCRIPT}</script>
</body>
</html>"""


def main():
    tree, unplaced, stats = build_model()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_page(tree, unplaced, stats), encoding="utf-8")
    print(f"  ✓ {OUT.relative_to(REPO_ROOT)}  ({OUT.stat().st_size:,} bytes)")
    print(f"    {stats['videos']} videos · {stats['placed']} placed · "
          f"{stats['unplaced']} unplaced")
    print(f"    {stats['sites']} sites · {stats['countries']} countries · "
          f"{stats['regions']} regions")
    print("Next step : python3 scripts/build-seo-pages.py")


if __name__ == "__main__":
    sys.exit(main())
