"""Install complete social metadata for previously uncovered published pages."""
from pathlib import Path
import json,re,html
R=Path(__file__).resolve().parents[1]
for item in json.loads((R/'data/sharing-pages.json').read_text()):
 p=R/'public'/item['path'];s=p.read_text()
 url='https://theancientatlas.com/'+item['path'].replace('index.html','')
 title=item['title']+' — Ancient Atlas'
 image='https://theancientatlas.com/assets/social/'+item['image']+'-og.png?v=1'
 values={'og:type':'website','og:site_name':'Ancient Atlas','og:title':title,'og:description':item['description'],'og:url':url,'og:image':image,'og:image:width':'1200','og:image:height':'630','og:image:alt':item['title']+'. '+item['subtitle'],'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':item['description'],'twitter:image':image,'twitter:image:alt':item['title']+'. '+item['subtitle']}
 for key,value in values.items():
  s=re.sub(r'<meta\b(?=[^>]*(?:property|name)=[\"\x27]'+re.escape(key)+r'[\"\x27])[^>]*>\s*','',s,flags=re.I)
 tags='\n'.join('<meta '+('name' if k.startswith('twitter') else 'property')+'="'+k+'" content="'+html.escape(v,quote=True)+'">' for k,v in values.items())
 s=s.replace('</head>',tags+'\n</head>',1);p.write_text(s)
print('Installed sharing metadata for 6 pages')
