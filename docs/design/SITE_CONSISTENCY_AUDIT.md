# Site consistency inventory — 26 October 2026

Scope: 724 HTML documents (including the map), excluding two local research/design previews. 723 secondary documents now load the shared return-navigation component. Counts include an older standalone site page; they are not the count of active archaeological sites.

## Findings and current fixes

| Area | Finding | Local change / next work |
|---|---|---|
| Return navigation | Root destination alternately labeled Atlas, Map, or only a brand mark | Explicit Back to map control on secondary documents |
| Embedded articles | Root links can navigate inside the library iframe | Same-origin, frame-validated message closes the drawer and retains the existing map |
| Article drawer | Exit was a small × and Escape hint | Explicit Back to map footer action; Escape works from article focus |
| Page generation | Several independent generators and hand-authored pages | Shared navigation installer runs at the end of the main build |
| Typography / colors | Repeated inline palettes and CSS; near-black backgrounds vary; muted text and gold do many jobs | Shared navigation and player now use neutral charcoal/stone and restrained gold; full palette migration remains pending |
| Section vocabulary | Library vs Articles; Studies vs Creators; Sites vs map index | Requires coordinated naming across main nav, headings and breadcrumbs; not renamed blindly |
| Brand marks | SVG compass, star characters, text-only brand and raster mark coexist | Consolidate after visual review; creator identities remain separate |
| Experiences | Standalone packaged experience has a different page shell | Add explicit return route without rewriting the experience |
| Player | Previously repeated title/credit/link text | Compact movable player already prototyped; shared on map and static pages |
| Glyphs | Six generated Higgsfield concepts; 24 research feature candidates | Neither constitutes 24 production-ready icons |

## Color direction

Retain obsidian / ivory / champagne identity, but use shared semantic roles: canvas, surface, elevated surface, main text, secondary text, action and focus. Colored feature accents must have labels, not carry meaning alone. Do not globally replace arbitrary hex values: some belong to maps, charts, photographs or culturally specific illustrations.

Neutral player/navigation pilot:
- Surface #202124
- Text #EEEAE2
- Border #666159
- Focus / restrained accent #E1C77F

The source palette also contains ocean, moss, clay, violet and rose. Their use needs a defined role before broader rollout.

## Limits

Inventory is source-level across all documents; browser verification samples page families at mobile and desktop widths. This is not an exhaustive accessibility, contrast, external-link or editorial audit. No deployment in this pass. External store and YouTube navigation are outside the local-page installer.

Machine inventory: docs/research/site-consistency-inventory-2026-10-26.json.

## Verification

Browser checks passed at 390px and 1440px for article detail, library index, creators, island guide, site detail, patterns, photos, contact and Feel the Weight. The return control was visible and unobscured. Embedded article Back to map closed the drawer without navigating the parent map. The packaged experience's document replacement required navigation to be restored after rendering. Installer rerun is idempotent. Full visual harmonization remains a separate follow-up.
