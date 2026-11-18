# Obelisks map layer

Open `/?obelisks=1` or a monument link such as `/?obelisks=1&obelisk=new-york`.
Desktop and mobile Explore sections and the Overlays controls expose the same collection.

The 29 initial entries are an explicitly categorized research collection. They include pharaonic and Ptolemaic examples, Roman commissions, uncertain objects, Egyptian benchmarks, and the San Jose concrete replica. They do not increase the main ancient-site or walkthrough counts.

## Editorial source

Edit `data/obelisks.json`. The build mirrors it to `public/data/obelisks.json` for the layer's lazy load. Each record retains its stable ID, present coordinates, material, classification, original or earliest known setting, dated journey milestones, qualified dimensions, historical sources, and photograph credits.

Historical coordinates are approximate site or city positions. A milestone can retain a historical place and date with null coordinates where it cannot be mapped responsibly. The drawn links connect known places; they are not reconstructed shipping tracks. Unknown intervening history is not filled with guesses.

San Jose's Egyptian model is separate from the replica's local creation. It has no Egypt-to-California relocation line. Aswan's unfinished quarry object has a planned length, with no standing shaft height. Vatican origins and several Roman initial settings remain qualified.

## Photographs

Serve images locally from `public/assets/obelisks/`. Every photograph must retain creator, title, source page, license, license URL, dimensions, alt text, and any changes. `PHOTO-CREDITS.md` records the initial image sources. The dossier displays creator, license, and source links beside the image. The initial files are unedited Wikimedia-supplied scaled images.

## Checks

Run `python3 scripts/verify-obelisks.py` and `node --check public/assets/js/atlas-obelisks.js`. The dedicated workflow repeats these checks on relevant pull requests. The data check covers source/mirror equality, unique identities, paired coordinates, current endpoints, image files and attribution, and replica/unfinished semantics.

Browser checks should cover direct links, unknown-ID fallback, toggle persistence after filters redraw, keyboard selection focus, stage selection/reset, Rome groups, desktop and portrait/landscape phone layout, and coexistence with ordinary site details and LiDAR.

The layer groups its small collection in screen space. This keeps isolated monuments visible when the host map's minimum zoom changes fractionally. At close zooms, an overlapping group offers a list of its monuments. Existing site layers and their filters remain independently managed.
