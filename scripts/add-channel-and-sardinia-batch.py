"""Idempotent 2026-10-23 catalog completion and first Sardinia evidence batch.
Sources and classification decisions: docs/research/ and CREATOR_DISCOVERY.md.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
D=ROOT/'data'
def load(name):return json.loads((D/name).read_text())
def save(name,obj):(D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    videos=load('videos.json');sites=load('sites.json');creators=load('creators.json');countries=load('countries.json');catalog=load('ancientatlas-channel.json');conversations=load('conversations.json')
    meta={x['id']:x for x in json.loads((ROOT/'docs/research/channel-review-2026-10-23.json').read_text())}
    # This film is explicitly described as part three of an interview, with site footage.
    # Keep it discoverable as a discussion, not as a standalone walked tour.
    videos['Dendera Temple Complex']=[x for x in videos['Dendera Temple Complex'] if x['id']!='sSxekluuFfc']
    paracas='Paracas Candelabra'
    if paracas not in {s['n'] for s in sites}:
        sites.append(dict(n=paracas,lat=-13.79454,lng=-76.30860,cat='geoglyph',region='South America',tier=2,signal='open',criteria=['scale'],desc='A branching geoglyph cut into the northern face of the Paracas Peninsula, visible from boats crossing Pisco Bay. Roughly 180 metres long, its deep grooves stand out against the desert slope. Its makers, date and purpose remain uncertain. Protected within the Paracas National Reserve.'))
    countries[paracas]='Peru'
    x=meta['zLU3OEQ23LM'];entry=dict(id=x['id'],title=x['title'],cr='ancientatlas',added='2026-10-23',published='2026-10-18')
    if not any(y['id']==x['id'] for y in videos.setdefault(paracas,[])):videos[paracas].append(entry)
    for vs in videos.values():
        for v in vs:
            if v.get('cr')=='ancientatlas' and v['id'] in meta:
                x=meta[v['id']];v['title']=x['title'];d=x['upload_date'];v['published']=f'{d[:4]}-{d[4:6]}-{d[6:]}'
    for c in conversations['conversations']:
        if c.get('episode')=='CC02':
            c.update(id='zqYJ_H1TYpM',title=meta['zqYJ_H1TYpM']['title'],published='2026-09-08',sites=[{'n':'Angkor Wat'},{'n':'Ta Keo'}],note='Published episode verified from the channel description and chapter list on 2026-10-23. Angkor Wat is the main subject; Ta Keo has a dedicated chapter at 23:15. Other passing references are not mapped.')
            c.pop('status',None);c.pop('recorded',None)
    museums={'zolCFgN1R2E','ecy2Lu_euOY','Mh40gYv9ChI'}
    discussions={'oKdXnR-uFW0','6r90XRNQtUA','XVeZ-xoUYCc','nIeos8fSbjk','sSxekluuFfc','wVtuI4CIIXY','0rwtMIIRmg8','zqYJ_H1TYpM','2OSddPnrShw'}
    for item in catalog['items']:
        ident=item['id'];mapped=[name for name,vs in videos.items() if any(v['id']==ident for v in vs)]
        item.pop('site',None);item['sites']=mapped
        if ident in meta:
            x=meta[ident];item['title']=x['title'];item['duration']=x['duration'];d=x['upload_date'];item['published']=f'{d[:4]}-{d[4:6]}-{d[6:]}'
        item['kind']='short' if item['format']=='short' else 'museum' if ident in museums else 'conversation' if ident in discussions else 'fieldwork'
        item['catalog_status']='mapped' if mapped else 'catalog_only'
        if item['kind']=='conversation':item['placement_note']='Conversation or commentary; kept separate from on-location walkthroughs.'
        elif item['kind']=='museum':item['placement_note']='Museum collection; available on the channel page without an ancient-site pin.'
        elif item['kind']=='short':item['placement_note']='Short-form channel discovery; no speculative site assignment.'
        if ident=='zLU3OEQ23LM':item['start']=57
        if ident=='zqYJ_H1TYpM':item['related_sites']=['Angkor Wat','Ta Keo']
    catalog['scope']='All public Videos and Shorts tabs checked 2026-10-23; channel has no public Streams tab.'
    credit_by_id={'oKdXnR-uFW0':'Ancient Atlas with Travis Robinson','6r90XRNQtUA':'Ancient Atlas · source explorations by Luzhou Abo (@luzhouabo)','zqYJ_H1TYpM':'Ancient Atlas with Solstice Hunter','2OSddPnrShw':'Ancient Atlas with Ageless Rock','i6ehCHkzf3Y':'Ancient Atlas with Brien Foerster and Jimmy Church','nPmq9Iz3XJc':'Ancient Atlas with Brien Foerster'}
    for item in catalog['items']:
        item['credit']=credit_by_id.get(item['id'],'Ancient Atlas with UnchartedX' if item['id'] in meta and 'UnchartedX' in meta[item['id']]['description'] else 'Ancient Atlas')
    sardinia=json.loads((ROOT/'docs/research/sardinia-review-2026-10-23.json').read_text())
    creators.setdefault('haswelltravelled',dict(name='Haswell Travelled',handle='@HaswellTravelled',subs='James Haswell · on-location travel films and archaeological site visits',color='#7D9D91',tier=3))
    placements={'FZRBwGtS_As':('Sacred Well of Sa Testa','megalithomania'),'KBu3J8v7kfU':('Sardinia Nuraghi (Su Nuraxi)','haswelltravelled'),'nGp-GWDv4B0':('San Andrea Priù','megalithomania')}
    for x in sardinia:
        site,cr=placements[x['id']];assert site in {s['n'] for s in sites};d=x['upload_date']
        if not any(y['id']==x['id'] for y in videos.setdefault(site,[])):
            videos[site].append(dict(id=x['id'],title=x['title'],cr=cr,added='2026-10-23',published=f'{d[:4]}-{d[4:6]}-{d[6:]}'))
    for file,obj in [('videos.json',videos),('sites.json',sites),('creators.json',creators),('countries.json',countries),('conversations.json',conversations),('ancientatlas-channel.json',catalog)]:save(file,obj)
if __name__=='__main__':main()
