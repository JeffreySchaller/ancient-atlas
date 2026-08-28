# The conversations lane

*A walkthrough shows you a place. A conversation shows you a person thinking about places.
They are different objects and the data should say so.*

**Files** `data/conversations.json` · `data/conversations.schema.json` · `scripts/verify-conversations.py`
**Status** Phase 1. The data contract and its verifier exist. **Nothing renders it yet** — see *Not built yet*, below.

---

## Why this exists

`data/feature.json` holds exactly one `interview`, one `reply`, one `featured_study`. It is a
singleton. The Ageless Rock episode occupies it now; the next episode overwrites it. Creator
Conversations is the flagship format and it has nowhere that holds more than one.

The instinct to fix this by wiring episodes into `videos.json` is wrong, and the repo already
says so twice. `creators.json.ancientatlas.subs` reads *"First-party fieldwork · the channel of
theancientatlas.com"*, and `feature.json` carries the ruling in a note: *"Not a site walkthrough,
so it lives here rather than in videos.json."*

---

## The rules

Nine. Each can fail, and `scripts/verify-conversations.py` proves it does with a named-rule
assertion per fixture.

| # | Rule | Number | Fails when |
|---|---|---|---|
| **R1** | Walked or discussed, never both. A video belongs in `videos.json` only if the camera was at the site. | 0 IDs shared, checked across **every** copy of `videos.json` | an episode id **or a reply id** also appears in videos.json |
| **R2** | Every `guest` is an existing key in `creators.json`. | 100% resolve | the key is absent — the message names the record to create |
| **R3** | `guest` is never `ancientatlas`. The host is implicit; a conversation is defined by someone else being in it. | 0 host-guest entries | a first-party walkthrough is moved in: R1 and R3 both fire |
| **R4** | Sites resolve by **exact** string match against `data/sites.json`. | 100%, no fuzzy matching | a near-miss spelling is used |
| **R5** | Every entry is reachable: ≥1 site **or** a `study` slug whose page exists on disk. | ≥1, and the file must be there | both empty, **or** the slug resolves to no page |
| **R6** | IDs are 11 URL-safe characters and unique within this file, replies included. | 11 chars, 0 duplicates | an episode is entered twice, or an id is truncated |
| **R7** | The featured slot is a pointer, never a store, and the collection is non-empty. | ≥1 stored, pointer resolves | the pointer aims at nothing, **or the file is empty** |
| **R8** | Release state is coherent: a real id needs a past `published`; an empty id needs `status: "coming"`; never both. | 0 future-dated, 0 contradictions | an unreleased episode is dated forward instead of marked coming |
| **R9** | Field hygiene: required fields present, no fields the schema does not allow. | schema `allowed_fields` only | an invented key silently joins the data |

**R3 is the swap test.** Substitute a walkthrough for a conversation; if the spec notices
nothing, it encodes nothing. It notices.

**On R4's number.** `sites.json` is not ASCII-normalised. It carries `Kaymakli Underground City`,
`Ağırnas Underground City`, `Aydıntepe Underground City`, `Nemrut Dağı`. The near-miss runs both
directions: typing `Kaymaklı` with a dotted i fails, and so does typing `Nemrut Dagi` in ASCII.
Exact match is the only safe rule.

---

## Corrections made under adversarial review

An adversarial pass found **20 defects** in the first draft of this instrument. Four were
substantive enough to be worth recording, because each is a failure mode this lane will meet again.

**The verifier passed an empty file.** R7 only ran `if featured_id:`, and `feature.json`'s
documented pre-release state is `interview.id = ""`. So in the state the repo calls normal, R7
switched itself off and an entirely empty `conversations.json` scored a clean pass. R7 now checks
`min_entries` unconditionally.

**R5 could be satisfied by fabrication.** Any non-empty string passed as a `study` slug.
`study: "this-study-does-not-exist"` returned zero findings, while `public/creators/` holds three
files. The rule's stated failure — *nothing on the map links to it* — was the one thing it could
not detect. The slug is now resolved against the filesystem.

**Replies were entirely unvalidated.** A `reply` block containing a real `videos.json` walkthrough
id and a date in 2099 returned zero findings, straight through the middle of R1 and R8. Reply ids
are now first-class: shape-checked, de-duplicated and lane-separated.

**R6's rationale was cited backwards.** The draft claimed *"videos.json has 997 entries and no
duplicates."* It has 997 rows and **908 unique ids**: 34 ids appear more than once, one of them
eleven times. That duplication is correct there, because the file is keyed by site and one video
can cover seven. Uniqueness is therefore a **new** requirement of a flat conversations list, not
an inherited precedent. The satisfying fact was the wrong one.

Two smaller corrections: `getCreatorStats()` seeds from `CREATORS` before walking `VIDEOS`, so
"walks VIDEOS and nothing else" was false, though the conclusion survives. And the seed entry for
the SOLSTICE HUNTER episode originally asserted Peru fieldwork and a Cusco-to-Cambodia framing
that **no record in this repo supports** — `solsticehunter` has exactly one row in all 997 videos,
at Phnom Bok. That claim came from conversation, not data, and has been removed.

---

## Failure modes, by shape

**The tidy-up.** An episode gets wired to `videos.json` because it is easier than adding a file. A
viewer clicks "jump to the site it covers" and lands somewhere the camera never went. R1, R3.

**The name-drop inflation.** Forty sites mentioned in passing, forty sites listed, every site page
diluted. Not mechanizable. The editorial test: *would a viewer arriving from that site page feel served?*

**The overwrite.** A new episode replaces the old in `feature.json` and the previous conversation
stops existing. The bug that prompted this. R7.

**The near-miss site.** `Kaymaklı` for `Kaymakli`. Renders as nothing, fails silently, reviews
clean. R4.

**The confident seed.** Filling a new entry from memory rather than from the record. Caught in
this document's own first draft.

---

## Not built yet

Naming this plainly, because a spec that implies working software is its own defect.

1. **Nothing reads `data/conversations.json`.** No `public/data/` copy, no inlined const, no
   render path. Per the pre-commit hook's own doctrine, a JSON-only addition changes nothing a
   visitor sees.
2. **`feature.json` is still a store**, duplicating title, published and the whole reply block. It
   should shrink to a pointer once a renderer exists, or the two will drift.
3. **`scripts/set-interview.py` has no idea this file exists.** It writes an id and today's date
   into `feature.json` without consulting the collection, so the release command can point at
   nothing. R7 catches it after the fact; it should be prevented before.
4. **The Creator Hub needs a fifth grouping** beside Curated, A–Z, By Site and Latest.
5. **The Creator Hub needs a conversation count** in `getCreatorStats()`, which currently
   seeds from `CREATORS` and then walks `VIDEOS` only.

---

## Deliberate omissions

Recorded so they are not re-litigated. The repo already keeps decisions like this — see the GEM
Museum walkthrough, unwired because a modern museum is not an atlas site.

**EP02, the Brent Slava conversation, is deliberately not entered.** Recorded 15 August 2026 and
published, but Brent is a fellow traveller from the Egypt trips rather than a channel owner. He has
no handle, no subscriber line and no colour, and `creators.json` is a registry of channels. Rather
than invent a record to satisfy R2, the episode stays out. Decision taken 2026-08-27.

**This exposes a known limit, not an oversight.** R2 assumes every guest publishes. Most of the
interesting guests over time will not. If a second non-channel guest appears, the fix is an optional
`guest_name` plus an explicit `no_channel: true`, with R2 relaxed to accept either a `creators.json`
key or a declared bare name — so the absence is stated rather than faked. Not built, because one
case is an anecdote and two is a pattern.

---

## Checklist

1. `python3 scripts/verify-conversations.py` exits 0
2. Guest has a `creators.json` record, tier chosen deliberately
3. Every site named is one the episode genuinely serves, not a name-drop
4. Unreleased episodes carry `id: ""` and `status: "coming"`
5. `feature.json.interview.id` still points at a stored entry
6. The episode is **not** also in `videos.json`

---

## What this cannot do

It cannot tell you whether the camera was at the site. R1 is load-bearing and is the one judgement
call in the set; the verifier only catches the case where the same id sits in both files.

It cannot tell you whether a site is genuinely discussed or merely mentioned, which is the
distinction deciding whether a site page is enriched or diluted.

It cannot make an episode worth watching. This removes the obvious ways for the conversations lane
to be wrong. It protects the floor; it does not raise the ceiling.
