# Creator discovery: first batch

Reviewed 2026-10-23: all 26 public long-form films and 35 Shorts are in the searchable channel catalog. Fourteen field visits are mapped (eight existing plus six added), nine conversations and three museum films remain discoverable without speculative walkthrough pins. Shorts remain catalog-only. CC02, the published Solstice Hunter conversation, now links the discussed Angkor Wat and Ta Keo sites. Dendera interview sSxekluuFfc was removed from the draft walkthrough additions and retained as a conversation.

Final totals: 633 sites, 99 creators, 1,041 video/site associations. Every main-branch video and its creator association is retained. The channel page prominently links other creators before its film grid.

## Sardinia coverage queue

| Site | Videos | Creators |
|---|---:|---|
| Sardinia Nuraghi (Su Nuraxi) | 2 | stoneriddles, haswelltravelled |
| San Andrea Priù | 1 | megalithomania |
| Nuraghe Santu Antine | 1 | stoneriddles |
| Giants' Grave S'Ena e Thomes | 1 | stoneriddles |
| Sacred Well of Sa Testa | 2 | stoneriddles, megalithomania |
| Nuraghe Su Mulinu | 1 | stoneriddles |
| Hypogeum of Sas Puntas | 1 | stoneriddles |
| Nuraghe Santa Barbara (Bauladu) | 1 | stoneriddles |
| Iloi Complex (Sedilo) | 3 | stoneriddles |
| Protonuraghe Bruncu Madugui | 1 | stoneriddles |
| Nuraghe Serbissi | 1 | stoneriddles |
| Nuraghe Piscu | 1 | stoneriddles |
| Nuraghe Corbos | 1 | stoneriddles |
| Nuraghe Piricu | 1 | stoneriddles |
| Giants' Grave of Imbertighe | 1 | stoneriddles |
| Giants' Grave Mura Cuada | 1 | stoneriddles |
| Domus de Janas of Corongiu (Pimentel) | 1 | stoneriddles |
| Giants' Grave Su Mont'e s'Abe | 1 | stoneriddles |
| Sacred Well Is Pirois | 1 | stoneriddles |

## Repeatable intake

1. Collect public upload metadata for known creators; keep source channel, video ID, title and discovery date.
2. Compare IDs against both walkthroughs and conversations. Keep Shorts separate.
3. Match canonical site names and aliases. Review new places before creating pins.
4. Verify on-location footage versus commentary, accessibility and uploader. Record site timestamps for multi-site films. A title match establishes placement, not the truth of historical claims.
5. Prioritize missing coverage and independent viewpoints, including local Sardinian and Italian-language creators.
6. Review a small batch, build, validate, then publish. Maintain rejected and deferred candidates so they are not repeatedly rediscovered.

## Visitor journey

Site → choose a film with creator attribution → watch → explore nearby sites or another creator. Ancient Atlas films also offer a direct channel link. Keep the own-channel catalog accessible from the creator hub without pinning own films above all contributors.

## Review evidence

Uploader metadata and chapter lists are saved in `research/channel-review-2026-10-23.json` and `research/sardinia-review-2026-10-23.json`. The three accepted Sardinia films were also sampled during playback around 100–105 seconds to confirm on-location footage. This is placement review, not a full review of historical claims. Remaining candidates are tracked in `sardinia-candidates.json`.

New map films: Great Pyramid, Unfinished Obelisk, Sillustani, Moray, Coricancha and Paracas Candelabra. Paracas opens at the 0:57 chapter on the channel page. Its new pin uses OpenStreetMap way 173837516 coordinates via https://mapcarta.com/es/W173837516. Description sources: https://visitaareasnaturales.sernanp.gob.pe/en/anps/paracas-national-reserve/ and https://www.peru.travel/experiences/photography-of-the-paracas-candelabro . Date and makers are explicitly uncertain.

Validation: build.py, conversation fixtures, video audit, generated social image, desktop 1440px and mobile 390px browser checks, filters/search/empty state, no-JavaScript visibility and no horizontal overflow. Existing creator associations retained. CI is largely a placeholder and is not a substitute for these manual checks.

## Claude coordination

Claude Desktop's website inventory artifact was read: https://claude.ai/artifact/WnujQ1TDPWzxhdnw2zqLCs#97acd1fe-f933 . It provided prior website and Fourthwall context. A follow-up review of this batch has not yet been confirmed. The last readable model setting was Fable 5.1 Medium; the requested High setting could not be selected reliably through accessibility. Do not describe this as a completed Claude review.

Handoff for Claude: review PR #3 and its channel catalog, preserving other-creator prominence and all existing films. Review the remaining Sardinia candidates, prioritize local Sardinian/Italian-language on-location sources, and propose the next small evidence-backed batch. Coordinate before editing the branch.
