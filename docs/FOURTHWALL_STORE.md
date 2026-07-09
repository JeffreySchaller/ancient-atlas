# Fourthwall Store — Launch Plan

## REVISED 2026-06-11: Capsule model (supersedes the 8-SKU lineup below)
Apple discipline: one design family per season, three price altitudes,
dropped and gone. Lineup below kept for reference; only the poster
exists (hidden draft).

### Capsule I · The Painted Ones — F/W 2026 drop
| Altitude | Product | Design | Target price |
|---|---|---|---|
| Flagship | Knitted Crewneck Sweater (Knitwise, real knit) | Mammoth medallion, knitted in | $95-120 |
| Middle | Heavyweight tee/crew (DTG, black) + 18x24 print | Full 5-band fair isle | $32-38 / $27 |
| Gateway | Embroidered beanie (5x1.75 front) or compass pin | Compass mark | $22 / $8 |

### Standing policies (write once, never violate)
1. **Drops, not catalog.** Each capsule colorway sells for a defined
   window (~4 weeks), then retires permanently. Next season = new
   colorway or new capsule, never a restock.
2. **No discounts, ever.** Atlas merch never goes on sale; it goes away.
3. **Sample gate.** Nothing publishes before a physical sample passes
   (gold-on-black DTG shift risk; knit gauge fidelity).
4. **Gerald veto** on every design surface, per the roles doc.
5. **Story before product.** Every drop ships with a 15-30s mini-doc
   (Shorts pipeline): cave wall → stitch chart → garment. The Wrangel
   Island line is the whole ad. Retention across capsules > ROAS.

### Knitwise panel spec (flagship)
Design area 1250x1400 px @300dpi (4.166" x 4.666"), TEMPLATE_KNITWISE,
file: `branding/merch-design/knit-panel-mammoth-1250x1400.png`.
Machines quantize to yarn palette; flat 4-hex chart input is ideal.

Status: assets built 2026-06-11 (`branding/print/make-merch.py`), store
setup pending. **Anchor everything to theancientatlas.com and Jeff's
personal email.** The YouTube channel connection waits until the account
appeal resolves; the store is independent of it by design.

## Store identity
| Field | Value |
|---|---|
| Store name | The Ancient Atlas |
| Fourthwall URL | ancient-atlas-shop.fourthwall.com (placeholder; claim closest) |
| Custom domain | shop.theancientatlas.com (CNAME at Hover after setup) |
| Tagline | A map of the deep past, on paper and cotton |
| Theme | Obsidian #0D0D12 bg · champagne #C9A84C accents · ivory #F0EEE9 text · Fraunces headings if theme allows |

## Launch lineup (8 products)
| Product | Asset | Suggested price | Notes |
|---|---|---|---|
| The Atlas Poster · 24x36 · 2026 Edition | `atlas-poster-24x36-2026.png` | $35 | Hero product. 560 sites, full map |
| Egypt · 18x24 | `poster-egypt-18x24.png` | $27 | 46 sites, tier-1 labels, Nile reads instantly |
| Türkiye · 18x24 | `poster-turkiye-18x24.png` | $27 | 79 sites; pairs with launch fieldwork |
| Compass Print · 18x24 | `poster-compass-18x24.png` | $25 | Minimal; the office-wall option |
| The Atlas Tee | front `merch-tee-front-light.png`, back `merch-back-dotmap.png` | $30 | Dark garments (obsidian/black/charcoal). Dark-ink variant for sand/ivory garments |
| Deep Past Hoodie | front `merch-tee-front-light.png` | $54 | Dark garments only at launch |
| Compass Sticker | `merch-sticker-compass.png` | $4 | Die-cut circle, 3in |
| The Atlas Mug | `merch-mug-wrap.png` | $18 | 11oz wrap; reposition in Fourthwall's mug editor |

Pricing logic: Fourthwall sets base cost per item; these targets keep
margins in the 35-55% band typical for creator stores while staying
under the impulse ceiling for each category. Adjust to the nearest
clean number after seeing actual base costs.

## Product descriptions (paste-ready)

**The Atlas Poster · 24x36 · 2026 Edition**
Every site on the atlas, plotted as a single field of light. 560
ancient places : : one map. Printed at 300dpi from the live dataset,
dated as the 2026 edition because the atlas keeps growing.

**Egypt · 18x24**
Forty-six sites from Tanis to Abu Simbel. The Nile draws itself.
Tier-one sites named, the rest left as points of light for you to
chase down on theancientatlas.com.

**Türkiye · 18x24**
Seventy-nine sites, from Troy to Göbekli Tepe. The Cappadocian
underground cities cluster at the center, exactly as they do in the
ground.

**Compass Print · 18x24**
The Ancient Atlas mark, alone on obsidian. For the wall that wants
one quiet object.

**The Atlas Tee**
Compass on the front, the entire atlas across the back : : 560 sites
in champagne and amber. Printed on heavyweight cotton.

**Deep Past Hoodie**
The compass mark and wordmark on heavyweight fleece. Made for site
mornings that start before the sun does.

**Compass Sticker**
Three inches of obsidian and champagne. Water bottles, field cases,
laptop lids.

**The Atlas Mug**
The full dot map wraps the cup. Coffee on one side of the world,
tea on the other.

## Collections
1. **Prints** — all four posters
2. **Field Kit** — tee, hoodie, sticker, mug

## Setup checklist
- [ ] Create Fourthwall account (Jeff's personal email)
- [ ] Claim site name, set theme colors to brand tokens
- [ ] Upload 8 products, set prices after reviewing base costs
- [ ] Order samples of poster + tee before promoting (quality gate)
- [ ] Connect shop.theancientatlas.com (Hover CNAME)
- [ ] Add Shop link to theancientatlas.com nav (pre-flight count check before push)
- [ ] AFTER YouTube restoration: connect channel for merch shelf
- [ ] Defer paid promotion of the store until the channel situation is settled

## Asset specs (for upload screens)
Apparel art: 4500x5400 transparent PNG, 300dpi (15x18in print area).
Sticker: 1500x1500 transparent, die-cut circle. Mug: 2700x1100 full
bleed. Posters: 5400x7200 (18x24) and 7200x10800 (24x36), RGB; let
Fourthwall handle color conversion.
