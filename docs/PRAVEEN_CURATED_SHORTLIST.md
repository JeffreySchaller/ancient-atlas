# Praveen Mohan — Curated Shortlist for Atlas Wiring

**Filter applied:** Strict — title must name a specific site, content must be documented archaeology, not theory ramble. Provocative framing tolerated only when the site is unambiguously identified.

**Current state:** 11 Praveen wires across 8 sites (Ajanta, Angkor Wat, Hampi, Prambanan, Rani ki Vav, Si Thep, plus Asuka sites).

**Channel review:** ~250 videos + ~200 shorts catalog. After filter: ~22 walkthroughs pass.

---

## Net-new sites to add (5)

| Site | Country | Why it qualifies |
|------|---------|------------------|
| Phimai (Prasat Hin Phimai) | Thailand | 11-12th c. Khmer sandstone temple, Nakhon Ratchasima. Three Praveen videos. Architecturally significant — northern terminus of the Khmer road network and the prototype for Angkor Wat's tower. |
| Phanom Rung | Thailand | Khmer hilltop sanctuary in Buri Ram, 10-12th c. Volcanic outcrop site with sandstone construction. Two Praveen videos. |
| Banteay Samré | Cambodia | Angkor outlier, 12th c. Khmer. Walled enclosure with precision sandstone fitment. |
| Ta Nei | Cambodia | Small Jayavarman VII-era Angkor temple, less restored than Ta Prohm but stylistically similar. |
| Ta Keo | Cambodia | Khmer "lightning pyramid" — unfinished sandstone temple-mountain c. 1000 CE, struck by lightning during construction per inscription. Distinct architectural anomaly. |

Optionally add: **Yangshan Quarry (China)** if not already wired — the abandoned Ming-era megalithic block extraction site, contextual companion to Aswan and Baalbek monoliths.

---

## Approved walkthroughs (full-length) — 22

### Existing sites — wire additional Praveen coverage

1. **Angkor Wat** — `This is inside the MAIN CHAMBER of Angkor Wat? Evidence of Ancient Technology`
2. **Phnom Bok** — `10 Ton 'Cosmic Antenna' Found in Cambodia? World's Largest Lingam at Phnom Bok Mountain` *(site-clear, framing spicy)*
3. **Spean Praptos (Kampong Kdei Bridge)** — `They Destroyed Every Face On This Ancient Bridge. What Were They Hiding?` *(verify against existing wire — may already be in)*
4. **Osaka Castle** — `The Enormous Megaliths of Osaka Castle in Japan`
5. **Osaka Castle** — `How Japanese Polygonal Megalithic Walls Differ from those in Peru?` *(comparative, anchors at Osaka)*
6. **Ishibutai Kofun** — `Mysterious Ancient Japanese Megalithic Tomb – Ishibutai Kofun 石舞台古墳`
7. **Asuka monoliths** — `The Mysterious Monoliths of Asuka Nara, Japan`
8. **Masuda no Iwafune** — `Japan's Mysterious "Rock Ship" of Masuda`
9. **Ishi-no-Hoden** — `MYSTERIOUS "FLOATING STONE", MY THEORY | Ishi-no-Hoden`
10. **Sannai-Maruyama** — `Sannai-Maruyama - Aomori - 国指定特別史跡 三内丸山遺跡`
11. **Longyou Caves** — `The Longyou Caves Mystery: Ancient Engineering & Hidden Grottoes of China` *(verify dedup against existing Gimbal walkthrough — both can coexist)*
12. **Yonaguni** — `Freediving Yonaguni Pyramid | Yonaguni Monument` *(strip the 'Aliens or Lost Civilization' subtitle in our metadata)*
13. **Daisen / multi-kofun** — `Kofun: Japan's Megalithic Tombs` *(wire to Daisen, with also-covers tags)*

### New sites — wire from this batch

14. **Phimai** — `Phimai Temple – The Greatest Mystery of Thailand | Part 1`
15. **Phimai** — `Evidence of Ancient Technology – Phimai Temple Part II`
16. **Phimai** — `Impossible Ancient Technology – Phimai Temple, Thailand | Part 3`
17. **Phimai** — `The Naga Connection to the Phimai Temple` *(borderline — iconography focus)*
18. **Phanom Rung** — `Phanom Rung Temple - Ancient Underground Technology Uncovered?`
19. **Phanom Rung** — `Impossible Stone Objects Excavated From Phanom Rung Temple`
20. **Banteay Samré** — `Ancient Secrets Hidden in Main Chamber? Banteay Samré Temple`
21. **Ta Nei** — `Strange Stone at Main Chamber of Ta Nei Temple, Cambodia`
22. **Ta Keo** — `Cambodia's Lightning Pyramid of Ta Keo: Ancient Machine or Simple Temple?`

### Cross-channel collaboration (verify host channel before wiring)

- **Hugh Newman vs Praveen — England's Most Impossible Ancient Site** (1:05:51) *(channel: Megalithomania OR Praveen — verify; likely Stonehenge/Avebury)*

---

## REJECTED — 220+ uploads

**Rejection categories:**
- **UFO / Aliens / Anunnaki / Vimana / Disclosure framing** (~40 uploads): Ravana's Lingam UFO Reactor, Aliens.gov, Trump 8-Pointed Star UFO, Anunnaki Temple in India, 108 Underwater Machines Lidar, Cambodian Vimana, etc.
- **Brahmastra / Nephilim / Giants / Sleeping Giant** (~15 uploads): Stonehenge Built By Giants, Jungle Hiding Evidence of Ancient War, HE IS AWAKENING etc.
- **Anachronism bait** (~30 uploads): Cellphone Carved in Hindu Temple, Steam Engine Ship, Bicycle, Headphones, Tesla Coil, Sankara Stones, Dendera Light, Anti-Gravity Lingam, etc.
- **Theory podcasts / debate episodes** (~10): Rupert Sheldrake Vs Praveen, Matt Beall Vs Praveen, Hugh Newman Gobekli Hindu Temple discussion. Atlas wants site walkthroughs, not theory debate.
- **Religious doctrine pieces** (~50): Multiple Shiva/Vishnu/Murugan/Nagas iconography explainers — interesting content but not site-archaeology.
- **Multi-site theory roll-ups** (~15): "ancient builders left the same signature on every continent", "Pre-Historic Mega Structures of Japan & Unexcavated Giant Tombs", "Gigantic Ancient Megastructures in China" — too diffuse to wire cleanly. Could rescue if we extract specific site segments with timestamps.
- **Shorts (~200)** — almost all rejected. The shorts catalog leans heavily on iconography close-ups (Lingam this, Shiva that, "Did Ancient People Use Cellphones") and is the loudest part of his catalog. A handful might wire to specific sites with care, but the ROI is low.

---

## Implementation plan

1. **Approve this shortlist** (Jeff edits if needed).
2. **Fetch IDs via Chrome MCP** — open `youtube.com/@RealPraveenMohan/videos`, find each shortlisted title, capture the 11-char ID. Estimated 20-25 lookups.
3. **Run `add-praveen-curated-batch.py`** (scaffold below).
4. **Build + commit + push.**

---

*Generated 2026-06-08. Filter: Strict. Editorial principle: atlas wires represent site documentation, not interpretive theory.*
