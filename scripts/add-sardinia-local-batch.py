"""Add reviewed Sardinian site visits without replacing existing coverage."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
D=ROOT/'data'
def load(n): return json.loads((D/n).read_text())
def save(n,x): (D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    sites=load('sites.json'); creators=load('creators.json'); videos=load('videos.json'); countries=load('countries.json')
    meta={x['id']:x for x in json.loads((ROOT/'docs/research/sardinia-local-review-2026-10-23.json').read_text())}
    new_sites=[dict(n='Nuraghe Losa',lat=40.1169,lng=8.79007,cat='megalithic',region='Europe',tier=2,desc='A Bronze Age basalt nuraghe on the Abbasanta plateau. A central tower and three-lobed bastion contain corbelled chambers and passages; a surrounding wall encloses the remains of a settlement. Excavations began in the 1890s and revealed a long history of occupation.'),dict(n='Nuraghe Arrubiu',lat=39.661944,lng=9.2975,cat='megalithic',region='Europe',tier=2,desc='A large Bronze Age nuragic complex near Orroli, with a central tower enclosed by a five-tower bastion and additional outer defences. Courtyards and corbelled chambers survive among basalt walls coloured by reddish lichens. Excavated pottery records connections with the wider Mediterranean.')]
    for s in new_sites:
        if s['n'] not in {x['n'] for x in sites}: sites.append(s)
        countries[s['n']]='Italy'
    new_creators={
      'sardegnasacra':dict(name='Sardegna Sacra',handle='@sardegnasacra',subs='Ilaria Montis · archaeologist and guide working in Sardinia · Italian-language site visits',color='#92AC86',tier=2),
      'sardegnastorica':dict(name='Sardegna Storica',handle='@sardegnastorica6867',subs='Sardinian archaeology and heritage · visits and interviews with local specialists',color='#BC9874',tier=2),
      'sardegnaturistica':dict(name='Sardegna Turistica',handle='@sardegnaturistica9590',subs='Sardinian cultural heritage channel · on-site conversations with archaeologists',color='#83A6BB',tier=2),
      'marcomura':dict(name='Marco Mura',handle='@MarcoMura',subs='Travel filmmaker from Alghero · Italian-language visits in Sardinia and beyond',color='#B598BF',tier=3)}
    for k,v in new_creators.items(): creators.setdefault(k,v)
    placements={'44FzDVy6cxE':('Nuraghe Losa','sardegnastorica'),'aSUbwMSH5nI':('Nuraghe Arrubiu','sardegnasacra'),'3s1AS9qMLrQ':('Nuraghe Santu Antine','sardegnaturistica'),'qGzL-Kuzfpo':('Nuraghe Santu Antine','marcomura')}
    for ident,(site,cr) in placements.items():
        x=meta[ident];d=x['upload_date']
        if not any(v['id']==ident for v in videos.setdefault(site,[])):videos[site].append(dict(id=ident,title=x['title'],cr=cr,added='2026-10-23',published=f'{d[:4]}-{d[4:6]}-{d[6:]}'))
    for vs in videos.values():
        for v in vs:
            if v['id']=='q0YNkMIt3BY': v['title']=meta[v['id']]['title']
    for n,x in [('sites.json',sites),('creators.json',creators),('videos.json',videos),('countries.json',countries)]:save(n,x)
if __name__=='__main__':main()
