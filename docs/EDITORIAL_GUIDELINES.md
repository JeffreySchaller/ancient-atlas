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
