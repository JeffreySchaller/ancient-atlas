# Automation Roadmap

> Goals stated towards full automation in some cases.

The atlas evolves from "Jeff manually edits a giant HTML file" to a self-maintaining editorial platform in four phased weeks. Each phase delivers a working version of the atlas with progressively more automation.

The phases are ordered so each one's output becomes the next one's input. Skipping a phase breaks the chain.

---

## Phase 1 : GitHub foundation (Week 1)

**Goal :** Source of truth moves to a public GitHub repo. Netlify auto-deploys on push to main. The atlas keeps working without behavior change for users, but contributors can now submit PRs.

| What ships | Automation level |
|---|---|
| `ancient-atlas` public GitHub repo | — |
| `data/sites.json`, `data/videos.json`, `data/creators.json` extracted from `index.html` | manual extract once |
| `scripts/build.py` reassembles `public/index.html` from `data/` files | runs locally, optionally in CI |
| Netlify connected to repo → auto-deploys on push to main | **fully automatic** |
| `README.md`, `CONTRIBUTING.md`, `LICENSE` published | — |
| `audit-videos.py` and `generate-og.py` moved to `scripts/` | — |

**End-state by Friday of week 1 :** Jeff, Gerald, and Cody can each open PRs against the JSON files. Pushes to main trigger Netlify rebuilds within 60 seconds. The atlas's user-facing behavior is identical to today.

---

## Phase 2 : Contributor experience + CI quality gates (Week 2)

**Goal :** Friction for contributors drops to near-zero. Every PR is automatically validated. Bad data never reaches main.

| What ships | Automation level |
|---|---|
| `/contribute.html` page with **single-URL mode** | — |
| `/contribute.html` **bulk mode** (paste up to 25 URLs at once) | — |
| YouTube oEmbed verification at the contribute page (instant feedback before PR) | **fully automatic** |
| GitHub Actions CI workflow runs on every PR | **fully automatic** |
| CI check 1 : **oEmbed verification** (confirms creator + title for every new video) | **fully automatic** |
| CI check 2 : **duplicate detection** (re-runs `audit-videos.py` against the PR's branch) | **fully automatic** |
| CI check 3 : **schema validation** (every JSON entry has required fields with correct types) | **fully automatic** |
| `PULL_REQUEST_TEMPLATE.md` guides contributors through the editorial checklist | — |
| `ISSUE_TEMPLATE/new-site.md` for proposing new sites | — |

**End-state by Friday of week 2 :** Cody pastes a URL into the contribute page → page verifies it → opens a PR → CI runs and shows ✓✓✓ within 30 seconds → maintainer merges in one click → atlas updates within 60 seconds. End-to-end < 5 minutes per addition.

---

## Phase 3 : Evergreen discovery (Week 3)

**Goal :** The atlas starts maintaining itself. New videos from existing creators are discovered automatically and surfaced for editorial review.

| What ships | Automation level |
|---|---|
| GitHub Actions cron workflow runs daily at 09:00 UTC | **fully automatic** |
| Workflow polls the YouTube RSS feed for each of the 32 registered creators | **fully automatic** |
| New videos detected → cross-referenced against `data/sites.json` for keyword matches | **fully automatic** |
| **High-confidence matches** : workflow opens a draft PR with the entry pre-populated and labeled `auto-draft` | **fully automatic** |
| **Low-confidence matches** : workflow adds to `data/review-queue.json` for contributor review | **fully automatic** |
| `/review-queue.html` page lists pending videos and lets contributors assign sites | manual review |
| Editorial review of auto-draft PRs becomes the maintainer's primary workflow | manual review |

**End-state by Friday of week 3 :** When Brien Foerster uploads a new walkthrough, within 24 hours there's a draft PR waiting in the maintainer's inbox with the entry pre-filled. One review, one merge. The atlas absorbs new content with near-zero manual discovery effort.

---

## Phase 4 : Community + mission infrastructure (Week 4)

**Goal :** The atlas becomes a *cause* for ancient-site exploration. Visitors are encouraged to film their own walkthroughs at lesser-known sites. The editorial mission gets architectural support.

| What ships | Automation level |
|---|---|
| `/atlas-calling.html` page listing sites with 0–1 walkthroughs, filtered by region | regenerated on each build |
| **"Filmed for the Atlas" badge** : visual mark on videos created in response to the assignment desk | manual flag in JSON |
| Contributor leaderboard at `/contributors.html` showing PR counts and tenure | regenerated on each build |
| Tier-based self-merge privileges (5 PRs → existing sites, 20 PRs → new sites, 50 PRs → editorial team) | manual but documented |
| OG image regeneration on every build via `generate-og.py` in CI | **fully automatic** |
| Auto-attribution : when an editorial-team contributor merges, their name appears in the commit + the contributor page | **fully automatic** |
| Public Discord or community space for editorial discussion (optional, if traction warrants it) | manual |

**End-state by Friday of week 4 :** The atlas is no longer a one-person catalog. It is a platform that other people contribute to, that generates assignment-desk surfaces for content creators, and that auto-discovers new content as it's published.

The transformation Jeff described after traveling with UnchartedX, Yousef, and Brothers of the Serpent — being changed by direct contact with these places — now has architectural support : the atlas points visitors toward the same kind of trip, and rewards those who come back with a camera.

---

## Phase 5+ : The "if we get traction" moves

These are not on the 4-week plan. They're the next horizon if the atlas grows beyond the editorial team.

| Possible | When |
|---|---|
| Netlify Edge Function for per-site OG meta tags (Dolmen of Menga's preview shows Dolmen, not just brand) | When share volume justifies it |
| Server-rendered per-site pages at `/site/dolmen-of-menga.html` | If SEO becomes a priority |
| Tour partnership program (atlas-affiliated travel) | If contributor base reaches ~20 |
| Patreon / Ko-fi integrations beyond the current "Support" link | If audience reaches ~5k MAU |
| API for third-party clients (Wikipedia editors, academic researchers) | If repeat data requests appear |
| Multi-language support (Spanish, Portuguese for Andean content; Hindi for Indian sites) | If non-English audience grows organically |

---

## Automation tier summary

After Phase 4, here's what runs without human intervention :

- ✅ Site deploys on every push to main (Netlify)
- ✅ Build script reassembles index.html from JSON files (GitHub Actions on push)
- ✅ Every PR is verified for oEmbed + duplicates + schema (CI)
- ✅ New creator uploads are discovered daily and turned into draft PRs (cron)
- ✅ OG image regenerates with current site count on every build (CI)
- ✅ Copyright year updates on every page load (client-side JS)
- ✅ Audit script runs on every PR (CI)

What still requires a human :
- ❌ Editorial judgment ("is this video atlas-worthy?")
- ❌ Site additions (lat/lng research, era determination, civilization attribution)
- ❌ Library entries (writing the deep articles)
- ❌ Brand and design evolution
- ❌ Approving auto-draft PRs from the evergreen workflow

That's the right division of labor. Automate the mechanical work. Reserve human attention for editorial judgment.

---

## How to track progress against this roadmap

Each phase has a milestone in GitHub Issues. Issue tags :

- `phase-1-foundation`
- `phase-2-contributor-experience`
- `phase-3-evergreen`
- `phase-4-mission`

Open issues against the current phase. Close them as they ship. The phase moves when its issues are all closed and the end-state criteria are met.

---

## The editorial through-line

Every automation choice serves the same editorial goal : **the atlas should grow without losing its voice or its rigor.**

Automation handles discovery and verification. Humans handle judgment. The atlas catalogs more sites, surfaces more walkthroughs, and reaches more readers — without becoming a YouTube-recommendations slurry. The friction lives where it should : at the editorial moment, not at the contribution moment.

That's the goal.
