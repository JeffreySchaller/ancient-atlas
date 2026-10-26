#!/usr/bin/env python3
"""Idempotent, source-reviewed October Ageless Rock catch-up.
See docs/research/ageless-rock-placement-2026-10-26.json.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'
def load(n): return json.loads((D/n).read_text())
def save(n,x): (D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    ledger=json.loads((ROOT/'docs/research/ageless-rock-placement-2026-10-26.json').read_text())
    audit=json.loads((ROOT/'docs/research/ageless-rock-channel-audit-2026-10-26.json').read_text())
    uploads={v['id']:v for v in audit['uploads']}
    sites=load('sites.json'); videos=load('videos.json')
    assert 'agelessrock' in load('creators.json')
    names={s['n'] for s in sites}
    for row in ledger['new_sites']:
        s=row['site']
        if s['n'] not in names:
            assert not any(abs(t['lat']-s['lat'])<.001 and abs(t['lng']-s['lng'])<.001 for t in sites), s['n']
            sites.append(s); names.add(s['n'])
        for filename,value in [('countries.json','Spain'),('civilizations.json',row['civilization']),('eras.json',row['era']),('tags.json',row['tags'])]:
            m=load(filename); m[s['n']]=value; save(filename,m)
    for row in ledger['links']:
        name,vid=row['site'],row['id']; assert name in names
        src=uploads[vid]; assert src['uploader']=='Ageless Rock'
        date=src['upload_date']; published=f'{date[:4]}-{date[4:6]}-{date[6:]}'
        rows=videos.setdefault(name,[])
        if not any(v['id']==vid for v in rows):
            rows.append({'id':vid,'title':src['title'],'cr':'agelessrock','added':'2026-10-26','published':published})
    save('sites.json',sites); save('videos.json',videos)
    print(f'{len(sites)} sites; {sum(len(v) for v in videos.values())} film links')
if __name__=='__main__': main()
