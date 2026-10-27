# Feature glyphs on the map

The map reuses the 24 published feature definitions and WebP tiles. Five initial browse filters use existing catalogue coverage: polygonal walls, fitted joints, water channels, underground spaces and rock-cut buildings. The selected glyph also appears on individual map markers. Clear feature restores the normal category markers.

Site badges appear before the films. Activating a badge moves focus to the first Watch here control, without starting playback or choosing a creator for the visitor. All films and creator jump links remain available. Sites without films link to the corresponding feature explanation instead. Filtering does not replace the active player.

## Assignment rules

- Existing polygonal and precision criteria map to polygonal and joints respectively. These are prompts for observation, not measured tolerances or proof of a particular construction method.
- Existing underground and rock-cut categories map to the corresponding glyphs.
- Explicit additions live in data/site-features.json. Tipón channels/terraces and Petra channels are already described in their catalogue records and the Supporting life essay. Santa Cristina storage/corbelled roof is documented in the site's Sardegna Turismo source.
- Do not infer video-level coverage from site badges. No individual film has been newly tagged or retimestamped.
- This is a partial catalogue of features, not a comprehensive survey. Expand explicit mappings as sources and footage are checked; do not assign all 24 from keyword matches.

## Sharing card

scripts/render-atlas-og.cjs renders the 1200 × 630 card with Playwright/Chrome, using the map's actual compass SVG and existing glyph assets. It reads current site and creator counts. This replaces the earlier visual layout from regenerate-og-image.py; use the new renderer for future updates. Main-map Open Graph and Twitter URLs have a new cache version. Already-cached previews may persist on sharing services.

Validation: scripts/test-map-features.cjs exercises mobile and desktop filters, clear, badge-to-film focus, both Tipón creators, embedded playback and player persistence through filtering.
