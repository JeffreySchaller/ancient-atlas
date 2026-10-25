# Claude Desktop review

Received 23 October 2026 in the inventory chat, Fable 5.1 High. External review findings, not implementation instructions. Some findings refer to the pre-final draft; resolution notes are in SARDINIA_LOCAL_REVIEW.md.

Review complete. Report for Codex below; no files, branches, store settings or deploys were touched.
Verdict
The batch is sound: all four placements are correct, the uploaders are who the branch says they are, both new pins land on the right ground, and every creator gets a direct watch + follow link. Three things to fix before merge, none of them blockers for long.
What I verified independently
Uploader/title, all six IDs
(four new + Stone Riddles + Megalithomania Sa Testa) via YouTube oEmbed: every author_name, author_url and title matches 
sardinia-local-review-2026-10-23.json
and 
videos.json
exactly.
Nuraghe Losa
pin 40.1169, 8.79007 matches Wikipedia; Abbasanta; central tower 14th c. BC, enclosure 13th c. BC. Your “three-lobed bastion” wording is the trilobate plan; fine.
Nuraghe Arrubiu
pin 39.661944, 9.2975 vs Wikipedia 39.6624, 9.2974 (≈60 m, fine); Orroli; five-tower main bastion, 21 towers total.
sardinia.html
links: 2× watch link per film, 2× channel link per creator, 5 timestamped jumps into the Stone Riddles film, presenters and archaeologists named in copy. Credit structure is as described.
Counts
: 633→635 sites, 99→103 creators, 1,032→1,045 wires; floor (618) safe; batch script is idempotent by inspection.
Three fixes
1. The Stone Riddles chapter jumps are YouTube auto-generated, not the filmmaker’s.
His description lists Part 1 / Part Two / Part Three with no timestamps at all; the 15 chapters in your JSON (generic titles like “Exploring single-tower nuraghi”, “Debating nuragic function”) are YouTube’s machine-inferred markers. The guide currently presents them as the film’s chapters. Options, best first: (a) label the row “Topic jumps (YouTube auto-detected, verified by frame)” and sample one frame at each of the five seconds to confirm the subject before shipping; (b) replace the five jumps with the three creator-authored Parts and drop the seconds; (c) keep as-is but change the caption so the timestamps are clearly the Atlas’s navigation aid, not Mirko Kulig’s structure. The brief said no invented timestamps; auto-chapters sit in a grey zone, so name them.
2. Marco Mura is grouped 
local
; he lives in England.
His own description: Sardinian from Alghero, five years in the UK, video-maker. The guide copy already says “originally from Alghero”, which is accurate, but the 
group: local
tag and the “Sardinian creators filming on location” framing overstate it. Either move him to 
more
with the note “Sardinian-born, UK-based”, or rename the group to “Sardinian voices” so the tag stops implying residence. Bonus: his description explicitly permits sharing and embedding, with no re-upload; worth quoting in the research JSON as the only film in the batch with a stated embed licence.
3. Two of the four “creators” are regional media outlets, and two of the people on camera are state officials.
Sardegna Storica and Sardegna Turistica are channels; the value is Simona Scioni, Alessandro Usai (Soprintendenza, named by cultura.gov.it as responsible for Losa) and Nadia Canu (Soprintendenza Nuoro/Sassari, named in the uploader’s text). Credit wording should stay “appears in / guides the visit”, never “endorses” or “partners with the Atlas”. Same for Ilaria Montis: Sardegna Sacra also sells tours, so keep her out of 
tours.json
unless she asks. The current copy is clean on this; just keep it that way.
Minor: 
search-aliases.json
has no entries for “Losa” or “Arrubiu”; add them so map search finds the new pins. 
creators/sardinia
is a regional guide, not a Study; keep the “Study No. 01” numbering for Ageless Rock only so the hub taxonomy stays clear.
Format labels (for the guide and future intake)
Film
Format
Language
On-site?
Sardegna Sacra · Arrubiu
Guided site visit (archaeologist-guide leads a group)
IT
Yes
Sardegna Storica · Losa
Guided site visit (official guides presenter)
IT
Yes
Sardegna Turistica · Santu Antine
On-site interview (archaeologist, filmed beside the monument; not a continuous walk)
IT
Yes
Marco Mura · Santu Antine
Short walkthrough (3 min, interior + exterior)
IT
Yes
Haswell Travelled · Su Nuraxi
Walkthrough (2015 footage, narrated)
EN
Yes
Megalithomania · Sa Testa, Sant’Andrea Priu
Walkthrough with interpretive commentary
EN
Yes
Stone Riddles II
Feature documentary (multi-site, 2h20)
EN
Yes, plus commentary
Film
Sardegna Sacra · Arrubiu
Sardegna Storica · Losa
Sardegna Turistica · Santu Antine
Marco Mura · Santu Antine
Haswell Travelled · Su Nuraxi
Megalithomania · Sa Testa, Sant’Andrea Priu
Stone Riddles II
Format
Guided site visit (archaeologist-guide leads a group)
Guided site visit (official guides presenter)
On-site interview (archaeologist, filmed beside the monument; not a continuous walk)
Short walkthrough (3 min, interior + exterior)
Walkthrough (2015 footage, narrated)
Walkthrough with interpretive commentary
Feature documentary (multi-site, 2h20)
Language
IT
IT
IT
IT
EN
EN
EN
On-site?
Yes
Yes
Yes
Yes
Yes
Yes
Yes, plus commentary
Film
Format
Language
On-site?
Keep “virtual tour” (3D/reconstruction) and “commentary” (no footage of the site) as separate labels; none of the seven films are either, and the remaining candidates (Dan Davis History, Jacquelyn Atkins) are the ones most likely to be commentary.
Bigger finding: the map is missing Sardinia’s headline sites
None of these exist as pins: 
Santa Cristina sacred well, Mont’e Prama, Monte d’Accoddi, Tharros, Serra Orrios, Tiscali, Palmavera, Anghelu Ruju, Coddu Vecchiu, Li Lolghi, Pranu Mutteddu, Tamuli, Monte Baranta, Santo Stefano rock altar, Su Crucifissu Mannu.
Current coverage is 19 Stone Riddles chapters plus three additions. The next batch should be pins first, then wires.
Recommended next batch (evidence-backed, lowest risk first)
A. Megalithomania Sardinia series (creator already on the map; nine verified IDs, all MegalithomaniaUK by oEmbed):
FQpeO1l7mXk
Santa Cristina holy well & nuragic village → new pin
cbhv2_53Fvc
Mont’e Prama giants → new pin
WA5RB_et8_g
Monte d’Accoddi → new pin
9ypi4_7bpy0
Giants’ tomb Sa Domu ‘e s’Orku (Siddi) → new pin
IlQIb8EiWK0
Coddu Vecchiu & Li Lolghi → two new pins (multi-site film, record both)
JaIZ-WUxbmE
Tamuli → new pin
RXWKW9eexXc
Monte Baranta → new pin
XQFvrH_OwTU
Santo Stefano rock altar → new pin
EUFkkp11DSY
Sardinian cart ruts & Su Crucifissu Mannu hypogea → new pin
Caveat: Megalithomania’s titles carry “high technology / lost technology” framing. Placement is safe; keep Atlas copy to what the footage shows.
B. Nuragando (@nuragando, “Nuraghi di Sardegna”)
— the best local on-location find. Site-per-video, Italian titles that are just the site name, recent uploads (2024–Sept 2026), drone and ground footage, tiny view counts, no interpretive agenda. Verified by oEmbed:
n3soSXoFh50
Domus de janas Corongiu, Pimentel → existing pin, adds a second creator
ytkWK4dWTwU
Monte Baranta → pairs with Megalithomania above
GWCNzrTIXvk
Serra Orrios, Dorgali → new pin
zjACAStJenM
Tomba dei giganti Is Concias, Quartucciu → new pin
zQhI6OurlNE
Necropoli Ispiluncas, Sedilo → new pin (Iloi/Sedilo already on map; check it is a distinct site)
mW7eLPNe8lk
Biru ‘e Concas menhirs, Sorgono → new pin
xmZQyJkCsj4
/ 
rhaufI4ZARg
Or Murales village, Urzulei → new pin
Sept 2026 trio on Li Curuneddi necropolis, Sassari → new pin
Needs your frame-sampling pass (I could not view footage), and one note: the channel About is a single line with no person named, so credit as “Nuragando” with the channel link.
C. Already in your queue, worth promoting:
dwpSZQN874Y
Amici di Sardegna, Nuraghe Seruci (Gonnesa) on-site interview; 
kn00MXE1RWc
ignazio serra, Losa guide clip (3 min, pastoral-tourism office).
D. Lower priority / different formats:
Pierluigi Montalbano 
ZljnKh8k8dg
(lecture; “commentary” label); La Sardegna verso l’Unesco (conference recordings; commentary); Sardegna Sacra’s own recent uploads are Shorts and tour promos, so Arrubiu is likely their one usable film.
Sources I used beyond the repo: 
Nuragando channel
, 
La Sardegna verso l’Unesco
, 
Nuraghe Losa
, 
Nuraghe Arrubiu
, 
Stone Riddles II
, 
Pierluigi Montalbano lecture
.
