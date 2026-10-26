#!/usr/bin/env python3
"""Idempotent BBC Reel addition; source notes in docs/research/regaleira-bbc.json."""
import json
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'data'
def load(f):return json.loads((D/f).read_text())
def save(f,x):(D/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
n='Quinta da Regaleira Initiation Well'
s=load('sites.json')
if not any(x['n']==n for x in s):
 s.append({'n':n,'lat':38.79453,'lng':-9.39691,'cat':'underground','region':'Europe','tier':3,'criteria':[],'desc':'Modern revival architecture, late 19th to early 20th century (estate construction programme: 1893–1920). The spiral Initiation Well and connected passages form part of Carvalho Monteiro and Luigi Manini’s symbolic landscape at Sintra. Its references to older traditions belong to this modern design. Featured film: BBC Reel, published 5 November 2019, by Fernando Teixeira and Izabela Cardosa.'})
 save('sites.json',s)
for f,v in [('countries.json','Portugal'),('civilizations.json','Modern Portuguese revival architecture'),('eras.json',1900),('tags.json','Sintra Quinta da Regaleira initiation well Poco Iniciatico modern revival architecture late nineteenth early twentieth century BBC Reel Fernando Teixeira Izabela Cardosa')]:
 x=load(f);x[n]=v;save(f,x)
v=load('videos.json');rows=v.setdefault(n,[])
if not any(x['id']=='0538DzrFonk' for x in rows):rows.append({'id':'0538DzrFonk','title':"Sintra's mysterious 'inverted tower' - BBC REEL",'cr':'bbcglobal','added':'2026-10-26','published':'2019-11-05'})
save('videos.json',v)
print('Regaleira added with date and BBC/filmmaker credits')
