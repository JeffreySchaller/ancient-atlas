# Ancient Atlas — YouTube Channel Setup

One-pass setup guide. Assets live in `branding/youtube/`. Regenerate any time
with `python3 branding/youtube/generate-channel-assets.py` (the banner pulls
the live site count from `data/sites.json`, so rebuild it when the atlas grows).

## 1. Channel identity

| Field | Value |
|---|---|
| Channel name | **The Ancient Atlas** |
| Handle | `@theancientatlas` (fallbacks: `@ancientatlasmap`, `@theancientatlas_com`) |
| Model | One brand, credited hosts. Each video credits who walked it (Jeff, Cody, Gerald). The channel is the atlas, not a personality. |
| Account | Create as a **Brand Account** (YouTube Studio → create channel → "Use a business or other name"), so Cody and Gerald can be added as Managers later without sharing a personal login. |

## 2. Channel art

| Asset | File | Where |
|---|---|---|
| Profile picture | `avatar-800.png` | Studio → Customization → Branding |
| Banner | `banner-2560x1440.png` | Same page. All text sits inside the 1546×423 safe area, full image shows on desktop/TV. |
| Video watermark | `watermark-150.png` | Same page. Display: "Entire video". |

## 3. About / description copy

**Channel description** (final, 2026-06-10). Editorial stance: GUESTS ARE
THE SHOW. Fieldwork walkthroughs are launch content + standing credibility
("we walk sites too"), not the channel's focus. No site count by design:

> Three friends in conversation with the people walking the world's
> ancient places : : explorers, filmmakers, and researchers of the
> deep past.
>
> We sit down with the creators documenting ancient sites: their
> expeditions, their open questions, the places that keep calling them
> back.
> And we do the walking ourselves: original fieldwork from Türkiye,
> Egypt, and wherever pulls us next.
>
> Every guest and every site lands on theancientatlas.com, a
> hand-curated interactive map of the deep past, organized by region,
> era, and the questions still standing.

**Links block:** theancientatlas.com (primary) · contact email.

## 4. Upload defaults (Studio → Settings → Upload defaults)

- Title format: `SITE NAME | Fieldwork Walkthrough · Region`
- Description boilerplate (bottom of every video):

  > Walked by: [HOST]
  > Site on the atlas: https://theancientatlas.com/#/site/[SITE]
  > The Ancient Atlas is a hand-curated map of 559+ ancient sites: https://theancientatlas.com
- Tags: ancient sites, megalithic, archaeology, [site name], [region], fieldwork
- Category: Education · License: Standard · Visibility default: Private (publish deliberately)

## 5. Playlists (create before first upload)

Pillar order reflects the channel's center of gravity: conversations
first, fieldwork as launch content and standing credibility.

1. **Creator Conversations** — THE FLAGSHIP. Interviews with the people
   walking and documenting ancient sites. The atlas's 55+ wired creators
   are the guest list (Hugh Newman at 81 wires, Anthony Murphy, and the
   Mr.mountainbeast outreach are natural first invitations)
2. **Fieldwork: Full Site Walkthroughs** — single launch playlist that
   establishes the hosts as part of the empirical-exploration community.
   Description: "Our boots on the ground. Full, unscripted walkthroughs
   of the ancient sites we visit ourselves: the underground cities of
   Türkiye, the temples and plateaus of Egypt, and wherever pulls us
   next. Filmed the way we found them. / Every site lands on the atlas,
   beside the work of every creator we've curated:
   https://theancientatlas.com". Split into Fieldwork: Türkiye /
   Fieldwork: Egypt once the library passes ~8-10 videos
3. **Atlas Reveals** — new sites and walkthroughs surfacing on
   theancientatlas.com, presented by the hosts (between-interview cadence
   filler that keeps the channel alive between guests and trips)

Add playlists only when content exists (honesty over completeness
applies to playlists too).

## 6. Per-video metadata template

```
Title:    Göbekli Tepe | Fieldwork Walkthrough · Türkiye
Host:     Jeff
Thumb:    thumbnail-template-1280x720.png layout:
          footage still left 65%, obsidian panel right:
          FIELDWORK badge / region in mono caps / site name in Fraunces /
          "Episode NN · walked by [host]" / compass mark
Chapters: 0:00 Approach · then one chapter per structure/feature
Pinned comment: link to the site's atlas card + one open question
```

## 7. Wiring uploads into the atlas (next phase)

When the first video is live: add creator key `ancientatlas` to
`data/creators.json` (tier 1, champagne #C9A84C), then wire each upload to
its site in `data/videos.json` via a standard batch script
(`scripts/add-ancientatlas-fieldwork-batch.py`, copied from the
`add-hugh-newman-batch.py` template). First-party walkthroughs follow the
same editorial rules as every other creator. No special treatment on
`signal:open` sites: pair perspectives as usual.

## Launch order

1. Create Brand Account + handle
2. Upload avatar, banner, watermark
3. Paste About copy + links
4. Set upload defaults
5. Create 3 playlists
6. Upload Türkiye + Egypt walkthroughs as Private
7. Thumbnails per template, metadata per template
8. Publish in sequence (one per day beats all-at-once for a new channel)
9. Run the atlas wiring batch (section 7)
