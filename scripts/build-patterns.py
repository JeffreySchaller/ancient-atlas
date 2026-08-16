#!/usr/bin/env python3
"""build-patterns.py — the comparative shelf.

WHY THIS EXISTS
---------------
The Atlas's whole claim is convergence: the same method turning up in cultures
that never met. Until now that claim only ever appeared as prose in the Library
or as a strip on a creator study. There was nowhere to put the evidence itself.

So comparison got stuffed into the site model, and it lied. An earlier batch
(add-machining-criterion-architecture.py) deliberately wired one Bazda Caves
video onto Longyou, Longmen, Kotukal and San Andrea Priù as a cross-reference
for the machining criterion. The intent was right. The presentation was not:
Bernie Ong opened the China card and got a Türkiye video, because a
cross-reference rendered as that site's own walkthrough.

A pattern page is where that comparison always belonged. The wire comes back
here, labelled as what it is.

WHAT IT BUILDS
--------------
/patterns/<key>/index.html for each entry in data/patterns.json, where <key> is
one of the seven criteria already carried by sites.json. Nothing here invents a
taxonomy — the criteria are the patterns, and the page is the criterion's own
page: the claim, the comparative videos that argue it, and every site in the
Atlas that carries it, grouped by country so the spread is the argument.

Idempotent. Run from repo root, then build-seo-pages.py.
"""
import html
import json
import re
import unicodedata
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUT = REPO / "public" / "patterns"

VALID = {"precision", "polygonal", "scale", "hardness", "stratigraphy", "geometry", "machining"}


def e(s):
    return html.escape(str(s), quote=True)


def load(name):
    return json.loads((DATA / name).read_text())


sites = load("sites.json")
countries = load("countries.json")
creators = load("creators.json")
patterns = load("patterns.json")
world = load("world-outline.json")
site_pos = {x["n"]: (x["lat"], x["lng"]) for x in sites}

CSS = """
:root{--obsidian:#0B0B0F;--charcoal:#14141A;--slate:#1C1C24;--stone:#2A2A35;
--champagne:#C9A84C;--amber:#E8B960;--ivory:#F0EEE9;--cloud:#C5C5D0;--mist:#8A8A9A;
--font-serif:'Fraunces',Georgia,serif;--font-sans:'Inter',-apple-system,sans-serif;
--font-mono:'JetBrains Mono',ui-monospace,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--obsidian);color:var(--ivory);font-family:var(--font-sans);
-webkit-font-smoothing:antialiased;line-height:1.6}
header{position:sticky;top:0;z-index:20;background:rgba(11,11,15,.92);backdrop-filter:blur(18px);
border-bottom:1px solid rgba(42,42,53,.5);padding:13px 22px;display:flex;align-items:center;
justify-content:space-between;gap:14px}
header a.home{color:var(--ivory);text-decoration:none;font-family:var(--font-mono);font-size:11px;
letter-spacing:.14em;text-transform:uppercase;display:flex;align-items:center;gap:9px}
header a.home span{color:var(--champagne)}
header nav a{color:var(--mist);text-decoration:none;font-family:var(--font-mono);font-size:10.5px;
letter-spacing:.12em;text-transform:uppercase;margin-left:16px}
header nav a:hover{color:var(--champagne)}
main{max-width:860px;margin:0 auto;padding:34px 22px 90px}
.kicker{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
color:var(--champagne);margin:0 0 16px;display:flex;align-items:center;gap:14px}
.glyph{color:var(--champagne);flex:none}
h1{font-family:var(--font-serif);font-weight:600;font-size:clamp(28px,5vw,44px);line-height:1.1;
margin:0 0 14px;letter-spacing:-.01em}
.claim{font-size:clamp(15.5px,2vw,18px);color:var(--cloud);max-width:66ch;margin:0 0 22px}
.ledger{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--stone);
border-bottom:1px solid var(--stone);margin:0 0 44px}
.ledger div{flex:1 1 130px;padding:15px 16px 14px;border-right:1px solid var(--stone)}
.ledger div:last-child{border-right:0}
.ledger b{display:block;font-family:var(--font-mono);font-size:23px;color:var(--amber);
font-weight:500;line-height:1}
.ledger span{display:block;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.14em;
text-transform:uppercase;color:var(--mist);margin-top:7px}
h2{font-family:var(--font-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
color:var(--champagne);font-weight:400;margin:0 0 18px;padding-bottom:11px;
border-bottom:1px solid var(--stone)}
.essay p{max-width:64ch;color:var(--cloud);margin:0 0 17px}
.essay p+p{margin-top:0}
section{margin:0 0 52px}
.vids{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:16px}
.vid{display:block;text-decoration:none;color:inherit;border:1px solid var(--stone);
border-radius:11px;overflow:hidden;background:var(--charcoal);transition:border-color .18s,transform .18s}
.vid:hover{border-color:rgba(201,168,76,.45);transform:translateY(-2px)}
.vid img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;opacity:.88}
.vid:hover img{opacity:1}
.vid .m{padding:11px 13px 13px}
.vid .t{font-size:13.5px;line-height:1.4;color:var(--ivory);display:block}
.vid .c{font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
color:var(--champagne);margin-top:7px;display:block}
.vid .x{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.07em;color:var(--mist);
margin-top:6px;display:block}
.mapwrap{position:relative;border:1px solid var(--stone);border-radius:12px;overflow:hidden;
background:linear-gradient(180deg,#0E0E14,#0A0A0F);margin:0 0 14px}
.mapwrap svg{display:block;width:100%;height:auto}
.land{fill:#1B1B24;stroke:#262632;stroke-width:.8;vector-effect:non-scaling-stroke}
.dot{fill:var(--amber)}
.halo{fill:none;stroke:var(--champagne);stroke-opacity:.5;stroke-width:1.6;vector-effect:non-scaling-stroke}
.maplegend{font-family:var(--font-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);display:flex;justify-content:space-between;gap:12px;margin:0 0 40px;flex-wrap:wrap}
.vid .mini{border-top:1px solid var(--stone);background:#0A0A0F}
.vid .mini .land{fill:#23232E;stroke:#30303D}
.vid .mini svg{display:block;width:100%;height:auto}
.country{margin:0 0 22px}
.country h3{font-family:var(--font-mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
color:var(--mist);font-weight:400;margin:0 0 8px}
.country ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.country li a{display:inline-block;font-size:13.5px;color:var(--cloud);text-decoration:none;
border:1px solid var(--stone);border-radius:999px;padding:5px 12px;transition:.15s}
.country li a:hover{border-color:rgba(201,168,76,.5);color:var(--ivory);background:rgba(201,168,76,.06)}
.note{font-family:var(--font-mono);font-size:11px;line-height:1.75;color:var(--mist);
border-left:2px solid var(--stone);padding:2px 0 2px 15px;max-width:62ch}
.siblings{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.siblings a{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--cloud);text-decoration:none;border:1px solid var(--stone);border-radius:999px;padding:6px 13px}
.siblings a:hover{border-color:rgba(201,168,76,.5);color:var(--ivory)}
.siblings a.off{opacity:.42;pointer-events:none}
details{border-top:1px solid var(--stone);border-bottom:1px solid var(--stone);padding:0}
summary{cursor:pointer;list-style:none;padding:15px 0;font-family:var(--font-mono);font-size:11px;
letter-spacing:.16em;text-transform:uppercase;color:var(--champagne);display:flex;
align-items:center;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:15px;color:var(--mist)}
details[open] summary::after{content:"\2212"}
details[open] summary{border-bottom:1px solid var(--stone)}
details .essay,details p:first-of-type{margin-top:17px}
details p:last-child{margin-bottom:17px}
footer{border-top:1px solid var(--stone);margin-top:60px;padding:22px 0 0;font-family:var(--font-mono);
font-size:10.5px;letter-spacing:.06em;color:var(--mist)}
footer a{color:var(--cloud);text-decoration:none}
footer a:hover{color:var(--champagne)}
@media(max-width:560px){main{padding:34px 17px 70px}.ledger div{flex:1 1 50%}}
"""



# ---------------------------------------------------------------------------
# GLYPHS
# Lifted verbatim from the "six properties" list in library/megaliths.html.
# That list was already this taxonomy - fitted joints, hardness, mass,
# interlock, layers, geometry - drawn before there was a Patterns shelf to put
# it on. Reusing the exact paths means the Library and this section speak one
# visual language rather than two.
# `machining` is the only one with no glyph, because it was the seventh
# criterion, added later. Drawn to match: three parallel striations and a bore.
# ---------------------------------------------------------------------------
GLYPHS = {
    "precision": '<path d="M3 19 L3 8 L7 5 L11 5 L13 9 L13 19 Z"/>'
                 '<path d="M21 19 L21 6 L17 6 L13 9 L13 19 Z"/>',
    "hardness":  '<path d="M9 3 L15 3 L15 14 L12 21 L9 14 Z"/><path d="M9 7 L15 7"/>',
    "scale":     '<path d="M4 8 L12 4 L20 8 L20 18 L12 22 L4 18 Z"/>'
                 '<path d="M4 8 L12 12 L20 8 M12 12 L12 22"/>',
    "polygonal": '<path d="M10 2 L14 2 L15.5 5 L13 7 L9 7 L8.5 4 Z"/>'
                 '<path d="M3 13 L7 12 L9 15 L7 19 L3 18 L2 15 Z"/>'
                 '<path d="M16 14 L20 13 L22 16 L20 20 L17 20 L15 17 Z"/>',
    "stratigraphy": '<path d="M3 5 L21 5" stroke-width="0.7" opacity="0.5"/>'
                    '<path d="M3 10 L21 10" stroke-width="0.9" opacity="0.7"/>'
                    '<path d="M3 15 L21 15" stroke-width="1.2" opacity="0.85"/>'
                    '<path d="M3 20 L21 20" stroke-width="1.7"/>',
    "geometry":  '<circle cx="9" cy="12" r="7"/><circle cx="15" cy="12" r="7"/>',
    "machining": '<path d="M3 8 C8 6.4, 16 6.4, 21 8"/>'
                 '<path d="M3 12 C8 10.4, 16 10.4, 21 12"/>'
                 '<path d="M3 16 C8 14.4, 16 14.4, 21 16"/>'
                 '<circle cx="17.6" cy="19.4" r="2.1"/>',
}


def glyph(key, size=26):
    g = GLYPHS.get(key)
    if not g:
        return ""
    return (f'<svg class="glyph" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round" '
            f'stroke-linecap="round" aria-hidden="true">{g}</svg>')


def minimap(names, r=7.0, halo=True, window=None):
    """Equirectangular world with a dot per site. The projection is the crude
    one on purpose — this is a spread indicator, not a chart to measure off.

    `window` zooms to a regional box around the sites. A whole globe at card
    width is 190 px across; one dot on it is unreadable. A 380-wide window is
    about a continent, which is the scale at which "where is this" answers
    itself."""
    W, H = 1000.0, 500.0
    pts = []
    for n in names:
        if n in site_pos:
            lat, lng = site_pos[n]
            pts.append(((lng + 180.0) / 360.0 * W, (90.0 - lat) / 180.0 * H))

    if window and pts:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        vw = float(window)
        vh = vw * 0.52
        vx = min(max(cx - vw / 2, 0.0), W - vw)
        vy = min(max(cy - vh / 2, 30.0), H - vh - 60.0)
        view = f"{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}"
        scale = vw / W                      # keep dots the same size on screen
    else:
        view = "0 60 1000 330"              # Antarctica holds no sites
        scale = 1.0

    dots = []
    for x, y in pts:
        rr = r * scale
        if halo:
            dots.append(f'<circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="{rr*2.1:.1f}"/>')
        dots.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}"/>')

    return (f'<svg viewBox="{view}" role="img" aria-label="Map, {len(pts)} sites marked" '
            f'preserveAspectRatio="xMidYMid slice">'
            f'<use class="land" href="#landmass"/>{"".join(dots)}</svg>')


def land_defs():
    return ('<svg width="0" height="0" aria-hidden="true" focusable="false" '
            'style="position:absolute">'
            f'<defs><path id="landmass" d="{world["path"]}"/></defs></svg>')


def video_card(v, sites_by_name):
    cr = creators.get(v.get("cr"), {})
    name = cr.get("name", v.get("cr", ""))
    note = v.get("note", "")
    return (
        f'<a class="vid" href="https://www.youtube.com/watch?v={e(v["id"])}" target="_blank" rel="noopener">'
        f'<img src="https://i.ytimg.com/vi/{e(v["id"])}/mqdefault.jpg" alt="" loading="lazy" decoding="async">'
        f'<span class="m"><span class="t">{e(v["title"])}</span>'
        f'<span class="c">{e(name)}</span>'
        + (f'<span class="x">{e(note)}</span>' if note else "")
        + "</span>"
        # a per-card map only when the coverage has actually been indexed —
        # guessing which sites a comparison visits would be exactly the kind of
        # soft claim this section exists to avoid
        + (f'<span class="mini">{minimap(v["sites"], r=9, halo=True, window=360)}</span>'
           if v.get("sites") else "")
        + "</a>"
    )


def build(key, spec, order):
    carriers = [s for s in sites if key in (s.get("criteria") or [])]
    if not carriers:
        sys.exit(f"ABORT: no site in sites.json carries criterion {key!r} — "
                 "refusing to publish a pattern page with no evidence")

    by_country = {}
    for s in carriers:
        by_country.setdefault(countries.get(s["n"], "Unplaced"), []).append(s["n"])
    n_countries = len(by_country)

    vids = spec.get("videos", [])
    ledger = (
        f'<div><b>{len(carriers)}</b><span>sites carry it</span></div>'
        f'<div><b>{n_countries}</b><span>countries</span></div>'
        f'<div><b>{len(vids)}</b><span>comparisons</span></div>'
    )

    country_html = ""
    for c in sorted(by_country):
        lis = "".join(
            f'<li><a href="/sites/{slug(n)}.html">{e(n)}</a></li>'
            for n in sorted(by_country[c])
        )
        country_html += f'<div class="country"><h3>{e(c)}</h3><ul>{lis}</ul></div>'

    sibs = "".join(
        f'<a class="{"" if k in order and k != key else ("off" if k == key else "off")}" '
        f'href="/patterns/{k}/">{e(patterns[k]["name"])}</a>'
        if k != key and patterns[k].get("videos")
        else f'<a class="off" href="/patterns/{k}/">{e(patterns[k]["name"])}</a>'
        for k in order
    )

    essay = "".join(f"<p>{e(p)}</p>" for p in spec["essay"])
    vids_html = "".join(video_card(v, None) for v in vids)

    hero = minimap([x["n"] for x in carriers])
    legend = (
        f'<span>{len(carriers)} sites · {n_countries} countries</span>'
        f'<span>Equirectangular · every dot is a site in the Atlas</span>'
    )

    title = f'{spec["name"]}: a pattern across {n_countries} countries | The Ancient Atlas'
    desc = spec["claim"]

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="/favicon-32.png" type="image/png">
<link rel="canonical" href="https://theancientatlas.com/patterns/{key}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The Ancient Atlas">
<meta property="og:title" content="{e(spec['name'])} · The Ancient Atlas">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="https://theancientatlas.com/patterns/{key}/">
<meta property="og:image" content="https://theancientatlas.com/patterns/og/{key}.png?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(spec['name'])} on The Ancient Atlas: {len(carriers)} sites in {n_countries} countries, marked on a world map.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(spec['name'])} · The Ancient Atlas">
<meta name="twitter:description" content="{e(spec['claim'])}">
<meta name="twitter:image" content="https://theancientatlas.com/patterns/og/{key}.png?v=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
{land_defs()}
<header>
  <a class="home" href="/"><span>✦</span> The Ancient Atlas</a>
  <nav><a href="/">Atlas</a><a href="/library/">Library</a><a href="/creators/">Studies</a><a href="/sites/">Sites</a></nav>
</header>
<main>
  <p class="kicker">{glyph(key, 40)}<span>Patterns · {e(spec['index'])} · {e(spec['name'])}</span></p>
  <h1>{e(spec['headline'])}</h1>
  <p class="claim">{e(spec['claim'])}</p>

  <div class="mapwrap">{hero}</div>
  <p class="maplegend">{legend}</p>

  <section>
    <h2>Watch the comparison · {len(vids)} studies</h2>
    <div class="vids">{vids_html}</div>
    <p class="note" style="margin-top:18px">{e(spec['videos_note'])}</p>
  </section>

  <section class="essay">
    <details>
      <summary>What the pattern is, and what it is not: the argument in full</summary>
      {essay}
    </details>
  </section>

  <section>
    <h2>Every site in the Atlas that carries it · {len(carriers)} across {n_countries} countries</h2>
    {country_html}
  </section>

  <section>
    <h2>The other patterns</h2>
    <div class="siblings">{sibs}</div>
    <p class="note" style="margin-top:14px">Dimmed patterns are tagged across the Atlas but have no
comparative study written yet.</p>
  </section>

  <footer>
    The Ancient Atlas, a hand-curated map of the deep past.
    <a href="/">Map</a> · <a href="/library/">Library</a> · <a href="/creators/">Creator Studies</a> ·
    <a href="/contribute.html">Contribute</a>
  </footer>
</main>
</body>
</html>
"""
    d = OUT / key
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(doc)
    return len(carriers), n_countries, len(vids)


def slug(name):
    """MUST match build-seo-pages.slugify exactly, or every site link 404s.
    Copied rather than imported because these builders run standalone."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("ı", "i").replace("ħ", "h").replace("ø", "o").replace("ß", "ss")
    s = re.sub(r"[\u2018\u2019']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "site"



def build_index(order, built_keys):
    """The shelf's front door. Every criterion is listed whether or not it has
    a study yet — the unwritten ones are the honest backlog, and showing the
    counts makes the gap legible rather than hidden."""
    cards = []
    for k in order:
        spec = patterns[k]
        carriers = [x for x in sites if k in (x.get("criteria") or [])]
        cs = {countries.get(x["n"], "?") for x in carriers}
        live = k in built_keys
        nvid = len(spec.get("videos") or [])
        head = spec.get("headline") or f'{spec["name"]}: not yet written'
        blurb = spec.get("claim") or (
            f'{len(carriers)} sites across {len(cs)} countries carry this criterion. '
            "No comparative study written yet."
        )
        inner = (
            f'<p class="pk">{glyph(k, 34)}<span>{e(spec["index"])} · {e(spec["name"])}</span></p>'
            f'<h3>{e(head)}</h3>'
            f'<p class="pb">{e(blurb)}</p>'
            f'<p class="pm">{len(carriers)} sites · {len(cs)} countries'
            + (f' · {nvid} studies' if nvid else " · no study yet") + "</p>"
        )
        cards.append(
            f'<a class="pcard" href="/patterns/{k}/">{inner}</a>' if live
            else f'<div class="pcard off">{inner}</div>'
        )

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Patterns: the same idea, in places that never met | The Ancient Atlas</title>
<meta name="description" content="Seven engineering signatures tracked across 618 ancient sites, each with the comparative studies that argue it. The Atlas organised by method rather than by map.">
<link rel="icon" href="/favicon-32.png" type="image/png">
<link rel="canonical" href="https://theancientatlas.com/patterns/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Ancient Atlas">
<meta property="og:title" content="Patterns · The Ancient Atlas">
<meta property="og:description" content="Seven engineering signatures tracked across 618 ancient sites, each with the comparative studies that argue it.">
<meta property="og:url" content="https://theancientatlas.com/patterns/">
<meta property="og:image" content="https://theancientatlas.com/patterns/og/index.png?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Patterns on The Ancient Atlas: seven engineering signatures, every carrier site marked on a world map.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Patterns · The Ancient Atlas">
<meta name="twitter:description" content="Seven engineering signatures tracked across 618 ancient sites, each with the comparative studies that argue it.">
<meta name="twitter:image" content="https://theancientatlas.com/patterns/og/index.png?v=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}}
.pcard{{display:block;text-decoration:none;color:inherit;border:1px solid var(--stone);
border-radius:12px;padding:19px 20px 17px;background:var(--charcoal);transition:.18s}}
.pcard:hover{{border-color:rgba(201,168,76,.5);transform:translateY(-2px)}}
.pcard.off{{opacity:.5}}
.pk{{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
color:var(--champagne);margin:0 0 12px;display:flex;align-items:center;gap:13px}}
.pcard h3{{font-family:var(--font-serif);font-weight:600;font-size:20px;line-height:1.2;margin:0 0 9px}}
.pb{{font-size:13.5px;line-height:1.5;color:var(--cloud);margin:0 0 12px;
display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;
overflow:hidden;text-overflow:ellipsis}}
.pm{{font-family:var(--font-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
color:var(--mist);margin:0}}
</style>
<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<header>
  <a class="home" href="/"><span>✦</span> The Ancient Atlas</a>
  <nav><a href="/">Atlas</a><a href="/library/">Library</a><a href="/creators/">Studies</a><a href="/sites/">Sites</a></nav>
</header>
<main>
  <p class="kicker">Patterns</p>
  <h1>The same idea, in places that never met.</h1>
  <p class="claim">The Atlas is normally sorted by where things are. This shelf sorts it by how they
were made: seven engineering signatures tracked across 618 sites, each with the studies that
argue it. Sort by country and these never appear together. Sort by method and you are looking
at one idea.</p>
  <div class="pgrid">{"".join(cards)}</div>
  <footer>
    The Ancient Atlas, a hand-curated map of the deep past.
    <a href="/">Map</a> · <a href="/library/">Library</a> · <a href="/creators/">Creator Studies</a> ·
    <a href="/contribute.html">Contribute</a>
  </footer>
</main>
</body>
</html>
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(doc)
    return len(built_keys)

order = [k for k in ("machining", "precision", "polygonal", "geometry",
                     "scale", "hardness", "stratigraphy") if k in patterns]

# keys beginning with "_" are notes to whoever edits the file next, not criteria
patterns = {k: v for k, v in patterns.items() if not k.startswith("_")}
bad = set(patterns) - VALID
if bad:
    sys.exit(f"ABORT: patterns.json names criteria that are not in the site taxonomy: {sorted(bad)}")

built = 0
for key in order:
    spec = patterns[key]
    if not spec.get("videos"):
        continue
    n, c, v = build(key, spec, order)
    print(f"  ✓ /patterns/{key}/  {n} sites · {c} countries · {v} comparisons")
    built += 1

if not built:
    sys.exit("ABORT: nothing built — every pattern in patterns.json has an empty video list")

live = [k for k in order if patterns[k].get("videos")]
build_index(order, set(live))
print(f"  ✓ /patterns/  index · {len(live)} live, {len(order) - len(live)} awaiting a study")
print(f"{built} pattern page(s) written to public/patterns/")
