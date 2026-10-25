# Site-bound photographs

Published collection reviewed 24 October 2026: 70 photographs at 35 canonical map sites, comprising 26 Sardinian sites and all nine currently mapped Corsican sites. Ceccia, Renaghju and Palaggiu have photographs despite having no linked film. No site coordinates were inferred from a photo or changed for this collection.

## Data and surfaces

`data/site-photos.json` keys must exactly match `data/sites.json`. Each image includes local path, dimensions, caption, photographer, stated licence and licence URL, Commons source page, changes and review date. New selections also retain the Commons file title and description as identity evidence. Existing curated island-guide images retain their original source/credit records. The public data mirror provides full credits.

Map detail panels, phone site sheets and the phone feed render credited horizontal galleries. The feed's Photographs filter includes photo-only sites. Hover previews and grid cards can show photographs when no film exists. Static site pages provide full-composition image galleries. `/photos/` is an image-first directory with island and photo-only filters. Original source links open the attributed Commons pages. The island guides and desktop sidebar link to the directory.

## Selection and rights

Commons API title, category, image description, named monument and visually reviewed photographs were used together. Every selected image has a named author and a reusable stated licence (CC BY, CC BY-SA or public domain). One Arrubiu photograph was rejected because its Commons category identified Sardara, not the mapped Orroli complex. Missing-author files were excluded. Approach-path and information-board photographs were excluded from the final selection. Same-named or nearby subjects are not acceptable substitutes.

Full originals remain in local research under `Corsica/research/site-photos/` and the earlier Corsica image-comparison collection. Public files are resized WebP derivatives, preserving the full composition without colour changes; some reuse existing island-guide assets. Original licence conditions remain attached to each image. A derivative's conversion note is displayed on static site pages. Assets are lazy-loaded. Keep the current image IDs stable when expanding this collection.

No verified photo was selected in this pass for Sas Puntas, Santa Barbara at Bauladu, Piricu, Mura Cuada, Corongiu at Pimentel, or Su Mont'e s'Abe. Their existing film coverage remains available. This is a substantial first collection, not a claim that Commons has no images of those places.

## Validation

Run `python3 scripts/verify-site-photos.py`, `python3 scripts/build.py`, the video audit and conversation fixtures. Browser review covered 1440px desktop and 390px phone, directory filters, photo-only site navigation, credited galleries, decoded image loading and horizontal overflow. Portrait map deep-links skip Leaflet animation while the map has zero dimensions; the feed remains the active surface. Existing sites, creators, film associations and documentary start times are retained.
