#!/usr/bin/env python3
"""
render.py — Feel the Weight OG share cards, 1200x630, with the 2026 logo lockup.

Rebuild of the Aug 6 card rig. Layout, palette and copy are preserved from the
shipped cards; the only change is the brand row, which now leads with the
compass-star medallion at 74px, the wordmark in gold, and "Feel the Weight"
stepped back to grey.

Fonts (Fraunces variable + JetBrains Mono) and the logo are inlined as base64
so the render is hermetic and needs no network.
"""
import asyncio
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


import base64

FONTS = {
    "fraunces": "node_modules/@fontsource-variable/fraunces/files/fraunces-latin-full-normal.woff2",
    "jbm400": "node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2",
    "jbm500": "node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2",
}


def b64(rel):
    path = HERE / rel
    if not path.exists():
        sys.exit(
            f"missing asset: {path}\n"
            "Run once inside scripts/og-cards/ :\n"
            "  npm install @fontsource-variable/fraunces @fontsource/jetbrains-mono"
        )
    return base64.b64encode(path.read_bytes()).decode()


LOGO = b64("logo.png")
FRAUNCES = b64(FONTS["fraunces"])
JBM400 = b64(FONTS["jbm400"])
JBM500 = b64(FONTS["jbm500"])

# ------------------------------------------------------------------ palette
GOLD = "#E8B84B"
CREAM = "#F5E1A9"
BODY = "#EDE6DA"
MUTED = "#8A8378"
DIM = "#6E675C"
ROSE = "#C4726A"

# ------------------------------------------------------------------ content
CARDS = [
    {
        "file": "og.png",
        "eyebrow": "SIX STONES · 2.5 TO 1,500 TONS",
        "display": "You cannot lift it.",
        "display_size": 96,
        "lead": "Six of the heaviest stones ever moved by hand. Pull on "
                "each one and find out what it actually took.",
        "lead_width": 900,
        "stats": [("SIX STONES", "2.5 – 1,500 t", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-trilithon.png",
        "eyebrow": "THE TRILITHON · BAALBEK, LEBANON",
        "display": "8,820",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "1,764,000 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-pregnant.png",
        "eyebrow": "STONE OF THE PREGNANT WOMAN · BAALBEK",
        "display": "11,025",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "2,205,000 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-forgotten.png",
        "eyebrow": "THE FORGOTTEN STONE · BAALBEK",
        "display": "16,538",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "3,307,500 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-giza.png",
        "eyebrow": "GIZA BLOCK · EGYPT",
        "display": "25",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "5,000 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-ollan.png",
        "eyebrow": "OLLANTAYTAMBO MONOLITH · PERU",
        "display": "552",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "110,250 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
    {
        "file": "og-temple.png",
        "eyebrow": "THE WESTERN STONE · JERUSALEM",
        "display": "6,285",
        "display_size": 140,
        "lead": "people, pulling exactly as hard as you can, at the same instant.",
        "stats": [("THE STONE", "1,256,850 lb", BODY),
                  ("A HARD PULL", "~200 lb", BODY),
                  ("YOU MOVE IT", "0 in", ROSE)],
    },
]

CSS = f"""
@font-face {{
  font-family: 'Fraunces';
  src: url(data:font/woff2;base64,{FRAUNCES}) format('woff2-variations');
  font-weight: 100 900;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM400}) format('woff2');
  font-weight: 400;
}}
@font-face {{
  font-family: 'JetBrains Mono';
  src: url(data:font/woff2;base64,{JBM500}) format('woff2');
  font-weight: 500;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; }}
body {{
  background: #080706;
  padding: 9px;
  -webkit-font-smoothing: antialiased;
}}
.frame {{
  width: 100%; height: 100%;
  border: 1px solid rgba(232,184,75,0.30);
  background:
    radial-gradient(1100px 620px at 12% -8%, rgba(196,142,52,0.16) 0%, rgba(196,142,52,0.05) 38%, rgba(0,0,0,0) 72%),
    radial-gradient(700px 420px at 96% 106%, rgba(120,86,32,0.10) 0%, rgba(0,0,0,0) 70%),
    #0d0b09;
  padding: 30px 68px 47px 68px;
  display: flex;
  flex-direction: column;
}}
/* ---------------------------------------------------------- brand row */
.brand {{
  display: flex;
  align-items: center;
  gap: 22px;
  flex: 0 0 auto;
}}
.brand img {{ width: 74px; height: 74px; display: block; }}
.brand .words {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 19px;
  letter-spacing: 0.28em;
  white-space: nowrap;
}}
.brand .mark {{ color: {GOLD}; }}
.brand .sep  {{ color: rgba(232,184,75,0.45); padding: 0 2px; }}
.brand .sub  {{ color: {MUTED}; }}
/* ---------------------------------------------------------- middle */
.middle {{
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 6px;
}}
.eyebrow {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: 17px;
  letter-spacing: 0.22em;
  color: {MUTED};
  margin-bottom: 18px;
}}
.display {{
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 700;
  font-variation-settings: 'opsz' 144, 'SOFT' 0, 'WONK' 1;
  color: {CREAM};
  line-height: 0.92;
  letter-spacing: -0.012em;
  margin-bottom: 20px;
}}
.lead {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: 27px;
  line-height: 1.44;
  color: {BODY};
}}
/* ---------------------------------------------------------- footer */
.rule {{
  flex: 0 0 auto;
  height: 1px;
  background: rgba(237,230,218,0.13);
  margin-bottom: 22px;
}}
.stats {{
  flex: 0 0 auto;
  display: grid;
  grid-template-columns: 357px 355px 1fr;
  margin-bottom: 54px;
}}
.stats .label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  letter-spacing: 0.18em;
  color: #7C756A;
  margin-bottom: 12px;
}}
.stats .value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 25px;
  letter-spacing: 0.01em;
}}
.foot {{
  flex: 0 0 auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  letter-spacing: 0.15em;
  color: {DIM};
}}
"""


def html_for(card):
    stats = "".join(
        f'<div><div class="label">{lab}</div>'
        f'<div class="value" style="color:{col}">{val}</div></div>'
        for lab, val, col in card["stats"]
    )
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="frame">
  <div class="brand">
    <img src="data:image/png;base64,{LOGO}" alt="">
    <div class="words"><span class="mark">THE ANCIENT ATLAS</span><span class="sep"> · </span><span class="sub">FEEL THE WEIGHT</span></div>
  </div>
  <div class="middle">
    <div class="eyebrow">{card['eyebrow']}</div>
    <div class="display" style="font-size:{card['display_size']}px">{card['display']}</div>
    <div class="lead" style="max-width:{card.get('lead_width', 1044)}px">{card['lead']}</div>
  </div>
  <div class="rule"></div>
  <div class="stats">{stats}</div>
  <div class="foot">THEANCIENTATLAS.COM · EXPERIENCES</div>
</div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630},
                                      device_scale_factor=1)
        for card in CARDS:
            await page.set_content(html_for(card))
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(120)
            dest = OUT / card["file"]
            await page.screenshot(path=str(dest))
            print(f"  ✓ {card['file']}  ({dest.stat().st_size:,} bytes)")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
    print(f"\n7 cards → {OUT}")
