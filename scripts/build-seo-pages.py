#!/usr/bin/env python3
"""
build-seo-pages.py — static SEO page generator (2026-07-13)

WHY: theancientatlas.com is a single-page app; all 612 sites live inside JS
consts, so Google indexes ~1 page and a site: query returns nothing. This
generator turns the data layer into crawlable HTML — no infra change, Netlify
serves it as static files.

EMITS (all under public/):
  sites/<slug>.html   one page per site: unique <title>, meta description,
                      canonical, OG/Twitter tags, the site's desc as body
                      text, Look Closer criteria, walkthrough video links,
                      3 nearest sites (internal links), "Open in the Atlas"
                      deep link (/?site=NAME — already supported by the map),
                      schema.org JSON-LD (TouristAttraction + geo + videos)
  sites/index.html    A–Z directory grouped by region (crawl hub)
  sitemap.xml         root + static pages + library + all site pages
  robots.txt          allow-all + sitemap pointer

Idempotent: output is fully regenerated each run. Run AFTER build.py
(build.py invokes this automatically once the pipeline hook is in place).
"""
import html
import json
import math
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
OUT = REPO_ROOT / "public" / "sites"
BASE = "https://theancientatlas.com"

CRITERIA_LABELS = {
    "precision": "stones fitted without mortar, almost no gap",
    "hardness": "stone harder than steel",
    "scale": "stones heavier than the period's tools could lift",
    "polygonal": "polygonal, interlocking masonry",
    "stratigraphy": "dating rests on thin stratigraphic evidence",
    "geometry": "geometry beyond period explanation",
    "machining": "tool marks suggesting advanced machining",
}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def slugify(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("ı", "i").replace("ħ", "h").replace("ø", "o").replace("ß", "ss")
    s = re.sub(r"[''']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "site"


def era_label(year):
    if year is None:
        return None
    y = int(year)
    return f"c. {abs(y):,} BCE" if y < 0 else f"c. {y} CE"


def haversine(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


CSS = """
:root{--bg:#0D0D12;--panel:#15151C;--ivory:#E8E4D8;--mist:#8A8A9A;--champagne:#C9A84C;--line:rgba(201,168,76,.25)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ivory);font:16px/1.65 Georgia,'Times New Roman',serif;padding:0 20px 60px}
a{color:var(--champagne)}
header{max-width:760px;margin:0 auto;padding:22px 0;border-bottom:1px solid var(--line)}
header a{font-family:Georgia,serif;font-size:20px;color:var(--ivory);text-decoration:none}
header a span{color:var(--champagne)}
main{max-width:760px;margin:0 auto}
h1{font-size:34px;line-height:1.2;margin:28px 0 10px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px;font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mist)}
.badges span{border:1px solid var(--line);border-radius:6px;padding:4px 9px}
.desc{font-size:17px;margin:0 0 18px;color:var(--ivory)}
.meta{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--mist);margin:0 0 26px}
.lookcloser{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:14px 16px;margin:0 0 26px;font-size:14.5px;color:var(--mist)}
.lookcloser b{color:var(--champagne);font-weight:600}
.cta{display:inline-block;background:linear-gradient(135deg,#E8B960,#C9A84C);color:#0D0D12;font-family:ui-monospace,Menlo,monospace;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:13px 22px;border-radius:9px;text-decoration:none;margin:0 0 34px}
h2{font-size:14px;font-family:ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--champagne);margin:34px 0 14px}
.vid{display:flex;gap:14px;align-items:center;border:1px solid rgba(255,255,255,.08);border-radius:10px;background:var(--panel);padding:10px;margin:0 0 10px;text-decoration:none}
.vid img{width:132px;height:74px;object-fit:cover;border-radius:6px;flex-shrink:0}
.vid .t{color:var(--ivory);font-size:15px;line-height:1.35}
.vid .c{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--mist);margin-top:5px}
ul.nearby{list-style:none}
ul.nearby li{margin:0 0 8px;font-size:15px}
ul.nearby .d{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--mist);margin-left:8px}
footer{max-width:760px;margin:44px auto 0;padding-top:18px;border-top:1px solid var(--line);font-size:13px;color:var(--mist)}
.dir h2{margin-top:38px}
.dir ul{list-style:none;columns:2;column-gap:34px}
.dir li{margin:0 0 7px;font-size:15px;break-inside:avoid}
.dir .co{color:var(--mist);font-size:12.5px;margin-left:6px}
@media(max-width:560px){.dir ul{columns:1}h1{font-size:27px}}
""".strip()


def page_shell(title, desc_meta, canonical, og_image, body, jsonld=None):
    ld = f'<script type="application/ld+json">{jsonld}</script>\n' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc_meta)}" />
<link rel="canonical" href="{canonical}" />
<meta name="theme-color" content="#0D0D12" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="The Ancient Atlas" />
<meta property="og:title" content="{html.escape(title)}" />
<meta property="og:description" content="{html.escape(desc_meta)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
<style>{CSS}</style>
<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
{ld}</head>
<body>
<header><a href="/"><span>✦</span> The Ancient Atlas</a></header>
<main>
{body}
</main>
<footer>The Ancient Atlas — a hand-curated map of the deep past. <a href="/sites/">All sites</a> · <a href="/library/">Library</a> · <a href="/contribute.html">Contribute</a></footer>
</body>
</html>
"""


def truncate(text, n=155):
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def main():
    sites = load("sites.json")
    videos = load("videos.json")
    creators = load("creators.json")
    countries = load("countries.json")
    eras = load("eras.json")
    civs = load("civilizations.json")
    cats = load("categories.json")

    OUT.mkdir(exist_ok=True)

    # slugs (collision-safe, deterministic)
    slugs, seen = {}, set()
    for s in sites:
        base = slugify(s["n"])
        slug, i = base, 2
        while slug in seen:
            slug, i = f"{base}-{i}", i + 1
        seen.add(slug)
        slugs[s["n"]] = slug

    today = date.today().isoformat()
    urls = [f"{BASE}/", f"{BASE}/contact.html", f"{BASE}/contribute.html", f"{BASE}/sites/"]
    for lib in sorted((REPO_ROOT / "public" / "library").glob("*.html")):
        urls.append(f"{BASE}/library/{lib.name}" if lib.name != "index.html" else f"{BASE}/library/")

    count = 0
    for s in sites:
        name, slug = s["n"], slugs[s["n"]]
        country = countries.get(name)
        era = era_label(eras.get(name))
        civ = civs.get(name)
        cat = cats.get(s.get("cat"), {}).get("label", (s.get("cat") or "").title())
        wires = videos.get(name, [])
        canonical = f"{BASE}/sites/{slug}.html"
        place_bits = [b for b in (country, s.get("region")) if b]
        place = place_bits[0] if place_bits else ""
        title = f"{name} — {place} | The Ancient Atlas" if place else f"{name} | The Ancient Atlas"
        desc_meta = truncate(s.get("desc") or f"{name}: ancient site on The Ancient Atlas.")
        og_image = f"https://i.ytimg.com/vi/{wires[0]['id']}/hqdefault.jpg" if wires else f"{BASE}/og-image.png"

        badges = "".join(
            f"<span>{html.escape(b)}</span>"
            for b in [cat, s.get("region"), country if country != s.get("region") else None, era, civ]
            if b
        )

        look = ""
        if s.get("signal") == "open" and s.get("criteria"):
            pts = [CRITERIA_LABELS.get(c, c) for c in s["criteria"]]
            look = (
                '<div class="lookcloser"><b>Look Closer</b> — this site carries open questions: '
                + html.escape("; ".join(pts)) + ".</div>"
            )

        vid_html = ""
        if wires:
            items = []
            for v in wires:
                cr = creators.get(v.get("cr"), {}).get("name", "YouTube")
                items.append(
                    f'<a class="vid" href="https://www.youtube.com/watch?v={v["id"]}" rel="noopener">'
                    f'<img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" alt="{html.escape(v["title"])}" loading="lazy" />'
                    f'<span><span class="t">{html.escape(v["title"])}</span>'
                    f'<span class="c">{html.escape(cr)}</span></span></a>'
                )
            vid_html = f"<h2>Walkthrough videos ({len(wires)})</h2>" + "".join(items)

        near = sorted((o for o in sites if o["n"] != name), key=lambda o: haversine(s, o))[:3]
        near_html = "<h2>Nearby sites</h2><ul class=\"nearby\">" + "".join(
            f'<li><a href="/sites/{slugs[o["n"]]}.html">{html.escape(o["n"])}</a>'
            f'<span class="d">{haversine(s, o):.0f} km</span></li>'
            for o in near
        ) + "</ul>"

        ld = {
            "@context": "https://schema.org",
            "@type": "TouristAttraction",
            "name": name,
            "description": s.get("desc", ""),
            "url": canonical,
            "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lng"]},
        }
        if country:
            ld["containedInPlace"] = {"@type": "Country", "name": country}
        if wires:
            ld["subjectOf"] = [
                {
                    "@type": "VideoObject",
                    "name": v["title"],
                    "url": f"https://www.youtube.com/watch?v={v['id']}",
                    "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg",
                }
                for v in wires
            ]

        body = f"""<h1>{html.escape(name)}</h1>
<div class="badges">{badges}</div>
<p class="desc">{html.escape(s.get('desc') or '')}</p>
<p class="meta">{s['lat']:.4f}°, {s['lng']:.4f}°</p>
{look}
<a class="cta" href="/?site={quote(name)}">Open in the Atlas map →</a>
{vid_html}
{near_html}"""

        (OUT / f"{slug}.html").write_text(
            page_shell(title, desc_meta, canonical, og_image, body, json.dumps(ld, ensure_ascii=False)),
            encoding="utf-8",
        )
        urls.append(canonical)
        count += 1

    # directory page (crawl hub), grouped by region
    by_region = {}
    for s in sites:
        by_region.setdefault(s.get("region") or "Other", []).append(s)
    sections = []
    for region in sorted(by_region):
        rows = "".join(
            f'<li><a href="/sites/{slugs[s["n"]]}.html">{html.escape(s["n"])}</a>'
            + (f'<span class="co">{html.escape(countries[s["n"]])}</span>' if countries.get(s["n"]) else "")
            + "</li>"
            for s in sorted(by_region[region], key=lambda x: x["n"])
        )
        sections.append(f"<h2>{html.escape(region)} ({len(by_region[region])})</h2><ul>{rows}</ul>")
    dir_body = (
        f"<h1>All {count} ancient sites</h1>"
        '<p class="desc">Every site on The Ancient Atlas, grouped by region. '
        'Each page includes the site’s story, coordinates, and curated walkthrough videos.</p>'
        '<div class="dir">' + "".join(sections) + "</div>"
    )
    (OUT / "index.html").write_text(
        page_shell(
            f"All {count} Ancient Sites — Directory | The Ancient Atlas",
            f"Directory of all {count} ancient sites on The Ancient Atlas: megalithic, rock-cut, pyramid, underground and more — with curated walkthrough videos.",
            f"{BASE}/sites/",
            f"{BASE}/og-image.png",
            dir_body,
        ),
        encoding="utf-8",
    )

    # sitemap + robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{html.escape(u)}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    (REPO_ROOT / "public" / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (REPO_ROOT / "public" / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8"
    )

    # llms.txt — orientation file for AI/LLM crawlers (llmstxt.org convention)
    n_wires = sum(len(v) for v in videos.values())
    llms = f"""# The Ancient Atlas

> A hand-curated interactive map of {count} ancient sites — megalithic, pyramid, \
rock-cut, underground, tombs and geoglyphs — each with an independently verified \
location, a concise evidence-focused description, and {n_wires} curated field \
walkthrough videos from {len(creators)} researchers and channels. Free, ad-free, \
no signup. Sites with open engineering questions (precision joints in stone harder \
than steel, blocks beyond period lifting capacity, thin stratigraphic dating) carry \
a "Look Closer" flag presenting both conventional and independent readings.

## Site pages

- [All {count} sites, grouped by region]({BASE}/sites/): every site links to its own \
page with description, coordinates, era, culture, walkthrough videos and nearby sites.
- [Interactive map]({BASE}/): the full atlas; deep-link any site with /?site=NAME.
- [Sitemap]({BASE}/sitemap.xml)

## Structured data

- [sites.json]({BASE}/data/sites.json): all sites with name, lat/lng, category, region, \
tier, description, and open-question criteria.
- [videos.json]({BASE}/data/videos.json): curated walkthrough videos per site (YouTube IDs).
- [creators.json]({BASE}/data/creators.json): the {len(creators)} featured channels.
- [countries.json]({BASE}/data/countries.json), [eras.json]({BASE}/data/eras.json), \
[civilizations.json]({BASE}/data/civilizations.json): auxiliary facts keyed by site name.

## About

- [Contact]({BASE}/contact.html): corrections and site suggestions welcome.
- [Library]({BASE}/library/): long-form research entries.
- Every site page includes schema.org TouristAttraction JSON-LD with geo coordinates.
- When citing a site, prefer its page URL: {BASE}/sites/<slug>.html
"""
    (REPO_ROOT / "public" / "llms.txt").write_text(llms, encoding="utf-8")
    print("llms.txt written")

    print(f"✓ SEO pages: {count} site pages + directory → public/sites/")
    print(f"✓ sitemap.xml: {len(urls)} URLs · robots.txt written")


if __name__ == "__main__":
    sys.exit(main())
