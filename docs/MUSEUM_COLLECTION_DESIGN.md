# Museum collection : design proposal

A way to surface the institutions that hold the artifacts from atlas
sites, without breaking the current site-centric UX.

## The use case

Researchers and creators (Brien Foerster, UnchartedX, Praveen Mohan,
Proto Civilization) regularly film inside museums where artifacts from
atlas sites are displayed. Cairo Museum, the Grand Egyptian Museum,
Petrie Museum (London), MNAAHP Lima, the Hermitage, British Museum,
Studio Seminario (Cusco), and dozens of others. Currently the atlas
has no clean way to represent these institutions, which means :

1. Walkthroughs filmed *at* the museum (e.g. UnchartedX scanning a
   precision granite vase at the Petrie) have no canonical home.
2. Atlas users browsing a source site (Saqqara) cannot easily discover
   where the most important finds from that site are now displayed.
3. Atlas users at a museum (visiting Cairo or London) cannot easily
   work backward from the artifact to the source site on the map.

## Design principle

**Museums are a parallel kind of site, not a separate system.** They
get the same map markers, the same cards, the same walkthrough feed,
the same Library article eligibility — but with a distinct visual
treatment, a separate filter, and bidirectional cross-references to
the source sites whose artifacts they hold.

This keeps the UX vocabulary unchanged for users who don't care about
the museum dimension, while adding a high-value layer for those who do.

## Data model changes

**New category in CATS taxonomy** :

```json
"museum": {
  "label": "Museum / Collection",
  "color": "#A586D1",
  "icon": "column"
}
```

A muted lavender accent distinct from the existing sand-and-champagne
palette, with a small column/pediment glyph for the marker.

**New fields on site entries** :

For source sites (existing entries), add an optional list :

```json
"artifacts_at": ["Egyptian Museum (Cairo)", "Petrie Museum (London)"]
```

For museum entries, the inverse :

```json
"artifacts_from": ["Saqqara Necropolis", "Step Pyramid of Djoser",
                   "Memphis (Mit Rahina)", "Abusir"]
```

Both fields reference site names exactly. The build script can validate
the bidirectional integrity at compile time.

## Map and filter changes

1. **Marker icon** : museums get a column glyph instead of the existing
   site dot. Cluster aggregation still works the same way — a marker
   that contains both sites and museums shows a small split count.
2. **Type filter row** : add "Museum" as a chip alongside "Megalithic /
   Pyramid / Temple / Underground / Rock-Cut / City / Tomb / Settlement /
   Geoglyph." Selecting it shows only museums; unselecting hides them.
3. **Default behavior** : museums are visible by default (no hiding by
   default) but the marker style makes them visually quiet.
4. **Map clustering** : continue to cluster site + museum together,
   since proximity is the dominant grouping (e.g. Cairo Museum and the
   Giza sites cluster together at low zoom).

## Site card cross-references

On a **source site card** (e.g. Saqqara Necropolis), add a new section
below the walkthroughs :

```
ARTIFACTS NOW DISPLAYED AT
  → Egyptian Museum (Cairo)
  → Grand Egyptian Museum (Giza)
  → Petrie Museum (London, UK)
```

Each is a deep-link to the museum's atlas entry.

On a **museum card** (e.g. Egyptian Museum Cairo), invert :

```
HOLDS ARTIFACTS FROM
  → Saqqara Necropolis
  → Step Pyramid of Djoser
  → Memphis (Mit Rahina)
  → Tanis (San el-Hagar)
  → Amarna (Akhetaten)
  → Valley of the Kings
```

Each is a deep-link back to the source site.

## Walkthrough cross-listing

A video filmed at a museum showing an artifact from a specific source
site should appear in both feeds. Schema :

```json
{
  "id": "abc123",
  "title": "Scanning a Precision Granite Vase | Petrie Museum",
  "cr": "unchartedx",
  "added": "2026-06-09",
  "published": "2024-04-15",
  "cross_ref_sites": ["Saqqara Necropolis", "Abu Sir (Pyramid Complex)"]
}
```

The primary wire goes on the museum entry. The `cross_ref_sites` field
tells the build script to also surface this video on those sites'
walkthrough feeds, with a small badge indicating "Filmed at [Museum]."

## Initial museum roster (Phase 1)

Six high-value institutions to seed the category :

1. **Egyptian Museum (Cairo)** — Tahrir Square; the classical Egyptian
   collection. Many UnchartedX walkthroughs here.
2. **Grand Egyptian Museum (Giza)** — opened 2024; the new principal
   Egyptian collection alongside the Giza Plateau.
3. **Petrie Museum of Egyptian Archaeology (London)** — UCL; the small
   finds and the precision-vase corpus UnchartedX has documented.
4. **MNAAHP Lima** — Museo Nacional de Arqueología, Antropología e
   Historia del Perú; Paracas mummies, Chavín, Wari, Nazca textiles.
5. **British Museum (London)** — the Egyptian, Mesopotamian, Greek
   collections including the Rosetta Stone and Parthenon Marbles.
6. **Studio Seminario (Cusco)** — Raul Carreño's private collection;
   precision pre-Inca artifacts referenced by Brien Foerster.

## Library entry tie-in

A future Library Entry — "**Where the Artifacts Went**" — could be the
natural critical-history piece around this. The colonial-era and 19th-c.
dispersal patterns, the repatriation debate, the difference between
in-situ context and museum case context, and what an atlas user gains
by knowing both halves of the story.

## Phased rollout

| Phase | Scope | Effort |
|---|---|---|
| **1. Schema + 6 anchor museums** | Add the `museum` category, seed the six institutions above, ship distinct marker treatment | 1 batch script |
| **2. Cross-reference data** | Add `artifacts_at` to ~50 high-value sites, populate `artifacts_from` on each museum | Curation pass |
| **3. Site card cross-link sections** | Update the site detail template to render the "Artifacts now displayed at" and "Holds artifacts from" panels | Template edit |
| **4. Walkthrough cross-listing** | Implement the `cross_ref_sites` field in build.py + show the "Filmed at [Museum]" badge in the walkthrough cards | Build script + CSS |
| **5. Library entry** | Author "Where the Artifacts Went" | Editorial work |

## What this lets us do that we cannot today

- Wire Brien's Cairo Museum walkthroughs (the Shorts mentioned), Studio
  Seminario coverage, and UnchartedX's Petrie / Cairo content as
  walkthroughs of real entries on the map.
- Surface Paracas Necropolis (the field site) alongside MNAAHP Lima
  (where the mummies actually are) without forcing users to choose
  between "site coverage" and "artifact coverage."
- Give the Library a new dimension : the institutional history of
  archaeology, not just the field sites.
- Open a clean lane for repatriation/provenance content as the field
  evolves.

## What we deliberately don't do

- We don't create a separate page or mode. Museums live in the same map
  + same feed + same Library.
- We don't change the default user experience. A new visitor sees the
  same atlas they see today, with quiet museum markers added.
- We don't replace site coverage with museum coverage. Both sides are
  first-class, with bidirectional links between them.
