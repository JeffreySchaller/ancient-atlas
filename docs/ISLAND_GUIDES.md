# Corsica and Sardinia visual guides

New routes: `/islands/`, `/islands/corsica/`, `/islands/sardinia/`.

`data/island-guides.json` is the editorial and image-credit source. `scripts/build-island-guides.py` builds the pages, shared stylesheet, gallery filter script and public image-credit JSON. `scripts/build.py` runs it before generating the sitemap. All photos are locally hosted WebP derivatives of the credited Commons files; source and licence links are on each photo card. Some previews crop with CSS; opening the photo shows its complete composition.

Corsica includes 12 photographs covering torre, enclosures, passages, dolmens, menhir rows and carved figures. Sardinia includes six photographs of Su Nuraxi, Santu Antine and Santa Cristina. The guides distinguish architectural comparisons from unsupported claims of equivalence. No close Corsican counterpart to Santa Cristina or decorated Domus de Janas was verified in this survey.

## Film placement

The Sardinia guide gives the original Stone Riddles documentary the first film card. The Ancient Atlas episode with Jeff and Gerald appears as a separately labelled conversation, with source footage credited to Stone Riddles. Haswell Travelled's Su Nuraxi film is the third card. All cards link to original films; channel and mapped-site links encourage exploration of other creators. No creator ranking, mapped walkthrough or existing video association was changed.

The new Ancient Atlas episode is added only to the channel catalog's conversation lane. Its exact title and channel were verified with YouTube oEmbed on 24 October 2026. It is not presented as an original field walkthrough.

Discovery is through the existing homepage's mobile editorial strip and desktop Atlas tooltip. Existing creator-study links remain in place. The separate creator-focused Sardinia watch-guide PR is complementary; this change does not alter its route or data.

## Validation

- Full build and existing conversation fixtures passed.
- Existing video audit completed; existing associations preserved.
- Desktop (1440px) and mobile (390px) browser checks passed for all three pages: no horizontal overflow, local images decode, filters and counts work, no JavaScript errors.
- Corsica's full photo content remains available without JavaScript.
- Source, licence and internal-link checks performed; sitemap includes all three routes.

## Research references

- Collectivité de Corse: Cucuruzzu–Capula and Cauria monument pages.
- Filitosa official site: architecture and corbelled construction.
- UNESCO: Su Nuraxi (833) and Domus de Janas (1730).
