# Session Handoff — Mammoth Merch Capsule (Ancient Atlas)

Written for a fresh Claude Cowork session. Read this first, then continue.

## How to resume (say this to Claude)
"Continue the Ancient Atlas mammoth merch work. Read
`~/Documents/GitHub/ancient-atlas/branding/merch-design/mammoth/SESSION_HANDOFF.md`."
Reconnect these folders if prompted: the GitHub repo `~/Documents/GitHub/ancient-atlas`,
`~/Downloads`, and iCloud Drive.

## Where everything lives
- Canonical repo: `~/Documents/GitHub/ancient-atlas/`
- All merch assets: `branding/merch-design/mammoth/`
- Alternate lighter-coat design: `branding/merch-design/mammoth-classic/`
- Design briefs: `branding/merch-design/GEMINI_MEGAFAUNA_BRIEF.md`, `FOURTHWALL_CATALOG.md`; `docs/FOURTHWALL_STORE.md`
- Store: ancient-atlas-shop.fourthwall.com

## Key asset files (mammoth/ folder)
- `mammoth-master.svg` — CANONICAL vector logo (clean Illustrator geometry, recolor via the two fills in its `<style>`: `.ink` = champagne, `.tusk` = ivory)
- `mammoth-champagne-{256..4500}.png` — transparent mark at sizes
- `mammoth-champagne-4500.png` — print master
- `mammoth-tee-front-4500x5400.png`, `mammoth-tee-back-4500x5400.png` — tee print files
- `mammoth-gemini-back-bold.png` — **USE THIS for the hoodie back** (strengthened for DTG; the lush Gemini plate, transparent, works on black + navy)
- `mammoth-gemini-back-transparent.png` — same plate, thinner lines (superseded by -bold for print)
- colorway SVGs: `mammoth-mono-obsidian`, `mammoth-mono-ivory`, `mammoth-for-ivory-bg`
- `mammoth-icon-{32,180,512}.png` — favicons
- `mammoth-reflection.png`, `mammoth-reflection-ice.png` — **DISPLAY ONLY, never print** (web/social/slides)

## Brand rules (locked)
- Palette: obsidian `#0D0D12`, champagne `#C9A84C`, amber `#E8B960`, ivory `#F0EEE9`. Headings: Fraunces.
- The amber dot is the brand atom: creature eye = map pin = compass center. Fractal principle = self-similar in structure, minimal in surface (no fractal/psychedelic textures).
- Champagne/ivory only read on DARK/earthy garments. Never light, pastel, or warm-orange (gold vanishes).
- Left-chest placement: ~4" wide, pocket height, facing inward.
- Reflection art = screen only. Plain mammoth = anything physically printed.
- Photoreal mammoth render = light garments / black-only / web hero. Do NOT vectorize it; it has no clean vector.
- Gemini rule: never let it set type (AI gibberish). Generate "artwork only, no product/mockup, no text," leave text areas blank, typeset in Fraunces afterward.

## Products built (all in Fourthwall)
Collection: **The Last Animals of the Ice Age**
- **The Mammoth · Heavyweight Tee** — Comfort Colors Garment-Dyed. Black + Navy (Espresso pending sample). Left-chest ~4". Price **$32**.
- **The Mammoth · Heavyweight Hoodie** — Cotton Heritage. Left-chest front + bold Gemini plate on back. 4 dark colors. Price **$56**.
- **The Mammoth · Mug** — black glossy, line-art mammoth. **$18 / $20**.
- **The Mammoth · Portrait Mug** — white, photoreal mammoth. **$18 / $20 / $22**.

## Canonical copy (NLP + JTBD; no em dashes; "pyramids already stood" is debate-proof)
**Tee:**
> A woolly mammoth in clean champagne line, printed on a garment-dyed heavyweight tee that softens and deepens with every wash.
>
> At a glance, a beautifully drawn mammoth. Look closer and the amber eye is the same point of light that marks every site on theancientatlas.com.
>
> Across the Ice Age world they once moved in herds beyond counting. After the Younger Dryas their numbers thinned to a last few, holding on at the edge of the world on Wrangel Island until about four thousand years ago. By then, the pyramids of Giza already stood. Now one walks with you.

**Hoodie:**
> Pull the hood up and the day goes quiet. Heavyweight, brushed-soft fleece that holds warmth and gets more yours with every wear, the one you reach for first.
>
> A small mammoth marks the chest. Turn around and the full study opens across the back: the mammoth charted within its own geometry, a globe, a golden spiral, a field of stars, the same way the atlas maps everything else. Quiet up front, a whole world behind you.
>
> These were the last of the great Ice Age animals. Herds beyond counting once, then a final few holding on at the edge of the world until about four thousand years ago. By then the pyramids of Giza already stood. Now one walks with you.

**Mug (line art, black):**
> Wrap your hands around it and the morning slows. A single mammoth rests on the black glaze, gold and calm, the same mark that runs through the rest of the collection.
>
> One of the last great animals of the Ice Age, keeping you company while the coffee's hot.
>
> Herds beyond counting once. Now one walks your mornings.

**Portrait Mug (photoreal, white):**
> Wrap your hands around it and he's right there: frost in the fur, the long sweep of the tusks, a dark and knowing eye. The animal as it lived, not as it's remembered.
>
> The last of the great Ice Age giants, here for the length of a cup of coffee.
>
> Herds beyond counting once. Now one looks back at you each morning.

## OPEN LOOPS / NEXT STEPS
1. **Samples:** Jeff ordered 1 tee + 1 mug to test. Add a hoodie sample. Judge gold-on-dark DTG in person, especially (a) the hoodie back's faint lines and (b) the espresso tee's low contrast.
2. **Set the published hoodie back to HIDDEN** until its sample passes (it was flipped to Public).
3. **Confirm all prices** are set (several products defaulted to $3 profit): Tee $32, Hoodie $56, Mugs $18–22.
4. **Espresso tee** — sample before keeping; it is the lowest-contrast colorway.
5. **Storefront theme** — set Fourthwall Style to brand tokens: Background `#0D0D12`, Text `#F0EEE9`, Primary `#C9A84C`, Text-over-Primary `#0D0D12`; Fraunces headings; upload logo + favicon; clear all demo/placeholder products and blog posts.
6. **Drop 2 (next species):** sabertooth, glyptodon, ground sloth — same Gemini → Illustrator Image Trace + Expand → vector pipeline that produced the mammoth.

## SEPARATE open item — Ancient Atlas data push (NOT merch)
Earlier this session, the **Sicilian Channel monolith** (new site) + **Osiris Shaft EP03** first-party wire were added to the atlas data locally and built (`data/`, `public/data/`, `public/index.html`, `public/og-image.png`) but NOT pushed. Counts went 560→561 sites, 59→60 creators, 828→830 walkthroughs. To ship, from repo root:
```
rm -f .git/index.lock
git add data/ public/data/ public/index.html public/og-image.png scripts/add-sicilian-monolith-and-osiris-wire-batch.py
git commit -m "Sicilian monolith + Osiris Shaft wire batch: +1 site, +1 creator, +2 wires"
git push origin main
```
Netlify auto-deploys. Pre-flight rule: never let the live site count drop below the previous deploy.

## Gotchas
- Sandbox scratch disk fills up from large image renders (this session filled it). Periodically clean `/tmp` and `~/outputs`; if the shell won't launch, start a fresh Cowork session (files persist).
- Fourthwall mockups dim fine detail; the real print reads a bit stronger, but faint gold lines on dark are the genuine DTG risk. Sample before publishing.
