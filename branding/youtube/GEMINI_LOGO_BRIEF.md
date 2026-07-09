# Gemini Logo Brief — Compass Mark Refinement

Goal: evolve the programmatic compass rose (avatar-800.png) into a finished
brand mark. Same identity, more craft: the current mark is geometrically
correct but mechanically flat. Attach `avatar-800.png` as the reference.

## What "more like a brand logo" means here

1. Weight balance: the long cardinal points are too thin at the tips,
   the short diagonals too stubby; a drawn mark tapers with intent
2. Optical centering and a hub that feels machined, not stamped
3. Facet shading with real edge logic (one light source), not two flat fills
4. A ring that relates to the star (echo, interrupt, or double-rule),
   not just a circle floating nearby
5. Subtle age: the champagne gold can carry a faint engraved/etched
   quality, like a cartouche on an old map plate

## Master prompt (paste, attach avatar-800.png)

> Refine this compass rose logo into a premium brand mark. Keep exactly:
> the 8-point compass star concept, the champagne gold (#C9A84C) on
> near-black (#0D0D12) palette, and the circular enclosure.
>
> Improve: give the star points elegant tapered proportions like a
> hand-engraved map compass, with faceted shading from a single
> upper-left light source. Make the center hub a small machined ring.
> Integrate the outer circle with the star: a fine double ring with a
> small break where each cardinal point crosses it.
>
> Style: flat vector brand mark, engraved cartography feel, luxury
> expedition brand. Crisp edges, no gradients except the facet shading,
> no texture noise, no text, no extra ornaments. Centered on a square
> canvas with even margins, suitable for a circular avatar crop.

## Variations to request (one at a time)

- "Same mark, but the ring is a single hairline interrupted only at north,
  with a tiny diamond at the north break" (favors the N of navigation)
- "Same mark with a faint meridian arc grid inside the circle, 8% opacity"
  (map-plate depth)
- "Monochrome version: single champagne color, no facets" (small-size test)

## Acceptance tests before adopting

1. Legible at 32px (favicon) and 150px (watermark): squint test
2. Survives circular crop with no clipped points
3. Reads as one mark, not star + circle
4. Sits comfortably next to Fraunces type (engraved serif kinship)

## Hand-back workflow

1. Save the winner as `logo-mark-gemini.png` in `branding/youtube/`
2. Claude recrops to 800x800 avatar, regenerates the 150px watermark and
   32/256px favicon sizes from it, and swaps it into the banner composite
3. Old programmatic mark stays in `generate-channel-assets.py` as fallback
