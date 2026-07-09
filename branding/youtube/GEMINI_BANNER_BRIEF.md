# Gemini Banner Brief — "The Trio at Giza"

Goal: a Top Gear-style trio promo (Clarkson/May/Hammond formula) of Jeff,
Cody, and Gerald at Giza, used as the photographic plate for the YouTube
banner. Gemini generates the PLATE ONLY. No text in the image: the wordmark,
tagline, and site count get composited afterward from the brand pipeline
(crisp type, correct fonts, regenerable).

## Why the reference works (steal these, name them in the prompt)

1. Low camera angle, slightly below chest height: makes the trio monumental
2. Center figure half a step forward, hands clasped low: the anchor
3. Flankers angled 15-20° inward, weight on back foot: closes the triangle
4. Long empty ground plane receding to a low horizon: scale
5. Big moody sky, two-thirds of frame: drama without props
6. Desaturated cinematic grade, faces a stop brighter than the scene

## Photo prep (before prompting)

- 2-3 photos per person: one frontal face in good light, one 3/4 body.
  Sharpest available; Gemini matches likeness from what it sees.
- One group shot if available (helps relative heights).
- The Top Gear reference image itself, as the composition guide.
- Feed all images in one conversation and label them in the prompt
  ("Image 1 is Jeff...").

## Master prompt (paste, then attach images)

> Create a cinematic 16:9 promotional photograph of the three men from my
> reference photos standing on the Giza plateau in Egypt, in the exact
> composition style of the attached three-presenter promo image.
>
> Composition: the man from [JEFF IMAGES] stands center, half a step
> forward, hands clasped low. The man from [CODY IMAGES] stands to his
> left, the man from [GERALD IMAGES] to his right, both angled slightly
> inward. Camera at chest height, shooting slightly upward. Frame them
> waist-up, with all three heads at the VERTICAL CENTER of the frame,
> not the top third. Leave the left third of the frame open: empty
> plateau and pyramids, no people.
>
> Setting: the Great Pyramid and the pyramid of Khafre behind them on
> the left, hazy with distance. Late golden hour, low warm light from
> the left, long soft shadows on the sand.
>
> Wardrobe: practical field clothing they wear in the photos. Keep faces
> exactly as in the reference photos: same likeness, no beautification.
>
> Grade: cinematic and slightly desaturated, deep near-black shadows,
> warm champagne-gold highlights (#C9A84C tones), faces about one stop
> brighter than the scene. No text, no logos, no watermarks anywhere.

## Iteration prompts (common fixes)

- Likeness drift: "Make the center man's face match Image 1 exactly:
  [2-3 concrete features]. Change nothing else."
- Heads too high: "Move the camera back and down so all three heads sit
  at the vertical middle of the frame. Keep everything else identical."
- Plastic skin: "Natural skin texture, visible pores, documentary
  realism, not retouched."
- Sky too busy: "Simplify the sky: thin high haze, single tone gradient."

## Banner geometry (why the layout is what it is)

| Surface | What survives |
|---|---|
| Mobile/default | center 1546×423 band ONLY: faces must live here |
| Desktop | ~2560×423 band |
| TV | full 2560×1440 |

Trio on the RIGHT two-thirds with heads at vertical center → faces always
visible. Open LEFT third → wordmark + tagline get composited there, inside
the safe band, over a subtle obsidian scrim.

## Hand-back workflow

1. Export Gemini's best plate at maximum resolution, no text version
2. Drop it in `branding/youtube/` as `banner-plate-giza.png`
3. Claude upscales/letterboxes to 2560×1440 and composites the compass
   mark + THE ANCIENT ATLAS wordmark + tagline from the brand pipeline
   (same tokens as `generate-channel-assets.py`)
4. Review against all three crop bands before upload

The vector banner (`banner-2560x1440.png`, dot-map version) stays in the
repo as the fallback and as channel art for anywhere a photo feels wrong.
