#!/usr/bin/env python3
"""Validate exact site bindings, reusable licences and locally hosted photo assets."""
import json
from pathlib import Path
from urllib.parse import urlparse
R=Path(__file__).resolve().parent.parent
sites={x['n'] for x in json.loads((R/'data/sites.json').read_text())}
photos=json.loads((R/'data/site-photos.json').read_text());total=0
for site,rows in photos.items():
 assert site in sites,site
 sources=set()
 for p in rows:
  for k in ['image','width','height','caption','author','license','license_url','source','changes','reviewed']:assert p.get(k),(site,k)
  assert p['source'] not in sources,(site,'duplicate original');sources.add(p['source'])
  assert urlparse(p['source']).hostname=='commons.wikimedia.org',(site,'source')
  assert urlparse(p['license_url']).hostname=='creativecommons.org',(site,'licence URL')
  assert p['license'].startswith(('CC BY ','CC BY-SA ','CC0','Public domain')),(site,p['license'])
  assert p['image'].startswith('/img/') and '..' not in p['image']
  assert (R/'public'/p['image'].lstrip('/')).is_file(),p['image']
  assert isinstance(p['width'],int) and isinstance(p['height'],int) and min(p['width'],p['height'])>100
  total+=1
print(f'PASS: {total} credited photo records bound to {len(photos)} known sites; assets and licence URLs present')
