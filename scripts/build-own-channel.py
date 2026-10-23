"""Build the Ancient Atlas public channel index from a reviewed metadata snapshot."""
import json
from html import escape
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def main():
    data = json.loads((ROOT / 'data/ancientatlas-channel.json').read_text())
    parts = []
    for kind, label in [('film', 'Films'), ('short', 'Shorts')]:
        cards = ''.join('<li><a href="' + escape(x['url'], quote=True) + '">' + escape(x['title']) + '</a></li>' for x in data['items'] if x['format'] == kind)
        parts.append('<section><h2>' + label + '</h2><ul>' + cards + '</ul></section>')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ancient Atlas films and Shorts | The Ancient Atlas</title><meta name="description" content="Films, conversations and Shorts from Ancient Atlas. Explore the places, meet the guests and watch on YouTube."><link rel="canonical" href="https://theancientatlas.com/creators/ancient-atlas"><style>body{margin:0;background:#11121a;color:#eee8dc;font:18px/1.6 Georgia,serif}main,nav{max-width:850px;margin:auto;padding:24px}a{color:#d8bb70}nav{display:flex;flex-wrap:wrap;gap:20px}h1{font-size:clamp(32px,6vw,54px);line-height:1.15}li{margin:0 0 16px}a:focus-visible{outline:3px solid #fff;outline-offset:5px}footer{margin:40px 0}small{color:#c8c2b6}</style></head><body><nav aria-label="Main"><a href="/">Map</a><a href="/sites/">Sites</a><a href="/creators/">All creators</a><a href="/library/">Library</a></nav><main><h1>Ancient Atlas on film</h1><p>Field visits, conversations and close looks at the places on the map.</p><p><a href="https://www.youtube.com/@AncientAtlasMap">Visit @AncientAtlasMap on YouTube</a></p><p>The Atlas brings many voices to each place. <a href="/creators/">Explore the other creators</a>, or choose a film below.</p>''' + ''.join(parts) + '<footer><small>Public Videos and Shorts catalog checked ' + escape(data['checked']) + '. Each title opens the original video on YouTube.</small></footer></main><script defer src="/assets/js/analytics.js"></script></body></html>'
    (ROOT / 'public/creators/ancient-atlas.html').write_text(page)

if __name__ == '__main__':
    main()
