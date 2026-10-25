#!/usr/bin/env python3
"""Apply reviewed island sites, site-specific documentary timestamps and field films."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent.parent;D=R/'data'
def load(n):return json.loads((D/n).read_text())
def save(n,x):(D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 spec=load('island-map-review.json');sites=load('sites.json');countries=load('countries.json');eras=load('eras.json');civs=load('civilizations.json');videos=load('videos.json');creators=load('creators.json');aliases=load('search-aliases.json')
 names={s['n'] for s in sites}
 for row in spec['new_sites']:
  s=row['site'];n=s['n']
  if n not in names:sites.append(s);names.add(n)
  countries[n]=row['country'];eras[n]=row['era'];civs[n]=row['civilization']
 new_creators={'marcvillinger':dict(name='Dr. Marc Villinger',handle='@marcvillinger',subs='On-location travel films · Cucuruzzu archaeological site visit',color='#83A498',tier=3),'videotourist':dict(name='Video Tourist Adventures',handle='@video-tourist',subs='Travel and archaeological site visits · videoturysta.eu',color='#9EAE7A',tier=3),'horsfrontieres':dict(name='Hors Frontières',handle='@HorsFrontieres',subs='French-language travel films · on-location archaeological visits',color='#C1A87B',tier=3),'valincotv':dict(name='valinco tv',handle='@valincotv',subs='Corsican landscape and heritage · filmed site visits and time-lapses',color='#7DA7B5',tier=3)}
 meta={m['id']:m for m in json.loads((R/'docs/research/islands-video-review-2026-10-24.json').read_text())}
 # Use verified channel handles rather than assumptions about capitalisation.
 for key,id in [('marcvillinger','LM5C_Zr9nGE'),('videotourist','N6TpJFxjHfc'),('horsfrontieres','eXeX73aspL4'),('valincotv','BO2Hv4XvfFQ')]:
  new_creators[key]['handle']=meta[id]['uploader_id'];creators.setdefault(key,new_creators[key])
 doc=spec['documentary'];published=meta[doc['id']]['upload_date'];published=f'{published[:4]}-{published[4:6]}-{published[6:]}'
 for p in doc['placements']:
  assert p['site'] in names
  vs=videos.setdefault(p['site'],[]);v=next((v for v in vs if v['id']==doc['id']),None)
  if v is None:v=dict(id=doc['id'],cr='stoneriddles',added='2026-10-24');vs.append(v)
  v.update(title=doc['title'],t=p['seconds'],published=published)
 for p in spec['additional_videos']:
  assert p['creator'] in creators,(p['creator'],p['site'])
  m=meta[p['id']];dt=m['upload_date'];vs=videos.setdefault(p['site'],[])
  if not any(x['id']==p['id'] for x in vs):
   v=dict(id=p['id'],title=m['title'],cr=p['creator'],added='2026-10-24',published=f'{dt[:4]}-{dt[4:6]}-{dt[6:]}')
   if p['seconds']:v['t']=p['seconds']
   vs.append(v)
 # Match established alias schema: alias string -> canonical site name.
 for alias,name in {'Santa Cristina':'Sacred Well of Santa Cristina','Saint Christina':'Sacred Well of Santa Cristina','St Christina':'Sacred Well of Santa Cristina','Cucuruzzu':'Cucuruzzu (Corsica)','Araghju':'Araghju (Corsica)','Funtanaccia':'Funtanaccia Dolmen (Corsica)'}.items():
  if isinstance(aliases,dict):aliases.setdefault(alias.lower(),name)
 for n,x in [('sites.json',sites),('countries.json',countries),('eras.json',eras),('civilizations.json',civs),('videos.json',videos),('creators.json',creators),('search-aliases.json',aliases)]:save(n,x)
 print('Reviewed additions applied:',len(spec['new_sites']),'sites;',len(doc['placements']),'documentary links')
if __name__=='__main__':main()
