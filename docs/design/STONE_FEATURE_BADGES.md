# Stone feature badges — 26 October 2026

Status: local design preview; not published. Claude Desktop coordination attempted, but navigation did not change the visible accessibility tree. Model control reported Fable 5.1 Medium. No brief confirmed sent and no Claude review received.

## Purpose

Help a visitor decide what they can actually see in a film. Use recurring visual features to connect geographically distant sites, while keeping creators, original titles and Watch here prominent. Similar appearance is a reason to compare, not evidence of common builders, age or technology.

## Visible vocabulary

Six definitions and SVG paths live in data/site-character-icons.json:
- Polygonal walls: irregular, many-sided blocks fitted into a wall.
- Stone joints: a close view of how worked stone faces meet.
- Rock-cut spaces: spaces or architectural forms cut into bedrock.
- Waterworks: channels, basins and other visible water-management features.
- Large stones: large blocks or monoliths with a visible sense of scale.
- Surface marks: visible marks and textures on worked stone.

Retain the legacy precision key for compatibility; display Stone joints to avoid presenting visual fit as a measured engineering tolerance. Rock-cut describes a construction approach, not material hardness. Record stone type separately with a source. Water-channel function may require verification even where a carved groove is visible.

## Presentation

One shared stroke weight, rounded line ends, warm neutral gold, a softly rounded square tile and a visible text label. No icon-only meanings. At compact size, use 24px glyph / 40px tile / 12px radius; specimen board uses 36px glyph / 64px tile / 18px radius. Noninteractive badges must not look or behave like buttons. Any future filter version requires focus, pressed state and an explicit accessible name.

Use at most three relevant badges per film, selected by verified visible content. Follow with one short observation, keeping Watch here a consistent action. Do not copy every site's category onto every film. Existing site-level badges remain site-level; new families are not assigned automatically.

## Detailed evidence record

For each site-film observation retain:
- site ID/name and YouTube video ID; creator key and original title
- feature family and specific subfeature
- start/end timestamps and factual viewing cue
- evidence source: direct footage inspection, transcript, chapter or independent source
- reviewer and date; pending / reviewed / disputed status
- observation separate from interpretation
- material, dimensions and precision measurements only when sourced, with units and method
- sources for chronology and proposed function, separate from what the film shows

A timestamp is a source locator, not evidence by itself. Confirm footage before displaying a claim. No per-video claims have been created in this pass.

## Pending example review

The user's coastal Stone Riddles channel example may refer to Cosa; exact film and channel still need identification. Compare only verified observations with examples from Israel and Peru. Petra is a candidate for rock-cut architecture; do not label it hard stone by analogy. These are research leads, not new site classifications.

## Rollout

Local preview is /badge-preview.html. Existing three badge types use the new container on local map and static pages. Added families are vocabulary only. Map markers, category icons, navigation symbols and the Ancient Atlas brand mark need separate review against this family; the brand mark is not a site feature. Retain creator logos/credits unchanged.

## Brief for Claude Desktop

Jeff asks us to collaborate on a coherent Ancient Atlas visual vocabulary. Please review the six families above, suggest useful merges or missing distinctions, and help recover the earlier Ancient Atlas definitions from your records. Aim for observable features and thoughtful film-specific viewing expectations. Keep detailed material, chronology and measurement evidence behind the concise visible badges. Review rounded-square line glyphs, not replacements for creator identity or thumbnails. Identify the coastal Stone Riddles water-channel example if your records support it. Do not infer common origins from similar forms. Return proposed definitions and any evidence-supported changes; do not publish or edit the repository concurrently. This brief has not yet been delivered.

## Refinement and audience — 26 October 2026

Original icons were authored SVG paths. Higgsfield concept job 77db0bd8-7658-424e-a49c-88a24e278129 completed using gpt_image_2_5, one 3:2 sheet, quoted 0.25 credits. Result:
https://d8j0ntlcm91z4.cloudfront.net/user_3EKwOBOsqIIcj29EvrTwHGXIc6q/hf_20261026_233411_77db0bd8-7658-424e-a49c-88a24e278129.png

Concept explores limestone bas-relief, restrained gold edges, upper-left lighting, shallow bevels and contact shadows. It is a visual study, not production assets or factual site imagery. Generated labels explore Fitted stone, Water channels, Monumental stones and Carved details alongside Polygonal walls and Rock-cut spaces. These wording alternatives do not silently replace the taxonomy: Carved details does not encompass all surface marks, and Water channels is narrower than Waterworks.

Connected vidIQ channel analytics for Ancient Atlas, 2026-07-27 through 2026-10-25:
- Male 57.3%, female 42.6% (rounding total 99.9%).
- Age 55+ 34.6%; age 65+ 21.7%; age 25–34 23.6%.
- These are returned YouTube audience percentages, not website visitor demographics. No inference of occupation, education or technical expertise.
- Source: vidiq_channel_analytics audience_demographics, channel UCMmnEB7cq_oQN2gKwEyyr5g.

Design hypotheses:
1. New visitors need literal, readable labels and a clear action.
2. Returning enthusiasts need useful distinctions and consistent visual recognition.
3. Visitors interested in construction need specific observable details and evidence, rather than generic mystery claims.
4. Travel-minded visitors need a sense of scale, surroundings and on-site experience.

These are use cases, not measured audience segments. Six stone-feature families are a pilot, not a comprehensive taxonomy for the ancient world. Keep site type, visible feature and film format separate. Check possible missing themes (carvings/art, underground spaces, landscape/setting) against actual films and visitor comprehension before expanding.

Next validation: compare flat and shallow-relief icons at 24, 40 and 64px; require plain labels, adequate contrast and distinct silhouettes. Ask newcomers and experienced viewers what each means before naming it. Test whether each badge predicts footage content. Restrict displayed badges to 1–3 per film after footage review. Keep Watch here and creator identity more prominent than icon ornament.
