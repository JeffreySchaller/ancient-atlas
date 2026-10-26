#!/usr/bin/env python3
"""User-requested film; title and channel verified via YouTube oEmbed, 2026-10-26."""
import json
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'data/videos.json'
data = json.loads(p.read_text())
if not any(v['id'] == 'N0IvaD4xnMk' for v in data['Tipón']):
    data['Tipón'].append({'id':'N0IvaD4xnMk','title':"The Megalithic Evidence They Don't Want You to See at Tipon",'cr':'earthexplorer','added':'2026-10-26'})
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
