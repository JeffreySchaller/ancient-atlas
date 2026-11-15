#!/usr/bin/env python3
"""Add verified Megalithic Mystery sites and credited walkthroughs, idempotently.

Location sources and held candidates: docs/research/megalithic-mystery-2026-11-15.md.
Run this script, then scripts/build.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
CREATOR = 'megalithicmystery'
ADDED = '2026-11-15'

NEW_SITES = [
    ('Choquechurco', -13.4732, -72.5396, 'rock-cut', 'Peru', 'Inca', 1450,
     'Hilltop Inca complex above Mollepata in the Cusco region, with terraces, stone enclosures and worked rock outcrops along an old Inca route. Carved steps and the relationship between masonry and exposed bedrock make it worth exploring closely. Aaron Hynes visits the ceremonial sector and a wall below the summit in his Megalithic Mystery walkthrough.'),
    ('Muyuqhawa', -14.78688, -71.29594, 'settlement', 'Peru', 'K’ana / Inca', 1400,
     'Fortified hilltop settlement near Espinar, also written Muyoqhawa or Molloqhawa. Successive defensive walls and trapezoidal entrances enclose circular and rectangular structures and funerary towers. Its mountain setting makes the relationship between fortification and terrain especially legible. Megalithic Mystery explores the gateways and interior, then shows the complex from the air.'),
    ('Yaxunah', 20.5416, -88.66254, 'city', 'Mexico', 'Maya', 800,
     'Maya city east of the present-day village of Yaxunah in Yucatán. Monumental platforms, an acropolis and a ball court sit among woodland and cultivated land. Its long raised causeway to Cobá connects the site to a much wider political landscape. Megalithic Mystery walks the ruins in the first chapter of a four-site Yucatán film.'),
    ('Kabah', 20.247976, -89.647521, 'city', 'Mexico', 'Maya (Puuc)', 800,
     'Puuc Maya city southeast of Uxmal, distinguished by the Codz Pop façade and its dense mosaic of carved stone masks. Multiroom palaces, vaulted interiors and carefully arranged plazas show the architectural ambition of the city during its Late Classic flourishing. The walkthrough follows the buildings and their sculptural details at ground level.'),
    ('Sayil', 20.178093, -89.651912, 'city', 'Mexico', 'Maya (Puuc)', 850,
     'Puuc Maya city whose three-level Great Palace combines long colonnaded façades with finely cut stone decoration. Paths connect the palace with other architectural groups spread through the surrounding woodland. Megalithic Mystery’s visit places the monumental façade within that wider settlement.'),
    ('Xlapak', 20.174077, -89.606149, 'settlement', 'Mexico', 'Maya (Puuc)', 850,
     'Small Puuc Maya settlement between Sayil and Labná, also spelled Xlapac. Its palace preserves elaborate stone mosaic decoration and masks associated with the rain deity Chaac. The community flourished around 750–950 CE, supported by the agricultural land in its small valley. The final chapter of Megalithic Mystery’s four-site film visits these surviving buildings.'),
    ('Dzibilchaltún', 21.090934, -89.597261, 'city', 'Mexico', 'Maya', 700,
     'Long-lived Maya city north of Mérida, with plazas, raised causeways and the Temple of the Seven Dolls. The cenote Xlacah lies beside the monumental core, while a later open chapel records the site’s colonial history. Megalithic Mystery walks the central buildings and finishes at the temple, allowing the scale and layout to unfold on foot.'),
]

WIRES = [
    ('Choquechurco', 'VwSpNmjL0qU', 0),
    ('Muyuqhawa', 'j-scw8Wg9YI', 0),
    ('Yaxunah', '2ukrxJGLVPE', 100),
    ('Kabah', '2ukrxJGLVPE', 1183),
    ('Sayil', '2ukrxJGLVPE', 2163),
    ('Xlapak', '2ukrxJGLVPE', 2945),
    ('Dzibilchaltún', '0fTp1N8sm5M', 0),
    ('Inkilltambo', 'nsyE9P-DAAE', 0),
    ('Tipón', 'l5Ym2Xhl85Q', 0),
    ('Tambomachay', 'pZnXuaDlgeg', 0),
    ('Pikillaqta', 'j79nH5joF_4', 641),
    ('Uxmal', 'sQCQqby8wIk', 0),
    ('Zone X (Cheqtaqaqa)', 'bIH8zZXlSCc', 0),
    ('Amaru Markawasi', 'B1HOnxqImN4', 0),
]

def main():
    files = ['sites', 'creators', 'videos', 'countries', 'civilizations', 'eras', 'tags', 'search-aliases']
    data = {f: json.loads((DATA / (f + '.json')).read_text()) for f in files}
    metadata = {v['id']: v for v in json.loads((ROOT / 'docs/research/megalithic-mystery-video-metadata-2026-11-15.json').read_text())}
    data['creators'][CREATOR] = {
        'name': 'Megalithic Mystery', 'handle': '@megalithicmystery',
        'subs': 'Aaron Hynes · Peru and Mexico field walkthroughs',
        'color': '#80B6A0', 'tier': 3,
    }
    names = {s['n'] for s in data['sites']}
    for name, lat, lng, category, country, culture, year, desc in NEW_SITES:
        if name not in names:
            data['sites'].append(dict(n=name, lat=lat, lng=lng, cat=category,
                region='South America' if country == 'Peru' else 'Central America', tier=3, desc=desc))
            names.add(name)
        for file, value in [('countries', country), ('civilizations', culture), ('eras', year),
                            ('tags', f'{name} {country} {culture} archaeology Megalithic Mystery Aaron Hynes')]:
            data[file][name] = value
    data['search-aliases'].update({'muyoqhawa': 'Muyuqhawa', 'mullu qawa': 'Muyuqhawa',
        'molloqhawa': 'Muyuqhawa', 'xlapac': 'Xlapak', 'yaxuna': 'Yaxunah'})
    for site, video_id, start in WIRES:
        assert site in names, site
        video = metadata[video_id]
        assert video['channelId'] == 'UCqNQ3r7zHzTStU-vbPCeuVw'
        entries = data['videos'].setdefault(site, [])
        if any(v['id'] == video_id for v in entries):
            continue
        entry = dict(id=video_id, title=video['title'], cr=CREATOR,
                     added=ADDED, published=video['publishedAt'][:10])
        if start:
            entry['t'] = start
        entries.append(entry)
    for file, value in data.items():
        (DATA / (file + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(f"Sites: {len(data['sites'])}; Megalithic Mystery placements: {sum(v['cr'] == CREATOR for vs in data['videos'].values() for v in vs)}")

if __name__ == '__main__':
    main()
