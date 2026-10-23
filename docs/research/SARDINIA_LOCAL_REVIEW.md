# Sardinia local creator review, 23 October 2026

Adds four films and four creators, two new pins (Nuraghe Losa and Nuraghe Arrubiu). Totals: 635 sites, 103 creators, 1,045 video/site associations. All prior creator/video associations retained. The repeatable script is `scripts/add-sardinia-local-batch.py`; curated guide content is `data/sardinia-guide.json`.

## Placement evidence

Metadata saved in `sardinia-local-review-2026-10-23.json` includes uploader identity, original title, date, duration, description and chapter list. Sampled original video frames at 90 and 180 seconds confirm on-site footage for Losa, Arrubiu and the Sardegna Turistica Santu Antine interview. Marco Mura was sampled at 90 and 130 seconds (interior and exterior). Browser playback errored; direct video frame extraction succeeded. This was a placement/footage review, not a full factual review of all commentary.

- Sardegna Sacra / Ilaria Montis: https://www.sardegnasacra.it/la-nostra-storia/ and https://www.sardegnasacra.it/team/ establish the Sardinia-based archaeology and guiding project. Video credits Prospettive Vegetali too; both are named in the guide.
- Sardegna Storica: uploader describes Alessandro Usai guiding Simona Scioni at Losa. https://cultura.gov.it/index.php/luogo/abbasanta-nuraghe-losa confirms the site context and names Usai as responsible. Guide credits both people and links the original channel.
- Sardegna Turistica: uploader identifies the on-site Santu Antine conversation with archaeologist Nadia Canu. Labelled as an on-site conversation in the guide, not a continuous walk.
- Marco Mura: uploader description identifies him as Sardinian, from Alghero, and living in the UK. Guide says originally from Alghero, not currently resident in Sardinia.

## New pins

Losa description: https://cultura.gov.it/index.php/luogo/abbasanta-nuraghe-losa ; coordinates 40.1169, 8.79007 from https://en.wikipedia.org/wiki/Nuraghe_Losa .
Arrubiu description: https://nuraghearrubiu.it/ (archaeological content only) and https://www.italia.it/it/sardegna/nuraghe-arrubiu ; coordinates 39°39′43″N, 9°17′51″E from https://nuraghearrubiu.it/index.php/come-raggiungere-il-nuraghe . No current opening hours or prices copied.

## Stone Riddles

https://www.youtube.com/watch?v=q0YNkMIt3BY is the full 8,380-second documentary (2:19:40), already linked at Su Nuraxi. Updated its original title and featured it prominently in the Sardinia guide. Five thematic chapter jumps follow YouTube's returned chapter metadata. They are not site-specific timestamp assignments, and no guessed new site links were added. Film authorship is credited to Stone Riddles / Mirko Kulig, with a direct channel link. The guide distinguishes the filmmaker's interpretations from the guided site visits.

## Visibility and validation

The guide provides direct original-film links, creator channel links, named guide/presenter credits, language/format labels and map links. Linked from the creator hub, Ancient Atlas catalog and the relevant static site pages; included in generated sitemap. Existing contributors remain in place.

Build and conversation fixtures pass. Browser checks cover 1440px desktop and 390px mobile, seven film cards, five chapter links, and horizontal overflow. Batch rerun is idempotent. Existing CI is mostly placeholder; manual checks remain necessary.

## Claude coordination

Handoff successfully sent via Claude Desktop in Ancient Atlas Website — Inventory & Handoff (Oct 2026), with Fable 5.1 High confirmed. Requested a read-only review and further local creator recommendations; Codex owns edits. Response pending at initial note creation.
