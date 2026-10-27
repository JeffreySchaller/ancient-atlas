#!/usr/bin/env python3
"""Idempotent shared navigation installation after page generation."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
count=0
for p in (root/'public').rglob('*.html'):
    if p.relative_to(root/'public').as_posix() in ['index.html','badge-preview.html','pattern-research.html']:continue
    s=p.read_text()
    bundle=re.search(r'(<script type="__bundler/template">)(.*?)(</script>)',s,re.S)
    if bundle:
        template=json.loads(bundle[2])
        if '/assets/js/site-navigation.js' not in template:
            template=template.replace('</head>','<link rel="stylesheet" href="/assets/site-navigation.css"></head>',1)
            template=template.replace('</body>','<script src="/assets/js/site-navigation.js"></script></body>',1)
            encoded=json.dumps(template).replace('</','<\\/')
            s=s[:bundle.start(2)]+encoded+s[bundle.end(2):]
            p.write_text(s)
    if '/assets/js/site-navigation.js' in s:continue
    if '</head>' not in s:continue
    s=s.replace('</head>','<link rel="stylesheet" href="/assets/site-navigation.css">\n<script defer src="/assets/js/site-navigation.js"></script>\n</head>',1)
    p.write_text(s);count+=1
print(f'Shared navigation installed on {count} pages')
