#!/usr/bin/env python3
"""
build-creator-feature.py — Ageless Rock, the feature edition (2026-08-07)

Builds public/creators/ageless-rock.html.

The by-place index (build-creator-page.py, now at ageless-rock-by-place.html)
answers "where has he been". It is a good reference and a bad front door: one
long scroll, no argument, and it buries the thing that makes the body of work
unusual under an alphabet of countries.

This page is built the other way round, Minto style. One question at the top.
The answer immediately under it. Then the four arguments that support the
answer, each as a magazine spread that puts places from different continents
beside each other, because the resemblance IS the argument and geography is
what hides it. The complete catalogue sits underneath in a paged deck, so the
archive is still there for anyone who wants to work through it.

The families are not invented for the page. Each is defined below as an
explicit list of sites, and every one is asserted against data/sites.json and
against his actual wires at build time, so a theme cannot quietly drift out of
sync with the record.

"Best" is a judgement, so it is made from evidence already in the Atlas rather
than from popularity: tier 1 flagships, sites flagged with open questions, and
depth of coverage (how many times he went back). That basis is stated on the
page rather than implied.

Run from repo root :  python3 scripts/build-creator-feature.py
"""
import json
import html
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA = REPO_ROOT / "data"
OUT = REPO_ROOT / "public" / "creators" / "ageless-rock.html"
CATALOGUE = Path.home() / "Downloads" / "ageless-rock-videos.md"

CREATOR_KEY = "agelessrock"
HANDLE = "@AgelessRock888"
CHANNEL_URL = "https://www.youtube.com/@AgelessRock888"
INDEX_PAGE = "/creators/ageless-rock-by-place"

PER_PAGE = 24

CAT_LABEL = {
    "megalithic": "Megalithic", "city": "City / Ruins", "temple": "Temple",
    "rock-cut": "Rock-Cut", "rockcut": "Rock-Cut", "tomb": "Tomb / Burial",
    "underground": "Underground", "pyramid": "Pyramid",
    "settlement": "Settlement", "geoglyph": "Geoglyph", "monolithic": "Monolithic",
}

# =====================================================================
# The four arguments. Each `sites` list is checked at build time.
# `hero` must be one of the sites; its first walkthrough leads the spread.
# =====================================================================
THEMES = [
    {
        "n": "01",
        "key": "subtractive",
        "claim": "They cut downward into the rock instead of building upward on it.",
        "kicker": "The subtractive tradition",
        "hero": "Lalibela Rock-Hewn Churches",
        "essay": (
            "A building is normally an act of addition. You quarry a block, move it, "
            "lift it, set it down, and repeat until the thing stands. The sites in "
            "this family reverse that completely. Nothing is carried in. The masons "
            "start at the top of a living rock face and remove everything that is not "
            "the building, which means every cut is final, the plan has to be held "
            "in the head before the first blow, and there is no correcting a wall "
            "that has been cut too thin. "
            "Ethiopia sinks whole churches into the ground. India carves a temple "
            "complex out of one hillside from the roof down. Türkiye takes it "
            "underground for eighteen storeys. Afghanistan cuts a stupa out of the "
            "bedrock rather than raising one. China opens grottoes into cliffs by the "
            "thousand. These are separate cultures with separate histories and no "
            "plausible line of contact, using the same counter-intuitive method."
        ),
        "sites": [
            "Lalibela Rock-Hewn Churches", "Kailasa Temple (Ellora Cave 16)",
            "Ellora Caves", "Barabar Caves", "Takht-e Rustam (Afghanistan)",
            "Longyou Caves", "Bazda Caves", "Derinkuyu Underground City",
            "Leshan Giant Buddha", "Bamiyan", "Naqsh-e Rustam",
            "Gümüşler Rock-Cut Monastery", "Mogao Grottoes", "Longmen Grottoes",
            "Toraja Rock-Cut Burials", "Zedekiah's Cave", "Gilmerton Cove",
        ],
    },
    {
        "n": "02",
        "key": "interlock",
        "claim": "They fitted many-sided blocks to each other without mortar, on five continents.",
        "kicker": "The interlocked wall",
        "hero": "Ollantaytambo",
        "essay": (
            "Square your stone and you can stack it fast, but the wall is only as "
            "strong as the mortar and the courses run straight through, which is "
            "exactly where a wall fails when the ground moves. The alternative is "
            "slower and stranger: take the block roughly as the quarry gives it, "
            "then cut each face to the blocks already laid, so no two stones are "
            "alike and no vertical joint runs through. "
            "The result is a wall that flexes. In an earthquake the empty joints act "
            "as energy sinks, blocks rocking and sliding fractionally against each "
            "other instead of storing the shock until something snaps. "
            "That is the practical reason the technique recurs. What it does not "
            "explain is the tolerance at the top of the range, or joint faces that "
            "curve in two directions so a block cannot be lowered straight in along "
            "any axis."
        ),
        "sites": [
            "Ollantaytambo", "Orbetello", "Rusellae", "Vetulonia", "Cosa",
            "Tall-e Takht (Cyclopean Wall of Pasargadae)", "Temple Mount Megaliths",
            "Menehune Ditch (Kīkīaola)", "Kosrae Leluh Island", "Machu Picchu",
        ],
    },
    {
        "n": "03",
        "key": "mass",
        "claim": "They moved single stones that no obvious method accounts for.",
        "kicker": "Mass without machines",
        "hero": "Yangshan Quarry",
        "essay": (
            "Every culture in this family reached a point where it stopped making "
            "the stones bigger, and the place where each one stopped is the most "
            "informative thing about it. China left the Yangshan stele lying in its "
            "quarry, cut free on three sides, far past any weight that could have "
            "been moved. Micronesia ferried limestone discs between islands by sea. "
            "The Marianas raised capped pillars; Nan Madol stacked basalt logs into "
            "an island city on a reef. Peru brought porphyry across a river and up "
            "the opposite slope. "
            "The common thread is not size for its own sake. It is that in each case "
            "the effort is wildly disproportionate to any structural need, which "
            "means the mass itself was the point, and that is a statement about "
            "intent rather than engineering."
        ),
        "sites": [
            "Yangshan Quarry", "Ollantaytambo", "Nan Madol", "Yap Rai Stones",
            "Latte Stones of Guam", "Latte Stones of Tinian",
            "Rota Quarry (As Nieves)", "Temple Mount Megaliths",
            "Marquesas Islands", "Palau Megalithic Site",
        ],
    },
    {
        "n": "04",
        "key": "water",
        "claim": "They engineered water at a scale the buildings never needed.",
        "kicker": "The waterworks nobody photographs",
        "hero": "West Baray",
        "essay": (
            "This is the family that gets walked past, because a reservoir does not "
            "photograph like a pyramid. Angkor is the clearest case: the temples are "
            "what visitors come for, but the barays around them are the larger "
            "achievement by volume of earth moved, and they are laid out with a "
            "precision that has nothing to do with irrigation alone. "
            "Jerusalem cuts a tunnel through solid rock from both ends at once and "
            "meets in the middle. Kauai builds a ditch of dressed, fitted stone to "
            "carry water to taro, and a fishpond wall long enough to be visible from "
            "altitude. "
            "Sort by country and these never appear together. Sort by what was "
            "actually built and they are obviously one idea: control the water, at a "
            "cost that only makes sense if water was the sacred part."
        ),
        "sites": [
            "West Baray", "East Baray", "Neak Poan (Jayatataka Baray)",
            "Srah Srang", "West Mebon", "Hezekiah's Tunnel",
            "Menehune Fishpond (Alekoko)", "Menehune Ditch (Kīkīaola)",
            "Chichen Itza",
        ],
    },
]


def slugify(name):
    """Same rule as scripts/build-seo-pages.py. Do not simplify: dropping the
    transliteration silently 404s every site whose name carries a diacritic."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("ı", "i").replace("ħ", "h").replace("ø", "o").replace("ß", "ss")
    s = re.sub(r"[''']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "site"


def e(x):
    return html.escape(str(x), quote=True)


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def parse_catalogue():
    if not CATALOGUE.exists():
        sys.exit(f"ABORT: catalogue not found at {CATALOGUE}")
    pat = re.compile(r"^(\d+)\.\s+\[(.+?)\]\(https://www\.youtube\.com/watch\?v=([\w-]+)\)\s*$")
    rows = []
    for line in CATALOGUE.read_text(encoding="utf-8").splitlines():
        m = pat.match(line.strip())
        if m:
            rows.append({"title": m.group(2), "id": m.group(3)})
    if not rows:
        sys.exit("ABORT: parsed zero videos")
    return rows


def build_model():
    videos = load("videos.json")
    sites = {s["n"]: s for s in load("sites.json")}
    countries = load("countries.json")

    wires = {}
    for site_name, lst in videos.items():
        for v in lst:
            if v.get("cr") == CREATOR_KEY:
                wires.setdefault(v["id"], []).append(site_name)

    by_site = {}
    catalogue = parse_catalogue()
    for vid in catalogue:
        targets = wires.get(vid["id"]) or []
        vid["site"] = targets[0] if targets else None
        vid["country"] = countries.get(vid["site"], "") if vid["site"] else ""
        st = sites.get(vid["site"]) if vid["site"] else None
        vid["cat"] = (st or {}).get("cat", "")
        vid["tier"] = (st or {}).get("tier")
        vid["open"] = bool((st or {}).get("signal") == "open" and (st or {}).get("criteria"))
        # index under EVERY site the walkthrough is wired to, not just the
        # first. Several videos legitimately cover more than one place — the
        # Bazda Caves piece is wired to Longyou, Longmen, Kotukal and San
        # Andrea Priu as well — and a theme should be able to reach any of them.
        for target in targets:
            if target in sites:
                by_site.setdefault(target, []).append(vid)

    # -------------------------------------------------- validate the themes
    problems = []
    for t in THEMES:
        kept = []
        for name in t["sites"]:
            if name not in sites:
                problems.append(f"{t['key']}: {name!r} is not a site in sites.json")
            elif name not in by_site:
                problems.append(f"{t['key']}: {name!r} has no walkthrough by this creator")
            else:
                kept.append(name)
        t["sites"] = kept
        if t["hero"] not in kept:
            problems.append(f"{t['key']}: hero {t['hero']!r} did not survive validation")
    if problems:
        print("ABORT: theme definitions are out of sync with the record:")
        for p in problems:
            print("   ·", p)
        sys.exit(1)

    stats = {
        "videos": len(catalogue),
        "sites": len(by_site),
        "countries": len({v["country"] for v in catalogue if v["country"]}),
        "unplaced": sum(1 for v in catalogue if not v["site"]),
    }
    return catalogue, by_site, sites, countries, stats


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --obsidian:#0B0B0F;--charcoal:#14141A;--slate:#1C1C24;--stone:#2A2A35;
  --mist:#8A8A9A;--cloud:#C5C5D0;--ivory:#F0EEE9;--champagne:#C9A84C;--amber:#E8B960;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  --serif:'Fraunces',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --gut:clamp(20px,4vw,64px);
}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{font-family:var(--sans);background:var(--obsidian);color:var(--ivory);-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;opacity:.032;pointer-events:none;z-index:9999;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
::selection{background:var(--champagne);color:var(--obsidian)}
a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 var(--gut)}

/* ---------------- masthead ---------------- */
header.site{position:sticky;top:0;z-index:100;background:linear-gradient(180deg,rgba(11,11,15,.98),rgba(11,11,15,.9));backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(42,42,53,.5);padding:12px var(--gut);display:flex;align-items:center;gap:18px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand svg{width:30px;height:30px;filter:drop-shadow(0 2px 8px rgba(201,168,76,.2))}
.brand b{font-family:var(--serif);font-size:19px;font-weight:600;letter-spacing:-.4px}
.sp{flex:1}
.toplinks{display:flex;gap:20px;font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.toplinks a{color:var(--cloud);text-decoration:none;transition:color .15s}
.toplinks a:hover,.toplinks a.on{color:var(--champagne)}

/* ---------------- the question ---------------- */
.opening{padding:clamp(56px,9vw,132px) 0 clamp(40px,6vw,84px);position:relative}
.opening::after{content:'';position:absolute;inset:0;background:radial-gradient(1000px 500px at 50% -10%,rgba(201,168,76,.11),transparent 65%);pointer-events:none;z-index:-1}
.issue{font-family:var(--mono);font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--champagne);font-weight:700;text-align:center;margin-bottom:clamp(28px,5vw,52px)}
.issue span{color:var(--mist)}
.qlabel{font-family:var(--mono);font-size:10px;letter-spacing:.28em;text-transform:uppercase;color:var(--mist);text-align:center;margin-bottom:20px}
h1.q{font-family:var(--serif);font-weight:500;font-size:clamp(31px,5.4vw,68px);line-height:1.1;letter-spacing:-.022em;text-align:center;max-width:19ch;margin:0 auto;font-variation-settings:"opsz" 144}
h1.q em{font-style:italic;color:var(--champagne)}
.qrule{height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,.5),transparent);max-width:220px;margin:clamp(36px,5vw,56px) auto}
.alabel{font-family:var(--mono);font-size:10px;letter-spacing:.28em;text-transform:uppercase;color:var(--champagne);text-align:center;margin-bottom:18px;font-weight:700}
p.answer{font-family:var(--serif);font-size:clamp(19px,2.5vw,29px);line-height:1.42;letter-spacing:-.008em;text-align:center;max-width:26ch;margin:0 auto;color:var(--ivory)}
p.answer b{color:var(--amber);font-weight:600}
p.answer-sub{font-size:clamp(15px,1.5vw,17px);line-height:1.7;color:var(--cloud);max-width:62ch;margin:clamp(26px,4vw,38px) auto 0;text-align:center}
.byline{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mist);text-align:center;margin-top:34px}
.byline a{color:var(--champagne);text-decoration:none;border-bottom:1px solid rgba(201,168,76,.4)}
.contents{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:clamp(34px,5vw,54px)}
.contents a{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--cloud);text-decoration:none;padding:8px 14px;border:1px solid rgba(42,42,53,1);border-radius:99px;transition:all .16s}
.contents a:hover{color:var(--champagne);border-color:rgba(201,168,76,.5);background:rgba(201,168,76,.06)}
.contents a i{font-style:normal;color:var(--champagne);margin-right:7px}

/* ---------------- feature spread ---------------- */
.feature{padding:clamp(58px,8vw,110px) 0;border-top:1px solid rgba(42,42,53,.55)}
.fhead{display:grid;grid-template-columns:auto 1fr;gap:clamp(18px,3vw,38px);align-items:start;margin-bottom:clamp(26px,4vw,44px)}
.fnum{font-family:var(--serif);font-size:clamp(46px,7vw,104px);font-weight:500;line-height:.8;color:rgba(201,168,76,.26);font-variation-settings:"opsz" 144;letter-spacing:-.04em}
.kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.26em;text-transform:uppercase;color:var(--champagne);font-weight:700;margin-bottom:14px}
h2.claim{font-family:var(--serif);font-weight:500;font-size:clamp(24px,3.4vw,42px);line-height:1.16;letter-spacing:-.018em;max-width:22ch;font-variation-settings:"opsz" 96}
.fbody{display:grid;grid-template-columns:1.35fr 1fr;gap:clamp(24px,4vw,54px);align-items:start}
.feature.flip .fbody{grid-template-columns:1fr 1.35fr}
.feature.flip .fbody .fart{order:2}
.feature.flip .fbody .fessay{order:1}
.fessay p{font-size:16px;line-height:1.72;color:var(--cloud)}
.fessay p+p{margin-top:16px}
.fart figure{margin:0}
.fart img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:10px;border:1px solid rgba(42,42,53,.9);background:var(--charcoal)}
.fart figcaption{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--mist);margin-top:12px;line-height:1.6}
.fart figcaption b{color:var(--champagne);font-weight:600}
.heroa{display:block;text-decoration:none;position:relative;border-radius:10px;overflow:hidden}
.heroa::after{content:'';position:absolute;left:50%;top:50%;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;background:rgba(11,11,15,.55);border:1px solid rgba(240,238,233,.3);backdrop-filter:blur(3px);opacity:0;transition:opacity .2s}
.heroa:hover::after{opacity:1}
.heroa img{transition:transform .6s cubic-bezier(.2,.7,.3,1),opacity .3s}
.heroa:hover img{transform:scale(1.03)}

/* the juxtaposition strip: same idea, different continents */
.strip{margin-top:clamp(28px,4vw,44px)}
.striplabel{font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--mist);padding-bottom:11px;border-bottom:1px solid rgba(42,42,53,.7);margin-bottom:18px}
.striplabel b{color:var(--cloud);font-weight:600}
.strip .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:16px}
.sc{text-decoration:none;display:block}
.sc .co{font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--champagne);margin-bottom:8px}
.sc img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:7px;border:1px solid rgba(42,42,53,.9);opacity:.86;transition:opacity .2s,transform .2s,border-color .2s;background:var(--charcoal)}
.sc:hover img{opacity:1;transform:translateY(-2px);border-color:rgba(201,168,76,.5)}
.sc .nm{font-size:12.5px;line-height:1.4;color:var(--cloud);margin-top:9px}
.sc:hover .nm{color:var(--ivory)}

/* ---------------- pull quote ---------------- */
.pull{padding:clamp(46px,7vw,92px) 0;border-top:1px solid rgba(42,42,53,.55)}
.pull p{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(20px,2.9vw,34px);line-height:1.36;text-align:center;max-width:24ch;margin:0 auto;color:var(--ivory);letter-spacing:-.01em}
.pull small{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--mist);margin-top:24px}

/* ---------------- catalogue ---------------- */
.cat{padding:clamp(56px,8vw,104px) 0 clamp(70px,9vw,120px);border-top:1px solid rgba(201,168,76,.24)}
.cathead{text-align:center;margin-bottom:clamp(28px,4vw,44px)}
.cathead h2{font-family:var(--serif);font-weight:500;font-size:clamp(26px,3.6vw,44px);letter-spacing:-.02em;font-variation-settings:"opsz" 96}
.cathead p{font-size:15px;line-height:1.7;color:var(--cloud);max-width:60ch;margin:14px auto 0}
.controls{display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;margin-bottom:26px}
.filters{display:flex;gap:7px;flex-wrap:wrap;justify-content:center}
.filters button{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--cloud);background:transparent;border:1px solid rgba(42,42,53,1);border-radius:99px;padding:7px 13px;cursor:pointer;transition:all .15s}
.filters button:hover{color:var(--champagne);border-color:rgba(201,168,76,.45)}
.filters button.on{color:var(--obsidian);background:var(--champagne);border-color:var(--champagne);font-weight:700}
#cq{font-family:var(--mono);font-size:11.5px;color:var(--ivory);background:rgba(28,28,36,.9);border:1px solid rgba(42,42,53,1);border-radius:8px;padding:8px 13px;width:210px;outline:none}
#cq::placeholder{color:var(--mist)}
#cq:focus{border-color:rgba(201,168,76,.6)}
.deck{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:18px;min-height:300px}
.cell{text-decoration:none;display:block}
.cell img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:7px;border:1px solid rgba(42,42,53,.9);opacity:.85;transition:opacity .2s,transform .2s,border-color .2s;background:var(--charcoal)}
.cell:hover img{opacity:1;transform:translateY(-2px);border-color:rgba(201,168,76,.5)}
.cell .t{font-size:12.5px;line-height:1.42;color:var(--cloud);margin-top:9px}
.cell:hover .t{color:var(--ivory)}
.cell .m{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist);margin-top:5px}
.flip{display:flex;align-items:center;justify-content:center;gap:20px;margin-top:38px}
.flip button{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--cloud);background:transparent;border:1px solid rgba(42,42,53,1);border-radius:8px;padding:10px 18px;cursor:pointer;transition:all .15s}
.flip button:hover:not(:disabled){color:var(--champagne);border-color:rgba(201,168,76,.5);background:rgba(201,168,76,.06)}
.flip button:disabled{opacity:.3;cursor:default}
#pageinfo{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mist);min-width:170px;text-align:center}
#pageinfo b{color:var(--champagne)}
.none{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mist);text-align:center;padding:70px 0}
.hidden{display:none!important}

footer.site{border-top:1px solid rgba(42,42,53,.6);padding:34px var(--gut);text-align:center;font-size:13px;color:var(--mist)}
footer.site a{color:var(--champagne);text-decoration:none}

@media(max-width:860px){
  .fbody,.feature.flip .fbody{grid-template-columns:1fr}
  .feature.flip .fbody .fart,.feature.flip .fbody .fessay{order:0}
  .fhead{grid-template-columns:1fr;gap:8px}
  .fnum{font-size:40px}
  .deck{grid-template-columns:repeat(auto-fill,minmax(142px,1fr));gap:13px}
  .strip .row{grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:12px}
  #cq{width:100%}
  .toplinks{gap:12px;font-size:9.5px}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}html{scroll-behavior:auto}}
"""


LOGO = ('<svg viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<defs><linearGradient id="g" x1="50%" y1="0%" x2="50%" y2="100%">'
        '<stop offset="0%" stop-color="#F5DCA0"/><stop offset="100%" stop-color="#8E7234"/>'
        '</linearGradient></defs><polygon points="-36.71,-36.71 -12.28,-29.64 0,-84 12.28,-29.64 '
        '36.71,-36.71 29.64,-12.28 84,0 29.64,12.28 36.71,36.71 12.28,29.64 0,84 -12.28,29.64 '
        '-36.71,36.71 -29.64,12.28 -84,0 -29.64,-12.28" fill="url(#g)"/>'
        '<circle cx="0" cy="0" r="6" fill="#F5DCA0"/></svg>')

FALLBACK = ("this.onerror=null;this.src='https://i.ytimg.com/vi/'"
            "+this.dataset.vid+'/mqdefault.jpg'")


def thumb(vid, big=False):
    q = "maxresdefault" if big else "mqdefault"
    return (f'<img src="https://i.ytimg.com/vi/{e(vid["id"])}/{q}.jpg" '
            f'data-vid="{e(vid["id"])}" onerror="{FALLBACK}" alt="" '
            f'loading="lazy" decoding="async">')


def watch(vid):
    return f'https://www.youtube.com/watch?v={e(vid["id"])}'


def render_feature(t, by_site, sites, countries, idx):
    hero = by_site[t["hero"]][0]
    hero_country = countries.get(t["hero"], "")

    # one card per site, preferring a country we have not shown yet — the
    # whole point of the strip is that the neighbours are far apart
    seen, cards = set(), []
    pool = [n for n in t["sites"] if n != t["hero"]]
    for prefer_new in (True, False):
        for name in pool:
            if len(cards) >= 6:
                break
            if any(c[0] == name for c in cards):
                continue
            c = countries.get(name, "")
            if prefer_new and c in seen:
                continue
            seen.add(c)
            cards.append((name, c, by_site[name][0]))

    strip = "".join(
        f'<a class="sc" href="{watch(v)}" target="_blank" rel="noopener">'
        f'<div class="co">{e(c)}</div>{thumb(v)}'
        f'<div class="nm">{e(name)}</div></a>'
        for name, c, v in cards)

    paras = "".join(f"<p>{e(p).strip()}</p>"
                    for p in t["essay"].split("  ") if p.strip())

    return f"""<section class="feature{' flip' if idx % 2 else ''}" id="f-{t['key']}">
  <div class="wrap">
    <div class="fhead">
      <div class="fnum">{t['n']}</div>
      <div><div class="kicker">{e(t['kicker'])}</div>
        <h2 class="claim">{e(t['claim'])}</h2></div>
    </div>
    <div class="fbody">
      <div class="fart">
        <figure>
          <a class="heroa" href="{watch(hero)}" target="_blank" rel="noopener">{thumb(hero, big=True)}</a>
          <figcaption><b>{e(t['hero'])}</b> · {e(hero_country)} — {e(hero['title'])}</figcaption>
        </figure>
      </div>
      <div class="fessay">{paras}</div>
    </div>
    <div class="strip">
      <div class="striplabel">The same idea, <b>{e(len(seen))} more places that never met</b></div>
      <div class="row">{strip}</div>
    </div>
  </div>
</section>"""


def render_cell(v):
    meta = " · ".join(x for x in [v["site"] or "Unplaced", v["country"]] if x)
    return (f'<a class="cell" href="{watch(v)}" target="_blank" rel="noopener" '
            f'data-t="{e((v["title"] + " " + meta).lower())}" data-cat="{e(v["cat"] or "other")}">'
            f'{thumb(v)}<div class="t">{e(v["title"])}</div>'
            f'<div class="m">{e(meta)}</div></a>')


SCRIPT = """
(function(){
  var PER=%d;
  var deck=document.getElementById('deck');
  var cells=[].slice.call(deck.querySelectorAll('.cell'));
  var info=document.getElementById('pageinfo');
  var prev=document.getElementById('prev'), next=document.getElementById('next');
  var none=document.getElementById('none'), q=document.getElementById('cq');
  var filter='all', term='', page=0, live=cells;
  function recompute(){
    live=cells.filter(function(c){
      var okF=(filter==='all')||c.dataset.cat===filter;
      var okQ=!term||c.dataset.t.indexOf(term)>-1;
      return okF&&okQ;
    });
    page=0; draw();
  }
  function draw(){
    var pages=Math.max(1,Math.ceil(live.length/PER));
    if(page>pages-1) page=pages-1;
    cells.forEach(function(c){c.classList.add('hidden')});
    live.slice(page*PER,(page+1)*PER).forEach(function(c){c.classList.remove('hidden')});
    info.innerHTML= live.length? ('Page <b>'+(page+1)+'</b> of '+pages+' · '+live.length+' entries') : '';
    prev.disabled=(page===0); next.disabled=(page>=pages-1);
    none.classList.toggle('hidden', live.length>0);
  }
  function go(d){
    var pages=Math.max(1,Math.ceil(live.length/PER));
    var t=Math.min(Math.max(page+d,0),pages-1);
    if(t===page) return;
    page=t; draw();
    deck.scrollIntoView({behavior:'smooth',block:'start'});
  }
  prev.addEventListener('click',function(){go(-1)});
  next.addEventListener('click',function(){go(1)});
  [].slice.call(document.querySelectorAll('.filters button')).forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on')});
      b.classList.add('on'); filter=b.dataset.cat; recompute();
    });
  });
  q.addEventListener('input',function(){term=q.value.trim().toLowerCase();recompute()});
  document.addEventListener('keydown',function(ev){
    if(ev.target===q) return;
    if(ev.key==='ArrowLeft') go(-1);
    if(ev.key==='ArrowRight') go(1);
  });
  draw();
})();
"""


def render(catalogue, by_site, sites, countries, stats):
    features = "".join(render_feature(t, by_site, sites, countries, i)
                       for i, t in enumerate(THEMES))

    contents = "".join(
        f'<a href="#f-{t["key"]}"><i>{t["n"]}</i>{e(t["kicker"])}</a>' for t in THEMES
    ) + '<a href="#catalogue"><i>05</i>The complete catalogue</a>'

    cats = {}
    for v in catalogue:
        cats[v["cat"] or "other"] = cats.get(v["cat"] or "other", 0) + 1
    order = sorted(cats, key=lambda k: -cats[k])
    filters = '<button class="on" data-cat="all">Everything ' + str(len(catalogue)) + '</button>'
    filters += "".join(
        f'<button data-cat="{e(c)}">{e(CAT_LABEL.get(c, c.title()))} {cats[c]}</button>'
        for c in order if cats[c] >= 8)

    cells = "".join(render_cell(v) for v in catalogue)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Ageless Rock — a creator study | The Ancient Atlas</title>
<meta name="description" content="Four ways of working stone that recur on separate continents, and one man who has stood inside all four. A study of Bernie Ong's fieldwork across {stats['sites']} sites in {stats['countries']} countries." />
<meta name="theme-color" content="#0B0B0F" />
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png" />
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png" />
<link rel="canonical" href="https://theancientatlas.com/creators/ageless-rock" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="The Ancient Atlas" />
<meta property="og:title" content="Ageless Rock : four ways of working stone" />
<meta property="og:description" content="What repeats when you stop sorting these places by where they are? Four techniques do — and they turn up between places that never met." />
<meta property="og:url" content="https://theancientatlas.com/creators/ageless-rock" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preconnect" href="https://i.ytimg.com" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>{CSS}</style>
<script data-goatcounter="https://ancientatlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>

<header class="site">
  <a class="brand" href="/">{LOGO}<b>Ancient Atlas</b></a>
  <div class="sp"></div>
  <nav class="toplinks">
    <a href="/">Atlas</a><a href="/library/">Library</a>
    <a href="/creators/ageless-rock" class="on">Creator Study</a>
    <a href="{INDEX_PAGE}">The Index</a>
  </nav>
</header>

<section class="opening">
  <div class="wrap">
    <div class="issue">The Ancient Atlas <span>·</span> Creator Study <span>·</span> No. 01</div>
    <div class="qlabel">The question</div>
    <h1 class="q">What repeats when you stop sorting these places by <em>where they are</em>?</h1>
    <div class="qrule"></div>
    <div class="alabel">The answer</div>
    <p class="answer">Four ways of working stone do — and <b>Bernie Ong has stood inside all four.</b></p>
    <p class="answer-sub">He has walked {stats['sites']} sites in {stats['countries']} countries and filmed {stats['videos']} of them from the ground. Laid out by country, that reads as a travel record. Laid out by <em>what was done to the rock</em>, four families appear, and each one turns up in places with no history of contact. What follows is those four, then the complete archive.</p>
    <p class="byline">Fieldwork by Bernie Ong · {e(HANDLE)} · <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">Follow the channel ↗</a></p>
    <nav class="contents">{contents}</nav>
  </div>
</section>

{features}

<section class="pull">
  <div class="wrap">
    <p>Sorted by country, these are four separate holidays. Sorted by method, they are four arguments.
      <small>Why this page is built the way it is</small></p>
  </div>
</section>

<section class="cat" id="catalogue">
  <div class="wrap">
    <div class="cathead">
      <h2>The complete catalogue</h2>
      <p>All {stats['videos']} walkthroughs, {stats['sites']} sites, {stats['countries']} countries. Filter by what a place is, search by name, and turn the pages with the arrows or the ← → keys. {stats['unplaced']} entries have no site record in the Atlas yet and are marked unplaced rather than hidden.</p>
    </div>
    <div class="controls">
      <div class="filters">{filters}</div>
      <input id="cq" type="search" placeholder="Search the archive" autocomplete="off" spellcheck="false" aria-label="Search the catalogue" />
    </div>
    <div class="deck" id="deck">{cells}</div>
    <div class="none hidden" id="none">Nothing in the archive matches that.</div>
    <div class="flip">
      <button id="prev" type="button">‹ Previous</button>
      <div id="pageinfo"></div>
      <button id="next" type="button">Next ›</button>
    </div>
  </div>
</section>

<footer class="site">
  Fieldwork and footage by <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">Ageless Rock</a>.
  Study, sequencing and site records by <a href="/">The Ancient Atlas</a> — hand-curated, ad-free.
  · <a href="{INDEX_PAGE}">Browse the same work by place →</a>
</footer>

<script>{SCRIPT % PER_PAGE}</script>
</body>
</html>"""


def main():
    catalogue, by_site, sites, countries, stats = build_model()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(catalogue, by_site, sites, countries, stats), encoding="utf-8")
    print(f"  ✓ {OUT.relative_to(REPO_ROOT)}  ({OUT.stat().st_size:,} bytes)")
    print(f"    {stats['videos']} walkthroughs · {stats['sites']} sites · "
          f"{stats['countries']} countries · {stats['unplaced']} unplaced")
    for t in THEMES:
        print(f"    {t['n']} {t['kicker']:<34} {len(t['sites'])} sites")


if __name__ == "__main__":
    sys.exit(main())
