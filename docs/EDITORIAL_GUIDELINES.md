# Editorial Guidelines

> The atlas writes with a particular voice. Editorial discipline is what separates it from a YouTube playlist.

This document captures the standard for what goes in, what stays out, and how the atlas speaks. Apply it to PRs, issues, and any text-bearing contribution.

---

## The atlas's voice

| Principle | What it looks like in practice |
|---|---|
| **Answer first, then mechanism, then forward-opening close** | "Six properties recur at the most demanding sites. Each is a question worth holding in mind." (lead with the claim, support it, leave the reader curious for the next section) |
| **Future-forward language; contrast through specificity not negation** | NOT "this is not just a temple" → INSTEAD "this is a calendar built in stone" |
| **Confident expert tone; doesn't need to prove credibility** | NOT "research suggests possibly that" → INSTEAD "the alignment is exact to within 0.05°" |
| **Concise without being terse** | A four-word sentence and a forty-word one can both be right. Length follows the idea. |
| **Allow restraint to be the design choice** | Sometimes a one-line caption is more powerful than three paragraphs. Trust the reader. |

## Writing rules (mechanical)

- **No em dashes.** A telltale LLM signal. Use periods, commas, colons, semicolons instead. (`—` is forbidden; `:` and `:` `:` `:` are allowed)
- **No filler words.** Specifically excluded : *genuinely*, *delve*, *straightforward*, *that being said*. Why : these words add no information.
- **No author-self-reference unless necessary.** "We catalog" not "I catalog." "The atlas tracks" not "I track." The voice is institutional.
- **No "obviously" or "clearly."** If it's obvious to you, name the thing rather than telling the reader they should have already known it.
- **No fake urgency.** No "you won't believe what they found" framing. Let the find speak.

## The `:` `:` signature pause (for visual contexts)

A space-colon-space-colon-space construction — `:` ` ` `:` — is the atlas's deliberate stylistic mark for visual contexts only.

Allowed in : slide-style web copy, Library entry pull quotes, hero copy, og-image text.

NOT in : continuous prose paragraphs, video card descriptions, site descriptions, contact emails.

Use sparingly. Two beats of breath. Parallel weight on both sides. Slightly off-rhythm so the eye registers it as intentional.

Example : *"His first profitable runs were indulgences : : get-out-of-purgatory receipts the Vatican mass-printed for cash."*

## Site descriptions

Each site has a 1-4 sentence description in `data/sites.json`. The rules :

| Aspect | Standard |
|---|---|
| Length | 30-80 words typically. Tier 1 sites can be longer; tier 3 sites tend to be shorter. |
| Opening | Lead with the site's distinguishing feature, not a generic introduction. "Largest religious monument ever built (162.6 hectares)" beats "Famous ancient temple located in Cambodia." |
| Specificity | Include numbers : tons, meters, dates, counts. Concrete beats abstract. |
| Editorial restraint | Note what the conventional account says, but flag the contested points without taking sides. "Officially dated to 975 CE" then "the masonry style and weathering suggest a far older substrate" reads as fair witness. |
| UNESCO status | Mention it when the site has UNESCO World Heritage status. Sounds prestigious. |
| Closing | Don't end on a generic flourish. End on the most interesting detail you have. |

**Good example** (Sacsayhuamán) :
> 15th-century fortress on a hilltop above Cusco at 3,701 m elevation. Cyclopean polygonal walls with stones up to 100+ tons fitted without mortar at razor-tight seams. The largest concentration of pre-Columbian megalithic stonework in South America. UNESCO World Heritage.

**Bad example** (would not pass review) :
> An ancient site in Peru that is very famous and important to the Inca civilization. People come from all over the world to see this amazing place which was built thousands of years ago and is truly mysterious.

## Video titles

Most video titles come directly from YouTube. **Don't paraphrase the title** unless it's genuinely misleading or oversized. The CI verifies the title matches YouTube's title.

Exception : if a video's YouTube title is itself a clickbait or harmful framing (rare for our credible creator pool), edit to a neutral description with a `(note: actual YouTube title is "X")` annotation in the PR description.

## Creator entries

Each creator has a `subs` field that doubles as an editorial note. Use it to give a one-sentence frame of what they cover :

| Good `subs` example | Why it works |
|---|---|
| `"Türkiye specialist · cinematic walkthroughs"` | Names their specialty + what makes their work visually distinctive |
| `"Hugh Newman · 47K subs · megalith research · Gobekli & Karahan Tepe"` | Identifies the person, scale, and topical focus |
| `"Boots-on-ground walkthroughs · long-form unedited gimbal tours of Chinese megalithic sites"` | Communicates the editorial value (the unedited, long-form perspective) |

Avoid `subs` that just restate the channel name or count subscribers without context.

## Library entries

Library entries are deep treatments (~3,000-5,000 words). They follow extra discipline :

- **Minto Pyramid Principle** : open with a single governing thought before the supporting structure
- **MECE bullets** : undertone bullets at the top of major sections, each a discrete dimension
- **NLP framing** : presuppositional language (assume the reader has the new capability after reading), outcome framing (this entry will change what you notice)
- **Sourced** : every claim should be traceable. Include a Sources section.

See the existing `library/megaliths.html` and `library/stone-circles.html` for the standard.

## Cultural sensitivity

The atlas catalogs sites built by living and historical peoples. Some standards :

- Never mock or trivialize the cultures depicted
- Don't promote "ancient aliens" hypotheses as established fact — engage with the evidence
- When alt-archaeology positions are noted, present them as positions ("Foerster argues...") not as established truth
- Use respectful place-names. Türkiye, not "Turkey" when discussing the modern state. Indigenous names when contemporary.
- Avoid colonial framings. "Hiram Bingham re-discovered Machu Picchu" should be "Machu Picchu, known to local Quechua-speaking residents continuously, was brought to global academic attention by Hiram Bingham in 1911."

## Things we don't write

- Marketing copy ("ten amazing things you didn't know")
- Affiliate or sponsored content
- AI-generated descriptions (the verification check will likely catch these)
- "We" content that conflates the atlas with the user

## When in doubt

Open a PR with your best attempt and flag the uncertainty in the description. Maintainers prefer "I wasn't sure how to phrase this" over silence.

The atlas isn't perfect. But it tries to be consistent. Consistency is what makes the editorial voice trustworthy.
# Editorial Guidelines · Signal & Criteria addendum

> Append this to the bottom of `docs/EDITORIAL_GUIDELINES.md`.

---

## Signal : marking sites where readings diverge

The atlas catalogs sites with two epistemic stances :

- **Convergent** (default) : mainstream archaeological and independent investigator readings agree on what the site is. No field needed in the data. The vast majority of sites.
- **Open** : readings genuinely diverge. The site's age, builders, or even classification as constructed is an active question. Tagged with `"signal": "open"`.

The badge that appears next to open-question sites is a small triangulation glyph (three dots in a triangle). Tapping it reveals which specific engineering signatures the site exhibits, each one a link into the megalith library reference.

This stance is structural, not editorial decoration. **Convergent Triangulation** treats every reading as a satellite signal. When signals don't converge, the badge reflects that honestly. The atlas doesn't pick a winner.

## When to mark `"signal": "open"`

A site qualifies for the open mark when at least one of these is true :

- Mainstream geological or archaeological reading and independent field investigator reading disagree on classification (natural vs. constructed)
- Carbon dating, GPR scanning, or other quantitative evidence produces results inconsistent with the conventional cultural attribution
- The engineering signature of the work (precision, scale, tools required) does not match the documented capability of the attributed culture
- The site has been the subject of published research from both mainstream and independent archaeology, with substantially different conclusions

A site does NOT qualify just because :

- Alternative-archaeology YouTubers have covered it (popularity is not divergence)
- It's mysterious or visually striking (most ancient sites are)
- A single author has proposed an unconventional theory (one source is not divergence)
- The construction method is unknown but the site itself is uncontested

**Scarcity preserves the signal.** If 60% of sites have the badge, it stops meaning anything. Target : under 5% of the catalog. As of the first rollout, 13 of 296 sites (4.4%).

## The criteria taxonomy (closed set of 6)

Each open-question site carries a `"criteria"` array naming which engineering anomalies it exhibits. The taxonomy is closed — these six and no others :

| Key | Meaning | Library section |
|---|---|---|
| `precision` | Mortarless joinery, sub-millimeter tolerance | `#precision` |
| `hardness` | Stone material harder than tools available to the attributed period | `#hardness` |
| `scale` | Block weights exceed documented lift capability of the attributed period | `#scale` |
| `polygonal` | Polygonal interlock pattern matching the global signature (Cusco / Japan / Mediterranean) | `#polygonal` |
| `stratigraphy` | Stratigraphic layers run backwards : deeper = more advanced technology | `#stratigraphy` |
| `geometry` | Geometric alignment encodes astronomy, terrestrial proportions, or human proportions | `#geometry` |

These map 1:1 to the six properties enumerated in `/library/megaliths.html`. Adding new criteria requires extending the library article first ; the badge taxonomy follows.

**Maximum 4 criteria per site.** If a site exhibits five or six, pick the four that are most diagnostically interesting. The flip-down card stays breathable.

## The engineering voice

This stance is anchored in the framing Jeff articulated during the UnchartedX Egypt tour : *on a tour of one of the most "settled" archaeological sites in the world, one-third of the participants were extremely smart engineers, not archaeologists.* The atlas is for that audience first. Builders looking at physical artifacts and reading the construction as a system.

This shifts the vocabulary of site descriptions :

- Replace *contested, debated, disputed, controversial, pseudoarchaeology, fringe* with **precision, tolerance, joinery, scale, signature, weathering, tool mark, alignment**.
- Name what each reading says (geological, archaeological, independent), don't pick the winner.
- End on the most interesting engineering specific. The reader brings craft knowledge to the description ; the description respects that.

When signals converge, this discipline isn't needed — describe the site normally. The triangulation language is reserved for sites where readings actually diverge, which is where the engineering eye matters most.

## Adding new open-question sites

Maintainer workflow (via `/contribute.html` or direct PR) :

1. Pick `signal: "open"` deliberately. Default convergent.
2. Pick up to 4 criteria from the closed set.
3. Write the description using the engineering voice. Name each reading. Close on the inviting specific.
4. The badge and flip-down appear automatically once the data fields are set.

If the site exhibits an anomaly not covered by the six criteria, that's a signal to expand the library article first. The taxonomy stays tight by design.
