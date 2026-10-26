#!/usr/bin/env python3
"""Idempotent monument-level placement of three Ageless Rock films."""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
def load(f):return json.loads((D/f).read_text())
def save(f,x):(D/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 ledger=json.loads((ROOT/'docs/research/ageless-portugal-placement-2026-10-26.json').read_text())
 audit=json.loads((ROOT/'docs/research/ageless-rock-channel-audit-2026-10-26.json').read_text())
 uploads={v['id']:v for v in audit['uploads']}
 sites=load('sites.json');videos=load('videos.json');assert 'agelessrock' in load('creators.json')
 before=len(sites)
 for r in ledger['new_sites']:
  s=r['site'];n=s['n']
  if not any(x['n']==n for x in sites):
   for x in sites:
    km=111*math.hypot(s['lat']-x['lat'],(s['lng']-x['lng'])*math.cos(math.radians(s['lat'])))
    assert km>.1,f'Nearby existing record: {x["n"]}, {n}'
   sites.append(s)
  for f,val in [('countries.json','Portugal'),('civilizations.json',r['civilization']),('eras.json',r['era']),('tags.json','Portugal '+n+' Ageless Rock Bernie Ong')]:
   m=load(f);m[n]=val;save(f,m)
  vid=r['video_id'];src=uploads[vid];assert src['uploader']=='Ageless Rock'
  date=src['upload_date'];rows=videos.setdefault(n,[])
  if not any(v['id']==vid for v in rows):rows.append({'id':vid,'title':src['title'],'cr':'agelessrock','t':r['start_seconds'],'added':'2026-10-26','published':f'{date[:4]}-{date[4:6]}-{date[6:]}'})
 save('sites.json',sites);save('videos.json',videos)
 print(f'Sites {before} -> {len(sites)}; total film associations {sum(map(len,videos.values()))}')
if __name__=='__main__':main()
