# Fourthwall Print Specs — Launch SKUs

Harvested live from the product designers (DOM-as-API method, 2026-06-11).
Pixel sizes = inches x dpi. Author files at exact pixel size, nearest-
neighbor scaling only (protects stitch crispness).

## Next Level Premium Fitted Long Sleeve Crew (base $19.58, Black)
| Placement | Area | Pixels |
|---|---|---|
| Front | 12" x 16" @150dpi | 1800 x 2400 |
| Back | 12" x 16" @150dpi | 1800 x 2400 |
| Left/Right Sleeve | 3" x 12" @150dpi | 450 x 1800 |
| Inside Label | 3" x 2.25" @150dpi | 450 x 338 |

Files built: `crew-front-1800x2400.png`, `crew-inside-label-450x338.png`.

## Enhanced Matte Paper Poster (Allcolor P001)
Offered sizes (2:3 only, locked in the hidden draft product): 12x18
($11.50 base), 20x30 ($13.00), 24x36 ($18.00). Source art 300dpi+
accepted; we author at 5400x7200 or larger.

## SUPERSEDED: full catalog harvested 2026-06-11
All 348 products (dims, dpi, colors+hex, sizes, surcharges, min orders)
via the public API: `GET api.fourthwall.com/api/products` (index) →
`/api/products/slug/{slug}?allVariants=true` (detail + generator id) →
`/api/generators/{gen_id}` (regions[].dimensions = inches/pixels/dpi).
No auth required. See `FOURTHWALL_CATALOG.md` (readable) and
`fourthwall_catalog.json` (machine-readable). Note: API label areas are
bounding boxes; the designer badge (e.g. inside label 3x2.25) is the
usable area — trust the smaller number for art.

## The harvester (paste into the designer page console, or Claude runs it)
```js
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const results = {};
  const badgeRe = /(\d+(?:\.\d+)?"?\s*x\s*\d+(?:\.\d+)?")\s*\((\d+)\s*dpi\)/i;
  const readBadge = () => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) {
      const m = n.textContent.match(badgeRe);
      if (m) return m[1] + ' @ ' + m[2] + 'dpi';
    }
    return null;
  };
  const labels = ['Front','Back','Left Sleeve','Right Sleeve','Inside Label','Outside Label'];
  const nodes = [...document.querySelectorAll('*')].filter(el =>
    labels.includes((el.textContent||'').trim()) && el.children.length === 0);
  const clicked = new Set();
  for (const el of nodes) {
    const name = el.textContent.trim();
    if (clicked.has(name)) continue;
    clicked.add(name);
    (el.closest('button,[role=button],div[class]')||el).click();
    await sleep(900);
    results[name] = readBadge();
  }
  console.log(JSON.stringify(results, null, 2));
  return results;
})()
```

## Method notes (the API spelunking ladder)
1. **Watch network traffic** as the page loads (attach monitor BEFORE
   navigation; caching can hide refetches).
2. **Read embedded SSR state** — Next.js apps ship data in
   `self.__next_f`; product pages carry `printAreas` JSON.
3. **Grep public JS bundles** for endpoint strings — found
   `/api/customization/*`, `/api/knitwise/*` etc., but the API base
   host is injected at runtime (404 from page origin).
4. **DOM-as-API** — when the API hides, script the UI state and read
   the rendered values. Always works; slightly slower; brittle only
   if the UI text format changes.
